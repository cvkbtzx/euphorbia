# -*- coding:utf-8 -*-

##  EUPHORBIA - GTK LaTeX Editor
##  Copyright (C) 2008-2010   Bzoloid
##
##  This program is free software; you can redistribute it and/or
##  modify it under the terms of the GNU General Public License
##  as published by the Free Software Foundation; either version 2
##  of the License, or (at your option) any later version.
##
##  This program is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##  GNU General Public License for more details.
##
##  You should have received a copy of the GNU General Public License
##  along with this program; if not, write to the Free Software Foundation,
##  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.


"""Module with documents management classes."""

import gobject
import gtk
import pango
import gtksourceview2 as gtksv

import dialogs
import tabwrapper
import EuphorbiaEditor.utils.texparser as texparser

STYLEM = gtksv.style_scheme_manager_get_default()


#------------------------------------------------------------------------------

class Document(tabwrapper.TabWrapper):
    """Class for documents managing. Includes notebook tabs and edit zone."""
    
    def __init__(self, notebook, filename=None, hlight=None):
        hp = gtk.HPaned()
        tabwrapper.TabWrapper.__init__(self, notebook, hp)
        self.ev = EditView()
        hp.pack1(self.ev, True, False)
        filename = filename if filename else "New document"
        self.set_title(filename)
        self.icon.set_from_stock(gtk.STOCK_FILE, gtk.ICON_SIZE_MENU)
        self.datafile = {'file':filename, 'encoding':None, 'hlight':hlight}
        self.ev.set_language(hlight)
        self.clipb = gtk.clipboard_get()
        self.gen_doc_struct()
        self.ev.buffer.connect('modified-changed', self.ev_modified)
        self.button_close.connect('enter', lambda x: self.set_close_icon())
        self.button_close.connect('leave', lambda x: self.ev_modified())
    
    def set_file(self, f, enc=None, hl=None):
        """Change file."""
        if f.uri is not None or f.mime is not None:
            hlguess = self.ev.lang_manager.guess_language(f.uri, f.mime)
            hlguess = None if hlguess is None else hlguess.get_id()
        self.datafile['file'] = f
        self.datafile['encoding'] = enc if enc else 'utf-8'
        self.datafile['hlight'] = hl if hl else hlguess
        f.encoding = self.datafile['encoding']
        self.set_icon(*f.get_icons())
        name = f.get_name()
        if name:
            self.set_title(name)
        self.ev.set_language(self.datafile['hlight'])
        return
    
    def get_fname(self):
        """Get tab name."""
        f = self.datafile['file']
        return f if type(f) is str else f.get_name()
    
    def open_file(self, f, enc=None, hl=None):
        """Load given file as the document."""
        self.set_file(f, enc, hl)
        txt = f.read()
        self.ev.buffer.begin_not_undoable_action()
        self.ev.buffer.set_text("" if txt is None else txt)
        self.ev.buffer.place_cursor(self.ev.buffer.get_start_iter())
        self.ev.buffer.end_not_undoable_action()
        self.ev.buffer.set_modified(False)
        if txt is None:
            self.datafile['file'] = f.get_name()
        self.gen_doc_struct()
        return False if txt is None else True
    
    def save(self, f, backup=False):
        """Save the text data in a file."""
        if f is None:
            f = self.datafile['file']
        else:
            f.encoding = self.datafile['encoding']
        ibeg, iend = self.ev.buffer.get_bounds()
        txt = self.ev.buffer.get_text(ibeg, iend, False)
        ret = f.write(txt, backup)
        f.update_infos()
        self.gen_doc_struct()
        if ret:
            self.set_file(f,self.datafile['encoding'],self.datafile['hlight'])
            self.ev.buffer.set_modified(False)
        return ret
    
    def fileinfos(self):
        """Return infos (name, file, modified) about the file to save."""
        f = self.datafile['file']
        m = self.ev.buffer.get_modified()
        return (f,None,m) if type(f) is str else (f.get_name(),f,m)
    
    def connect_print_compositor(self, printop, prefm):
        """Connect document print compositor to PrintOperation."""
        compoz = gtksv.print_compositor_new_from_view(self.ev.view)
        # Compositor options from PrefsManager
        for m in ['1header','2footer']:
            s = prefm.get_pref('print_%s_separator' % (m))
            txt = prefm.get_pref('print_%s_text' % (m)).split('|')
            txt = [t.strip() for t in txt]
            if len(txt) == 3:
                fmt = tuple(self.get_fname() if t=="%f" else t for t in txt)
            else:
                fmt = ("", "", "")
            f = prefm.get_pref('print_%s_font' % (m))
            d = prefm.get_pref('print_%s' % (m))
            getattr(compoz, 'set_%s_format' % (m[1:]))(*((s,)+fmt))
            getattr(compoz, 'set_%s_font_name' % (m[1:]))(f)
            getattr(compoz, 'set_print_%s' % (m[1:]))(d)
        for i,m in enumerate(['top','left','right','bottom']):
            p, u = 'print_margin_%i%s' % (i+1, m), gtk.UNIT_POINTS
            getattr(compoz, 'set_%s_margin' % (m))(prefm.get_pref(p), u)
        compoz.set_line_numbers_font_name(prefm.get_pref('print_nlinesfont'))
        compoz.set_print_line_numbers(prefm.get_pref('print_nlinesinterval'))
        # ProntOperation events
        dp_cb = lambda op,ct,pn,cp: cp.draw_page(ct, pn)
        printop.connect('begin-print', self.ev_begin_print, compoz)
        printop.connect('draw-page', dp_cb, compoz)
        printop.set_job_name("Euphorbia: %s" % self.get_fname())
        return
    
    def ev_begin_print(self, printop, context, compoz):
        """Callback for 'begin-print' event."""
        while not compoz.paginate(context):
            pass
        printop.set_n_pages(compoz.get_n_pages())
        return
    
    def cut(self):
        """Cut text into clipboard."""
        tv = self.ev.view
        self.ev.buffer.cut_clipboard(self.clipb, tv.get_editable())
        return
    
    def undo(self):
        """Undo last action."""
        if self.ev.buffer.can_undo():
            self.ev.buffer.undo()
            self.ev.view.scroll_mark_onscreen(self.ev.buffer.get_insert())
        return
    
    def redo(self):
        """Redo last action."""
        if self.ev.buffer.can_redo():
            self.ev.buffer.redo()
            self.ev.view.scroll_mark_onscreen(self.ev.buffer.get_insert())
        return
    
    def copy(self):
        """Copy text into clipboard."""
        self.ev.buffer.copy_clipboard(self.clipb)
        return
    
    def paste(self):
        """Paste text from clipboard."""
        tv = self.ev.view
        self.ev.buffer.paste_clipboard(self.clipb, None, tv.get_editable())
        return
    
    def search(self, txt, case, dir, loop):
        """Search text in document."""
        buffer = self.ev.buffer
        flags = gtksv.SEARCH_TEXT_ONLY | gtksv.SEARCH_VISIBLE_ONLY
        if not case:
            flags = flags | gtksv.SEARCH_CASE_INSENSITIVE
        ibeg, iend = buffer.get_bounds()
        if dir > 0:
            iter = buffer.get_iter_at_mark(buffer.get_selection_bound())
            res = gtksv.iter_forward_search(iter, txt, flags, None)
            if res is None and loop:
                res = gtksv.iter_forward_search(ibeg, txt, flags, None)
        elif dir < 0:
            iter = buffer.get_iter_at_mark(buffer.get_insert())
            res = gtksv.iter_backward_search(iter, txt, flags, None)
            if res is None and loop:
                res = gtksv.iter_backward_search(iend, txt, flags, None)
        else:
            iter = buffer.get_iter_at_mark(buffer.get_insert())
            res = gtksv.iter_forward_search(iter, txt, flags, None)
            if res is None and loop:
                res = gtksv.iter_forward_search(ibeg, txt, flags, None)
        s = self.get_selection()
        low = lambda x: x.decode('utf8').lower().encode('utf8')
        if res is not None:
            buffer.select_range(*res)
            self.ev.view.scroll_to_mark(buffer.get_insert(), 0.25, True)
        elif loop or (txt!=s and case) or (low(txt)!=low(s) and not case):
            buffer.place_cursor(iter)
        return
    
    def insert(self, txt, select=False):
        """Insert text at cursor position, replacing the selection."""
        buffer = self.ev.buffer
        if buffer.get_has_selection():
            buffer.delete_selection(True, self.ev.view.get_editable())
        iter = buffer.get_iter_at_mark(buffer.get_insert())
        m1 = buffer.create_mark(None, iter, True)
        m2 = buffer.create_mark(None, iter, False)
        buffer.insert_at_cursor(txt)
        if select:
            i1 = buffer.get_iter_at_mark(m1)
            i2 = buffer.get_iter_at_mark(m2)
            buffer.select_range(i1, i2)
        buffer.delete_mark(m1)
        buffer.delete_mark(m2)
        return
    
    def insert2(self, txt1, txt2):
        """Insert text around selection."""
        buffer = self.ev.buffer
        if buffer.get_has_selection():
            ibeg, iend = buffer.get_selection_bounds()
            ibeg.order(iend)
        else:
            ibeg = buffer.get_iter_at_mark(buffer.get_insert())
            iend = ibeg.copy()
        m1 = buffer.create_mark(None, ibeg)
        m2 = buffer.create_mark(None, iend)
        buffer.insert(buffer.get_iter_at_mark(m1), txt1)
        buffer.insert(buffer.get_iter_at_mark(m2), txt2)
        iter = buffer.get_iter_at_mark(m2)
        buffer.delete_mark(m1)
        buffer.delete_mark(m2)
        buffer.place_cursor(iter)
        return
    
    def get_selection(self):
        """Get selected text."""
        if self.ev.buffer.get_has_selection():
            ibeg, iend = self.ev.buffer.get_selection_bounds()
            txt = self.ev.buffer.get_text(ibeg, iend, False)
        else:
            txt = None
        return txt
    
    def focus(self):
        """Set the focus to the tab."""
        self.ev.view.grab_focus()
        return
    
    def gen_doc_struct(self):
        """Generate document structure."""
        f = self.get_fname()
        ibeg, iend = self.ev.buffer.get_bounds()
        lp = texparser.LatexParser(self.ev.buffer.get_text(ibeg, iend, False))
        self.struct = [(f, None, lp.parse('struct'))]
        g = lp.parse('graphic')
        if len(g) > 0:
            self.struct.append((_("Graphics"), None, g))
        return
    
    def goto_index(self, index):
        """Go to the given position."""
        iter = self.ev.buffer.get_iter_at_line(index-1 if index>0 else 0)
        self.ev.view.scroll_to_iter(iter, 0, True, 0, 0)
        return
    
    def ev_modified(self, *data):
        """Callback executed when modification flag changes."""
        stock = 'save' if self.ev.buffer.get_modified() else 'close'
        self.set_close_icon(stock)
        return


#------------------------------------------------------------------------------

class EditView(gtk.ScrolledWindow):
    """Edit view for the document."""
    
    def __init__(self):
        gtk.ScrolledWindow.__init__(self)
        self.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        self.lang_manager = gtksv.language_manager_get_default()
        self.buffer = gtksv.Buffer()
        self.buffer.set_modified(False)
        self.buffer.set_highlight_syntax(True)
        self.view = gtksv.View(self.buffer)
        self.view.set_name('editview')
        self.view.set_font = self.set_font
        self.view.set_max_undo_levels = self.buffer.set_max_undo_levels
        self.view.set_highlight_matching_brackets = self.buffer.set_highlight_matching_brackets
        self.view.set_stylescheme = self.set_stylescheme
        self.add(self.view)
        self.show_all()
        gobject.timeout_add(250, self.view.grab_focus)
    
    def set_font(self, font):
        """Set font."""
        f = None if font is None else pango.FontDescription(font)
        self.view.modify_font(f)
        return
    
    def set_stylescheme(self, id):
        """Set style scheme."""
        self.buffer.set_style_scheme(STYLEM.get_scheme(id))
        return
    
    def set_language(self, id):
        """Set language."""
        if id is None:
            self.buffer.set_language(None)
        else:
            lang = self.lang_manager.get_language(id)
            self.buffer.set_language(lang)
        return


#------------------------------------------------------------------------------

if __name__ == '__main__':
    setattr(__builtins__, '_', str)
    win = gtk.Window()
    win.set_default_size(640, 480)
    win.set_position(gtk.WIN_POS_CENTER)
    win.connect('destroy', lambda w: gtk.main_quit())
    nb = gtk.Notebook()
    nb.set_show_tabs(True)
    nb.set_scrollable(True)
    nb.tab_list = set()
    nb.show()
    win.add(nb)
    Document(nb,"Hello")
    Document(nb)
    Document(nb,"Bye")
    for d in nb.tab_list:
        d.ev.view.set_show_line_marks(True)
        d.ev.view.set_show_line_numbers(True)
        d.ev.view.set_cursor_visible(True)
        d.ev.view.set_wrap_mode(gtk.WRAP_WORD)
        d.ev.view.set_highlight_current_line(True)
    win.show()
    gtk.main()


#------------------------------------------------------------------------------



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

STYLEM = gtksv.style_scheme_manager_get_default()


#------------------------------------------------------------------------------

class Document(tabwrapper.TabWrapper):
    """Class for documents managing. Includes notebook tabs and edit zone."""
    
    def __init__(self, notebook, filename=None, hlight=None):
        hp = gtk.HPaned()
        tabwrapper.TabWrapper.__init__(self, notebook, hp)
        self.ev = EditView()
        hp.pack1(self.ev, True, False)
        filename = filename if filename else _("New document")
        self.set_title(filename)
        self.icon.set_from_stock(gtk.STOCK_FILE, gtk.ICON_SIZE_MENU)
        self.datafile = {'file':filename, 'encoding':None, 'hlight':hlight}
        self.ev.set_language(hlight)
        self.clipb = gtk.clipboard_get()
        self.gen_doc_struct()
    
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
        self.ev.buffer.set_text("" if txt is None else txt)
        self.ev.buffer.place_cursor(self.ev.buffer.get_start_iter())
        self.ev.buffer.set_modified(False)
        self.gen_doc_struct()
        return
    
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
    
    def saveinfos(self):
        """Return infos about the file to save."""
        f = self.datafile['file']
        m = self.ev.buffer.get_modified()
        return (f,None,m) if type(f) is str else (None,f,m)
    
    def connect_print_compositor(self, printop, **opts):
        """Connect document print compositor to PrintOperation."""
        compoz = gtksv.print_compositor_new_from_view(self.ev.view)
        for k,v in opts:
            func = getattr(compoz, k)
            func(*v)
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
    
    def insert(self, txt):
        """Insert text in cursor position."""
        if self.ev.buffer.get_has_selection():
            self.ev.buffer.delete_selection(True, self.ev.view.get_editable())
        self.ev.buffer.insert_at_cursor(txt)
        return
    
    def search(self, txt, case_sensitive, dir, loop):
        """Search text in document."""
        flags = gtksv.SEARCH_TEXT_ONLY | gtksv.SEARCH_VISIBLE_ONLY
        if not case_sensitive:
            flags = flags | gtksv.SEARCH_CASE_INSENSITIVE
        ibeg, iend = self.ev.buffer.get_bounds()
        if dir > 0:
            iter = self.ev.buffer.get_iter_at_mark(self.ev.buffer.get_selection_bound())
            res = gtksv.iter_forward_search(iter, txt, flags, None)
            if res is None and loop:
                res = gtksv.iter_forward_search(ibeg, txt, flags, None)
        elif dir < 0:
            iter = self.ev.buffer.get_iter_at_mark(self.ev.buffer.get_insert())
            res = gtksv.iter_backward_search(iter, txt, flags, None)
            if res is None and loop:
                res = gtksv.iter_backward_search(iend, txt, flags, None)
        else:
            iter = self.ev.buffer.get_iter_at_mark(self.ev.buffer.get_insert())
            res = gtksv.iter_forward_search(iter, txt, flags, None)
            if res is None and loop:
                res = gtksv.iter_forward_search(ibeg, txt, flags, None)
        if res is not None:
            self.ev.buffer.select_range(*res)
            self.ev.view.scroll_to_mark(self.ev.buffer.get_insert(), 0, True)
        elif loop or txt != self.get_selection():
            self.ev.buffer.place_cursor(iter)
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
        self.struct = [(f, None, [])]
        for i,v in enumerate(["Hi!","Good morning","Hello"]):
            self.struct[0][2].append((v,i,[]))
        return
    
    def close(self, *data):
        """Close document."""
        if self.ev.buffer.get_modified():
            pwin = self.notebook.app.gui.win
            dwin = dialogs.MsgWin(pwin, 'question', 'yes_no', _("Save?"))
            ret = dwin.run()
            dwin.destroy()
            if ret == gtk.RESPONSE_YES:
                self.notebook.app.gui.act_save(tab=self)
        tabwrapper.TabWrapper.close(self, *data)
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

if __name__ == "__main__":
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
        d.close = tabwrapper.TabWrapper.close
        d.ev.view.set_show_line_marks(True)
        d.ev.view.set_show_line_numbers(True)
        d.ev.view.set_cursor_visible(True)
        d.ev.view.set_wrap_mode(gtk.WRAP_WORD)
        d.ev.view.set_highlight_current_line(True)
    win.show()
    gtk.main()


#------------------------------------------------------------------------------



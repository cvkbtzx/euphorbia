# -*- coding:utf-8 -*-

"""Module with tab and document management classes."""

import gobject
import pygtk
pygtk.require('2.0')
import gtk
import pango
import gtksourceview2 as gtksv

ICONTHEME = gtk.icon_theme_get_default()


#------------------------------------------------------------------------------

gtk.rc_parse_string ("""
style "euphorbia-tab-style" {
    GtkWidget::focus-padding = 0
    GtkWidget::focus-line-width = 0
    xthickness = 0
    ythickness = 0
}
widget "*-euphorbia-tab" style "euphorbia-tab-style"
""")


#------------------------------------------------------------------------------

class TabWrapper:
    """Wrapper for notebook tabs."""
    
    def __init__(self, notebook, child):
        # Tab name
        self.title = gtk.Label()
        self.title.set_alignment(0.0, 0.5)
        # Tab close button
        img = gtk.Image()
        img.set_from_stock(gtk.STOCK_CLOSE, gtk.ICON_SIZE_MENU)
        b_close = gtk.Button()
        b_close.set_relief(gtk.RELIEF_NONE)
        b_close.set_focus_on_click(False)
        b_close.connect('clicked', self.close)
        b_close.set_name("b" + str(hash(str(b_close))) + "-euphorbia-tab")
        b_close.add(img)
        # Tab icon
        self.icon = gtk.Image()
        # Packing
        hb = gtk.HBox(False, 5)
        hb.pack_start(self.icon, False, False)
        hb.pack_start(self.title, True, True)
        hb.pack_end(b_close, False, False)
        # Add the tab to the notebook
        self.content = child
        notebook.append_page(self.content, hb)
        notebook.set_tab_reorderable(self.content, True)
        notebook.set_current_page(notebook.page_num(self.content))
        notebook.tab_list.add(self)
        self.notebook = notebook
        # Display
        hb.show_all()
        self.content.show()
    
    def set_icon(self, *names):
        """Set icon from its name(s)."""
        for n in names:
            if ICONTHEME.has_icon(n):
                self.icon.set_from_icon_name(n, gtk.ICON_SIZE_MENU)
                return
        self.icon.set_from_stock(gtk.STOCK_FILE, gtk.ICON_SIZE_MENU)
        return
    
    def close(self, *data):
        """Close the tab."""
        self.notebook.tab_list.remove(self)
        self.notebook.remove_page(self.notebook.page_num(self.content))
        return


#------------------------------------------------------------------------------

class Document(TabWrapper):
    """Class for documents managing. Includes notebook tabs and edit zone."""
    
    def __init__(self, notebook, filename=None, highlight=None):
        self.ev = EditView()
        TabWrapper.__init__(self, notebook, self.ev)
        filename = filename if filename else "New document"
        self.title.set_text(filename)
        self.icon.set_from_stock(gtk.STOCK_FILE, gtk.ICON_SIZE_MENU)
        self.datafile = {'file':None, 'encoding':None, 'highlight':highlight}
        self.ev.set_language(highlight)
        self.clipb = gtk.clipboard_get()
    
    def set_file(self, f, enc=None, hl=None):
        """Change file."""
        if f.uri is not None or f.mime is not None:
            hlguess = self.ev.lang_manager.guess_language(f.uri, f.mime)
            hlguess = None if hlguess is None else hlguess.get_id()
        self.datafile['file'] = f
        self.datafile['encoding'] = enc if enc else 'utf-8'
        self.datafile['highlight'] = hl if hl else hlguess
        f.encoding = self.datafile['encoding']
        self.set_icon(*f.get_icons())
        name = f.gfile.get_basename()
        if name:
            self.title.set_text(name)
        self.ev.set_language(self.datafile['highlight'])
        self.ev.buffer.set_modified(False)
        return
    
    def open_file(self, f, enc=None, hl=None):
        """Load given file as the document."""
        self.set_file(f, enc, hl)
        txt = f.read()
        self.ev.buffer.set_text("" if txt is None else txt)
        self.ev.buffer.place_cursor(self.ev.buffer.get_start_iter())
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
    
    def search(self, txt, case_sensitive, dir, loop):
        """Search text in document."""
        flags = gtksv.SEARCH_TEXT_ONLY | gtksv.SEARCH_VISIBLE_ONLY
        if not case_sensitive:
            flags = flags | gtksv.SEARCH_CASE_INSENSITIVE
        ibegin, iend = self.ev.buffer.get_bounds()
        if dir > 0:
            iter = self.ev.buffer.get_iter_at_mark(self.ev.buffer.get_selection_bound())
            res = gtksv.iter_forward_search(iter, txt, flags, None)
            if res is None and loop:
                res = gtksv.iter_forward_search(ibegin, txt, flags, None)
        elif dir < 0:
            iter = self.ev.buffer.get_iter_at_mark(self.ev.buffer.get_insert())
            res = gtksv.iter_backward_search(iter, txt, flags, None)
            if res is None and loop:
                res = gtksv.iter_backward_search(iend, txt, flags, None)
        else:
            iter = self.ev.buffer.get_iter_at_mark(self.ev.buffer.get_insert())
            res = gtksv.iter_forward_search(iter, txt, flags, None)
            if res is None and loop:
                res = gtksv.iter_forward_search(ibegin, txt, flags, None)
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
        self.view.set_name("editview")
        self.view.set_font = self.set_font
        self.view.set_max_undo_levels = self.buffer.set_max_undo_levels
        self.view.set_highlight_matching_brackets = self.buffer.set_highlight_matching_brackets
        self.add(self.view)
        self.show_all()
        gobject.timeout_add(250, self.view.grab_focus)
    
    def set_font(self, font):
        """Set font."""
        f = None if font is None else pango.FontDescription(font)
        self.view.modify_font(f)
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



# -*- coding:utf-8 -*-

"""Module with tab and document management classes."""

import gobject
import pygtk
pygtk.require('2.0')
import gtk
import pango
import gtksourceview2 as gtksv


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
        b_close.connect('clicked', lambda w: self.ev_close_clicked(w))
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
    
    def ev_close_clicked(self, *data):
        self.close()
        return
    
    def close(self):
        self.notebook.tab_list.remove(self)
        self.notebook.remove_page(self.notebook.page_num(self.content))
        return


#------------------------------------------------------------------------------

class Document(TabWrapper):
    """Class for documents managing. Includes notebook tabs and edit zone."""
    
    def __init__(self, notebook, filename=None, filetype=None):
        self.ev = EditView()
        TabWrapper.__init__(self, notebook, self.ev)
        self.filename = filename if filename else "New document"
        self.title.set_text(self.filename)
        self.icon.set_from_stock(gtk.STOCK_FILE, gtk.ICON_SIZE_MENU)
        self.clipb = gtk.clipboard_get()
    
    def cut(self):
        """Cut text into clipboard."""
        tv = self.ev.view
        self.ev.buffer.cut_clipboard(self.clipb, tv.get_editable())
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
    
    def search(self):
        """Show/hide search toolbar."""
        if self.ev.searchbar.props.visible:
            self.ev.searchbar.hide()
        else:
            self.ev.searchbar.show()
        return


#------------------------------------------------------------------------------

class SearchBarEditView(gtk.VBox):
    """Search toolbar for EditView."""
    
    def __init__(self, buffer, view):
        gtk.VBox.__init__(self)
        self.buffer = buffer
        self.view = view
        sb = gtk.Toolbar()
        sb.set_name('toolbar_search')
        sb.set_style(gtk.TOOLBAR_BOTH_HORIZ)
        sb.set_icon_size(gtk.ICON_SIZE_SMALL_TOOLBAR)
        sb.set_tooltips(True)
        t = gtk.ToolItem()
        t.add(gtk.Label("Search:"))
        t.get_child().set_padding(5, 0)
        sb.insert(t, -1)
        t = gtk.ToolItem()
        t.set_expand(False)
        self.searchtxt = gtk.Entry()
        self.searchtxt.connect('changed', lambda w: self.ev_search(w, 0))
        t.add(self.searchtxt)
        sb.insert(t, -1)
        t = gtk.ToolButton(gtk.STOCK_GO_BACK)
        t.connect('clicked', lambda w: self.ev_search(w, -1))
        sb.insert(t, -1)
        t = gtk.ToolButton(gtk.STOCK_GO_FORWARD)
        t.connect('clicked', lambda w: self.ev_search(w, 1))
        sb.insert(t, -1)
        t = gtk.ToolItem()
        self.case = gtk.CheckButton("Case sensitive")
        self.case.set_focus_on_click(False)
        self.case.connect('toggled', lambda w: self.ev_search(w, 0))
        t.add(self.case)
        sb.insert(t, -1)
        t = gtk.ToolItem()
        t.add(gtk.Label())
        t.set_expand(True)
        sb.insert(t, -1)
        t = gtk.ToolButton(gtk.STOCK_CLOSE)
        t.connect('clicked', self.ev_search_close)
        sb.insert(t, -1)
        self.pack_start(gtk.HSeparator(), False, True)
        self.pack_start(sb, True, True)
        self.show_all()
        self.connect('show', self.ev_show)
    
    def ev_search(self, w, dir):
        """Callback search."""
        flags = gtksv.SEARCH_TEXT_ONLY | gtksv.SEARCH_VISIBLE_ONLY
        if not self.case.get_active():
            flags = flags | gtksv.SEARCH_CASE_INSENSITIVE
        txt = self.searchtxt.get_text()
        if dir > 0:
            iter = self.buffer.get_iter_at_mark(self.buffer.get_selection_bound())
            res = gtksv.iter_forward_search(iter, txt, flags, None)
        elif dir < 0:
            iter = self.buffer.get_iter_at_mark(self.buffer.get_insert())
            res = gtksv.iter_backward_search(iter, txt, flags, None)
        else:
            iter = self.buffer.get_iter_at_mark(self.buffer.get_insert())
            res = gtksv.iter_forward_search(iter, txt, flags, None)
        if res is not None:
            self.buffer.select_range(*res)
            self.view.scroll_to_mark(self.buffer.get_insert(), 0, True)
        return
    
    def ev_show(self, *data):
        """Callback for 'show' event."""
        self.searchtxt.grab_focus()
        return
    
    def ev_search_close(self, *data):
        """Callback search close."""
        self.hide()
        return


#------------------------------------------------------------------------------

class EditView(gtk.VBox):
    """Edit view for the document."""
    
    def __init__(self):
        gtk.VBox.__init__(self)
        scroll = gtk.ScrolledWindow()
        scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        self.buffer = gtksv.Buffer()
        self.lang_manager = gtksv.LanguageManager()
        self.lang = self.lang_manager.get_language('latex')
        self.buffer.set_language(self.lang)
        self.buffer.set_highlight_syntax(True)
        self.view = gtksv.View(self.buffer)
        self.view.set_name("editview")
        self.view.set_show_line_marks(True)
        self.view.set_show_line_numbers(True)
        self.view.set_cursor_visible(True)
        self.view.set_wrap_mode(gtk.WRAP_WORD)
        self.view.set_highlight_current_line(True)
        self.view.set_font = self.set_font
        scroll.add(self.view)
        self.pack_start(scroll, True, True)
        self.searchbar = SearchBarEditView(self.buffer, self.view)
        self.pack_start(self.searchbar, False, True)
        self.show_all()
        self.searchbar.hide()
        gobject.timeout_add(250, self.view.grab_focus)
    
    def set_font(self, font):
        """Set font."""
        f = None if font is None else pango.FontDescription(font)
        self.view.modify_font(f)
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
    win.show()
    gtk.main()


#------------------------------------------------------------------------------



# -*- coding:utf-8 -*-

"""Module with tab and document management classes."""

import gobject
import pygtk
pygtk.require('2.0')
import gtk
import pango
import gtksourceview2 as gtksv


#------------------------------------------------------------------------------

class SearchBar(gtk.Toolbar):
    """Search toolbar for EditView."""
    
    def __init__(self, app):
        gtk.Toolbar.__init__(self)
        self.app = app
        self.set_name('toolbar_search')
        t = gtk.ToolItem()
        t.add(gtk.Label("Search:"))
        t.get_child().set_padding(5, 0)
        self.insert(t, -1)
        t = gtk.ToolItem()
        t.set_expand(False)
        self.searchtxt = gtk.Entry()
        self.searchtxt.connect('changed', lambda w: self.ev_search(w, 0))
        t.add(self.searchtxt)
        self.insert(t, -1)
        t = gtk.ToolButton(gtk.STOCK_GO_BACK)
        t.connect('clicked', lambda w: self.ev_search(w, -1))
        self.insert(t, -1)
        t = gtk.ToolButton(gtk.STOCK_GO_FORWARD)
        t.connect('clicked', lambda w: self.ev_search(w, 1))
        self.insert(t, -1)
        t = gtk.ToolItem()
        self.case = gtk.CheckButton("Case sensitive")
        self.case.set_focus_on_click(False)
        self.case.connect('toggled', lambda w: self.ev_search(w, 0))
        t.add(self.case)
        self.insert(t, -1)
        t = gtk.ToolItem()
        t.add(gtk.Label())
        t.set_expand(True)
        self.insert(t, -1)
        t = gtk.ToolButton(gtk.STOCK_CLOSE)
        t.connect('clicked', self.ev_search_close)
        self.insert(t, -1)
        self.show_all()
        self.connect('show', self.ev_show)
    
    def ev_search(self, w, dir):
        """Callback search."""
        txt = self.searchtxt.get_text()
        tab = self.app.gui.get_current_tab()
        if txt == "" or tab is None:
            return
        loop = self.app.prefm.get_pref('search_loop')
        if hasattr(tab, 'search'):
            tab.search(txt, self.case.get_active(), dir, loop)
        return
    
    def ev_show(self, *data):
        """Callback for 'show' event."""
        tab = self.app.gui.get_current_tab()
        if hasattr(tab, 'get_selection'):
            txt = tab.get_selection()
            if txt is not None:
                if '\n' not in txt and '\t' not in txt and len(txt) < 32:
                    self.searchtxt.set_text(txt)
        self.searchtxt.grab_focus()
        self.ev_search(None, 0)
        return
    
    def ev_search_close(self, *data):
        """Callback search close."""
        self.hide()
        tab = self.app.gui.get_current_tab()
        if hasattr(tab, 'focus'):
            tab.focus()
        return


#------------------------------------------------------------------------------



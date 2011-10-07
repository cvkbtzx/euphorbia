#-*- coding:utf-8 -*-

##  EUPHORBIA - GTK LaTeX Editor
##  Module: EuphorbiaEditor.ui.searchbar
##  Copyright (C) 2008-2011   Bzoloid
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


"""Search toolbar."""

import gtk


#------------------------------------------------------------------------------

class SearchBar(gtk.Toolbar):
    """Search toolbar."""
    
    def __init__(self, app, accels):
        gtk.Toolbar.__init__(self)
        self.app = app
        self.set_name('toolbar_search')
        # Search entry
        t = gtk.ToolItem()
        t.set_expand(True)
        self.searchtxt = gtk.Entry()
        self.searchtxt.set_icon_from_stock(gtk.ENTRY_ICON_PRIMARY, gtk.STOCK_FIND)
        self.searchtxt.set_icon_activatable(gtk.ENTRY_ICON_PRIMARY, False)
        self.searchtxt.set_icon_from_stock(gtk.ENTRY_ICON_SECONDARY, gtk.STOCK_CLEAR)
        self.searchtxt.set_icon_activatable(gtk.ENTRY_ICON_SECONDARY, True)
        self.searchtxt.connect('changed', lambda w: self.ev_search(w, 0))
        self.searchtxt.connect('icon-release', self.ev_clear)
        t.add(self.searchtxt)
        self.insert(t, -1)
        # Search directions
        t = gtk.ToolButton(gtk.STOCK_GO_BACK)
        t.connect('clicked', lambda w: self.ev_search(w, -1))
        ak, am = gtk.accelerator_parse("<Shift>F3")
        t.add_accelerator('clicked', accels, ak, am, gtk.ACCEL_VISIBLE)
        self.insert(t, -1)
        t = gtk.ToolButton(gtk.STOCK_GO_FORWARD)
        t.connect('clicked', lambda w: self.ev_search(w, 1))
        ak, am = gtk.accelerator_parse("F3")
        t.add_accelerator('clicked', accels, ak, am, gtk.ACCEL_VISIBLE)
        self.insert(t, -1)
        # Case sensitivity button
        t = gtk.ToolItem()
        self.case = gtk.CheckButton(_("Case sensitive"))
        self.case.set_focus_on_click(False)
        self.case.connect('toggled', lambda w: self.ev_search(w, 0))
        t.add(self.case)
        self.insert(t, -1)
        # Space
        t = gtk.ToolItem()
        t.add(gtk.Label())
        t.set_expand(True)
        self.insert(t, -1)
        # Close button
        t = gtk.ToolButton(gtk.STOCK_CLOSE)
        t.connect('clicked', lambda w: self.hide())
        self.insert(t, -1)
        # Display
        self.show_all()
        self.hide()
        self.connect('show', self.ev_show)
        self.connect('hide', self.ev_hide)
    
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
    
    def ev_clear(self, *data):
        """Callback clear."""
        self.searchtxt.set_text("")
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
        return
    
    def ev_hide(self, *data):
        """Callback for 'hide' event."""
        tab = self.app.gui.get_current_tab()
        if hasattr(tab, 'focus'):
            tab.focus()
        return


#------------------------------------------------------------------------------



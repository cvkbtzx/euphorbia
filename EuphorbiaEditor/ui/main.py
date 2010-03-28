# -*- coding:utf-8 -*-

"""GUI constructor."""

import os.path
import pygtk
pygtk.require('2.0')
import gtk

import actions
import sidepanel
import document
import searchbar


#------------------------------------------------------------------------------

class EuphorbiaGUI(actions.ActionsManager):
    """Graphical User Interface."""
    
    def __init__(self, app):
        actions.ActionsManager.__init__(self, app)
        self.clipb = gtk.clipboard_get()
        self.build_interface()
        nb = self.builder.get_object('notebook_docs')
        nb.tab_list = set()
        self.win.show()
    
    def build_interface(self):
        """Build the graphical interface."""
        datadir = self.app.prefm.get_pref('system_datadir')
        # Widgets loading
        self.builder = gtk.Builder()
        self.builder.add_from_file(os.path.join(datadir, "main.glade"))
        self.builder.connect_signals(self)
        # Main window
        self.win = self.builder.get_object('window')
        self.win.set_transient_for(None)
        img, sizes = os.path.join(datadir,"euphorbia.svg"), [16,22,24,32,36,48,64]
        icons = (gtk.gdk.pixbuf_new_from_file_at_size(img,s,s) for s in sizes)
        self.win.set_icon_list(*icons)
        # Side panel
        hp = self.builder.get_object('hpaned')
        hp.get_child1().destroy()
        hp.pack1(sidepanel.SidePanel(), False, True)
        # UI Manager
        self.uim = gtk.UIManager()
        # Accels
        accg = self.uim.get_accel_group()
        self.win.add_accel_group(accg)
        # Actions (actions.ActionsManager.actgrp)
        self.uim.insert_action_group(self.actgrp, 0)
        # Interface
        self.uim.add_ui_from_file(os.path.join(datadir, "main-ui.xml"))
        menu = self.uim.get_widget("/menu_main")
        self.builder.get_object('vbox_main').pack_start(menu, False, True)
        self.builder.get_object('vbox_main').reorder_child(menu, 0)
        toolbar = self.uim.get_widget("/toolbar_main")
        self.builder.get_object('handlebox_main').add(toolbar)
        # Searchbar
        sb = searchbar.SearchBar(self.app, accg)
        self.builder.get_object('vbox_docs').pack_start(sb, False, True)
        self.searchb = sb
        return
    
    def get_widgets_by_name(self, wname, parent=None):
        """Get widget(s) instance(s) from name."""
        wlist = set()
        parent = parent if parent else self.win
        if hasattr(parent, 'name'):
            if parent.name == wname:
                wlist.add(parent)
        if hasattr(parent, 'get_children'):
            for c in parent.get_children():
                wlist.update(self.get_widgets_by_name(wname,c))
        return wlist
    
    def ev_hide_bottom(self, *data):
        """Callback hide bottom notebook."""
        self.builder.get_object('hbox_bottom').hide()
        return
    
    def ev_delete_event(self, *data):
        """Callback for 'delete_event' event."""
        print "'delete_event' event occurred"
        q = not self.do_quit()
        return q
    
    def ev_destroy(self, *data):
        """Callback for 'destroy' event."""
        print "'destroy' event occurred"
        gtk.main_quit()
    
    def main(self):
        """Main loop."""
        gtk.main()
        return 0


#------------------------------------------------------------------------------



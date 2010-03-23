# -*- coding:utf-8 -*-

"""GUI constructor."""

import pygtk
pygtk.require('2.0')
import gtk

import actions
import sidepanel
import document


#------------------------------------------------------------------------------

class EuphorbiaGUI(actions.ActionsManager):
    """Graphical User Interface."""
    
    def __init__(self, app):
        actions.ActionsManager.__init__(self, app)
        self.build_interface()
        self.clipb = gtk.clipboard_get()
        nb = self.builder.get_object('notebook_docs')
        nb.tab_list = set()
        document.Document(nb)
        self.win.set_transient_for(None)
        self.win.show()
    
    def build_interface(self):
        """Build the graphical interface."""
        # Widgets loading
        self.builder = gtk.Builder()
        self.builder.add_from_file("./ui/main.glade")
        self.builder.connect_signals(self)
        self.win = self.builder.get_object('window')
        # Other widgets
        hp = self.builder.get_object('hpaned')
        hp.get_child1().destroy()
        hp.pack1(sidepanel.SidePanel(), False, True)
        hp.set_position(215)
        # UI Manager
        self.uim = gtk.UIManager()
        # Accels
        self.win.add_accel_group(self.uim.get_accel_group())
        # Actions (actions.ActionsManager.actgrp)
        self.uim.insert_action_group(self.actgrp, 0)
        # Interface
        self.uim.add_ui_from_file("./ui/main-ui.xml")
        menu = self.uim.get_widget("/menu_main")
        self.builder.get_object('vbox_main').pack_start(menu, False, True)
        self.builder.get_object('vbox_main').reorder_child(menu, 0)
        toolbar = self.uim.get_widget("/toolbar_main")
        self.builder.get_object('handlebox_main').add(toolbar)
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



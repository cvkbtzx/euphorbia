# -*- coding:utf-8 -*-

import pygtk
pygtk.require('2.0')
import gtk

import actions
import sidepanel
import document


#------------------------------------------------------------------------------

class EuphorbiaGUI:
    """Graphical User Interface."""
    
    def __init__(self):
        self.build_interface()
        document.Document(self.builder.get_object('notebook_docs'))
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
        hp.set_position(175)
        # UI Manager
        self.uim = gtk.UIManager()
        # Accels
        self.win.add_accel_group(self.uim.get_accel_group())
        # Actions
        actg = gtk.ActionGroup('base')
        actg.add_actions(actions.get(self))
        self.uim.insert_action_group(actg, 0)
        # Interface
        self.uim.add_ui_from_file("./ui/main-ui.xml")
        menu = self.uim.get_widget("/menu_main")
        self.builder.get_object('vbox_main').pack_start(menu, False, True)
        self.builder.get_object('vbox_main').reorder_child(menu, 0)
        toolbar = self.uim.get_widget("/toolbar_main")
        ###toolbar.set_style(gtk.TOOLBAR_BOTH_HORIZ)
        ###toolbar.set_icon_size(gtk.ICON_SIZE_MENU)
        ###toolbar.set_tooltips(True)
        ###toolbar.set_show_arrow(True)
        self.builder.get_object('handlebox_main').add(toolbar)
        return
    
    def ev_quit(self, *data):
        ###self.save_conf()
        self.ev_destroy()
    
    def ev_delete_event(self, *data):
        """Callback for 'delete_event' event."""
        print "'delete_event' event occurred"
        ###self.save_conf()
        return False
    
    def ev_destroy(self, *data):
        """Callback for 'destroy' event."""
        print "'destroy' event occurred"
        gtk.main_quit()
    
    def main(self):
        """Main loop."""
        gtk.main()
        return 0


#------------------------------------------------------------------------------



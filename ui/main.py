# -*- coding:utf-8 -*-

import pygtk
pygtk.require('2.0')
import gtk

import sidepanel


#------------------------------------------------------------------------------

class EuphorbiaGUI:
    """Graphical User Interface."""
    
    def __init__(self):
        self.build_interface()
        self.win.set_transient_for(None)
        self.win.show()
        return
    
    def build_interface(self):
        """Build the graphical interface."""
        # Widgets loading
        self.builder = gtk.Builder()
        self.builder.add_from_file("./ui/main.glade")
        self.builder.connect_signals(self)
        self.win = self.builder.get_object('window')
        # Other widgets
        hp = self.builder.get_object('hpaned1')
        hp.get_child1().destroy()
        hp.pack1(sidepanel.SidePanel(), False, True)
        hp.set_position(175)
        # Manager
        self.uim = gtk.UIManager()
        self.win.add_accel_group(self.uim.get_accel_group())
        # Actions
        ag = gtk.ActionGroup('base')
        for w in self.builder.get_objects():
            if type(w) is gtk.Action:
                ag.add_action_with_accel(w, None)
        self.uim.insert_action_group(ag, 0)
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



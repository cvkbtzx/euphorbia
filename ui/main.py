# -*- coding:utf-8 -*-

import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade

import sidepanel


#------------------------------------------------------------------------------

class EuphorbiaGUI:
    """Graphical User Interface."""
    
    def __init__(self):
        self.build_interface()
        self['window'].show()
        return
    
    def build_interface(self):
        """Build the graphical interface."""
        # Glade widgets loading
        self.widgets = gtk.glade.XML("./ui/main.glade", 'window')
        events = {
            'on_window_delete_event':   self.ev_delete,
            'on_window_destroy':        self.ev_destroy
        }
        self.widgets.signal_autoconnect(events)
        # Other widgets
        self['hpaned1'].get_child1().destroy()
        self['hpaned1'].pack1(sidepanel.SidePanel(), False, True)
        self['hpaned1'].set_position(175)
        self['window'].set_transient_for(None)
        return
    
    def ev_delete(self, widget=None, event=None, data=None):
        """Callback for 'delete_event' event."""
        print "'delete_event' event occurred"
        ###self.save_conf()
        return False
    
    def ev_destroy(self, widget=None, data=None):
        """Callback for 'destroy' event."""
        print "'destroy' event occurred"
        gtk.main_quit()
    
    def main(self):
        """Main loop."""
        gtk.main()
        return 0
    
    def __getitem__(self, key):
        """Get a widget by calling: self['widget_name']."""
        return self.widgets.get_widget(key)


#------------------------------------------------------------------------------



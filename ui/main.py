# -*- coding:utf-8 -*-

"""GUI constructor."""

import pygtk
pygtk.require('2.0')
import gtk

import actions
import sidepanel
import document


#------------------------------------------------------------------------------

class EuphorbiaGUI:
    """Graphical User Interface."""
    
    def __init__(self, app):
        self.app = app
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
        hp.set_position(215)
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
    
    def quit(self):
        """Ensure the application quits correctly."""
        self.app.plugm.stop_all_plugins()
        return True
    
    def ev_quit(self, *data):
        """Callback for 'Quit' action."""
        q = self.quit()
        if q:
            self.ev_destroy()
        return
    
    def ev_delete_event(self, *data):
        """Callback for 'delete_event' event."""
        print "'delete_event' event occurred"
        q = not self.quit()
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



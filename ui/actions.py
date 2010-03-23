# -*- coding:utf-8 -*-

"""Definition of default actions."""

import gtk
import dialogs


#------------------------------------------------------------------------------

def get_actions_list(cls):
    """Get actions with appropriate callbacks from specified class."""
    actions = [
        # Name, Stock, Label, Accelerator, Tooltip, Callback
        ('menu_file',     None,                  "File"),
        ('action_newdoc', gtk.STOCK_NEW,         None, None, None, None),
        ('action_open',   gtk.STOCK_OPEN,        None, None, None, None),
        ('action_save',   gtk.STOCK_SAVE,        None, None, None, None),
        ('action_saveas', gtk.STOCK_SAVE_AS,     None, None, None, None),
        ('action_quit',   gtk.STOCK_QUIT,        None, None, None, cls.act_quit),
        ('menu_edit',     None,                  "Edit"),
        ('action_cut',    gtk.STOCK_CUT,         None, None, None, None),
        ('action_copy',   gtk.STOCK_COPY,        None, None, None, None),
        ('action_paste',  gtk.STOCK_PASTE,       None, None, None, None),
        ('menu_view',     None,                  "View"),
        ('menu_settings', None,                  "Settings"),
        ('action_prefs',  gtk.STOCK_PREFERENCES, None, None, None, cls.act_prefs),
        ('menu_help',     None,                  "Help"),
        ('action_about',  gtk.STOCK_ABOUT,       None, None, None, None)
    ]
    return actions


#------------------------------------------------------------------------------

class ActionsManager:
    """Class containing actions callbacks."""
    
    def __init__(self, app):
        self.app = app
        self.actgrp = gtk.ActionGroup('base')
        self.actgrp.add_actions(get_actions_list(self))
    
    def act_prefs(self, *data):
        """Callback for 'Preferences' action."""
        dwin = dialogs.PrefsWin(self.app)
        dwin.run()
        dwin.destroy()
        return
    
    def act_quit(self, *data):
        """Callback for 'Quit' action."""
        q = self.do_quit()
        if q:
            self.ev_destroy()
        return
    
    # * * *
    
    def do_quit(self):
        """Ensure that the application quits correctly."""
        self.app.plugm.stop_all_plugins()
        return True


#------------------------------------------------------------------------------


# -*- coding:utf-8 -*-

"""Definition of default actions."""

import gtk


#------------------------------------------------------------------------------

def get(cls):
    """Get actions with appropriate callbacks from specified class."""
    actions = [
        # Name, Stock, Label, Accelerator, Tooltip, Callback
        ('menu_file',     None,              "File"),
        ('action_newdoc', gtk.STOCK_NEW,     None, None, None, None),
        ('action_open',   gtk.STOCK_OPEN,    None, None, None, None),
        ('action_save',   gtk.STOCK_SAVE,    None, None, None, None),
        ('action_saveas', gtk.STOCK_SAVE_AS, None, None, None, None),
        ('action_quit',   gtk.STOCK_QUIT,    None, None, None, cls.ev_quit),
        ('menu_edit',     None,              "Edit"),
        ('action_cut',    gtk.STOCK_CUT,     None, None, None, None),
        ('action_copy',   gtk.STOCK_COPY,    None, None, None, None),
        ('action_paste',  gtk.STOCK_PASTE,   None, None, None, None),
        ('menu_display',  None,              "Display"),
        ('menu_help',     None,              "Help"),
        ('action_about',  gtk.STOCK_ABOUT,   None, None, None, None)
    ]
    return actions


#------------------------------------------------------------------------------



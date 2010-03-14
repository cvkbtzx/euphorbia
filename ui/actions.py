# -*- coding:utf-8 -*-

import gtk

def get(cls):
    """Get actions with appropriate callbacks from specified class."""
    actions = [
        ('FileMenu',     None,              "File"),
        ('NewdocAction', gtk.STOCK_NEW,     None, None, None, None),
        ('OpenAction',   gtk.STOCK_OPEN,    None, None, None, None),
        ('SaveAction',   gtk.STOCK_SAVE,    None, None, None, None),
        ('SaveasAction', gtk.STOCK_SAVE_AS, None, None, None, None),
        ('QuitAction',   gtk.STOCK_QUIT,    None, None, None, cls.ev_quit),
        ('EditMenu',     None,              "Edit"),
        ('CutAction',    gtk.STOCK_CUT,     None, None, None, None),
        ('CopyAction',   gtk.STOCK_COPY,    None, None, None, None),
        ('PasteAction',  gtk.STOCK_PASTE,   None, None, None, None),
        ('DisplayMenu',  None,              "Display"),
        ('HelpMenu',     None,              "Help"),
        ('AboutAction',  gtk.STOCK_ABOUT,   None, None, None, None)
    ]
    return actions



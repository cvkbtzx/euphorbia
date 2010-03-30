# -*- coding:utf-8 -*-

"""Definition of default actions."""

import gtk

import dialogs
import document
import EuphorbiaEditor.utils.iofiles as iofiles


#------------------------------------------------------------------------------

def get_actions_list(cls):
    """Get actions with appropriate callbacks from specified class."""
    actions = [
        # Name, Stock, Label, Accelerator, Tooltip, Callback
        ('menu_file',     None,                  _("File")),
        ('action_newdoc', gtk.STOCK_NEW,         None, None, None, cls.act_new),
        ('action_open',   gtk.STOCK_OPEN,        None, None, None, cls.act_open),
        ('action_save',   gtk.STOCK_SAVE,        None, None, None, None),
        ('action_saveas', gtk.STOCK_SAVE_AS,     None, None, None, None),
        ('action_close',  gtk.STOCK_CLOSE,       None, None, None, cls.act_close),
        ('action_quit',   gtk.STOCK_QUIT,        None, None, None, cls.act_quit),
        ('menu_edit',     None,                  _("Edit")),
        ('action_undo',   gtk.STOCK_UNDO,        None, None, None, cls.act_undo),
        ('action_redo',   gtk.STOCK_REDO,        None, None, None, cls.act_redo),
        ('action_cut',    gtk.STOCK_CUT,         None, '',   None, cls.act_cut),
        ('action_copy',   gtk.STOCK_COPY,        None, '',   None, cls.act_copy),
        ('action_paste',  gtk.STOCK_PASTE,       None, '',   None, cls.act_paste),
        ('action_search', gtk.STOCK_FIND,        None, None, None, cls.act_search),
        ('menu_view',     None,                  _("View")),
        ('menu_settings', None,                  _("Settings")),
        ('action_prefs',  gtk.STOCK_PREFERENCES, None, None, None, cls.act_prefs),
        ('menu_help',     None,                  _("Help")),
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
    
    def act_new(self, *data):
        """Callback for 'New' action."""
        self.do_open(None, hl='latex')
        return
    
    def act_open(self, *data):
        """Callback for 'Open' action."""
        dwin = dialogs.OpenWin(self.app)
        resp = dwin.run()
        uris = dwin.get_uris() if resp == gtk.RESPONSE_OK else []
        code = dwin.get_extra_widget().get_children()[1].get_active_text()
        dwin.destroy()
        for u in uris:
            self.do_open(u, enc=code)
        return
    
    def act_close(self, *data):
        """Callback for 'Close' action."""
        tab = self.get_current_tab()
        if hasattr(tab, 'close'):
            tab.close()
        return
    
    def act_undo(self, *data):
        """Callback for 'Undo' action."""
        tab = self.get_current_tab()
        if hasattr(tab, 'undo'):
            tab.undo()
        return
    
    def act_redo(self, *data):
        """Callback for 'Redo' action."""
        tab = self.get_current_tab()
        if hasattr(tab, 'redo'):
            tab.redo()
        return
    
    def act_cut(self, *data):
        """Callback for 'Cut' action."""
        tab = self.get_current_tab()
        if hasattr(tab, 'cut'):
            tab.cut()
        return
    
    def act_copy(self, *data):
        """Callback for 'Copy' action."""
        tab = self.get_current_tab()
        if hasattr(tab, 'copy'):
            tab.copy()
        return
    
    def act_paste(self, *data):
        """Callback for 'Paste' action."""
        tab = self.get_current_tab()
        if hasattr(tab, 'paste'):
            tab.paste()
        return
    
    def act_search(self, *data):
        """Callback for 'Search' action."""
        if self.searchb.props.visible:
            self.searchb.hide()
        else:
            self.searchb.show()
        return
    
    def act_quit(self, *data):
        """Callback for 'Quit' action."""
        q = self.do_quit()
        if q:
            self.ev_destroy()
        return
    
    # * * *
    
    def get_current_tab(self):
        """Get the current tab object (TabWrapper subclass)."""
        nb = self.app.gui.get_widgets_by_name('notebook_docs').pop()
        obj = nb.get_nth_page(nb.get_current_page())
        tab = [t for t in nb.tab_list if t.content is obj]
        return tab[0] if len(tab)==1 else None
    
    def do_open(self, filename, enc=None, hl=None):
        """Open file in new tab."""
        nb = self.app.gui.get_widgets_by_name('notebook_docs').pop()
        d = document.Document(nb, highlight=hl)
        self.app.prefm.autoconnect_gtk(d.ev)
        if filename is not None:
            f = iofiles.FileManager(filename, enc)
            f.update_infos()
            d.open_file(f, enc, hl)
        return
    
    def do_quit(self):
        """Ensure that the application quits correctly."""
        self.app.plugm.stop_all_plugins()
        return True


#------------------------------------------------------------------------------


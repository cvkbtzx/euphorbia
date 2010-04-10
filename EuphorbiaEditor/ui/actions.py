# -*- coding:utf-8 -*-

##  EUPHORBIA - GTK LaTeX Editor
##  Copyright (C) 2008-2010   Bzoloid
##
##  This program is free software; you can redistribute it and/or
##  modify it under the terms of the GNU General Public License
##  as published by the Free Software Foundation; either version 2
##  of the License, or (at your option) any later version.
##
##  This program is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##  GNU General Public License for more details.
##
##  You should have received a copy of the GNU General Public License
##  along with this program; if not, write to the Free Software Foundation,
##  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.


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
        ('action_save',   gtk.STOCK_SAVE,        None, None, None, cls.act_save),
        ('action_saveas', gtk.STOCK_SAVE_AS,     None, None, None, cls.act_saveas),
        ('action_page',   gtk.STOCK_PAGE_SETUP,  None, None, None, cls.act_page),
        ('action_print',  gtk.STOCK_PRINT,       None, None, None, cls.act_print),
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
        ('menu_tools',    None,                  _("Tools")),
        ('menu_settings', None,                  _("Settings")),
        ('action_prefs',  gtk.STOCK_PREFERENCES, None, None, None, cls.act_prefs),
        ('menu_help',     None,                  _("Help")),
        ('action_about',  gtk.STOCK_ABOUT,       None, None, None, cls.act_about)
    ]
    return actions


def get_toggle_actions_list(cls):
    """Get toggle actions with appropriate callbacks from specified class."""
    actions = [
        # Name, Stock, Label, Accelerator, Tooltip, Callback, Active
        ('action_showsidepan',   None, _("ShowSidePan"),   None, None, cls.act_showsidepan),
        ('action_showbottompan', None, _("ShowBottomPan"), None, None, cls.act_showbottompan),
    ]
    return actions


#------------------------------------------------------------------------------

class ActionsManager:
    """Class containing actions callbacks."""
    
    def __init__(self, app):
        self.app = app
        self.actgrp = gtk.ActionGroup('base')
        self.actgrp.add_actions(get_actions_list(self))
        self.actgrp.add_toggle_actions(get_toggle_actions_list(self))
    
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
    
    def act_save(self, *data):
        """Callback for 'Save' action."""
        tab = self.get_current_tab()
        if hasattr(tab, 'save') and hasattr(tab, 'saveinfos'):
            if tab.saveinfos()[1] is None:
                self.act_saveas()
            else:
                tab.save(None, self.app.prefm.get_pref('files_backup'))
        return
    
    def act_saveas(self, *data):
        """Callback for 'Save as' action."""
        tab = self.get_current_tab()
        if hasattr(tab, 'save') and hasattr(tab, 'saveinfos'):
            infos = tab.saveinfos()
            dwin = dialogs.SaveWin(self.app, *infos[:2])
            resp = dwin.run()
            uri = dwin.get_uri() if resp == gtk.RESPONSE_OK else None
            dwin.destroy()
            if uri is not None:
                f = iofiles.FileManager(uri)
                f.update_infos()
                tab.save(f, self.app.prefm.get_pref('files_backup'))
        return
    
    def act_page(self, *data):
        """Setup page."""
        pwin = self.app.gui.win
        f = gtk.print_run_page_setup_dialog
        self.print_setup = f(pwin, self.print_setup, self.print_settings)
        return
    
    def act_print(self, *data):
        """Callback for 'Print' action."""
        pwin = self.app.gui.win
        tab = self.get_current_tab()
        if not hasattr(tab, 'connect_print_compositor'):
            return
        printop = gtk.PrintOperation()
        printop.set_print_settings(self.print_settings)
        printop.set_default_page_setup(self.print_setup)
        tab.connect_print_compositor(printop)
        res = printop.run(gtk.PRINT_OPERATION_ACTION_PRINT_DIALOG, pwin)
        if res == gtk.PRINT_OPERATION_RESULT_ERROR:
            dwin = dialogs.MsgWin(self.app, 'error', 'close', _("PrintError"))
            dwin.run()
            dwin.destroy()
        elif res == gtk.PRINT_OPERATION_RESULT_APPLY:
            self.print_settings = printop.get_print_settings()
            print "File printed"
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
    
    def act_showsidepan(self, *data):
        """Callback for 'Show sidepanel' action."""
        p = self.app.prefm.get_pref('gui_sidepanelshow')
        self.do_showpanel(not p, 'side')
        return
    
    def act_showbottompan(self, *data):
        """Callback for 'Show bottompanel' action."""
        p = self.app.prefm.get_pref('gui_bottompanelshow')
        self.do_showpanel(not p, 'bottom')
        return
    
    def act_about(self, *data):
        """Callback for 'About' action."""
        dwin = dialogs.AboutWin(self.app)
        dwin.run()
        dwin.destroy()
        return
    
    def do_showsidepanel(self, visible):
        """Show sidepanel."""
        self.do_showpanel(visible, 'side')
        return
    
    def do_showbottompanel(self, visible):
        """Show bottompanel."""
        self.do_showpanel(visible, 'bottom')
        return
    
    def do_showpanel(self, visible, panel):
        """Show specified panel."""
        self.app.prefm.set_pref('gui_'+panel+'panelshow', visible)
        path = "/menu_main/menu_view/action_show"+panel+"pan"
        a = self.app.gui.uim.get_action(path)
        for p in a.get_proxies():
            a.block_activate_from(p)
            p.set_active(visible)
            a.unblock_activate_from(p)
        w = self.app.gui.get_widgets_by_name(panel+'panel').pop()
        func = w.show if visible else w.hide
        func()
        return
    
    def do_open(self, filename, enc=None, hl=None):
        """Open file in new tab."""
        nb = self.app.gui.get_widgets_by_name('notebook_docs').pop()
        d = document.Document(nb, hlight=hl)
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



#-*- coding:utf-8 -*-

##  EUPHORBIA - GTK LaTeX Editor
##  Module: EuphorbiaEditor.ui.actions
##  Copyright (C) 2008-2011   Bzoloid
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

from . import dialogs
from . import document
from ..utils import iofiles


#------------------------------------------------------------------------------

def get_actions_list(cls):
    """Get actions with appropriate callbacks from specified class."""
    actions = [
        # Name, Stock, Label, Accelerator, Tooltip, Callback
        ('action_file',     None,                   _("File")),
        ('action_newdoc',   gtk.STOCK_NEW,          None, None, None, cls.act_new),
        ('action_open',     gtk.STOCK_OPEN,         None, None, None, cls.act_open),
        ('action_save',     gtk.STOCK_SAVE,         None, None, None, cls.act_save),
        ('action_saveas',   gtk.STOCK_SAVE_AS,      None, None, None, cls.act_saveas),
        ('action_page',     gtk.STOCK_PAGE_SETUP,   None, None, None, cls.act_page),
        ('action_print',    gtk.STOCK_PRINT,        None, None, None, cls.act_print),
        ('action_prefs',    gtk.STOCK_PREFERENCES,  None, None, None, cls.act_prefs),
        ('action_close',    gtk.STOCK_CLOSE,        None, None, None, cls.act_close),
        ('action_quit',     gtk.STOCK_QUIT,         None, None, None, cls.act_quit),
        ('action_edit',     None,                   _("Edit")),
        ('action_undo',     gtk.STOCK_UNDO,         None, None, None, cls.act_undo),
        ('action_redo',     gtk.STOCK_REDO,         None, None, None, cls.act_redo),
        ('action_cut',      gtk.STOCK_CUT,          None, '',   None, cls.act_cut),
        ('action_copy',     gtk.STOCK_COPY,         None, '',   None, cls.act_copy),
        ('action_paste',    gtk.STOCK_PASTE,        None, '',   None, cls.act_paste),
        ('action_mark',     None,                   _("Mark"), '<Ctrl>F2', None, cls.act_mark),
        ('action_gomark',   None,                   _("GoMark"), 'F2', None, cls.act_gomark),
        ('action_search',   gtk.STOCK_FIND,         None, None, None, cls.act_search),
        ('action_view',     None,                   _("View")),
        ('action_hlight',   gtk.STOCK_SELECT_COLOR, _("Syntax highlighting")),
        ('action_hlauto',   None,                   _("Auto"),  None, None, cls.act_hlight),
        ('action_hllatex',  None,                   _("LaTeX"), None, None, cls.act_hlight),
        ('action_hlnone',   None,                   _("None"),  None, None, cls.act_hlight),
        ('action_project',  None,                   _("Project")),
        ('action_newproj',  gtk.STOCK_NEW,          None, '',   None, cls.act_newproj),
        ('action_openproj', gtk.STOCK_OPEN,         None, '',   None, cls.act_open),
        ('action_tools',    None,                   _("Tools")),
        ('action_help',     None,                   _("Help")),
        ('action_about',    gtk.STOCK_ABOUT,        None, None, None, cls.act_about)
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

class ActionsManager(object):
    """Class containing actions callbacks."""
    
    def __init__(self, app):
        self.app = app
        self.actgrp = gtk.ActionGroup('euphorbia')
        self.actgrp.add_actions(get_actions_list(self))
        self.actgrp.add_toggle_actions(get_toggle_actions_list(self))
        self.newdoccount = 0
    
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
    def act_new(self, *data):
        """Callback for 'New' action."""
        self.newdoccount += 1
        n = _("New_doc_%i.tex") % (self.newdoccount)
        self.do_open(None, 'latex', fname=n)
        return
    
    def act_open(self, *data, **args):
        """Callback for 'Open' action."""
        actions = {'action_open':'latex', 'action_openproj':'project'}
        h = actions.get(data[0].get_name(), 'all') if len(data)>0 else 'all'
        tab, folder = self.get_current_tab(), None
        if tab is not None:
            if tab.get_file_infos()[1] is not None:
                folder = tab.get_file_infos()[1].gfile.get_parent().get_uri()
        dwin = dialogs.OpenWin(self.app, folder, h)
        resp = dwin.run()
        uris = dwin.get_uris() if resp == gtk.RESPONSE_OK else []
        code = dwin.get_extra_widget().get_children()[1].get_active_text()
        filter = dwin.get_filter_name()
        dwin.destroy()
        do_open = args.get('do_open', True)
        if do_open:
            for u in uris:
                self.do_open(u, filter, enc=code)
        return None if do_open else uris
    
    def act_save(self, *data, **args):
        """Callback for 'Save' action."""
        tab = args['tab'] if 'tab' in args else self.get_current_tab()
        if hasattr(tab, 'save'):
            if tab.get_file_infos()[1] is None:
                self.act_saveas(**args)
            else:
                if tab.save(None, self.app.prefm.get_pref('files_backup')):
                    self.emit('save', tab)
        return
    
    def act_saveas(self, *data, **args):
        """Callback for 'Save as' action."""
        tab = args['tab'] if 'tab' in args else self.get_current_tab()
        if hasattr(tab, 'save'):
            infos = tab.get_file_infos()
            dwin = dialogs.SaveWin(self.app, *infos[:2])
            resp = dwin.run()
            uri = dwin.get_uri() if resp == gtk.RESPONSE_OK else None
            dwin.destroy()
            if uri is not None:
                f = iofiles.FileManager(uri)
                f.update_infos()
                if tab.save(f, self.app.prefm.get_pref('files_backup')):
                    self.emit('save', tab)
        return
    
    def act_page(self, *data):
        """Setup page."""
        f = gtk.print_run_page_setup_dialog
        self.print_setup = f(self.win, self.print_setup, self.print_settings)
        return
    
    def act_print(self, *data):
        """Callback for 'Print' action."""
        tab = self.get_current_tab()
        if not hasattr(tab, 'connect_print_compositor'):
            return
        printop = gtk.PrintOperation()
        printop.set_default_page_setup(self.print_setup)
        printop.set_print_settings(self.print_settings)
        tab.connect_print_compositor(printop)
        pst = lambda x: self.status_msg(_("Print: %s") % (x), 'print')
        printop.connect('status-changed', lambda p: pst(p.get_status_string()))
        res = printop.run(gtk.PRINT_OPERATION_ACTION_PRINT_DIALOG, self.win)
        if res == gtk.PRINT_OPERATION_RESULT_ERROR:
            self.popup_msg('error', 'close', _("PrintError"))
        elif res == gtk.PRINT_OPERATION_RESULT_APPLY:
            self.print_settings = printop.get_print_settings()
        return
    
    def act_prefs(self, *data):
        """Callback for 'Preferences' action."""
        dwin = dialogs.PrefsWin(self.app)
        dwin.run()
        dwin.destroy()
        pluglist = self.app.plugm.list_loaded_plugins()
        self.app.prefm.set_pref('plugins_list', pluglist)
        self.app.prefm.store()
        return
    
    def act_close(self, *data, **args):
        """Callback for 'Close' action."""
        tab = args['tab'] if 'tab' in args else self.get_current_tab()
        if tab is None:
            return
        asksave = self.do_ask_save([tab])
        if asksave is not None:
            if tab in asksave:
                self.act_save(**{'tab':tab})
            tab.close()
            self.emit('close')
        return
    
    def act_quit(self, *data):
        """Callback for 'Quit' action."""
        tabs = list(self.nbd.tab_list)
        asksave = self.do_ask_save(tabs)
        if asksave is not None:
            for t in asksave:
                self.act_save(**{'tab':t})
            self.do_quit()
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
    
    def act_mark(self, *data):
        """Callback for 'Mark' action."""
        tab = self.get_current_tab()
        if hasattr(tab, 'toggle_mark'):
            tab.toggle_mark()
        return
    
    def act_gomark(self, *data):
        """Callback for 'GoMark' action."""
        tab = self.get_current_tab()
        if hasattr(tab, 'goto_next_mark'):
            tab.goto_next_mark()
        return
    
    def act_search(self, *data):
        """Callback for 'Search' action."""
        if self.searchb.props.visible:
            self.searchb.hide()
        else:
            self.searchb.show()
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
    
    def act_hlight(self, *data):
        """Callback for 'Syntax highlighting' actions."""
        tab = self.get_current_tab()
        actions = {'action_hlauto':'auto', 'action_hllatex':'latex'}
        hl = actions.get(data[0].get_name(), None) if len(data)>0 else None
        if hasattr(tab, 'set_hlight'):
            tab.set_hlight(hl)
        return
    
    def act_newproj(self, *data):
        """Callback for 'New project' action."""
        dwin = dialogs.SaveWin(self.app, filename=_("New_project.ephb"))
        resp = dwin.run()
        uri = dwin.get_uri() if resp == gtk.RESPONSE_OK else None
        dwin.destroy()
        if uri is not None:
            self.do_open(uri, 'project', new=True)
        return
    
    def act_about(self, *data):
        """Callback for 'About' action."""
        dwin = dialogs.AboutWin(self.app)
        dwin.run()
        dwin.destroy()
        return
    
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
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
        a = self.uim.get_action(path)
        for p in a.get_proxies():
            a.block_activate_from(p)
            p.set_active(visible)
            a.unblock_activate_from(p)
        w = self.get_widgets_by_name(panel+'panel').pop()
        exe = w.show() if visible else w.hide()
        return
    
    def do_ask_save(self, tabs):
        """Ask if save tab before closing."""
        tabask = []
        for t in tabs:
            if hasattr(t, 'save'):
                i = t.get_file_infos()
                if i[2]:
                    n = i[0] if i[1] is None else i[1].fullname()
                    tabask.append((t, n))
        if len(tabask) > 0:
            dwin = dialogs.SaveBeforeCloseWin(self.app, tabask)
            resp = dwin.run()
            tosave = dwin.get_tabs_to_save()
            dwin.destroy()
            if resp == gtk.RESPONSE_REJECT:
                tosave = []
            elif resp != gtk.RESPONSE_OK:
                tosave = None
        else:
            tosave = []
        return tosave
    
    def do_open(self, filepath, filter, **args):
        """Open file in new tab."""
        if filter == 'all' and filepath is not None:
            filter = self.get_handler_from_path(filepath)
        i = [fh[0] for fh in self.file_handlers].index(filter)
        tab_type = self.file_handlers[i][3]
        tab_opts = self.file_handlers[i][4].copy()
        tab_opts.update(args)
        if filepath is not None:
            enc = tab_opts['enc'] if 'enc' in tab_opts else None
            f = iofiles.FileManager(filepath, enc)
            f.update_infos()
            for ti in self.get_tabs_infos():
                if f.is_same_file_as(ti[3]):
                    self.nbd.set_current_page(ti[2])
                    return
        else:
            f = None
        log("do_open > '"+filter+"' "+repr(tab_opts))
        tab = tab_type(self.app, f, **tab_opts)
        if hasattr(tab, 'content'):
            self.app.prefm.autoconnect_gtk(tab.content)
        if tab in self.nbd.tab_list:
            self.emit('open', tab)
        return
    
    def do_quit(self):
        """Ensure that the application quits correctly."""
        self.emit('quit')
        if self.project is not None:
            self.project.save()
        pluglist = self.app.plugm.list_loaded_plugins()
        self.app.prefm.set_pref('plugins_list', pluglist)
        self.app.plugm.stop_all_plugins()
        self.app.prefm.store()
        self.ev_destroy()
        return


#------------------------------------------------------------------------------



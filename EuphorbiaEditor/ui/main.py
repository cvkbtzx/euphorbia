#-*- coding:utf-8 -*-

##  EUPHORBIA - GTK LaTeX Editor
##  Module: EuphorbiaEditor.ui
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


"""Euphorbia GUI management."""

import os.path
import fnmatch
import gtk
import pango
import gtksourceview2 as gtksv

from . import actions
from . import dialogs
from . import document
from . import project
from . import searchbar
from . import sidepanel


#------------------------------------------------------------------------------

SIGNALS = ['open', 'save', 'close', 'changetab', 'quit', 'openprj', 'closeprj']

DEFAULT_PREFS_TABS = [
    # Name, widget
    ("General", dialogs.PrefsWinGeneral),
    ("LaTeX",   dialogs.PrefsWinLatex),
    ("Plugins", dialogs.PrefsWinPlugins),
]

DEFAULT_FILE_HANDLERS = [
    # ID, description, patterns, object, default_params
    ('all', "All files", ["*"], document.Document, {}),
    ('latex', "LaTeX files", ["*.tex","*.latex","*.bib"], document.Document, {'hlight':"latex"}),
    ('project', "Project files", ["*.ephb","*.kilepr"], project.ProjectManager, {'new':False}),
]


#------------------------------------------------------------------------------

class EuphorbiaGUI(actions.ActionsManager):
    """Graphical User Interface."""
    
    def __init__(self, app):
        actions.ActionsManager.__init__(self, app)
        self.clipb = gtk.clipboard_get()
        self.setup_printers()
        self.connections = dict((s,[]) for s in SIGNALS)
        trad = lambda x,n: x[:n] + (_(x[n]),) + x[n+1:]
        self.prefs_tabs = [trad(p,1) for p in DEFAULT_PREFS_TABS]
        self.file_handlers = [trad(h,1) for h in DEFAULT_FILE_HANDLERS]
        self.build_interface()
        self.nbd = self.builder.get_object('notebook_docs')
        self.nbd.tab_list = set()
        self.project = None
        self.win.show()
    
    def build_interface(self):
        """Build the graphical interface."""
        maindir = self.app.prefm.get_pref('system_maindir')
        # Widgets loading
        self.builder = gtk.Builder()
        self.builder.set_translation_domain(None)
        self.builder.add_from_file(os.path.join(maindir, "main.glade"))
        self.set_builder_names()
        self.builder.connect_signals(self)
        # Main window
        self.win = self.builder.get_object('window')
        self.win.set_transient_for(None)
        img, sizes = os.path.join(maindir,"euphorbia.svg"), [16,24,32,48,64]
        icons = (gtk.gdk.pixbuf_new_from_file_at_size(img,s,s) for s in sizes)
        self.win.set_icon_list(*icons)
        # Side panel
        hp = self.builder.get_object('hpaned_main')
        hp.get_child1().destroy()
        hp.pack1(sidepanel.EuphorbiaSidePanel(self.app, self), False, True)
        hp.get_child1().showpanel = lambda x: self.do_showpanel(x, 'side')
        bp = self.builder.get_object('bottompanel')
        bp.showpanel = lambda x: self.do_showpanel(x, 'bottom')
        # UI Manager
        self.uim = gtk.UIManager()
        # Accels
        accg = self.uim.get_accel_group()
        self.win.add_accel_group(accg)
        # Actions (actions.ActionsManager.actgrp)
        self.uim.insert_action_group(self.actgrp, 0)
        # Interface
        self.uim.add_ui_from_file(os.path.join(maindir, "main-ui.xml"))
        menu = self.uim.get_widget("/menu_main")
        self.builder.get_object('vbox_main').pack_start(menu, False, True)
        self.builder.get_object('vbox_main').reorder_child(menu, 0)
        toolbar = self.uim.get_widget("/toolbar_main")
        self.builder.get_object('handlebox_main').add(toolbar)
        # Statusbar
        self.status = self.builder.get_object('statusbar')
        self.locmsg = gtk.Label()
        statusbox = self.status.get_children()[0].get_children()[0]
        statusbox.pack_start(self.locmsg, False, True)
        self.locmsg.show_all()
        # Searchbar
        sb = searchbar.SearchBar(self.app, accg)
        self.builder.get_object('vbox_docs').pack_start(sb, False, True)
        self.searchb = sb
        # Sourceview styles
        ssm = gtksv.style_scheme_manager_get_default()
        s = [(ssm.get_scheme(id).get_name(),id) for id in ssm.get_scheme_ids()]
        self.app.prefm.set_pref_values('editview_style', dict(s))
        return
    
    def set_builder_names(self):
        """Set widgets names from their builder ID."""
        for w in self.builder.get_objects():
            if hasattr(w, 'set_name'):
                w.set_name(gtk.Buildable.get_name(w))
        return
    
    def setup_printers(self):
        """Setup print properties."""
        dps = gtk.PaperSize(gtk.paper_size_get_default())
        self.print_setup = gtk.PageSetup()
        self.print_setup.set_paper_size_and_default_margins(dps)
        self.print_settings = gtk.PrintSettings()
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
    
    def get_handler_from_path(self, path):
        """Try to guess file handler from patterns."""
        handlers = []
        for fh in self.file_handlers:
            if any(fnmatch.fnmatch(path,e) for e in fh[2]) and fh[0] != 'all':
                handlers.append(fh[0])
        return handlers[0] if len(handlers)>0 else 'all'
    
    def get_current_tab(self, n=None):
        """Get the current tab object (TabWrapper subclass)."""
        n = self.nbd.get_current_page() if n is None else n
        obj = self.nbd.get_nth_page(n)
        tab = [t for t in self.nbd.tab_list if t.content is obj]
        return tab[0] if len(tab) == 1 else None
    
    def get_tabs_infos(self):
        """Get list of tabs infos [(tab, title, position, gfile)]."""
        infos = []
        for tab in self.nbd.tab_list:
            title = tab.get_title()
            pos = self.nbd.page_num(tab.content)
            f = tab.get_file_infos()[1]
            infos.append((tab, title, pos, f))
        return infos
    
    def connect(self, signal, func, *args):
        """Connect a function to the specified Euphorbia signal."""
        self.connections[signal].append((func, args))
        return
     
    def emit(self, signal, *params):
        """Emit the specified Euphorbia signal."""
        self.status_msg(_("signal_"+signal))
        log("signal > "+signal)
        for cb in self.connections[signal]:
            func = cb[0]
            func(*(params+cb[1]))
        return
    
    def status_msg(self, txt, id='standard'):
        """Update statusbar message."""
        cid = self.status.get_context_id(id)
        self.status.push(cid, txt)
        return
    
    def popup_msg(self, t, b, txt):
        """Display a message in a dialog window."""
        dwin = dialogs.MsgWin(self.app.gui.win, t, b, txt)
        ret = dwin.run()
        dwin.destroy()
        return ret
    
    def ev_switch_page(self, *data):
        """Callback switch document."""
        tab = self.get_current_tab(data[2])
        if tab is not None:
            if hasattr(tab, 'ev_selected'):
                tab.ev_selected()
            self.emit('changetab', tab)
        return
    
    def ev_win_state(self, win, event):
        """Callback to handle window (un)maximize event."""
        m = gtk.gdk.WINDOW_STATE_MAXIMIZED
        if event.changed_mask & m:
            p = True if event.new_window_state & m else False
            self.app.prefm.set_pref('window_maximized', p)
        return
    
    def ev_hide_bottom(self, *data):
        """Callback hide bottom notebook."""
        self.do_showpanel(False, 'bottom')
        return
    
    def ev_delete_event(self, *data):
        """Callback for 'delete_event' event."""
        self.act_quit()
        return True
    
    def ev_destroy(self, *data):
        """Callback for 'destroy' event."""
        gtk.main_quit()
    
    def main(self):
        """Main loop."""
        gtk.main()
        return 0


#------------------------------------------------------------------------------



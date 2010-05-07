# -*- coding:utf-8 -*-

##  EUPHORBIA - GTK LaTeX Editor
##  Module: EuphorbiaEditor.ui.project
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


"""Project manager."""

import os.path
import gtk
import gio
import pango
import gobject
import ConfigParser

import EuphorbiaEditor.utils.iofiles as iofiles


#------------------------------------------------------------------------------

MENU = """
<menubar name="menu_main">
  <menu name="menu_project" action="action_project">
    <menuitem action="action_closeproj" />
    <separator />
    <menuitem action="action_openaddproj" />
    <menuitem action="action_addtabproj" />
    <menuitem action="action_rmtabproj" />
    <menuitem action="action_projmaster" />
    <separator />
    <menuitem action="action_archiveproj" />
    <menuitem action="action_projprops" />
  </menu>
</menubar>
"""

def get_actions(cls):
    actions = [
        ('action_closeproj', gtk.STOCK_CLOSE, None, '', None, cls.act_close),
        ('action_openaddproj', gtk.STOCK_ADD, _("Add files"), '', None, cls.act_openadd),
        ('action_addtabproj', gtk.STOCK_ADD, _("Add current tab"), '', None, cls.act_addtab),
        ('action_rmtabproj', gtk.STOCK_REMOVE, _("Remove current tab"), '', None, cls.act_rmtab),
        ('action_projmaster', gtk.STOCK_HOME, _("Set as master document"), '', None, cls.act_setmaster),
        ('action_archiveproj', gtk.STOCK_HARDDISK, _("Archive"), '', None, cls.act_archive),
        ('action_projprops', gtk.STOCK_PROPERTIES, None, '', None, cls.act_properties),
    ]
    return actions


#------------------------------------------------------------------------------

class ProjectManager(object):
    """Manage project files."""
    
    def __init__(self, app, fileobj, **args):
        self.app = app
        self.fileobj = fileobj
        self.rootdir = URImanager(fileobj.gfile.get_parent().get_uri())
        self.master = None
        self.cparser = ConfigParser.RawConfigParser()
        if self.load(**args):
            if self.app.gui.project is not None:
                self.app.gui.project.act_close()
            self.app.gui.project = self
            self.listfiles = {}
            # Menu actions
            self.actgrp = gtk.ActionGroup('euphorbia')
            self.actgrp.add_actions(get_actions(self))
            self.app.gui.uim.insert_action_group(self.actgrp, -1)
            self.menu = self.app.gui.uim.add_ui_from_string(MENU)
            # Side panel
            sidepanel = self.app.gui.get_widgets_by_name('sidepanel').pop()
            self.pb = ProjectBrowser(self)
            sidepanel.add_expander('project', _("Project content"), self.pb)
            sidepanel.reorder_child(sidepanel.expanders['project'], 0)
            self.app.prefm.autoconnect_gtk(sidepanel)
            self.pb.update()
    
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
    def act_close(self, *data):
        """Callback for 'Close' action."""
        self.save()
        sidepanel = self.app.gui.get_widgets_by_name('sidepanel').pop()
        sidepanel.remove_expander('project')
        self.app.gui.uim.remove_ui(self.menu)
        self.app.gui.uim.remove_action_group(self.actgrp)
        self.menu, self.actgrp = None, None
        self.app.gui.project = None
        return
    
    def act_openadd(self, *data):
        """Callback for 'Add files' action."""
        uris = self.app.gui.act_open(do_open=False)
        for u in uris:
            f = iofiles.FileManager(u)
            f.update_infos()
            self.add_file(f)
        return
    
    def act_addtab(self, *data):
        """Callback for 'Add tab' action."""
        tab = self.app.gui.get_current_tab()
        if tab is not None:
            self.add_tab(tab)
        return
    
    def act_rmtab(self, *data):
        """Callback for 'Remove tab' action."""
        tab = self.app.gui.get_current_tab()
        if tab is not None:
            self.rm_tab(tab)
        return
    
    def act_setmaster(self, *data):
        """Callback for 'Set master' action."""
        tab = self.app.gui.get_current_tab()
        if tab is not None:
            f = tab.get_file_infos()[1]
            if f is not None:
                self.set_master(f.uri)
        return
    
    def act_archive(self, *data):
        """Callback for 'Archive' action."""
        print "Project archive"
        return
    
    def act_properties(self, *data):
        """Callback for 'Archive' action."""
        print "Project properties"
        return
    
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
    def belongs(self, urim):
        """Test if URImanager belongs to the project."""
        return any(urim == u for u in self.listfiles)
    
    def add(self, urim, hl=None, enc=None):
        """Add an urim to the project."""
        # {"file_urim": [hlight, enc, open, archive]}
        test = not self.belongs(urim)
        if test:
            isopen = self.is_opened(urim)
            self.listfiles[urim] = [hl, enc, isopen, True]
            self.pb.update()
        return test
    
    def add_file(self, f, hl=None):
        """Add a file to the project."""
        if f.uri is None:
            return False
        urim = URImanager(f.uri)
        return self.add(urim, hl, f.encoding)
    
    def add_tab(self, tab):
        """Add tab's file to the project's files."""
        i = tab.get_file_infos()
        if i[1] is not None:
            hl = tab.datafile['hlight'] if hasattr(tab, 'datafile') else None
            ret = self.add_file(i[1], hl)
        else:
            ret = False
        return ret
    
    def remove(self, urim):
        """Remove an urim from the project."""
        if self.master == urim:
            self.master = None
        if self.belongs(urim):
            for u in self.listfiles.keys():
                if u == urim:
                    del self.listfiles[u]
            self.pb.update()
        return
    
    def rm_file(self, f):
        """Remove a file from the project."""
        urim = URImanager(f.uri)
        self.remove(urim)
        return
    
    def rm_tab(self, tab):
        """Remove tab's file from the project's files."""
        i = tab.get_file_infos()
        if i[1] is not None:
            self.rm_file(i[1])
        return
    
    def set_master(self, uri):
        """Set the master document (uri or URImanager)."""
        urim = URImanager(uri) if type(uri) is str else uri
        if not self.belongs(urim):
            log("project > this tab does not belong to the project", 'error')
        else:
            self.master = urim
            self.pb.update()
        return
    
    def is_opened(self, urim):
        """Test if an urim is opened in a tab."""
        func = lambda x: URImanager(x.uri)
        tab_urims = map(func, self.app.gui.list_opened_files())
        return any(urim == u for u in tab_urims)
    
    def in_archive(self, urim, value=None):
        """Set if urim is to be archived."""
        ### TODO ###
        if value in [True, False]:
            val = 'true' if value else 'false'
        else:
            value = True
        return value
    
    def list_files(self):
        """List the files (URImanager) belonging to the project."""
        return self.listfiles.keys()
    
    def open_uri(self, urim):
        """Open the given file (URImanager) in a new tab."""
        self.app.gui.do_open(urim.gfile.get_uri(), 'all')
        return
    
    def load(self, **args):
        """Load the project from a file."""
        print "Project load"
        return True
    
    def save(self):
        """Save the project into a file."""
        print "Project save"
        return


#------------------------------------------------------------------------------

class URImanager(gobject.GObject):
    """Class to manage URIs."""
    
    def __init__(self, uri):
        gobject.GObject.__init__(self)
        self.gfile = gio.File(uri)
    
    def relative(self, root):
        """Return path of URI relative to root."""
        rel = os.path.relpath(self.gfile.get_uri(), root.gfile.get_uri())
        return rel
    
    def __repr__(self):
        return self.gfile.get_uri()
    
    def __eq__(self, urim2):
        if urim2 is None:
            return False
        return self.gfile.equal(urim2.gfile)
    
    def __ne__(self, urim2):
        return not self.__eq__(urim2)


#------------------------------------------------------------------------------

class ProjectBrowser(gtk.ScrolledWindow):
    """TreeView which displays project files."""
    
    def __init__(self, manager):
        gtk.ScrolledWindow.__init__(self)
        self.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        self.set_shadow_type(gtk.SHADOW_NONE)
        self.set_name("projectbrowser")
        self.manager = manager
        self.build_treeview()
        self.add(self.tv)
        self.show_all()
    
    def build_treeview(self):
        """Build the treeview."""
        # Model
        self.ts = gtk.ListStore(URImanager, gtk.gdk.Pixbuf, str, pango.Weight)
        # View
        self.tv = gtk.TreeView()
        self.tv.set_model(self.ts)
        self.tv.set_headers_visible(False)
        self.tv.set_reorderable(False)
        self.tv.set_enable_search(True)
        self.tv.set_search_column(2)
        self.tv.set_enable_tree_lines(False)
        self.tv.get_selection().set_mode(gtk.SELECTION_SINGLE)
        self.tv.props.can_focus = False
        self.tv.connect('button-press-event', self.ev_right_click)
        self.tv.connect('row-activated', self.ev_row_activated)
        # Column
        c = gtk.TreeViewColumn("Files")
        crp = gtk.CellRendererPixbuf()
        c.pack_start(crp, False)
        c.add_attribute(crp, 'pixbuf', 1)
        crt = gtk.CellRendererText()
        crt.props.ellipsize = pango.ELLIPSIZE_END
        crt.props.scale = pango.SCALE_SMALL
        c.pack_start(crt, True)
        c.add_attribute(crt, 'text', 2)
        c.add_attribute(crt, 'weight', 3)
        c.set_expand(True)
        self.tv.append_column(c)
        return
    
    def update(self):
        """Update treeview content."""
        self.ts.clear()
        names = {}
        for urim in self.manager.listfiles:
            names[urim.relative(self.manager.rootdir)] = urim
        master = self.manager.master
        for n in sorted(names.keys()):
            urim = names[n]
            w = pango.WEIGHT_BOLD if urim == master else pango.WEIGHT_NORMAL
            pix = self.render_icon(gtk.STOCK_FILE, gtk.ICON_SIZE_MENU)
            self.ts.append([urim, pix, n, w])
        return
    
    def get_context_menu(self, iter):
        """Get right-click contextual menu."""
        urim = self.ts.get_value(iter, 0)
        item_o = gtk.ImageMenuItem(gtk.STOCK_OPEN)
        item_o.connect('activate', self.ev_open, urim)
        item_m = gtk.ImageMenuItem(gtk.STOCK_HOME)
        item_m.set_label(_("Set as master document"))
        item_m.connect('activate', self.ev_setmaster, urim)
        item_r = gtk.ImageMenuItem(gtk.STOCK_REMOVE)
        item_r.set_label(_("Remove from project"))
        item_r.connect('activate', self.ev_remove, urim)
        item_a = gtk.CheckMenuItem(_("Include in archive"))
        item_a.set_active(self.manager.in_archive(urim))
        item_a.connect('activate', self.ev_archive, urim)
        menu = gtk.Menu()
        for i in [item_o, item_m, item_r, gtk.SeparatorMenuItem(), item_a]:
            menu.append(i)
        menu.show_all()
        return menu
    
    def ev_right_click(self, w, event):
        """Handle right-click on treeview."""
        if event.button == 3  and event.type == gtk.gdk.BUTTON_PRESS:
            pathinfo = self.tv.get_path_at_pos(int(event.x), int(event.y))
            if pathinfo is not None:
                iter = self.ts.get_iter(pathinfo[0])
                self.tv.get_selection().select_iter(iter)
                menu = self.get_context_menu(iter)
                menu.popup(None, None, None, event.button, event.time)
            else:
                self.tv.get_selection().unselect_all()
            return True
        return False
    
    def ev_open(self, menuitem, urim):
        """Callback for 'open' menu event."""
        self.manager.open_uri(urim)
        return
    
    def ev_setmaster(self, menuitem, urim):
        """Callback for 'set master' menu event."""
        self.manager.set_master(urim)
        return
    
    def ev_remove(self, menuitem, urim):
        """Callback for 'remove' menu event."""
        self.manager.remove(urim)
        return
    
    def ev_archive(self, menuitem, urim):
        """Callback for 'archive' menu event."""
        self.manager.in_archive(urim, not menuitem.get_active())
        return
    
    def ev_row_activated(self, w, path, column):
        """Callback for double-click event."""
        iter = self.ts.get_iter(path)
        urim = self.ts.get_value(iter, 0)
        self.manager.open_uri(urim)
        return


#------------------------------------------------------------------------------



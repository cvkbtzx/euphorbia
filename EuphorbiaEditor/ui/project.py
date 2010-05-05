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
import pango
import ConfigParser


#------------------------------------------------------------------------------

class ProjectManager(object):
    """Manage project files."""
    
    def __init__(self, app, fileobj, **args):
        self.app = app
        if self.app.gui.project is not None:
            self.app.gui.project.close()
        self.fileobj = fileobj
        self.rootdir = os.path.dirname(fileobj.uri)
        self.listfiles = {}        # {"filename": [hlight, enc, open, archive]}
        self.app.gui.project = self
        sidepanel = self.app.gui.get_widgets_by_name('sidepanel').pop()
        pb = ProjectBrowser(self)
        sidepanel.add_expander('project', _("Project content"), pb)
        sidepanel.reorder_child(sidepanel.expanders['project'], 0)
        self.app.prefm.autoconnect_gtk(sidepanel)
    
    def add_file(self, f, hl=None):
        """Add a file to the project."""
        uri = f.uri
        if uri is None:
            return False
        isopen = uri in map(lambda x: x.uri, self.app.gui.list_opened_files())
        self.listfiles[uri] = [hl, f.encoding, isopen, True]
        return True
    
    def del_file(self, f):
        """Remove a file from the project."""
        uri = f.uri
        if uri in self.listfiles:
            del self.listfiles[uri]
        return
    
    def add_tab(self, tab):
        """Add tab's file to the project's files."""
        i = tab.get_file_infos()
        if i[1] is not None:
            hl = tab.datafile['hlight'] if hasattr(tab, 'datafile') else None
            ret = self.add_file(i[1], hl)
        else:
            ret = False
        return ret
    
    def del_tab(self, tab):
        """Remove tab's file from the project's files."""
        i = tab.get_file_infos()
        if i[1] is not None:
            self.del_file(i[1])
        return
    
    def list_files(self):
        """List the files belonging to the project."""
        return self.listfiles.keys()
    
    def load(self):
        """Load the project from a file."""
        return
    
    def save(self):
        """Save the project into a file."""
        return
    
    def close(self):
        """Close the project."""
        self.save()
        sidepanel = self.app.gui.get_widgets_by_name('sidepanel').pop()
        sidepanel.remove_expander('project')
        self.app.gui.project = None
        return


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
        self.ts = gtk.TreeStore(gtk.gdk.Pixbuf, str, pango.Weight)
        # View
        self.tv = gtk.TreeView()
        self.tv.set_model(self.ts)
        self.tv.set_headers_visible(False)
        self.tv.set_reorderable(False)
        self.tv.set_enable_search(True)
        self.tv.set_search_column(1)
        self.tv.set_enable_tree_lines(False)
        self.tv.get_selection().set_mode(gtk.SELECTION_NONE)
        self.tv.connect('row-activated', self.ev_row_activated)
        # Column
        c = gtk.TreeViewColumn("Files")
        crp = gtk.CellRendererPixbuf()
        c.pack_start(crp, False)
        c.add_attribute(crp, 'pixbuf', 0)
        crt = gtk.CellRendererText()
        crt.props.ellipsize = pango.ELLIPSIZE_END
        crt.props.scale = pango.SCALE_SMALL
        c.pack_start(crt, True)
        c.add_attribute(crt, 'text', 1)
        c.add_attribute(crt, 'weight', 2)
        c.set_expand(True)
        self.tv.append_column(c)
        return
    
    def ev_row_activated(self, w, path, column):
        """Callback for double-click event."""
        return


#------------------------------------------------------------------------------



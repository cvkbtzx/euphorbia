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


"""Document structure tree widget."""

import gtk
import pango


#------------------------------------------------------------------------------

class TreeDocStruct(gtk.ScrolledWindow):
    """TreeView which displays a document structure."""
    
    def __init__(self):
        gtk.ScrolledWindow.__init__(self)
        self.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        self.set_shadow_type(gtk.SHADOW_NONE)
        self.set_name("treedocstruct")
        self.activate_cb = None
        self.expand_level = 2
        self.tree = []
        self.build_treeview()
        self.add(self.tv)
        self.show_all()
    
    def build_treeview(self):
        """Build the treeview."""
        # Model
        self.ts = gtk.TreeStore(str, pango.Weight)
        # View
        self.tv = gtk.TreeView()
        self.tv.set_model(self.ts)
        self.tv.set_headers_visible(False)
        self.tv.set_reorderable(False)
        self.tv.set_enable_search(True)
        self.tv.set_search_column(0)
        self.tv.set_enable_tree_lines(True)
        self.tv.get_selection().set_mode(gtk.SELECTION_NONE)
        self.tv.connect('row-activated', self.ev_row_activated)
        # Column
        cr = gtk.CellRendererText()
        cr.props.ellipsize = pango.ELLIPSIZE_END
        cr.props.scale = pango.SCALE_SMALL
        c = gtk.TreeViewColumn("Structure", cr, text=0, weight=1)
        c.set_expand(True)
        self.tv.append_column(c)
        return
    
    def set_data(self, tree):
        """Set tree rows from list."""
        self.tree = tree
        self.ts.clear()
        self._populate_tree_rec(None, self.tree, 0)
        self.expand_at_level()
        return
    
    def _populate_tree_rec(self, parent, subtree, level):
        """Populate tree recursively."""
        weight = pango.WEIGHT_BOLD if level == 0 else pango.WEIGHT_NORMAL
        for i,l,v in subtree:
            it = self.ts.append(parent, [i, weight])
            self._populate_tree_rec(it, v, level+1)
        return
    
    def set_expand_level(self, level):
        """Set default expand level value."""
        self.expand_level = level
        self.expand_at_level()
        return
    
    def expand_at_level(self, level=None):
        """Expand tree at specified level."""
        self.tv.collapse_all()
        level = self.expand_level if level is None else level
        etp, id = self.tv.expand_to_path, self.ts.iter_depth
        self.ts.foreach(lambda m,p,i: etp(p) if id(i)<level else None)
        return
    
    def get_row_at_path(self, path):
        """Get tree row from its path."""
        t, l = self.tree, None
        for p in path:
            r, l, t = t[p]
        return (r, l)
    
    def ev_row_activated(self, w, path, column):
        """Callback for double-click event."""
        row = self.get_row_at_path(path)
        if self.activate_cb is not None:
            self.activate_cb(row)
        return


#------------------------------------------------------------------------------

if __name__ == "__main__":
    win = gtk.Window()
    win.connect('destroy', lambda w: gtk.main_quit())
    win.set_default_size(200, 300)
    tds = TreeDocStruct()
    data, n = [("Filename", None, [])], 1
    for i in "ABC":
        x, n = (i, n, []), n + 1
        for j in "abc":
            y, n = (i+j, n, []), n + 1
            for k in "123":
                z, n = (i+j+k, n, []), n + 1
                y[2].append(z)
            x[2].append(y)
        data[0][2].append(x)
    tds.set_data(data)
    win.add(tds)
    win.show()
    gtk.main()


#------------------------------------------------------------------------------



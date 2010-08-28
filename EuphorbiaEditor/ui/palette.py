#-*- coding:utf-8 -*-

##  EUPHORBIA - GTK LaTeX Editor
##  Module: EuphorbiaEditor.ui.palette
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


"""Palette widget."""

import gtk


#------------------------------------------------------------------------------

class Palette(gtk.ScrolledWindow):
    """Palette toolbar with automatic lines/columns adaptation."""
    
    def __init__(self):
        gtk.ScrolledWindow.__init__(self)
        self.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        self.set_shadow_type(gtk.SHADOW_NONE)
        self.iacb, self.iacb_args = None, ()
        # Create the ListStore
        self.store = gtk.ListStore(str, str, gtk.gdk.Pixbuf)
        # Setup the IconView
        SPACING = 1
        self.iw = gtk.IconView(self.store)
        self.iw.set_tooltip_column(1)
        self.iw.set_pixbuf_column(2)
        self.iw.set_text_column(-1)   # deactivate text
        self.iw.set_markup_column(-1)   # deactivate markup
        self.iw.set_selection_mode(gtk.SELECTION_SINGLE)
        self.iw.set_reorderable(False)
        self.iw.set_spacing(0)
        self.iw.set_row_spacing(SPACING)
        self.iw.set_column_spacing(SPACING)
        self.iw.set_margin(SPACING)
        self.iw.props.can_focus = False
        self.iw.connect('selection-changed', self.on_selection_changed)
        # Display
        self.add(self.iw)
        self.show_all()
    
    def add_tool(self, tool):
        """Add a tool to the palette: [ID(str), tooltip(str), icon(gtk.gdk.Pixbuf)]."""
        self.store.append(tool)
        return
    
    def remove_all_tools(self):
        """Remove all tools."""
        self.store.clear()
        return
    
    def set_item_activated_callback(self, cb=None, *args):
        """Set the function to execute when an item is activated."""
        self.iacb = cb
        self.iacb_args = args
        return
    
    def on_selection_changed(self, *data):
        """Handle clic on tool."""
        paths = self.iw.get_selected_items()
        if len(paths) != 1:
            return
        iter = self.store.get_iter(paths[0])
        p = self.store.get_value(iter, 0)
        self.iw.unselect_all()
        if self.iacb == None:
            print "Click on '" + p + "'"
        else:
            self.iacb(p, *self.iacb_args)
        return


#------------------------------------------------------------------------------

if __name__ == '__main__':
    win = gtk.Window()
    win.connect('destroy', lambda w: gtk.main_quit())
    win.set_default_size(400, 300)
    hp = gtk.HPaned()
    p = Palette()
    for id in gtk.stock_list_ids():
        t = [id, id, win.render_icon(id, gtk.ICON_SIZE_MENU)]
        p.add_tool(t)
    hp.pack1(p, resize=False, shrink=True)
    hp.pack2(gtk.Label("Hello !"), resize=True, shrink=False)
    hp.set_position(200)
    win.add(hp)
    win.show_all()
    gtk.main()


#------------------------------------------------------------------------------



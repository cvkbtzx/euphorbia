# -*- coding:utf-8 -*-

import pygtk
pygtk.require('2.0')
import gtk


#------------------------------------------------------------------------------

class Palette(gtk.ScrolledWindow):
    """Palette toolbar with automatic lines/columns adaptation."""
    
    def __init__(self):
        gtk.ScrolledWindow.__init__(self)
        self.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        self.set_shadow_type(gtk.SHADOW_NONE)
        self.iacb = None
        # Create the ListStore
        self.store = gtk.ListStore(str, str, gtk.gdk.Pixbuf)
        # Setup the IconView
        SPACING = 1
        self.iw = gtk.IconView(self.store)
        self.iw.set_tooltip_column(1)
        self.iw.set_pixbuf_column(2)
        self.iw.set_selection_mode(gtk.SELECTION_NONE)
        self.iw.set_reorderable(False)
        self.iw.set_spacing(0)
        self.iw.set_row_spacing(SPACING)
        self.iw.set_column_spacing(SPACING)
        self.iw.set_margin(SPACING)
        self.iw.connect('item-activated', self.on_item_activated)
        # Display
        self.add(self.iw)
        self.iw.show_all()
    
    def add_tool(self, tool):
        """Add a tool to the palette: [ID(str), tooltip(str), icon(gtk.gdk.Pixbuf)]."""
        self.store.append(tool)
        return
    
    def remove_all_tools(self):
        """Remove all tools."""
        self.store.clear()
        return
    
    def set_item_activated_callback(self, cb=None):
        """Set the function to execute when an item is activated."""
        self.iacb = cb
        return
    
    def on_item_activated(self, *data):
        """Handle clic on tool."""
        p = self.store[data[1][0]][0]
        if self.iacb == None:
            print "Click on '" + p + "'"
        else:
            self.iacb(p)
        return


#------------------------------------------------------------------------------

if __name__ == "__main__":
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



# -*- coding:utf-8 -*-

import pygtk
pygtk.require('2.0')
import gtk
import palette


#------------------------------------------------------------------------------

class SidePanel(gtk.VBox):
    """Side panel with symbols insertion and document managment facilities."""
    
    def __init__(self):
        gtk.VBox.__init__(self)
        self.expanders = {}
        #####   TODO   #####
        box = palette.Palette()
        for id in gtk.stock_list_ids():
            t = [id, id, self.render_icon(id, gtk.ICON_SIZE_MENU)]
            box.add_tool(t)
        self.add_expander('tree',       "Project tree",   gtk.Label("Hello !"))
        self.add_expander('struct',     "File structure", gtk.Label("Hello !"))
        self.add_expander('operators',  "Operators",      box)
        self.add_expander('arrows',     "Arrows",         gtk.Label("Hello !"))
        self.add_expander('greek',      "Greek letters",  gtk.Label("Hello !"))
        self.add_expander('diacritics', "Diacritics",     gtk.Label("Hello !"))
        ####################
        self.show()
    
    def add_expander(self, name, label, child):
        """Add an Expander object to the panel."""
        exp = Expander(label, child)
        self.pack_start(exp, expand=False, fill=True)
        self.expanders[name] = exp
        self.check_expand_status()
        return
    
    def remove_expander(self, name):
        """Remove the specified Expander object from the panel."""
        exp = self.expanders.pop(name)
        self.remove(exp)
        self.check_expand_status()
        return
    
    def check_expand_status(self):
        """Check if one of the Expanders is indeed expanded."""
        c = self.get_children()
        if len(c)>0 and not any(map(lambda x: x.get_expanded(), c)):
            self.on_expander(c[0])
        return
    
    def on_expander(self, widget=None):
        """Callback to execute when an Expander is selected."""
        for n,exp in self.expanders.iteritems():
            if exp is widget:
                exp.set_expanded(True)
                self.set_child_packing(exp, True, True, 0, gtk.PACK_START)
            else:
                exp.set_expanded(False)
                self.set_child_packing(exp, False, True, 0, gtk.PACK_START)
        return


#------------------------------------------------------------------------------

class Expander(gtk.VBox):
    """Expander class for side panel (show/hide child widget)."""
    
    def __init__(self, label, child):
        gtk.VBox.__init__(self)
        # Button
        button = gtk.Button()
        button.connect('clicked', lambda w: self.on_button_selected(w))
        ###button.connect('enter', lambda w: self.on_button_selected(w))
        button.set_focus_on_click(False)
        button.set_relief(gtk.RELIEF_NONE)
        hbox = gtk.HBox()
        self.arrow = gtk.Arrow(gtk.ARROW_RIGHT, gtk.SHADOW_IN)
        text = gtk.Label(label)
        text.set_use_markup(True)
        text.set_alignment(0, 0.5)
        hbox.pack_start(self.arrow, expand=False, fill=True)
        hbox.pack_start(text, expand=True, fill=True)
        button.add(hbox)
        button.show_all()
        # Child widget
        self.expanded = False
        self.widget = child
        child.hide()
        # Separator
        sep = gtk.HSeparator()
        sep.show_all()
        # Packing
        self.pack_start(button, expand=False, fill=True)
        self.pack_start(child, expand=True, fill=True)
        self.pack_start(sep, expand=False, fill=True)
        self.show()
    
    def set_expanded(self, bool):
        """Show the child widget if 'True', hide it if 'False'."""
        if bool:
            self.arrow.set(gtk.ARROW_DOWN, gtk.SHADOW_IN)
            self.widget.show()
            self.expanded = True
        else:
            self.arrow.set(gtk.ARROW_RIGHT, gtk.SHADOW_IN)
            self.widget.hide()
            self.expanded = False
        return
    
    def get_expanded(self):
        """Return 'True' if the Expander is expanded."""
        return self.expanded
    
    def on_button_selected(self, widget=None):
        """Callback to execute when the button is selected."""
        self.get_parent().on_expander(self)
        return


#------------------------------------------------------------------------------

if __name__ == "__main__":
    win = gtk.Window()
    win.connect('destroy', lambda w: gtk.main_quit())
    sp = SidePanel()
    win.add(sp)
    win.show()
    gtk.main()


#------------------------------------------------------------------------------



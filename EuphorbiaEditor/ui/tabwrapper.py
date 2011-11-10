#-*- coding:utf-8 -*-

##  EUPHORBIA - GTK LaTeX Editor
##  Module: EuphorbiaEditor.ui.tabwrapper
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


"""Tab management."""

import gtk

ICONTHEME = gtk.icon_theme_get_default()


#------------------------------------------------------------------------------

gtk.rc_parse_string("""
style "euphorbia-tabbutton" {
    GtkWidget::focus-padding = 0
    GtkWidget::focus-line-width = 0
    xthickness = 0
    ythickness = 0
}
widget_class "*.GtkNotebook.GtkHBox.GtkButton" style "euphorbia-tabbutton"
widget_class "*.GtkNotebook.GtkAspectFrame.GtkButton" style "euphorbia-tabbutton"
""")


#------------------------------------------------------------------------------

class TabWrapper(object):
    """Wrapper for notebook tabs."""
    
    def __init__(self, app, child):
        self.app = app
        self.notebook = self.app.gui.nbd
        self.type_id = ""
        # Tab title
        self.title = gtk.Label()
        self.title.set_alignment(0.0, 0.5)
        # Tab close button
        b_close = gtk.Button()
        b_close.set_relief(gtk.RELIEF_NONE)
        b_close.set_focus_on_click(False)
        b_close.connect('clicked', self.ev_close)
        self.button_close = b_close
        self.set_close_icon()
        # Tab icon
        self.icon = gtk.Image()
        # Packing
        hb = gtk.HBox(False, 5)
        hb.pack_start(self.icon, False, False)
        hb.pack_start(self.title, True, True)
        hb.pack_end(b_close, False, False)
        # Add the tab to the notebook
        self.content = child
        self.notebook.append_page(self.content, hb)
        self.notebook.set_tab_reorderable(self.content, True)
        self.notebook.set_current_page(self.notebook.page_num(self.content))
        self.notebook.tab_list.add(self)
        # Display
        hb.show_all()
        self.content.show()
        self.notebook.set_current_page(self.notebook.page_num(self.content))
    
    def get_file_infos(self):
        """Return infos (file_name, file_obj, is_modified) about the file."""
        # Subclasses should override this method
        return ("", None, False)
    
    def set_title(self, txt):
        """Set tab title."""
        self.title.set_text(txt)
        return
    
    def get_title(self):
        """Get tab title."""
        return self.title.get_text()
    
    def set_icon(self, *names):
        """Set icon from its name(s)."""
        for n in names:
            if ICONTHEME.has_icon(n):
                self.icon.set_from_icon_name(n, gtk.ICON_SIZE_MENU)
                return
        self.icon.set_from_stock(gtk.STOCK_FILE, gtk.ICON_SIZE_MENU)
        return
    
    def set_close_icon(self, stock=None):
        """Set close button icon."""
        stock = "gtk-close" if stock is None else "gtk-"+stock
        img = gtk.image_new_from_stock(stock, gtk.ICON_SIZE_MENU)
        self.button_close.set_image(img)
        return
    
    def ev_selected(self):
        """Tabselected callback."""
        loc = self.get_location() if hasattr(self, 'get_location') else ""
        self.app.gui.locmsg.set_text(loc)
        return
    
    def ev_close(self, *data):
        """Close callback."""
        self.app.gui.act_close(**{'tab':self})
        return
    
    def close(self):
        """Close the tab."""
        self.notebook.tab_list.remove(self)
        self.notebook.remove_page(self.notebook.page_num(self.content))
        self.content.destroy()
        self.content = None
        return


#------------------------------------------------------------------------------



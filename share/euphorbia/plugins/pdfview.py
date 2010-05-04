# -*- coding:utf-8 -*-

##  PDF viewer plugin for Euphorbia LaTeX editor
##  Copyright (C) 2010   Bzoloid
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


"""PDF viewer plugin."""

import gtk
import evince
import euphorbia


#------------------------------------------------------------------------------

class PdfView(euphorbia.Plugin):
    """PDF viewer."""
    
    def __init__(self):
        euphorbia.Plugin.__init__(self)
    
    def activate(self):
        handler = (
            'evince',
            _("Output files"), ["*.pdf","*.dvi","*.ps"],
            EvinceTab, {}
        )
        self.app.gui.file_handlers.append(handler)
        return
    
    def deactivate(self):
        i = [fh[0] for fh in self.app.gui.file_handlers].index('evince')
        del self.app.gui.file_handlers[i]
        return


#------------------------------------------------------------------------------

class EvinceTab(euphorbia.TabWrapper):
    """Notebook tab containing an EvinceView."""
    
    def __init__(self, app, fileobj, **args):
        ev = EvinceView(fileobj.uri)
        euphorbia.TabWrapper.__init__(self, app, ev)
        self.gfile = fileobj
        self.set_title(fileobj.get_name())
        self.set_icon(*fileobj.get_icons())
    
    def get_file_infos(self):
        """Return infos (file_name, file_obj, is_modified) about the file."""
        return (self.gfile.get_name(), self.gfile, False)


#------------------------------------------------------------------------------

class EvinceView(gtk.VBox):
    """Display area, handled by evince."""
    
    def __init__(self, filename):
        gtk.VBox.__init__(self)
        dpi = gtk.settings_get_default().get_property('gtk-xft-dpi') / 1024
        self.doc = evince.factory_get_document(filename)
        self.eview = evince.View()
        self.eview.set_loading(False)
        self.eview.set_document(self.doc)
        self.eview.set_screen_dpi(int(dpi))
        self.eview.set_sizing_mode(evince.SIZING_FREE)
        scroll = gtk.ScrolledWindow()
        scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        scroll.add(self.eview)
        tb = gtk.Toolbar()
        tb.set_style(gtk.TOOLBAR_BOTH_HORIZ)
        tb.set_icon_size(gtk.ICON_SIZE_SMALL_TOOLBAR)
        tb.set_tooltips(True)
        self.populate_toolbar(tb)
        self.pack_start(tb, False, True)
        self.pack_start(scroll, True, True)
        self.show_all()
    
    def populate_toolbar(self, tb):
        """Add buttons to the toolbar."""
        tb.set_name('toolbar_pdfview')
        for n in ["GO_UP", "GO_DOWN"]:
            b = gtk.ToolButton(getattr(gtk, "STOCK_"+n))
            b.connect('clicked', getattr(self, "ev_"+n.split('_')[-1].lower()))
            tb.insert(b, -1)
        b = gtk.ToolItem()
        b.add(gtk.Label(""))
        b.set_expand(True)
        tb.insert(b, -1)
        b = gtk.ToolItem()
        b.set_expand(False)
        cb = gtk.combo_box_new_text()
        cb.append_text(_("Zoom page"))
        cb.append_text(_("Zoom width"))
        cb.append_text(_("Zoom 100%"))
        cb.set_active(2)
        cb.connect('changed', self.ev_combo)
        al = gtk.Alignment(0.5, 0.5, 1.0, 0.0)
        al.add(cb)
        b.add(al)
        tb.insert(b, -1)
        return
    
    def ev_combo(self, widget):
        """Callback zoom."""
        i = widget.get_active()
        if i == 0:
            self.eview.set_sizing_mode(evince.SIZING_BEST_FIT)
            self.eview.update_view_size(self.eview.get_parent())
        if i == 1:
            self.eview.set_sizing_mode(evince.SIZING_FIT_WIDTH)
            self.eview.update_view_size(self.eview.get_parent())
        if i == 2:
            self.eview.set_sizing_mode(evince.SIZING_FREE)
            self.eview.set_zoom(1.0, False)
        return
    
    def ev_up(self, *data):
        """Callback previous page."""
        self.eview.previous_page()
        return
    
    def ev_down(self, *data):
        """Callback next page."""
        self.eview.next_page()
        return


#------------------------------------------------------------------------------



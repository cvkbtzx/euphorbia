# -*- coding:utf-8 -*-

"""PDF viewer plugin."""

import gtk
import evince
import euphorbia

import os.path
CWD = os.path.dirname(__file__)
FILE = "file://" + CWD + "/test-doc.pdf"


#------------------------------------------------------------------------------

class PdfView(euphorbia.Plugin):
    """PDF viewer."""
    
    def __init__(self):
        euphorbia.Plugin.__init__(self)
    
    def activate(self):
        nb = self.app.gui.get_widgets_by_name('notebook_docs')
        self.et = EvinceTab(nb.pop(), FILE)
        return
    
    def deactivate(self):
        self.et = None
        return


#------------------------------------------------------------------------------

class EvinceTab(euphorbia.TabWrapper):
    """Notebook tab containing an EvinceView."""
    
    def __init__(self, nb, filename):
        ev = EvinceView(filename)
        euphorbia.TabWrapper.__init__(self, nb, ev)
        self.title.set_text(filename.split('/')[-1])
        self.icon.set_from_stock(gtk.STOCK_ZOOM_FIT, gtk.ICON_SIZE_MENU)


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
        self.eview.set_screen_dpi(dpi)
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
        for n in ["GO_UP", "GO_DOWN"]:
            b = gtk.ToolButton(getattr(gtk, "STOCK_"+n))
            b.connect('clicked', getattr(self, "ev_"+n.split('_')[-1].lower()))
            tb.insert(b, -1)
        b = gtk.SeparatorToolItem()
        b.set_draw(True)
        tb.insert(b, -1)
        b = gtk.ToolItem()
        b.set_expand(False)
        cb = gtk.combo_box_new_text()
        cb.append_text("Zoom page")
        cb.append_text("Zoom width")
        cb.append_text("Zoom 100%")
        cb.set_active(2)
        cb.connect('changed', self.ev_combo)
        b.add(cb)
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



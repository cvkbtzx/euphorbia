#-*- coding:utf-8 -*-

##  EUPHORBIA - GTK LaTeX Editor
##  Module: EuphorbiaEditor.ui.sidepanel
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


"""Side panel widget."""

import os
import glib
import gtk
import ConfigParser

from . import palette
from . import treestruct


#------------------------------------------------------------------------------

class SidePanel(gtk.VBox):
    """Side panel with symbols insertion and document managment facilities."""
    
    def __init__(self):
        gtk.VBox.__init__(self)
        self.expanders = {}
        self.switchsignal = 'clicked'
        self.set_data('id', "sidepanel")
        self.show()
    
    def add_expander(self, name, label, child):
        """Add an Expander object to the panel."""
        exp = Expander(label, child, self.switchsignal)
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
        if len(c)>0 and not any(w.get_expanded() for w in c):
            self.ev_expander(c[0])
        return
    
    def ev_expander(self, widget):
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
    
    def __init__(self, label, child, switchsignal):
        gtk.VBox.__init__(self)
        # Button
        button = gtk.Button()
        button.connect(switchsignal, lambda w: self.ev_button_selected(w))
        button.set_focus_on_click(False)
        button.set_relief(gtk.RELIEF_NONE)
        hbox = gtk.HBox()
        self.arrow = gtk.Arrow(gtk.ARROW_RIGHT, gtk.SHADOW_IN)
        text = gtk.Label(label)
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
        sep.show()
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
    
    def ev_button_selected(self, *data):
        """Callback to execute when the button is selected."""
        self.get_parent().ev_expander(self)
        return


#------------------------------------------------------------------------------

class EuphorbiaSidePanel(SidePanel):
    """Euphorbia side panel."""
    
    def __init__(self, app, gui):
        SidePanel.__init__(self)
        self.app = app
        ss = self.app.prefm.get_pref('sidepanel_switchonclick')
        self.switchsignal = 'clicked' if ss else 'enter'
        tc = gtk.widget_get_default_style().text[gtk.STATE_NORMAL]
        textcolor = "".join(map(chr, [tc.red, tc.green, tc.blue]))
        self.structbrowser = treestruct.StructBrowser()
        self.add_expander('struct', _("Structure"), self.structbrowser)
        for s in ['changetab', 'open', 'save', 'close']:
            gui.connect(s, self.update_structbrowser)
        self.structbrowser.activated_cb = self.ev_struct_activate
        self.syms = self.load_symbols_from_files()
        for categ in sorted(self.syms.keys()):
            pal = palette.Palette()
            for t in sorted(self.syms[categ].keys()):
                try:
                    tool = self.syms[categ][t]
                    pixb = gtk.gdk.pixbuf_new_from_file(tool['Img'])
                    if self.app.prefm.get_pref('sidepanel_symcolorfromtheme'):
                        datapix = pixb.get_pixels()
                        datapix2 = ""
                        for i in xrange(len(datapix)/4):
                            datapix2 += textcolor + datapix[4*i+3]
                        pixb = gtk.gdk.pixbuf_new_from_data(datapix2,
                                pixb.get_colorspace(), pixb.get_has_alpha(),
                                pixb.get_bits_per_sample(), pixb.get_width(),
                                pixb.get_height(), pixb.get_rowstride())
                    tooltip = glib.markup_escape_text(tool['Insert'])
                    pal.add_tool([t, tooltip, pixb])
                except StandardError:
                    msg = "sidepanel > can't load symbol '%s/%s'" % (categ,t)
                    log(msg, 'warning')
            pal.set_item_activated_callback(self.insert_symbol, categ)
            name = self.get_local_name(tool)
            self.add_expander(categ, name, pal)
    
    def load_symbols_from_files(self):
        """Get a list of the categories and their symbols."""
        symlist = {}
        for d in ["maindir", "datadir"]:
            p = self.app.prefm.get_pref("system_"+d)
            dir = os.path.join(p, "symbols")
            if os.path.isdir(dir):
                for f in [i for i in os.listdir(dir) if i.endswith(".data")]:
                    cp = ConfigParser.RawConfigParser()
                    cp.optionxform = str
                    cp.read([os.path.join(dir,f)])
                    id = cp.defaults()['Id']
                    if id not in symlist:
                        symlist[id] = {}
                    for s in cp.sections():
                        sd = dict(cp.items(s))
                        sd['Img'] = os.path.join(dir, id, s+".png")
                        if s not in symlist[id]:
                            symlist[id][s] = {}
                        symlist[id][s].update(sd)
                    if not symlist[id]:
                        del symlist[id]
        return symlist
    
    def get_local_name(self, tool):
        """Get category's localized name from a tool dataset."""
        keys = ['Name']
        lng = self.app.locale[0]
        if lng is not None:
            lng = lng.lower()
            if '_' in lng:
                keys.append("Name["+lng.split('_')[0]+"]")
            keys.append("Name["+lng+"]")
        ret = None
        for k in keys:
            if k in tool:
                ret = tool[k]
        return ret
    
    def insert_symbol(self, symb, categ):
        """Handle click on symbol button."""
        txt = self.syms[categ][symb]['Insert']
        tab = self.app.gui.get_current_tab()
        if hasattr(tab, 'insert'):
            if hasattr(tab, 'insert2') and "{}" in txt:
                i = txt.find("{}") + 1
                txt1, txt2 = txt[:i], txt[i:]
                tab.insert2(txt1, txt2)
            else:
                tab.insert(txt)
        return
    
    def update_structbrowser(self, tab=None):
        """Update structbrowser widget from tab data."""
        if hasattr(tab, 'struct'):
            self.structbrowser.set_struct(tab.struct)
        elif len(self.app.gui.nbd.tab_list) == 0:
            self.structbrowser.set_struct([])
        elif tab is not None:
            self.structbrowser.set_struct([])
        return
    
    def ev_struct_activate(self, row):
        """Callback for tree structure activated event."""
        tab = self.app.gui.get_current_tab()
        line = row[1]
        if line is None:
            tab.gen_doc_struct()
            self.update_structbrowser(tab)
        else:
            tab.goto_index(line)
        return


#------------------------------------------------------------------------------

if __name__ == '__main__':
    win = gtk.Window()
    win.connect('destroy', lambda w: gtk.main_quit())
    # Example palette
    pal = palette.Palette()
    for id in gtk.stock_list_ids():
        t = [id, id, win.render_icon(id, gtk.ICON_SIZE_MENU)]
        pal.add_tool(t)
    # Side panel
    sp = SidePanel()
    sp.add_expander('tree',       "Project tree",   gtk.Label("Hello !"))
    sp.add_expander('struct',     "File structure", gtk.Label("Hello !"))
    sp.add_expander('operators',  "Operators",      pal)
    sp.add_expander('arrows',     "Arrows",         gtk.Label("Hello !"))
    sp.add_expander('greek',      "Greek letters",  gtk.Label("Hello !"))
    sp.add_expander('diacritics', "Diacritics",     gtk.Label("Hello !"))
    win.add(sp)
    # Display
    win.show()
    gtk.main()


#------------------------------------------------------------------------------



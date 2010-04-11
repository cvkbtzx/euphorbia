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


"""Various dialog windows."""

import gtk
import pango


#------------------------------------------------------------------------------

class PrefsWin(gtk.Dialog):
    """Preferences dialog."""
    
    def __init__(self, app):
        # Dialog initialization
        flags = gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT
        buttons = (gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE)
        gtk.Dialog.__init__(self, _("Preferences"), app.gui.win, flags, buttons)
        self.app = app
        self.set_default_size(650, 450)
        self.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
        self.set_has_separator(False)
        self.set_default_response(gtk.RESPONSE_CLOSE)
        # Populate
        self.nbook = gtk.Notebook()
        self.nbook.set_tab_pos(gtk.POS_LEFT)
        self.nbook.set_border_width(9)
        self.vbox.pack_start(self.nbook, True, True)
        self.nbook.append_page(PrefsWinGeneral(app), gtk.Label(_("General")))
        self.nbook.append_page(gtk.Label("empty"), gtk.Label(_("LaTeX")))
        self.nbook.append_page(PrefsWinPlugins(app), gtk.Label(_("Plugins")))
        self.vbox.show_all()


#------------------------------------------------------------------------------

class PrefsWinGeneral(gtk.ScrolledWindow):
    """'General' tab of the preferences dialog."""
    
    def __init__(self, app):
        gtk.ScrolledWindow.__init__(self)
        self.app = app
        self.set_policy(gtk.POLICY_NEVER, gtk.POLICY_ALWAYS)
        container = gtk.VBox()
        container.set_spacing(21)
        container.set_border_width(15)
        categs = {}
        for code,lv,cv in self.app.prefm.iter_prefs_data():
            cg = code.split('_')[0]
            w = self.build_widget(code, lv, cv)
            if w is not None:
                if cg in categs:
                    categs[cg].append((code,w))
                else:
                    categs[cg] = [(code,w)]
        for cg in sorted(categs.keys(), reverse=True):
            f = gtk.Frame("")
            f.props.label_widget.set_alignment(0, 0.5)
            f.props.label_widget.set_padding(3, 0)
            f.props.label_widget.set_markup("<b>"+_("opt_"+cg)+"</b>")
            vb = gtk.VBox()
            vb.set_homogeneous(True)
            vb.set_spacing(3)
            vb.set_border_width(7)
            for code,w in sorted(categs[cg], key=lambda x: x[0]):
                l = gtk.Label(_(code))
                l.set_alignment(0, 0.5)
                l.set_padding(7, 0)
                hb = gtk.HBox()
                hb.pack_start(l, True, True)
                hb.pack_start(w, False, True)
                vb.pack_start(hb, False, False)
            f.add(vb)
            container.pack_start(f, False, False)
        self.add_with_viewport(container)
        container.get_parent().set_shadow_type(gtk.SHADOW_NONE)
    
    def build_widget(self, code, lv, cv):
        """Detect the widget type and return an instance."""
        w = None
        if type(lv) is dict:
            w = self.build_combobox(code, lv, cv)
        if type(lv) is str:
            if lv == 'bool':
                w = self.build_checkbutton(code, lv, cv)
            if lv == 'font':
                w = self.build_fontbutton(code, lv, cv)
            if lv.startswith('int,'):
                w = self.build_spinbutton(code, lv, cv)
        return w
    
    def build_checkbutton(self, code, lv, cv):
        """Build a checkbutton."""
        w = gtk.CheckButton()
        w.set_active(cv)
        w.connect('toggled', self.ev_checkbutton, code)
        return w
    
    def ev_checkbutton(self, w, code):
        """Callback for checkbuttons."""
        self.app.prefm.apply_pref(code, w.get_active())
        return
    
    def build_combobox(self, code, lv, cv):
        """Build a combobox."""
        vals = sorted(lv.items(), key=lambda x: x[1])
        w = gtk.combo_box_new_text()
        na = None
        for i,v in enumerate(vals):
            w.append_text(v[0])
            na = i if v[1]==cv else na
        if na is not None:
            w.set_active(na)
        w.connect('changed', self.ev_combobox, code, [i[1] for i in vals])
        return w
    
    def ev_combobox(self, w, code, lvals):
        """Callback for comboboxes."""
        self.app.prefm.apply_pref(code, lvals[w.get_active()])
        return
    
    def build_spinbutton(self, code, lv, cv):
        """Build a spinbutton."""
        w = gtk.SpinButton()
        w.set_numeric(True)
        w.set_range(*tuple(map(int,lv.split(',')[1:])))
        w.set_digits(0)
        w.set_increments(1, 5)
        w.set_snap_to_ticks(True)
        w.set_value(cv)
        w.connect('changed', self.ev_spinbutton, code)
        return w
    
    def ev_spinbutton(self, w, code):
        """Callback for spinbuttons."""
        self.app.prefm.apply_pref(code, w.get_value_as_int())
        return
    
    def build_fontbutton(self, code, lv, cv):
        """Build a fontbutton."""
        w = gtk.FontButton()
        w.set_show_style(True)
        w.set_show_size(True)
        w.set_use_font(True)
        w.set_use_size(False)
        if cv is not None:
            w.set_font_name(cv)
        w.connect('font-set', self.ev_fontbutton, code)
        return w
    
    def ev_fontbutton(self, w, code):
        """Callback for fontbuttons."""
        self.app.prefm.apply_pref(code, w.get_font_name())
        return


#------------------------------------------------------------------------------

class PrefsWinPlugins(gtk.VBox):
    """'Plugins' tab of the preferences dialog."""
    
    def __init__(self, app):
        gtk.VBox.__init__(self)
        self.app = app
        self.set_spacing(9)
        self.set_border_width(15)
        # TreeView
        self.build_treeview()
        sv = gtk.ScrolledWindow()
        sv.set_policy(gtk.POLICY_NEVER, gtk.POLICY_ALWAYS)
        sv.set_shadow_type(gtk.SHADOW_IN)
        sv.add(self.tv)
        self.pack_start(sv, True, True)
        # ButtonBox
        hbb = gtk.HButtonBox()
        hbb.set_layout(gtk.BUTTONBOX_END)
        b = gtk.Button(stock=gtk.STOCK_ABOUT)
        b.connect('clicked', self.ev_about)
        hbb.pack_start(b)
        self.pack_start(hbb, False, True)
    
    def build_treeview(self):
        """Build the treeview containing the plugins list."""
        # Model
        self.tm = gtk.ListStore(str, bool, str)
        for p in self.app.plugm.list_available_plugins():
            a = self.app.plugm.is_loaded(p)
            n = self.app.plugm.get_plugin_info(p, 'Name', True)
            d = self.app.plugm.get_plugin_info(p, 'Description', True)
            self.tm.append([p, a, "<b>"+n+"</b>"+'\n'+d])
        # View
        self.tv = gtk.TreeView()
        self.tv.set_model(self.tm)
        self.tv.set_headers_visible(False)
        self.tv.get_selection().set_mode(gtk.SELECTION_SINGLE)
        # Column 1
        cr = gtk.CellRendererToggle()
        cr.props.xpad = 9
        cr.connect('toggled', self.ev_toggled)
        c = gtk.TreeViewColumn("Active", cr, active=1)
        c.set_expand(False)
        self.tv.append_column(c)
        # Column 2
        cr = gtk.CellRendererText()
        cr.props.ellipsize = pango.ELLIPSIZE_END
        c = gtk.TreeViewColumn("Plugin", cr, markup=2)
        c.set_expand(True)
        self.tv.append_column(c)
        self.tm.set_sort_column_id(2, gtk.SORT_ASCENDING)
        return
    
    def ev_toggled(self, cr, path):
        """Handle click on toggle button."""
        iter = self.tm.get_iter(path)
        p = self.tm.get_value(iter, 0)
        if self.tm.get_value(iter, 1):
            self.app.plugm.unload_plugin(p)
        else:
            self.app.plugm.load_plugin(p)
        v = self.app.plugm.is_loaded(p)
        self.tm.set_value(iter, 1, v)
        return
    
    def ev_about(self, *data):
        """Handle click on about button."""
        (model, iter) = self.tv.get_selection().get_selected()
        if iter:
            plugin = model.get_value(iter, 0)
            infos = {}
            for i in ['Name','Description','Version','Authors','License','Copyright','Website']:
                infos[i] = self.app.plugm.get_plugin_info(plugin, i, True)
            dwin = AboutPluginWin(self.get_toplevel(), infos)
            dwin.run()
            dwin.destroy()
        return


#------------------------------------------------------------------------------

class OpenWin(gtk.FileChooserDialog):
    """Open file dialog."""
    
    def __init__(self, app):
        buttons = (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK)
        action = gtk.FILE_CHOOSER_ACTION_OPEN
        gtk.FileChooserDialog.__init__(self, _("Open..."), app.gui.win, action, buttons)
        # Window
        self.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
        self.set_modal(True)
        self.set_destroy_with_parent(True)
        # Encoding
        hb = gtk.HBox()
        l = gtk.Label(_("Character encoding:"))
        l.set_alignment(1, 0.5)
        l.set_padding(7, 0)
        hb.pack_start(l, True, True)
        cb = gtk.combo_box_entry_new_text()
        cb.append_text("UTF-8")
        cb.append_text("Latin1")
        cb.append_text("Latin9")
        cb.append_text("Windows-1252")
        cb.set_active(0)
        hb.pack_start(cb, False, True)
        self.set_extra_widget(hb)
        hb.show_all()
        # Files
        filters = {_("All files"):["*"], _("LaTeX files"):["*.tex","*.bib"]}
        for txt,exts in filters.iteritems():
            f = gtk.FileFilter()
            f.set_name(txt)
            for e in exts:
                f.add_pattern(e)
            self.add_filter(f)
        self.set_select_multiple(True)


#------------------------------------------------------------------------------

class SaveWin(gtk.FileChooserDialog):
    """Save file dialog."""
    
    def __init__(self, app, filename=None, fileobj=None):
        buttons = (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_SAVE, gtk.RESPONSE_OK)
        action = gtk.FILE_CHOOSER_ACTION_SAVE
        gtk.FileChooserDialog.__init__(self, _("Save..."), app.gui.win, action, buttons)
        # Window
        self.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
        self.set_modal(True)
        self.set_destroy_with_parent(True)
        # Files
        if fileobj is not None:
            self.select_uri(fileobj.uri)
        if filename is not None:
            self.set_current_name(filename)
        self.set_do_overwrite_confirmation(True)


#------------------------------------------------------------------------------

class MsgWin(gtk.MessageDialog):
    """Message dialog."""
    
    def __init__(self, app, mtype, buttons, txt):
        # Dialog initialization
        flags = gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT
        b = getattr(gtk, "BUTTONS_"+buttons.upper())
        t = getattr(gtk, "MESSAGE_"+mtype.upper())
        gtk.MessageDialog.__init__(self, app.gui.win, flags, t, b, txt)
        self.set_position(gtk.WIN_POS_CENTER_ON_PARENT)


#------------------------------------------------------------------------------

class AboutPluginWin(gtk.AboutDialog):
    """About dialog for plugins."""
    
    def __init__(self, parent, infos):
        gtk.AboutDialog.__init__(self)
        # Window
        self.set_transient_for(parent)
        self.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
        self.set_modal(True)
        self.set_destroy_with_parent(True)
        # Data
        f = lambda x: x.strip()
        for i,v in infos.iteritems():
            i = i.lower()
            i = "comments" if i == "description" else i
            v = map(f, v.split(",")) if i == "authors" and v is not None else v
            func = getattr(self, "set_"+i)
            func(v)


#------------------------------------------------------------------------------

class AboutWin(gtk.AboutDialog):
    """About dialog."""
    
    def __init__(self, app):
        gtk.AboutDialog.__init__(self)
        # Window
        self.set_transient_for(app.gui.win)
        self.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
        self.set_modal(True)
        self.set_destroy_with_parent(True)
        # Data
        self.set_name(_("Euphorbia"))
        self.set_comments(_("GTK LaTeX editor"))
        self.set_version(euphorbia_version)
        self.set_license(euphorbia_license)
        self.set_authors(euphorbia_authors)
        self.set_copyright("Copyright \xc2\xa9 2008-2010   Bzoloid")
        self.set_website("http://euphorbia.googlecode.com/")
        self.set_logo_icon_name("euphorbia")


#------------------------------------------------------------------------------



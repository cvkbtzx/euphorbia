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

TXTBOLD = pango.AttrList()
TXTBOLD.insert(pango.AttrWeight(pango.WEIGHT_BOLD, 0, -1))
ENCODINGS = ["UTF-8", "Latin1", "Latin9", "Windows-1252"]


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
        # Populate
        self.nbook = gtk.Notebook()
        self.nbook.set_tab_pos(gtk.POS_LEFT)
        self.nbook.set_border_width(9)
        self.vbox.pack_start(self.nbook, True, True)
        self.vbox.show_all()
        for p in self.app.gui.prefs_tabs:
            self.nbook.append_page(p[1](app), gtk.Label(p[0]))
        self.app.prefm.autoconnect_gtk(self)
        self.set_default_response(gtk.RESPONSE_CLOSE)


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
            f.props.label_widget.set_attributes(TXTBOLD)
            f.props.label_widget.set_text(_("opt_"+cg))
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
        self.show_all()
    
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
            if lv == 'text':
                w = self.build_textentry(code, lv, cv)
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
    
    def build_textentry(self, code, lv, cv):
        """Build a textentry."""
        w = gtk.Entry()
        w.set_text(cv)
        w.connect('changed', self.ev_textentry, code)
        return w
     
    def ev_textentry(self, w, code):
        """Callback for textentries."""
        self.app.prefm.apply_pref(code, w.get_text())
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
        w.connect('value-changed', self.ev_spinbutton, code)
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
        w.set_use_font(False)
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
        sw = gtk.ScrolledWindow()
        sw.set_policy(gtk.POLICY_NEVER, gtk.POLICY_ALWAYS)
        sw.set_shadow_type(gtk.SHADOW_IN)
        sw.add(self.tv)
        self.pack_start(sw, True, True)
        # ButtonBox
        hbb = gtk.HButtonBox()
        hbb.set_layout(gtk.BUTTONBOX_END)
        b = gtk.Button(stock=gtk.STOCK_ABOUT)
        b.connect('clicked', self.ev_about)
        hbb.pack_start(b)
        self.pack_start(hbb, False, True)
        self.show_all()
    
    def build_treeview(self):
        """Build the treeview containing the plugins list."""
        # Model
        self.tm = gtk.ListStore(str, bool, str, pango.AttrList)
        for p in self.app.plugm.list_available_plugins():
            a = self.app.plugm.is_loaded(p)
            n = self.app.plugm.get_plugin_info(p, 'Name', True)
            d = self.app.plugm.get_plugin_info(p, 'Description', True)
            l = pango.AttrList()
            l.insert(pango.AttrWeight(pango.WEIGHT_BOLD, 0, len(n)))
            self.tm.append([p, a, n+'\n'+d, l])
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
        c = gtk.TreeViewColumn("Plugin", cr, text=2, attributes=3)
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
            ret = self.app.plugm.load_plugin(p)
            if not ret:
                msg = _("Plugin '%s' loading error") % (p)
                self.app.gui.disp_message('error', 'close', msg)
        v = self.app.plugm.is_loaded(p)
        self.tm.set_value(iter, 1, v)
        return
    
    def ev_about(self, *data):
        """Handle click on about button."""
        (model, iter) = self.tv.get_selection().get_selected()
        if iter:
            plugin = model.get_value(iter, 0)
            infos = {}
            for i in ['Name','Description','Authors','License','Copyright','Website']:
                infos[i] = self.app.plugm.get_plugin_info(plugin, i, True)
            dwin = AboutPluginWin(self.get_toplevel(), infos)
            dwin.run()
            dwin.destroy()
        return


#------------------------------------------------------------------------------

class PrefsWinLatex(gtk.VBox):
    """'LaTeX' tab of the preferences dialog."""
    
    def __init__(self, app):
        gtk.VBox.__init__(self)
        self.add(gtk.Label("empty"))
        self.show_all()


#------------------------------------------------------------------------------

class OpenWin(gtk.FileChooserDialog):
    """Open file dialog."""
    
    def __init__(self, app, folder=None, handler='latex'):
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
        for e in ENCODINGS:
            cb.append_text(e)
        cb.set_active(0)
        hb.pack_start(cb, False, True)
        self.set_extra_widget(hb)
        hb.show_all()
        # Files
        self.set_local_only(False)
        if folder is not None:
            self.set_current_folder_uri(folder)
        self.filters = {}
        for h in app.gui.file_handlers:
            f = gtk.FileFilter()
            f.set_name(h[1])
            for e in h[2]:
                f.add_pattern(e)
            self.add_filter(f)
            self.filters[h[0]] = f
        self.set_filter(self.filters[handler])
        self.set_select_multiple(True)
    
    def get_filter_name(self):
        """Get currently selected filter."""
        cf = self.get_filter()
        r = ''.join(n if f is cf else '' for n,f in self.filters.iteritems())
        return 'all' if r == '' else r


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
        self.set_local_only(False)
        if fileobj is not None:
            self.select_uri(fileobj.uri)
        elif filename is not None:
            self.set_current_name(filename)
        self.set_do_overwrite_confirmation(True)


#------------------------------------------------------------------------------

class SaveBeforeCloseWin(gtk.Dialog):
    """Dialog that propose to save before quitting."""
    
    def __init__(self, app, tabnames):
        # Dialog initialization
        flags = gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT
        buttons = (
            _("Ignore all"), gtk.RESPONSE_REJECT,
            gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
            gtk.STOCK_SAVE, gtk.RESPONSE_OK,
        )
        gtk.Dialog.__init__(self, _("Save..."), app.gui.win, flags, buttons)
        self.set_default_size(400, 250)
        self.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
        self.set_has_separator(True)
        vb = gtk.VBox()
        vb.set_spacing(7)
        vb.set_border_width(9)
        self.vbox.add(vb)
        # Message
        lab = gtk.Label(_("SaveBeforeClose?"))
        lab.set_alignment(0, 0.5)
        lab.set_padding(0, 5)
        vb.pack_start(lab, False, True)
        # Treeview
        self.tabnames = sorted(tabnames, key=lambda x: x[1])
        self.build_treeview()
        sw = gtk.ScrolledWindow()
        sw.set_policy(gtk.POLICY_NEVER, gtk.POLICY_ALWAYS)
        sw.set_shadow_type(gtk.SHADOW_IN)
        sw.add(self.tv)
        vb.pack_start(sw, True, True)
        # Display
        self.set_default_response(gtk.RESPONSE_OK)
        self.vbox.show_all()
    
    def build_treeview(self):
        """Build treeview containing filenames."""
        # Model
        self.numtabs = {}
        self.tm = gtk.ListStore(int, bool, str)
        for n,t in enumerate(self.tabnames):
            self.numtabs[n] = t[0]
            self.tm.append([n, True, t[1]])
        # View
        self.tv = gtk.TreeView()
        self.tv.set_model(self.tm)
        self.tv.set_headers_visible(False)
        self.tv.get_selection().set_mode(gtk.SELECTION_NONE)
        self.tv.props.can_focus = False
        # Column 1
        cr = gtk.CellRendererToggle()
        cr.props.xpad = 9
        cr.connect('toggled', self.ev_toggled)
        c = gtk.TreeViewColumn("Save", cr, active=1)
        c.set_expand(False)
        self.tv.append_column(c)
        # Column 2
        cr = gtk.CellRendererText()
        cr.props.ellipsize = pango.ELLIPSIZE_MIDDLE
        c = gtk.TreeViewColumn("File", cr, text=2)
        c.set_expand(True)
        self.tv.append_column(c)
        return
    
    def ev_toggled(self, cr, path):
        """Handle click on toggle button."""
        iter = self.tm.get_iter(path)
        v = self.tm.get_value(iter, 1)
        self.tm.set_value(iter, 1, not v)
        return
    
    def get_tabs_to_save(self):
        """Get list of tabs to save."""
        lst, n, gv = [], self.numtabs, self.tm.get_value
        f = lambda m,p,i: lst.append(n[gv(i,0)]) if gv(i,1) else None
        self.tm.foreach(f)
        return lst


#------------------------------------------------------------------------------

class MsgWin(gtk.MessageDialog):
    """Message dialog."""
    
    def __init__(self, parent, mtype, buttons, txt):
        # Dialog initialization
        flags = gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT
        b = getattr(gtk, "BUTTONS_"+buttons.upper())
        t = getattr(gtk, "MESSAGE_"+mtype.upper())
        gtk.MessageDialog.__init__(self, parent, flags, t, b, txt)
        self.set_title(_("Euphorbia"))
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
            v = map(f, v.split(",")) if i=="authors" and v is not None else v
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



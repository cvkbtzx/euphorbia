# -*- coding:utf-8 -*-

"""Various dialog windows."""

import gtk


#------------------------------------------------------------------------------

class PrefsWin(gtk.Dialog):
    """Preferences dialog."""
    
    def __init__(self, app):
        # Dialog initialization
        flags = gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT
        buttons = (gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE)
        gtk.Dialog.__init__(self, "Preferences", app.gui.win, flags, buttons)
        self.app = app
        self.set_default_size(600, 400)
        self.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
        self.set_has_separator(False)
        self.set_default_response(gtk.RESPONSE_CLOSE)
        # Populate
        self.nbook = gtk.Notebook()
        self.nbook.set_tab_pos(gtk.POS_LEFT)
        self.nbook.set_border_width(9)
        self.vbox.pack_start(self.nbook, True, True)
        self.nbook.append_page(PrefsWinGeneral(app), gtk.Label("General"))
        self.nbook.append_page(gtk.Label("empty"), gtk.Label("LaTeX"))
        self.nbook.append_page(gtk.Label("empty"), gtk.Label("Plugins"))
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
            f.props.label_widget.set_markup("<b>"+cg.capitalize()+"</b>")
            vb = gtk.VBox()
            vb.set_homogeneous(True)
            vb.set_spacing(3)
            vb.set_border_width(7)
            for code,w in sorted(categs[cg], key=lambda x: x[0]):
                l = gtk.Label(code)
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
        vals = lv.items()
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

class OpenWin(gtk.FileChooserDialog):
    """Open file dialog."""
    
    def __init__(self, app):
        buttons = (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK)
        action = gtk.FILE_CHOOSER_ACTION_OPEN
        gtk.FileChooserDialog.__init__(self, "Open...", app.gui.win, action, buttons)
        # Window
        self.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
        self.set_modal(True)
        self.set_destroy_with_parent(True)
        # Encoding
        hb = gtk.HBox()
        l = gtk.Label("Character encoding:")
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
        filters = {"All files":["*"], "LaTeX files":["*.tex","*.bib"]}
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
    
    def __init__(self, app, filename):
        buttons = (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_SAVE, gtk.RESPONSE_OK)
        action = gtk.FILE_CHOOSER_ACTION_SAVE
        gtk.FileChooserDialog.__init__(self, "Save...", app.gui.win, action, buttons)
        # Window
        self.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
        self.set_modal(True)
        self.set_destroy_with_parent(True)
        # Files
        self.set_current_name(filename)
        self.set_do_overwrite_confirmation(True)


#------------------------------------------------------------------------------


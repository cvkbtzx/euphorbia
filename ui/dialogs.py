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
        self.set_default_size(500, 350)
        self.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
        self.set_has_separator(False)
        self.set_default_response(gtk.RESPONSE_CLOSE)
        # Populate
        self.nbook = gtk.Notebook()
        self.nbook.set_tab_pos(gtk.POS_LEFT)
        self.nbook.set_border_width(7)
        self.vbox.pack_start(self.nbook, True, True)
        self.nbook.append_page(PrefsWinGeneral(app), gtk.Label("General"))
        self.nbook.append_page(gtk.Label("empty"), gtk.Label("LaTeX"))
        self.vbox.show_all()


class PrefsWinGeneral(gtk.ScrolledWindow):
    """'General' tab of the preferences dialog."""
    
    def __init__(self, app):
        gtk.ScrolledWindow.__init__(self)
        self.app = app
        self.set_policy(gtk.POLICY_NEVER, gtk.POLICY_ALWAYS)
        container = gtk.VBox()
        container.set_homogeneous(True)
        container.set_spacing(3)
        container.set_border_width(5)
        self.add_with_viewport(container)
        container.get_parent().set_shadow_type(gtk.SHADOW_NONE)
        for code,lv,cv in self.app.prefm.iter_prefs():
            l = gtk.Label(code)
            l.set_alignment(0, 0.5)
            l.set_padding(5, 0)
            t = self.build_widget(code, lv, cv)
            if t is None:
                continue
            hb = gtk.HBox()
            hb.pack_start(l, True, True)
            hb.pack_start(t, False, True)
            container.pack_start(hb, False, False)
    
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


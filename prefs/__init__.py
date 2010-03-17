# -*- coding:utf-8 -*-

PREFS_DIR = "./"

PREFS = [
    ("gui.uim.get_widget('/MainToolbar').set_show_arrow", [True, False], 0, True),
    ("gui.uim.get_widget('/MainToolbar').set_icon_size", {"menu":1, "small-tool":2, "large-tool":3, "button":4, "dnd":5, "dialog":6}, "menu", 1),
    ("gui.uim.get_widget('/MainToolbar').set_tooltips", [True, False], 0, True),
    ("gui.uim.get_widget('/MainToolbar').set_style", {"icon":0, "text":1, "text under icon":2, "text alongside icon":3}, "icon", 0),
]

DEFAULT_PREFS = {
    # Key:              [function, {values}, index_default_value, current_value]
    "toolbar_arrow":    ['toolbar*/set_show_arrow', [False, True], 1, True],
    "toolbar_iconsize": ['toolbar*/set_icon_size', {"menu":1, "small-tool":2, "large-tool":3, "button":4, "dnd":5, "dialog":6}, "menu", 1],
    "toolbar_tooltips": ['toolbar*/set_tooltips', [False, True], 1, True],
    "toolbar_style":    ['toolbar*/set_style', {"icon":0, "text":1, "text under icon":2, "text alongside icon":3}, "icon", 0],
}


#------------------------------------------------------------------------------

class PrefsManager:
    """Class used to manage preferences."""
    
    def __init__(self):
        self.prefs = DEFAULT_PREFS
        self.widgets = {}
    
    def set_func(self, name, func):
        """Set function associated with given pref name."""
        if name in self.prefs:
            self.prefs[name][0] = func
            return True
        else:
            return False
    
    def set_pref_value(self, name, value=None, index=None):
        """Set pref, either from index or with direct value."""
        if (value is not None) and (index is not None):
            return
        if value is not None:
            self.prefs[name][-1] = value
        if index is not None:
            self.prefs[name][-1] = self.prefs[name][1][index]
        if (value is None) and (index is None):
            self.prefs[name][-1] = self.prefs[name][1][self.prefs[name][2]]
        return
    
    def apply(self, name):
        """Execute function associated with given pref name."""
        func = self.prefs[name][0]
        if type(func) is str:
            obj, fn = func.split('/')
            if obj[-1] == '*':
                objs = [w for w in self.widgets.iterkeys() if w.startswith(obj[:-1])]
            else:
                objs = [self.widgets[obj]]
            for o in objs:
                for w in self.widgets[o]:
                    f = getattr(w, fn)
                    f(self.prefs[name][-1])
        else:
            func(self.prefs[name][-1])
        return
    
    def apply_all(self):
        """Apply all prefs."""
        for pref in self.prefs.keys():
            self.apply(pref)
        return
    
    def build_widget_dict(self, parent):
        """Build and memorize a list of all widgets with their name."""
        self.widgets.clear()
        self.__widgets_scan(parent, self.widgets)
        ###for w in self.widgets:
        ###    print w
        return
    
    def __widgets_scan(self, w, d):
        """Scan widgets recursively."""
        if hasattr(w, 'get_children'):
            for c in w.get_children():
                self.__widgets_scan(c, d)
        name = w.get_name()
        if name:
            if d.has_key(name):
                d[name].append(w)
            else:
                d[name] = [w]
        return
    
    def load(self):
        """Load prefs from file."""
        return
    
    def save(self):
        """Save prefs in file."""
        return


#------------------------------------------------------------------------------



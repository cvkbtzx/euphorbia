# -*- coding:utf-8 -*-

"""Preferences manager."""

from defaults import *


#------------------------------------------------------------------------------

class PrefsManager:
    """Class used to manage preferences."""
    
    def __init__(self):
        self.codes = {}
        self.types = {}
        for p in DEFAULT_PREFS:
            self.add_pref(*p)
    
    def add_pref(self, code, func, lvals, val, type=None):
        """Add a pref from (code, func, list_values, default_value)."""
        self.codes[code] = [set(), func, lvals, val]
        if type is not None:
            if type in self.types:
                self.types[type].add(code)
            else:
                self.types[type] = set([code])
        return
    
    def del_pref(self, code):
        """Delete pref from its code."""
        for t,c in self.types.iteritems():
            if code in c:
                c.remove(code)
            if not c:
                del self.types[t]
        if code in self.codes:
            del self.codes[code]
        return
    
    def connect_pref(self, obj, code):
        """Connect an object to a pref."""
        if code in self.codes:
            self.codes[code][0].add(obj)
            return True
        else:
            return False
    
    def connect_prefs_by_type(self, obj):
        """Connect an object to all prefs matching its type."""
        if not hasattr(obj, 'name'):
            return
        name = obj.name
        clst = self.types[name] if name in self.types else set([])
        for t,c in self.types.iteritems():
            if name.startswith(t[:-1]) and t[-1]=='*':
                clst.update(c)
        for c in clst:
            self.connect_pref(obj, c)
        return
    
    def autoconnect_gtk(self, parentobj):
        """Scan GTK widgets recursively and connect prefs from type."""
        if hasattr(parentobj, 'name'):
            if parentobj.name:
                self.connect_prefs_by_type(parentobj)
        if hasattr(parentobj, 'get_children'):
            for c in parentobj.get_children():
                self.autoconnect_gtk(c)
        return
    
    def disconnect_pref(self, obj, code):
        """Disconnect an object to a pref."""
        if code in self.codes:
            if obj in self.codes[code][0]:
                self.codes[code][0].remove(obj)
        return
    
    def list_prefs(self, obj):
        """List prefs connected with given object."""
        return [c for c in self.codes if obj in self.codes[c][0]]
    
    def set_pref(self, code, val):
        """Assign a value to a pref."""
        if code in self.codes:
            if type(self.codes[code][2]) is dict:
                if val not in self.codes[code][2].values():
                    return False
            self.codes[code][-1] = val
            return True
        else:
            return False
    
    def get_pref(self, code):
        """Get pref's current value."""
        return self.codes[code][-1] if code in self.codes else None
    
    def get_pref_values(self, code):
        """Get allowed pref's values."""
        return self.codes[code][2] if code in self.codes else None
    
    def apply_pref(self, code, *user_data):
        """Execute the pref's function."""
        fname = self.codes[code][1]
        if type(fname) is dict:
            fname = fname[self.codes[code][-1]]
        for obj in self.codes[code][0]:
            f = getattr(obj, fname)
            f(self.codes[code][-1], *user_data)
        return
    
    def apply_all_prefs(self):
        """Execute all pref's functions."""
        for c in self.codes:
            self.apply_pref(c)
        return


#------------------------------------------------------------------------------



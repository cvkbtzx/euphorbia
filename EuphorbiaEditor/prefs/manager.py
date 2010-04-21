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


"""Preferences manager."""

import os
import os.path
import pickle

from defaults import *


#------------------------------------------------------------------------------

class PrefsManager:
    """Class used to manage preferences."""
    
    def __init__(self, cfgfile, use_defaults_only):
        self.cfgfile = cfgfile
        self.codes = {}
        self.types = {}
        self.load(use_defaults_only)
    
    def has_pref(self, code):
        """Get if a pref exists."""
        return code in self.codes
    
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
        """Connect a pref to an object."""
        if code in self.codes:
            self.codes[code][0].add(obj)
            self.apply_pref(code, object=obj)
            return True
        else:
            return False
    
    def connect_prefs_by_type(self, obj):
        """Connect all prefs matching an object type to this object."""
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
    
    def iter_prefs_data(self):
        """Iter on all prefs."""
        for c,v in self.codes.iteritems():
            yield (c, v[2], v[-1])
        return
    
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
    
    def set_pref_values(self, code, vals):
        """Set allowed pref's values."""
        if code in self.codes:
            self.codes[code][2] = vals
        return
    
    def get_pref_values(self, code):
        """Get allowed pref's values."""
        return self.codes[code][2] if code in self.codes else None
    
    def apply_pref(self, code, val=None, object=None):
        """Execute the pref's function."""
        if val is not None:
            self.set_pref(code, val)
        fname = self.codes[code][1]
        if fname is None:
            return
        if type(fname) is dict:
            fname = fname[self.codes[code][-1]]
            args = ()
        else:
            args = (self.codes[code][-1],)
        objs = self.codes[code][0] if object is None else [object]
        for obj in objs:
            f = getattr(obj, fname)
            f(*args)
        return
    
    def apply_all_prefs(self):
        """Execute all pref's functions."""
        for c in self.codes:
            self.apply_pref(c)
        return
    
    def load(self, default=False):
        """Load prefs from file."""
        if os.path.isfile(self.cfgfile) and not default:
            with open(self.cfgfile, 'r') as f:
                save = pickle.load(f)
            if type(save) is tuple:
                if len(save)==2 and all(map(lambda x: type(x) is dict, save)):
                    self.codes = save[0]
                    self.types = save[1]
        if len(self.codes) * len(self.types) == 0:
            self.codes, self.types = {}, {}
            for p in DEFAULT_PREFS:
                self.add_pref(*p)
        return
    
    def store(self):
        """Store prefs in file."""
        save = {}
        for code,v in self.codes.iteritems():
            save[code] = [set()] + v[1:]
        dirname = os.path.dirname(self.cfgfile)
        if not os.path.isdir(dirname):
            os.makedirs(dirname, 0755)
        with open(self.cfgfile, 'w') as f:
            pickle.dump((save, self.types), f)
        return


#------------------------------------------------------------------------------



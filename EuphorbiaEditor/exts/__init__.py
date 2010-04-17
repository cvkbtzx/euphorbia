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


"""Plugins management."""

import sys
import os
import os.path
import ConfigParser

import euphorbia
sys.modules['euphorbia'] = sys.modules['EuphorbiaEditor.exts.euphorbia']


#------------------------------------------------------------------------------

class PluginsManager:
    """Class to manage plugins."""
    
    def __init__(self, app):
        self.app = app
        setattr(euphorbia, 'app', self.app)
        self.find_plugins_paths()
        self.plugins = {}
        self.detect_plugins()
        self.instances = {}
        return
    
    def load_plugin(self, plugin):
        """Load plugin."""
        if plugin in self.instances:
            return False
        ret = False
        try:
            for p in self.paths:
                self.add_plugin_path(p)
            __import__(plugin, None, None, [''])
            for p in self.paths:
                self.del_plugin_path(p)
            sc = [sc for sc in euphorbia.Plugin.__subclasses__() if sc.__module__ == plugin]
            if len(sc) != 1:
                raise AttributeError("Too much euphorbia.Plugin subclasses")
            plugclass = sc[0]
            pluginstance = plugclass()
            pluginstance.activate()
        except StandardError:
            print "\nError in plugin '%s':" % (plugin)
            sys.excepthook(*sys.exc_info())
            print ""
        else:
            self.instances[plugin] = pluginstance
            ret = True
        return ret
    
    def unload_plugin(self, plugin):
        """Unload plugin."""
        if plugin not in self.instances:
            return False
        pluginstance = self.instances[plugin]
        ret = False
        try:
            pluginstance.deactivate()
            del self.instances[plugin]
            del pluginstance
        except StandardError:
            print "\nError in plugin '%s':" % (plugin)
            sys.excepthook(*sys.exc_info())
            print ""
        else:
            ret = True
        return ret
    
    def add_plugin_path(self, path):
        """Add given path to PYTHONPATH."""
        if not path in sys.path:
            sys.path.insert(0, path)
        return
    
    def del_plugin_path(self, path):
        """Remove given path from PYTHONPATH."""
        if path in sys.path:
            sys.path.remove(path)
        return
    
    def stop_all_plugins(self):
        """Deactivate all plugins."""
        for p in self.instances.keys():
            self.unload_plugin(p)
        return
    
    def is_loaded(self, plugin):
        """Check if the given plugin is loaded."""
        return plugin in self.instances
    
    def list_loaded_plugins(self):
        """List plugins which have been loaded."""
        return self.instances.keys()
    
    def detect_plugins(self):
        """Detect available plugins and retrieve informations."""
        self.plugins.clear()
        opts = ['Module', 'Name', 'Description']
        sect = "Euphorbia Plugin"
        ext = ".euphorbia-plugin"
        for p in self.paths:
            for f in [i for i in os.listdir(p) if i.endswith(ext)]:
                cp = ConfigParser.RawConfigParser()
                with open(os.path.join(p,f), 'r') as fp:
                    cp.readfp(fp)
                test = all(cp.has_option(sect, o) for o in opts)
                if not test:
                    continue
                self.plugins[cp.get(sect, 'Module')] = cp
        return
    
    def get_plugin_info(self, pname, opt, loc=False):
        """Get plugin's data (try to localize if loc=True)."""
        sect = "Euphorbia Plugin"
        cp = self.plugins[pname]
        onames = [opt]
        if loc:
            lng = self.app.locale[0]
            if lng is not None:
                if '_' in lng:
                    onames.append(opt+"["+lng.split('_')[0]+"]")
                onames.append(opt+"["+lng+"]")
        ret = None
        for i in onames:
            if cp.has_option(sect, i):
                ret = cp.get(sect, i)
        return ret
    
    def list_available_plugins(self):
        """List available plugins."""
        return self.plugins.keys()
    
    def find_plugins_paths(self):
        """Setup plugins paths."""
        self.paths = []
        for d in ["maindir", "datadir"]:
            p = self.app.prefm.get_pref("system_"+d)
            dir = os.path.join(p, "plugins")
            if os.path.isdir(dir):
                self.paths.append(dir)
        return


#------------------------------------------------------------------------------



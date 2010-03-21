# -*- coding:utf-8 -*-

"""Plugins management."""

import sys
import euphorbia

sys.modules['euphorbia'] = sys.modules['plugins.euphorbia']


#------------------------------------------------------------------------------

class PluginsManager:
    """Class to manage plugins."""
    
    def __init__(self, mainapp):
        self.paths = ["/mnt/data/prog/python/euphorbia/archives/plugins"]
        setattr(euphorbia, 'app', mainapp)
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
            print ""
            print "ERROR in plugin '%s':" % (plugin)
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
            print ""
            print "ERROR in plugin '%s':" % (plugin)
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
    
    def list_loaded_plugins(self):
        """List plugins which have been loaded."""
        return self.instances.keys()
    
    def get_available_plugins(self):
        """List available plugins."""
        return ['kikoo']


#------------------------------------------------------------------------------



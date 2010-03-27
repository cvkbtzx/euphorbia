# -*- coding:utf-8 -*-

"""Execute external programms."""

import gobject


#------------------------------------------------------------------------------

class SpawnManager:
    """Class that can run an external prog."""
    
    def __init__(self, exe, pwd, func):
        self.exe = exe
        self.pwd = pwd
        self.func = func
        self.pid = None
    
    def run(self):
        """Start the programm."""
        data = gobject.spawn_async(self.exe, None, self.pwd, 0, None, None, False, True, True)
        self.pid = data[0]
        gobject.child_watch_add(self.pid, self.callback, tuple(data[2:]))
        return
    
    def callback(self, pid, condition, *data):
        """Callback to execute when the programm exits."""
        self.func(*data)
        return


#------------------------------------------------------------------------------



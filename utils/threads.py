# -*- coding:utf-8 -*-

"""Threads management."""

import gobject
import threading

gobject.threads_init()


#------------------------------------------------------------------------------

class ThreadManager(threading.Thread):
    """Class that can run a function in another thread."""
    # Usage:
    #   tm = ThreadManager()
    #   tm.set_func(f, arg1, arg2, ...)
    #   tm.start()
    
    def __init__(self):
        threading.Thread.__init__(self)
        self.func = None
        self.args = None
    
    def set_func(self, func, *args):
        """Set the function (and arguments) to execute."""
        self.func = func
        self.args = args
    
    def run(self):
        self.func(*self.args)
        # Execute GUI stuff from func:
        #   gobject.idle_add(update_label, value)
        return


#------------------------------------------------------------------------------



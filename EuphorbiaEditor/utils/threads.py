#-*- coding:utf-8 -*-

##  EUPHORBIA - GTK LaTeX Editor
##  Module: EuphorbiaEditor.utils.threads
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


"""Threads management."""

import gobject
import threading


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



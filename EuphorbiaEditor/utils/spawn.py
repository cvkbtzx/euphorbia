# -*- coding:utf-8 -*-

##  EUPHORBIA - GTK LaTeX Editor
##  Module: EuphorbiaEditor.utils.spawn
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



#-*- coding:utf-8 -*-

##  EUPHORBIA - GTK LaTeX Editor
##  Module: EuphorbiaEditor.utils.spawn
##  Copyright (C) 2008-2011   Bzoloid
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

import os
import glib


#------------------------------------------------------------------------------

class SpawnManager(object):
    """Class that can run an external prog."""
    
    def __init__(self, exe, pwd, cb_end=None, cb_out=None, cb_err=None):
        self.exe = exe
        self.pwd = pwd
        self.cb_end = cb_end
        self.cb_out = cb_out
        self.cb_err = cb_err
        self.pid = None
        self.wid = [None, None]
    
    def run(self):
        """Start the programm."""
        flags = glib.SPAWN_SEARCH_PATH|glib.SPAWN_STDOUT_TO_DEV_NULL|glib.SPAWN_STDERR_TO_DEV_NULL
        try:
            data = glib.spawn_async(self.exe, [], self.pwd, flags, None, None, False, False, False)
            self.pid = data[0]
            glib.child_watch_add(self.pid, self.callback_end)
        except:
            return False
        return True
    
    def run_with_output(self):
        """Start the programm and retrieve the output."""
        flags = glib.SPAWN_SEARCH_PATH
        try:
            data = glib.spawn_async(self.exe, [], self.pwd, flags, None, None, False, True, True)
            self.pid = data[0]
            glib.child_watch_add(self.pid, self.callback_end)
        except:
            return False
        out = os.fdopen(data[2])
        err = os.fdopen(data[3])
        self.wid[0] = glib.io_add_watch(data[2], glib.IO_IN|glib.IO_HUP, self.callback_out, out)
        self.wid[1] = glib.io_add_watch(data[3], glib.IO_IN|glib.IO_HUP, self.callback_err, err)
        return True
    
    def callback_out(self, src, condition, data):
        """Callback to execute when the programm writes on std output."""
        if condition == glib.IO_HUP:
            data.close()
            self.callback_end(self.pid, None)
            return False
        if self.cb_out is not None:
            self.cb_out(data.readline())
        return True
    
    def callback_err(self, src, condition, data):
        """Callback to execute when the programm writes on err output."""
        if condition == glib.IO_HUP:
            data.close()
            self.callback_end(self.pid, None)
            return False
        if self.cb_err is not None:
            self.cb_err(data.readline())
        return True
    
    def callback_end(self, pid, condition):
        """Callback to execute when the programm exits."""
        if self.wid[0] is not None:
            glib.source_remove(self.wid[0])
        if self.wid[1] is not None:
            glib.source_remove(self.wid[1])
        if self.cb_end is not None:
            self.cb_end()
        return


#------------------------------------------------------------------------------

if __name__ == '__main__':
    import sys
    import gtk
    def disp(txt):
        if txt:
            print txt.replace('\n', '')
    end = lambda: gtk.main_quit()
    sm = SpawnManager(sys.argv[1:], "./", end, disp, None)
    sm.run_with_output()
    gtk.main()


#------------------------------------------------------------------------------



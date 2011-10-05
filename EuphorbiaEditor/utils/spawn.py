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
        self.end = [False, False]
        self.isrunning = False
    
    def run(self):
        """Start the programm and retrieve the output."""
        flags = glib.SPAWN_SEARCH_PATH | glib.SPAWN_DO_NOT_REAP_CHILD
        log("spawn > start > " + repr(self.exe))
        try:
            data = glib.spawn_async(self.exe, [], self.pwd, flags, None, None, False, True, True)
            self.pid = data[0]
            glib.child_watch_add(self.pid, self.callback_end)
        except:
            return False
        out = os.fdopen(data[2], 'r')
        err = os.fdopen(data[3], 'r')
        self.wid[0] = glib.io_add_watch(data[2], glib.IO_IN|glib.IO_HUP, self.read_callback, out, 1)
        self.wid[1] = glib.io_add_watch(data[3], glib.IO_IN|glib.IO_HUP, self.read_callback, err, 2)
        self.isrunning = True
        return True
    
    def is_running(self):
        """Check if the child process is running."""
        return self.isrunning
    
    def read_callback(self, src, condition, data, t):
        """Callback to execute when the programm writes on std output."""
        txt = data.readline()
        if txt:
            if (t == 1) and (self.cb_out is not None):
                self.cb_out(txt)
            if (t == 2) and (self.cb_err is not None):
                self.cb_err(txt)
        elif self.end[t-1]:
            log("spawn > closepipe > %d" % t)
            data.close()
            glib.source_remove(self.wid[t-1])
            return False
        if condition == glib.IO_HUP:
            self.end[t-1] = True
        return True
    
    def callback_end(self, pid, condition):
        """Callback to execute when the programm exits."""
        log("spawn > end")
        self.isrunning = False
        if self.cb_end is not None:
            self.cb_end()
        return


#------------------------------------------------------------------------------

if __name__ == '__main__':
    import sys
    import gtk
    import logm
    log = logm.log_main
    f_disp = sys.stdout.write
    f_end = lambda: glib.timeout_add(1000, gtk.main_quit)
    sm = SpawnManager(sys.argv[1:], "./", f_end, f_disp, None)
    sm.run()
    gtk.main()


#------------------------------------------------------------------------------



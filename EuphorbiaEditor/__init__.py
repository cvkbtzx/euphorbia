#!/usr/bin/python2
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


"""Euphorbia LaTeX editor."""

__version__ = '0.0.7'
__date__    = '2010-04-06'
__authors__  = ['Bzoloid <bzoloid@gmail.com>']
__license__ = 'GNU GPL v2'

import sys
import os
import os.path
import gettext

import ui
import prefs
import exts


#------------------------------------------------------------------------------

for var in ['version', 'date', 'authors', 'license']:
    __builtins__['euphorbia_'+var] = locals()['__'+var+'__']


#------------------------------------------------------------------------------

class Euphorbia:
    """Main class."""
    
    def __init__(self):
        # Command line args
        args = sys.argv[1:]
        root = os.path.dirname(__path__[0]) if "--test" in args else sys.prefix
        # Preferences and localization
        datadir = os.path.join(root, 'share', 'euphorbia')
        homedir = os.path.join(os.getenv('HOME'), '.config', 'euphorbia')
        locales = os.path.join(root, 'share', 'locale')
        gettext.install('euphorbia', locales)
        self.prefm = prefs.PrefsManager()
        self.prefm.set_pref('system_datadir', datadir)
        self.prefm.set_pref('system_homedir', homedir)
        # Load application
        self.plugm = exts.PluginsManager(self)
        self.gui = ui.EuphorbiaGUI(self)
        ###self.plugm.load_plugin('pdfview')
        self.prefm.autoconnect_gtk(self.gui.win)
        # Open files given in command line
        args = [a for a in args if not a.startswith("--")]
        if args:
            for f in args:
                self.gui.do_open(f)
        else:
            self.gui.act_new()
    
    def run(self):
        self.gui.main()


#------------------------------------------------------------------------------

if __name__ == "__main__":
    print "START"
    Euphorbia().run()
    print "STOP"


#------------------------------------------------------------------------------



#!/usr/bin/python2 -O
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

#------------------------------------------------------------------------------

"""Euphorbia: LaTeX editor."""

__version__ = '0.0.3'
__date__    = '2010-03-17'
__author__  = 'Bzoloid <bzoloid@gmail.com>'
__licence__ = 'GNU GPL v2'

import ui
import prefs


#------------------------------------------------------------------------------

class Euphorbia:
    """Main class."""
    
    def __init__(self):
        self.pm = prefs.PrefsManager()
        self.gui = ui.EuphorbiaGUI()
        self.pm.autoconnect_gtk(self.gui.win)
        self.pm.apply_all_prefs()
    
    def run(self):
        self.gui.main()


#------------------------------------------------------------------------------

if __name__ == "__main__":
    print "START"
    Euphorbia().run()
    print "STOP"


#------------------------------------------------------------------------------



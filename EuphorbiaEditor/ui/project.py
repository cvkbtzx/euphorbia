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


"""Project manager."""

import gtk


#------------------------------------------------------------------------------

class ProjectManager(object):
    """Manage project files."""
    
    def __init__(self, app, filename, **args):
        self.app = app
        self.rootdir = ""
        self.listfiles = {}
    
    def add_file(self, f):
        """"""
        # {"filename": [type, hlight, enc, open]}
        return
    
    def del_file(self, f):
        """"""
        return
    
    def add_tab(self, t):
        """"""
        return
    
    def del_tab(self, t):
        """"""
        return
    
    def list_files(self):
        """"""
        return
    
    def list_tabs(self):
        """"""
        return


#------------------------------------------------------------------------------



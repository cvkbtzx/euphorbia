#-*- coding:utf-8 -*-

##  EUPHORBIA - GTK LaTeX Editor
##  Module: EuphorbiaEditor.ui.outlogview
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


"""Interface to manage output log textviews."""

import gtk
import pango

from ..utils import spawn


#------------------------------------------------------------------------------

class OutputLogsView(object):
    """Manage output log textviews."""
    
    def __init__(self, app, builder):
        self.app = app
        self.tvout = builder.get_object('textview_out')
        self.tverr = builder.get_object('textview_err')
        self.tvout.modify_font(pango.FontDescription('Monospace 8'))
        self.tverr.modify_font(pango.FontDescription('Monospace 8'))
        self.tvout.get_buffer().connect('changed', self.ev_changed, self.tvout)
        self.tverr.get_buffer().connect('changed', self.ev_changed, self.tverr)
    
    def clear_logs(self):
        """Clear text logs."""
        self.tvout.get_buffer().set_text("")
        self.tverr.get_buffer().set_text("")
        return
    
    def ev_changed(self, buffer, view):
        """Handle changed event on output textviews."""
        a = view.get_vadjustment()
        a.set_value(a.get_upper())
        return


#------------------------------------------------------------------------------



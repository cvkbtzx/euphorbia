# -*- coding:utf-8 -*-

##  EUPHORBIA - GTK LaTeX Editor
##  Module: EuphorbiaEditor.utils.log
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


"""Logging management."""

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("euphorbia")


#------------------------------------------------------------------------------

def log_main(msg, ltype='debug'):
    """Display log in stdout."""
    # ltype: 'debug','info','warning','error','critical'
    getattr(logger, ltype)(msg)
    return


def log_null(*data):
    """Do not display log."""
    pass


#------------------------------------------------------------------------------



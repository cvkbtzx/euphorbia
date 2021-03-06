#!/usr/bin/python2
#-*- coding:utf-8 -*-

##  EUPHORBIA - GTK LaTeX Editor
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


"""Euphorbia LaTeX editor."""

__version__   = '0.0.12'
__authors__   = ['Bzoloid <bzoloid@gmail.com>']
__license__   = 'GNU GPL v2'
__copyright__ = "Copyright \xc2\xa9 2008-2011   Bzoloid"
__website__   = "https://github.com/cvkbtzx/euphorbia"

import sys
import os.path
import locale
import gettext
import glib

from . import ui
from . import prefs
from . import exts
from .utils import logm


#------------------------------------------------------------------------------

glib.threads_init()

for var in ['version', 'authors', 'license', 'copyright', 'website']:
    __builtins__['euphorbia_'+var] = locals()['__'+var+'__']

locale.setlocale(locale.LC_ALL, '')


#------------------------------------------------------------------------------

class Euphorbia(object):
    """Main class."""
    
    def __init__(self):
        # Command line args
        args = sys.argv[1:]
        testmode = True if "--test" in args else False
        root = os.path.dirname(__path__[0]) if testmode else sys.prefix
        debugmode = True if "--debug" in args else False
        __builtins__['log'] = logm.log_main if debugmode else logm.log_null
        # Directories and localization
        self.locale = locale.getlocale()
        maindir = os.path.join(root, 'share', 'euphorbia')
        datadir = os.path.join(glib.get_user_data_dir(), 'euphorbia')
        confdir = os.path.join(glib.get_user_config_dir(), 'euphorbia')
        cfgfile = os.path.join(confdir, 'euphorbia.cfg')
        locales = os.path.join(root, 'share', 'locale')
        gettext.install('euphorbia', locales)
        # Preferences
        self.prefm = prefs.PrefsManager(cfgfile, testmode)
        self.prefm.set_pref('system_maindir', maindir)
        self.prefm.set_pref('system_datadir', datadir)
        self.prefm.set_pref('system_confdir', confdir)
        # Load application
        self.plugm = exts.PluginsManager(self)
        self.gui = ui.EuphorbiaGUI(self)
        self._load_plugins()
        self.prefm.autoconnect_gtk(self.gui.win)
        # Open files given in command line
        args = [a for a in args if not a.startswith("--")]
        projfile = self.prefm.get_pref('files_lastprj')
        if len(args) > 0:
            for f in args:
                self.gui.do_open(f, 'all')
        elif self.prefm.get_pref('files_reopenprj') and projfile is not None:
            self.gui.do_open(projfile, 'project')
        else:
            self.gui.act_new()
    
    def _load_plugins(self):
        """Load plugins from saved list."""
        plugins = self.prefm.get_pref('plugins_list')
        availables = self.plugm.list_available_plugins()
        for p in sorted(plugins):
            ok = self.plugm.load_plugin(p) if p in availables else False
            if not ok:
                plugins.remove(p)
        return
    
    def run(self):
        """Run the programm."""
        self.gui.main()


#------------------------------------------------------------------------------

if __name__ == '__main__':
    print "START"
    Euphorbia().run()
    print "STOP"


#------------------------------------------------------------------------------



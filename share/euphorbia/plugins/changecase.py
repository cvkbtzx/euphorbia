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


"""Plugin to change text case."""

import gtk
import euphorbia

MENU = """
<menubar name="menu_main">
  <menu name="menu_edit" action="action_edit">
    <separator />
    <menu name="menu_changecase" action="action_changecase">
      <menuitem action="action_changecase_low" />
      <menuitem action="action_changecase_upp" />
      <menuitem action="action_changecase_cap" />
      <menuitem action="action_changecase_inv" />
    </menu>
  </menu>
</menubar>
"""


#------------------------------------------------------------------------------

class ChangeCase(euphorbia.Plugin):
    """Test plugin."""
    
    def __init__(self):
        euphorbia.Plugin.__init__(self)
        self.menu = None
        self.actgrp = gtk.ActionGroup('euphorbia')
        f = self.replace
        actions = [
            ('action_changecase',     None, _("Change case")),
            ('action_changecase_low', None, _("Lower"), None, None, f),
            ('action_changecase_upp', None, _("Upper"), None, None, f),
            ('action_changecase_cap', None, _("Capitalize"), None, None, f),
            ('action_changecase_inv', None, _("Invert"), None, None, f),
        ]
        self.actgrp.add_actions(actions)
    
    def activate(self):
        print "Hello!"
        self.app.gui.uim.insert_action_group(self.actgrp, -1)
        self.menu = self.app.gui.uim.add_ui_from_string(MENU)
    
    def deactivate(self):
        self.app.gui.uim.remove_ui(self.menu)
        self.app.gui.uim.remove_action_group(self.actgrp)
        print "Bye!"
    
    def replace(self, action):
        """Replace selected text after changing its case."""
        print action.get_name()
        mode = action.get_name().split('_')[-1]
        tab = self.app.gui.get_current_tab()
        if hasattr(tab, 'get_selection') and hasattr(tab, 'insert'):
            txt = tab.get_selection()
            if txt:
                if mode == "low":
                    txt = txt.lower()
                elif mode == "upp":
                    txt = txt.upper()
                elif mode == "cap":
                    txt = txt.title()
                elif mode == "inv":
                    txt = txt.swapcase()
                tab.insert(txt, True)
        return


#------------------------------------------------------------------------------


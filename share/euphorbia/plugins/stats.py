#-*- coding:utf-8 -*-

##  Stats plugin for Euphorbia LaTeX editor
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


"""Stats plugin."""

import gtk
import pango
import euphorbia

MENU = """
<menubar name="menu_main">
  <menu name="menu_tools" action="action_tools">
    <separator />
    <menuitem action="action_stats" />
  </menu>
</menubar>
"""


#------------------------------------------------------------------------------

class StatsPlugin(euphorbia.Plugin):
    """Stats plugin."""
    
    def __init__(self):
        euphorbia.Plugin.__init__(self)
        self.menu = None
        self.actgrp = gtk.ActionGroup('euphorbia')
        actions = [
            ('action_stats', None, _("Stats..."), None, None, self.disp_stats),
        ]
        self.actgrp.add_actions(actions)
    
    def activate(self):
        self.app.gui.uim.insert_action_group(self.actgrp, -1)
        self.menu = self.app.gui.uim.add_ui_from_string(MENU)
    
    def deactivate(self):
        self.app.gui.uim.remove_ui(self.menu)
        self.app.gui.uim.remove_action_group(self.actgrp)
        self.menu, self.actgrp = None, None
    
    def disp_stats(self, *data):
        """Displays stats dialog."""
        stats = self.get_stats()
        if stats is not None:
            dwin = StatsDialog(self.app.gui.win, stats)
            dwin.run()
            dwin.destroy()
        return
    
    def get_stats(self, *data):
        """Get current document stats."""
        tab = self.app.gui.get_current_tab()
        ret = None
        if hasattr(tab, 'ev'):
            if hasattr(tab.ev, 'buffer'):
                title = tab.get_title()
                iter = tab.ev.buffer.get_start_iter()
                nwords, test = -1, True
                while test:
                    test = iter.forward_visible_word_end()
                    nwords += 1
                nlines = tab.ev.buffer.get_line_count()
                nchars = tab.ev.buffer.get_char_count()
                ret = (title, nlines, nwords, nchars)
        return ret


#------------------------------------------------------------------------------

class StatsDialog(gtk.Dialog):
    """Dialog to display stats."""
    
    def __init__(self, parent, stats):
        # Dialog initialization
        flags = gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT
        buttons = (gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE)
        gtk.Dialog.__init__(self, None, parent, flags, buttons)
        self.set_default_size(300, 100)
        self.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
        self.set_has_separator(False)
        # Content
        bold = pango.AttrList()
        bold.insert(pango.AttrWeight(pango.WEIGHT_BOLD, 0, -1))
        f = gtk.Frame(stats[0])
        f.get_label_widget().set_attributes(bold)
        f.set_shadow_type(gtk.SHADOW_NONE)
        f.set_border_width(15)
        t = gtk.Table(3, 2)
        t.set_border_width(9)
        t.set_row_spacings(5)
        t.set_col_spacings(5)
        for i,n in enumerate([_("Lines:"),_("Words:"),_("Characters:")]):
            l = gtk.Label(n)
            l.set_alignment(0, 0.5)
            t.attach(l, 0, 1, i, i+1)
            v = gtk.Label(stats[i+1])
            v.set_alignment(1, 0.5)
            t.attach(v, 1, 2, i, i+1)
        f.add(t)
        self.vbox.pack_start(f, True, True)
        self.show_all()


#------------------------------------------------------------------------------



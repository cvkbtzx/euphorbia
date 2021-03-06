#-*- coding:utf-8 -*-

##  EUPHORBIA - GTK LaTeX Editor
##  Module: EuphorbiaEditor.ui.project
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


"""Project manager."""

import gtk
import pango
import ConfigParser

from ..utils import iofiles


#------------------------------------------------------------------------------

MENU = """
<menubar name="menu_main">
  <menu name="menu_project" action="action_project">
    <menuitem action="action_closeproj" />
    <separator />
    <menuitem action="action_openaddproj" />
    <menuitem action="action_addtabproj" />
    <menuitem action="action_rmtabproj" />
    <menuitem action="action_projmaster" />
    <separator />
    <menuitem action="action_archiveproj" />
    <menuitem action="action_projprops" />
  </menu>
</menubar>
"""

DEFAULT_GENERAL_OPTS = {
    'name'           : "",
    'lastDocument'   : "",
    'masterDocument' : "",
}

DEFAULT_ITEM_OPTS = {
    'archive'  : "true",
    'column'   : "0",
    'encoding' : "",
    'highlight': "",
    'line'     : "0",
    'open'     : "false",
    'order'    : "-1",
}


#------------------------------------------------------------------------------

def get_actions(cls):
    actions = [
        ('action_closeproj', gtk.STOCK_CLOSE, None, '', None, cls.act_close),
        ('action_openaddproj', gtk.STOCK_ADD, _("Add files"), '', None, cls.act_openadd),
        ('action_addtabproj', gtk.STOCK_ADD, _("Add current tab"), '', None, cls.act_addtab),
        ('action_rmtabproj', gtk.STOCK_REMOVE, _("Remove current tab"), '', None, cls.act_rmtab),
        ('action_projmaster', gtk.STOCK_HOME, _("Set as master document"), '', None, cls.act_setmaster),
        ('action_archiveproj', gtk.STOCK_HARDDISK, _("Archive"), '', None, cls.act_archive),
        ('action_projprops', gtk.STOCK_PROPERTIES, None, '', None, cls.act_properties),
    ]
    return actions


#------------------------------------------------------------------------------

class ProjectManager(object):
    """Manage project files."""
    
    def __init__(self, app, p_gfile, **args):
        self.app = app
        self.fileobj = iofiles.FalseFileObj(p_gfile)
        self.rootdir = iofiles.URImanager(p_gfile.gfile.get_parent().get_uri())
        self.master = None
        self.listfiles = {}
        if self.load(**args):
            if self.app.gui.project is not None:
                self.app.gui.project.act_close()
            self.app.gui.project = self
            self.app.prefm.set_pref('files_lastprj', self.fileobj._gfile.uri)
            # Menu actions
            self.actgrp = gtk.ActionGroup('euphorbia')
            self.actgrp.add_actions(get_actions(self))
            self.app.gui.uim.insert_action_group(self.actgrp, -1)
            self.menu = self.app.gui.uim.add_ui_from_string(MENU)
            # Side panel
            sidepanel = self.app.gui.get_widgets_by_id('sidepanel').pop()
            self.pb = ProjectBrowser(self)
            sidepanel.add_expander('project', _("Project content"), self.pb)
            sidepanel.reorder_child(sidepanel.expanders['project'], 0)
            self.app.prefm.autoconnect_gtk(sidepanel)
            self.pb.update()
            self.app.gui.emit('openprj')
    
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
    def act_close(self, *data):
        """Callback for 'Close' action."""
        self.app.gui.emit('closeprj')
        self.save()
        sidepanel = self.app.gui.get_widgets_by_id('sidepanel').pop()
        sidepanel.remove_expander('project')
        self.app.gui.uim.remove_ui(self.menu)
        self.app.gui.uim.remove_action_group(self.actgrp)
        self.menu, self.actgrp = None, None
        self.app.prefm.set_pref('files_lastprj', None)
        self.app.gui.project = None
        return
    
    def act_openadd(self, *data):
        """Callback for 'Add files' action."""
        uris = self.app.gui.act_open(do_open=False)
        for u in uris:
            f = iofiles.FileManager(u)
            f.update_infos()
            self.add_file(f)
        return
    
    def act_addtab(self, *data):
        """Callback for 'Add tab' action."""
        tab = self.app.gui.get_current_tab()
        if tab is not None:
            self.add_tab(tab)
        return
    
    def act_rmtab(self, *data):
        """Callback for 'Remove tab' action."""
        tab = self.app.gui.get_current_tab()
        if tab is not None:
            self.rm_tab(tab)
        return
    
    def act_setmaster(self, *data):
        """Callback for 'Set master' action."""
        tab = self.app.gui.get_current_tab()
        if tab is not None:
            f = tab.get_file_infos()[1]
            if f is not None:
                urim = iofiles.URImanager(f.uri)
                self.set_master(urim)
        return
    
    def act_archive(self, *data):
        """Callback for 'Archive' action."""
        print "Project: archive"
        return
    
    def act_properties(self, *data):
        """Callback for 'Archive' action."""
        print "Project: properties"
        return
    
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
    def belongs(self, urim):
        """Test if URImanager belongs to the project."""
        if urim is None:
            return False
        return any(urim.is_same_file_as(u) for u in self.listfiles)
    
    def set_opt(self, urim, opt, val):
        """Set urim option from config."""
        sec = "item:" + self.get_id(urim)
        special = {True:'true', False:'false', None:''}
        if val in special:
            val = special[val]
        self.cparser.set(sec, opt, val)
        return
    
    def get_opt(self, urim, opt):
        """Get urim option in config."""
        sec = "item:" + self.get_id(urim)
        if opt in ['archive','open']:
            val = self.cparser.getboolean(sec, opt)
        elif opt in ['order','line','column']:
            val = self.cparser.getint(sec, opt)
        else:
            val = self.cparser.get(sec, opt)
            val = None if val == "" else val
        return val
    
    def get_id(self, urim):
        """Get relative path id of given urim."""
        r = [v for u,v in self.listfiles.iteritems() if urim.is_same_file_as(u)]
        return r[0] if len(r) > 0 else None
    
    def add(self, urim, hlight=None, enc=None, arch=True):
        """Add an urim to the project."""
        test = not self.belongs(urim)
        if test:
            sec = urim.get_relative_path_from(self.rootdir)
            self.listfiles[urim] = sec
            self.cparser.add_section("item:"+sec)
            opts = {'highlight':hlight, 'encoding':enc, 'archive':arch}
            for op,v in DEFAULT_ITEM_OPTS.iteritems():
                val = opts[op] if op in opts else v
                self.set_opt(urim, op, val)
            self.pb.update()
        return test
    
    def add_file(self, f, hl=None):
        """Add a file to the project."""
        if f.uri is None:
            return False
        urim = iofiles.URImanager(f.uri)
        return self.add(urim, hlight=hl, enc=f.encoding)
    
    def add_tab(self, tab):
        """Add tab's file to the project's files."""
        i = tab.get_file_infos()
        if i[1] is not None:
            hl = tab.datafile['hlight'] if hasattr(tab, 'datafile') else None
            ret = self.add_file(i[1], hl)
        else:
            ret = False
        return ret
    
    def remove(self, urim):
        """Remove an urim from the project."""
        if urim.is_same_file_as(self.master):
            self.set_master(None)
        if self.belongs(urim):
            for u,rel in self.listfiles.copy().iteritems():
                if urim.is_same_file_as(u):
                    sec = "item:" + rel
                    self.cparser.remove_section(sec)
                    del self.listfiles[u]
            self.pb.update()
        return
    
    def rm_file(self, f):
        """Remove a file from the project."""
        urim = iofiles.URImanager(f.uri)
        self.remove(urim)
        return
    
    def rm_tab(self, tab):
        """Remove tab's file from the project's files."""
        i = tab.get_file_infos()
        if i[1] is not None:
            self.rm_file(i[1])
        return
    
    def set_master(self, urim):
        """Set the master document."""
        if self.belongs(urim) or urim is None:
            self.master = urim
            val = None if urim is None else self.get_id(urim)
            self.cparser.set('General', 'masterDocument', val)
            self.pb.update()
        else:
            log("project > this tab does not belong to the project", 'error')
        return
    
    def get_master(self):
        """Get the master document."""
        return self.master
    
    def get_status(self, urim, tabs_infos):
        """Get status of given urim."""
        status = {'encoding':None, 'highlight':None, 'open':False, 'order':"-1"}
        itab = None
        for ti in tabs_infos:
            if ti[3] is not None:
                if ti[3].uri is not None:
                    turim = iofiles.URImanager(ti[3].uri)
                    if urim.is_same_file_as(turim):
                        itab = ti
        if itab is not None:
            tab = itab[0]
            status['open'] = True
            status['order'] = "%i" % (itab[2])
            if hasattr(tab, 'datafile'):
                status['highlight'] = tab.datafile['hlight']
                status['encoding'] = tab.datafile['encoding']
            if hasattr(tab, 'get_pos'):
                pos = tab.get_pos()
                status['line'] = "%i" % (pos[0])
                status['column'] = "%i" % (pos[1])
        return status
    
    def set_archive(self, urim, val):
        """Set if urim should be archived."""
        self.set_opt(urim, 'archive', val)
        return
    
    def get_archive(self, urim,):
        """Get if urim should be archived."""
        return self.get_opt(urim, 'archive')
    
    def list_files(self):
        """List the files (URImanager) belonging to the project."""
        return self.listfiles.keys()
    
    def open_uri(self, urim):
        """Open the given file (URImanager) in a new tab."""
        e, h = self.get_opt(urim, 'encoding'), self.get_opt(urim, 'highlight')
        p = (self.get_opt(urim, 'line'), self.get_opt(urim, 'column'))
        args = {'enc':e, 'hlight':h.lower() if h is not None else h, 'pos':p}
        self.app.gui.do_open(urim.gfile.get_uri(), 'all', **args)
        return
    
    def load(self, **args):
        """Load the project from a file."""
        log("project > load")
        self.cparser = ConfigParser.RawConfigParser()
        self.cparser.optionxform = str
        if not args.get('new', False):
            self.fileobj.g_read()
            self.cparser.readfp(self.fileobj)
        if not self.cparser.has_section('General'):
            self.cparser.add_section('General')
        for op,val in DEFAULT_GENERAL_OPTS.iteritems():
            if not self.cparser.has_option('General', op):
                self.cparser.set('General', op, val)
        if not self.cparser.get('General', 'name'):
            pname = self.fileobj._gfile.get_name()
            if pname.endswith(".ephb") or pname.endswith(".kilepr"):
                pname = pname.rsplit(".", 1)[0]
            self.cparser.set('General', 'name', pname)
        openlist, lastopen = [], None
        for sec in self.cparser.sections():
            if not sec.startswith("item:"):
                continue
            for op,val in DEFAULT_ITEM_OPTS.iteritems():
                if not self.cparser.has_option(sec, op):
                    self.cparser.set(sec, op, val)
            rel = sec[5:]
            f = self.rootdir.gfile.resolve_relative_path(rel)
            urim = iofiles.URImanager(f.get_uri())
            if not self.belongs(urim):
                self.listfiles[urim] = rel
                if self.cparser.get('General', 'masterDocument') == rel:
                    self.master = urim
                if self.cparser.get('General', 'lastDocument') == rel:
                    lastopen = urim
            if self.cparser.getboolean(sec, 'open'):
                order = self.cparser.get(sec, 'order')
                openlist.append((urim, order))
        for u in sorted(openlist, key=lambda x: x[1]):
            self.open_uri(u[0])
        if lastopen is not None:
            self.open_uri(lastopen)
        return True
    
    def save(self):
        """Save the project into a file."""
        tabs_infos = self.app.gui.get_tabs_infos()
        for urim in self.listfiles:
            for opt,val in self.get_status(urim, tabs_infos).iteritems():
                self.set_opt(urim, opt, val)
        curr_tab = self.app.gui.get_current_tab()
        if curr_tab is not None:
            cf = curr_tab.get_file_infos()[1]
            if cf is not None:
                urim = iofiles.URImanager(cf.uri)
                self.cparser.set('General', 'lastDocument', self.get_id(urim))
        self.cparser.write(self.fileobj)
        if not self.cparser.has_option('General', 'kileversion'):
            log("project > save")
            self.fileobj.g_write()
        return


#------------------------------------------------------------------------------

class ProjectBrowser(gtk.ScrolledWindow):
    """TreeView which displays project files."""
    
    def __init__(self, manager):
        gtk.ScrolledWindow.__init__(self)
        self.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        self.set_shadow_type(gtk.SHADOW_NONE)
        self.set_data('id', "projectbrowser")
        self.manager = manager
        self.build_treeview()
        self.add(self.tv)
        self.show_all()
    
    def build_treeview(self):
        """Build the treeview."""
        # Model
        self.ts = gtk.ListStore(object, gtk.gdk.Pixbuf, str, pango.Weight)
        # View
        self.tv = gtk.TreeView()
        self.tv.set_model(self.ts)
        self.tv.set_headers_visible(False)
        self.tv.set_reorderable(False)
        self.tv.set_enable_search(True)
        self.tv.set_search_column(2)
        self.tv.set_enable_tree_lines(False)
        self.tv.get_selection().set_mode(gtk.SELECTION_SINGLE)
        self.tv.props.can_focus = False
        self.tv.connect('button-press-event', self.ev_right_click)
        self.tv.connect('row-activated', self.ev_row_activated)
        # Column
        c = gtk.TreeViewColumn("Files")
        crp = gtk.CellRendererPixbuf()
        c.pack_start(crp, False)
        c.add_attribute(crp, 'pixbuf', 1)
        crt = gtk.CellRendererText()
        crt.props.ellipsize = pango.ELLIPSIZE_END
        crt.props.scale = pango.SCALE_SMALL
        c.pack_start(crt, True)
        c.add_attribute(crt, 'text', 2)
        c.add_attribute(crt, 'weight', 3)
        c.set_expand(True)
        self.tv.append_column(c)
        return
    
    def update(self):
        """Update treeview content."""
        self.ts.clear()
        master = self.manager.get_master()
        for u in sorted(self.manager.listfiles.items(), key=lambda x: x[1]):
            urim, n = u
            if urim.is_same_file_as(master):
                w = pango.WEIGHT_BOLD
                stock = gtk.STOCK_HOME
            else:
                w = pango.WEIGHT_NORMAL
                stock = gtk.STOCK_FILE
            pix = self.render_icon(stock, gtk.ICON_SIZE_MENU)
            self.ts.append([urim, pix, n, w])
        return
    
    def get_context_menu(self, iter):
        """Get right-click contextual menu."""
        urim = self.ts.get_value(iter, 0)
        if urim is None:
            return None
        item_o = gtk.ImageMenuItem(gtk.STOCK_OPEN)
        item_o.connect('activate', self.ev_open, urim)
        item_m = gtk.ImageMenuItem(gtk.STOCK_HOME)
        item_m.set_label(_("Set as master document"))
        item_m.connect('activate', self.ev_setmaster, urim)
        item_r = gtk.ImageMenuItem(gtk.STOCK_REMOVE)
        item_r.set_label(_("Remove from project"))
        item_r.connect('activate', self.ev_remove, urim)
        item_a = gtk.CheckMenuItem(_("Include in archive"))
        item_a.set_active(self.manager.get_archive(urim))
        item_a.connect('activate', self.ev_archive, urim)
        item_s = gtk.SeparatorMenuItem
        menu = gtk.Menu()
        for i in [item_o, item_s(), item_m, item_r, item_s(), item_a]:
            menu.append(i)
        menu.show_all()
        return menu
    
    def ev_right_click(self, w, event):
        """Handle right-click on treeview."""
        if event.button == 3  and event.type == gtk.gdk.BUTTON_PRESS:
            pathinfo = self.tv.get_path_at_pos(int(event.x), int(event.y))
            if pathinfo is not None:
                iter = self.ts.get_iter(pathinfo[0])
                self.tv.get_selection().select_iter(iter)
                menu = self.get_context_menu(iter)
                if menu is not None:
                    menu.popup(None, None, None, event.button, event.time)
            else:
                self.tv.get_selection().unselect_all()
            return True
        return False
    
    def ev_open(self, menuitem, urim):
        """Callback for 'open' menu event."""
        self.manager.open_uri(urim)
        return
    
    def ev_setmaster(self, menuitem, urim):
        """Callback for 'set master' menu event."""
        self.manager.set_master(urim)
        return
    
    def ev_remove(self, menuitem, urim):
        """Callback for 'remove' menu event."""
        self.manager.remove(urim)
        return
    
    def ev_archive(self, menuitem, urim):
        """Callback for 'archive' menu event."""
        self.manager.set_archive(urim, menuitem.get_active())
        return
    
    def ev_row_activated(self, w, path, column):
        """Callback for double-click event."""
        iter = self.ts.get_iter(path)
        urim = self.ts.get_value(iter, 0)
        self.manager.open_uri(urim)
        return


#------------------------------------------------------------------------------



#-*- coding:utf-8 -*-

##  HTML viewer plugin for Euphorbia LaTeX editor
##  Copyright (C) 2011-2011   Bzoloid
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


"""Web viewer plugin."""

import gtk
import webkit
import euphorbia

MENU = """
<menubar name="menu_main">
  <menu name="menu_help" action="action_help">
    <placeholder name="placeholder_help">
      <separator />
      <menuitem action="action_html_help" />
    </placeholder>
  </menu>
</menubar>
"""


#------------------------------------------------------------------------------

class WebView(euphorbia.Plugin):
    """HTML viewer."""
    
    def __init__(self):
        euphorbia.Plugin.__init__(self)
        self.default_helpurl = "http://en.wikibooks.org/wiki/LaTeX"
        # Menu actions
        self.menu = None
        self.actgrp = gtk.ActionGroup('euphorbia')
        actions = [
            ('action_html_help', gtk.STOCK_DIALOG_INFO, _("ShowHtmlHelp"), None, None, self.help)
        ]
        self.actgrp.add_actions(actions)
    
    def activate(self):
        # File handlers
        exts = ["*.html","*.htm"]
        handler = ('webview', _("HTML files"), exts, WebkitTab, {})
        self.app.gui.file_handlers.append(handler)
        # Menu items
        self.app.gui.uim.insert_action_group(self.actgrp, -1)
        self.menu = self.app.gui.uim.add_ui_from_string(MENU)
        # Prefs
        if not self.app.prefm.has_pref('pluginwebview_helpurl'):
            self.app.prefm.add_pref('pluginwebview_helpurl', None, 'text', self.default_helpurl)
        return
    
    def deactivate(self):
        # File handlers
        i = [fh[0] for fh in self.app.gui.file_handlers].index('webview')
        del self.app.gui.file_handlers[i]
        # Menu items
        self.app.gui.uim.remove_ui(self.menu)
        self.app.gui.uim.remove_action_group(self.actgrp)
        self.menu, self.actgrp = None, None
        return
    
    def help(self, *data):
        """Show the HTML help."""
        url = self.app.prefm.get_pref('pluginwebview_helpurl')
        self.app.gui.do_open(url, 'webview', title=_("Handbook"), icon=gtk.STOCK_HELP)
        return


#------------------------------------------------------------------------------

class WebkitTab(euphorbia.TabWrapper):
    """Notebook tab containing a WebkitFrame."""
    
    def __init__(self, app, fileobj, **args):
        wf = WebkitFrame(app, fileobj.uri)
        euphorbia.TabWrapper.__init__(self, app, wf)
        self.wf = wf
        self.app.gui.autobuild_tooltips(self.wf.get_children()[0])
        self.type_id = "webview"
        self.iofile = fileobj
        t = fileobj.get_name()
        if 'icon' in args:
            self.set_icon(args['icon'])
        else:
            self.set_icon(*fileobj.get_icons())
        if 'title' in args:
            t = args['title']
        self.set_title(t)
    
    def get_file_infos(self):
        """Return infos (file_name, file_obj, is_modified) about the file."""
        return (self.iofile.get_name(), self.iofile, False)
    
    def cut(self):
        """Cut text into clipboard."""
        self.wf.wview.cut_clipboard()
        return
    
    def copy(self):
        """Copy text into clipboard."""
        self.wf.wview.copy_clipboard()
        return
    
    def paste(self):
        """Paste text from clipboard."""
        self.wf.wview.paste_clipboard()
        return
    
    def search(self, txt, case, dir, loop):
        """Search text in page."""
        dir = True if dir > 0 else False
        self.wf.wview.search_text(txt, case, dir, loop)
        return


#------------------------------------------------------------------------------

class WebkitFrame(gtk.VBox):
    """Display area, handled by webkit."""
    # http://webkitgtk.org/reference/index.html
    
    def __init__(self, app, uri):
        gtk.VBox.__init__(self)
        self.app = app
        # Webkit.WebView
        self.wview = webkit.WebView()
        s = self.wview.get_settings()
        ###s.set_property('enable-dns-prefetching', False)
        s.set_property('enable-html5-database', False)
        s.set_property('enable-html5-local-storage', False)
        s.set_property('enable-java-applet', False)
        s.set_property('enable-offline-web-application-cache', False)
        s.set_property('enable-plugins', False)
        s.set_property('enable-private-browsing', True)
        s.set_property('enable-scripts', True)
        s.set_property('javascript-can-open-windows-automatically', False)
        # Scroll
        scroll = gtk.ScrolledWindow()
        scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        scroll.add(self.wview)
        # Toolbar
        tb = gtk.Toolbar()
        self.build_toolbar(tb)
        self.pack_start(tb, False, True)
        self.pack_start(scroll, True, True)
        # Display
        self.wview.connect('load-started', self.ev_load_started)
        self.wview.connect('document-load-finished', self.ev_load_finished)
        self.wview.load_uri(uri)
        self.show_all()
    
    def build_toolbar(self, tb):
        """Add buttons to the toolbar."""
        accels = self.app.gui.uim.get_accel_group()
        tb.set_name('toolbar_webview')
        # Browse buttons
        t = gtk.ToolButton(gtk.STOCK_GO_BACK)
        t.set_expand(False)
        t.connect('clicked', self.ev_back)
        ak, am = gtk.accelerator_parse("<Alt>Left")
        t.add_accelerator('clicked', accels, ak, am, gtk.ACCEL_VISIBLE)
        tb.insert(t, -1)
        t = gtk.ToolButton(gtk.STOCK_GO_FORWARD)
        t.set_expand(False)
        t.connect('clicked', self.ev_forward)
        ak, am = gtk.accelerator_parse("<Alt>Right")
        t.add_accelerator('clicked', accels, ak, am, gtk.ACCEL_VISIBLE)
        tb.insert(t, -1)
        # Separator
        t = gtk.SeparatorToolItem()
        t.set_expand(False)
        tb.insert(t, -1)
        # Refresh / stop
        self.bstop = gtk.ToolButton(gtk.STOCK_STOP)
        self.bstop.set_expand(False)
        self.bstop.connect('clicked', self.ev_stop)
        tb.insert(self.bstop, -1)
        # URL entry
        t = gtk.ToolItem()
        t.set_expand(True)
        self.urlentry = gtk.Entry()
        self.urlentry.set_icon_from_stock(gtk.ENTRY_ICON_SECONDARY, gtk.STOCK_OK)
        self.urlentry.set_icon_activatable(gtk.ENTRY_ICON_SECONDARY, True)
        self.urlentry.connect('icon-release', self.ev_activate)
        self.urlentry.connect('activate', self.ev_activate)
        t.add(self.urlentry)
        tb.insert(t, -1)
        # Zoom
        t = gtk.ToolButton(gtk.STOCK_ZOOM_IN)
        t.set_expand(False)
        t.connect('clicked', self.ev_zoom_in)
        tb.insert(t, -1)
        t = gtk.ToolButton(gtk.STOCK_ZOOM_OUT)
        t.set_expand(False)
        t.connect('clicked', self.ev_zoom_out)
        tb.insert(t, -1)
        return
    
    def ev_back(self, *data):
        """Callback previous page."""
        self.wview.go_back()
        return
    
    def ev_forward(self, *data):
        """Callback next page."""
        self.wview.go_forward()
        return
    
    def ev_stop(self, *data):
        """Callback stop."""
        self.wview.stop_loading()
        return
    
    def ev_zoom_in(self, *data):
        """Callback zoom in."""
        self.wview.zoom_in()
        return
    
    def ev_zoom_out(self, *data):
        """Callback zoom out."""
        self.wview.zoom_out()
        return
    
    def ev_activate(self, *data):
        """Callback zoom out."""
        self.wview.load_uri(self.urlentry.get_text())
        return
    
    def ev_load_started(self, *data):
        """Handle 'onload-event event."""
        self.bstop.set_sensitive(True)
        return
    
    def ev_load_finished(self, *data):
        """Handle 'document-load-finished' event."""
        self.bstop.set_sensitive(False)
        if hasattr(self.wview, 'get_uri'):
            uri = self.wview.get_uri()
        else:
            uri = self.wview.get_property('uri')
        self.urlentry.set_text("" if uri is None else uri)
        return


#------------------------------------------------------------------------------



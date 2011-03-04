#-*- coding:utf-8 -*-

##  Image viewer plugin for Euphorbia LaTeX editor
##  Copyright (C) 2010-2011   Bzoloid
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


"""Image viewer plugin."""

import gtk
import gobject
import euphorbia


#------------------------------------------------------------------------------

class ImageView(euphorbia.Plugin):
    """Image viewer."""
    
    def __init__(self):
        euphorbia.Plugin.__init__(self)
    
    def activate(self):
        formats = gtk.gdk.pixbuf_get_formats()
        exts = set("*."+e for f in formats for e in f['extensions'])
        handler = ('images', _("Image files"), list(exts), ImageTab, {})
        self.app.gui.file_handlers.append(handler)
        return
    
    def deactivate(self):
        i = [fh[0] for fh in self.app.gui.file_handlers].index('images')
        del self.app.gui.file_handlers[i]
        return


#------------------------------------------------------------------------------

class ImageTab(euphorbia.TabWrapper):
    """Notebook tab containing an image."""
    
    def __init__(self, app, fileobj, **args):
        li = LargeImage(fileobj.gfile)
        euphorbia.TabWrapper.__init__(self, app, li)
        self.type_id = "imgview"
        self.gfile = fileobj
        self.set_title(fileobj.get_name())
        self.set_icon(*fileobj.get_icons())
    
    def get_file_infos(self):
        """Return infos (file_name, file_obj, is_modified) about the file."""
        return (self.gfile.get_name(), self.gfile, False)


#------------------------------------------------------------------------------

class LargeImage(gtk.ScrolledWindow):
    
    def __init__(self, gfile):
        gtk.ScrolledWindow.__init__(self)
        self.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.set_shadow_type(gtk.SHADOW_NONE)
        self.img = gtk.Image()
        self.add_with_viewport(self.img)
        self.get_child().set_shadow_type(gtk.SHADOW_NONE)
        self.count = 65536
        if not self.test_format(gfile):
            log("imgview > format not supported", 'error')
            self.close()
        else:
            self.pix = gtk.gdk.PixbufLoader()
            self.pix.connect('area-updated', self.ev_update)
            self.pix.connect('closed', self.ev_close)
            gobject.timeout_add(100, lambda: gfile.read_async(self.ev_read))
            self.show_all()
    
    def test_format(self, f):
        """Return False if file is not in supported formats."""
        path = f.get_path()
        if path is None:
            return True
        return False if gtk.gdk.pixbuf_get_file_info(path) is None else True
    
    def ev_read(self, gfile, result):
        """Start reading file asynchronously."""
        try:
            stream = gfile.read_finish(result)
        except StandardError:
            log("plugin_imgview > can't read image", 'error')
            self.pix.close()
        else:
            stream.read_async(self.count, self.read)
        return
    
    def read(self, stream, result):
        """Read small amounts of the file and put data in pixbuf loader."""
        data = stream.read_finish(result)
        if data:
            try:
                self.pix.write(data)
            except StandardError:
                log("plugin_imgview > can't decode image", 'error')
                self.pix.close()
            stream.read_async(self.count, self.read)
        else:
            self.pix.close()
        return
    
    def ev_update(self, *data):
        """Update display if possible."""
        self.img.set_from_pixbuf(self.pix.get_pixbuf())
        return
    
    def ev_close(self, *data):
        """Close event callback (end of loading)."""
        self.ev_update()
        log("plugin_imgview > image loaded")
        del self.pix
        return


#------------------------------------------------------------------------------



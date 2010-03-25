# -*- coding:utf-8 -*-

"""Files management."""

import gtk
import gio

ICONTHEME = gtk.icon_theme_get_default()


#------------------------------------------------------------------------------

class FileManager:
    """File manager based on GIO."""
    
    def __init__(self, name, encoding=None):
        self.gfile = gio.File(name)
        self.mime = None
        self.encoding = encoding
        self.uri = self.gfile.get_uri()
        self.path = self.gfile.get_path()
        self.infos = {
            'name':None, 'icon':None, 'type':None, 'size':None,
            'content-type':None,'fast-content-type':None,
            'can-read':None, 'can-write':None,
            'can-delete':None, 'can-trash':None,
        }
    
    def update_infos(self):
        """Update file infos."""
        try:
            qi = self.gfile.query_info("standard::*,access::*")
        except:
            for a in self.infos:
                self.infos[a] = None
            self.mime = None
            return False
        attrs = qi.list_attributes("standard") + qi.list_attributes("access")
        for a in self.infos:
            fn = "get_" + a.replace('-', '_')
            if hasattr(qi, fn):
                func = getattr(qi, fn)
                self.infos[a] = func()
            else:
                arg = tuple(i for i in attrs if i.split("::")[-1] == a)
                val = qi.get_attribute_as_string(*arg)
                if val == 'TRUE':
                    self.infos[a] = True
                elif val == 'FALSE':
                    self.infos[a] = False
                else:
                    self.infos[a] = val
        if self.infos['content-type'] is not None:
            self.mime = self.infos['content-type']
        elif self.infos['fast-content-type'] is not None:
            self.mime = self.infos['fast-content-type']
        else:
            self.mime = None
        return True
    
    def read(self):
        """Read data from file."""
        if self.infos['can-read'] is False:
            return None
        try:
            data, length, etag = self.gfile.load_contents()
            if self.encoding not in [None, 'utf-8', 'UTF-8']:
                data = data.decode(self.encoding).encode('utf-8')
        except:
            data = None
        return data
    
    def write(self, data, backup=False):
        """Write data in file."""
        if self.infos['can-write'] is False:
            return False
        try:
            if self.encoding not in [None, 'utf-8', 'UTF-8']:
                data = data.decode('utf-8').encode(self.encoding)
            self.gfile.replace_contents(data, None, backup)
        except:
            return False
        return True
    
    def launch(self):
        """Launch file with default application."""
        app = self.gfile.get_app()
        if app.supports_uris():
            ret = app.launch([self.gfile.get_uri()], None)
        elif app.supports_files():
            ret = app.launch([self.gfile.get_path()], None)
        else:
            ret = False
        return ret
    
    def trash(self):
        """Put file in the trash."""
        return self.gfile.trash() if self.infos['can-trash'] else False
    
    def delete(self):
        """Delete file."""
        return self.gfile.delete() if self.infos['can-delete'] else False
    
    def get_app(self):
        """Get file's default application."""
        type = "" if self.mime is None else self.mime
        return gio.app_info_get_default_for_type(self.mime, False)
    
    def get_icon(self, size):
        """Get icon pixbuf."""
        # pixbuf_from_stock = gtk.Widget.render_icon(stock, size)
        pixbuf = None
        try:
            flag = gtk.ICON_LOOKUP_USE_BUILTIN
            names = self.infos['icon'].get_names()
            iconinfo = ICONTHEME.choose_icon(names, size, flag)
            if iconinfo is not None:
                pixbuf = iconinfo.load_icon()
        except:
            pass
        return pixbuf


#------------------------------------------------------------------------------



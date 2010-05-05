# -*- coding:utf-8 -*-

##  EUPHORBIA - GTK LaTeX Editor
##  Module: EuphorbiaEditor.utils.iofiles
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


"""Files management."""

import gio
import os.path


#------------------------------------------------------------------------------

class FileManager(object):
    """File manager based on GIO."""
    
    def __init__(self, name, encoding=None):
        self.gfile = gio.File(name)
        self.original_name = name
        self.mime = None
        self.encoding = encoding
        self.uri = self.gfile.get_uri()
        self.path = self.gfile.get_path()
        self.infos = {
            'name':None, 'display-name':None, 'type':None, 'size':None,
            'content-type':None,'fast-content-type':None, 'icon':None,
            'can-read':None, 'can-write':None,
            'can-delete':None, 'can-trash':None,
        }
    
    def update_infos(self):
        """Update file infos."""
        try:
            qi = self.gfile.query_info("standard::*,access::*")
        except StandardError:
            log("iofiles > can't query file infos", 'warning')
            for a in self.infos:
                self.infos[a] = None
            self.infos['name'] = os.path.basename(self.original_name)
            self.mime = None
            return
        attrs = qi.list_attributes("standard") + qi.list_attributes("access")
        for a in self.infos:
            fn = "get_" + a.replace('-', '_')
            if hasattr(qi, fn):
                func = getattr(qi, fn)
                self.infos[a] = func()
            else:
                arg = tuple(i for i in attrs if i.split("::")[-1] == a)
                if not arg:
                    self.infos[a] = None
                else:
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
        return
    
    def get_name(self):
        """Get name as UTF-8 string (if possible)."""
        i = self.infos
        if self.infos['display-name']:
            ret = self.infos['display-name']
        elif self.infos['name']:
            ret = self.infos['name']
        else:
            ret = self.gfile.get_basename()
        return ret
    
    def fullname(self):
        """Get file full name."""
        if self.path:
            ret = self.path
        elif self.uri:
            ret = self.uri
        else:
            ret = self.get_name()
        return ret
    
    def read(self):
        """Read text data from file."""
        if self.infos['can-read'] is False:
            return None
        code = None if self.encoding is None else self.encoding.lower()
        try:
            data, length, etag = self.gfile.load_contents()
            if code not in [None, 'utf-8', 'utf8']:
                data = data.decode(code).encode('utf-8')
            else:
                data.decode('utf-8')   # raise error if not utf-8
        except StandardError as e:
            data = None
            if type(e) == gio.Error:
                if e.code == gio.ERROR_NOT_FOUND:
                    data = ""
            else:
                log("iofiles > can't read from the file", 'error')
        return data
    
    def write(self, data, backup=False):
        """Write text data in file."""
        if self.infos['can-write'] is False:
            return False
        code = None if self.encoding is None else self.encoding.lower()
        try:
            if code not in [None, 'utf-8', 'utf8']:
                data = data.decode('utf-8').encode(code)
            self.gfile.replace_contents(data, None, backup)
        except StandardError:
            log("iofiles > can't write into the file", 'error')
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
    
    def get_icons(self):
        """Get icon pixbuf."""
        if hasattr(self.infos['icon'], 'get_names'):
            names = self.infos['icon'].get_names()
        else:
            names = []
        return names


#------------------------------------------------------------------------------



# -*- coding:utf-8 -*-

from ui.palette import Palette
from ui.document import TabWrapper, Document

app = None


#------------------------------------------------------------------------------

class Plugin(object):
    def __init__(self):
        self.app = app
    def activate(self):
        pass
    def deactivate(self):
        pass


#------------------------------------------------------------------------------



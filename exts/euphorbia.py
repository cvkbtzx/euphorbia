# -*- coding:utf-8 -*-

"""Euphorbia plugin wrapper."""

from ui.palette import Palette
from ui.document import TabWrapper

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



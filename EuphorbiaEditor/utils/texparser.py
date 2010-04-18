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


"""Parse LaTeX code."""

import string


#------------------------------------------------------------------------------

class LatexParser:
    """Class to retrieve informations in a LaTeX document."""
    
    def __init__(self, txt):
        self.text, self.eol = txt+'\n', chr(10)
        self.clean()
        self.keywords = {
            'struct':["part","chapter","section","subsection","subsubsection"],
            'graphic':["includegraphics"],
            'table':["tabular"],
            'biblio':["cite"],
        }
    
    def clean(self):
        """Clean the code by removing comments."""
        self.text = self.text.replace(chr(13), chr(10))
        i = self.text.find('%', 0)
        while i > -1:
            if self.text[i-1] != '\\':
                j = self.text.find(self.eol, i)
                self.text = self.text[:i] + self.text[j:]
            i = self.text.find('%', i)
        return
    
    def parse(self, keygrp):
        """Parse the code with given keywords group."""
        keys = self.keywords[keygrp]
        return


#------------------------------------------------------------------------------

if __name__ == '__main__':
    txt = ""
    with open("test-parse.tex", 'r') as f:
        txt = f.read()
    lp = LatexParser(txt)
    print lp.text


#------------------------------------------------------------------------------



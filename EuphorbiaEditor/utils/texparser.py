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

LATEX_KEYWORDS = {
    'struct':  ["part", "chapter", "section", "subsection", "subsubsection"],
    'graphic': ["includegraphics"],
    'table':   ["tabular"],
    'package': ["usepackage"],
}


#------------------------------------------------------------------------------

class LatexParser(object):
    """Class to retrieve informations in a LaTeX document."""
    
    def __init__(self, txt):
        self.text = txt + '\n'
        self._clean()
        self.keywords = LATEX_KEYWORDS
    
    def _clean(self):
        """Clean the code by removing comments."""
        self.text = self.text.replace(chr(13)+chr(10), chr(10))   # Windows eol
        self.text = self.text.replace(chr(13), chr(10))   # MacOSX eol
        i = self.text.find('%', 0)
        while i > -1:
            if self.text[i-1] != '\\':
                j = self.text.find(chr(10), i)
                self.text = self.text[:i] + self.text[j:]
            i = self.text.find('%', i+1)
        return
    
    def parse(self, keygrp):
        """Parse the code with given keywords group."""
        keys = self.tokenize(keygrp)
        if len(keys) == 0:
            return []
        tree, paths = [], []
        for k in xrange(len(keys)):
            v = keys[k][1:]+([],)
            for h in reversed(range(k)):
                if keys[h][0] < keys[k][0]:
                    paths[h][2].append(v)
                    paths.append(v)
                    break
            else:
                tree.append(v)
                paths.append(v)
        return tree
    
    def tokenize(self, keygrp):
        """Tokenize the code with given keywords group."""
        keys = []
        for i,k in enumerate(self.keywords[keygrp]):
            for t,l in self._iter_keyword(k):
                keys.append((i,t,l))
        return sorted(keys, key=lambda x: x[2])
    
    def _iter_keyword(self, kw):
        """Iter on given keyword."""
        ckw = string.letters + string.digits
        kw, lkw = '\\' + kw, len(kw)+1
        i = self.text.find(kw, 0)
        while i > -1:
            if i + lkw < len(self.text):
                if self.text[i-1] != '\\' and self.text[i+lkw] not in ckw:
                    j1 = self.text.find('{', i) + 1
                    j2 = self.text.find('}', j1)
                    t = self.text[j1:j2][:128]
                    for c in string.whitespace:
                        t = t.replace(c, ' ')
                    line = self.text.count(chr(10), 0, i) + 1
                    yield (t.strip(), line)
            i = self.text.find(kw, i+lkw)
        return


#------------------------------------------------------------------------------

if __name__ == '__main__':
    txt = ""
    with open("test-parse.tex", 'r') as f:
        txt = f.read()
    lp = LatexParser(txt)
    print lp.parse('struct')


#------------------------------------------------------------------------------



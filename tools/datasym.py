#!/usr/bin/python2
#-*- coding:utf-8 -*-

import sys
import os
import os.path
import string
import ConfigParser


#------------------------------------------------------------------------------

in_files = sys.argv[1:]

for ifn in in_files:
    cp = ConfigParser.RawConfigParser()
    fi = open(ifn, 'r')
    for l in fi:
        sym = l.strip('\n')
        sec = sym if len(sym) == 1 else sym[1:]
        cp.add_section(sec)
        cp.set(sec, "Insert", sym)
        cp.set(sec, "Compile", "$"+sym+"$")
        cp.set(sec, "Math", "true")
    with open(ifn+".data", 'w') as fo:
        cp.write(fo)


#------------------------------------------------------------------------------



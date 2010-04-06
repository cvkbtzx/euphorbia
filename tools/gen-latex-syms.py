#!/usr/bin/python2
# -*- coding:utf-8 -*-

import sys
import os
import os.path
import subprocess
import ConfigParser

FBEG = """
\documentclass[12pt,pdflatex]{minimal}
\usepackage[T1]{fontenc}
\usepackage{ae,aecompl}
\usepackage[utf8]{inputenc}
\usepackage{amsmath}
\usepackage{amsfonts}
\usepackage{amssymb}
\\begin{document}
"""

FEND = """
\end{document}
"""

DIM = "22"
DPI = "%i" % (22/0.176)


#------------------------------------------------------------------------------

rootdir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "symbols")
os.chdir(rootdir)

datafiles = [d for d in os.listdir(".") if d.endswith(".data")]

for df in datafiles:
    dir = os.path.splitext(df)[0]
    os.mkdir(dir)
    cp = ConfigParser.RawConfigParser()
    cp.read([df])
    for s in cp.sections():
        print "Symbol:", s
        fn = lambda e: os.path.join(".", dir, s+"."+e)
        with open(fn("tex"), 'w') as lf:
            cmd = cp.get(s, "Compile")
            lf.write(FBEG + cmd + FEND)
        devnull = open(os.devnull, 'w')
        p = subprocess.Popen(["pdflatex", "-interaction", "nonstopmode", "-output-directory", dir, fn("tex")], stdout=devnull, stderr=devnull)
        p.wait()
        p = subprocess.Popen(["perl", "/usr/bin/pdfcrop", "--margins", "1", fn("pdf"), fn("2.pdf")], stdout=devnull, stderr=devnull)
        p.wait()
        p = subprocess.Popen(["convert", "-density", DPI, "-resize", DIM+"x"+DIM+">", "-gravity", "Center", "-extent", DIM+"x"+DIM, fn("2.pdf"), "-define", "png:color-type=4", "-quality", "90", fn("2.png")])
        p.wait()
        p = subprocess.Popen(["convert", "-negate", fn("2.png"), "-alpha", "copy", "-negate", "-define", "png:color-type=6", "-format", "PNG32", "-quality", "90", fn("png")])
        p.wait()
    for f in os.listdir(dir):
        if len(f.split(".")) != 2 or not f.endswith(".png"):
            os.remove(os.path.join(".", dir, f))


#------------------------------------------------------------------------------



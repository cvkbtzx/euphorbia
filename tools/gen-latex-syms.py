#!/usr/bin/python2
#-*- coding:utf-8 -*-

__author__ = 'Bzoloid <bzoloid@gmail.com>'
__date__ = '2010-08-28'

import os
import os.path
import subprocess
import ConfigParser

FBEG = r"""
\documentclass[12pt,pdflatex]{minimal}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{ae,aecompl}
\usepackage{amsmath}
\usepackage{amsfonts}
\usepackage{amssymb}
\begin{document}
"""

FEND = r"""
\end{document}
"""

DIM = "24"
DPI = "150"


#------------------------------------------------------------------------------

rootdir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "symbols")
os.chdir(rootdir)

datafiles = [d for d in os.listdir(".") if d.endswith(".data")]

for df in datafiles:
    dir = os.path.splitext(df)[0]
    os.mkdir(dir)
    cp = ConfigParser.RawConfigParser()
    cp.read([df])
    print "Id:", cp.get("DEFAULT", "Id")
    for s in cp.sections():
        print "Symbol:", s
        fn = lambda e: os.path.join(dir, s+"."+e)
        with open(fn("tex"), 'w') as lf:
            cmd = cp.get(s, 'Compile')
            lf.write(FBEG + cmd + FEND)
        devnull = open(os.devnull, 'w')
        subprocess.Popen(["pdflatex", "-interaction", "nonstopmode", "-output-directory", dir, fn("tex")], stdout=devnull, stderr=devnull).wait()
        subprocess.Popen(["perl", "/usr/bin/pdfcrop", "--margins", "0", fn("pdf"), fn("2.pdf")], stdout=devnull, stderr=devnull).wait()
        subprocess.Popen(["sh", "../autodensity.sh", fn("2.pdf"), DPI, DIM, fn("2.png")]).wait()
        subprocess.Popen(["convert", "-size", DIM+"x"+DIM, "xc:white", fn("2.png"), "-negate", "-compose", "Copy_Opacity", "-composite", "-define", "png:color-type=6",  "-depth", "8", "-quality", "90", fn("png")]).wait()
        devnull.close()
    for f in os.listdir(dir):
        if len(f.split(".")) != 2 or not f.endswith(".png"):
            os.remove(os.path.join(".", dir, f))


#------------------------------------------------------------------------------



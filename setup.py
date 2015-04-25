#!/usr/bin/python
#-*- coding:utf-8 -*-

import os
import os.path
from distutils.core import setup


#------------------------------------------------------------------------------

pkgname = "EuphorbiaEditor"
pkgs = [pkgname] + ['.'.join([pkgname,d]) for d in os.listdir(pkgname) if os.path.isdir(os.path.join(pkgname,d))]
datafiles = [(w[0],map(lambda f: os.path.join(w[0],f), w[2])) for w in os.walk("share") if len(w[2])>0]
binfiles = ["euphorbia"]

ver, lic = None, None
with open(os.path.join(pkgname,"__init__.py"), 'r') as f:
    for line in f:
        l = line.split(" = ")
        if l[0] == "__version__":
            ver = l[1].strip("""'"\n\r""")
        if l[0] == "__license__":
            lic = l[1].strip("""'"\n\r""")


#------------------------------------------------------------------------------

setup(
    name = "euphorbia",
    version = ver,
    description = "Euphorbia - GTK LaTeX editor",
    long_description = "Euphorbia provides a powerful and extensible environment to edit and manage LaTeX documents.",
    author = "Bzoloid",
    author_email = "bzoloid@gmail.com",
    url = "https://github.com/cvkbtzx/euphorbia",
    license = lic,
    packages = pkgs,
    scripts = binfiles,
    data_files = datafiles
)


#------------------------------------------------------------------------------



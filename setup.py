#!/usr/bin/python

import os
import os.path
from distutils.core import setup


pkgname = "EuphorbiaEditor"
pkgs = [pkgname] + ['.'.join([pkgname,d]) for d in os.listdir(pkgname) if os.path.isdir(os.path.join(pkgname,d))]
datafiles = [(w[0],map(lambda f: os.path.join(w[0],f), w[2])) for w in os.walk("share") if len(w[2])>0]
binfiles = ["euphorbia"]

ver, lic = None, None
f = open(os.path.join(pkgname,"__init__.py"))
try:
    for line in f:
        l = line.split(" = ")
        if l[0] == "__version__":
            ver = l[1].strip("""'"\n\r""")
        if l[0] == "__licence__":
            lic = l[1].strip("""'"\n\r""")
finally:
    f.close()


#------------------------------------------------------------------------------

setup(
    name = "euphorbia",
    version = ver,
    description = "Euphorbia LaTeX editor",
    author = "Bzoloid",
    author_email = "bzoloid@gmail.com",
    url = "http://code.google.com/p/euphorbia/",
    license = lic,
    packages = pkgs,
    scripts = binfiles,
    data_files = datafiles
)

#------------------------------------------------------------------------------



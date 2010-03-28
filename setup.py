#!/usr/bin/python

import os
import os.path
from distutils.core import setup


name = "EuphorbiaEditor"
pkgs = [name] + ['.'.join([name,d]) for d in os.listdir(name) if os.path.isdir(os.path.join(name,d))]
datafiles = [(w[0],map(lambda f: os.path.join(w[0],f), w[2])) for w in os.walk("share") if len(w[2])>0]


setup(
    name = "euphorbia",
    version = '0.0.5',
    description = "Euphorbia LaTeX editor",
    author = "Bzoloid",
    author_email = "bzoloid@gmail.com",
    url = "http://code.google.com/p/euphorbia/",
    license = 'GNU-GPL v2',
    packages = pkgs,
    scripts = ["euphorbia"],
    data_files = datafiles
)


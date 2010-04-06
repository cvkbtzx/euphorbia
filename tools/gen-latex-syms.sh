#!/bin/bash
# -*- coding:utf-8 -*-

dn=$(dirname "$0")
cd "${dn}"

workdir="./symbols"

gvfs-trash "${workdir}"
mkdir "./symbols"
cp -v ../share/euphorbia/symbols/*.data "${workdir}/"

python2 gen-latex-syms.py

for f in ${workdir}/* ; do
    test -d "${f}" && cp -Rfv "${f}" "../share/euphorbia/symbols/"
done

gvfs-trash "${workdir}"

exit 0


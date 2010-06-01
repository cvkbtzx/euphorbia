#!/bin/bash
# -*- coding:utf-8 -*-

dn=$(dirname "$0")
cd "${dn}/../share/"
rm -Rv ./locale/

for f in ../po/*.po ; do
    poname=$(basename "${f}")
    lang=${poname%.*}
    dname="locale/${lang}/LC_MESSAGES"
    fname="${dname}/euphorbia.mo"
    echo "${fname}"
    mkdir -p "${dname}"
    msgfmt "${f}" -o "${fname}"
done

exit 0


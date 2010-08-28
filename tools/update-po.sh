#!/bin/bash
#-*- coding:utf-8 -*-

dn=$(dirname "$0")
cd "${dn}/../"

for f in ./po/*.po ; do
    msgmerge -N -U --previous "${f}" ./po/messages.pot
done

exit 0


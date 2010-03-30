#!/bin/bash
# -*- coding:utf-8 -*-

dn=$(dirname "$0")
cd "${dn}/../"

xgettext -o ./po/euphorbia.pot -j --from-code=UTF-8 --no-location  *{/,/*/}*.py ./share/euphorbia/*.glade

for f in ./po/*.po ; do
    msgmerge -N -U --previous "${f}" ./po/messages.pot
done

exit 0


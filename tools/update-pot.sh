#!/bin/bash
#-*- coding:utf-8 -*-

dn=$(dirname "$0")
cd "${dn}/../"

xgettext -o ./po/messages.pot -j --from-code=UTF-8 --no-location  *{/,/*/}*.py ./share/euphorbia/plugins/*.py ./share/euphorbia/*.glade

exit 0


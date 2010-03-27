#!/bin/bash
# -*- coding:utf-8 -*-

cd $(dirname "$0")

for dim in 16 22 24 32 48 64 72 96 128 256 ; do
    inkscape --without-gui \
             --file=euphorbia.svg \
             --export-png="../icons/hicolor/${dim}x${dim}/apps/euphorbia.png" \
             --export-width=${dim} \
             --export-height=${dim}
done

cp -v euphorbia.svg "../icons/hicolor/scalable/apps/euphorbia.svg"

exit 0


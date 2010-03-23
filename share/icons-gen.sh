#!/bin/bash
# -*- coding:utf-8 -*-

cd $(dirname "$0")

for dim in 16 22 24 32 48 64 72 96 128 256 ; do
    inkscape --without-gui \
             --file=euphorbia.svg \
             --export-png="euphorbia-${dim}.png" \
             --export-width=${dim} \
             --export-height=${dim}
done

exit 0


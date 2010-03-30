#!/bin/bash
# -*- coding:utf-8 -*-

dn=$(dirname "$0")
cd "${dn}"

DPI=600
DIM=22

pdfcrop --margins 1 aaa.pdf bbb.pdf
convert -density ${DPI} -resize ${DIM}x${DIM} -gravity Center -extent ${DIM}x${DIM} bbb.pdf -format PNG24 -quality 90 ccc.png
convert -negate ccc.png -alpha copy -negate -define png:color-type=6 -format PNG32 -quality 90 ddd.png

exit 0


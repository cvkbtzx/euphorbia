#!/bin/bash
# -*- coding:utf-8 -*-

dn=$(dirname "$0")
cd "${dn}/../share/euphorbia/"

for dim in 16 22 24 32 36 48 64 72 96 128 192 256 "scalable" ; do
    if [[ ${dim} == "scalable" ]] ; then
        dimdir="scalable"
        ext="svg"
    else
        dimdir="${dim}x${dim}"
        ext="png"
    fi
    icondir="../icons/hicolor/${dimdir}/apps"
    iconname="${icondir}/euphorbia.${ext}"
    test -d "${icondir}" || mkdir -p "${icondir}"
    test -f "$iconname{}" && rm -v "${iconname}"
    if [[ ${dim} == "scalable" ]] ; then
        cp -v euphorbia.svg "${iconname}"
    else
        inkscape --without-gui \
                 --file=euphorbia.svg \
                 --export-png="${iconname}" \
                 --export-width=${dim} \
                 --export-height=${dim}
    fi
done

exit 0


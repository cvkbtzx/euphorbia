#!/bin/bash
#-*- coding:utf-8 -*-

# ARGS: input_pdf_file, max_density, output_size, output_png_file

height=$(identify -density ${2} -format "%h" "${1}")
width=$(identify -density ${2} -format "%w" "${1}")

if (( ${width} > ${height} )) ; then isize=${width} ; else isize=${height} ; fi
if (( ${isize} > ${3} )) ; then density=$(( (${2}*${3})/${isize} )) ; else density=${2} ; fi

convert -density ${density} -gravity center -extent ${3}x${3} "${1}" -type GrayScale -depth 8 -quality 90 "${4}"

exit 0


#!/bin/bash

set -ex

source ${XC2CT_GENHEADER}


python ../generate.py >top.v

mkdir -p xst/projnav.tmp/
xst -intstyle ise -ifn "../top.xst" -ofn "top.syr"
ngdbuild -intstyle ise -dd _ngo -i -p xc2c32a-CP56-4 top.ngc top.ngd
cpldfit -intstyle ise -p xc2c32a-4-CP56 -ofmt vhdl -optimize density -htmlrpt -loc on -slew fast -init low -nogclkopt -nogsropt -nogtsopt -nomlopt -wysiwyg -blkfanin 40 -inputs 40 -pterms 56 -unused keeper -terminate keeper -iostd LVCMOS18 top.ngd
hprep6 -s IEEE1149 -i top

# LD_LIBRARY_PATH= awk '/Fitting Status: Successful/{flag=1;next}/CTC - Control Term Clock/{flag=0}flag' top.rpt

python ../theorem.py top.jed top.vm6  top.segbits


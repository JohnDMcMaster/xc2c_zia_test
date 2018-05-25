all:
	python gen.py >top.v
	xst -intstyle ise -ifn "top.xst" -ofn "top.syr"
	ngdbuild -intstyle ise -dd _ngo -i -p xc2c64-VQ100-5 top.ngc top.ngd
	cpldfit -intstyle ise -p xc2c64-5-VQ100 -ofmt vhdl -optimize density -htmlrpt -loc on -slew fast -init low -inputs 40 -pterms 56 -unused keeper -terminate keeper -iostd LVCMOS18 top.ngd
	hprep6 -s IEEE1149 -i top


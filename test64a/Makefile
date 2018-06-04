all:
	mkdir -p xst/projnav.tmp/
	python gen.py >top.v
	xst -intstyle ise -ifn "top.xst" -ofn "top.syr"
	ngdbuild -intstyle ise -dd _ngo -i -p xc2c64a-VQ100-5 top.ngc top.ngd
	cpldfit -intstyle ise -p xc2c64a-5-VQ100 -ofmt vhdl -optimize density -htmlrpt -loc on -slew fast -init low -nogclkopt -nogsropt -nogtsopt -nomlopt -wysiwyg -blkfanin 40 -inputs 40 -pterms 56 -unused keeper -terminate keeper -iostd LVCMOS18 top.ngd
	# generates prog file
	hprep6 -s IEEE1149 -i top

	# "Generate Timing"
	# taengine -intstyle ise -f top.vm6 -w --format html1 -l top_html/tim/timing_report.htm

	# "Generate Post-Fit Simulation Model"
	# netgen -intstyle ise -sdf_anno true -sdf_path "netgen/fit" -insert_glbl true -w -dir netgen/fit -ofmt verilog -sim top.nga top_timesim.v

    # "Generate Text Power Report"
    # xpwr -intstyle ise top.cxt -o top.pwr

    # "Generate IBIS Model"
    # ibiswriter -intstyle ise top.pnx top.ibs



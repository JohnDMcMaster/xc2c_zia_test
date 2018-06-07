LD_LIBRARY_PATH= awk '/Fitting Status: Successful/{flag=1;next}/CTC - Control Term Clock/{flag=0}flag' specimen_001/top.rpt

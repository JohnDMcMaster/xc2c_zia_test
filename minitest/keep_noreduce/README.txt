Demonstrates effects of various optimization constraints
Basically, applying something to other than the register results in it getting shoved to a new macrocell

See Xilinx CPLD notes here: https://www.xilinx.com/support/documentation/sw_manuals/help/iseguide/mergedProjects/destech/html/ca_cpld_attributes.htm#NOREDUCE

WARNING: over constraining a design may result in various internal errors

Other: seems that ISE allocates related macrocells sequentially
If you LOC a macrocell then have a related macrocell it must be replaced adjacent
That is, if you allocate the first 8 macrocells manually,
but macrocell 2 generates an additional macrocell (ie by using KEEP on the PLA term) you may get an error like this:
ERROR:Cpld:8 - Cannot assign macrocell fb1_out_post_5 to Pin A2 (FB1_7). 
   Location is already occupied by fb1_out_post_7.

Note on FB1:
    (* KEEP="true"*) output wire        out_pre_0,
    (* DONT_TOUCH="true"*) output wire  out_pre_1,
    (* NOREDUCE="true"*) output wire    out_pre_2,
Result:
*********************************** FB1  ***********************************
This function block is part of I/O Bank number:               2
Number of function block inputs used/remaining:               11/29
Number of function block control terms used/remaining:        0/4
Number of PLA product terms used/remaining:                   8/48
Signal                        Total Loc     Pin  Pin     Pin   CTC CTR CTS CTE
Name                          Pt            No.  Type    Use   
fb1_out_post_0                1     FB1_1   F1   I/O     O                 
fb1_out_post_1                1     FB1_2   E3   I/O     O                 
fb1_out_post_2                1     FB1_3   E1   I/O     O                 
fb1_out_post_3                1     FB1_4   D1   GTS/I/O O                 
fb1_out_post_4                2     FB1_5   C1   GTS/I/O O                 
fb1_out_post_5                1     FB1_6   A3   GTS/I/O O                 
fb1_out_post_6                1     FB1_7   A2   GTS/I/O O                 
fb1_out_post_7                1     FB1_8   B1   GSR/I/O O                 
(unused)                      0     FB1_9   A1   I/O           
(unused)                      0     FB1_10  C4   I/O           
(unused)                      0     FB1_11  C5   I/O           
(unused)                      0     FB1_12  C8   I/O           
(unused)                      0     FB1_13  A10  I/O           
fb1/out_pre_0                 1     FB1_14  B10  I/O     (b)               
fb1/out_pre_2                 2     FB1_15  C10  I/O     (b)               
fb1/out_pre_1                 2     FB1_16  E8   I/O     (b)    

Note on FB2:
    (* KEEP="true"*)        wire pterm_0 = ...;
    (* DONT_TOUCH="true"*)  wire pterm_1 = ...;
    (* NOREDUCE="true"*)    wire pterm_2 = ...;
Result:
*********************************** FB2  ***********************************
This function block is part of I/O Bank number:               1
Number of function block inputs used/remaining:               11/29
Number of function block control terms used/remaining:        0/4
Number of PLA product terms used/remaining:                   7/49
Signal                        Total Loc     Pin  Pin     Pin   CTC CTR CTS CTE
Name                          Pt            No.  Type    Use   
fb2_out_post_0                3     FB2_1   G1   I/O     O                 
fb2_out_post_1                2     FB2_2   F3   I/O     O                 
fb2_out_post_2                2     FB2_3   H1   I/O     O                 
fb2_out_post_3                1     FB2_4   G3   I/O     O                 
(unused)                      0     FB2_5   J1   GCK/I/O GCK   
fb2_out_post_4                2     FB2_6   K1   GCK/I/O O                 
fb2_out_post_5                1     FB2_7   K2   GCK/I/O O                 
fb2_out_post_6                1     FB2_8   K3   I/O     O                 
fb2_out_post_7                1     FB2_9   H3   I/O     O                 
(unused)                      0     FB2_10  K5   I/O           
(unused)                      0     FB2_11  H5   I/O           
(unused)                      0     FB2_12  H8   I/O           
(unused)                      0     FB2_13  K8   I/O           
fb2/pterm_2                   1     FB2_14  H10  I/O     (b)               
fb2/pterm_1                   1     FB2_15  G10  I/O     (b)               
fb2/pterm_0                   1     FB2_16  F10  I/O     (b)               


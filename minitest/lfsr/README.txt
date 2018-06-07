Demonstrates an LFSR
Requires no inputs but consumes P-term + OR-term + macrocells

Sample output summary

Function Mcells   FB Inps  Pterms   IO       CTC      CTR      CTS      CTE     
Block    Used/Tot Used/Tot Used/Tot Used/Tot Used/Tot Used/Tot Used/Tot Used/Tot
FB1       8/16      8/40    16/56     8/16    0/1      0/1      0/1      0/1
FB2       0/16      0/40     0/56     0/16    0/1      0/1      0/1      0/1
         -----    -------  -------   -----    ---      ---      ---      ---
Total     8/32      8/80    16/112    8/32    0/2      0/2      0/2      0/2 

*********************************** FB1  ***********************************
Signal                        Total Loc     Pin  Pin     Pin   CTC CTR CTS CTE
Name                          Pt            No.  Type    Use   
fb1_out_post_0                2     FB1_1   F1   I/O     O                 
fb1_out_post_1                2     FB1_2   E3   I/O     O                 
fb1_out_post_2                2     FB1_3   E1   I/O     O                 
fb1_out_post_3                2     FB1_4   D1   GTS/I/O O                 
fb1_out_post_4                2     FB1_5   C1   GTS/I/O O                 
fb1_out_post_5                2     FB1_6   A3   GTS/I/O O                 
fb1_out_post_6                2     FB1_7   A2   GTS/I/O O                 
fb1_out_post_7                2     FB1_8   B1   GSR/I/O O                 
(unused)                      0     FB1_9   A1   I/O           
(unused)                      0     FB1_10  C4   I/O           
(unused)                      0     FB1_11  C5   I/O           
(unused)                      0     FB1_12  C8   I/O           
(unused)                      0     FB1_13  A10  I/O           
(unused)                      0     FB1_14  B10  I/O           
(unused)                      0     FB1_15  C10  I/O           
(unused)                      0     FB1_16  E8   I/O           

Signals Used by Logic in Function Block
  1: fb1_out_post_0     4: fb1_out_post_3     7: fb1_out_post_6 
  2: fb1_out_post_1     5: fb1_out_post_4     8: fb1_out_post_7 
  3: fb1_out_post_2     6: fb1_out_post_5   

Signal                     1         2         3         4 FB      
Name             0----+----0----+----0----+----0----+----0 Inputs  
fb1_out_post_0    ..X..X.................................. 2       
fb1_out_post_1    ...X..X................................. 2       
fb1_out_post_2    ....X..X................................ 2       
fb1_out_post_3    X....X.................................. 2       
fb1_out_post_4    .X....X................................. 2       
fb1_out_post_5    ..X....X................................ 2       
fb1_out_post_6    X..X.................................... 2       
fb1_out_post_7    .X..X................................... 2       


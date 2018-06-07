Basic idea
PoC decoding XC2C32A ZIA bitstream using statistical methods like project x-ray
Much of the following bitstream specifics are based on azonenberg's "not datasheet"
The main contribution here is automating them using ISE


********************************************************************************
Background
********************************************************************************
The XC2C32A is a product term CPLD consistenting of:
-I/O
-Functional blocks (FB): poroduct terms + FF's
-ZIA: interconnect

Each FB consistents of 16 macrocells
Each macrocell has two outputs: before the FF and after

azonenberg notes the ZIA bus can take from any of the following:
-FB1_IBUF[16]
-FB2_FF[16]
-FB1_FF[16]
-FB2_IBUF[16]
-Dedicated input pin
That is, the dedicated input pin is treated specially
Generally I/O goes directly into FBs rather than through ZIA


********************************************************************************
How?
********************************************************************************
There is some limited ability to place signals in a given FB based on the output used
However, for the most part, the software tends to place things whever it wants

Fortunately it does seem to report where the signals were placed.
This can be fetched from either the .rpt file or the .vm6 file:
FB_INSTANCE | FOOBAR1_ | top_COPY_0_COPY_0 | 0 | 0 | 0
    FBPIN | 1 | out_0_MC | 1 | NULL | 0 | out_0 | 1 | F1 | 49152
    FBPIN | 2 | out_10_MC | 1 | NULL | 0 | out_10 | 1 | E3 | 49152
    FBPIN | 3 | out_11_MC | 1 | NULL | 0 | out_11 | 1 | E1 | 49152
    FBPIN | 4 | out_12_MC | 1 | NULL | 0 | out_12 | 1 | D1 | 53248


This file also has:
    FB_IMUX_INDEX | FOOBAR1_ | 46 | 48 | 35 | 47 | 44 | 40 | 33 | 45 | 43 | 37 | 36 | -1 | -1 | 42 ...
which appears to document which ZIA bus entry FB inputs connect to

Flow spits out a clearly labeled JED file with one ZIA block per FB
It appears these are linearly mapped to entries in the .rpt file such as the following:
Sample entry:
    Note Block 0 *
    Note Block 0 ZIA *
    L000000 01101111*
    L000008 01101111*
    L000016 01110111*
    ...
    L000160 11111111*
    L000168 01110111*
    L000176 11111111*
    ...
    L000296 11111111*
    L000304 11111111*
    L000312 11111111*
Where 11111111 rows are clearly unused
There are 40 rows, matching the 40 inputs to a FB

With this information, we construct designs with random connections between the various FBs,
noting how the connections were made

Originally I was going to use project x-ray stuff more heavily, but there is so much info here its simply not needed
Instead I'm just keeping compatible format maybe





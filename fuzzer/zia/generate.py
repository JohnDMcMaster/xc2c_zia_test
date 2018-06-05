import random
import os

random.seed(0)

def randnot():
    return ''
    return random.choice(['', '!'])

# External inputs
FB_I = 40
# All PLA inputs (includes I/O / FF)
FB_IA = 56
# Outputs
FB_O = 16
N_PINS = 33

def module_header(name, pins):
    print 'module %s(' % name
    for pi, (pdir, name) in enumerate(pins):
        if pi != len(pins) - 1:
            eol = ','
        else:
            eol = ');'
        print '        %s wire %s%s' % (pdir, name, eol)

def module_connect(module_name, instance_name, pins):
    print '    %s %s(' % (module_name, instance_name)
    for pi, (pin_name, net_name) in enumerate(pins):
        if pi != len(pins) - 1:
            eol = ','
        else:
            eol = ');'
        print '            .%s(%s)%s' % (pin_name, net_name, eol)

def gen_fb_module(fbn, fb_i=FB_I, fb_o=FB_O, ff=False, feedback=False):
    module_name = 'my_FB%d' % fbn
    pins = (
        [('input', 'in_%d' % i) for i in xrange(fb_i)] +
        [('output', 'out_%d' % i) for i in xrange(fb_o)]
        )
    if ff:
        pins += [('input', 'clk')]
    module_header(module_name, pins)

    print
    print

    if ff:
        for i in xrange(fb_o):
            print
            # XXX: think can combine these two lines 
            print '    (* LOC="FB%d", keep="true", DONT_TOUCH="true" *) reg ff_%d = 1\'b%d;' % (fbn, i, random.randint(0, 1))
            print '    assign out_%d = ff_%d;' % (i, i)

        print
        print
        print '    always @(posedge clk) begin'
        for outi in xrange(fb_o):
            terms = [randnot() + 'in_%d' % i for i in xrange(fb_i)]
            if feedback:
                terms += [randnot() + 'out_%d' % i for i in xrange(fb_o)]
            print '        ff_%d <= %s;' % (outi, ' | '.join(terms))
        print '    end'
    else:
        for i in xrange(fb_o):
            print
            # XXX: think can combine these two lines 
            print '    (* LOC="FB%d", keep="true", DONT_TOUCH="true" *) wire loc_out_%d;' % (fbn, i)
            print '    assign out_%d = loc_out_%d;' % (i, i)

        print
        print

        for fboi in xrange(fb_o):
            # assign myout1 = myin1 & myin2 & !myin3 & !myin4;
            terms = [randnot() + 'in_%d' % i for i in xrange(fb_i)]
            print '    assign loc_out_%d = %s;' % (fboi, ' | '.join(terms))
    print 'endmodule'

def gen_fb_shift_module(fbn):
    fb_i = FB_I
    fb_o = FB_O

    module_name = 'my_FB%d' % fbn
    pins = (
        [('input', 'clk')] +
        [('input', 'in_%d' % i) for i in xrange(fb_i)] +
        [('output', 'out_%d' % i) for i in xrange(fb_o)]
        )
    module_header(module_name, pins)

    print
    print

    for i in xrange(fb_o):
        print
        # XXX: think can combine these two lines 
        print '    (* LOC="FB%d", keep="true", DONT_TOUCH="true" *) reg ff_%d = 1\'b%d;' % (fbn, i, random.randint(0, 1))
        print '    assign out_%d = ff_%d;' % (i, i)

    print
    print
    print '    always @(posedge clk) begin'
    for outi in xrange(fb_o):
        terms = [randnot() + 'in_%d' % i for i in xrange(fb_i)]
        # maybe just do previous?
        #terms += [randnot() + 'ff_%d' % i for i in xrange(fb_o)]
        terms += ['ff_%d' % ((outi - 1) % fb_o,)]
        print '        ff_%d <= %s;' % (outi, ' | '.join(terms))
    print '    end'

    print 'endmodule'

def fb_inout(fbn):
    '''Connect given FB to matching inputs and outputs'''
    ipins = [('in_%d' % i, 'in_%d' % i) for i in xrange(FB_I)]
    opins = [('out_%d' % i, 'out_%d' % i) for i in xrange(FB_O)]
    module_connect('my_FB%s' % fbn, 'fb%d' % fbn,
        ipins + opins)

def run_fb2():
    '''Simple test fully instantiating FB2, connecting directly to I/O'''
    fbn = 2
    ff = True
    print '`timescale 1ns / 1ps'
    print
    # top
    module_name = 'top'
    fb_o = FB_O
    fb_i = N_PINS - fb_o

    fb_o = 2
    fb_i = 8

    pins = []
    if ff:
        pins += [('input', 'clk')]
    pins += [('input', 'in_%d' % i) for i in xrange(fb_i)]
    pins += [('output', 'out_%d' % i) for i in xrange(fb_o)]
    module_header(module_name, pins)

    print

    if ff:
        print '    wire clk_buf;'
        print '    BUFG bufg(.I(clk), .O(clk_buf));'
        print

    pins = []
    if ff:
        pins += [('clk', 'clk_buf')]
    pins += [('in_%d' % i, 'in_%d' % i) for i in xrange(fb_i)]
    pins += [('out_%d' % i, 'out_%d' % i) for i in xrange(fb_o)]
    module_connect('my_FB%s' % fbn, 'fb%d' % fbn, pins)
    print 'endmodule'

    print
    gen_fb_module(fbn, fb_i=fb_i, fb_o=fb_o, ff=ff)

def run_inflated():
    ''' to use a lot of logic, only using a few pins
    Should be easy to shift through the FB I think
    '''
    fbn = 2
    ff = True
    print '`timescale 1ns / 1ps'
    print
    # top
    module_name = 'top'
    fb_o = FB_O
    fb_i = N_PINS - fb_o

    fb_o = 2
    fb_i = 8

    pins = []
    if ff:
        pins += [('input', 'clk')]
    pins += [('input', 'in_%d' % i) for i in xrange(fb_i)]
    pins += [('output', 'out_%d' % i) for i in xrange(fb_o)]
    module_header(module_name, pins)

    print

    if ff:
        print '    wire clk_buf;'
        print '    BUFG bufg(.I(clk), .O(clk_buf));'
        print

    pins = []
    if ff:
        pins += [('clk', 'clk_buf')]
    pins += [('in_%d' % i, 'in_%d' % i) for i in xrange(fb_i)]
    pins += [('out_%d' % i, 'out_%d' % i) for i in xrange(fb_o)]
    module_connect('my_FB%s' % fbn, 'fb%d' % fbn, pins)
    print 'endmodule'

    print
    gen_fb_shift_module(fbn)

def run_inflated2():
    ''' to use a lot of logic, only using a few pins
    Should be easy to shift through the FB I think
    '''
    fbn = 2
    ff = True
    print '`timescale 1ns / 1ps'
    print
    # top
    module_name = 'top'
    fb_o = FB_O
    fb_i = N_PINS - fb_o

    fb_o = 2
    fb_i = 8

    pins = []
    if ff:
        pins += [('input', 'clk')]
    pins += [('input', 'in_%d' % i) for i in xrange(fb_i)]
    pins += [('output', 'out_%d' % i) for i in xrange(fb_o)]
    module_header(module_name, pins)

    print

    if ff:
        print '    wire clk_buf;'
        print '    BUFG bufg(.I(clk), .O(clk_buf));'
        print

    pins = []
    if ff:
        pins += [('clk', 'clk_buf')]
    pins += [('in_%d' % i, 'in_%d' % i) for i in xrange(fb_i)]
    pins += [('out_%d' % i, 'out_%d' % i) for i in xrange(fb_o)]
    module_connect('my_FB%s' % fbn, 'fb%d' % fbn, pins)
    print 'endmodule'

    print
    gen_fb_shift_module(1)
    print
    gen_fb_shift_module(2)

def run_clkout():
    '''
    Proof of concept using all outputs but no inputs
    This is important as it fixes all the paths in place for a given FB pair
    For some reason only outputs that connect to a pin can be LOC'd it seems

    fb_o = 4
    Function Mcells   FB Inps  Pterms   IO       CTC      CTR      CTS      CTE     
    Block    Used/Tot Used/Tot Used/Tot Used/Tot Used/Tot Used/Tot Used/Tot Used/Tot
    FB1      16/16*    16/40    16/56     4/16    0/1      0/1      0/1      0/1
    FB2      16/16*    16/40    16/56     4/16    0/1      0/1      0/1      0/1
             -----    -------  -------   -----    ---      ---      ---      ---
    Total    32/32     32/80    32/112    8/32    0/2      0/2      0/2      0/2

    fb_o = 15
    Function Mcells   FB Inps  Pterms   IO       CTC      CTR      CTS      CTE     
    Block    Used/Tot Used/Tot Used/Tot Used/Tot Used/Tot Used/Tot Used/Tot Used/Tot
    FB1      16/16*    16/40    16/56    15/16    0/1      0/1      0/1      0/1
    FB2      16/16*    16/40    16/56    15/16    0/1      0/1      0/1      0/1
             -----    -------  -------   -----    ---      ---      ---      ---
    Total    32/32     32/80    32/112   30/32    0/2      0/2      0/2      0/2 


    fb_o = 16
    ERROR:Cpld:848 - Insufficient number of output pins.  This design needs at least
       32 but only 31 left after allocating other resources.
    weird
    One of the pins is I only
    Since CLK goes to dedicated CLK pin, this leaves only 31 pins for output
    '''

    FBS = 2
    print '`timescale 1ns / 1ps'
    print
    # top
    module_name = 'top'

    fb_o = 15
    fb_i0 = 40

    pins = []
    pins += [('input', 'clk')]
    pins += [('output', 'out_%d' % i) for i in xrange(FBS * fb_o)]
    module_header(module_name, pins)

    print

    print '    wire clk_buf;'
    print '    BUFG bufg(.I(clk), .O(clk_buf));'
    print

    for fbi in xrange(FBS):
        fbn = fbi + 1
        print

        pins = [('clk', 'clk_buf')]
        pins += [('in_%d' % i, "1'b0") for i in xrange(fb_i0)]
        pins += [('out_%d' % i, 'out_%d' % (i + fbi * fb_o)) for i in xrange(fb_o)]
        module_connect('my_FB%s' % fbn, 'fb%d' % fbn,
            pins)
    print 'endmodule'

    print
    gen_fb_shift_module(1)
    print
    gen_fb_shift_module(2)

def run_fb_both():
    '''Instantiates several FB with shared inputs, connecting outputs directly to I/O'''

    FBS = 2
    # Use all inputs
    if 1:
        fb_i = 40
        fb_o = min((64 - fb_i) / FBS, FB_O)
    # Use all outputs
    # uses all the pins...
    if 0:
        fb_o = 16
        fb_i = 40 - fb_o * FBS
    assert fb_i > 0, fb_i
    assert fb_o > 0, fb_o
    assert fb_i <= FB_I, fb_i
    assert fb_o <= FB_O, fb_o
    MOD_I = fb_i
    MOD_O = FBS * fb_o

    print '`timescale 1ns / 1ps'
    print
    # top
    module_name = 'top'
    pins = ([('input', 'in_%d' % i) for i in xrange(MOD_I)] + 
            [('output', 'out_%d' % i) for i in xrange(MOD_O)])
    if len(pins) > N_PINS:
        raise Exception("Insufficient device pins. Require %d <= %d" % (len(pins), N_PINS))
    module_header(module_name, pins)

    for fbi in xrange(FBS):
        fbn = fbi + 1
        print

        ipins = [('in_%d' % i, 'in_%d' % i) for i in xrange(FB_I)]
        opins = [('out_%d' % i, 'out_%d' % (i + fbi * fb_o)) for i in xrange(fb_o)]
        module_connect('my_FB%s' % fbn, 'fb%d' % fbn,
            ipins + opins)

    print 'endmodule'

    for fbi in xrange(FBS):
        fbn = fbi + 1
        print
        gen_fb_module(fbn, fb_i=fb_i, fb_o=fb_o)

def run_fb_ff():
    '''Instantiates FB with all outputs fed back'''

    FBS = 1

    if 0:
        # Use all inputs
        fb_i = 40
        fb_o = min((64 - fb_i) / FBS, FB_O)
    if 1:
        fb_i = 39
        fb_o = 4

    assert fb_i > 0, fb_i
    assert fb_o > 0, fb_o
    assert fb_i <= FB_I, fb_i
    assert fb_o <= FB_O, fb_o
    MOD_I = fb_i
    MOD_O = FBS * fb_o

    print '//fb_i %d' % fb_i
    print '//fb_o %d' % fb_o
    print '`timescale 1ns / 1ps'
    print
    # top
    module_name = 'top'
    pins = (
            [('input', 'clk')] +
            [('input', 'in_%d' % i) for i in xrange(MOD_I)] + 
            [('output', 'out_%d' % i) for i in xrange(MOD_O)]
            )
    if len(pins) > N_PINS:
        raise Exception("Insufficient device pins. Require %d <= %d" % (len(pins), N_PINS))
    module_header(module_name, pins)


    print '    wire clk_buf;'
    print '    BUFG bufg(.I(clk), .O(clk_buf));'

    fbi = 1
    fbn = 2
    print

    pins = (
        [('in_%d' % i, 'in_%d' % i) for i in xrange(fb_i)] +
        [('out_%d' % i, 'out_%d' % i) for i in xrange(fb_o)] +
        [('clk', 'clk_buf')]
        )
    module_connect('my_FB%s' % fbn, 'fb%d' % fbn,
        pins)

    print 'endmodule'

    fbi = 1
    fbn = 2
    print
    gen_fb_module(fbn, fb_i=fb_i, fb_o=fb_o, ff=True)

def run_zia():
    '''
    Instantiates FBs with some connections

    Instantiate two FFs
    Connect each of the first 8 or so inputs to matching input pins
    For each remaining FB input randomly connect it to one of
        output from other FB
        an input pin
    '''

    FBS = 2

    # Use all inputs
    # for some reason going to 40 changes things
    fb_i = 39
    # 12 for FBS=2
    fb_o = min((64 - fb_i) / FBS, FB_O)
    fb_o = 4

    assert fb_i > 0, fb_i
    assert fb_o > 0, fb_o
    assert fb_i <= FB_I, fb_i
    assert fb_o <= FB_O, fb_o
    MOD_I = 40
    MOD_O = FBS * fb_o

    print '//fb_i %d' % fb_i
    print '//fb_o %d' % fb_o
    print '`timescale 1ns / 1ps'
    print
    # top
    module_name = 'top'
    pins = (
            [('input', 'clk')] +
            [('input', 'in_%d' % i) for i in xrange(MOD_I)] + 
            [('output', 'out_%d' % i) for i in xrange(MOD_O)]
            )
    if len(pins) > N_PINS:
        raise Exception("Insufficient device pins. Require %d <= %d" % (len(pins), N_PINS))
    module_header(module_name, pins)


    for fbi in xrange(FBS):
        fbn = fbi + 1
        print

        pins = (
            [('clk', 'clk')] +
            [('out_%d' % i, 'out_%d' % (i + fbi * fb_o)) for i in xrange(fb_o)]
            )

        for i in xrange(fb_i):
            # Connect first 8 pins to inputs to make sure they are used
            if i != 0:
               net = 'in_%d' % i
            else:
                which = random.choice(['input', 'fb'])
                which = 'fb'
                if which == 'input':
                    net = 'in_%d' % random.randint(8, MOD_I - 1)
                else:
                    # hacky...
                    fb_target = FBS - fbi - 1
                    omin = fb_target * fb_o
                    omax = (1 + fb_target) * fb_o - 1
                    assert omin < MOD_O, (omin, 'FBS', FBS, fbi, 'fb_target', fb_target, fb_o)
                    net = 'out_%d' % random.randint(omin, omax)
            pins.append(('in_%d' % i, net))

        module_connect('my_FB%s' % fbn, 'fb%d' % fbn,
            pins)

    print 'endmodule'

    for fbi in xrange(FBS):
        fbn = fbi + 1
        print
        gen_fb_module(fbn, fb_i=fb_i, fb_o=fb_o, ff=True)

def run_fb2_in1_sweep():
    '''
    Try all 16 possible FB1.out_* => FB.in_1
    See how this changes FB2 ZIA

    Saturate connections best we can  as is

    without any connections:
    Function Mcells   FB Inps  Pterms   IO       CTC      CTR      CTS      CTE     
    Block    Used/Tot Used/Tot Used/Tot Used/Tot Used/Tot Used/Tot Used/Tot Used/Tot
    FB1      16/16*    16/40    16/56    16/16*   0/1      0/1      0/1      0/1
    FB2      16/16*    16/40    16/56    15/16    0/1      0/1      0/1      0/1
             -----    -------  -------   -----    ---      ---      ---      ---
    Total    32/32     32/80    32/112   31/32    0/2      0/2      0/2      0/2 

    adding a connection:
    Function Mcells   FB Inps  Pterms   IO       CTC      CTR      CTS      CTE     
    Block    Used/Tot Used/Tot Used/Tot Used/Tot Used/Tot Used/Tot Used/Tot Used/Tot
    FB1      16/16*    16/40    16/56    16/16*   0/1      0/1      0/1      0/1
    FB2      16/16*    17/40    16/56    15/16    0/1      0/1      0/1      0/1
             -----    -------  -------   -----    ---      ---      ---      ---
    Total    32/32     33/80    32/112   31/32    0/2      0/2      0/2      0/2 


    Result: seems to optimize inputs down to one side of the array
    Outputs I think have some effect
    Next text: try adding additional inputs
    '''

    FBS = 2
    print '`timescale 1ns / 1ps'
    print
    # top
    module_name = 'top'

    conn_src = (1, int(os.getenv('ZIA_SRC', '-1')))
    conn_dst = (2, int(os.getenv('ZIA_DST', '-1')))

    fb_os = {1: 16, 2: 15}
    fb_i0 = 40

    pins = []
    pins += [('input', 'clk')]
    pins += [('output', 'out_%d' % i) for i in xrange(sum(fb_os.values()))]
    module_header(module_name, pins)

    print

    print '    wire clk_buf;'
    print '    BUFG bufg(.I(clk), .O(clk_buf));'
    print

    def fb_in_val(fbn, i):
        if (fbn, i) == conn_dst:
            assert conn_src[0] == 1
            return 'out_%d' % conn_src[1]
        else:
            return "1'b0"

    for fbi in xrange(FBS):
        fbn = fbi + 1
        print

        pins = [('clk', 'clk_buf')]

        pins += [('in_%d' % i, fb_in_val(fbn, i)) for i in xrange(fb_i0)]
        pins += [('out_%d' % i, 'out_%d' % (i + fbi * fb_os[1])) for i in xrange(fb_os[fbn])]
        module_connect('my_FB%s' % fbn, 'fb%d' % fbn,
            pins)
    print 'endmodule'

    print
    gen_fb_shift_module(1)
    print
    gen_fb_shift_module(2)

def run_fb2_ins_sweep():
    '''
    '''

    FBS = 2
    print '`timescale 1ns / 1ps'
    print
    # top
    module_name = 'top'

    conn_src = (1, int(os.getenv('ZIA_SRC', '-1')))
    conn_dst = (2, int(os.getenv('ZIA_DST', '-1')))

    fb_os = {1: 16, 2: 15}
    fb_i0 = 40

    pins = []
    pins += [('input', 'clk')]
    pins += [('output', 'out_%d' % i) for i in xrange(sum(fb_os.values()))]
    module_header(module_name, pins)

    print

    print '    wire clk_buf;'
    print '    BUFG bufg(.I(clk), .O(clk_buf));'
    print

    def fb_in_val(fbn, i):
        #if (fbn, i) == conn_dst:
        if fbn == conn_dst[0] and i <= conn_dst[1]:
            assert conn_src[0] == 1
            return 'out_%d' % conn_src[1]
        else:
            return "1'b0"

    for fbi in xrange(FBS):
        fbn = fbi + 1
        print

        pins = [('clk', 'clk_buf')]

        pins += [('in_%d' % i, fb_in_val(fbn, i)) for i in xrange(fb_i0)]
        pins += [('out_%d' % i, 'out_%d' % (i + fbi * fb_os[1])) for i in xrange(fb_os[fbn])]
        module_connect('my_FB%s' % fbn, 'fb%d' % fbn,
            pins)
    print 'endmodule'

    print
    gen_fb_shift_module(1)
    print
    gen_fb_shift_module(2)

#run_fb2()
#run_fb_both()
#run_fb_ff()
#run_zia()
#run_inflated()
#run_inflated2()

# run_fb2_in1_sweep()
run_fb2_ins_sweep()

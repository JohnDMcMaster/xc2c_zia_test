'''
`timescale 1ns / 1ps
module top(
    input wire myin1,
    input wire myin2,
    input wire myin3,
    output wire myout1,
    output wire myout2,
    output wire myout3
    );
    assign myout1 = myin1 & myin2;
    wire tmp = (!myin1) & myin2 & (!myin3);
    assign myout2 = tmp;

    reg ff;
    always @(posedge myin1) begin
        ff <= tmp;
    end
    assign myout3 = (!myin1) & myin2 & (!myin3) & ff;
endmodule
'''

import random

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
N_PINS = 64

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
                terms += [randnot() + 'loc_out_%d' % i for i in xrange(fb_o)]
            print '        ff_%d <= %s;' % (outi, ' & '.join(terms))
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
                print '    assign loc_out_%d = %s;' % (fboi, ' & '.join(terms))
    print 'endmodule'

def fb_inout(fbn):
    '''Connect given FB to matching inputs and outputs'''
    ipins = [('in_%d' % i, 'in_%d' % i) for i in xrange(FB_I)]
    opins = [('out_%d' % i, 'out_%d' % i) for i in xrange(FB_O)]
    module_connect('my_FB%s' % fbn, 'fb%d' % fbn,
        ipins + opins)

def run_fb2():
    '''Simple test fully instantiating FB2, connecting directly to I/O'''
    print '`timescale 1ns / 1ps'
    print
    # top
    module_name = 'top'
    ipins = [('input', 'in_%d' % i) for i in xrange(FB_I)]
    opins = [('output', 'out_%d' % i) for i in xrange(FB_O)]
    module_header(module_name, ipins + opins)

    print

    fb_inout(2)
    print 'endmodule'

    print
    gen_fb_module(2)

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
    '''
    this was caused by not explicitly using a clock buffer
    # 20, 4
    # FB2       4/16     20/40     4/56     4/16    0/1      0/1      0/1      0/1
    # 20, 8
    # FB2       8/16     20/40     8/56     8/16    0/1      0/1      0/1      0/1
    # FB2       9/16     20/40     9/56     9/16    0/1      0/1      0/1      0/1
    # when it goes to 10 outputs for some reason another output is generated
    # FB2      10/16     21/40    11/56    10/16    1/1*     0/1      0/1      0/1
    # FB2      11/16     21/40    12/56    11/16    1/1*     0/1      0/1      0/1
    # 20, 12
    # FB2      12/16     21/40    13/56    12/16    1/1*     0/1      0/1      0/1
    # 30, 12
    # FB2      12/16     31/40    13/56    12/16    1/1*     0/1      0/1      0/1
    # weird
    # CTC - Control Term Clock activates
    # lets try turning off optimizations


    after clk
    39, 4
    Block    Used/Tot Used/Tot Used/Tot Used/Tot Used/Tot Used/Tot Used/Tot Used/Tot
    FB1       0/16      0/40     0/56     0/16    0/1      0/1      0/1      0/1
    FB2       4/16     39/40     4/56     4/16    0/1      0/1      0/1      0/1

    40, 4
    Block    Used/Tot Used/Tot Used/Tot Used/Tot Used/Tot Used/Tot Used/Tot Used/Tot
    FB1       4/16     40/40*    4/56     0/16    0/1      0/1      0/1      0/1
    FB2       4/16      4/40     4/56     4/16    0/1      0/1      0/1      0/1
    '''
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

#run_fb2()
#run_fb_both()
#run_fb_ff()
run_zia()


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

def gen_fb_module(fbn, fb_i=FB_I, fb_o=FB_O):
    module_name = 'my_FB%d' % fbn
    ipins = [('input', 'in_%d' % i) for i in xrange(fb_i)]
    opins = [('output', 'out_%d' % i) for i in xrange(fb_o)]
    module_header(module_name, ipins + opins)

    print

    for i in xrange(FB_O):
        # XXX: think can combine these two lines 
	    print '    (* LOC="FB%d", keep="true", DONT_TOUCH="true" *) wire loc_out_%d;' % (fbn, i)
	    print '    assign out_%d = loc_out_%d;' % (i, i)

    print

    for i in xrange(FB_O):
	    # assign myout1 = myin1 & myin2 & !myin3 & !myin4;
	    print '    assign loc_out_%d = %s;' % (i, ' & '.join([randnot() + 'in_%d' % i for i in xrange(fb_i)]))
    print 'endmodule'

def fb_inout(fbn):
    '''Connect given FB to matching inputs and outputs'''
    ipins = [('in_%d' % i, 'in_%d' % i) for i in xrange(FB_I)]
    opins = [('out_%d' % i, 'out_%d' % i) for i in xrange(FB_O)]
    module_connect('my_FB%s' % fbn, 'fb%d' % fbn,
        ipins + opins)

def run_fb2():
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
    FBS = 2
    # Use all inputs
    if 1:
        fb_i = 40
        fb_o = (64 - fb_i) / FBS
    # Use all outputs
    # uses all the pins...
    if 0:
        fb_o = 16
        fb_i = 40 - fb_o * FBS
    assert fb_i > 0
    assert fb_o > 0
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

#run_fb2()
run_fb_both()


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

# last one that doesn't completly explode
if 1:
    nin = 40
    nout = 16

# External inputs
FB_I = 40
# All PLA inputs (includes I/O / FF)
FB_IA = 56
# Outputs
FB_O = 16

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

def gen_fb_module(fbn):
    module_name = 'my_FB%d' % fbn
    ipins = [('input', 'in_%d' % i) for i in xrange(FB_I)]
    opins = [('output', 'out_%d' % i) for i in xrange(FB_O)]
    module_header(module_name, ipins + opins)

    print

    for i in xrange(nout):
        # XXX: think can combine these two lines 
	    print '    (* LOC="FB%d", keep="true", DONT_TOUCH="true" *) wire loc_out_%d;' % (fbn, i)
	    print '    assign out_%d = loc_out_%d;' % (i, i)

    print

    for i in xrange(nout):
	    # assign myout1 = myin1 & myin2 & !myin3 & !myin4;
	    print '    assign loc_out_%d = %s;' % (i, ' & '.join([randnot() + 'in_%d' % i for i in xrange(nin)]))
    print 'endmodule'

def fb_inout(fbn):
    ipins = [('in_%d' % i, 'in_%d' % i) for i in xrange(FB_I)]
    opins = [('out_%d' % i, 'out_%d' % i) for i in xrange(FB_O)]
    module_connect('my_FB%s' % fbn, 'fb%d' % fbn,
        ipins + opins)

def run():
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
run()


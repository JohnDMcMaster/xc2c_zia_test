'''
https://www.xilinx.com/support/documentation/sw_manuals/help/iseguide/mergedProjects/destech/html/ca_cpld_attributes.htm#NOREDUCE
'''

import random
import os
from __builtin__ import True

myrand = random.Random()
myrand.seed(0)

def randnot():
    return myrand.choice(['', '!'])

def randbool():
    return myrand.randint(0, 1)

def attr_str(attributes):
    if len(attributes) == 0:
        return ''
    return '(* ' + ', '.join(['%s="%s"' % (k, v) for k, v in attributes.items()]) + '*)'

def attr_barrier():
    #return ''
    attrs = {
        'KEEP': 'true',
        'DONT_TOUCH': 'true',
        'NOREDUCE': 'true',
        }
    return attr_str(attrs)

# External inputs
FB_I = 40
# All PLA inputs (includes I/O / FF)
FB_IA = 56
# Outputs
FB_O = 16
N_PINS = 33

# FB2 has CLK pin hogging input
fb_os = {1: 16, 2: 15}
# zia_w = 65
fb_ins = 40

if 1:
    FB_O = 8
    fb_os = {1: 8, 2: 8}

def module_header(name, pins):
    print 'module %s(' % name
    for pi, (pdir, name) in enumerate(pins):
        if pi != len(pins) - 1:
            eol = ','
        else:
            eol = ');'
        print '        %s wire %s%s' % (pdir, name, eol)

def module_header2(name, pins):
    print 'module %s(' % name
    for pi, (attr, pdir, wtype, name, init) in enumerate(pins):
        if init:
            inits = ' = %s' % init
        else:
            inits = ''
        if pi != len(pins) - 1:
            eol = ','
        else:
            eol = ');'
        print '        %s %s %s %s%s%s' % (attr, pdir, wtype, name, inits, eol)

def module_connect(module_name, instance_name, pins):
    print '    %s %s(' % (module_name, instance_name)
    for pi, (pin_name, net_name) in enumerate(pins):
        if pi != len(pins) - 1:
            eol = ','
        else:
            eol = ');'
        print '            .%s(%s)%s' % (pin_name, net_name, eol)



# tests without any inputs
# just internal FB testing
def attr_pterm(fbn, pi):
    # touching any of these forces it to a macrocell
    attrs = {
        "LOC": "FB%u" % fbn,
        }
    if fbn == 2:
        if pi == 0:
            attrs['KEEP'] = 'true'
        elif pi == 1:
            attrs['DONT_TOUCH'] =  'true'
        elif pi == 2:
            attrs['NOREDUCE'] =  'true'
    return attr_str(attrs)

def attr_oterm(fbn, oi):
    # these are even worse than pterm
    # any of these causes it to split both pterm and oterm to macrocell
    attrs = {
        "LOC": "FB%u" % fbn,
        }
    if fbn == 1:
        if oi == 0:
            attrs['KEEP'] = 'true'
        elif oi == 1:
            attrs['DONT_TOUCH'] =  'true'
        elif oi == 2:
            attrs['NOREDUCE'] =  'true'
    return attr_str(attrs)

def attr_ff(fbn, i):
    '''
    Activating will generate this message:
    ERROR:Cpld:8 - Cannot assign macrocell fb1_out_post_5 to Pin A2 (FB1_7). 
       Location is already occupied by fb1_out_post_7.
    '''
    #mc = ((i + 1) % 8) + 4
    #return attr_str({"LOC": "FB1_%u" % mc})
    return attr_str({
        "LOC": "FB%u" % fbn,
        "KEEP": "true",
        "DONT_TOUCH": "true",
        "NOREDUCE": "true",
        })

def gen_fb_counting(fbn):
    fb_i = FB_I
    fb_o = FB_O

    def gen_header():
        module_name = 'my_FB%d' % fbn
        pins = (
            [('', 'input', 'wire', 'clk', None)] +
            #[('', 'input', 'wire', 'in_%d' % i, None) for i in xrange(fb_i)] +
            [(attr_oterm(fbn, i), 'output', 'wire', 'out_pre_%d' % i, None) for i in xrange(fb_o)] +
            [(attr_ff(fbn, i), 'output', 'reg', 'out_post_%d' % i, '1\'b%d' % myrand.randint(0, 1)) for i in xrange(fb_o)]
            #[(attrs(i), 'output', 'reg', 'out_post_%d' % i, '1\'b%d' % 1) for i in xrange(fb_o)]
            )
        module_header2(module_name, pins)
    gen_header()

    print

    PTERMS = 3
    def gen_pterms():
        # Generate and terms
        print '    //P-terms'
        for pi in xrange(PTERMS):
            # Default 0 => invert to drop out
            terms = []
            #terms += ['!in_%d' % i for i in xrange(fb_i)]
            # Randomly include outputs
            for i in xrange(fb_o):
                # can create feedback loops
                # lets skip these for now
                #if randbool():
                #    terms += [randnot() + 'out_pre_%d' % i,]
                if randbool() or (i == fb_o - 1 and len(terms) == 0):
                    terms += [randnot() + 'out_post_%d' % i,]
                    #terms += ['out_post_%d' % i,]
            print '    %s wire pterm_%d = %s;' % (attr_pterm(fbn, pi), pi, ' & '.join(terms))
    gen_pterms()

    print

    def gen_orterm():
        print '    //OR terms'
        for outi in xrange(fb_o):
            terms = []
            for pi in xrange(PTERMS):
                def gen_term():
                    if pi == PTERMS - 1 and len(terms) == 0:
                        return True
                    # Count up terms to make sure they are all unique
                    gen = 1 ^ int(bool(outi & (1 << pi)))
                    # gen = gen ^ randbool()
                    return gen
                if gen_term():
                    terms += ['pterm_%d' % pi,]
            print '    assign out_pre_%d = %s;' % (outi, ' | '.join(terms))
    gen_orterm()

    print

    def gen_ff():
        print '    always @(posedge clk) begin'
        for outi in xrange(fb_o):
            print '        out_post_%d <= out_pre_%d;' % (outi, outi)
        print '    end'
    gen_ff()

    print 'endmodule'

def run():
    FBS = 2
    print '`timescale 1ns / 1ps'
    print '`default_nettype none'
    print
    module_name = 'top'

    pins = []
    # Will get placed on CLK pin
    pins += [('input', 'clk')]
    # Use all outputs
    for fb, outputs in fb_os.items():
        if fb > FBS:
            break
        pins += [('output', 'fb%u_out_post_%d' % (fb, i)) for i in xrange(outputs)]
    module_header(module_name, pins)

    # Make sure clock gets routed correctly
    print
    print '    wire clk_buf;'
    print '    BUFG bufg(.I(clk), .O(clk_buf));'

    for fbi in xrange(FBS):
        print
        fbn = fbi + 1
        for outi in xrange(FB_O):
            print '    wire fb%u_out_pre_%u;' % (fbn, outi)
            if outi >= fb_os[fbn]:
                print '    wire fb%u_out_post_%u; //no pin' % (fbn, outi)
    print

    for fbi in xrange(FBS):
        fbn = fbi + 1
        print

        pins = [('clk', 'clk_buf')]

        pins += [('out_pre_%d' % i, '') for i in xrange(FB_O)]
        pins += [('out_post_%d' % i, 'fb%d_out_post_%d' % (fbn, i)) for i in xrange(FB_O)]
        module_connect('my_FB%s' % fbn, 'fb%d' % fbn, pins)
    print 'endmodule'

    for fbi in xrange(FBS):
        print
        gen_fb_counting(fbi + 1)

run()


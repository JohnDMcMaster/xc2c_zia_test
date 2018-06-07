'''
https://www.xilinx.com/support/documentation/sw_manuals/help/iseguide/mergedProjects/destech/html/ca_cpld_attributes.htm#NOREDUCE

Magic tricks:
-(* KEEP="true", DONT_TOUCH="true" *)
-(* LOC="FB%d *): can be applied to output pins only. I'm applying to FF's
-NOREDUCE: look into, see note below

WARNING:Cpld - The signal(s) 'fb1/pterm_1' are in combinational feedback loops.
   These signals may cause hazards/glitches. Apply the NOREDUCE parameter to the
   hazard reduction circuitry.
   Timing analysis of paths involving this node may be inaccurate or incomplete.
https://www.xilinx.com/support/answers/9912.html
flatten hierarchy must be set

Set user-defined property "source_node =  yes" for signal <pterm_33> in unit <my_FB2>.
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
#FB_O = 16
N_PINS = 33

fb_os = {1: 8, 2: 8}
fb_is = fb_os

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




def attr_ff(fbn, i):
    return attr_str({
        # possibly excessive and difficult to manage with clk in the mix
        #"LOC": "FB%u_%u" % (fbn, i + 1),
        "LOC": "FB%u" % (fbn,),

        'KEEP': 'true',
        'DONT_TOUCH': 'true',
        'NOREDUCE': 'true',
        })

# tests without any inputs
# just internal FB testing
def attr_pterm():
    return attr_str({
        # touching any of these forces it to a macrocell
        #'KEEP': 'true',
        #'DONT_TOUCH': 'true',
        #'NOREDUCE': 'true',
        })

def attr_oterm():
    return attr_str({
        # these are even worse than pterm
        # any of these causes it to split both pterm and oterm to macrocell
        #'KEEP': 'true',
        #'DONT_TOUCH': 'true',
        #'NOREDUCE': 'true',
        })

def gen_fb_lfsr(fbn):
    '''Generate FBs as an XOR ring osc'''
    fb_i = fb_is[fbn]
    fb_o = fb_os[fbn]


    def gen_header():
        module_name = 'my_FB%d' % fbn
        pins = (
            [('', 'input', 'wire', 'clk', None)] +
            [('', 'input', 'wire', 'in_%d' % i, None) for i in xrange(fb_i)] +
            [(attr_oterm(), 'output', 'wire', 'out_pre_%d' % i, None) for i in xrange(fb_o)] +
            [(attr_ff(fbn, i), 'output', 'reg', 'out_post_%d' % i, '1\'b%d' % myrand.randint(0, 1)) for i in xrange(fb_o)]
            )
        module_header2(module_name, pins)
    gen_header()

    print

    '''
    ff1 <= ...
    ff2 <= (ff1 & !ff2) | (!ff1 & ff2)
    ff3 <= (ff2 & !ff3) | (!ff2 & ff3)
    '''
    # Connect to previous
    def gen_pterms():
        # Generate and terms
        print '    //P-terms'
        for pi in xrange(fb_o):
            wl = 'out_post_%d' % ((pi + 2) % fb_o,)
            wr = 'out_post_%d' % ((pi + 5) % fb_o,)
            # XXX: only using FB_O (16) inputs
            wi = 'in_%d' % (pi,)
            # 3 input XOR
            # 3 pterms * 16 max => 48
            # within 56 cell limit I think?
            print '    %s wire pterm_%dl = %s;' % (attr_pterm(), pi, ' & '.join([wl, '!' + wr, '!' + wi]))
            print '    %s wire pterm_%dr = %s;' % (attr_pterm(), pi, ' & '.join(['!' + wl, wr, '!' + wi]))
            print '    %s wire pterm_%di = %s;' % (attr_pterm(), pi, ' & '.join(['!' + wl, '!' + wr, wi]))
    gen_pterms()

    print

    # Passthrough
    def gen_orterm():
        print '    //OR terms'
        for outi in xrange(fb_o):
            terms = []
            terms += ['pterm_%dl' % outi, 'pterm_%dr' % outi, 'pterm_%di' % outi]
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

def run_fuzzer3():
    FBS = 2
    print '`timescale 1ns / 1ps'
    print '`default_nettype none'
    print
    # top
    module_name = 'top'

    conn_src = (1, int(os.getenv('ZIA_SRC', '-1')))
    conn_dst = (2, int(os.getenv('ZIA_DST', '-1')))

    pins = []
    # Will get placed on CLK pin
    pins += [('', 'input', 'wire', 'clk', '')]
    # dedicated input: with all other I/O allocated, will be forced to this pin
    pins += [('', 'input', 'wire', 'ded_in', '')]
    # Use all outputs
    for fbn, outputs in fb_os.items():
        def attrs(fbn, i):
            if fbn == 2 and i == 0:
                return attr_ff(fbn, i)
            else:
                return ''
        pins += [(attrs(fbn, i), 'output', 'wire', 'fb%u_out_post_%d' % (fbn, i), '') for i in xrange(outputs)]
    module_header2(module_name, pins)

    # Make sure clock gets routed correctly
    print
    print '    wire clk_buf;'
    print '    BUFG bufg(.I(clk), .O(clk_buf));'

    for fbi in xrange(FBS):
        print
        fbn = fbi + 1
        for outi in xrange(fb_os[fbn]):
            print '    wire fb%u_out_pre_%u;' % (fbn, outi)
            if outi >= fb_os[fbn]:
                print '    wire fb%u_out_post_%u; //no pin' % (fbn, outi)
    print

    '''
    Assign FB inputs randomly
    Each wire can be assigned 3-4 times max, so don't exceed 3

    "65 choose 40"
    Don't choose the same signal twice on either side since they'll be optimized down to 1 signal
    ''' 
    def assign_fb_ins():
        for fbn in xrange(1, 3):
            for ini in xrange(FB_I):
                fbn_c = {1:2, 2:1}[fbn]
                if ini < 0:
                    src = 'fb%u_out_pre_%u' % (fbn_c, ini)
                elif fbn == 1 and ini < 1:
                    src = 'fb%u_out_post_%u' % (fbn_c, ini)
                else:
                    src = "1'b0"
                print '    wire fb%u_in_%u = %s;' % (fbn, ini, src)
        print
    assign_fb_ins()

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

        pins += [('in_%d' % i, 'fb%d_in_%d' % (fbn, i)) for i in xrange(fb_is[fbi + 1])]
        pins += [('out_pre_%d' % i, 'fb%d_out_pre_%d' % (fbn, i)) for i in xrange(fb_os[fbn])]
        pins += [('out_post_%d' % i, 'fb%d_out_post_%d' % (fbn, i)) for i in xrange(fb_os[fbn])]
        module_connect('my_FB%s' % fbn, 'fb%d' % fbn, pins)
    print 'endmodule'

    for fbi in xrange(FBS):
        print
        #gen_fb_rand2(fbi + 1)
        #gen_fb_ring(fbi + 1)
        gen_fb_lfsr(fbi + 1)









run_fuzzer3()

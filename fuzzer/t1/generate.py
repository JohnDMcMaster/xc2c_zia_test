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
FB_O = 16
N_PINS = 33

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




if 0:
    def gen_fb_rand(fbn):
        fb_i = FB_I
        fb_o = FB_O
    
        def gen_header():
            def attrs(i):
                return attr_barrier()
                attrs = {
                    'KEEP': 'true',
                    'DONT_TOUCH': 'true',
                    }
                # WARNING: xst will hard crash if this line is removed
                # (LOC'd more pins than exist)
                #if not (fbn == 2 and i == 15):
                #    attrs['LOC'] = "FB%d" % fbn
                return attr_str(attrs)
            module_name = 'my_FB%d' % fbn
            pins = (
                [('', 'input', 'wire', 'clk', None)] +
                [('', 'input', 'wire', 'in_%d' % i, None) for i in xrange(fb_i)] +
                [('', 'output', 'wire', 'out_pre_%d' % i, None) for i in xrange(fb_o)] +
                [(attrs(i), 'output', 'reg', 'out_post_%d' % i, '1\'b%d' % myrand.randint(0, 1)) for i in xrange(fb_o)]
                #[(attrs(i), 'output', 'reg', 'out_post_%d' % i, '1\'b%d' % 1) for i in xrange(fb_o)]
                )
            module_header2(module_name, pins)
        gen_header()
    
        print
    
        PTERMS = 40
        PTERMS = 3
        def gen_pterms():
            # Generate and terms
            print '    //P-terms'
            for pi in xrange(PTERMS):
                # Default 0 => invert to drop out
                terms = ['!in_%d' % i for i in xrange(fb_i)]
                # Randomly include outputs
                for i in xrange(fb_o):
                    # can create feedback loops
                    # lets skip these for now
                    #if randbool():
                    #    terms += [randnot() + 'out_pre_%d' % i,]
                    if randbool() or (i == fb_o - 1 and len(terms) == 0):
                        terms += [randnot() + 'out_post_%d' % i,]
                        #terms += ['out_post_%d' % i,]
                attrs = '(* NOREDUCE="true" *)'
                attrs = attr_barrier()
                print '    %s wire pterm_%d = %s;' % (attrs, pi, ' & '.join(terms))
        gen_pterms()
    
        print
    
        def gen_orterm():
            print '    //OR terms'
            for outi in xrange(fb_o):
                terms = []
                for pi in xrange(PTERMS):
                    if randbool() or (pi == PTERMS - 1 and len(terms) == 0):
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
    
    def run_fuzzer():
        '''
        There are 40 inputs on each FB
    
        General notes:
        -ZIA bus is 65 wide
            Each FB supplying 16 pre-FF output + 16 post-FF output => 2 * 32 => 64
            Dedicated input
        -40 FB inputs
        -Each FB input can attach to one of 6 bus wires (+ vdd and ground)
        -Total number connections (bits to solve): 6 * 40 = 240
        -If was split evenly among bus: 240 / 65 = 3.7
        -It seems in general things can connect to 3 or 4 inputs, so never specify something more than 3 times for now 
    
        Note pins (expect for the dedicated input) do not appear on ZIA
        '''
    
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
        pins += [('input', 'clk')]
        # dedicated input: with all other I/O allocated, will be forced to this pin
        pins += [('input', 'ded_in')]
        # Use all outputs
        for fb, outputs in fb_os.items():
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
                    if 0:
                        pass
                    #if ini < 4:
                    #    src = 'fb%u_out_pre_%u' % (fbn_c, ini)
                    elif ini < 8:
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
    
            pins += [('in_%d' % i, 'fb%d_in_%d' % (fbn, i)) for i in xrange(fb_ins)]
            pins += [('out_pre_%d' % i, 'fb%d_out_pre_%d' % (fbn, i)) for i in xrange(FB_O)]
            pins += [('out_post_%d' % i, 'fb%d_out_post_%d' % (fbn, i)) for i in xrange(FB_O)]
            module_connect('my_FB%s' % fbn, 'fb%d' % fbn, pins)
        print 'endmodule'
    
        print
        gen_fb_rand(1)
        print
        gen_fb_rand(2)









# tests without any inputs
# just internal FB testing
if 1:
    def attr_pterm():
        attrs = {
            # touching any of these forces it to a macrocell
            #'KEEP': 'true',
            #'DONT_TOUCH': 'true',
            #'NOREDUCE': 'true',
            }
        return attr_str(attrs)
    
    def attr_oterm():
        attrs = {
            # these are even worse than pterm
            # any of these causes it to split both pterm and oterm to macrocell
            #'KEEP': 'true',
            #'DONT_TOUCH': 'true',
            #'NOREDUCE': 'true',
            }
        return attr_str(attrs)

    def attr_ff(fbn, i):
        if 1:
            attrs = {
                'KEEP': 'true',
                'DONT_TOUCH': 'true',
                'NOREDUCE': 'true',
                }
            return attr_str(attrs)
        if 0:
            return attr_str({"LOC": "FB%d" % fbn})
        if 0:
            return attr_str({"LOC": "FB2"})
        # internal error
        # think this is caused by CLK needing to go on certain FB2 pin
        if 0:
            mc = ((i + 1) % 8) + 1
            return attr_str({"LOC": "FB2_%u" % mc})
        # seems to work
        if 0:
            mc = ((i + 1) % 8) + 1
            return attr_str({"LOC": "FB1_%u" % mc})
        if 0:
            return attr_barrier()
        if 0:
            attrs = {
                'KEEP': 'true',
                'DONT_TOUCH': 'true',
                }
            # WARNING: xst will hard crash if this line is removed
            # (LOC'd more pins than exist)
            #if not (fbn == 2 and i == 15):
            #    attrs['LOC'] = "FB%d" % fbn
            return attr_str(attrs)
    
    def gen_fb_rand2(fbn):
        fb_i = FB_I
        fb_o = FB_O
    
        def gen_header():
            module_name = 'my_FB%d' % fbn
            pins = (
                [('', 'input', 'wire', 'clk', None)] +
                #[('', 'input', 'wire', 'in_%d' % i, None) for i in xrange(fb_i)] +
                [(attr_oterm(), 'output', 'wire', 'out_pre_%d' % i, None) for i in xrange(fb_o)] +
                [(attr_ff(fbn, i), 'output', 'reg', 'out_post_%d' % i, '1\'b%d' % myrand.randint(0, 1)) for i in xrange(fb_o)]
                #[(attrs(i), 'output', 'reg', 'out_post_%d' % i, '1\'b%d' % 1) for i in xrange(fb_o)]
                )
            module_header2(module_name, pins)
        gen_header()
    
        print
    
        PTERMS = 40
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
                print '    %s wire pterm_%d = %s;' % (attr_pterm(), pi, ' & '.join(terms))
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

    def gen_fb_ring(fbn):
        '''Generate FBs as a ring osc'''
        fb_i = FB_I
        fb_o = FB_O

        def attr_ff(fbn, i):
            mc = ((i + 1) % 8) + 1
            return attr_str({"LOC": "FB1_%u" % mc})

        def gen_header():
            module_name = 'my_FB%d' % fbn
            pins = (
                [('', 'input', 'wire', 'clk', None)] +
                [(attr_oterm(), 'output', 'wire', 'out_pre_%d' % i, None) for i in xrange(fb_o)] +
                [(attr_ff(fbn, i), 'output', 'reg', 'out_post_%d' % i, '1\'b%d' % myrand.randint(0, 1)) for i in xrange(fb_o)]
                )
            module_header2(module_name, pins)
        gen_header()
    
        print
    
        # Connect to previous
        def gen_pterms():
            # Generate and terms
            print '    //P-terms'
            for pi in xrange(fb_o):
                terms = []
                terms += ['out_post_%d' % ((pi - 1) % fb_o,),]
                print '    %s wire pterm_%d = %s;' % (attr_pterm(), pi, ' & '.join(terms))
        gen_pterms()
    
        print
    
        # Passthrough
        def gen_orterm():
            print '    //OR terms'
            for outi in xrange(fb_o):
                terms = []
                terms += ['pterm_%d' % outi,]
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
    
    def run_fuzzer2():
        '''
        There are 40 inputs on each FB
    
        General notes:
        -ZIA bus is 65 wide
            Each FB supplying 16 pre-FF output + 16 post-FF output => 2 * 32 => 64
            Dedicated input
        -40 FB inputs
        -Each FB input can attach to one of 6 bus wires (+ vdd and ground)
        -Total number connections (bits to solve): 6 * 40 = 240
        -If was split evenly among bus: 240 / 65 = 3.7
        -It seems in general things can connect to 3 or 4 inputs, so never specify something more than 3 times for now 
    
        Note pins (expect for the dedicated input) do not appear on ZIA
        '''
    
        FBS = 1
        print '`timescale 1ns / 1ps'
        print '`default_nettype none'
        print
        # top
        module_name = 'top'
    
        pins = []
        # Will get placed on CLK pin
        pins += [('input', 'clk')]
        # dedicated input: with all other I/O allocated, will be forced to this pin
        #pins += [('input', 'ded_in')]
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
    
        '''
        Assign FB inputs randomly
        Each wire can be assigned 3-4 times max, so don't exceed 3
    
        "65 choose 40"
        Don't choose the same signal twice on either side since they'll be optimized down to 1 signal
        ''' 
        '''
        def assign_fb_ins():
            for fbn in xrange(1, 3):
                for ini in xrange(FB_I):
                    fbn_c = {1:2, 2:1}[fbn]
                    if 0:
                        pass
                    #if ini < 4:
                    #    src = 'fb%u_out_pre_%u' % (fbn_c, ini)
                    elif ini < 8:
                        src = 'fb%u_out_post_%u' % (fbn_c, ini)
                    else:
                        src = "1'b0"
                    print '    wire fb%u_in_%u = %s;' % (fbn, ini, src)
            print
        assign_fb_ins()
        '''
    
        for fbi in xrange(FBS):
            fbn = fbi + 1
            print
    
            pins = [('clk', 'clk_buf')]
    
            #pins += [('in_%d' % i, 'fb%d_in_%d' % (fbn, i)) for i in xrange(fb_ins)]
            #pins += [('out_pre_%d' % i, 'fb%d_out_pre_%d' % (fbn, i)) for i in xrange(FB_O)]
            pins += [('out_pre_%d' % i, '') for i in xrange(FB_O)]
            pins += [('out_post_%d' % i, 'fb%d_out_post_%d' % (fbn, i)) for i in xrange(FB_O)]
            module_connect('my_FB%s' % fbn, 'fb%d' % fbn, pins)
        print 'endmodule'
    
        for fbi in xrange(FBS):
            print
            #gen_fb_rand2(fbi + 1)
            gen_fb_ring(fbi + 1)












#run_fuzzer()
run_fuzzer2()


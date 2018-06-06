import random
import os

myrand = random.Random()
myrand.seed(0)

def randnot():
    return ''
    return myrand.choice(['', '!'])

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

def gen_fb_shift_module2(fbn):
    fb_i = FB_I
    fb_o = FB_O

    def attrs(i):
        locstr = 'LOC="FB%d", ' % fbn
        # WARNING: xst will hard crash if this line is removed
        # (LOC'd more pins than exist)
        if i == 15:
            locstr = ''
        return '(* %skeep="true", DONT_TOUCH="true" *)' % locstr

    module_name = 'my_FB%d' % fbn
    pins = (
        [('', 'input', 'wire', 'clk', None)] +
        [('', 'input', 'wire', 'in_%d' % i, None) for i in xrange(fb_i)] +
        [('', 'output', 'wire', 'out_pre_%d' % i, None) for i in xrange(fb_o)] +
        [(attrs(i), 'output', 'reg', 'out_post_%d' % i, '1\'b%d' % myrand.randint(0, 1)) for i in xrange(fb_o)]
        )
    module_header2(module_name, pins)

    print
    print

    print
    for outi in xrange(fb_o):
        terms = [randnot() + 'in_%d' % i for i in xrange(fb_i)]
        # FF chain prevents many optimizations
        terms += ['out_post_%d' % ((outi - 1) % fb_o,)]
        print '    assign out_pre_%d = %s;' % (outi, ' | '.join(terms))

    print
    print
    print '    always @(posedge clk) begin'
    for outi in xrange(fb_o):
        print '        out_post_%d <= out_pre_%d;' % (outi, outi)
    print '    end'

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
    print
    # top
    module_name = 'top'

    conn_src = (1, int(os.getenv('ZIA_SRC', '-1')))
    conn_dst = (2, int(os.getenv('ZIA_DST', '-1')))

    fb_os = {1: 16, 2: 15}
    # zia_w = 65
    fb_ins = 40

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
        freqs = {}
        freqs[('ded_in',)] = 0
        if 0:
            for fbn in xrange(1, 3):
                for ini in xrange(FB_O):
                    freqs[('out_pre', fbn, ini)] = 0
                    # FFs setup as ring buffer
                    freqs[('out_post', fbn, ini)] = 1

        for fbi in xrange(FBS):
            print
            fbn = fbi + 1
            for ini in xrange(FB_I):
                # lets do something more predictable
                if fbn == 1 and ini < 16:
                    src_wire = 'fb%u_%s_%d' % (2, 'out_post', ini)
                elif fbn == 2 and ini < 16:
                    src_wire = 'fb%u_%s_%d' % (1, 'out_post', ini)
                elif fbn == 1 and ini < 32:
                    src_wire = 'fb%u_%s_%d' % (2, 'out_pre', ini - 16)
                #elif fbn == 2 and ini < 17:
                #    src_wire = 'fb%u_%s_%d' % (1, 'out_pre', ini - 16)
                elif 0 and (fbn == 1 and ini < 40):
                    while True:
                        randkey = myrand.choice(freqs.keys())
                        if 1 or freqs[randkey] < 3:
                            break
                    if randkey[0] == 'ded_in':
                        src_wire = 'ded_in'
                    else:
                        where, rand_fbn, rand_ini = randkey
                        src_wire = 'fb%u_%s_%d' % (rand_fbn, where, rand_ini)
                    freqs[randkey] += 1
                else:
                    src_wire = "1'b0"
                print '    wire fb%u_in_%u = %s;' % (fbn, ini, src_wire)
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
    gen_fb_shift_module2(1)
    print
    gen_fb_shift_module2(2)

run_fuzzer()

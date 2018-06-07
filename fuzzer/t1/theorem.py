'''
Convention
FB's are indexed as 1/2 to keep consistency with FB1/FB2 naming
'''

import re

def load_jed_bits(fin):
    '''
    Note Block 1 *
    Note Block 1 ZIA *
    '''

    ret = {}
    txt = fin.read()
    for blocki, block in enumerate(txt.split('ZIA')[1:]):
        rows = []
        for l in block.split('\n'):
            l = l.strip()
            # end of table?
            if not l:
                break
            m = re.match(r'L(......) (........)\*', l)
            if not m:
                continue
            addr = int(m.group(1), 10)
            bits = int(m.group(2), 2)
            assert 0x00 <= bits <= 0xFF, bits
            rows.append((addr, bits))
        # 40 inputs
        assert len(rows) == 40
        ret[blocki + 1] = rows

    assert len(ret) == 2
    print 'JED: load %d entries' % sum([len(x) for x in ret.values()])
    return ret

def load_vm6_imuxes(fin):
    '''
    Find and parse lines like:
    FB_IMUX_INDEX | FOOBAR1_ | 46 | 48 | 35 |...
    FB_IMUX_INDEX | FOOBAR2_ | 58...
    '''
    ret = {}
    for l in fin:
        parts = l.replace(' ', '').split('|')
        if parts[0] != 'FB_IMUX_INDEX':
            continue
        # FOOBAR1_, FOOBAR2_
        m = re.match(r'FOOBAR(.*)_', parts[1])
        fbn = int(m.group(1))
        indexes = parts[2:]
        # 40 inputs
        assert len(indexes) == 40
        ret[fbn] = [int(index) for index in indexes]

    assert len(ret) == 2
    print 'VM6: load %d entries' % sum([len(x) for x in ret.values()])
    return ret

def run(jedf, vm6f, fout):
    '''
    The MSB is active high, drives bus high
    All other bits are active low

    segbits format example
    CLB.SLICE_X0.A5FF.MUX.A 30_09
    
    so maybe something like
    FB.IN[0].FB1_IBUF[0] 00_0
    FB.IN[8].FB2_IBUF[1] 08_1

    data structure with
    dict name to offset + bit i
    ex: {
        'FB.IN[0].FB1_IBUF[0]': (00, 0),
        'FB.IN[8].FB2_IBUF[1]': (08, 1),
    Note that row number should always be the same as the offset
    '''

    zia_bits = load_jed_bits(jedf)
    zia_imuxes = load_vm6_imuxes(vm6f)
    results = {}

    print zia_imuxes
    for fb in xrange(1, 3):
        def add_result(name, addr, biti):
            #name = ('FB%u.' % fb) + name
            name = 'FB.' + name
            # take off base address
            #addr = addr & 0x000FFF
            # 0x17f0
            if addr >= 6128:
                addr -= 6128
    
            if name in results:
                old = results[name]
                assert old == (addr, biti), "duplicate name %s w/ old (%03u, %u), new (%03u, %u)" % (name, old[0], old[1], addr, biti)
            else:
                results[name] = (addr, biti)

        for row, ((addr, bits), imux) in enumerate(zip(zia_bits[fb], zia_imuxes[fb])):
            # Unused entry?
            if imux == -1:
                assert bits == 0xFF
                continue
            # bus is 65 bits wide (2 * 16 + 2 * 16 + 1)
            assert 0 <= imux <= 64

            # There should be exactly two bits clear then
            # MSB must be clear (don't drive 1 onto bus)
            assert bits & 0x80 == 0x00
            add_result('FB.IN[%u].LOGIC1' % row, addr, 7)

            # Lets hack in bit 6 since we happen to know what it is
            # We don't expect to ever see it though
            assert bits & 0x40 == 0x40
            add_result('FB.IN[%u].LOGIC0' % row, addr, 6)

            # Now there should be exactly one bit set
            def cfg(biti):
                return 0x7F ^ (1 << biti)
            biti = {
                cfg(0): 0,
                cfg(1): 1,
                cfg(2): 2,
                cfg(3): 3,
                cfg(4): 4,
                cfg(5): 5,
                }[bits]

            '''
            Determine postfix and add
            From "not datasheet":
            -ZIABUS[15:0] = FB1 IBUF[15:0]
            -ZIABUS[16] = dedicated input pin
            -ZIABUS[32:17] = FB2 IBUF[15:0]
            -ZIABUS[48:33] = FB1 FF[15:0]
            -ZIABUS[64:49] = FB2 FF[15:0]
            '''
            if 0 <= imux <= 15:
                add_result('IN[%u].FB1_IBUF[%u]' % (row, imux), addr, biti)
            elif imux == 16:
                add_result('IN[%u].IPIN' % (row,), addr, biti)
            elif 17 <= imux <= 32:
                add_result('IN[%u].FB2_IBUF[%u]' % (row, imux - 17), addr, biti)
            elif 33 <= imux <= 48:
                add_result('IN[%u].FB1_FF[%u]' % (row, imux - 33), addr, biti)
            elif 49 <= imux <= 64:
                add_result('IN[%u].FB2_FF[%u]' % (row, imux - 49), addr, biti)
            else:
                assert 0

    for name, (addr, biti) in sorted(results.items()):
        fout.write('%s %02X_%d\n' % (name, addr, biti))

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description=
        'Find bit locations'
    )

    parser.add_argument('--verbose', type=int, help='')
    parser.add_argument('jed', help='.jed input file')
    parser.add_argument('vm6', help='.vm6 input file')
    parser.add_argument('segbits', help='segbits output file')
    args = parser.parse_args()
    run(open(args.jed, 'r'), open(args.vm6, 'r'), open(args.segbits, 'w'))

if __name__ == '__main__':
    main()

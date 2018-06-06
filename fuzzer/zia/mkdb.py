'''
Convention
FB's are indexed as 1/2 to keep consistency with FB1/FB2 naming
'''

import re

def load_db(fin):
    ret = {}
    for l in fin:
        # FB2.FB.IN[7].LOGIC0 38_6
        name, addri = l.strip().split()
        addr, offi = addri.split('_')
        ret[name] = (int(addr, 16), int(offi, 10))
    return ret

def run(fs, fout=None, verbose=False):
    db = {}
    for f in fs:
        new_db = load_db(f)
        for k, v in new_db.items():
            if k in db:
                assert db[k] == v
            else:
                db[k] = v

    # Index by bit position
    dbr = {}
    for k, v in db.items():
        assert v not in dbr, (k, v, dbr[v])
        dbr[v] = k
    assert len(dbr) == len(db), (len(dbr), len(db))

    # See which entires are missing
    good = 0
    bad = 0
    for addr in range(0, 320, 8):
        for offi in range(8):
            if (addr, offi) in dbr:
                good += 1
            else:
                bad += 1
                if verbose:
                    print 'Need %03u_%u' % (addr, offi)
    assert good == len(dbr)
    net = good + bad
    print 'DB: %s / %s filled' % (good, net)

def main():
    import argparse
    import glob

    parser = argparse.ArgumentParser(
        description=
        'Aggregate segdata files'
    )

    parser.add_argument('--verbose', type=int, help='')
    parser.add_argument('--out', help='segbits output file')
    parser.add_argument('ins', nargs='*', help='segbits input files')
    args = parser.parse_args()
    ins = args.ins
    if not ins:
        ins = glob.glob('specimen_*/*.segbits')
    assert len(ins) != 0
    run([open(x, 'r') for x in ins], open(args.out, 'w' ) if args.out else None)

if __name__ == '__main__':
    main()

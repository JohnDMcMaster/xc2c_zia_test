'''
/*
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
*/

`timescale 1ns / 1ps
module top(
    input wire myin1,
    input wire myin2,
    input wire myin3,
    input wire myin4,
    output wire myout1,
    output wire myout2,
    output wire myout3
    );

	assign myout1 = myin1 & myin2 & !myin3 & !myin4;
	assign myout2 = !myin1 & myin2 & !myin3 & !myin4;
	assign myout3 = myin1 & !myin2 & !myin3 & !myin4;
endmodule

NET mynet LOC=FBxx;
'''

import random

random.seed(0)

nin = 4
nout = 16

print '`timescale 1ns / 1ps'
print 'module top('

for i in xrange(nin):
    print '    input wire myin%d,' % i

for i in xrange(nout):
    print '    output wire myout%d_out' % i,
    if i != nout - 1:
        print ','
    else:
        print
print '    );'
print

def randnot():
    return random.choice(['', '!'])

for i in xrange(nout):
	print '    (* LOC="FB2" *) wire myout%d;' % (i)
	print '    assign myout%d_out = myout%d;' % (i, i)

for i in xrange(nout):
	# assign myout1 = myin1 & myin2 & !myin3 & !myin4;
	print '    assign myout%d = %s;' % (i, ' & '.join([randnot() + 'myin%d' % i for i in xrange(nin)]))

print 'endmodule'


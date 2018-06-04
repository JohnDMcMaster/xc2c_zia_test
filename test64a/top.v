//fb_i 39
//fb_o 4
`timescale 1ns / 1ps

module top(
        input wire clk,
        input wire in_0,
        input wire in_1,
        input wire in_2,
        input wire in_3,
        input wire in_4,
        input wire in_5,
        input wire in_6,
        input wire in_7,
        input wire in_8,
        input wire in_9,
        input wire in_10,
        input wire in_11,
        input wire in_12,
        input wire in_13,
        input wire in_14,
        input wire in_15,
        input wire in_16,
        input wire in_17,
        input wire in_18,
        input wire in_19,
        input wire in_20,
        input wire in_21,
        input wire in_22,
        input wire in_23,
        input wire in_24,
        input wire in_25,
        input wire in_26,
        input wire in_27,
        input wire in_28,
        input wire in_29,
        input wire in_30,
        input wire in_31,
        input wire in_32,
        input wire in_33,
        input wire in_34,
        input wire in_35,
        input wire in_36,
        input wire in_37,
        input wire in_38,
        input wire in_39,
        output wire out_0,
        output wire out_1,
        output wire out_2,
        output wire out_3,
        output wire out_4,
        output wire out_5,
        output wire out_6,
        output wire out_7);

    my_FB1 fb1(
            .clk(clk),
            .out_0(out_0),
            .out_1(out_1),
            .out_2(out_2),
            .out_3(out_3),
            .in_0(out_6),
            .in_1(in_1),
            .in_2(in_2),
            .in_3(in_3),
            .in_4(in_4),
            .in_5(in_5),
            .in_6(in_6),
            .in_7(in_7),
            .in_8(in_8),
            .in_9(in_9),
            .in_10(in_10),
            .in_11(in_11),
            .in_12(in_12),
            .in_13(in_13),
            .in_14(in_14),
            .in_15(in_15),
            .in_16(in_16),
            .in_17(in_17),
            .in_18(in_18),
            .in_19(in_19),
            .in_20(in_20),
            .in_21(in_21),
            .in_22(in_22),
            .in_23(in_23),
            .in_24(in_24),
            .in_25(in_25),
            .in_26(in_26),
            .in_27(in_27),
            .in_28(in_28),
            .in_29(in_29),
            .in_30(in_30),
            .in_31(in_31),
            .in_32(in_32),
            .in_33(in_33),
            .in_34(in_34),
            .in_35(in_35),
            .in_36(in_36),
            .in_37(in_37),
            .in_38(in_38));

    my_FB2 fb2(
            .clk(clk),
            .out_0(out_4),
            .out_1(out_5),
            .out_2(out_6),
            .out_3(out_7),
            .in_0(out_1),
            .in_1(in_1),
            .in_2(in_2),
            .in_3(in_3),
            .in_4(in_4),
            .in_5(in_5),
            .in_6(in_6),
            .in_7(in_7),
            .in_8(in_8),
            .in_9(in_9),
            .in_10(in_10),
            .in_11(in_11),
            .in_12(in_12),
            .in_13(in_13),
            .in_14(in_14),
            .in_15(in_15),
            .in_16(in_16),
            .in_17(in_17),
            .in_18(in_18),
            .in_19(in_19),
            .in_20(in_20),
            .in_21(in_21),
            .in_22(in_22),
            .in_23(in_23),
            .in_24(in_24),
            .in_25(in_25),
            .in_26(in_26),
            .in_27(in_27),
            .in_28(in_28),
            .in_29(in_29),
            .in_30(in_30),
            .in_31(in_31),
            .in_32(in_32),
            .in_33(in_33),
            .in_34(in_34),
            .in_35(in_35),
            .in_36(in_36),
            .in_37(in_37),
            .in_38(in_38));
endmodule

module my_FB1(
        input wire in_0,
        input wire in_1,
        input wire in_2,
        input wire in_3,
        input wire in_4,
        input wire in_5,
        input wire in_6,
        input wire in_7,
        input wire in_8,
        input wire in_9,
        input wire in_10,
        input wire in_11,
        input wire in_12,
        input wire in_13,
        input wire in_14,
        input wire in_15,
        input wire in_16,
        input wire in_17,
        input wire in_18,
        input wire in_19,
        input wire in_20,
        input wire in_21,
        input wire in_22,
        input wire in_23,
        input wire in_24,
        input wire in_25,
        input wire in_26,
        input wire in_27,
        input wire in_28,
        input wire in_29,
        input wire in_30,
        input wire in_31,
        input wire in_32,
        input wire in_33,
        input wire in_34,
        input wire in_35,
        input wire in_36,
        input wire in_37,
        input wire in_38,
        output wire out_0,
        output wire out_1,
        output wire out_2,
        output wire out_3,
        input wire clk);



    (* LOC="FB1", keep="true", DONT_TOUCH="true" *) reg ff_0 = 1'b1;
    assign out_0 = ff_0;

    (* LOC="FB1", keep="true", DONT_TOUCH="true" *) reg ff_1 = 1'b0;
    assign out_1 = ff_1;

    (* LOC="FB1", keep="true", DONT_TOUCH="true" *) reg ff_2 = 1'b1;
    assign out_2 = ff_2;

    (* LOC="FB1", keep="true", DONT_TOUCH="true" *) reg ff_3 = 1'b0;
    assign out_3 = ff_3;


    always @(posedge clk) begin
        ff_0 <= in_0 & in_1 & in_2 & in_3 & in_4 & in_5 & in_6 & in_7 & in_8 & in_9 & in_10 & in_11 & in_12 & in_13 & in_14 & in_15 & in_16 & in_17 & in_18 & in_19 & in_20 & in_21 & in_22 & in_23 & in_24 & in_25 & in_26 & in_27 & in_28 & in_29 & in_30 & in_31 & in_32 & in_33 & in_34 & in_35 & in_36 & in_37 & in_38;
        ff_1 <= in_0 & in_1 & in_2 & in_3 & in_4 & in_5 & in_6 & in_7 & in_8 & in_9 & in_10 & in_11 & in_12 & in_13 & in_14 & in_15 & in_16 & in_17 & in_18 & in_19 & in_20 & in_21 & in_22 & in_23 & in_24 & in_25 & in_26 & in_27 & in_28 & in_29 & in_30 & in_31 & in_32 & in_33 & in_34 & in_35 & in_36 & in_37 & in_38;
        ff_2 <= in_0 & in_1 & in_2 & in_3 & in_4 & in_5 & in_6 & in_7 & in_8 & in_9 & in_10 & in_11 & in_12 & in_13 & in_14 & in_15 & in_16 & in_17 & in_18 & in_19 & in_20 & in_21 & in_22 & in_23 & in_24 & in_25 & in_26 & in_27 & in_28 & in_29 & in_30 & in_31 & in_32 & in_33 & in_34 & in_35 & in_36 & in_37 & in_38;
        ff_3 <= in_0 & in_1 & in_2 & in_3 & in_4 & in_5 & in_6 & in_7 & in_8 & in_9 & in_10 & in_11 & in_12 & in_13 & in_14 & in_15 & in_16 & in_17 & in_18 & in_19 & in_20 & in_21 & in_22 & in_23 & in_24 & in_25 & in_26 & in_27 & in_28 & in_29 & in_30 & in_31 & in_32 & in_33 & in_34 & in_35 & in_36 & in_37 & in_38;
    end
endmodule

module my_FB2(
        input wire in_0,
        input wire in_1,
        input wire in_2,
        input wire in_3,
        input wire in_4,
        input wire in_5,
        input wire in_6,
        input wire in_7,
        input wire in_8,
        input wire in_9,
        input wire in_10,
        input wire in_11,
        input wire in_12,
        input wire in_13,
        input wire in_14,
        input wire in_15,
        input wire in_16,
        input wire in_17,
        input wire in_18,
        input wire in_19,
        input wire in_20,
        input wire in_21,
        input wire in_22,
        input wire in_23,
        input wire in_24,
        input wire in_25,
        input wire in_26,
        input wire in_27,
        input wire in_28,
        input wire in_29,
        input wire in_30,
        input wire in_31,
        input wire in_32,
        input wire in_33,
        input wire in_34,
        input wire in_35,
        input wire in_36,
        input wire in_37,
        input wire in_38,
        output wire out_0,
        output wire out_1,
        output wire out_2,
        output wire out_3,
        input wire clk);



    (* LOC="FB2", keep="true", DONT_TOUCH="true" *) reg ff_0 = 1'b0;
    assign out_0 = ff_0;

    (* LOC="FB2", keep="true", DONT_TOUCH="true" *) reg ff_1 = 1'b1;
    assign out_1 = ff_1;

    (* LOC="FB2", keep="true", DONT_TOUCH="true" *) reg ff_2 = 1'b1;
    assign out_2 = ff_2;

    (* LOC="FB2", keep="true", DONT_TOUCH="true" *) reg ff_3 = 1'b1;
    assign out_3 = ff_3;


    always @(posedge clk) begin
        ff_0 <= in_0 & in_1 & in_2 & in_3 & in_4 & in_5 & in_6 & in_7 & in_8 & in_9 & in_10 & in_11 & in_12 & in_13 & in_14 & in_15 & in_16 & in_17 & in_18 & in_19 & in_20 & in_21 & in_22 & in_23 & in_24 & in_25 & in_26 & in_27 & in_28 & in_29 & in_30 & in_31 & in_32 & in_33 & in_34 & in_35 & in_36 & in_37 & in_38;
        ff_1 <= in_0 & in_1 & in_2 & in_3 & in_4 & in_5 & in_6 & in_7 & in_8 & in_9 & in_10 & in_11 & in_12 & in_13 & in_14 & in_15 & in_16 & in_17 & in_18 & in_19 & in_20 & in_21 & in_22 & in_23 & in_24 & in_25 & in_26 & in_27 & in_28 & in_29 & in_30 & in_31 & in_32 & in_33 & in_34 & in_35 & in_36 & in_37 & in_38;
        ff_2 <= in_0 & in_1 & in_2 & in_3 & in_4 & in_5 & in_6 & in_7 & in_8 & in_9 & in_10 & in_11 & in_12 & in_13 & in_14 & in_15 & in_16 & in_17 & in_18 & in_19 & in_20 & in_21 & in_22 & in_23 & in_24 & in_25 & in_26 & in_27 & in_28 & in_29 & in_30 & in_31 & in_32 & in_33 & in_34 & in_35 & in_36 & in_37 & in_38;
        ff_3 <= in_0 & in_1 & in_2 & in_3 & in_4 & in_5 & in_6 & in_7 & in_8 & in_9 & in_10 & in_11 & in_12 & in_13 & in_14 & in_15 & in_16 & in_17 & in_18 & in_19 & in_20 & in_21 & in_22 & in_23 & in_24 & in_25 & in_26 & in_27 & in_28 & in_29 & in_30 & in_31 & in_32 & in_33 & in_34 & in_35 & in_36 & in_37 & in_38;
    end
endmodule

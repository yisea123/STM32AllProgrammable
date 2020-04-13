`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    08:34:36 04/13/2020 
// Design Name: 
// Module Name:    echo 
// Project Name: 
// Target Devices: 
// Tool versions: 
// Description: 
//
// Dependencies: 
//
// Revision: 
// Revision 0.01 - File Created
// Additional Comments: 
//
//////////////////////////////////////////////////////////////////////////////////

module echo(
    input SCLK,
    input MOSI,
    output MISO,
    input nCS,
    input Clk,
	 
	 output [1:0] Led,
	 output [2:0] Dbg
    );

wire [15:0] rxd;
wire [15:0] txd;
wire [7:0]  addr;
wire        sel;
wire        txe;
wire        rxe;

SPIGate gate(
	.SCLK(SCLK),
	.MOSI(MOSI),
	.MISO(MISO),
	.nCS(nCS),
	.RXD(rxd),
	.TXD(txd),
	.ADDR(addr),
	.SEL(sel),
	.TXE(txe),
	.RXE(rxe),
	.CLK(Clk)
);

assign Dbg = {rxe, txe, sel};

wire [15:0] p0data;
assign Led = ~p0data[1:0];

IOPort port0 (
	.ADDRESS(8'h0),
	.DI(16'hdead),
	.DO(p0data),
	.RXD(rxd),
	.TXD(txd),
	.ADDR(addr),
	.TXE(txe),
	.RXE(rxe),
	.CLK(Clk)
);

wire [15:0] p1data;

IOPort port1 (
	.ADDRESS(8'h1),
	.DI(p1data),
	.DO(p1data),
	.RXD(rxd),
	.TXD(txd),
	.ADDR(addr),
	.TXE(txe),
	.RXE(rxe),
	.CLK(Clk)
);

endmodule
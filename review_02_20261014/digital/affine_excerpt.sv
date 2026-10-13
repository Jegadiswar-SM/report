// Derived excerpt from digital/rtl/pulsar_affine.sv; full source is authoritative.
// Config must be stable for an accepted input. Rounding ties toward +infinity.
module pulsar_affine(
 input logic clk, reset_n, in_valid, bypass,
 input logic [7:0] in_code,
 input logic signed [15:0] offset_q8,
 input logic [15:0] gain_q12,
 output logic out_valid, output logic [7:0] out_code);
 logic signed [17:0] shifted;
 always_comb begin
   shifted=$signed({2'b0,in_code,8'b0})+$signed(offset_q8);
   product=shifted*$signed({1'b0,gain_q12});
   rounded=(product+35'sd524288)>>>20;
 always_ff @(posedge clk or negedge reset_n) begin
   if(!reset_n) begin out_valid<=0; out_code<=0; end
   else begin
     out_valid<=in_valid;
     if(in_valid) begin
       if(bypass) out_code<=in_code;
       else if(rounded<0) out_code<=0;
       else if(rounded>255) out_code<=255;
       else out_code<=rounded[7:0];
     end

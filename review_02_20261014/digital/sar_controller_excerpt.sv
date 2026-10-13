// Derived excerpt from digital/rtl/pulsar_sar_sync.sv; full source is authoritative.
// SETTLE_CYCLES >=1 plus comparator acceptance consumes >=2 edges per stage.
module pulsar_sar_sync #(parameter integer SETTLE_CYCLES=1, TIMEOUT_CYCLES=8)(
 input logic ctrl_clk, reset_n, start, clear_errors,
 input logic cmp_valid, input logic [2:0] cmp_therm,
 output logic busy, cmp_req, sample_track, output logic [2:0] stage,
 output logic code_valid, timeout_error, thermometer_error, overrun_error,
 output logic [8:0] cdac_reverse);
 import pulsar_math_pkg::*;
     // decision, so enumerate the only two permitted four-state patterns.
     case(cmp_therm)
       3'b000: begin digit=0; legal=1; end
     endcase
   end else case(cmp_therm)
     3'b000: begin digit=0; legal=1; end
     state<=IDLE; count<=0; stage<=0; dac_raw<=0; code<=0; code_valid<=0;
     cdac_reverse<=0;
     timeout_error<=0; thermometer_error<=0; overrun_error<=0;
     case(state)
       IDLE: if(start) begin state<=SETTLE; count<=0; stage<=0; dac_raw<=0; cdac_reverse<=0; end
       SETTLE: if(count+1>=SETTLE_CYCLES) begin state<=COMPARE; count<=0; end else count<=count+1;
       COMPARE: if(cmp_valid) begin
         if(!legal) begin thermometer_error<=1; state<=IDLE; end
           if(stage<4) begin
             if(digit[1]) cdac_reverse[2*stage]<=1'b1;
             if(digit[0]) cdac_reverse[2*stage+1]<=1'b1;
           end else if(digit[0]) cdac_reverse[8]<=1'b1;
           if(stage==4) begin code<=decode_raw(next_raw); code_valid<=1; state<=IDLE; end

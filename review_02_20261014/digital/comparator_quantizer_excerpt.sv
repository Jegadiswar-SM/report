// Derived excerpt from digital/rtl/pulsar_cmp_quantize.sv; full source is authoritative.
// latch outputs are invalid and must never be accepted as a SAR decision.
module pulsar_cmp_quantize(
  input  logic cmp0p, cmp0n, cmp1p, cmp1n, cmp2p, cmp2n,
  output logic [2:0] therm,
  output logic       pair_valid
);
  always_comb begin
    therm = 3'bxxx;
    pair_valid = 1'b0;
    case ({cmp2p,cmp2n,cmp1p,cmp1n,cmp0p,cmp0n})
      6'b01_01_01: begin therm=3'b111; pair_valid=1'b1; end
      6'b10_01_01: begin therm=3'b011; pair_valid=1'b1; end
      6'b10_10_01: begin therm=3'b001; pair_valid=1'b1; end
      6'b10_10_10: begin therm=3'b000; pair_valid=1'b1; end
      default: begin therm=3'bxxx; pair_valid=1'b0; end
    endcase

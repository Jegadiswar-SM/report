// Derived excerpt from digital/rtl/pulsar_cdac_ctrl.sv; full source is authoritative.
// Control adapter for oa/.../cdac_diff_v6.
// reverse[k]=0 selects the nominal complementary baseline (positive array
// to VREFP, negative array to VREFN); reverse[k]=1 swaps both sides.
// During acquisition both reference TGs are off and the sample TG is on.
module pulsar_cdac_ctrl (
    input  logic       sample_track,
    input  logic [8:0] reverse,
    output logic       sample,
    output logic       sample_b,
    output logic [8:0] nsel_b,
    output logic [8:0] psel_b,
    output logic [8:0] nsel_bn,
    output logic [8:0] psel_bn
);
            if (sample_track) begin
                nsel_b[k]  = 1'b0;
                psel_b[k]  = 1'b1;
                nsel_bn[k] = 1'b0;
                psel_bn[k] = 1'b1;
            end else begin
                // reference assignment on its negative-side branches.
                nsel_b[k]  = !reverse[k];
                psel_b[k]  = reverse[k];
                nsel_bn[k] = reverse[k];
                psel_bn[k] = !reverse[k];
            end

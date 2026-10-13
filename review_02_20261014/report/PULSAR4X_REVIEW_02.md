# PULSAR-4X: Four-Channel Time-Interleaved SAR ADC in SCL180 CMOS

**Review 02 — Design and verification progress**  
**Review date:** 14 October 2026  
**Project snapshot:** evidence saved through 13 October 2026  
**Repository:** `PULSAR4X_SCL180_FULLBUILD`  
**Status:** transistor-level mixed-signal feedback demonstrated; accurate ADC and physical signoff remain open.

> **Review claim in one sentence:** a real SCL180 sampler/CDAC/comparator hierarchy is connected to the SAR RTL in Xcelium AMS/Spectre, and five physical comparator decisions drive registered codes; the transfer function is not yet correct, as the zero differential case produces 172 instead of the golden 128.

## 1. Problem statement

An ADC must acquire an analog input, resolve it within a bounded time, and produce stable codes with adequate linearity, noise, power and area. At high sample rates the sampler, DAC settling, comparator regeneration, reference network and controller timing interact. Time interleaving raises aggregate throughput but adds channel mismatch and clock-skew errors. Schematic simulation is necessary evidence, but it does not establish extracted-layout or silicon performance.

## 2. Project objective

The target is an 8-bit, four-channel time-interleaved SAR ADC, nominally 100 MS/s per channel and 400 MS/s aggregate. The corresponding aggregate output stream is 3.2 Gb/s before framing. This remains a target specification. The current feedback bring-up is approximately 10 MS/s/channel with five decision phases separated by about 20 ns; it is not a rate qualification.

## 3. Proposed architecture

The intended top level uses four phase-staggered SAR channels, a differential sampler and capacitive DAC per channel, a multithreshold regenerative comparator bank, nonbinary/redundant SAR decisions, digital correction, and an interleaver/calibration/readout system. The active analog OA hierarchy and one channel's feedback controller exist. Four-channel clocking, interleaver and calibration are not integrated. The present comparator thresholds are fixed external sources (1.02, 1.04 and 1.06 V), not the stage-dependent residue thresholds needed by the golden grouped-SAR algorithm.

## 4. Technology and tools

The project uses the SCL180 0.18 µm CMOS PDK and Cadence OA libraries. Saved runs identify Spectre 21.1.0.546 ISR13, Xcelium 22.09-s003 and Genus 21.14-s082_1. Python/matplotlib is used only to render plots from saved numerical simulator results. The active project OA library is `PULSAR4X_FB_20261010`; its `cds.lib` points to the installed SCL180 primitive library. The historical `TI_SAR_8B4X` project is not the source of the evidence in this review.

## 5. Analog circuit implementation

The real OA hierarchy is `adc_analog_channel_bank3_v1`, with child instances for `sampler_core_v2`, `cdac_diff_v6` and `doubletail_bank3`. The executed AMS netlist inventory reports 230 `bsim3v3` instances. The OA source cells are present in `oa/PULSAR4X_FB_20261010/`; the saved top hierarchy is an actual schematic database. No actual Virtuoso GUI screenshot could be captured from this shell because `DISPLAY=localhost:20.0` is inaccessible (`xdpyinfo` cannot open it). The plots in `waveforms/` are therefore data exports, not screenshots of Virtuoso/ViVA.

The sampler waveform comes from an OA-generated transistor-level Spectre run at TT/27 °C, 1.8 V, 1 Ω source and +0.6 V differential. It records a +23.890 mV turn-off step and +5.097 LSB held error (4.6875 mV/LSB normalization). This fails the current sampler screening.

![OA sampler Spectre waveform export](../waveforms/01_sampler_oa_spectre.png)

The plotted standalone `cdac_diff_v4` experiment is explicitly separate from the integrated `cdac_diff_v6`: its 1-unit branch transfer is −27.94% after 18 ns, so its weight screen fails. It must not be read as a measurement of integrated v6 performance.

![Standalone CDAC v4 switched response](../waveforms/02_cdac_v4_standalone_spectre.png)

![Standalone CDAC v4 weight screen](../waveforms/03_cdac_v4_weight_error.png)

`doubletail_bank3` is a three-latch comparator bank. A standalone transistor-level comparator test produces the shown regeneration waveforms. In the integrated transactions, physical comparator outputs feed the electrical-to-logic bridge and thermometer quantizer. Fixed thresholds and bench-timed validity limit the interpretation. There is no on-chip qualified reference/bias generator in this review evidence.

![Comparator bank Spectre regeneration waveform](../waveforms/04_comparator_bank3_spectre.png)

## 6. Digital architecture

The implemented SystemVerilog includes `pulsar_sar_sync`, `pulsar_cdac_ctrl`, `pulsar_cmp_quantize` and `pulsar_affine`. The SAR state machine accepts thermometer decisions and emits accumulated nine-branch CDAC controls; the physical CDAC receives those commands through an electrical bridge. Comparator latch outputs return through the AMS electrical-to-logic interface. The affine correction and output-valid register follow the raw SAR result. Code excerpts in `digital/` are source-derived excerpts; the full RTL remains authoritative in `digital/rtl/`.

The Xcelium digital-only wrapper regression passed 256 ideal code-center transactions and correction/saturation checks. That proves the tested RTL behavior under its digital assumptions. It does not verify analog accuracy.

## 7. Mixed-signal integration

The saved three AMS/Spectre transaction runs connect the actual OA analog channel to actual SAR RTL. The physical comparator output decisions are captured at five stages and feed the controller; the controller's switch commands control the transistor-level CDAC. Logged output-valid is asserted. The comparison figure plots the actual saved analog strobe values and thermometer decisions; it is not a reconstructed continuous waveform. Full raw AMS logs, analog control nets and PSF/PSFXL data remain in the source result directories.

![Five-decision mixed-signal capture summary](../waveforms/05_ams_feedback_three_cases.png)

![Existing complete positive-input transaction plot](../waveforms/07_ams_conversion_timing_existing.png)

This second plot is preserved from the previous capture package and shows the saved stage timing with DAC+ samples, comparator thermometer states and CDAC command word. DAC+ is sampled at five comparator strobes; connecting line segments are visual guides, not a continuous waveform. It is a plot made from actual AMS capture data, not a ViVA or SimVision screenshot.

The present comparator `cmp_valid` event is bench-timed 2 ns after physical resolution, while comparator thresholds are fixed external sources. Accordingly this is a genuine closed-loop mixed-signal transaction demonstration, but not a qualified implementation of the intended stage-dependent decision mapping.

## 8. AMS binding validation

The earlier binding failure was caused by passing the `.scs` deck only as analog control, which compiled an empty Verilog-AMS electrical stub and left the Spectre device inventory empty. Supplying the `.scs` as an Xcelium design source generated the subcircuit port map; applying the OA netlist's `scale=1e-6` resolved device geometry interpretation. The minimal real 1 kΩ resistor test measured 1 V and 1.000 mA. The bound ADC hierarchy's executed inventory reports 230 SCL180 BSIM devices and a 60-port binding map. This proves binding, not conversion accuracy.

## 9. First closed-loop conversion experiments

Three completed capture cases each have five physical comparator decisions:

| Differential input | Physical decisions | Captured corrected code | Golden code | Interpretation |
|---:|---|---:|---:|---|
| −0.6 V | 0, 0, 0, 0, 0 | 0 | 0 | Endpoint code matches; sequence differs. |
| 0 V | 3, 0, 0, 0, 0 | 172 | 128 | **Fail:** central transfer point is wrong. |
| +0.6 V | 3, 3, 2, 1, 1 | 255 | 255 | Saturated endpoint matches; decision sequence differs. |

The positive and negative endpoints do not validate intermediate transfer. In particular, the zero-input discrepancy is consistent with the unresolved comparator threshold-to-residue mapping, but the root cause has not been proven by a controlled isolation experiment. The capture itself is an actual integrated simulation result; do not call it an accurate ADC code capture.

## 10. Functional results

There is no demonstrated monotonic transfer curve, no complete expected-code sweep, and no ADC static or dynamic characterization. The key evidence is three actual closed-loop transactions, with one explicit code mismatch and different physical/golden decision sequences. No ADC ENOB, SNDR, SFDR, SNR, THD, DNL or INL is measured. See `results/VERIFIED_RESULTS.csv` for values and provenance.

## 11. Digital synthesis

A prior saved Genus replay reports 2,572 mapped cells and 43,699.970 µm² for the digital wrapper. A later detailed report saved on 13 October reports 2,595 cells and 44,393.000 µm². Both are synthesized digital-wrapper results, not full ADC area and not placed-and-routed chip area. The difference is disclosed rather than silently choosing one.

![Genus saved area and timing summary](../digital/10_genus_area_timing_summary.png)

## 12. Timing analysis

The later Genus path report is the current detailed timing evidence. The critical path is `u_sar_code_reg[4]/CP → u_correction_out_code_reg[6]/D`, in group `ctrl_clk`, rising launch to falling capture, with a 650 ps clock edge. Arrival is 4,116 ps; required is 447 ps after 153 ps setup and 50 ps uncertainty; slack is −3,669 ps. The report lists 34 timing arcs and maximum fanout 9. A second controller path `u_sar_stage_reg[1]/CP → u_sar_dac_raw_reg[8]/D` arrives in 2,384 ps against 410 ps required, slack −1,974 ps. Both fail. The 650 ps constraint was not relaxed.

![Genus critical path timing plot](../digital/07_genus_critical_path.png) Genus synthesis timing is not placed-and-routed timing closure.

The older replay's 4,042 ps arrival, 464 ps required and −3,578 ps slack are a distinct earlier result. The current detailed report values should be used for the critical-path discussion.

## 13. Analog limitations

- **Sampler:** OA Spectre held error +5.097 LSB in the cited 1 Ω test. Other source-resistance results show acquisition and switch errors can cancel; that cancellation is not an acceptable fix.
- **CDAC:** standalone v4 branch transfer screening fails, reaching −27.94% at the 1-unit branch. Integrated v6 accuracy has not been established by that separate test.
- **Comparator mapping:** fixed external thresholds do not implement stage-dependent nonbinary residue thresholds.
- **Current equivalence:** standalone-versus-AMS current differs by 34.3% at 3.2 ns and 36.8% at 3.6 ns in saved point comparisons. DAC/comparator voltage checkpoints agree closely, but current equivalence remains FAIL and root cause is unresolved. Sparse integration is diagnostic only.
- **Reference and bias:** no qualified on-chip generator/distribution evidence is available in this review package.

## 14. Verification methodology

Evidence comprises OA schematic databases and generated transistor-level Spectre netlists, three Xcelium AMS/Spectre closed-loop runs, the digital Xcelium regression log, Genus reports and the Python software test log. The Python metrics suite reports 44 passing tests; these are software tests, not hardware verification. Figures in this package are generated from saved simulator data and explicitly labeled by circuit fidelity. No new circuit simulation was run to prepare this review.

## 15. Current overall status

| Area | Review status | Evidence boundary |
|---|---|---|
| OA analog sampler/CDAC/comparator hierarchy | Implemented; simulations exist | Actual schematic database and transistor-level runs; accuracy issues remain. |
| AMS binding | Verified | Real bound device netlist; 230 BSIM devices. |
| SAR physical feedback loop | Demonstrated, limited | Five decisions and output-valid in three runs; stage threshold map unqualified. |
| ADC transfer accuracy | Fail / not established | Zero differential 172 vs 128; no complete sweep. |
| Digital RTL regression | Pass under test assumptions | 256 code-center transactions and correction tests; not analog proof. |
| Digital timing | Fail | −3.669 ns and −1.974 ns slack in saved Genus path report. |
| Sampler/CDAC accuracy | Fail screening | +5.097 LSB sampler; separate v4 CDAC small-weight error. |
| Full performance metrics | Not measured | No qualified capture basis for ENOB/SNDR/DNL/INL. |
| Four-channel, layout, DRC/LVS/PEX, GDSII | Missing | No full-chip implementation/signoff artifacts. |

## 16. Work after Review 02

1. Correctly derive and verify stage-dependent comparator thresholds against the nonbinary residue algorithm.
2. Repair sampler and CDAC errors with same-condition Spectre tests.
3. Close the 650 ps digital paths without hiding or relaxing the requirement.
4. Expand the integrated transfer capture, then run static/dynamic metrics only when its quality supports them.
5. Integrate and calibrate four channels, then implement analog and digital layout.
6. Run foundry DRC/LVS/PEX, extracted simulation and only then evaluate GDSII handoff readiness.

## 17. Conclusion

The project has advanced from separate circuit and RTL work to a genuine transistor-level analog and RTL feedback experiment. AMS binding, physical comparator decisions, CDAC updates and registered output codes are present in the saved runs. The resulting codes are not yet a correct ADC transfer: zero differential gives 172 instead of 128, thresholds are fixed, and analog accuracy and controller timing fail. No four-channel physical ADC or silicon result is available. This is meaningful integration progress, with clear and testable next work, not a completed ADC.

## Appendix — Evidence paths and reproducibility

- OA library: `oa/PULSAR4X_FB_20261010/`.
- Active project library declarations: `cds.lib`.
- AMS first capture summary: `results/raw/first_integrated_adc_capture/case_summary.csv`.
- Per-case AMS runs: `results/raw/first_integrated_adc_capture/cases/` and positive case `results/physical/ams_adc_direction_20261013/`.
- AMS binding and current comparison: `results/physical/ams_oa_source_flow_20261013/`.
- Sampler: `results/physical/sampler_core_v2_OA_R1ohm/`.
- Standalone CDAC v4: `results/physical/cdac_diff_v4_spectre/`.
- Comparator bank: `results/physical/comparator_bank3_spectre/`.
- Genus: `results/digital/channel_wrapper_20261013/`.
- RTL regression: `results/digital/channel_wrapper_20261013/xrun_cdac_ctrl.log`.
- Software tests: `results/verification/replay_20261013/pytest.log`.
- Data-export regeneration: `python3 presentation/review_02_20261014/scripts/generate_review_assets.py` (uses installed NumPy/matplotlib; runs no simulator).
- For GUI steps and the current access limitation see `README.md` and `scripts/open_review_guis.sh`.

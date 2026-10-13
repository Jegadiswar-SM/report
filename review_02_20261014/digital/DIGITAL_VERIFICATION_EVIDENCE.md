# Digital verification and synthesis evidence excerpts

These are exact summaries from saved run artifacts, with the original log paths retained. They establish RTL test behavior and synthesis only; they do not establish analog conversion accuracy or physical timing closure.

## Xcelium RTL regression

**Source:** `results/digital/channel_wrapper_20261013/xrun_cdac_ctrl.log`  
**Tool:** Xcelium 22.09-s003  
**Log evidence:** `PASS channel digital wrapper: 256 bypass codes and corrected saturation`; simulation completes via `$finish` at 3,100,600 ps. The testbench is `digital/tb/tb_channel_digital.sv`.

**Scope:** ideal code-center and correction/saturation digital transactions. This is not a physical comparator or ADC sweep.

## Python verification suite

**Source:** `results/verification/replay_20261013/pytest.log`  
**Result:** `44 passed in 2.60s`. This is software/model/analysis verification, not hardware verification.

## Genus summary, two saved reports

**Later detailed reports:** `results/digital/channel_wrapper_20261013/area.rpt` and `timing.rpt`, Genus 21.14-s082_1.  
- 2,595 mapped cells; 44,393.000 µm².
- Critical path: `u_sar_code_reg[4]/CP` → `u_correction_out_code_reg[6]/D`.
- Arrival 4,116 ps; required 447 ps; slack −3,669 ps; 650 ps clock period; 153 ps setup; 50 ps uncertainty; 34 reported timing arcs; max fanout 9.
- SAR accumulation path: `u_sar_stage_reg[1]/CP` → `u_sar_dac_raw_reg[8]/D`; arrival 2,384 ps; required 410 ps; slack −1,974 ps.

**Earlier saved replay:** `results/digital/channel_wrapper_20261013/replay.json` reports 2,572 mapped cells, 43,699.970 µm², 4,042 ps arrival, 464 ps required and −3,578 ps slack. The revision difference is disclosed.

## Actual analog binding evidence

**Source:** `results/physical/ams_oa_source_flow_20261013/xrun_verified.log`. The generated Spectre inventory contains `bsim3v3 230`; the run ends `spectre completes with 0 errors, 5 warnings, and 4 notices.` This is analog binding and fixed-control simulation evidence, not ADC accuracy.

## Full physical-feedback capture

**Source:** `results/physical/ams_adc_direction_20261013/xrun_feedback.log` (also summarized in `results/raw/first_integrated_adc_capture/capture.json`). The executed Spectre inventory contains 230 BSIM devices. Five `AMS_ANALOG_COMPARATOR_WAVE` events have actual transistor comparator outputs and corresponding analog DAC+ strobe values. The final marker is `actual comparator outputs drove five SAR decisions; cdac=19f raw=255 corrected=255 valid=1`. The case uses +0.6 V differential input and fixed comparator thresholds; its decision sequence differs from the golden model.

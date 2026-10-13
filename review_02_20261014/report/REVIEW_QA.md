# Review 02 — likely questions and evidence-grounded answers

**Why SAR?** A SAR converts through iterative comparisons and a capacitive DAC, which fits a moderate-resolution, power-conscious architecture. Its practical limits are DAC settling, comparator noise/offset and controller timing.

**Why four-channel interleaving?** Four channels at 100 MS/s would nominally combine to 400 MS/s. Interleaving introduces timing, gain, offset and bandwidth mismatch; those channels and calibration are not yet implemented.

**What is nonbinary redundancy?** Decision weights include overlap/redundancy so neighboring decisions can tolerate some residue error and be corrected digitally. Here the intended weights are `[128,64,48,24,16,8,4,2,1]`. The physical fixed-threshold comparator mapping has not yet been made stage-dependent to match that algorithm.

**What does 2-bit/cycle mean?** A multithreshold bank can produce several ordered regions in one evaluation, potentially resolving more than one binary bit per phase. The current bring-up logs five decision phases. Do not infer a qualified 2-bit/cycle ADC from those runs.

**Why SCL180 is challenging?** Switch charge injection, capacitor ratios, device parasitics, regeneration, reference settling and limited timing margin all matter at 8-bit accuracy. The observed sampler and CDAC errors show this directly.

**Which transistor-level blocks exist?** OA schematic cells include sampler_core_v2, cdac_diff_v6, doubletail_bank3 and adc_analog_channel_bank3_v1. The AMS execution inventory reports 230 SCL180 BSIM devices. No on-chip reference/bias subsystem is demonstrated.

**What does the comparator bank do?** Three double-tail regenerative latch stages compare the analog DAC node against three threshold pins and produce a thermometer-like decision. The integrated experiment uses fixed external threshold sources.

**What do five closed-loop decisions demonstrate?** Physical analog comparator outputs travel through the AMS logic interface into SAR RTL; SAR commands return through an electrical bridge to switch the real CDAC. The controller registers a final code/valid. It proves feedback connectivity in the tested bench, not correct ADC transfer or target rate.

**Why does zero input give 172 instead of 128?** The captured physical decision sequence is `[3,0,0,0,0]`, while the golden sequence is `[2,0,2,2,0]`. Thresholds are fixed at 1.02/1.04/1.06 V rather than following stage residue. This is the leading mapping issue; a stage-by-stage same-state comparison is needed before assigning a definitive root cause.

**Why are matching endpoints insufficient?** Saturated negative and positive endpoints can match despite wrong intermediate thresholds. The center mismatch already disproves a correct transfer function.

**What are sampler/CDAC limitations?** Sampler held error is +5.097 LSB in the cited OA test. Separate standalone CDAC v4 screening shows −27.94% error at the 1-unit branch. The latter is not a measurement of integrated v6.

**How is CMOS connected to SystemVerilog?** The `.scs` design is included as an Xcelium design source; a generated AMS port map binds the OA subcircuit. Electrical/digital bridges drive 0/1.8 V gate controls and convey comparator latch outputs to the RTL. The resolved process includes `scale=1e-6` from the OA netlist.

**Why did binding initially fail?** The original invocation supplied the `.scs` only as analog control, so an empty electrical stub was compiled and no transistor subcircuit entered the Spectre device inventory. Passing the `.scs` as a design source generated the binding map; correct netlist scale fixed device geometry interpretation.

**What do 230 BSIM devices mean?** They are transistor device instances in the executed analog hierarchy, as inventoried by Spectre. This is not the total chip transistor count and says nothing by itself about accuracy.

**What did Genus achieve?** It synthesized the digital wrapper. Earlier replay: 2,572 cells / 43,699.970 µm². Later detailed report: 2,595 / 44,393 µm². These are digital synthesis results, not full-chip or routed area.

**Why does timing fail?** The saved 650 ps control-clock report gives 4.116 ns arrival against 0.447 ns required (−3.669 ns). A SAR accumulation path is 2.384 ns against 0.410 ns (−1.974 ns). Affine correction is on the first reported cone; timing has not been repaired.

**Schematic versus post-layout?** Schematic simulations use device models without extracted interconnect parasitics. Post-layout verification requires real layout, DRC/LVS and extraction, then simulation on extracted data. Those ADC physical gates are missing.

**Have DRC/LVS been completed?** No full ADC DRC/LVS/PEX. Existing qualification-cell evidence is not chip signoff.

**What remains before GDSII?** Four-channel integration, qualified references/clocks/pads, physical layout, foundry DRC/LVS, extraction, post-layout performance and validated stream-out. No ADC GDSII is claimed.

**What can be claimed about ENOB?** Nothing numerical. No qualified integrated ADC capture supports ENOB/SNDR/SFDR/DNL/INL. The sampler or component sine fits cannot be substituted.

# Review 02 slide outline (15 slides)

Use the matching PNG in `waveforms/`, `digital/`, and `diagrams/`; large readable titles, one claim per slide, 16:9. The HTML deck `slides/review_slides.html` is an offline editable-by-text presentation source. All plotted figures are simulator-data exports or reconstructed diagrams, never GUI screenshots.

1. **PULSAR-4X SCL180 CMOS ADC — Review 02.** State this is progress through 13 Oct 2026. Use OA hierarchy derived diagram (`diagrams/08_oa_hierarchy_derived.png`).
2. **Target versus present demonstration.** 8 bit, 4×100 MS/s target / 400 MS/s aggregate versus ~10 MS/s functional bring-up. Label target versus demonstrated.
3. **Proposed architecture.** Use `diagrams/09_feedback_dataflow_derived.png`; call out one-channel feedback implementation and missing interleaver.
4. **Technology and toolchain.** SCL180 0.18 µm; Virtuoso OA / Spectre / Xcelium AMS / Genus / Python. State live GUI screenshots unavailable in this environment.
5. **OA analog hierarchy.** Use derived hierarchy diagram, accompanied by actual library/cell paths and 230-device inventory. It is a hierarchy diagram, not a schematic screenshot.
6. **Sampler behavior.** `waveforms/01_sampler_oa_spectre.png`; +5.097 LSB held error. Label OA transistor-level Spectre.
7. **CDAC and comparator circuit evidence.** Show `waveforms/02_cdac_v4_standalone_spectre.png` and `waveforms/04_comparator_bank3_spectre.png`; state CDAC is standalone v4 screen while integration uses v6.
8. **SAR digital system.** Show actual RTL excerpt plus synthesized wrapper note; 256 ideal code-center tests, digital assumptions only.
9. **AMS binding and feedback path.** `diagrams/09_feedback_dataflow_derived.png`; 230 BSIM instances, real comparator-to-SAR and SAR-to-CDAC path.
10. **Five-decision transactions.** `waveforms/05_ams_feedback_three_cases.png`; fixed external thresholds, 20 ns spacing, approximate 10 MS/s/channel.
11. **Measured codes: matches and failure.** Highlight 0 V→172 vs golden 128. Endpoints match only at saturation; decision sequences differ.
12. **Genus synthesis and critical path.** `digital/07_genus_critical_path.png`; report 2,595/44,393 latest and older replay 2,572/43,699.970; −3.669 ns and −1.974 ns.
13. **What is verified and what remains.** AMS binding/feedback demonstrated; transfer accuracy, timing, sampler/CDAC and current equivalence fail; no ADC dynamic metrics.
14. **Next engineering milestones.** Stage thresholds, analog error, 650 ps timing, full transfer, four channels, layout/signoff.
15. **Conclusion / questions.** “Real feedback loop demonstrated; accurate ADC not yet demonstrated.”

## Figure sources and fidelity labels

- Sampler: `results/physical/sampler_core_v2_OA_R1ohm/waveforms.npz`, OA SCL180 transistor Spectre.
- CDAC: `results/physical/cdac_diff_v4_spectre/bit0/waveforms.npz`, standalone v4 transistor Spectre; not integrated v6.
- Comparator: `results/physical/comparator_bank3_spectre/case2_vin910mV/waveforms.npz`, standalone transistor Spectre.
- Feedback: three saved Xcelium/Spectre logs and `case_summary.csv`; actual integration strobes, not interpolated analog waveforms.
- Genus: `results/digital/channel_wrapper_20261013/timing.rpt`.

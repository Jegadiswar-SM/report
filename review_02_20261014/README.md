# PULSAR-4X Review 02 package

Evidence snapshot through 13 October 2026; review date 14 October 2026. Begin with `report/PULSAR4X_REVIEW_02.md`, then `results/COMPLETED_VS_PENDING.md`. The detailed numerical table is `results/VERIFIED_RESULTS.csv`, with source file and run directory on each row.

## Best 8–12 figures to present

1. `diagrams/08_oa_hierarchy_derived.png` — derived hierarchy diagram, not a Virtuoso screenshot.
2. `waveforms/01_sampler_oa_spectre.png` — actual OA sampler Spectre data; shows +5.097 LSB error.
3. `waveforms/02_cdac_v4_standalone_spectre.png` — standalone v4 CDAC screen; do not call it integrated v6.
4. `waveforms/03_cdac_v4_weight_error.png` — measured standalone branch errors.
5. `waveforms/04_comparator_bank3_spectre.png` — actual comparator regeneration vectors.
6. `diagrams/09_feedback_dataflow_derived.png` — feedback integration diagram reconstructed from actual RTL/AMS wrapper.
7. `waveforms/07_ams_conversion_timing_existing.png` — original saved five-decision timing plot with DAC+, thermometer decisions and SAR CDAC command sequence.
8. `waveforms/05_ams_feedback_three_cases.png` — three feedback cases, including 172 vs 128.
9. `waveforms/06_standalone_ams_checkpoints.png` — checkpoint agreement and current mismatch.
10. `digital/10_genus_area_timing_summary.png` — saved area reports and both timing failures.
11. `digital/07_genus_critical_path.png` — actual saved Genus timing path, fail.
12. `digital/sar_controller_excerpt.sv` and `digital/cdac_adapter_excerpt.sv` — genuine source-derived RTL excerpts.

## What was actually opened

No Virtuoso, ViVA, SimVision or Genus GUI was opened in this execution. The shell display `localhost:20.0` is inaccessible (`xdpyinfo` fails); a Virtuoso process exists but was not attached or disturbed. Authentic GUI screenshots are therefore absent. Saved OA databases and simulator results were inspected. The PNG figures are numerical exports or diagrams, with source paths in `evidence/SCREENSHOT_MANIFEST.csv`.

## Live review GUI procedure

Open the offline package with `xdg-open presentation/review_02_20261014/index.html` and the slides with `xdg-open presentation/review_02_20261014/slides/review_slides.html`. Run `bash presentation/review_02_20261014/scripts/open_review_guis.sh` from the project root to check EDA GUI availability. It checks current display and executable availability and reports options. On the authorized desktop where `xdpyinfo` succeeds and Cadence license is available:

1. Open a terminal in the project root.
2. Ensure the project environment and license settings are the same as used for the saved runs; do not print license-server credentials in projected terminals.
3. Run `/home/install/IC618/tools.lnx86/dfII/bin/virtuoso -log presentation/review_02_20261014/evidence/virtuoso_review.log` (or the site-approved Virtuoso version if different).
4. In Library Manager select library `PULSAR4X_FB_20261010`; open `adc_analog_channel_bank3_v1/schematic`, `sampler_core_v2/schematic`, `cdac_diff_v6/schematic`, and `doubletail_bank3/schematic`.
5. For saved raw data, use the Virtuoso Results Browser/ViVA to open `results/physical/sampler_core_v2_OA_R1ohm/` and the per-run PSF data. For Xcelium, inspect the case `xrun_feedback.log` and `spectre_raw` data. A saved SimVision database suitable for the full mixed-signal run was not located; do not claim one exists.
6. Open Genus only if a saved design checkpoint and license are available; the verified text evidence is `results/digital/channel_wrapper_20261013/{area.rpt,timing.rpt,genus.log}`.

Exact saved artifacts remain usable offline. The launcher does not run or overwrite simulations.

## Package map

- `waveforms/` — plots exported from actual saved Spectre/AMS data.
- `analog/` — exported numerical traces.
- `digital/` — Genus plot and source-derived RTL excerpts.
- `diagrams/` — reconstructed architecture diagrams, explicitly not screenshots.
- `results/` — verified numerical CSV and status summary.
- `report/` — technical report and faculty Q&A.
- `slides/` — 15-slide outline and HTML slide source.
- `evidence/SCREENSHOT_MANIFEST.csv` — source/fidelity manifest.
- `evidence/AMS_BINDING_EXCERPT.txt` — exact binding inventory/completion excerpts.
- `digital/DIGITAL_VERIFICATION_EVIDENCE.md` — Xcelium, Python and Genus result scopes.
- `scripts/` — plot regeneration and safe GUI availability launcher.

## Reproduce exported figures

`/tmp/pulsar-venv/bin/python presentation/review_02_20261014/scripts/generate_review_assets.py` (this environment’s matplotlib/numpy virtual environment)

This uses the stored NPZ/CSV/JSON/log data and does not execute Spectre, Xcelium, Genus or Virtuoso. Regenerate the local gallery and HTML deck with `python3 presentation/review_02_20261014/scripts/generate_review_gallery.py`. PDF report: `report/PULSAR4X_REVIEW_02.pdf`. Regenerate from saved Markdown and figures with `/tmp/pulsar-venv/bin/python presentation/review_02_20261014/scripts/export_report_pdf.py` (matplotlib only; runs no simulator).

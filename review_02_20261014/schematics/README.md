# OA schematic availability and screenshot status

The following genuine OpenAccess `schematic` views exist in the active project library (these are native OA databases, not exported artwork):

- `PULSAR4X_FB_20261010/adc_analog_channel_bank3_v1/schematic/sch.oa`
- `PULSAR4X_FB_20261010/sampler_core_v2/schematic/sch.oa`
- `PULSAR4X_FB_20261010/cdac_diff_v6/schematic/sch.oa`
- `PULSAR4X_FB_20261010/doubletail_bank3/schematic/sch.oa`

The library root is `oa/PULSAR4X_FB_20261010/` and the project's `cds.lib` maps this library plus the installed `ts018_scl_prim` library. The top-level OA schematic check and netlist evidence are retained in the engineering results. The executed AMS hierarchy reports 230 BSIM device instances; the independently generated top OA netlist reports 228 components before AMS inventory expansion/counting. These are different reported inventories and are not conflated.

No live Virtuoso screenshot was captured: the available display was inaccessible to this shell. This folder therefore contains no schematic screenshot or fabricated schematic export. The hierarchy illustration in `../diagrams/08_oa_hierarchy_derived.png` is a reconstruction from the generated netlist and is explicitly not a schematic.

On an authorized graphical desktop, use the exact steps in `../README.md` and open the named library/cells in Virtuoso Library Manager.

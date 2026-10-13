# Review status at a glance

| Item | Status | Evidence / qualification |
|---|---|---|
| OA sampler, CDAC, comparator bank and analog top | Implemented; transistor-level runs exist | `oa/PULSAR4X_FB_20261010/`; 230 BSIM in AMS hierarchy. |
| AMS binding | Verified | `.scs` as design source, 60-port binding, 230 BSIM; resistor sanity test 1.000 mA. |
| Analog-to-RTL comparator feedback | Demonstrated in transactions | Five comparator evaluations per case; fixed threshold and bench-valid limitations. |
| RTL-to-analog CDAC control | Demonstrated in transactions | SAR commands control physical CDAC switches. |
| Captured results | 3 transactions | −0.6 V→0 (golden 0); 0 V→172 (golden 128, FAIL); +0.6 V→255 (golden 255). |
| 100 MS/s/channel | NOT MET | Bring-up about 10 MS/s/channel. |
| Sampler accuracy | FAIL | +5.097 LSB held error in cited OA case. |
| CDAC accuracy | FAIL screening | Standalone v4 1-unit weight error −27.94%; integrated v6 not characterized by that run. |
| Digital RTL-only tests | PASS in scope | 256 ideal code-center cases; no analog proof. |
| Genus timing | FAIL | −3.669 ns critical; −1.974 ns SAR accumulation. |
| Full ADC ENOB/SNDR/SFDR/DNL/INL | NOT MEASURED | Do not infer from component plots or three points. |
| Four-channel ADC | MISSING | No full interleaver/channel hierarchy. |
| ADC layout/DRC/LVS/PEX/GDSII | MISSING | No full-chip physical signoff. |
| Full-chip area/power | NOT MEASURED | Digital wrapper synthesis area is not chip area. |

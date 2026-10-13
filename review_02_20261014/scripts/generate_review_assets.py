#!/usr/bin/env python3
"""Create data-derived review plots and results CSV; does not run simulations."""
from pathlib import Path
import csv,json,re
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch,FancyArrowPatch
ROOT=Path(__file__).resolve().parents[3]
PKG=ROOT/"presentation/review_02_20261014"
for x in ["waveforms","analog","digital","diagrams","results","evidence"]: (PKG/x).mkdir(parents=True,exist_ok=True)
plt.rcParams.update({"figure.facecolor":"white","axes.facecolor":"#fbfcfe","axes.edgecolor":"#64748b","axes.labelcolor":"#0f172a","text.color":"#0f172a","xtick.color":"#334155","ytick.color":"#334155","grid.color":"#cbd5e1","font.size":11})
def save(fig,name): fig.savefig(PKG/name,dpi=240,bbox_inches="tight"); plt.close(fig)
def npz(name): return np.load(ROOT/name)

# Real saved Spectre waveform from the OA sampler_core_v2 netlist.
sam=npz("results/physical/sampler_core_v2_OA_R1ohm/waveforms.npz"); t=sam["time"]*1e9
fig,ax=plt.subplots(2,1,figsize=(12,7),sharex=True,gridspec_kw={"height_ratios":[2,1]})
for k,label,c in [("inp","input p","#2563eb"),("inn","input n","#f97316"),("hp","held p","#0f766e"),("hn","held n","#9333ea")]: ax[0].plot(t,sam[k],label=label,color=c,lw=1.5)
ax[0].set_ylabel("Voltage (V)"); ax[0].set_title("OA sampler_core_v2 — Spectre, TT / 27 C, 1 ohm source"); ax[0].legend(ncol=2); ax[0].grid(True,alpha=.5)
for k,c in [("clk","#2563eb"),("clkb","#f97316")]: ax[1].plot(t,sam[k],label=k,color=c,lw=1.2)
ax[1].set_ylabel("Clock (V)"); ax[1].set_xlabel("Time (ns)"); ax[1].set_ylim(-.1,1.9); ax[1].legend(); ax[1].grid(True,alpha=.5)
for a in ax:
 for x in [3.0,3.02,3.12]: a.axvline(x,color="#64748b",ls=":",lw=.8)
ax[0].text(.01,.02,"Turn-off step +23.890 mV / +5.097 LSB; held error +5.097 LSB",transform=ax[0].transAxes,color="#b91c1c",weight="bold")
save(fig,"waveforms/01_sampler_oa_spectre.png")
with (PKG/"analog/sampler_trace.csv").open("w",newline="") as f:
 w=csv.writer(f); w.writerow(["time_s","input_p_V","input_n_V","hold_p_V","hold_n_V","clk_V","clkb_V"]); w.writerows(zip(sam["time"],sam["inp"],sam["inn"],sam["hp"],sam["hn"],sam["clk"],sam["clkb"]))

# Standalone OA cdac_diff_v4 plot. Distinct from integrated cdac_diff_v6.
cd=npz("results/physical/cdac_diff_v4_spectre/bit0/waveforms.npz"); ct=cd["time"]*1e9
fig,ax=plt.subplots(2,1,figsize=(12,7),sharex=True,gridspec_kw={"height_ratios":[2,1]})
ax[0].plot(ct,cd["vcp"]-cd["vcn"],color="#0f766e",lw=1.6); ax[0].set_ylabel("Differential DAC (V)"); ax[0].grid(True,alpha=.5); ax[0].set_title("Standalone OA cdac_diff_v4 — Spectre switched-charge screen, 128-unit branch")
for k,c in [("sample","#2563eb"),("sample_b","#f97316"),("nsel_b0","#9333ea")]: ax[1].plot(ct,cd[k],label=k,color=c,lw=1.2)
ax[1].set_ylabel("Control (V)"); ax[1].set_xlabel("Time (ns)"); ax[1].grid(True,alpha=.5); ax[1].legend(ncol=3)
ax[0].text(.01,.02,"18 ns step 1.03385 V vs 1.04136 V nominal (−0.721%). Standalone v4, not integrated v6.",transform=ax[0].transAxes,fontsize=9)
save(fig,"waveforms/02_cdac_v4_standalone_spectre.png")
with (PKG/"analog/cdac_v4_bit0_trace.csv").open("w",newline="") as f:
 w=csv.writer(f); w.writerow(["time_s","vcp_V","vcn_V","sample_V","sample_b_V","nsel_b0_V"]); w.writerows(zip(cd["time"],cd["vcp"],cd["vcn"],cd["sample"],cd["sample_b"],cd["nsel_b0"]))
wt=list(csv.DictReader((ROOT/"results/physical/cdac_diff_v4_spectre/weight_transfer.csv").open()))
fig,ax=plt.subplots(figsize=(10,5)); bits=[int(x["bit_index"]) for x in wt]; er=[float(x["relative_step_error_percent"]) for x in wt]
ax.bar(bits,er,color=["#0f766e" if abs(v)<=2 else "#dc2626" for v in er]); ax.axhline(0,color="#334155",lw=.8); ax.set_xticks(bits,[str(2**(8-b)) for b in bits]); ax.set_xlabel("Nominal branch weight (units)"); ax.set_ylabel("18 ns transfer error (%)"); ax.grid(axis="y",alpha=.5); ax.set_title("Standalone cdac_diff_v4 switched-charge transfer screen")
ax.text(.02,.04,"1-unit branch −27.94%; screening FAIL. v4 standalone data, not integrated v6.",transform=ax.transAxes,color="#b91c1c",weight="bold")
save(fig,"waveforms/03_cdac_v4_weight_error.png")

# Three-latch bank regeneration from real standalone transistor-level Spectre data.
co=npz("results/physical/comparator_bank3_spectre/case2_vin910mV/waveforms.npz"); tt=co["time"]*1e9
fig,ax=plt.subplots(3,1,figsize=(12,8),sharex=True,gridspec_kw={"height_ratios":[1,2,1]})
for k,c in [("clk","#2563eb"),("clkb","#f97316")]: ax[0].plot(tt,co[k],label=k,color=c)
ax[0].set_ylabel("Clock (V)"); ax[0].legend(ncol=2); ax[0].grid(True,alpha=.5)
for i,c in enumerate(["#0f766e","#9333ea","#dc2626"]): ax[1].plot(tt,co[f"outp{i}"]-co[f"outn{i}"],label=f"latch {i}",color=c,lw=1.3)
ax[1].axhline(0,color="#64748b",lw=.7); ax[1].set_ylabel("Output differential (V)"); ax[1].legend(ncol=3); ax[1].grid(True,alpha=.5)
ax[2].plot(tt,co["inp"],label="input",color="#2563eb")
for i,c in enumerate(["#0f766e","#9333ea","#dc2626"]): ax[2].axhline(co[f"inn{i}"][0],ls="--",color=c,label=f"threshold {i}")
ax[2].set_ylabel("Input (V)"); ax[2].set_xlabel("Time (ns)"); ax[2].legend(ncol=4,fontsize=9); ax[2].grid(True,alpha=.5); ax[0].set_title("OA doubletail_bank3 — Spectre regeneration, Vin=0.910 V")
save(fig,"waveforms/04_comparator_bank3_spectre.png")
with (PKG/"analog/comparator_bank3_trace.csv").open("w",newline="") as f:
 w=csv.writer(f); w.writerow(["time_s","clk_V","clkb_V","inp_V","inn0_V","inn1_V","inn2_V","cmp0_diff_V","cmp1_diff_V","cmp2_diff_V"]); w.writerows(zip(co["time"],co["clk"],co["clkb"],co["inp"],co["inn0"],co["inn1"],co["inn2"],co["outp0"]-co["outn0"],co["outp1"]-co["outn1"],co["outp2"]-co["outn2"]))

# Read five physical comparator-strobe measurements from each completed AMS log.
cases=[("−0.6 V",ROOT/"results/raw/first_integrated_adc_capture/cases/negative_fullscale/xrun_feedback.log",0,0),("0 V",ROOT/"results/raw/first_integrated_adc_capture/cases/zero/xrun_feedback.log",172,128),("+0.6 V",ROOT/"results/physical/ams_adc_direction_20261013/xrun_feedback.log",255,255)]
pat=re.compile(r"AMS_ANALOG_COMPARATOR_WAVE t=(\S+) stage=(\d+) therm=\d*([01xXzZ]{3}) valid=\d*(\d) dac_p=([\d.eE+-]+).*?cmp0p=([\d.eE+-]+) cmp0n=([\d.eE+-]+) cmp1p=([\d.eE+-]+) cmp1n=([\d.eE+-]+) cmp2p=([\d.eE+-]+) cmp2n=([\d.eE+-]+)")
allr=[]
for label,path,actual,golden in cases:
 rr=[]
 for line in path.read_text(errors="replace").splitlines():
  m=pat.search(line)
  if m:
   g=m.groups(); rr.append({"input_case":label,"time_s":float(g[0]),"stage":int(g[1]),"thermometer":g[2],"pair_valid":int(g[3]),"dac_p_V":float(g[4]),"cmp0p_V":float(g[5]),"cmp0n_V":float(g[6]),"cmp1p_V":float(g[7]),"cmp1n_V":float(g[8]),"cmp2p_V":float(g[9]),"cmp2n_V":float(g[10]),"actual_code":actual,"golden_code":golden,"source_log":str(path.relative_to(ROOT))})
 if len(rr)!=5 and label=="+0.6 V":
  for r in csv.DictReader((ROOT/"results/raw/first_integrated_adc_capture/stages.csv").open()):
   rr.append({"input_case":label,"time_s":float(r["time_s"]),"stage":int(r["stage"]),"thermometer":r["thermometer"],"pair_valid":int(r["pair_valid"]),"dac_p_V":float(r["dac_p_V"]),**{f"cmp{i}{s}_V":float(r[f"cmp{i}{s}_V"]) for i in range(3) for s in ("p","n")},"actual_code":actual,"golden_code":golden,"source_log":"results/raw/first_integrated_adc_capture/stages.csv"})
 allr.extend(rr)
fields=["input_case","time_s","stage","thermometer","pair_valid","dac_p_V","cmp0p_V","cmp0n_V","cmp1p_V","cmp1n_V","cmp2p_V","cmp2n_V","actual_code","golden_code","source_log"]
with (PKG/"waveforms/ams_feedback_stages.csv").open("w",newline="") as f: w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(allr)
fig,axes=plt.subplots(3,2,figsize=(13,9),sharex="col",gridspec_kw={"width_ratios":[2,1]})
for j,(label,path,actual,golden) in enumerate(cases):
 pts=[x for x in allr if x["input_case"]==label]; stages=[x["stage"] for x in pts]; vals=[x["dac_p_V"] for x in pts]
 axes[j,0].scatter(stages,vals,s=65,color="#0f766e",edgecolor="white")
 for x,y in zip(stages,vals): axes[j,0].annotate(f"{y:.3f} V",(x,y),xytext=(0,8),textcoords="offset points",ha="center",fontsize=8)
 axes[j,0].set_ylabel("DAC+ (V)"); axes[j,0].set_xticks(range(5)); axes[j,0].grid(True,alpha=.5); axes[j,0].set_title(f"{label} input — actual analog strobe values")
 lev=[int(x["thermometer"],2) for x in pts]; axes[j,1].scatter(stages,lev,s=65,color="#7c3aed",edgecolor="white")
 axes[j,1].set_yticks([0,1,3,7],["000","001","011","111"]); axes[j,1].set_ylim(-.5,7.5); axes[j,1].set_xticks(range(5)); axes[j,1].grid(True,alpha=.5)
 axes[j,1].set_title(f"actual {actual} / golden {golden} — "+("FAIL" if actual!=golden else "code match"))
for a in axes[-1,:]: a.set_xlabel("SAR decision stage")
fig.suptitle("Five-step closed-loop AMS/Spectre captures\nDots are saved physical comparator strobes, not interpolated waveforms",fontsize=14,weight="bold"); fig.tight_layout(rect=(0,0,1,.94))
save(fig,"waveforms/05_ams_feedback_three_cases.png")

# Saved cross-simulator checkpoints only.
cmpd=json.loads((ROOT/"results/physical/ams_oa_source_flow_20261013/comparison_edge_aligned_reltol1e-5.json").read_text())
fig,ax=plt.subplots(1,2,figsize=(12,5))
for a,key,title,ylabel,scale in [(ax[0],"dac_p_V","DAC+ output","V",1),(ax[1],"supply_current_A","Supply current","µA",1e6)]:
 for run,c,off in [("standalone","#2563eb",-.06),("ams","#f97316",.06)]:
  values=[cmpd["analog_comparison"][f"{t:.1f}ns"][run][key]*scale for t in [3.2,3.6]]
  a.scatter(np.array([3.2,3.6])+off,values,s=80,label=run,color=c)
  for x,y in zip(np.array([3.2,3.6])+off,values): a.annotate(f"{y:.4g}",(x,y),xytext=(0,7),textcoords="offset points",ha="center",fontsize=8)
 a.set_xticks([3.2,3.6],["3.2 ns","3.6 ns"]); a.set_title(title); a.set_ylabel(ylabel); a.grid(True,alpha=.5); a.legend()
ax[1].text(.02,.04,"34.3% / 36.8% mismatch — FAIL",transform=ax[1].transAxes,color="#b91c1c",weight="bold")
fig.suptitle("Standalone Spectre vs AMS — saved observation checkpoints only",weight="bold"); save(fig,"waveforms/06_standalone_ams_checkpoints.png")

# Actual timing arcs from Genus report.
seg=(ROOT/"results/digital/channel_wrapper_20261013/timing.rpt").read_text(errors="replace").split("Path 1:")[1].split("Path 2:")[0]
names=[]; delays=[]
for line in seg.splitlines():
 if "->" in line and "Arrival" not in line and "Cell" not in line:
  fs=line.split()
  if len(fs)>=8:
   try: delays.append(int(fs[-3])); names.append(fs[0].split("/")[-1])
   except ValueError: pass
fig,ax=plt.subplots(figsize=(14,7))
if names: ax.bar(range(len(names)),delays,color=["#dc2626" if x>=200 else "#2563eb" for x in delays]); ax.set_xticks(range(len(names)),names,rotation=75,ha="right",fontsize=7)
ax.set_ylabel("Cell delay (ps)"); ax.grid(axis="y",alpha=.5); ax.set_title("Genus critical path — 34 reported timing arcs")
fig.text(.02,.01,"u_sar_code_reg[4]/CP → u_correction_out_code_reg[6]/D; arrival 4116 ps; required 447 ps; slack −3669 ps. 650 ps cycle, setup 153 ps, uncertainty 50 ps. Synthesized only.",color="#b91c1c",weight="bold",fontsize=9)
save(fig,"digital/07_genus_critical_path.png")
# Saved Genus area/timing summary; both area runs are shown to expose report revision difference.
fig,ax=plt.subplots(1,2,figsize=(12,5))
labels=["Earlier replay","Later detailed report"]
cells=[2572,2595]; areas=[43699.970,44393.0]
colors=["#64748b","#2563eb"]
ax[0].bar(labels,cells,color=colors); ax[0].set_ylabel("Mapped cells"); ax[0].set_title("Synthesized digital wrapper"); ax[0].grid(axis="y",alpha=.4)
for i,v in enumerate(cells): ax[0].text(i,v+8,f"{v:,}",ha="center",weight="bold")
ax[1].bar(labels,areas,color=colors); ax[1].set_ylabel("Area (µm²)"); ax[1].set_title("Genus synthesis area"); ax[1].grid(axis="y",alpha=.4)
for i,v in enumerate(areas): ax[1].text(i,v+80,f"{v:,.3f}",ha="center",fontsize=9,weight="bold")
fig.suptitle("Saved Genus results: area revisions differ; both timing runs fail",weight="bold")
fig.text(.04,.01,"Earlier replay slack −3.578 ns (4042 ps / 464 ps); later detailed slack −3.669 ns (4116 ps / 447 ps). Timing target 650 ps. Synthesized wrapper only.",color="#b91c1c",fontsize=9)
save(fig,"digital/10_genus_area_timing_summary.png")

# Derived block diagrams from actual OA netlist and wrapper/RTL connections.
def box(ax,x,y,w,h,text,fc,fs=10):
 p=FancyBboxPatch((x,y),w,h,boxstyle="round,pad=.02,rounding_size=.04",facecolor=fc,edgecolor="#334155",linewidth=1.4); ax.add_patch(p); ax.text(x+w/2,y+h/2,text,ha="center",va="center",fontsize=fs,weight="bold")
def arrow(ax,a,b,label=""):
 ax.add_patch(FancyArrowPatch(a,b,arrowstyle="-|>",mutation_scale=15,color="#334155",lw=1.4))
 if label: ax.text((a[0]+b[0])/2,(a[1]+b[1])/2+.12,label,ha="center",fontsize=8)
fig,ax=plt.subplots(figsize=(12,6)); ax.set_xlim(0,12); ax.set_ylim(0,7); ax.axis("off")
box(ax,3.5,5.3,5,1,"adc_analog_channel_bank3_v1\nOA analog hierarchy","#dbeafe",14)
box(ax,.5,2.7,3.1,1.3,"sampler_core_v2\ntrack + ainp/ainn\ndac_p / dac_n","#dcfce7")
box(ax,4.4,2.7,3.1,1.3,"cdac_diff_v6\n9 weighted branches\nreference switching","#fef3c7")
box(ax,8.3,2.7,3.1,1.3,"doubletail_bank3\n3 regenerative latches\nth0/th1/th2","#fee2e2")
arrow(ax,(4,3.35),(4.4,3.35)); arrow(ax,(7.5,3.35),(8.3,3.35))
ax.text(6,1.45,"OA-generated netlist: sampler + CDAC + comparator bank. Executed AMS inventory: 230 BSIM devices.\nComparator bank senses dac_p versus three external thresholds; dac_n does not feed the bank.",ha="center",fontsize=10)
ax.text(6,.45,"Derived hierarchy diagram from OA netlist — not a Virtuoso schematic screenshot.",ha="center",color="#b91c1c",weight="bold")
save(fig,"diagrams/08_oa_hierarchy_derived.png")
fig,ax=plt.subplots(figsize=(14,7)); ax.set_xlim(0,14); ax.set_ylim(0,8); ax.axis("off")
box(ax,.4,5.7,2.2,1.1,"SCL180 OA analog\nsampler/CDAC/comparator","#e0f2fe",9); box(ax,3.4,5.7,2.2,1.1,"E2L bridge\n0.6 / 1.2 V","#fef3c7",9)
box(ax,6.4,5.7,2.2,1.1,"pulsar_cmp_quantize\ncomplement pairs → thermo","#ede9fe",9); box(ax,9.5,5.7,2.2,1.1,"pulsar_sar_sync\n5 phases","#dcfce7",9)
box(ax,9.5,2.6,2.2,1.1,"pulsar_cdac_ctrl\n9-bit command","#ffedd5",9); box(ax,6.4,2.6,2.2,1.1,"L2E bridge\n0 / 1.8 V gates","#fef3c7",9)
box(ax,3.4,2.6,2.2,1.1,"Real OA CDAC\nreference switches","#e0f2fe",9); box(ax,.4,2.6,2.2,1.1,"pulsar_affine\nregistered code/valid","#f3f4f6",9)
arrow(ax,(2.6,6.25),(3.4,6.25)); arrow(ax,(5.6,6.25),(6.4,6.25)); arrow(ax,(8.6,6.25),(9.5,6.25),"therm / valid")
arrow(ax,(10.6,5.7),(10.6,3.7),"cdac_reverse"); arrow(ax,(9.5,3.15),(8.6,3.15)); arrow(ax,(6.4,3.15),(5.6,3.15)); arrow(ax,(4.5,3.7),(4.5,5.7),"analog controls"); arrow(ax,(9.5,5.85),(2.6,3.5),"raw code / valid")
ax.text(7,1.2,"Physical comparator decisions feed SAR and SAR commands drive transistor CDAC. cmp_valid is bench-timed after resolution.\nThresholds are fixed external DC sources; stage-dependent residue mapping is unresolved.",ha="center",fontsize=10,color="#7f1d1d",weight="bold")
ax.text(7,.4,"Derived from actual AMS wrapper/RTL; not a schematic screenshot.",ha="center",fontsize=9,color="#b91c1c")
save(fig,"diagrams/09_feedback_dataflow_derived.png")

# Results CSV with condition, fidelity, tool, run and source for every value.
out=[]
def add(name,value,unit,cond,fid,tool,run,source,status,note):
 out.append({"measurement":name,"value":value,"unit":unit,"test_condition":cond,"circuit_fidelity":fid,"simulator_tool":tool,"run_directory":run,"source_filename":source,"design_revision":"PULSAR4X FULLBUILD evidence snapshot 2026-10-13","status":status,"interpretation":note})
add("Process technology","SCL180 / 0.18 um","process","SCL PDK","OA transistor hierarchy","Spectre/Xcelium AMS","ams_oa_source_flow_20261013","results/physical/ams_oa_source_flow_20261013/xrun_verified.log","VERIFIED","No fabricated silicon")
add("Analog core supply",1.8,"V","TT benches","transistor level","Spectre 21.1","sampler_core_v2_OA_R1ohm","results/physical/sampler_core_v2_OA_R1ohm/metrics.json","CONDITION","Genus SS run uses 1.62 V")
add("ADC resolution target",8,"bits","target","requirement","spec","—","reports/PULSAR4X_FINAL_TECHNICAL_REPORT.md","TARGET_ONLY","No performance claim")
add("Per-channel rate target",100,"MS/s","nominal","requirement","spec","—","reports/PULSAR4X_FINAL_TECHNICAL_REPORT.md","NOT_MET","Not qualified")
add("Aggregate rate target",400,"MS/s","four channels","requirement","spec","—","reports/PULSAR4X_FINAL_TECHNICAL_REPORT.md","NOT_MET","Four-channel ADC absent")
add("Functional bring-up rate","about 10","MS/s/channel","five decisions at 20 ns spacing","AMS transistor feedback + RTL","Xcelium 22.09 / Spectre 21.1","three AMS cases","results/raw/first_integrated_adc_capture/case_summary.json","FUNCTIONAL_ONLY","Not 100 MS/s qualification")
add("Executed SCL180 BSIM devices",230,"devices","adc_analog_channel_bank3_v1","OA transistor hierarchy","Xcelium AMS/Spectre","ams_oa_source_flow_20261013","results/physical/ams_oa_source_flow_20261013/xrun_verified.log","VERIFIED","Inventory reports bsim3v3 230")
add("Decision phases per conversion",5,"phases","physical comparator evaluated five times","transistor comparator feedback to SAR","Xcelium AMS/Spectre","three completed cases","results/raw/first_integrated_adc_capture/case_summary.json","DEMONSTRATED","Threshold mapping unresolved")
cs=json.loads((ROOT/"results/raw/first_integrated_adc_capture/case_summary.json").read_text())
for c in cs: add("AMS output code "+c["case"],c["actual_corrected_code"],"code",f"ainp={c['ainp_V']} V, ainn={c['ainn_V']} V, diff={c['differential_V']} V","actual OA analog + SAR RTL; fixed thresholds","Xcelium/Spectre",c["simulator_log"],"results/raw/first_integrated_adc_capture/case_summary.json","PASS_CODE_MATCH" if c["code_match"] else "FAIL_CODE_MISMATCH",f"golden {c['golden_corrected_code']}; physical decisions {c['actual_transistor_comparator_decisions']}; golden {c['golden_decisions']}")
replay=json.loads((ROOT/"results/digital/channel_wrapper_20261013/replay.json").read_text())
add("Genus cell count earlier replay",replay["genus"]["mapped_cells"],"cells","650 ps clock, SCL FS120 SS","synthesized wrapper","Genus 21.14","earlier replay","results/digital/channel_wrapper_20261013/replay.json","TIMING_FAIL","Earlier run; later area report differs")
add("Genus area earlier replay",replay["genus"]["area_um2"],"um^2","earlier replay","synthesized wrapper","Genus 21.14","earlier replay","results/digital/channel_wrapper_20261013/replay.json","TIMING_FAIL","Not full-chip area")
add("Genus cell count latest area report",2595,"cells","SS 1.62 V / 125 C / 650 ps","synthesized wrapper","Genus 21.14","Oct 13 12:15","results/digital/channel_wrapper_20261013/area.rpt","TIMING_FAIL","Latest saved detailed area report")
add("Genus area latest area report",44393.0,"um^2","same latest report","synthesized wrapper","Genus 21.14","Oct 13 12:15","results/digital/channel_wrapper_20261013/area.rpt","TIMING_FAIL","Not full-chip area")
for name,value,unit,note in [("Critical arrival",4116,"ps","SAR code register to affine output; 34 arcs"),("Critical required",447,"ps","650 ps edge minus setup/uncertainty"),("Critical slack",-3669,"ps","FAIL"),("SAR accumulator arrival",2384,"ps","stage register to raw accumulator"),("SAR accumulator required",410,"ps","FAIL"),("SAR accumulator slack",-1974,"ps","FAIL")]:
 add(name,value,unit,"650 ps control cycle","synthesized wrapper","Genus 21.14","Oct 13 12:15","results/digital/channel_wrapper_20261013/timing.rpt","FAIL",note)
sm=json.loads((ROOT/"results/physical/sampler_core_v2_OA_R1ohm/metrics.json").read_text())
add("Sampler held-sample error",sm["held_sample_error_LSB"],"LSB","TT/27 C, 1.8 V, 1 ohm, 0.6 V differential step","OA sampler Spectre","Spectre 21.1","sampler_core_v2_OA_R1ohm","results/physical/sampler_core_v2_OA_R1ohm/metrics.json","FAIL","100 ps after edge")
add("Sampler switch turn-off step",sm["turnoff_step_V"]*1e3,"mV","same test","OA sampler Spectre","Spectre 21.1","sampler_core_v2_OA_R1ohm","results/physical/sampler_core_v2_OA_R1ohm/metrics.json","FAIL","Switching/clock aggregate")
small=list(csv.DictReader((ROOT/"results/physical/cdac_diff_v4_spectre/weight_transfer.csv").open()))[-1]
add("CDAC 1-unit branch error",float(small["relative_step_error_percent"]),"%","v4 standalone, TT/27 C, 18 ns","OA SCL180 transistor/MIM screen","Spectre 21.1","cdac_diff_v4_spectre/bit8","results/physical/cdac_diff_v4_spectre/weight_transfer.csv","FAIL_SCREENING","Integrated top uses v6")
cmpd=json.loads((ROOT/"results/physical/ams_oa_source_flow_20261013/comparison_edge_aligned_reltol1e-5.json").read_text())
for when,p in cmpd["analog_comparison"].items():
 add("AMS minus standalone DAC+ "+when,p["ams"]["dac_p_V"]-p["standalone"]["dac_p_V"],"V","matched fixed-control checkpoint","OA transistor hierarchy","AMS/Spectre vs Spectre","ams_oa_source_flow_20261013","results/physical/ams_oa_source_flow_20261013/comparison_edge_aligned_reltol1e-5.json","WITHIN_1mV","Point only")
 add("AMS minus standalone DAC− "+when,p["ams"]["dac_n_V"]-p["standalone"]["dac_n_V"],"V","matched fixed-control checkpoint","OA transistor hierarchy","AMS/Spectre vs Spectre","ams_oa_source_flow_20261013","results/physical/ams_oa_source_flow_20261013/comparison_edge_aligned_reltol1e-5.json","WITHIN_1mV","Point only")
 add("AMS current relative error "+when,p["supply_current_abs_relative_error"]*100,"%","matched fixed-control checkpoint","OA transistor hierarchy","AMS/Spectre vs Spectre","ams_oa_source_flow_20261013","results/physical/ams_oa_source_flow_20261013/comparison_edge_aligned_reltol1e-5.json","FAIL","Cause unresolved")
add("Xcelium digital code-center cases",256,"cases","bypass/correction/saturation assumptions","RTL only","Xcelium 22.09","channel_wrapper_20261013","results/digital/channel_wrapper_20261013/xrun_cdac_ctrl.log","PASS_DIGITAL_ONLY","Not analog verification")
add("Python analysis tests",44,"tests","metrics/model tests","software only","pytest","verification replay 20261013","results/verification/replay_20261013/pytest.log","PASS_SOFTWARE_ONLY","Not hardware verification")
for metric in ["ENOB","SNDR","SFDR","DNL","INL","ADC SNR","ADC THD","ADC power","energy per conversion"]:
 add(metric,"NOT MEASURED","—","No qualified ADC capture","not measured","—","—","reports/ADC_FINAL_RESULTS_TABLE.csv","NOT_MEASURED","No estimate substituted")
with (PKG/"results/VERIFIED_RESULTS.csv").open("w",newline="") as f:
 w=csv.DictWriter(f,fieldnames=list(out[0])); w.writeheader(); w.writerows(out)

# Excerpts are source-derived text snippets, not GUI screenshots.
for name,src,keys in [("sar_controller_excerpt.sv","digital/rtl/pulsar_sar_sync.sv",["module pulsar_sar_sync","cmp_valid","cmp_therm","cdac_reverse","raw_valid"]),("cdac_adapter_excerpt.sv","digital/rtl/pulsar_cdac_ctrl.sv",["module pulsar_cdac_ctrl","reverse","nsel_b","psel_b"]),("comparator_quantizer_excerpt.sv","digital/rtl/pulsar_cmp_quantize.sv",["module pulsar_cmp_quantize","pair_valid","therm"]),("affine_excerpt.sv","digital/rtl/pulsar_affine.sv",["module pulsar_affine","gain_q12","offset_q8","out_valid","out_code"])]:
 lines=(ROOT/src).read_text(errors="replace").splitlines(); ix=[i for i,x in enumerate(lines) if any(k in x for k in keys)]; keep=sorted({j for i in ix for j in range(max(0,i-1),min(len(lines),i+2))})
 (PKG/"digital"/name).write_text("// Derived excerpt from "+src+"; full source is authoritative.\n"+"\n".join(lines[j] for j in keep)+"\n")
print("Generated",len(out),"verified-results rows and review plots under",PKG)

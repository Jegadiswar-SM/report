#!/usr/bin/env python3
"""Export report text and source-backed figures to a paginated PDF; runs no EDA tools."""
from pathlib import Path
import textwrap
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
P=Path(__file__).resolve().parents[1]
md=P/'report/PULSAR4X_REVIEW_02.md'
figures=[
('OA hierarchy (derived diagram, not a Virtuoso screenshot)','diagrams/08_oa_hierarchy_derived.png','Derived from the OA-generated Spectre netlist. Executed AMS inventory: 230 SCL180 BSIM devices.'),
('Sampler sample/hold','waveforms/01_sampler_oa_spectre.png','OA sampler_core_v2 Spectre data, TT/27 C, 1.8 V, 1 ohm. Measured held error: +5.097 LSB.'),
('Standalone CDAC switched response','waveforms/02_cdac_v4_standalone_spectre.png','Standalone OA cdac_diff_v4 data. This is not the integrated cdac_diff_v6.'),
('Standalone CDAC transfer screen','waveforms/03_cdac_v4_weight_error.png','Saved Spectre weight transfer. The 1-unit branch error is −27.94% after 18 ns.'),
('Comparator regeneration','waveforms/04_comparator_bank3_spectre.png','Transistor-level Spectre vectors from standalone doubletail_bank3.'),
('AMS feedback dataflow (derived diagram)','diagrams/09_feedback_dataflow_derived.png','Reconstructed from the AMS wrapper and RTL; not a schematic screenshot.'),
('Five-decision AMS captures','waveforms/05_ams_feedback_three_cases.png','Actual transaction comparator strobes and code outcomes. The zero input produces 172 versus golden 128.'),
('Standalone versus AMS checkpoints','waveforms/06_standalone_ams_checkpoints.png','Saved DAC and current checkpoints; current equivalence fails.'),
('Genus critical path','digital/07_genus_critical_path.png','Saved Genus timing report; digital wrapper synthesis only, −3.669 ns slack.')]
with PdfPages(P/'report/PULSAR4X_REVIEW_02.pdf') as pdf:
 lines=[]
 for line in md.read_text().splitlines():
  if line.startswith('#'): lines.append(('H',line.lstrip('#').strip()))
  elif line.startswith('> '): lines.append(('Q',line[2:]))
  else:
   if line.startswith('|'): line=line.replace('|','  |  ')
   lines.extend(('T',x) for x in (textwrap.wrap(line,width=98,break_long_words=False,replace_whitespace=False) or ['']))
 for page_no,start in enumerate(range(0,len(lines),43),1):
  fig=plt.figure(figsize=(8.27,11.69),facecolor='white');ax=fig.add_axes([.09,.075,.82,.86]);ax.axis('off');y=1.0
  for typ,txt in lines[start:start+43]:
   if typ=='H': fs=13 if txt.startswith('PULSAR') else 10.5;color='#12304a';weight='bold';step=.036
   elif typ=='Q': fs=8.3;color='#8b1e2d';weight='bold';step=.03
   else: fs=7.3;color='#172b3a';weight='normal';step=.023
   ax.text(.01,y,txt,fontsize=fs,color=color,weight=weight,va='top',wrap=True);y-=step
  fig.text(.09,.035,'PULSAR-4X Review 02 · evidence snapshot through 13 Oct 2026',fontsize=7,color='#64748b')
  fig.text(.89,.035,str(page_no),fontsize=7,color='#64748b',ha='right');pdf.savefig(fig);plt.close(fig)
 for index,(title,rel,caption) in enumerate(figures,1):
  fig=plt.figure(figsize=(11.69,8.27),facecolor='white')
  fig.text(.06,.94,title,fontsize=17,weight='bold',color='#12304a')
  ax=fig.add_axes([.055,.12,.89,.77]);ax.axis('off');ax.imshow(plt.imread(P/rel),aspect='auto')
  fig.text(.06,.06,caption,fontsize=9,color='#334155',wrap=True)
  fig.text(.94,.035,f'Figure {index} · source-backed export',fontsize=7,color='#64748b',ha='right')
  pdf.savefig(fig);plt.close(fig)
print(P/'report/PULSAR4X_REVIEW_02.pdf')

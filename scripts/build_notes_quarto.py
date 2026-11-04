"""Build an annotated Quarto edition without modifying the supplied Markdown notes."""
from pathlib import Path
import re,json
ROOT=Path(__file__).resolve().parents[1]
# notes section -> blog section, protocol, deeper companion
sections={
'0':('1–12','workflow.qmd','jiaxuan-reading-guide.qmd'),
'1':('8.1; 2.3','experiments/08-fitting.qmd','deep-dives/loss-and-allocation.qmd'),
'2':('2','experiments/02-objectives.qmd','deep-dives/capabilities-and-validation.qmd'),
'3':('3','experiments/03-measurement.qmd','deep-dives/measurement-and-compute.qmd'),
'4':('4; 5.1','experiments/04-architecture.qmd','architecture-evidence.qmd'),
'5':('5','experiments/05-grid-budget.qmd','deep-dives/grid-and-inference.qmd'),
'6':('6','experiments/06-optimizers.qmd','deep-dives/schedules-and-timescales.qmd'),
'7':('7','experiments/07-data-mixture.qmd','deep-dives/data-and-repetition.qmd'),
'8':('8','experiments/08-fitting.qmd','deep-dives/grid-and-inference.qmd'),
'9':('9','experiments/09-downstream.qmd','deep-dives/capabilities-and-validation.qmd'),
'10':('10','experiments/10-validation.qmd','deep-dives/capabilities-and-validation.qmd'),
'11':('11','experiments/11-specialized.qmd','nemotron-pretraining.qmd'),
'12':('12','experiments/12-execution.qmd','deep-dives/capabilities-and-validation.qmd'),
'A':('Appendix A','experiments/13-public-ladders.qmd','architecture-evidence.qmd'),
'B':('Various numerical examples','notes-review.qmd','source-guide.qmd'),
'C':('12.4','workflow.qmd','deep-dives/capabilities-and-validation.qmd')}
sub={
'1.1':'deep-dives/loss-and-allocation.qmd#allocation','1.2':'deep-dives/loss-and-allocation.qmd#coupling','1.3':'deep-dives/loss-and-allocation.qmd#compute-equivalence','1.4':'deep-dives/grid-and-inference.qmd#diagnostics',
'3.1':'deep-dives/measurement-and-compute.qmd#parameters','3.2':'deep-dives/measurement-and-compute.qmd#flops','3.3':'deep-dives/measurement-and-compute.qmd#tokens',
'4.1':'deep-dives/grid-and-inference.qmd#geometry','4.2':'architecture-evidence.qmd','4.3':'architecture-evidence.qmd','4.4':'nemotron-pretraining.qmd','4.5':'deep-dives/measurement-and-compute.qmd',
'5.1':'deep-dives/grid-and-inference.qmd#geometry','5.2':'deep-dives/grid-and-inference.qmd#ai2','5.3':'deep-dives/data-and-repetition.qmd#exposure','5.4':'deep-dives/grid-and-inference.qmd#dependence','5.5':'deep-dives/grid-and-inference.qmd#diagnostics','5.6':'nemotron-pretraining.qmd',
'6.2':'architecture-evidence.qmd','6.3':'optimizers/marin-hyperparameter-search.qmd','6.4':'deep-dives/schedules-and-timescales.qmd#timescale','6.5':'deep-dives/schedules-and-timescales.qmd#endpoints','6.6':'nemotron-pretraining.qmd','6.7':'deep-dives/schedules-and-timescales.qmd#experiment','6.8':'experiments/06-optimizers.qmd','6.9':'deep-dives/schedules-and-timescales.qmd#endpoints',
'7.1':'deep-dives/data-and-repetition.qmd#source-value','7.2':'deep-dives/data-and-repetition.qmd#exposure','7.3':'deep-dives/data-and-repetition.qmd#repetition',
'8.0':'deep-dives/measurement-and-compute.qmd','8.1':'deep-dives/loss-and-allocation.qmd','8.2':'deep-dives/schedules-and-timescales.qmd','8.3':'deep-dives/grid-and-inference.qmd#fitting','8.4':'deep-dives/grid-and-inference.qmd#diagnostics','8.5':'nemotron-pretraining.qmd',
'9.1':'deep-dives/capabilities-and-validation.qmd#ai2','9.2':'deep-dives/capabilities-and-validation.qmd#difficulty','9.3':'deep-dives/capabilities-and-validation.qmd#accuracy',
'10.1':'deep-dives/capabilities-and-validation.qmd#holdouts','10.2':'deep-dives/capabilities-and-validation.qmd#gates','10.3':'nemotron-pretraining.qmd','10.4':'experiments/10-validation.qmd','10.5':'experiments/10-validation.qmd','10.6':'deep-dives/capabilities-and-validation.qmd#gates',
'A.1':'source-guide.qmd','A.2':'experiments/13-public-ladders.qmd','A.3':'experiments/13-public-ladders.qmd','A.4':'workflow.qmd'}
source=(ROOT/'scaling_ladder_notes.md').read_text()
lines=source.splitlines(); records=[]; output=[];section=None;fenced=False
for line in lines:
 if line.startswith('# '):continue # YAML supplies the single document title.
 output.append(line)
 if line.startswith('```'):fenced=not fenced
 if fenced:continue
 if line.startswith('## '):
  heading=line[3:];m=re.match(r'(\d+)\.',heading) or re.match(r'Appendix ([ABC])\.',heading)
  if not m:continue
  section=m[1];blog,protocol,deeper=sections[section]
  output+=['','::: {.callout-note collapse="true"}','## Companion reading',f'This notes section corresponds to **blog §{blog}**. Read the [experiment protocol]({protocol}) and [detailed explanation]({deeper}). Claims needing qualifications are tracked in the [source review](notes-review.qmd).',':::','']
  records.append({'heading':heading,'level':2,'notes_section':section,'blog_section':blog,'protocol':protocol,'companion':deeper})
 elif line.startswith('### ') and section:
  heading=line[4:];m=re.match(r'([\dA]+\.\d+)',heading)
  target=sub.get(m[1] if m else '',sections[section][2])
  output+=['',f'[Read the detailed companion →]({target})','']
  records.append({'heading':heading,'level':3,'notes_section':m[1] if m else section,'companion':target})
front='''---
title: "The science of pretraining: annotated deep-dive notes"
number-sections: false
toc: true
toc-depth: 3
---

This Quarto edition is generated from the preserved [`scaling_ladder_notes.md`](../scaling_ladder_notes.md). The notes’ prose and equations are retained; the original top-level title is supplied through YAML, and companion-reading links are editorial additions. Regenerate with `python scripts/build_notes_quarto.py`.

::: {.callout-important}
Read the [primary-source review](notes-review.qmd) alongside these notes. In particular, the constant AdamW-timescale statement needs a cross-TPP qualification. Numerical claims in this synthesis are not all independently audited.
:::

Start with the [blog reading guide](jiaxuan-reading-guide.qmd) for the section crosswalk, or use the [source housekeeping page](source-guide.qmd) to locate papers and code.

'''
front+='For dedicated paper methods, read [Step Law](papers/step-law.qmd), [Farseer](papers/farseer.qmd), and [Power Lines](papers/power-lines.qmd). Marin replication is covered in the [optimizer search](optimizers/marin-hyperparameter-search.qmd) and [Datakit code manual](data/marin-code-walkthrough.qmd).\n\n'
front+='For the complete efforts, read [OLMo](olmo-pretraining.qmd), [Marin](marin-pretraining.qmd), and [the beginning-to-end pretraining design](from-data-to-pretraining.qmd).\n\n'
from doc_paths import rewrite, target, full_paths
old_page=ROOT/'doc/deep-dive-notes.qmd'; new_page=ROOT/'doc/reading/deep-dive-notes.qmd'
new_page.write_text(full_paths(rewrite(front+'\n'.join(output).strip()+'\n', old_page, new_page)))
for record in records:
 for key in ['protocol','companion']:
  if key in record: record[key]=target(record[key],old_page,new_page)
(ROOT/'doc/artifacts/notes-reading-map.json').write_text(json.dumps(records,indent=2,ensure_ascii=False)+'\n')
print('Annotated',len(records),'notes headings')

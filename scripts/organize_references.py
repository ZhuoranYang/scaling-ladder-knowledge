"""Rename references to topic/year/title folders; preserve identifiers in metadata."""
from pathlib import Path
import json,re,unicodedata
ROOT=Path(__file__).resolve().parents[1]; REF=ROOT/'references'
short={
'2412.02595':'nemotron-cc','2512.20848':'nemotron-3-nano','2604.12374':'nemotron-3-super','2606.15007':'nemotron-3-ultra','2203.15556':'chinchilla-compute-optimal-training','2203.03466':'mup-zero-shot-hyperparameter-transfer','2310.02244':'depth-mup-tensor-programs-vi','2412.04403':'ai2-task-scaling-model-ladders','2505.13738':'power-lines-batch-size-weight-decay','2503.04715':'step-law-hyperparameter-scaling','2409.19913':'scaling-learning-rate-across-token-horizons','2509.02046':'fantastic-pretraining-optimizers','2502.06857':'gemstones-width-depth-scaling','2402.00838':'olmo-technical-report','2501.00656':'olmo-2-technical-report','2512.13961':'olmo-3-technical-report','2409.02060':'olmoe-open-mixture-of-experts','2507.20534':'kimi-k2-technical-report','2602.02276':'kimi-k2-5-technical-report','2607.24653':'kimi-k3-technical-report'}
categories={'Scaling Law Foundations, Functional Forms, and Fitting':'scaling-laws','Hyperparameter Scaling Laws and Optimizers':'optimization','MoE':'architecture','Data Construction, Mixture, and Repetition':'data','LR Schedule and Training Wrap-up':'optimization','Downstream Task Prediction and Evaluation':'evaluation','Model Technical Reports and Ladder Examples':'model-reports','Further Reading':'optimization'}
titles={}; topics={};cat='scaling-laws'
blog=(ROOT/'doc/reading/scientific-scaling-ladder.md').read_text().split('## References',1)[1]
for line in blog.splitlines():
 if line.startswith('### '):cat=categories.get(line[4:],'scaling-laws')
 m=re.match(r'\d+\.\s+(.+?) — .*?arxiv.org/(?:abs|pdf)/(\d{4}\.\d{4,5})',line)
 if m:titles[m[2]]=re.sub(r'<[^>]*>','',m[1]);topics[m[2]]=cat
extras={'2409.02060':('OLMoE: Open Mixture-of-Experts Language Models','model-reports'),'OLMo-core-3-technical-report':('Olmo-core 3 technical report','model-reports'),'blog-delphi':('Delphi: An Open Scaling Suite','marin'),'blog-marin-data-pipeline-overview':('Marin Data Pipeline Overview','marin'),'blog-pretraining-speedup':('Marin Pretraining Efficiency','marin'),'papers-v11-cawley10a-html':('On Over-fitting in Model Selection and Subsequent Selection Bias','methodology')}
# Include fallback titles for further reading items not in numbered bibliography.
extras.update({'2512.20848':('Nemotron 3 Nano: Open, Efficient Mixture-of-Experts Hybrid Mamba-Transformer Model for Agentic Reasoning','model-reports'),'1812.06162':('An Empirical Model of Large-Batch Training','optimization'),'2305.13245':('GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints','architecture'),'2505.23971':('Critical Batch Size Revisited: A Simple Empirical Approach to Large-Batch Language Model Training','optimization'),'2503.09579':('Cost-Optimal Grouped-Query Attention for Long-Context Modeling','architecture')})
def slug(s):return re.sub(r'[^a-z0-9]+','-',unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower()).strip('-')[:82].rstrip('-')
rewrites={}
changes=json.loads((REF/'directory-map.json').read_text()) if (REF/'directory-map.json').exists() else {}
for folder in sorted(p.parent for p in REF.rglob('metadata.json') if (p.parent/'paper.pdf').exists() or (p.parent/'article.md').exists()):
 p=folder/'metadata.json'
 if not p.exists():continue
 meta=json.loads(p.read_text());aid=meta.get('id',next((k for k,v in changes.items() if v==str(folder.relative_to(REF))),folder.name));base=re.sub(r'v\d+$','',aid)
 title=titles.get(base);topic=topics.get(base,'scaling-laws')
 if base in extras:title,topic=extras[base]
 if not title:
  title=meta.get('title')
  topic=meta.get('topic',topic)
 if not title:raise ValueError('Missing human title for '+aid)
 year='20'+base[:2] if re.match(r'\d{4}\.',base) else ('2010' if 'cawley' in base else '2026')
 name=f'{year}-{short.get(base,slug(title))}'
 target=REF/topic/name
 if target.exists() and target!=folder:raise ValueError('Destination exists '+str(target))
 target.parent.mkdir(exist_ok=True)
 if folder!=target:folder.rename(target)
 old=str(folder.relative_to(REF))
 if old!=str(target.relative_to(REF)):rewrites[old]=str(target.relative_to(REF))
 for key,value in list(changes.items()):
  if value==old: changes[key]=str(target.relative_to(REF))
 changes[aid]=str(target.relative_to(REF))
 meta.update(title=title,topic=topic,folder=str(target.relative_to(REF)))
 (target/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
 readme=target/'README.md'
 if readme.exists():
  lines=readme.read_text().splitlines();lines[0]='# '+title;readme.write_text('\n'.join(lines)+'\n')
# Rewrite project-authored documents and notes; archived paper contents are immutable.
paths=list((ROOT/'doc').rglob('*.qmd'))+list((ROOT/'doc').rglob('*.md'))+[REF/'SOURCES.md',REF/'MARIN-READING.md',ROOT/'AGENTS.md']
for p in paths:
 s=p.read_text()
 for old,new in {**changes,**rewrites}.items():s=s.replace(old+'/',new+'/')
 p.write_text(s)
(REF/'directory-map.json').write_text(json.dumps(changes,indent=2)+'\n')
print('Renamed',len(changes),'reference folders')

"""Build the readable topic catalogue from per-reference metadata."""
import json
from collections import defaultdict
from pathlib import Path
root=Path(__file__).resolve().parents[1]/'references'
groups=defaultdict(list)
for p in root.rglob('metadata.json'):
 if not any((p.parent/n).exists() for n in ['paper.pdf','article.md','repository.tar.gz','audit.json']):continue
 m=json.loads(p.read_text());m['folder']=str(p.parent.relative_to(root));groups[m.get('topic','other')].append(m)
labels={'scaling-laws':'Scaling laws and fitting','architecture':'Architecture and MoE','optimization':'Optimizers and hyperparameter transfer','data':'Data construction, mixtures, and repetition','evaluation':'Evaluation and task prediction','model-reports':'Model technical reports','marin':'Marin reports and pipelines','methodology':'Research methodology','systems':'Training systems and source implementations'}
lines=['# Source catalogue','','References are organized by topic, then readable year/title folder names. ArXiv identifiers and versions remain in metadata. [Legacy-name lookup](directory-map.json) maps the earlier identifiers to the current folders.','','[Collection status and code availability](README.md) · [Machine-readable manifest](download-manifest.json)','','Each paper folder contains its PDF, extracted text, available LaTeX source, metadata, and discovered code archives. A linked code archive may be a baseline or dataset dependency; inspect its recorded role before reproducing an experiment.','']
for topic in labels:
 lines+=['## '+labels[topic],'','| Work | Identifier / source | Local files |','|---|---|---|']
 for m in sorted(groups.get(topic,[]),key=lambda m:m['folder']):
  f=m['folder'];item=next(n for n in ['paper.pdf','article.md','README.md'] if (root/f/n).exists())
  title=m.get('title',Path(f).name);identifier=m.get('id','Web report');url=m.get('url','')
  source=f'[{identifier}]({url})' if url else identifier
  lines.append(f'| {title} | {source} | [Read]({f}/{item}) · [Metadata]({f}/metadata.json) |')
 lines.append('')
(root/'SOURCES.md').write_text('\n'.join(lines))
print('Catalogued',sum(map(len,groups.values())),'references')

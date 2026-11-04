"""Rebuild the collection manifest and human-readable status report."""
from pathlib import Path
from collections import Counter
import json, zipfile
root=Path(__file__).resolve().parents[1]/'references'
records=[]
for p in sorted(root.rglob('metadata.json')):
 m=json.loads(p.read_text())
 for c in m.get('code',[]):
  if c.get('repository') and c.get('status')=='downloaded' and not c.get('archive'):
   name=c['repository'].split('github.com/')[-1].replace('/','--')
   archive=p.parent/'code'/name/'repository.zip'
   if archive.exists():
    c['archive']=str(archive.relative_to(p.parent))
    with zipfile.ZipFile(archive) as z: c['archive_root']=z.namelist()[0]
 m['folder']=str(p.parent.relative_to(root))
 p.write_text(json.dumps(m,indent=2)+'\n');records.append(m)
 if not (p.parent/'README.md').exists():
  (p.parent/'README.md').write_text(f'# {m.get("title",p.parent.name)}\n\nSource: {m.get("url","")}\n\n[Metadata](metadata.json) records downloaded artifacts and provenance.\n')
 elif 'id' in m:
  s=(p.parent/'README.md').read_text()
  note='\nCode archives snapshot the repository default branch at retrieval time, unless a commit is explicitly recorded. They are not established as the paper experiment revision. Repository roots inside ZIP archives are recorded in metadata where available.\n'
  if note.strip() not in s: (p.parent/'README.md').write_text(s+note)
(root/'download-manifest.json').write_text(json.dumps(records,indent=2)+'\n')
papers=[r for r in records if 'id' in r]
src=Counter(r['latex_source']['status'] for r in papers)
code=Counter(c['status'] for r in records for c in r.get('code',[]))
lines=['# Reference collection status','',f'{len(papers)} technical-report/paper folders, plus {len(records)-len(papers)} web/code/data-artifact reference folders.','',f'LaTeX source results: {dict(src)}.',f'Code archive results (per reference; shared repositories can appear more than once): {dict(code)}.','',
'References are grouped by topic, then readable year/title folder names. Identifiers remain in metadata and directory-map.json. ArXiv folders contain `paper.pdf`, extracted `paper.txt`, `metadata.json`, an `arxiv-source.tar` download, extracted `source/`, and discovered code archives under `code/`. Source archives may be gzip-compressed despite the `.tar` suffix. Unversioned arXiv requests resolve at collection time; do not assume they match an earlier paper version.','',
'Code discovery uses paper text, abstracts, and LaTeX links. These can include baselines, evaluation suites, and data tooling. An archive is evidence of code availability, not evidence of a complete training reproduction. Default-branch archives are current snapshots; inspect experiment-specific revisions before running them. Large downloads are capped by the collector and explicitly reported below.','',
'[Source inventory](SOURCES.md) · [Machine-readable manifest](download-manifest.json) · [Marin reading map](MARIN-READING.md)','','## Remaining code download failures','']
for r in records:
 for c in r.get('code',[]):
  if c['status']!='downloaded': lines.append(f'- `{r["folder"]}`: [{c["repository"]}]({c["repository"]}) — {c.get("reason",c["status"])}')
lines+=['','## Recollecting','', 'From the repository root, run `python scripts/collect_references.py`, then `python scripts/collect_reference_code.py`, then `python scripts/summarize_references.py` and `python scripts/build_reference_catalog.py`. The source-code pass searches extracted LaTeX for links lost in PDF text extraction. Existing downloads are reused. Review metadata before replacing or updating snapshots.','']
(root/'README.md').write_text('\n'.join(lines))
print('PAPERS',len(papers),'SOURCE',dict(src),'CODE',dict(code))
print('ZERO_TEX',[r['id'] for r in papers if r['latex_source'].get('status')=='downloaded' and r['latex_source'].get('tex_files',0)==0])

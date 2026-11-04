"""One-time folder migration with local-link rewrites and a durable path map.
Preserves the supplied root notes; only local links/assets change in imported blog.
"""
from pathlib import Path
import json,hashlib
from doc_paths import ROOT,rewrite,full_paths
GROUPS={
'reading':['scientific-scaling-ladder.md','jiaxuan-reading-guide.qmd','deep-dive-notes.qmd','notes-review.qmd'],
'sources':['source-guide.qmd'],
'workflow':['workflow.qmd','from-data-to-pretraining.qmd','industry-practice-audit.qmd'],
'architecture':['architecture-evidence.qmd','smelt-looped-moe.qmd'],
'efforts':['olmo-pretraining.qmd','marin-pretraining.qmd','nemotron-pretraining.qmd'],
'data':['marin-data-engineering.qmd'],
'plans':['plan-96-h100.qmd','hero-h100-candidate.qmd'],
'evaluation':['checkpoint-evaluation.qmd'],
'training':['trainer-playbook.qmd']}
def main():
 moves={f'doc/{n}':f'doc/{g}/{n}' for g,names in GROUPS.items() for n in names}
 for p in (ROOT/'doc/data').iterdir():
  if p.is_file() and p.suffix in ['.json','.csv','.md']:moves[p.relative_to(ROOT).as_posix()]='doc/artifacts/'+p.name
 mapfile=ROOT/'doc/path-migration.json'
 if mapfile.exists():raise SystemExit('Migration map exists: review/reuse the recorded map rather than migrating twice.')
 originals={k:hashlib.sha256((ROOT/k).read_bytes()).hexdigest() for k in moves if (ROOT/k).exists()}
 mapfile.write_text(json.dumps({'date':'2026-11-02','moves':moves,'before_sha256':originals,'note':'Supplied root Markdown notes are preserved. Imported blog content changes only for relocated local links/assets.'},indent=2)+'\n')
 docs=[p for p in (ROOT/'doc').rglob('*') if p.suffix in ['.qmd','.md'] and p.is_file()]
 for old in docs:
  key=old.relative_to(ROOT).as_posix();new=ROOT/moves.get(key,key);s=rewrite(old.read_text(),old,new);s=full_paths(s)
  new.parent.mkdir(parents=True,exist_ok=True);new.write_text(s)
  if old!=new:old.unlink()
 for k,v in moves.items():
  old=ROOT/k;new=ROOT/v
  if old.exists() and old!=new:
   new.parent.mkdir(parents=True,exist_ok=True);old.rename(new)
 for name in ['README.md','AGENTS.md','references/MARIN-READING.md','references/README.md','references/SOURCES.md']:
  p=ROOT/name;p.write_text(full_paths(rewrite(p.read_text(),p,p)))
 print('Moved',len(moves),'documentation/artifact paths; local links rewritten.')
if __name__=='__main__':main()

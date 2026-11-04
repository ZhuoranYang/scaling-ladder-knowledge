import sys,json,re
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0,str(Path('scripts').resolve()))
from collect_references import fetch
paths=[p for p in Path('references').rglob('metadata.json') if (p.parent/'source').exists()]
def collect(p):
 m=json.loads(p.read_text()); text=''
 for t in (p.parent/'source').rglob('*.tex'):
  text+='\n'+'\n'.join(l for l in t.read_text(errors='replace').splitlines() if not l.lstrip().startswith('%'))
 repos=sorted(set(r.rstrip('.') for r in re.findall(r'https?://github\.com/([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)',text)))
 existing={c['repository']:c for c in m.get('code',[])}
 for repo in repos:
  url='https://github.com/'+repo
  if url in existing and existing[url]['status']=='downloaded': continue
  target=p.parent/'code'/repo.replace('/','--');target.mkdir(parents=True,exist_ok=True)
  cap=150_000_000 if repo.startswith(('allenai/','MoonshotAI/')) else 30_000_000
  status=fetch(f'https://codeload.github.com/{repo}/zip/HEAD',target/'repository.zip',cap)
  status.update(repository=url,discovered_in='LaTeX source',role='paper-linked repository; inspect role before reproduction')
  existing[url]=status
 m['code']=list(existing.values())
 if m['code']:m.pop('code_status',None)
 p.write_text(json.dumps(m,indent=2)+'\n');print(p.parent.name,flush=True)
with ThreadPoolExecutor(max_workers=3) as pool:list(pool.map(collect,paths))

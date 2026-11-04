"""Select a deterministic small shard manifest from the downloaded public CC index.
This creates a URL list; it never downloads corpus objects.
"""
from pathlib import Path
import argparse,hashlib,json
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--index',default=str(ROOT/'configs/data/nemotron-cc-index/objects.jsonl'));p.add_argument('--quality',required=True,choices=['high','medium-high','medium','medium-low','low']);p.add_argument('--kind',default='actual',choices=['actual','synthetic']);p.add_argument('--kind2');p.add_argument('--count',type=int,default=4);p.add_argument('--seed',default='hero-v0');p.add_argument('--output',required=True)
a=p.parse_args();rows=[json.loads(x) for x in Path(a.index).read_text().splitlines()]
rows=[r for r in rows if r['quality']==a.quality and r['kind']==a.kind and (not a.kind2 or r['kind2']==a.kind2)]
rows.sort(key=lambda r:hashlib.sha256((a.seed+r['url']).encode()).hexdigest())
if len(rows)<a.count:raise SystemExit(f'Only {len(rows)} matching objects; requested {a.count}')
out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(''.join(json.dumps(r)+'\n' for r in rows[:a.count]))
out.with_suffix('.urls').write_text(''.join(r['url']+'\n' for r in rows[:a.count]))
print(f'Selected {a.count} objects. Corpus downloaded: none. URL list: {out.with_suffix(".urls")}')

"""Fetch the small public Nemotron-CC object index, not the multi-TB corpus.
Outputs shard URLs grouped by the upstream quality/kind partitions.
"""
import argparse,collections,gzip,hashlib,json,urllib.parse,datetime
from pathlib import Path
import requests
ROOT=Path(__file__).resolve().parents[1]
PAGE='https://data.commoncrawl.org/contrib/Nemotron/Nemotron-CC/index.html'
def main():
 p=argparse.ArgumentParser();p.add_argument('--output-dir',default=str(ROOT/'configs/data/nemotron-cc-index'));a=p.parse_args()
 out=Path(a.output_dir);out.mkdir(parents=True,exist_ok=True)
 from bs4 import BeautifulSoup
 r=requests.get(PAGE,timeout=60);r.raise_for_status();s=BeautifulSoup(r.text,'html.parser')
 href=next(x['href'] for x in s.select('a[href]') if x.get_text(strip=True)=='data-jsonl.paths.gz')
 url=urllib.parse.urljoin(PAGE,href)
 z=requests.get(url,timeout=60);z.raise_for_status();(out/'data-jsonl.paths.gz').write_bytes(z.content)
 text=gzip.decompress(z.content).decode();rows=[];counts=collections.Counter()
 for line in text.splitlines():
  path=line.strip()
  if not path:continue
  parts=dict(t.split('=',1) for t in path.split('/') if '=' in t)
  row={'url':path if path.startswith('https://') else 'https://data.commoncrawl.org/'+path.lstrip('/'),'quality':parts.get('quality'),'kind':parts.get('kind'),'kind2':parts.get('kind2')}
  rows.append(row);counts[(row['quality'],row['kind'],row['kind2'])]+=1
 (out/'objects.jsonl').write_text(''.join(json.dumps(row)+'\n' for row in rows))
 summary={'source':PAGE,'index_url':url,'retrieved_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'index_sha256':hashlib.sha256(z.content).hexdigest(),'object_count':len(rows),'downloaded_corpus_objects':0,'partitions':[{'quality':k[0],'kind':k[1],'kind2':k[2],'objects':v} for k,v in sorted(counts.items(),key=lambda kv:str(kv[0]))]}
 (out/'snapshot.json').write_text(json.dumps(summary,indent=2)+'\n')
 print(json.dumps(summary,indent=2))
if __name__=='__main__':main()

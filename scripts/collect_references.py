"""Collect one reference per directory, preserving provenance and failures. Run from repo root."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse
import datetime, gzip, io, json, re, shutil, subprocess, tarfile, requests
ROOT=Path(__file__).resolve().parents[1]
REF=ROOT/'references'
DATE=datetime.datetime.now(datetime.timezone.utc).isoformat()

def fetch(url, target, limit=100_000_000):
    if target.exists(): return {'status':'downloaded','url':url,'bytes':target.stat().st_size}
    try:
        with requests.get(url,timeout=(15,60),stream=True,headers={'User-Agent':'ScalingLadderReferenceCollector/1.0'}) as r:
            r.raise_for_status(); data=bytearray()
            for chunk in r.iter_content(65536):
                data.extend(chunk)
                if len(data)>limit: raise ValueError(f'exceeds {limit} byte collection limit')
            target.write_bytes(data)
            return {'status':'downloaded','url':url,'resolved_url':r.url,'bytes':len(data)}
    except Exception as e:
        return {'status':'unavailable','url':url,'reason':str(e)}

def collect(pdf):
    folder=pdf.parent if pdf.name=='paper.pdf' else REF/pdf.stem
    prior=json.loads((folder/'metadata.json').read_text()) if (folder/'metadata.json').exists() else {}
    aid=prior.get('id',pdf.stem if pdf.name!='paper.pdf' else folder.name)
    folder.mkdir(exist_ok=True)
    dst=folder/'paper.pdf'
    if pdf!=dst: shutil.move(str(pdf),dst)
    meta={**prior,'id':aid,'retrieved_at':DATE,'pdf':'paper.pdf','url':f'https://arxiv.org/abs/{aid}'}
    if aid.startswith('OLMo-'): meta['url']='https://allenai.org/papers/olmocore3'
    archive=folder/'arxiv-source.tar'
    if not aid.startswith('OLMo-'):
        meta['latex_source']=fetch(f'https://arxiv.org/src/{aid}',archive)
        if meta['latex_source']['status']=='downloaded':
            try:
                data=archive.read_bytes()
                if data.startswith(b'%PDF') or data.lstrip().startswith((b'<!DOCTYPE',b'<html')): raise ValueError('source endpoint returned PDF or HTML, not LaTeX source')
                source=folder/'source'; source.mkdir(exist_ok=True)
                if tarfile.is_tarfile(archive):
                    with tarfile.open(archive) as tf:
                        size=0
                        for m in tf.getmembers():
                            p=Path(m.name)
                            if m.isfile() and not p.is_absolute() and '..' not in p.parts:
                                size+=m.size
                                if size>150_000_000: raise ValueError('unpacked source exceeds size limit')
                                target=source/p; target.parent.mkdir(parents=True,exist_ok=True)
                                target.write_bytes(tf.extractfile(m).read())
                else:
                    if data.startswith(b'\x1f\x8b'): data=gzip.decompress(data)
                    if b'\\document' not in data and b'\\begin' not in data: raise ValueError('unrecognized source format')
                    (source/'main.tex').write_bytes(data)
                meta['latex_source']['tex_files']=len(list(source.rglob('*.tex')))
            except Exception as e: meta['latex_source'].update(status='unavailable',reason=str(e))
    else: meta['latex_source']={'status':'not_arxiv','reason':'Official direct PDF; no arXiv identifier established.'}
    # Find repositories explicitly linked from paper text or arXiv abstract, not guessed projects.
    text=''
    try:
        result=subprocess.run(['pdftotext','-layout',str(dst),'-'],capture_output=True,text=True,timeout=30)
        text=result.stdout
        (folder/'paper.txt').write_text(text)
    except Exception: pass
    try:
        r=requests.get(meta['url'],timeout=25); r.raise_for_status()
        if 'text/html' in r.headers.get('content-type',''): text+='\n'+r.text
    except Exception: pass
    for tex in (folder/'source').rglob('*.tex'):
        text+='\n'+tex.read_text(errors='replace')
    repos=sorted(set(re.findall(r'https?://github\.com/([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)',text)))
    repos=[r.rstrip('.') for r in repos if not r.endswith(('.png','.svg','.pdf'))]
    meta['code']=[]
    for repo in dict.fromkeys(repos):
        target=folder/'code'/repo.replace('/','--'); target.mkdir(parents=True,exist_ok=True)
        # Archives capture linked code without running or installing any of it.
        status=fetch(f'https://codeload.github.com/{repo}/zip/HEAD',target/'repository.zip',30_000_000)
        status.update(repository=f'https://github.com/{repo}',role='paper-linked repository; may be baseline, data, or evaluation code')
        meta['code'].append(status)
    if not meta['code']: meta['code_status']='No GitHub repository link discovered in PDF text or abstract; code availability is unconfirmed.'
    (folder/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
    readme=f'# {aid}\n\nSource: {meta["url"]}\n\n- [PDF](paper.pdf)\n- [Metadata and download status](metadata.json)\n'
    if (folder/'source').exists(): readme+='- LaTeX and other source files: `source/`\n'
    readme+='\nLinked code archives are stored under `code/`. Repository links may refer to dependencies or baselines; their presence does not establish that the experiment is reproducible. Download errors and source availability are recorded in metadata.\n'
    (folder/'README.md').write_text(readme)
    print(aid,meta['latex_source']['status'],len(meta['code']),flush=True)
    return meta

if __name__=='__main__':
    papers=list((REF/'papers').glob('*.pdf'))
    if not papers: papers=[p.parent/'paper.pdf' for p in REF.rglob('metadata.json') if 'id' in json.loads(p.read_text()) and (p.parent/'paper.pdf').exists()]
    with ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(collect,papers))
    # Migrate web references and preserve a one-folder-per-reference layout.
    for p in (REF/'web').glob('*.md'):
        d=REF/p.stem; d.mkdir(exist_ok=True); shutil.move(str(p),d/'article.md')
    for p in [ROOT/'references/SOURCES.md',ROOT/'references/MARIN-READING.md']:
        s=p.read_text()
        s=re.sub(r'papers/([^/)]+)\.pdf',r'\1/paper.pdf',s)
        s=re.sub(r'web/([^/)]+)\.md',r'\1/article.md',s)
        p.write_text(s)
    summary=[]
    for p in REF.rglob('metadata.json'): summary.append(json.loads(p.read_text()))
    (REF/'download-manifest.json').write_text(json.dumps(summary,indent=2)+'\n')

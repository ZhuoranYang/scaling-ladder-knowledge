#!/usr/bin/env python3
"""Query, inspect, index and validate the pretraining knowledge base.

The query/get/status commands use the committed index and Python stdlib only.
Generation and validation require PyYAML; no service credentials are needed.
"""
import argparse
import ast
from collections import Counter, defaultdict
from datetime import date
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import unicodedata
from urllib.parse import unquote, urlsplit

ROOT=Path(__file__).resolve().parents[1]
K=ROOT/'knowledge'
EXPECTED_QUESTIONS={'hero-compute','data-supply','bucket-reproduction','width-depth',
                    'optimizer-search','fit-identifiability','evaluation',
                    'long-context','posttraining','cyber-extension'}


def read_json(path):
    return json.loads((ROOT/path).read_text())


def yaml_read(text):
    try:
        import yaml
    except ImportError as exc:
        raise RuntimeError('Install PyYAML to generate or validate: pip install -r scripts/requirements-kb.txt') from exc
    return yaml.safe_load(text)


def frontmatter(path):
    text=path.read_text()
    match=re.match(r'^---\n(.*?)\n---\n(.*)',text,re.S)
    if not match:raise ValueError(f'{path.relative_to(ROOT)}: missing YAML frontmatter')
    meta=yaml_read(match[1])
    if not isinstance(meta,dict):raise ValueError(f'{path}: frontmatter must be a mapping')
    return meta,match[2]


def load_pages():
    pages=[]
    for folder in ['sources','wiki']:
        for path in sorted((ROOT/folder).rglob('*.md')):
            meta,body=frontmatter(path)
            pages.append({**meta,'path':path.relative_to(ROOT).as_posix(),'body':body})
    # Retained long-form guides are searchable but are explicitly not promoted
    # to schema-reviewed canonical wiki pages by discovery alone.
    for legacy in read_json('knowledge/legacy-guides.json')['guides']:
        path=ROOT/legacy['path'];text=path.read_text()
        pages.append({**legacy,'body':re.sub(r'^---\n.*?\n---\n','',text,count=1,flags=re.S)})
    return pages


def normalized(value):
    return unicodedata.normalize('NFKC',value).casefold().strip()


def canonical(term,aliases):
    for key,values in aliases.items():
        if normalized(term) in {normalized(v) for v in [key,*values]}:return key
    return term


def query_pages(pages,text='',tag=None,kind=None,architecture=None,confidence=None,limit=10,aliases=None):
    aliases=aliases or {};terms=[normalized(t) for t in text.split()]
    for key,values in aliases.items():
        if any(normalized(v) in normalized(text) for v in [key,*values]):terms.append(normalized(key))
    ranked=[]
    for page in pages:
        if tag and canonical(tag,aliases) not in page.get('tags',[]):continue
        if kind and kind not in [page['type'],page['type'].split('-',1)[-1]]:continue
        if architecture and architecture not in page.get('architectures',[]):continue
        if confidence and confidence!=page.get('confidence'):continue
        title=normalized(page['title']);tags=' '.join(page.get('tags',[]));body=normalized(page.get('body',''))
        score=sum(10*(t in title)+6*(t in tags)+min(body.count(t),3) for t in set(terms))
        if terms and not score:continue
        ranked.append((score,page))
    ranked.sort(key=lambda item:(-item[0],item[1]['id']))
    return [p for _,p in ranked[:limit]]


def resolve_pointer(data,pointer):
    for part in pointer.lstrip('/').split('/'):
        part=part.replace('~1','/').replace('~0','~')
        data=data[int(part)] if isinstance(data,list) else data[part]
    return data


def validate(pages,claims,versions,questions,schema,vocabulary,aliases,verify_artifacts=False,preserve=True):
    errors=[];by_id={};seen_aliases={}
    allowed_tags=set(vocabulary['tags'])
    for key,values in aliases.items():
        if key not in allowed_tags:errors.append(f'alias canonical term is not a controlled tag: {key}')
        for value in [key,*values]:
            n=normalized(value)
            if n in seen_aliases and seen_aliases[n]!=key:errors.append(f'ambiguous alias {value}')
            seen_aliases[n]=key
    for p in pages:
        sid=p.get('id')
        if not sid or sid in by_id:errors.append(f'missing/duplicate ID {sid}');continue
        by_id[sid]=p
        if not (ROOT/p['path']).is_file():errors.append(f'{sid}: missing page file')
        for link in re.findall(r'\]\(([^)]+)\)',p.get('body','')):
            parsed=urlsplit(link.strip('<>'))
            if parsed.scheme or parsed.netloc or not parsed.path:continue
            target=(ROOT/p['path']).parent/unquote(parsed.path)
            if not target.exists():errors.append(f'{sid}: broken Markdown link {link}')
        if p['type']=='guide':continue
        if not re.fullmatch('[a-z][a-z0-9-]*',sid):errors.append(f'{sid}: invalid stable ID syntax')
        kind=schema['page_types'].get(p.get('type'))
        if not kind:errors.append(f'{sid}: unknown page type {p.get("type")}');continue
        if not sid.startswith(kind['prefix']):errors.append(f'{sid}: wrong ID prefix')
        for field in schema['common_required']+kind['required']:
            if field not in p:errors.append(f'{sid}: missing {field}')
        if not isinstance(p.get('tags'),list) or any(t not in allowed_tags for t in p.get('tags',[])):
            errors.append(f'{sid}: unknown tags')
        if any(a not in vocabulary['architectures'] for a in p.get('architectures',[])):
            errors.append(f'{sid}: unknown architecture')
        if p['type'].startswith('wiki-'):
            if p.get('confidence') not in schema['confidence']:errors.append(f'{sid}: invalid confidence')
            level=p.get('reproducibility')
            if level not in schema['reproducibility']:errors.append(f'{sid}: invalid reproducibility')
            minimum=kind.get('min_reproducibility')
            if minimum and level in schema['reproducibility'] and schema['reproducibility'].index(level)<schema['reproducibility'].index(minimum):
                errors.append(f'{sid}: requires at least {minimum}')
            if minimum and not p.get('code_examples'):errors.append(f'{sid}: requires actual code examples')
            if not p.get('reproducibility_scope'):errors.append(f'{sid}: reproduction scope must be explicit')
            if p.get('confidence')=='verified':
                basis=p.get('evidence_basis',{})
                for field in schema['verified_requires']:
                    if not basis.get(field):errors.append(f'{sid}: verified requires {field} evidence')
            if level=='benchmarked' and not p.get('benchmark_receipt'):errors.append(f'{sid}: benchmarked requires receipt')
            for example in p.get('code_examples',[]):
                file=ROOT/example['path']
                if not file.is_file():errors.append(f'{sid}: code example missing');continue
                if file.suffix=='.py':
                    try:
                        tree=ast.parse(file.read_text())
                        names={node.name for node in ast.walk(tree) if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))}
                        if example.get('symbol') and example['symbol'] not in names:errors.append(f'{sid}: code example symbol missing')
                    except SyntaxError:errors.append(f'{sid}: invalid Python example')
        if p['type']=='source-pr':
            if not re.fullmatch('[a-f0-9]{40}',p.get('head_sha','')):errors.append(f'{sid}: invalid PR head pin')
            if not isinstance(p.get('merged'),bool):errors.append(f'{sid}: merged must be explicit boolean')
            for item in p.get('local_artifacts',[]):
                if item.get('role')=='pr-snapshot':
                    snapshot=read_json(item['path'])
                    captured=next((x['result'] for x in snapshot['prs'] if x['number']==p['pr']),None)
                    if not captured or any(p.get(k)!=captured.get(k) for k in ['head_sha','merged']) or p['status']!=captured['state']:
                        errors.append(f'{sid}: PR card differs from captured source status/head')
        for artifact in p.get('local_artifacts',[]):
            path=ROOT/artifact['path']
            if not path.resolve().is_relative_to(ROOT.resolve()):errors.append(f'{sid}: artifact escapes repository');continue
            if not path.is_file():errors.append(f'{sid}: missing artifact {artifact["path"]}')
            elif verify_artifacts and hashlib.sha256(path.read_bytes()).hexdigest()!=artifact['sha256']:
                errors.append(f'{sid}: artifact hash mismatch {artifact["path"]}')
    claim_map={c['id']:c for c in claims}
    if len(claim_map)!=len(claims):errors.append('duplicate claim IDs')
    version_map={v['id']:v for v in versions}
    for c in claims:
        cid=c['id']
        for field in schema['claim_required']:
            if field not in c:errors.append(f'{cid}: missing {field}')
        if c.get('kind') not in schema['claim_kinds']:errors.append(f'{cid}: invalid claim kind')
        for field in schema['claim_scope_required']:
            if not c.get('scope',{}).get(field):errors.append(f'{cid}: missing scope {field}')
        if not c.get('limitations'):errors.append(f'{cid}: requires explicit limitations')
        for sid in c.get('sources',[]):
            if sid not in by_id or not by_id[sid]['type'].startswith('source-'):errors.append(f'{cid}: missing source {sid}')
        for loc in c.get('locators',[]):
            if loc.get('source_id') not in c['sources'] or not loc.get('locator'):errors.append(f'{cid}: invalid locator')
        if c['kind']=='reported_measurement' and (not c.get('measurements') or not c.get('comparison')):
            errors.append(f'{cid}: reported result needs measurements/comparison context')
        for m in c.get('measurements',[]):
            if not all(k in m for k in ['metric','value','unit']):errors.append(f'{cid}: incomplete measurement')
        for vid in c.get('versions',[]):
            if vid not in version_map or cid not in version_map[vid]['claims']:errors.append(f'{cid}: version backreference missing {vid}')
        verification=c.get('verification',{})
        if verification.get('level') not in schema['verification']:errors.append(f'{cid}: invalid verification level')
        if verification.get('level')=='training_reproduced':
            errors.append(f'{cid}: no accepted GPU training reproduction contract exists yet')
        if verification.get('level')=='cpu_replayed':
            receipt_path=verification.get('receipt')
            if not receipt_path or not (ROOT/receipt_path).exists():errors.append(f'{cid}: CPU replay needs a receipt')
            else:
                receipt=read_json(receipt_path)
                script_hash=hashlib.sha256((ROOT/'scripts/kb_workbench.py').read_bytes()).hexdigest()
                if receipt.get('script_sha256')!=script_hash:errors.append(f'{cid}: replay code changed')
                for check in verification.get('result_checks',[]):
                    try:
                        if resolve_pointer(receipt,check['pointer'])!=check['equals']:errors.append(f'{cid}: receipt result mismatch')
                    except (KeyError,IndexError,TypeError):errors.append(f'{cid}: invalid receipt result pointer')
                for inp in receipt.get('inputs',[]):
                    path=ROOT/inp['path']
                    if not path.is_file() or (verify_artifacts and hashlib.sha256(path.read_bytes()).hexdigest()!=inp['sha256']):errors.append(f'{cid}: replay input changed')
    for v in versions:
        for cid in v['claims']:
            if cid not in claim_map or v['id'] not in claim_map[cid]['versions']:errors.append(f'{v["id"]}: claim backreference missing {cid}')
    for p in pages:
        for field in ['sources','related','prerequisites','candidate_techniques']:
            for sid in p.get(field,[]):
                if sid not in by_id:errors.append(f'{p["id"]}: unresolved {field} ID {sid}')
        for cid in p.get('claims',[]):
            if cid not in claim_map:errors.append(f'{p["id"]}: unresolved claim {cid}')
            elif any(s not in p.get('sources',[]) for s in claim_map[cid]['sources']):errors.append(f'{p["id"]}: claim sources absent from page sources for {cid}')
            if cid in claim_map and any(v not in p.get('version_sensitive',[]) for v in claim_map[cid]['versions']):
                errors.append(f'{p["id"]}: missing page version pointer for {cid}')
        for vid in p.get('version_sensitive',[]):
            if vid not in version_map:errors.append(f'{p["id"]}: unknown version-sensitive context {vid}')
        if p.get('confidence')=='verified':
            basis=p.get('evidence_basis',{})
            for field in schema['verified_requires']:
                for sid in basis.get(field,[]):
                    source=by_id.get(sid,{})
                    if sid not in p.get('sources',[]):errors.append(f'{p["id"]}: evidence basis is not in page sources')
                    official=source.get('source_category') in ['paper','official-doc','team-report']
                    implementation=source.get('source_category')=='upstream-code' and any(a['role'] in ['code','upstream-code'] for a in source.get('local_artifacts',[]))
                    if (field=='official_sources' and not official) or (field=='upstream_code' and not implementation):
                        errors.append(f'{p["id"]}: wrong evidence category for {field}')
        for perf in p.get('performance_claims',[]):
            for field in schema['performance_required']:
                if field not in perf:errors.append(f'{p["id"]}: performance claim missing {field}')
            c=claim_map.get(perf.get('claim_id'))
            if not c or perf.get('source_id') not in c['sources']:errors.append(f'{p["id"]}: unbound performance evidence')
            elif not any(m['metric']==perf.get('metric') and m['value']==perf.get('value') and m['unit']==perf.get('unit') for m in c['measurements']):errors.append(f'{p["id"]}: performance value differs from registered claim')
    visiting=set();visited=set()
    def visit(sid):
        if sid in visiting:errors.append(f'prerequisite cycle at {sid}');return
        if sid in visited:return
        visiting.add(sid)
        for target in by_id.get(sid,{}).get('prerequisites',[]):visit(target)
        visiting.remove(sid);visited.add(sid)
    for sid in by_id:visit(sid)
    qids={q['id'] for q in questions}
    if qids!=EXPECTED_QUESTIONS:errors.append(f'core question roster changed: {sorted(qids^EXPECTED_QUESTIONS)}')
    for q in questions:
        if not q.get('pages') or not q.get('claims'):errors.append(f'{q["id"]}: missing answer contract')
        for sid in q.get('pages',[]):
            if sid not in by_id:errors.append(f'{q["id"]}: unresolved answer page {sid}')
        for cid in q.get('claims',[]):
            if cid not in claim_map:errors.append(f'{q["id"]}: missing evidence claim {cid}')
        if q.get('status') in ['conditional','open'] and not q.get('gaps'):errors.append(f'{q["id"]}: undisclosed open inputs')
    if preserve:
        baseline=read_json('knowledge/literature-baseline.json')
        tracked={}
        output=subprocess.check_output(['git','ls-files','-s','--','references'],cwd=ROOT,text=True)
        for line in output.splitlines():
            left,path=line.split('\t',1);tracked[path]=left.split()[1]
        changed=set(subprocess.check_output(['git','diff','--name-only','--','references'],cwd=ROOT,text=True).splitlines())
        for entry in baseline['files']:
            path=entry['path']
            if not (ROOT/path).is_file():errors.append(f'original literature removed: {path}')
            if entry['git_blob'] and (tracked.get(path)!=entry['git_blob'] or path in changed):errors.append(f'original primary artifact changed: {path}')
    return errors


def status(pages,claims,versions):
    return {'pages_by_type':dict(sorted(Counter(p['type'] for p in pages).items())),
            'canonical_wiki_pages':sum(p['type'].startswith('wiki-') for p in pages),
            'legacy_guides_catalogued':sum(p['type']=='guide' for p in pages),
            'claims_by_kind':dict(sorted(Counter(c['kind'] for c in claims).items())),
            'claims_by_verification':dict(sorted(Counter(c['verification']['level'] for c in claims).items())),
            'expired_version_contexts':[v['id'] for v in versions if v['review_due']<date.today().isoformat()],
            'training_reproductions':sum(c['verification']['level']=='training_reproduced' for c in claims),
            'scope_note':'Cataloguing is not semantic review; CPU replay is not model-training reproduction.'}


def relative_link(path,from_file):
    return Path(os.path.relpath(path,Path(from_file).parent)).as_posix()


def generated_files(pages,claims,versions,questions,aliases):
    by_id={p['id']:p for p in pages};out={}
    clean=[{k:v for k,v in p.items() if k!='body'} for p in pages]
    out['knowledge/index.json']=json.dumps({'schema_version':1,'pages':clean,'claims':claims,'versions':versions,'aliases':aliases,'questions':questions},indent=2,ensure_ascii=False)+'\n'
    out['knowledge/source-map.json']=json.dumps({p['id']:p['path'] for p in pages if p['type'].startswith('source-')},indent=2)+'\n'
    def link(p,where):return f'[{p["title"]}](<{relative_link(p["path"],where)}>)'
    groups={
      'by-topic':lambda p:p.get('tags',[]),
      'by-stage':lambda p:[t for t in p.get('tags',[]) if t in ['data','architecture','optimization','scaling','evaluation','systems','midtraining','posttraining','governance']],
      'by-source':lambda p:p.get('sources',[]) if p['type'].startswith('wiki-') else [],
      'by-reproducibility':lambda p:[p['reproducibility']] if p['type'].startswith('wiki-') else [],
      'by-architecture':lambda p:p.get('architectures',[]) if p['type'].startswith('wiki-') else [],
      'by-evidence':lambda p:[c['kind'] for c in claims if c['id'] in p.get('claims',[])] if p['type'].startswith('wiki-') else []}
    for name,key in groups.items():
        path=f'queries/{name}.md';buckets=defaultdict(list)
        for p in pages:
            if p['type'].startswith('source-'):continue
            for value in set(key(p)):buckets[value].append(p)
        lines=['---',f'title: "Knowledge index: {name[3:]}"','---','','Generated by `python scripts/kb.py generate-indices`. Tags and architecture labels describe discussion scope; they do not establish measured transfer.','']
        if name=='by-source':
            lines+=['## Complete structured-source inventory','','All source cards are listed, including those not yet linked to a canonical synthesis. Downloaded literature remains in its original library folders.','','| Source | Kind | Linked canonical pages |','|---|---|---:|']
            for source in sorted((p for p in pages if p['type'].startswith('source-')),key=lambda p:p['id']):
                lines.append(f'| {link(source,path)} | `{source["type"]}` | {len(buckets.get(source["id"],[]))} |')
            lines.append('')
        for value,members in sorted(buckets.items()):
            label=by_id[value]['title'] if value in by_id else value
            lines+=['## '+label,'']
            for p in sorted(members,key=lambda p:p['id']):lines.append('- '+link(p,path)+f' — `{p["id"]}`; '+p.get('confidence','catalogued companion guide')+'.')
            lines.append('')
        out[path]='\n'.join(lines)
    path='queries/by-problem.md';lines=['---','title: "Knowledge index: team questions and open inputs"','---','','A documented answer does not certify the target hero recipe. Conditional questions expose the missing data, measurements or access.','']
    for q in questions:
        lines+=['## '+q['question'],'',f'Contract `{q["id"]}` · status **{q["status"]}**.','']
        lines.extend('- '+link(by_id[sid],path) for sid in q['pages']);lines+=['','Evidence: '+', '.join('`'+cid+'`' for cid in q['claims'])+'.','']
        if q.get('gaps'):lines+=['Remaining inputs: '+q['gaps'],'']
    out[path]='\n'.join(lines)
    # Preserve hand-authored metadata while generating these three page bodies.
    def yaml_page(path,body):
        text=(ROOT/path).read_text();header=text.split('\n---\n',1)[0]
        out[path]=header+'\n---\n\n'+body
    path='wiki/governance/claim-ledger.md';lines=['## Claim-level evidence ledger','','Each entry is scoped. `source_read` means inspected source evidence; `cpu_replayed` means only the named receipt was regenerated locally. No GPU training reproduction is claimed.','']
    for c in claims:
        lines += [f'## {c["id"]}','','**'+c['statement']+'**','',f'Kind: `{c["kind"]}` · verification: `{c["verification"]["level"]}`.','',
                  'Scope: '+'; '.join(f'{k}: {v}' for k,v in c['scope'].items())+'.','','Evidence: '+', '.join(link(by_id[sid],path) for sid in c['sources'])+'.','']
        lines += ['Locator: '+'; '.join(l['locator'] for l in c['locators'])+'.','','Limit: '+c['limitations'],'']
        if c['verification'].get('receipt'):lines+=['[CPU receipt](<'+relative_link(c['verification']['receipt'],path)+'>).','']
    yaml_page(path,'\n'.join(lines))
    path='wiki/governance/coverage.md';s=status(pages,claims,versions)
    body='## Current coverage, with explicit limits\n\nThe original library is retained. Structured pages and claim records are a new layer; old guides remain searchable companions. This is an initial reviewed slice, not a claim of KernelWiki-wide audit parity.\n\n'
    body+='| Quantity | Count |\n|---|---:|\n'+''.join(f'| {k} | {v} |\n' for k,v in s['pages_by_type'].items())
    body+='\n## Claim verification\n\n'+''.join(f'- `{k}`: {v} claims.\n' for k,v in s['claims_by_verification'].items())
    body+='\n**GPU training reproductions: 0.** Seven CPU recipes check public observations/configuration arithmetic or analytical fixtures; they do not reproduce Marin training.\n\n## Next scientific work\n\n1. Materialize one accessible, pinned real-source subset and qualify normalization, dedup/decon and scorer compatibility.\n2. Qualify one trainer/optimizer/evaluator on intended hardware, then measure throughput and resume parity.\n3. Run matched mixture/HP controls with seed handling and a predeclared larger holdout.\n4. Add semantic claim coverage to OLMo/Nemotron/Kimi guides and source-specific trainer/eval contracts.\n5. Treat cyber transfer, recurrence and very-long-context choices as conditional experiments.\n\n## Version-sensitive contexts\n\n| Context | Frozen version | Checked | Review due |\n|---|---|---|---|\n'
    body+=''.join(f'| {v["id"]} | `{v["version"]}` | {v["checked_at"]} | {v["review_due"]} |\n' for v in versions)
    body+='\nDates are review reminders, not proof that upstream remains unchanged. Refresh by appending a new snapshot and evaluating affected claims.\n'
    yaml_page(path,body)
    path='wiki/foundations/topic-map.md';lines=['## Navigate from the decision','','![The evidence-to-hero decision workflow, with data and optimizer experiments feeding fixed evaluation and an independent larger holdout.](../assets/pretraining-workflow.svg)','','[Editable Mermaid source](../assets/pretraining-workflow.mmd). The SVG is a derived navigation figure, not an empirical result.','','## Canonical pages','']
    for p in pages:
        if p['type'].startswith('wiki-') and p['id']!='foundation-topic-map':lines.append('- '+link(p,path)+' — `'+p['reproducibility']+'`; '+p['reproducibility_scope']+'.')
    lines+=['','## Literature and companion guides','','The [full literature catalogue](../../references/SOURCES.md) retains PDFs/LaTeX/code. [Long-form guides](../../doc/index.qmd) explain the original blog and team efforts. [Question contracts](../../queries/by-problem.md) expose unanswered inputs.','']
    yaml_page(path,'\n'.join(lines))
    return out


def current_data():
    return (load_pages(),read_json('knowledge/claims.json')['claims'],read_json('knowledge/version-claims.json')['versions'],
            read_json('knowledge/questions.json')['questions'],yaml_read((K/'schemas.yaml').read_text()),
            yaml_read((K/'tags.yaml').read_text()),yaml_read((K/'aliases.yaml').read_text()))


def validate_pdf_manifest(manifest=None,verify_artifacts=False):
    errors=[]
    if manifest is None:manifest=read_json('pdf/manifest.json')
    config=yaml_read((ROOT/'_quarto.yml').read_text())
    expected={p.relative_to(ROOT).as_posix() for pattern in config['project']['render'] for p in ROOT.glob(pattern.lstrip('/'))}
    actual={d['source'] for d in manifest['documents']}
    if actual!=expected:errors.append('PDF manifest does not cover the configured authored pages')
    renderer=hashlib.sha256((ROOT/'scripts/render_pdfs.py').read_bytes()).hexdigest()
    if manifest.get('renderer_sha256')!=renderer:errors.append('PDF renderer changed; regenerate PDFs')
    for d in manifest['documents']:
        source=ROOT/d['source'];pdf=ROOT/d['pdf']
        if not source.is_file() or hashlib.sha256(source.read_bytes()).hexdigest()!=d.get('source_sha256'):
            errors.append(f'PDF source is stale: {d["source"]}')
        if not pdf.is_file() or (verify_artifacts and hashlib.sha256(pdf.read_bytes()).hexdigest()!=d['sha256']):
            errors.append(f'PDF artifact is missing/changed: {d["pdf"]}')
    return errors


def main():
    parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='command',required=True)
    q=sub.add_parser('query');q.add_argument('text',nargs='?',default='');q.add_argument('--tag');q.add_argument('--type');q.add_argument('--architecture');q.add_argument('--confidence');q.add_argument('--limit',type=int,default=10);q.add_argument('--json',action='store_true')
    g=sub.add_parser('get');g.add_argument('id');g.add_argument('--follow-sources',action='store_true')
    c=sub.add_parser('claim');c.add_argument('id')
    sub.add_parser('questions');st=sub.add_parser('status');st.add_argument('--json',action='store_true')
    sub.add_parser('generate-indices')
    v=sub.add_parser('validate');v.add_argument('--verify-artifacts',action='store_true');v.add_argument('--check-generated',action='store_true')
    args=parser.parse_args()
    if args.command in ['query','get','claim','questions','status']:
        data=read_json('knowledge/index.json');pages=data['pages'];claims=data['claims'];versions=data['versions']
        if args.command=='query':
            for p in pages:p['body']=(ROOT/p['path']).read_text()
            found=query_pages(pages,args.text,args.tag,args.type,args.architecture,args.confidence,args.limit,data['aliases'])
            for p in found:p.pop('body',None)
            print(json.dumps(found,indent=2,ensure_ascii=False) if args.json else '\n'.join(f'{p["id"]}\t{p["title"]}\t{p["path"]}\t{p.get("confidence","catalogued")}' for p in found))
        elif args.command=='get':
            p=next((p for p in pages if args.id in [p['id'],p['path']]),None)
            if p is None:raise ValueError(f'Unknown page: {args.id}')
            print((ROOT/p['path']).read_text())
            if args.follow_sources:
                ids=set(p.get('sources',[]))
                for claim in claims:
                    if claim['id'] in p.get('claims',[]):ids.update(claim['sources'])
                for s in pages:
                    if s['id'] in ids:print('\nSOURCE '+s['id']+'\n'+json.dumps(s,indent=2,ensure_ascii=False))
        elif args.command=='claim':
            found=next((c for c in claims if c['id']==args.id),None)
            if found is None:raise ValueError(f'Unknown claim: {args.id}')
            print(json.dumps(found,indent=2,ensure_ascii=False))
        elif args.command=='questions':print(json.dumps(data['questions'],indent=2,ensure_ascii=False))
        else:print(json.dumps(status(pages,claims,versions),indent=2,ensure_ascii=False))
        return
    pages,claims,versions,questions,schema,vocabulary,aliases=current_data()
    outputs=generated_files(pages,claims,versions,questions,aliases)
    if args.command=='generate-indices':
        for path,text in outputs.items():
            (ROOT/path).parent.mkdir(parents=True,exist_ok=True);(ROOT/path).write_text(text)
        print(f'Generated {len(outputs)} index/registry views for {len(pages)} pages and {len(claims)} claims')
    else:
        errors=validate(pages,claims,versions,questions,schema,vocabulary,aliases,args.verify_artifacts)
        if args.check_generated:
            for path,text in outputs.items():
                if not (ROOT/path).is_file() or (ROOT/path).read_text()!=text:errors.append(f'stale generated index: {path}')
            errors.extend(validate_pdf_manifest(verify_artifacts=args.verify_artifacts))
        if errors:
            print('\n'.join(errors));raise SystemExit(1)
        print(f'PASS: {len(pages)} pages; {len(claims)} scoped claims; {len(questions)} question contracts; literature preserved.')


if __name__=='__main__':
    try:main()
    except (ValueError,KeyError,RuntimeError) as exc:
        print(str(exc),file=sys.stderr);raise SystemExit(2)

#!/usr/bin/env python3
"""Download small, pinned public HF artifacts; never download model weights."""
import hashlib
import json
from pathlib import Path
import shutil
import posixpath
import subprocess
from concurrent.futures import ThreadPoolExecutor
import requests

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'references/marin/2026-marin-code-data-evaluation-evidence'
DATE = '2026-11-04'
MODEL_PINS = {
    'marin-community/marin-8b-base': 'e1a2021fd607dfba5086e2cbe916c160d03870f1',
    'marin-community/marin-8b-instruct': '0378f9c932bd64ca189d2f2ca5bd2fb076cba61d',
    'marin-community/marin-32b-base': 'f19b346615212ff9a6d92c10861a9cdb100cbf97',
    'laion/delphi-1e22-p33m67-32p07b-lr0.67-54770ae7': '56cc5aaf65cd59d6632962cee636a0423abfbf66',
    'laion/delphi-9e19-p33m67-coldstart-magpie_lr1e5': '8be0758421b6ec928bd4d7a8fab0e8035430abb6',
}


def collect_model(repo):
    info = requests.get(f'https://huggingface.co/api/models/{repo}/revision/{MODEL_PINS[repo]}', timeout=90)
    info.raise_for_status()
    obj = info.json()
    if obj['sha'] != MODEL_PINS[repo]:
        raise ValueError(f'Model revision mismatch for {repo}')
    dest = OUT / 'huggingface' / repo.replace('/', '--')
    dest.mkdir(parents=True, exist_ok=True)
    (dest / 'api.json').write_text(json.dumps(obj, indent=2) + '\n')
    records = []
    names = {s['rfilename'] for s in obj.get('siblings', [])}
    for name in ['README.md', 'config.json', 'generation_config.json', 'eval_results.json', 'all_results.json']:
        if name not in names:
            continue
        url = f'https://huggingface.co/{repo}/resolve/{obj["sha"]}/{name}'
        response = requests.get(url, timeout=90)
        response.raise_for_status()
        (dest / name).write_bytes(response.content)
        records.append({'url': url, 'file': str((dest/name).relative_to(ROOT)),
                        'sha256': hashlib.sha256(response.content).hexdigest(), 'bytes': len(response.content)})
    return {'repo': repo, 'revision': obj['sha'], 'retrieved_at': DATE,
            'artifacts': records, 'weights_downloaded': False}


def main():
    baseline = subprocess.check_output(['git', '-C', str(ROOT/'tmp/marin'), 'rev-parse', 'HEAD'], text=True).strip()
    if baseline != '1d274b52c636b6f2a9177b1d4c14b2f74795a8a6':
        raise ValueError('Local Marin checkout does not match the documented baseline')
    repos = list(MODEL_PINS)
    with ThreadPoolExecutor(max_workers=5) as pool:
        models = list(pool.map(collect_model, repos))
    revision = '283eacf18b66b7888b59fd8f889d6be134aee879'
    name = 'registry/v1/transfer_campaign.parquet'
    url = f'https://huggingface.co/datasets/marin-community/grug-moe-mix-swarm/resolve/{revision}/{name}'
    response = requests.get(url, timeout=120)
    response.raise_for_status()
    digest = hashlib.sha256(response.content).hexdigest()
    expected = '5ed5fb024590dd4707b802caf8fe728be1b8d73375c100139f884b0728f0cca2'
    if digest != expected:
        raise ValueError(f'campaign digest mismatch: {digest}')
    dest = OUT / 'huggingface/transfer_campaign.parquet'
    dest.write_bytes(response.content)
    # Preserve code for independently readable evaluation protocols.
    codepaths = ['experiments/datasets/paloma.py', 'experiments/datasets/uncheatable.py',
                 'experiments/grug/moe_hero_ep/launch_scaling_ladder.py',
                 'experiments/evaluation/README.md', 'experiments/evaluation/evals.py',
                 'experiments/evaluation/configs/evalchemy/mrcr.yaml',
                 'experiments/evaluation/configs/evalchemy/gsm8k.yaml',
                 'experiments/sft/configs/delphi_1e22.py',
                 'experiments/june_tpu_67b_a2b/moe/sft_67b_a2b_2stage.py',
                 'experiments/evaluation/pipeline.py', 'lib/marin/src/marin/evaluation/records.py',
                 'experiments/evaluation/configs/harbor/swebench.yaml',
                 'docs/reports/marin-32b-retro.md']
    code = []
    for path in codepaths:
        source = ROOT / 'tmp/marin' / path
        if not source.is_file():
            code.append({'path': path, 'status': 'not at requested path'})
            continue
        target = OUT / 'baseline-code' / path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        code.append({'path': path, 'status': 'downloaded', 'sha256': hashlib.sha256(target.read_bytes()).hexdigest()})
    audit = {'retrieved_at': DATE, 'baseline_commit': '1d274b52c636b6f2a9177b1d4c14b2f74795a8a6',
             'models': models, 'campaign': {'url': url, 'revision': revision, 'sha256': digest,
             'bytes': len(response.content), 'file': str(dest.relative_to(ROOT))}, 'baseline_code': code,
             'scope': 'Metadata, cards, small result/config files, PR evidence. No model weights or training text.'}
    import pyarrow.parquet as pq
    campaign = pq.read_table(dest).to_pylist()[0]
    materialized = {}

    def artifact(relative, expected_hash):
        if relative.startswith('/') or '..' in Path(relative).parts:
            raise ValueError(relative)
        if relative in materialized:
            return materialized[relative]['value']
        uri = f'https://huggingface.co/datasets/marin-community/grug-moe-mix-swarm/resolve/{revision}/registry/v1/{relative}'
        response = requests.get(uri, timeout=120)
        response.raise_for_status()
        digest = hashlib.sha256(response.content).hexdigest()
        if digest != expected_hash:
            raise ValueError(f'hash mismatch for {relative}')
        target = OUT / 'huggingface/campaign' / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(response.content)
        value = (pq.read_table(target).to_pylist() if relative.endswith('.parquet')
                 else json.loads(response.content) if relative.endswith('.json') else None)
        materialized[relative] = {'value': value, 'url': uri, 'sha256': digest, 'bytes': len(response.content)}
        return value

    registry = artifact(campaign['registry']['path'], campaign['registry']['sha256'])[0]
    swarms = {s['swarm_id']: s for s in registry['swarms']}
    basis_ids = set()
    for swarm_id in [campaign['target_swarm'], *campaign['source_swarms']]:
        ref = swarms[swarm_id]
        swarm = artifact(ref['path'], ref['sha256'])[0]
        parent = posixpath.dirname(ref['path'])
        for kind in ['observations', 'buckets', 'content']:
            item = swarm[kind]
            rows = artifact(posixpath.join(parent, item['path']), item['sha256'])
            if kind == 'content':
                basis_ids.add(rows[0]['basis_id'])
    bases = {b['basis_id']: b for b in registry['content_bases']}
    for basis_id in basis_ids:
        ref = bases[basis_id]
        basis = artifact(ref['path'], ref['sha256'])[0]
        item = basis['lookup']
        artifact(posixpath.join(posixpath.dirname(ref['path']), item['path']), item['sha256'])
    audit['campaign_artifacts'] = [{k:v for k,v in item.items() if k != 'value'} | {'path': path}
                                   for path,item in materialized.items()]
    ledger = OUT / 'pr-metadata.json'
    if ledger.exists():
        audit['pr_count'] = len(json.loads(ledger.read_text())['prs'])
    audit['files'] = [{'path': str(p.relative_to(OUT)), 'bytes': p.stat().st_size,
                       'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
                      for p in sorted(OUT.rglob('*'))
                      if p.is_file() and p.name not in ['audit.json', 'README.md', 'metadata.json']]
    (OUT / 'audit.json').write_text(json.dumps(audit, indent=2) + '\n')
    print(json.dumps({'models': [(m['repo'],m['revision']) for m in models], 'campaign_sha256': digest,
                      'baseline_code': code}, indent=2))


if __name__ == '__main__':
    main()

"""Archive already downloaded source trees and a pinned historical Marin recipe.
No training, dependencies, model weights or pretraining corpus are fetched.
"""
from pathlib import Path
import subprocess,json,hashlib,concurrent.futures,requests
ROOT=Path(__file__).resolve().parents[1]
DATE='2026-11-02'
def snapshot(local,folder,url,title,paths):
 repo=ROOT/'tmp'/local;dst=ROOT/'references'/folder;dst.mkdir(parents=True,exist_ok=True)
 sha=subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD'],text=True).strip()
 archive=dst/'repository.tar.gz'
 subprocess.run(['git','-C',str(repo),'archive','--format=tar.gz',f'--output={archive}',sha],check=True)
 for rel in paths:
  src=repo/rel
  if src.exists():
   out=dst/'inspected'/rel;out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(src.read_bytes())
 meta={'title':title,'topic':folder.split('/')[0],'url':url,'retrieved_at':DATE,'revision':sha,'local_checkout':f'tmp/{local}','code':[{'repository':url,'status':'downloaded','revision':sha,'archive':'repository.tar.gz','bytes':archive.stat().st_size,'sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'role':'source snapshot; no GPU qualification performed'}]}
 (dst/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
 (dst/'README.md').write_text(f'# {title}\n\nSource: {url}\n\nCommit: `{sha}`. Retrieved {DATE}.\n\n`repository.tar.gz` preserves the tracked source tree; `inspected/` contains selected files reviewed for the guides. No dependencies installed or training executed.\n')
 return {'repository':url,'revision':sha,'checkout':str(repo.relative_to(ROOT)),'reference':str(dst.relative_to(ROOT))}
def main():
 entries=[('torchtitan','systems/2026-torchtitan-training-platform','https://github.com/pytorch/torchtitan','TorchTitan: training, dataset and evaluation implementation',['README.md','run_train.sh','docs/evaluation.md','torchtitan/config/README.md','torchtitan/components/data/README.md','torchtitan/components/checkpointer/README.md','scripts/checkpoint_conversion/convert_to_hf.py','torchtitan_recipes/models/llama3.py']),('megatron-lm','systems/2026-megatron-lm-training-platform','https://github.com/NVIDIA/Megatron-LM','Megatron-LM: training, indexed data and MoE implementation',['README.md','tools/preprocess_data.py','examples/mixtral/train_mixtral_8x7b_distributed.sh','megatron/core/transformer/moe/README.md','megatron/training/training.py','examples/gptoss/README.md']),('lm-evaluation-harness','evaluation/2026-lm-evaluation-harness','https://github.com/EleutherAI/lm-evaluation-harness','Language Model Evaluation Harness: checkpoint evaluation',['README.md','docs/interface.md','docs/model_guide.md'])]
 pins=[snapshot(*x) for x in entries]
 # This repository is an additional artifact of the existing Step Law reference.
 repo=ROOT/'tmp/steplaw';dst=ROOT/'references/optimization/2025-step-law-hyperparameter-scaling';sha=subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD'],text=True).strip();target=dst/'code/step-law--steplaw';target.mkdir(parents=True,exist_ok=True);archive=target/'repository.tar.gz';subprocess.run(['git','-C',str(repo),'archive','--format=tar.gz',f'--output={archive}',sha],check=True)
 m=json.loads((dst/'metadata.json').read_text());m['code']=[{'repository':'https://github.com/step-law/steplaw','status':'downloaded','revision':sha,'archive':'code/step-law--steplaw/repository.tar.gz','role':'official project website link; fitting code and tabular loss measurements'}];m['code_status']='Official fitting code and measurements found through https://step-law.github.io/; this does not establish a complete training stack.';(dst/'metadata.json').write_text(json.dumps(m,indent=2)+'\n')
 old='64a9483cf1a928e6db97b83130d8a5d171a4aead';dst=ROOT/'references/marin/2026-marin-data-pipeline-overview/pinned-code';dst.mkdir(exist_ok=True)
 names=['lib/marin/src/marin/datakit/sources.py','lib/marin/src/marin/datakit/normalize.py','experiments/datakit/reference_pipeline.py']
 def get(n):
  u=f'https://raw.githubusercontent.com/marin-community/marin/{old}/{n}';r=requests.get(u,timeout=60);r.raise_for_status();p=dst/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(r.content);return {'path':n,'url':u,'bytes':len(r.content),'sha256':hashlib.sha256(r.content).hexdigest()}
 rows=list(concurrent.futures.ThreadPoolExecutor(3).map(get,names));(dst/'snapshot.json').write_text(json.dumps({'revision':old,'retrieved_at':DATE,'files':rows},indent=2)+'\n')
 marin_sha=subprocess.check_output(['git','-C',str(ROOT/'tmp/marin'),'rev-parse','HEAD'],text=True).strip();pins.append({'repository':'https://github.com/marin-community/marin','revision':marin_sha,'checkout':'tmp/marin','blog_data_pipeline_revision':old})
 out=ROOT/'configs/industry';out.mkdir(exist_ok=True);(out/'source-pins.json').write_text(json.dumps({'retrieved_at':DATE,'repositories':pins,'step_law_revision':sha},indent=2)+'\n');print(json.dumps(pins,indent=2))
if __name__=='__main__':main()

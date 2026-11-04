"""Candidate finite research queue; analytical ceilings, no jobs are launched."""
from pathlib import Path
import json,csv
from hero_budget import count
ROOT=Path(__file__).resolve().parents[1]
def main():
 cfg=json.loads((ROOT/'configs/industry/budget-96-h100-30d.json').read_text());hero=cfg['examples'][1]['model'];common=cfg['common'];rows=[]
 def model(w,depth=8):return {**hero,'width':w,'physical_layers':depth,'expert_hidden':w//2,'query_heads':w//64,'kv_heads':max(1,w//256)}
 def add(stage,name,m,D,knobs,seed=0):
  s=count(m,common);rows.append({'stage':stage,'run_id':name,'seed':seed,'width':m['width'],'physical_layers':m['physical_layers'],'stored_parameters':s['total_parameters'],'tokens':int(D),'tpp':D/s['total_parameters'],'flops_per_token':s['training_flops_per_token'],'gpu_days_at_250tf_90pct':D*s['training_flops_per_token']/(250e12*.9*86400),'proposed_change':knobs,'status':'planned; actual LR centers require qualified reference'})
 ref=model(512)
 for lr in [.5,1,2]:
  for batch in [.5,1,2]:add('reference_hp',f'hp-lr{lr}-b{batch}',ref,10e9,f'LR center x{lr}, token-batch center x{batch}')
 for wd in [.5,1,2]:add('reference_hp',f'wd-{wd}',ref,10e9,f'weight decay center x{wd}, finalist LR/batch')
 for lr in [.5,1,2]:add('reference_hp',f'long-lr-{lr}',ref,100e9,f'long-horizon LR center x{lr}')
 for recipe in ['proportional','proposed','no-medium-low','include-low','high-web-up','no-synthetic','code-up','math-up']:
  for seed in [0,1]:add('mixture',f'mix-{recipe}-s{seed}',ref,20e9,f'{recipe}; fixed evaluator and epoch-matched pool',seed)
 for w in [256,512,768]:
  m=model(w);s=count(m,common)
  for tpp in [100,200,300]:
   for lr in [.5,1,2]:add('transfer',f'w{w}-tpp{tpp}-lr{lr}',m,tpp*s['total_parameters'],f'predicted LR x{lr}; locally validated batch/decay')
 for w in [256,512,768]:
  m=model(w);s=count(m,common)
  for tpp in [100,300]:
   for batch in [.5,1,2]:add('transfer_batch',f'w{w}-tpp{tpp}-batch{batch}',m,tpp*s['total_parameters'],f'fitted LR law then batch bracket x{batch}; recheck coupled neighborhood')
 h=model(1024,12);hs=count(h,common)
 for lr in [.5,1,2]:add('holdout',f'fresh-depth-size-lr{lr}',h,220*hs['total_parameters'],f'unseen depth/size/horizon; predicted LR x{lr}',42)
 add('holdout','hero-shape-rehearsal',hero,5e9,'full topology and real pipeline; no long-horizon claim',43)
 out=ROOT/'configs/industry/run-matrix.csv'
 with out.open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 totals={k:sum(r['gpu_days_at_250tf_90pct'] for r in rows if r['stage']==k) for k in sorted(set(r['stage'] for r in rows))}
 ledger={'assumed_rate':250,'duty':.9,'runs':len(rows),'standalone_training_gpu_days':sum(totals.values()),'stages':totals,'engineering_reserve_gpu_days':72,'contingency_gpu_days':72,'cap_gpu_days':576,'note':'Reference centers, batch rounding and reduced proxy data manifests are pending qualification. Independent runs are charged in full; no prefix-sharing discount. Additional HPO, control-family comparisons and GPU annotation must fit the unallocated balance or replace jobs.'}
 ledger['unallocated_gpu_days']=576-ledger['standalone_training_gpu_days']-144
 (ROOT/'configs/industry/run-ledger.json').write_text(json.dumps(ledger,indent=2)+'\n');print(json.dumps(ledger,indent=2))
if __name__=='__main__':main()

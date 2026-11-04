"""Audit the downloaded, revision-pinned Marin experiment records, not training text."""
from pathlib import Path
import json,hashlib
import pyarrow.parquet as pq
ROOT=Path(__file__).resolve().parents[1];p=ROOT/'references/marin/2026-datakit-proxy-run-records'
def main():
 d=json.loads((p/'hub-api.json').read_text());tables={}
 for name in ['harrier_18t75_d768.parquet','swarm_runs.parquet']:
  t=pq.read_table(p/name);rows=t.to_pylist();summary={'rows':len(rows),'columns':t.column_names,'sha256':hashlib.sha256((p/name).read_bytes()).hexdigest()}
  for key in ['training_mode','tokenizer','phase_count','group','full_scale_token_count','phase0_token_count','phase1_token_count']:
   if key in t.column_names:summary[key]=sorted(set(str(x[key]) for x in rows))[:20]
  summary['example']={k:rows[0][k] for k in ['run_name','training_mode','full_scale_token_count','phase0_token_count','phase1_token_count','macro_bpb','n_eval_tasks'] if k in rows[0]}
  summary['phase0_weight_cells']=len(rows[0].get('phase0_weights') or {})
  if 'phase0_weights' in t.column_names:summary['phase0_weight_sums']=[min(sum((x.get('phase0_weights') or {}).values()) for x in rows),max(sum((x.get('phase0_weights') or {}).values()) for x in rows)]
  tables[name]=summary
  (p/(name+'.sample.json')).write_text(json.dumps(rows[0],indent=2,default=str)+'\n')
 result={'revision':d['sha'],'retrieved_at':'2026-11-02','tables':tables,'interpretation':'Rows are experiments, not text examples; configs overlap and must not be summed as independent experiments. Public Hub paths can evolve.'}
 (p/'audit.json').write_text(json.dumps(result,indent=2)+'\n')
 (p/'metadata.json').write_text(json.dumps({'title':'Marin Datakit released mixture experiment records: audited snapshot','topic':'marin','url':'https://huggingface.co/datasets/marin-community/grug-moe-mix-swarm','retrieved_at':'2026-11-02','revision':d['sha'],'artifact':'audit.json','note':'Mixture experiments and bucket metadata; not pretraining text'},indent=2)+'\n')
 print(json.dumps(result,indent=2))
if __name__=='__main__':main()

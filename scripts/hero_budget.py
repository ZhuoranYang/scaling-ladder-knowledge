"""Auditable analytical projections for the candidate; does not instantiate/train a model."""
import csv,json,math,argparse
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def count(m,common,attention_length=None):
 d=m['width'];n=m['physical_layers'];h=m['expert_hidden'];e=m['experts'];k=common['experts_per_token'];v=common['vocab_size'];ell=attention_length or common['sequence_length']
 assert m['query_heads']*m['head_dim']==d
 assert m['query_heads']%m['kv_heads']==0
 assert e%8==0 and k<=e
 span=round(n*m['loop_middle_fraction']);visits=n+span*(m['middle_visits']-1)
 kv=m['kv_heads']*m['head_dim']
 attn=2*d*d+2*d*kv;expert=3*d*h;router=d*e
 norms=2*d+d+kv # two pre-norm vectors plus assumed per-channel QK norm vectors
 body=n*(attn+e*expert+router+norms)+d
 total=body+2*v*d
 physical_active=n*(attn+k*expert+router+norms)+d
 executed_active=visits*(attn+k*expert+router)
 # FMA=2 FLOPs; fwd+bwd=3*fwd. Excludes recompute, optimizer, softmax and data movement.
 linear=6*executed_active;head=6*v*d;attention=6*ell*d*visits # causal triangles skipped
 return {'physical_layers':n,'executed_layers':visits,'width':d,'experts':e,'top_k':k,'total_parameters':total,'body_parameters':body,'physical_active_body':physical_active,'executed_active_matrix_equivalent':executed_active,'training_flops_per_token':linear+head+attention,'linear_flops_per_token':linear,'head_flops_per_token':head,'attention_flops_per_token':attention,'bf16_kv_bytes_per_token':2*visits*kv*2,'attention_length_assumption':ell}
def main():
 p=argparse.ArgumentParser();p.add_argument('--config',default=str(ROOT/'configs/hero-h100/candidate.json'));p.add_argument('--output-dir',default=str(ROOT/'doc/artifacts'));a=p.parse_args();cfg=json.loads(Path(a.config).read_text());hw=cfg['hardware'];common=cfg['common'];out=Path(a.output_dir);out.mkdir(parents=True,exist_ok=True)
 models={k:count(cfg[k],common) for k in ['hero_looped','hero_baseline']}
 seconds=hw['hero_days']*86400;gpu_days=hw['gpus']*hw['hero_days'];peak=hw['gpus']*seconds*hw['dense_bf16_peak_tflops_per_gpu']*1e12
 compute=hw['gpus']*seconds*hw['planning_model_tflops_per_gpu']*1e12*hw['productive_wall_fraction'];scenarios=[]
 for rate in [150,200,250,300,350]:
  c=hw['gpus']*seconds*rate*1e12*hw['productive_wall_fraction']
  scenarios.append({'model_tflops_per_gpu':rate,'useful_compute':c,'looped_tokens':c/models['hero_looped']['training_flops_per_token']})
 rows=[];core_cost=0
 for tier in cfg['ladder']:
  for family in ['loop','base']:
   hero=cfg['hero_looped' if family=='loop' else 'hero_baseline'];m={**hero,'width':tier[family+'_width'],'physical_layers':tier['layers'],'expert_hidden':tier[family+'_ffn'],'head_dim':tier[family+'_head_dim'],'kv_heads':tier[family+'_kv_heads']};m['query_heads']=m['width']//m['head_dim'];stats=count(m,common)
   horizons=tier['horizons_tokens'];charged=max(horizons)+0.2*sum(sorted(horizons)[:-1]);core_cost+=charged*stats['training_flops_per_token']
   for horizon in horizons:rows.append({'tier':tier['tier'],'family':family,'width':m['width'],'physical_layers':m['physical_layers'],'experts':m['experts'],'horizon_tokens':horizon,'flops_per_token':stats['training_flops_per_token'],'standalone_compute':horizon*stats['training_flops_per_token'],'role':'fit; outcomes not a final holdout'})
 with (out/'hero-run-matrix.csv').open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 data=[];D=cfg['training_seed']['token_horizon']
 for bucket in cfg['mixture']:
  weight=.8*bucket['phase1']+.2*bucket['phase2'];data.append({**bucket,'weighted_total_fraction':weight,'target_exposures_tokens':D*weight,'minimum_unique_tokens_for_cap':D*weight/bucket['epoch_cap']})
 assert math.isclose(sum(x['phase1'] for x in data),1) and math.isclose(sum(x['phase2'] for x in data),1)
 with (out/'hero-data-mixture.csv').open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(data[0]));w.writeheader();w.writerows(data)
 # Planning ledger; these are additional to the hero window.
 rate=hw['planning_model_tflops_per_gpu']*1e12*86400*hw['productive_wall_fraction']
 def tier_model(t,fam):
  m={**cfg['hero_looped' if fam=='loop' else 'hero_baseline'],'width':t[fam+'_width'],'physical_layers':t['layers'],'expert_hidden':t[fam+'_ffn'],'head_dim':t[fam+'_head_dim'],'kv_heads':t[fam+'_kv_heads']};m['query_heads']=m['width']//m['head_dim'];return count(m,common)
 f0=max(tier_model(cfg['ladder'][0],f)['training_flops_per_token'] for f in ['loop','base'])
 f1=max(tier_model(cfg['ladder'][1],f)['training_flops_per_token'] for f in ['loop','base'])
 ledger=[{'stage':'trainer qualification reserve','compute':None,'gpu_days':64}, {'stage':'reference LR/batch/decay search: 14 S0 + 6 S1 runs x 10B','compute':14*10e9*f0+6*10e9*f1}, {'stage':'long-horizon LR brackets: 4 S0 x 160B','compute':4*160e9*f0}, {'stage':'data screen: 8 recipes x 2 seeds x 20B','compute':16*20e9*f0}, {'stage':'shape/expert screen: 8 x 20B at S1','compute':8*20e9*f1}, {'stage':'core ladder with shared stable trunks','compute':core_cost}, {'stage':'fresh paired S1 high-TPP holdouts: 2 x 720B','compute':2*720e9*f1}, {'stage':'fresh finalist replication: 4 x 40B S1','compute':4*40e9*f1}, {'stage':'hero-shaped holdout/rehearsal: 10B','compute':10e9*models['hero_looped']['training_flops_per_token']}]
 for r in ledger:
  if r['compute'] is not None:r['gpu_days']=r['compute']/rate
 result={'assumptions':'Analytical model FLOPs, full 4096 causal context, perfect top-k utilization; not measured hardware throughput. Counts assume per-channel QK norm, untied embeddings and every-layer SwiGLU MoE.','models':models,'gpu_days':gpu_days,'dense_peak_compute':peak,'planning_useful_compute':compute,'planning_mfu':hw['planning_model_tflops_per_gpu']/hw['dense_bf16_peak_tflops_per_gpu'],'nominal_tokens':D,'stored_tpp':D/models['hero_looped']['total_parameters'],'dense_20tpp_multiple':D/(20*models['hero_looped']['total_parameters']),'nominal_required_compute':D*models['hero_looped']['training_flops_per_token'],'planning_supported_tokens':compute/models['hero_looped']['training_flops_per_token'],'scenarios':scenarios,'core_ladder_compute_with_20pct_shared_decay_branches':core_cost,'core_ladder_gpu_days_at_planning_rate':core_cost/(hw['planning_model_tflops_per_gpu']*1e12*86400*hw['productive_wall_fraction']),'mixture':data,'rd_ledger':ledger,'rd_gpu_days_planning_total':sum(r['gpu_days'] for r in ledger)}
 (out/'hero-budget.json').write_text(json.dumps(result,indent=2)+'\n')
 lines=['## Derived candidate accounting','', '| Quantity | Looped candidate | Unlooped control |','|---|---:|---:|']
 for label,key,scale in [('Unique stored parameters (B)','total_parameters',1e9),('One physical traversal active body (B)','physical_active_body',1e9),('Executed matrix-equivalent count (B)','executed_active_matrix_equivalent',1e9),('Training model FLOPs/token (G)','training_flops_per_token',1e9),('KV bytes/token in BF16','bf16_kv_bytes_per_token',1)]:
  lines.append(f'| {label} | {models["hero_looped"][key]/scale:,.3f} | {models["hero_baseline"][key]/scale:,.3f} |')
 lines+=['','These are analytical projections from the candidate JSON, not profiler measurements. FLOPs assume 4,096-token full causal contexts with skipped masked triangles, no activation recomputation or optimizer overhead, and every-layer SwiGLU MoE. Stored parameter counts assume per-channel QK norm and untied embeddings. The matrix-equivalent count is an arithmetic counter, not a unique-parameter count.','','## Throughput sensitivity','', '| Sustained model TFLOP/s/GPU | Productive compute over hero window | Supported looped tokens |','|---:|---:|---:|']
 for r in scenarios:lines.append(f'| {r["model_tflops_per_gpu"]} | {r["useful_compute"]:.3e} | {r["looped_tokens"]/1e12:.2f}T |')
 lines+=['','The scenarios use the GPU count, hero duration and productive wall-clock fraction from the selected JSON. They are capacity projections, not measured rates.','','## Proposed mixture and capacity requirements','', '| Bucket | Phase 1 | Phase 2 | Total exposures (B tokens) | Epoch cap | Minimum unique pool (B tokens) |','|---|---:|---:|---:|---:|---:|']
 for r in data:lines.append(f'| {r["bucket"]} | {100*r["phase1"]:.0f}% | {100*r["phase2"]:.0f}% | {r["target_exposures_tokens"]/1e9:.1f} | {r["epoch_cap"]} | {r["minimum_unique_tokens_for_cap"]/1e9:.1f} |')
 lines+=['',f'Weights and caps are proposals for testing, not published optimal settings. Totals assume {D/1e12:.2f}T tokens and an 80/20 phase split. All minimum pools must be checked after our tokenizer, global deduplication, decontamination and splits.','','## Proposed pre-hero GPU ledger','', '| Experiment stage | Projected GPU-days |','|---|---:|']
 for r in ledger:lines.append(f'| {r["stage"]} | {r["gpu_days"]:.1f} |')
 lines.append(f'| **Total** | **{result["rd_gpu_days_planning_total"]:.1f}** |')
 lines+=['','Pre-hero estimates use the same 250 model-TFLOP/s/GPU and 90% duty assumptions; small jobs can be slower. The hard cap is 1,280 GPU-days, including contingency. Stop or prune before exceeding it.','']
 (out/'hero-budget-summary.md').write_text('\n'.join(lines))
 print(json.dumps({k:v for k,v in result.items() if k not in ['mixture']},indent=2))
if __name__=='__main__':main()

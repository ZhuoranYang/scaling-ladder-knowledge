"""96-H100 planning scenarios, using the existing analytical MoE counter.
No GPU benchmark, trainer instantiation, or corpus download is performed.
"""
from pathlib import Path
import json,csv
from hero_budget import count
ROOT=Path(__file__).resolve().parents[1]
def main():
 prior=json.loads((ROOT/'configs/hero-h100/candidate.json').read_text());common=prior['common'];model={**prior['hero_looped'],'width':1536,'query_heads':24,'kv_heads':6}
 scenarios=[]
 for name,days,experts,D in [('30-hero-days',30,96,3.3e12),('30-total-days',24,88,2.8e12)]:
  m={**model,'experts':experts};s=count(m,common);capacity=[]
  for rate in [150,200,250,300]:
   C=96*days*86400*rate*1e12*.9;capacity.append({'model_tflops_per_gpu':rate,'available_compute':C,'supported_tokens':C/s['training_flops_per_token']})
  exposures=[]
  for x in prior['mixture']:
   w=.8*x['phase1']+.2*x['phase2'];exposures.append({'bucket':x['bucket'],'fraction':w,'exposure_tokens':D*w,'epoch_cap':x['epoch_cap'],'minimum_unique_tokens':D*w/x['epoch_cap']})
  scenarios.append({'name':name,'gpus':96,'assumed_gpu':'H100 SXM 80GB; not reconfirmed','hero_days':days,'preparation_days_inside_30':30-days,'proposed_token_horizon':int(D),'model':m,'accounting':s,'tpp':D/s['total_parameters'],'scenarios':capacity,'proposed_mixture_exposures':exposures})
 old=count(prior['hero_looped'],common);result={'status':'Planning examples only; no empirically chosen architecture or HPs. Latest scope: 96 GPUs for 30 days.','assumptions':{'productive_wall_fraction':.9,'nominal_model_tflops_per_gpu':250,'context':4096,'rd_gpu_days_all_in_cap':576,'notes':'All-in variant allocates 6 days preparation and 24 hero days. Extra data CPU/storage/embedding effort must be costed independently; GPU use counts against the cap. Rate is useful model FLOPs divided by training wall time; recomputation overhead is absorbed in measured rate.'},'common':common,'examples':scenarios,'previous_20b_tokens_at_250tflops_30days':96*30*86400*250e12*.9/old['training_flops_per_token']}
 out=ROOT/'configs/industry';out.mkdir(exist_ok=True);(out/'budget-96-h100-30d.json').write_text(json.dumps(result,indent=2)+'\n')
 rows=[]
 for ex in scenarios:
  for r in ex['scenarios']:rows.append({'variant':ex['name'],'hero_days':ex['hero_days'],'stored_parameters':ex['accounting']['total_parameters'],'nominal_tokens':ex['proposed_token_horizon'],'nominal_tpp':ex['tpp'],**r})
 with (ROOT/'doc/artifacts/industry-budget.csv').open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 print(json.dumps([{'variant':x['name'],'parameters':x['accounting']['total_parameters'],'flops_per_token':x['accounting']['training_flops_per_token'],'nominal_tpp':x['tpp'],'capacity_at_250':x['scenarios'][2]['supported_tokens'],'minimum_unique_pool':sum(b['minimum_unique_tokens'] for b in x['proposed_mixture_exposures'])} for x in scenarios],indent=2))
if __name__=='__main__':main()

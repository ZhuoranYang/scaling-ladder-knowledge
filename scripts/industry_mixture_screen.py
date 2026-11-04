"""Make explicit proposed data weights for the finite mixture screen.
Proportional baseline is a rule pending retained unique-token inventory.
"""
from pathlib import Path
import json,copy,math
ROOT=Path(__file__).resolve().parents[1]
def main():
 c=json.loads((ROOT/'configs/hero-h100/candidate.json').read_text());base={f'phase{p}':{r['bucket']:r[f'phase{p}'] for r in c['mixture']} for p in [1,2]};recipes={'proposed':copy.deepcopy(base)}
 changes={'no-medium-low':('cc_medium_low_actual','cc_medium_actual',None),'include-low':('cc_medium_actual','cc_low_actual_ablation_only',.1),'high-web-up':('cc_medium_actual','cc_high_actual',.1),'no-synthetic':('cc_high_synthetic','cc_high_actual',None),'code-up':('cc_medium_actual','code_starcoderdata',.05),'math-up':('cc_medium_actual','math_proof_pile_2',.05)}
 for name,(src,dst,amount) in changes.items():
  recipe=copy.deepcopy(base)
  for phase in recipe.values():
   delta=phase[src] if amount is None else amount;phase[src]-=delta;phase[dst]+=delta
   assert min(phase.values())>=0 and math.isclose(sum(phase.values()),1)
  recipes[name]=recipe
 result={'status':'Proposed weights; not published optima. Not a trainer config.','phase_token_fractions':{'phase1':.8,'phase2':.2},'weights_are':'token fractions after packing/loss-mask accounting','epoch_caps':{r['bucket']:r['epoch_cap'] for r in c['mixture']},'recipes':recipes,'proportional':{'rule':'Start with retained unique-token fractions U_b/sum(U_b). Enforce D_b <= epoch_cap_b*U_b; if the requested horizon is infeasible, change the horizon or source inventory rather than invent tokens. Freeze evaluated weights in the release manifest.','pending':'retained unique-token inventory under pinned tokenizer'},'proxy_pool_rule':'Scale each bucket unique pool and target exposures by the same proxy/hero exposure ratio; audit actual epochs.','source_requirements':{'cc':'Original Nemotron-CC public quality/kind manifests; tokenizer recount and global cleanup required','code':'Pinned StarCoderData if access resolved; otherwise choose a pinned replacement and retune','math':'Pinned Proof-Pile-2, subject to retained counts','dolma':'Team must specify exact release/components before treating it as an additional source or replacing web buckets'}}
 (ROOT/'configs/industry/mixture-screen.json').write_text(json.dumps(result,indent=2)+'\n');print('Wrote 7 explicit recipes plus inventory-dependent proportional baseline')
if __name__=='__main__':main()

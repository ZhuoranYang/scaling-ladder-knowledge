#!/usr/bin/env python3
"""Offline CPU checks on pinned public records and explicitly synthetic fixtures.

These commands never train, submit jobs, download corpora or benchmark a GPU.
"""
import argparse
from collections import Counter, defaultdict
import csv
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()


def step_law():
    result = {}
    for kind, expected in [('dense',1911),('moe',708)]:
        path = f'knowledge/inputs/{kind}_lr_bs_loss.csv'
        rows = list(csv.DictReader((ROOT/path).open()))
        if len(rows) != expected:
            raise ValueError(f'Unexpected {kind} release row count: {len(rows)}')
        groups = defaultdict(list)
        # Keep declared shapes and token horizons together. This still cannot
        # recover unrecorded recipe changes or establish a continuous optimum.
        fields = ['N','D','h','ffnh','numh','numl']
        if kind == 'moe':
            fields += ['seq_len','topk','nume','moeh','moe_layer_enum_type','mfa_version']
        for row in rows:
            groups[tuple(row.get(k,'') for k in fields)].append(row)
        minima=[]
        for key,group in sorted(groups.items()):
            finite=[r for r in group if math.isfinite(float(r['smooth loss']))]
            best=min(finite,key=lambda r:float(r['smooth loss']))
            sequence_length=int(float(best.get('seq_len') or 2048))
            minima.append({'group':dict(zip(fields,key)), 'observations':len(group),
                           'best_observed_lr':float(best['lr']),
                           'batch_sequences':int(float(best['bs'])),
                           'batch_tokens':int(float(best['bs']))*sequence_length,
                           'smooth_loss':float(best['smooth loss']),
                           'lr_at_observed_boundary':float(best['lr']) in
                           [min(float(r['lr']) for r in finite),max(float(r['lr']) for r in finite)]})
        result[kind]={'rows':len(rows),'groups':len(groups),'observed_grid_minima':minima}
    return result, ['knowledge/inputs/dense_lr_bs_loss.csv','knowledge/inputs/moe_lr_bs_loss.csv'], 'public_record_replay'


def hf_records():
    import pyarrow.parquet as pq
    path='references/marin/2026-datakit-proxy-run-records/harrier_18t75_d768.parquet'
    rows=pq.read_table(ROOT/path).to_pylist()
    modes=Counter(r['training_mode'] for r in rows)
    if len(rows)!=116 or modes!={'fresh_full':72,'resumed_cooldown':44}:
        raise ValueError('Historical HF export cohort changed')
    deviations=[]
    for r in rows:
        for phase in [0,1]:
            weights=r.get(f'phase{phase}_weights') or {}
            if weights:
                if any(v<0 for v in weights.values()):raise ValueError('Negative mixture weight')
                deviations.append(abs(sum(weights.values())-1))
    if max(deviations)>1e-8:raise ValueError('Mixture simplex failed')
    example=rows[0]
    result={'rows':len(rows),'training_modes':dict(sorted(modes.items())),
            'phase0_cells':len(example['phase0_weights']),
            'max_weight_sum_error':max(deviations),
            'example':{k:example[k] for k in ['run_name','full_scale_token_count','macro_bpb','n_eval_tasks']},
            'interpretation':'Experiment records, not training text; shared-prefix branches are not independent full runs.'}
    return result,[path],'public_record_replay'


def phase_exposure():
    path='knowledge/inputs/marin-hero-mixture.json'
    data=json.loads((ROOT/path).read_text());phases=data['phases'];availability=data['available_tokens']
    if len(phases)!=3 or len(availability)!=200:raise ValueError('Unexpected hero mixture schema')
    initial=108000/390251
    # Target exposure budgets in the inspected recipe, not measured corpus size.
    budgets=[18.75e12*initial,15e12-18.75e12*initial,3.75e12]
    epochs=defaultdict(float)
    for phase,budget in zip(phases,budgets):
        weights=phase['weights']
        if abs(sum(weights.values())-1)>1e-8:raise ValueError('Phase weights do not sum to one')
        for key,weight in weights.items():
            if weight<0 or (weight>0 and availability[key]<=0):raise ValueError('Invalid cell exposure')
            epochs[key]+=budget*weight/availability[key]
    maximum=max(epochs.values())
    if maximum>8+1e-8:raise ValueError('Cumulative eight-epoch cap exceeded')
    return {'cells':len(availability),'phases':[p['name'] for p in phases],
            'target_phase_tokens':budgets,'metadata_available_tokens':sum(availability.values()),
            'max_cumulative_epochs':maximum,'highest_exposure_cell':max(epochs,key=epochs.get),
            'interpretation':'Arithmetic on published availability metadata and proposed target exposure; no corpus scan or training execution.'},[path],'public_configuration_check'


def matrix_rank(matrix,tolerance=1e-9):
    a=[list(map(float,row)) for row in matrix];rank=0
    for col in range(len(a[0])):
        pivot=max(range(rank,len(a)),key=lambda r:abs(a[r][col]),default=None)
        if pivot is None or abs(a[pivot][col])<=tolerance:continue
        a[rank],a[pivot]=a[pivot],a[rank];scale=a[rank][col]
        a[rank]=[v/scale for v in a[rank]]
        for r in range(len(a)):
            if r!=rank:
                scale=a[r][col];a[r]=[x-scale*y for x,y in zip(a[r],a[rank])]
        rank+=1
        if rank==len(a):break
    return rank


def identifiability():
    ns=[1e8,2e8,4e8,8e8]
    ray=[[1,math.log(n),math.log(200*n)] for n in ns]
    grid=[[1,math.log(n),math.log(d)] for n in ns for d in [2e10,8e10]]
    ranks={'fixed_tpp_design_rank':matrix_rank(ray),'crossed_size_horizon_rank':matrix_rank(grid)}
    if ranks!={'fixed_tpp_design_rank':2,'crossed_size_horizon_rank':3}:raise ValueError(ranks)
    return {**ranks,'required_columns':3,'interpretation':'Synthetic log-linear design demonstration; no empirical scaling coefficients fitted.'},[],'analytical_fixture'


def optimizer_timescale():
    eta=.001;decay=.1;tokens=1e9;batch=1e6;updates=tokens/batch
    original=(1-eta*decay)**updates
    new_batch=2*batch;new_updates=tokens/new_batch
    approximate_decay=decay*new_batch/batch
    exact_decay=-math.expm1((new_batch/batch)*math.log1p(-eta*decay))/eta
    exact=(1-eta*exact_decay)**new_updates
    if not math.isclose(original,exact,abs_tol=1e-12):raise ValueError('Decay-only preservation failed')
    return {'original_shrinkage':original,'new_exact_decay':exact_decay,
            'new_approximate_decay':approximate_decay,'exact_preserved_shrinkage':exact,
            'normalized_timescale':batch/(eta*decay*tokens),
            'interpretation':'Gradient-free, constant-LR analytical fixture; not AdamW training, not a Muon transfer law.'},[],'analytical_fixture'


def evaluation():
    # Same tokenizer, artificial independent evaluation subsets with known sums.
    losses=[100.,900.];tokens=[100,300];byte_counts=[500,1800]
    pooled=sum(losses)/sum(tokens);macro=sum(l/n for l,n in zip(losses,tokens))/2
    bpb=sum(losses)/(math.log(2)*sum(byte_counts))
    if pooled!=2.5 or macro!=2.:raise ValueError('Aggregation fixture failed')
    return {'pooled_token_nll':pooled,'equal_subset_macro_nll':macro,'pooled_bpb':bpb,
            'context_gate':{'prompt_tokens':65000,'generation_tokens':4096,'served_context':65536,'fits':65000+4096<=65536},
            'interpretation':'Synthetic denominator and context-budget checks, not benchmark scores.'},[],'analytical_fixture'


def compute():
    h=1024;layers=16;experts=32;topk=2;f=1024;qh=16;kvh=4;head=64;vocab=65536;loops=2;context=4096
    attn=2*h*qh*head+2*h*kvh*head;expert=3*h*f;router=h*experts
    stored=2*vocab*h+layers*(attn+experts*expert+router)
    core=layers*(attn+topk*expert+router)
    flops=6*(loops*core+vocab*h)+12*layers*loops*context*qh*head
    rate=250e12;gpus=96;days=24;productive=.9
    capacity=gpus*days*86400*rate*productive
    return {'assumed_architecture':{'width':h,'unique_blocks':layers,'routed_experts':experts,'experts_per_token':topk,
                                   'expert_ffn':f,'query_heads':qh,'kv_heads':kvh,'head_dim':head,'vocab':vocab,
                                   'visits_per_unique_block':loops,'context':context},
            'stored_matrix_parameters':stored,'single_visit_routed_core_parameters':core,
            'approximate_training_flops_per_token':flops,'assumed_available_model_flops':capacity,
            'analytical_supported_tokens':capacity/flops,'all_in_gpu_days':96*30,
            'prehero_gpu_days':576,'hero_gpu_days':gpus*days,
            'interpretation':'Illustrative matrix-only counter with explicit attention term, 3x backward factor and assumed useful throughput; excludes norms/biases/router nonlinearities and is not a qualified trainer.'},[],'analytical_fixture'


RECIPES={'step-law-release':step_law,'hf-mixture-records':hf_records,'phase-exposure':phase_exposure,
         'identifiability':identifiability,'optimizer-timescale':optimizer_timescale,
         'evaluation-denominators':evaluation,'compute-ledger':compute}


def run(name,check=False):
    result,inputs,kind=RECIPES[name]()
    receipt={'recipe':name,'kind':kind,'execution':'local CPU only; no model training',
             'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
             'inputs':[{'path':p,'sha256':digest(p)} for p in inputs],'result':result}
    target=ROOT/'knowledge/receipts'/f'{name}.json'
    if check:
        expected=json.loads(target.read_text())
        expected.pop('executed_at',None)
        if receipt!=expected:raise ValueError(f'Receipt is stale or results differ: {name}')
    else:
        receipt['executed_at']=datetime.now(timezone.utc).isoformat()
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_text(json.dumps(receipt,indent=2,allow_nan=False)+'\n')
    print(f'{"CHECK" if check else "RUN"} {name}: {kind}')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('recipe',nargs='?',choices=list(RECIPES))
    parser.add_argument('--all',action='store_true');parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    if not args.all and not args.recipe:parser.error('choose a recipe or --all')
    for name in RECIPES if args.all else [args.recipe]:run(name,args.check)

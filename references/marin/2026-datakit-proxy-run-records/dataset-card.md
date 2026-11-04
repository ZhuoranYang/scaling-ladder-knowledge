---
license: apache-2.0
task_categories:
  - text-generation
tags:
  - data-mixing
  - pretraining
  - scaling-laws
  - marin
pretty_name: Grug-MoE Data-Mix Experiments
size_categories:
  - n<1K
configs:
  - config_name: default
    data_files: swarm_runs.parquet
  - config_name: harrier_18t75_d768
    data_files: harrier_18t75_d768.parquet
  - config_name: registry_legacy_d512
    data_files: registry/v1/swarms/legacy-swarm-d512/observations.parquet
  - config_name: registry_harrier_b262968b_d768
    data_files: registry/v1/swarms/harrier-store-b262968b-d768/observations.parquet
  - config_name: registry_harrier_0381a974_d768
    data_files: registry/v1/swarms/harrier-store-0381a974-d768/observations.parquet
  - config_name: registry_rav_ladder_d768
    data_files: registry/v1/swarms/rav-ladder-store-81e7e39a-d768/observations.parquet
  - config_name: registry_h100_d512_from10pct
    data_files: registry/v1/swarms/h100-d512-from10pct-store-4d2e363d/observations.parquet
---

# Grug-MoE Data-Mix Experiments

The `default` config contains the original 840-run Fisher-DSP swarm. The `harrier_18t75_d768` config contains the Harrier experiments described below.

## Fisher-DSP swarm (`default`)

840 MoE pretraining runs from the **Grug-MoE Fisher-DSP data-mixing swarm** (d512, TPU / `us-central2`).
Each run trains on a distinct **data mixture** over 168 datakit buckets; the swarm is used to **regress
mixture weights → eval loss** and predict an optimized pretraining mix.

Group: `swarm_fisher_dsp_tau20_lam0p25_uscentral2`. Every candidate is `swarm_fisher_dsp_d512_<index>`,
`index` ∈ `0..839`.

## Row schema (`swarm_runs.parquet`, 840 rows)

| column | type | description |
|---|---|---|
| `experiment_index` | int | candidate id, `0..839` |
| `phase0_weights` | dict[str, float] (168) | phase-0 mixture, `{bucket: weight}` (sums to 1) |
| `phase1_weights` | dict[str, float] (168) | phase-1 mixture, `{bucket: weight}` (sums to 1) |
| `model_paths` | list[str] | `gs://` checkpoint dir(s) for the run (private bucket; path references only) |
| `n_eval_tasks` | int | number of lm-eval tasks with results for this run |
| `macro_bpb` | float | mean bits-per-byte across tasks that report `bpb` |
| `evals` | str (JSON) | `{task: {bpb?, acc?, acc_norm?}}` per-task lm-eval results |

Each weight column is a `{bucket: weight}` dict, so a row is self-describing. Buckets are `c<CC>q<Q>`
(lexical cluster `CC` ∈ 01..38, quality tier `Q` ∈ 0..4) plus `tail`; the full list is also in
`buckets.json`. Training is two-phase, hence the phase-0 / phase-1 mixtures.

`bpb` (bits per byte) is the per-task **loss**; `macro_bpb` is the headline regression target. `acc` /
`acc_norm` are provided where the task publishes them.

## Load

```python
from datasets import load_dataset
import json
ds = load_dataset("marin-community/grug-moe-mix-swarm", split="train")
row = ds[0]
evals = json.loads(row["evals"])   # {task: {bpb, acc, ...}}
weights = row["phase0_weights"]    # {bucket: weight}, e.g. weights["c01q0"]
```

## Provenance

- Mixtures: `production_swarm_168p_uscentral2_d_optimal_mixtures.csv`
- Evals: lm-eval logprob results (`grug_logprob/swarm_fisher_dsp_d512_*`)
- Checkpoints: `gs://marin-us-central2/grug/swarm_fisher_dsp_d512_*`

Assembled by the Marin team. Metadata only (mixture weights, eval losses, checkpoint path strings) — the
model weights themselves are not included.

## Harrier 18.75T d768 experiments (`harrier_18t75_d768`)

This config contains 116 completed Harrier d768 runs using the Marin tokenizer and the 200 `c00q0` through `c39q4` domain-quality cells. It includes ten proportional seeds, 40 domain cooldowns, four quality cooldowns, 32 aggressive priors, eight earlier mixture priors, two targeted mixtures, eight next-round mixtures, eight joint mixtures, and four intuitive mixtures. Datakit and Nemotron tokenizer baselines are excluded because their cell token counts are not comparable.

Token and epoch columns describe the intended 18.75T full-scale allocation represented by each proxy run. Two-phase schedules use 15T and 3.75T. Resumed cooldown rows reconstruct phase 0 from their shared proportional step-8,448 checkpoint and store the observed continuation as phase 1.

`harrier_buckets.json` lists the 200 cells with their cluster number, domain label, quality bucket, and available token count.

| column | type | description |
|---|---|---|
| `run_name`, `group` | string | Stable experiment name and experiment family. |
| `training_mode` | string | `fresh_full` or `resumed_cooldown`. |
| `wandb_url`, `model_path`, `results_path`, artifact paths | string | W&B and S3 provenance. |
| `full_scale_token_count` | int | Total represented training tokens; 18.75T for every row. |
| `available_tokens` | dict[str, int] | Available Marin-tokenizer tokens in every domain-quality cell. |
| `phase{0,1}_token_count` | int | Full-scale phase budget. Phase 1 is null for stationary runs. |
| `phase{0,1}_weights` | dict[str, float] | Dense 200-cell phase mixture. |
| `phase{0,1}_allocated_tokens` | dict[str, float] | Full-scale tokens assigned to every cell. |
| `phase{0,1}_epochs` | dict[str, float] | Per-cell phase exposure: allocated tokens divided by available tokens. |
| `cumulative_allocated_tokens`, `cumulative_epochs` | dict[str, float] | Per-cell exposure summed across phases. |
| `max_cumulative_epochs`, `median_active_cumulative_epochs` | float | Compact repetition diagnostics. |
| `cells_over_16_epochs` | int | Number of cells above the exploratory 16-epoch prior. |
| `n_eval_tasks`, `effective_sample_count` | int | Evaluation coverage. |
| `macro_bpb` | float | Mean BPB across wrappers that report BPB. |
| `target_mean_bpb`, `guardrail_mean_bpb`, `all21_mean_bpb` | float | Raw grouped BPB summaries for the optimization task sets. |
| `*_relative_bpb_delta_pct` | float | Mean per-task relative BPB change from the ten proportional seeds; lower is better. |
| `hinge_target_guardrail_pct_epsilon0` | float | Target sum plus positive guardrail regressions, using relative percent BPB and zero tolerance. This is diagnostic because final task scales and epsilon remain unset. |
| `evals` | string (JSON) | Per-wrapper BPB and accuracy metrics. |
| `grouped_bpb` | string (JSON) | Per-wrapper BPB plus grouped INCLUDE and Belebele means. |

```python
from datasets import load_dataset
import json

ds = load_dataset(
    "marin-community/grug-moe-mix-swarm",
    "harrier_18t75_d768",
    split="train",
)
row = ds[0]
evals = json.loads(row["evals"])
epochs = row["cumulative_epochs"]
```

The target group is HumanEval, GSM8K, GPQA, ARC Challenge, OpenBookQA, SciQ, MedQA, MedMCQA, and MMLU-Pro. Guardrails are BoolQ, COPA, CSQA, HellaSwag, LAMBADA, BBH, MuSR, PIQA, TruthfulQA MC1, Winogrande, grouped Belebele, and grouped INCLUDE. The low-noise summary uses HumanEval, OpenBookQA, HellaSwag, LAMBADA, PIQA, TruthfulQA MC1, Winogrande, and grouped INCLUDE.


## Canonical swarm registry

`registry/v1/transfer_campaign.json` is the entry point for transfer-GP fitting. Its registry contains four canonical swarms:

| swarm | rows | purpose |
|---|---:|---|
| `legacy-swarm-d512` | 804 | Original swarm rows with complete modeled BPBs |
| `harrier-store-b262968b-d768` | 115 | First Harrier store; objective and seed-noise reference |
| `harrier-store-0381a974-d768` | 56 | Second Harrier store; kernel calibration reference |
| `rav-ladder-store-81e7e39a-d768` | 3 | Current target swarm |

Each `swarm.json` pins canonical observations, bucket metadata, the shared Luxical content matrix, and the migration rejection ledger by SHA-256. The registry also pins the exact 5,000-to-1,000-cell lookup. The legacy ledger records 36 excluded rows and their missing modeled BPBs.

Use dataset revision `a593d4289da165b29ceee7c394b625c97ad81367` to reproduce the published registry data:

```python
from huggingface_hub import hf_hub_download

manifest = hf_hub_download(
    repo_id="marin-community/grug-moe-mix-swarm",
    repo_type="dataset",
    filename="registry/v1/transfer_campaign.json",
    revision="a593d4289da165b29ceee7c394b625c97ad81367",
)
```

`registry/v1/migration_input/` contains the source tables, bucket metadata, Rav content matrix, and shared-basis lookup used by the one-time migration. Runtime consumers should read the canonical swarm bundles.

## H100 d512 conditional mixture experiments (`registry_h100_d512_from10pct`)

This registry config currently contains 937 completed d512 observations from the controlled
mixture experiment matrix. Every run restores the same step-393 checkpoint after a fixed 10% baseline
prefix, varies the mixture through roughly 80% of training, and then uses a separately controlled
cooldown mixture. `phase0_weights` and `phase1_weights` describe only the 13.125T/3.75T simulated
continuation; the shared 1.875T prefix is not attributed to either intervention. Physical-token metadata
likewise describes work executed after restoration.

The runs use `store_4d2e363d`. Its per-cell available-token counts replace the Rav store counts for
exposure calculations. The 200-cell Luxical content representation is inherited unchanged from
`store_81e7e39a` under the assumption that the stores have the same features and differ only in token
counts. Simulated epoching is enabled; `c22q0` remains empty, and other active cells are floored at
`1/49152` unless the experiment intentionally ablates them.

The config is an incremental snapshot: additional rows are added only after the chained 54-task KRR
evaluation has completed and produced a full result artifact. `training_eval_metrics` contains the final
108 Paloma and uncheatable-eval metrics emitted during training, including standard and dropless BPB/loss
values and their macro/micro aggregates. `training_metrics_source` and `training_metrics_uri` identify the
training artifact used; W&B is used only when the training artifact is absent or incomplete.

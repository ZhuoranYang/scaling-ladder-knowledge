---
id: recipe-offline-workbench
title: 'Offline workbench: public records and analytical fixtures'
type: wiki-recipe
tags:
- reproducibility
- step-law
- marin
- compute
architectures:
- dense-transformer
- moe-transformer
- recurrent-moe
architecture_scope: discussion and stated limits; not empirical transfer certification
confidence: inferred
reproducibility: runnable
reproducibility_scope: Offline CPU record/configuration checks or analytical fixtures;
  not model training
prerequisites:
- governance-evidence-standard
related:
- case-marin-reproduction
sources:
- dataset-marin-harrier-export
- doc-farseer-v3
- doc-local-workbench
- doc-marin-code-baseline
- doc-power-lines-v2
- doc-step-law-v3
- pr-marin-9162
claims:
- claim-steplaw-release-rows
- claim-marin-hf-records
- claim-marin-phase-cap
- claim-fixed-tpp-identifiability
- claim-decay-only-fixture
- claim-evaluation-denominators
- claim-looped-compute-accounting
reviewed_at: '2026-11-05'
code_examples:
- path: scripts/kb_workbench.py
  symbol: run
  command: python scripts/kb_workbench.py --all --check
  scope: Offline CPU record/configuration checks or analytical fixtures; not model
    training
version_sensitive:
- harrier-export
- marin-baseline
- pretraining-library
- steplaw-release
---

## What can be run now

This workbench is executable evidence for **public-record and analytical checks**. It needs no cluster credentials, model weights, corpus ingestion or GPU. It does not train a model, reproduce a paper's entire study or qualify a trainer.

```bash
python -m pip install -r scripts/requirements-kb.txt
python scripts/kb_workbench.py --all
python scripts/kb_workbench.py --all --check
```

The first command sequence regenerates seven receipts under `knowledge/receipts/`. `--check` recomputes results and checks them against the committed receipts without rewriting them. Inputs carry SHA-256 hashes and each receipt identifies the exact workbench-script digest. A code/input change therefore requires a deliberate new receipt, even if its visible headline result remains the same.

## The seven recipes and their boundaries

| Recipe | Actual input | Local check | What it does not establish |
|---|---|---|---|
| `step-law-release` | Verbatim dense/MoE CSVs from the pinned official archive |1911/708rows, declared groups, best observed grid points, sequence→token batch conversion | Continuous optima, complete original logs, causal recipe equivalence |
| `hf-mixture-records` | Pinned Harrier Parquet release |116rows;72fresh/44resumed; nonnegative phase-simplex weights | Possession of training text or independence of all rows |
| `phase-exposure` | Pinned hero mixture JSON |200cells, three phases, cumulative exposure/cap arithmetic | A measured corpus scan, phase deployment or an actual training run |
| `identifiability` | Explicit synthetic log-linear designs | Rank deficiency of a fixed-TPP ray versus a crossed grid | Empirical exponents or the correct nonlinear loss model |
| `optimizer-timescale` | Gradient-free constant-LR recurrence | Exact versus approximate batch/decay compensation | A trained AdamW optimum or transfer to MuonH |
| `evaluation-denominators` | Synthetic loss/token/byte sums and context budget | Macro versus pooled NLL; prompt-plus-output fit | Model capability scores or real data coverage |
| `compute-ledger` | Fully declared illustrative MoE dimensions and budget assumptions | Stored matrices, executed work, attention term and GPU-day ledger | Measured throughput, qualified recurrence or an optimal hero shape |

The [source card](../../sources/repositories/local-workbench.md) lists the actual files. The [input provenance manifest](../../knowledge/inputs/provenance.json) identifies the upstream archive member or pinned repository path. The original archives remain in `references/`.

## Inspect one empirical-record example

```bash
python scripts/kb_workbench.py step-law-release
python scripts/kb.py claim claim-steplaw-release-rows
```

The dense1.0737B/20B-token group yields a best observed smooth loss2.2254960 at LR0.001381 and sequence batch256. The2048-token context makes that524288tokens per batch. This row is descriptive finite-grid evidence under the released recipe. The checker groups by exposed shape fields; missing recipe metadata still limits causal interpretation.

Use this replay to learn the data contract before reproducing a training cell. A genuine training reproduction additionally needs the original data/tokenization, implementation, initialization/optimizer/schedule, numerical precision, hardware/runtime and evaluation definitions. A fitting repository is not automatically that complete training stack.

## Inspect one Marin record and its target exposure

```bash
python scripts/kb_workbench.py hf-mixture-records
python scripts/kb_workbench.py phase-exposure
```

The legacy export's116observations and the newer transfer registry's804/56/115/3tables describe different scopes. Do not add them as independent runs. An18.75Tfull-scale target field simulates desired exposure; the physical proxy did not necessarily consume18.75Ttokens. Shared-prefix cooldown runs reuse a history, which matters for cost and uncertainty.

The later hero JSON contains **three** phases, whereas some legacy search records contain one or two. The workbench checks that exact later configuration instead of silently flattening all generations into “the Marin mixture”.

## Reading a receipt correctly

A receipt's `kind` can be `public_record_replay`, `public_configuration_check` or `analytical_fixture`. Its `result` records measurements or calculations from that specific input. The `execution` explicitly says local CPU only. A page's claim links identify which parts of the result it relies on.

The original source's reported training results remain reported. For example, checking the HF table's file hash and row count does not independently reproduce the loss stored in a row. Similarly, recomputing a candidate's exposure fractions does not prove the referenced cloud store exists or its corpus was deduplicated as intended.

## From these checks to real experiments

1. Rebuild a small real-data subset and save source/normalized/token/attribute/store lineage.
2. Qualify trainer correctness, optimizer-group semantics, checkpoint/export parity and evaluation on actual hardware.
3. Measure representative end-to-end throughput and memory, including routing/drop behavior and resume continuity.
4. Run matched controls and a predeclared larger holdout, saving complete per-run records.
5. Add a training reproduction receipt only when inputs, environment, outputs and agreement tolerances are reviewable.

No current CPU receipt satisfies step5. The validator rejects `training_reproduced` claims under the current policy rather than accepting a label without a training-artifact contract.

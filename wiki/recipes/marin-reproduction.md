---
id: case-marin-reproduction
title: 'Marin replication: a stage-by-stage evidence and acceptance contract'
type: wiki-case-study
tags:
- marin
- data
- optimization
- evaluation
- midtraining
- posttraining
- cyber
architectures:
- not-applicable
architecture_scope: discussion and stated limits; not empirical transfer certification
confidence: inferred
reproducibility: runnable
reproducibility_scope: Offline CPU record/configuration checks or analytical fixtures;
  not model training
prerequisites:
- technique-data-mixture-design
- technique-hyperparameter-transfer
- technique-evaluation-contract
related:
- recipe-offline-workbench
sources:
- doc-marin-code-baseline
- issue-marin-8734
- issue-marin-8790
- issue-marin-8813
- issue-marin-9126
- pr-marin-10623
- pr-marin-7250
- pr-marin-8303
- pr-marin-9162
- pr-marin-9694
claims:
- claim-marin-normalized-id
- claim-marin-quality-alignment
- claim-marin-quality-compatibility
- claim-marin-phase-cap
- claim-marin-transfer-d1536
- claim-long-context-completions
- claim-sft-smoke-boundary
- claim-rsi-tradeoff
reviewed_at: '2026-11-05'
code_examples:
- path: scripts/kb_workbench.py
  symbol: hf_records
  command: python scripts/kb_workbench.py --all --check
  scope: Offline CPU record/configuration checks or analytical fixtures; not model
    training
performance_claims:
- claim_id: claim-marin-transfer-d1536
  metric: macro_bpb
  value: 0.91844
  unit: bits/byte
  model: d1536 mixture-swap rung
  data: Harrier three-phase comparison; frozen issue9126
  compute: 90767 updates; compute-equivalent saving is fitted, not runtime
  optimizer: Recipe linked in issue; not independently qualified
  evaluation: Final16-subset Paloma macro
  baseline: Old ladder in issue8435
  uncertainty: No final-rung confidence interval retrieved
  source_id: issue-marin-9126
  source_locator: Issue body and completion comment5688777500
  hardware: H100 ladder; exact runtime details in source
  dtype: Not re-established from the captured final metric
version_sensitive:
- marin-baseline
- marin-pr-snapshot
---

## Choose the exact reproduction lane

The existing [Marin code walkthrough](../../doc/data/marin-code-walkthrough.qmd), [artifact-lineage manual](../../doc/data/marin-artifact-lineage.qmd), [optimizer-search account](../../doc/optimizers/marin-hyperparameter-search.qmd) and [evaluation guide](../../doc/evaluation/marin-evaluation.qmd) provide the long-form details. This case study ties their stages to explicit handoff artifacts and rejection conditions.

| Lane | Frozen object | Status here |
|---|---|---|
| Historical Harrier | Adopted normalized leaves, Harrier embeddings/centroids, fusion/content types/calibration, original store and phase schedule | Source/code/results available; cloud input access and complete corpus reconstruction remain unresolved |
| Current reference DAG | Pinned Luxical/token-only pipeline and compatible new corpus/scorer/store | Code inspected; no end-to-end corpus pilot executed |
| Public-record replay | HF observations, bucket/content artifacts and recipe JSON | Selected offline record/configuration checks executed |
| Portable extension | New selected corpus and/or trainer, plus cyber additions | Proposed experiment requiring its own validation |

Do not call the fourth lane a byte-identical Marin reproduction. It can be a scientifically useful replication of methodology while changing implementation/data.

## Stage1: download and normalize one selected source

Resolve exact registry component names and upstream snapshots. Build a source manifest containing access status, raw filenames/checksums, extraction configuration, source IDs and output locations. Start with a selected subset, not the full default registry.

Normalize using the pinned policy. The content ID is xxh3_128 of normalized UTF-8 text; preserve upstream record identity separately. Save raw→normalized counts and fixtures where whitespace or code formatting matters. Re-running must preserve declared identities. [Claim](../governance/claim-ledger.md#claim-marin-normalized-id).

**Reject the stage** if required input snapshots cannot be retrieved, text boundaries are wrong, provenance disappears, normalization changes meaning, or the same bytes yield incompatible identities under the declared configuration.

## Stage2: duplicate and evaluation-overlap attributes

Exact cross-source canonicalization, fuzzy candidate generation and containment verification are separate operations. Preserve their versioned exception policies and representative choices. Do not convert an LSH connected component into “all but one are duplicates” without the actual verification rule.

Freeze benchmark text/features before decontamination. Inject known exact copies and inspect boilerplate collisions. Keep Bloom/index, common-feature drop-set, mark and report artifacts. The reported292-source production census is evidence of the author's pass, not our own scan.

**Reject the stage** for failed ID alignment, missing benchmark features, uncontrolled false removals or changed source-set semantics hidden under the same cache identity.

## Stage3: compatible topic and quality attributes

Historical fusion scoring reads stored Nemotron tokens and Harrier embeddings in normalized row order, then applies content-type-conditioned calibration. The current token-only reference path is a different interface. Freeze scorer/config/remap/calibration digests and check source/tokenizer compatibility before allocating expensive workers.

The [PR8303source](../../sources/prs/marin/PR-8303.md) reports18,710,478,349documents in its row-alignment census and a292-source bucket pass. Its NSF replay reports tolerance-sized raw-score differences under changed bf16 batch reduction order. Distinguish exact IDs/bucket reproduction from numerical raw-score tolerance. [Claim](../governance/claim-ledger.md#claim-marin-quality-alignment).

**Reject the stage** if a token-only caller is supplied per-type calibration without types, if joined IDs differ, if model bytes are inaccessible, or if old cell numbers are applied to newly trained centroids without a mapping.

## Stage4: commit retained stores and measure available supply

Join all co-partitioned attributes with ID checks; filter; construct token runs/caches; finalize successful output and count manifests. Count retained supply under the training tokenizer and reconcile source→bucket→store totals. Measure loader sample realization and resume continuity, not only a normalized weight vector.

```bash
python scripts/kb_workbench.py phase-exposure
```

This checks published configuration arithmetic. The team still needs actual source/bucket caches and empirical count/loader receipts before a corpus is declared prepared.

## Stage5: establish one proxy control, then search

Hold model/optimizer/resources/token horizon/evaluator fixed when screening mixtures. Preserve proportional and quality-biased controls. Tune the optimizer under the chosen conditional recipe, retaining the search history, unstable points, group settings and actual cost. If both data and optimizer change, use controlled comparisons to attribute gains.

The public mixture-search PRs and HF records provide concrete designs and outcomes, but a script's existence is not its execution. Shared-prefix branches must retain parent checkpoint and consumed-token lineage. The [offline replay](offline-workbench.md) is a practical first step, not completion of proxy training.

## Stage6: compare on a larger untouched rung

The [reported d1536comparison](../governance/claim-ledger.md#claim-marin-transfer-d1536) finishes90767updates at macro BPB0.91844,0.72%below the older ladder and improved on15/16Paloma subsets. The fitted1.20×compute-equivalent speedup assumes equal throughput. Code-related gains differ across sizes; Wikipedia regresses. These outcomes support evaluating transfer **with subset checks**, not assuming a universal mixture winner.

Our project needs its own matched larger-rung control and a predeclared acceptance region before approving the hero recipe. The budget must include this check; it is not free.

## Mid/post-training is a separate handoff

A long-context treatment requires the base checkpoint, optimizer/sampler offsets, context/QK choices, retained long-document supply and separate fixed/long-context evaluation. Captured2×/4×completion reports do not establish that8×is best. Chat SFT adds a canonical conversation/template/mask contract and weights-only initialization semantics. An eight-step SFT smoke is not final instruction-following evidence.

For RL or synthetic cyber curricula, compare base/control/treatment on held-out tasks and families, record attempts/uncertainty and broad-task guardrails. The reported RSI probe/pool tradeoff demonstrates why targeted improvement cannot be substituted for general validation.

## What is actionable for the team today

Run the offline checks; select an accessible source subset; obtain compatible scoring/embedding inputs or explicitly choose a new pipeline generation; qualify one trainer/evaluator; then budget and run matched pilots. The [question index](../../queries/by-problem.md) lists the inputs still missing for data access, hardware throughput, architecture selection and cyber transfer. None is silently filled by the documentation.

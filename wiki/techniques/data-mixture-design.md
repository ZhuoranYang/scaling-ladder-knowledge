---
id: technique-data-mixture-design
title: 'Data-mixture experiments: supply, exposure, controls and transfer'
type: wiki-technique
tags:
- data
- mixture
- repetition
- marin
architectures:
- not-applicable
architecture_scope: discussion and stated limits; not empirical transfer certification
confidence: inferred
reproducibility: runnable
reproducibility_scope: Offline CPU record/configuration checks or analytical fixtures;
  not model training
prerequisites:
- foundation-compute-accounting
related:
- recipe-offline-workbench
sources:
- dataset-marin-harrier-export
- doc-marin-code-baseline
- doc-marin-historical-datakit
- issue-marin-9126
- pr-marin-8303
- pr-marin-9162
- pr-marin-9694
claims:
- claim-marin-phase-cap
- claim-marin-hf-records
- claim-harrier-luxical-separation
- claim-marin-quality-compatibility
- claim-marin-transfer-d1536
reviewed_at: '2026-11-05'
code_examples:
- path: scripts/kb_workbench.py
  symbol: phase_exposure
  command: python scripts/kb_workbench.py --all --check
  scope: Offline CPU record/configuration checks or analytical fixtures; not model
    training
version_sensitive:
- harrier-export
- marin-baseline
- marin-pr-snapshot
---

## The scientific object is retained supply plus an exposure policy

A raw corpus name does not define a training distribution. Freeze source snapshots, extraction, normalization, deduplication, decontamination, tokenizer, quality model, calibration and domain assignments. These operations determine which documents survive and how much token supply remains. The mixture then determines repeated exposure over time.

[Marin’s detailed build account](../../doc/data/marin-code-walkthrough.qmd) and [PR/artifact lineage](../../doc/data/marin-artifact-lineage.qmd) remain the implementation references. This page specifies the experiment that should consume those artifacts.

## Inventory after processing, under the actual tokenizer

For bucket $i$, let $U_i$ be retained available token supply under the declared pipeline. For phase $s$, let $B_s$ be its target exposure budget and $w_{s,i}$ the token-sampling weight. Then

$$
A_i=\sum_s B_sw_{s,i},\qquad E_i=A_i/U_i,\qquad
w_{s,i}\ge0,\quad\sum_iw_{s,i}=1.
$$

$U_i$ is not the sum of source publishers' advertised token counts. Source overlap, failed downloads, duplicate representatives, benchmark removals, tokenizer changes and minimum-length rules change it. $A_i$ counts repeated training exposure; $E_i$ is a cumulative epoch equivalent, not a guarantee that every document was sampled equally.

If a quality rule removes half a bucket, holding its absolute weight fixed doubles its exposure pressure. Refit or at least revalidate the availability-aware search after substantial supply changes. A threshold that improves average quality can worsen achievable diversity and repetition.

## Historical labels cannot be ported by bucket number

[Claim `claim-harrier-luxical-separation`](../governance/claim-ledger.md#claim-harrier-luxical-separation) distinguishes the historical Harrier basis from the newer Luxical DAG. Both can produce40topic cells, but index14 does not identify the same semantic region across independently trained centroids. A compatible scorer/calibration is also necessary: the token-only quality caller and historical fusion/content-type bucketer have different input contracts.

For a faithful historical reproduction, adopt the exact embedding, centroid, quality and store artifacts. For a portable rebuild, declare a new basis and search mixtures for it. A stable text ID helps join attributes; it does not make incompatible cluster labels interchangeable.

## Reproduce a concrete feasibility check

```bash
python scripts/kb_workbench.py phase-exposure
```

The [receipt](../../knowledge/receipts/phase-exposure.json) checks the published hero JSON's200cells and three phase vectors under the documented18.75Ttarget exposure. Its availability metadata sums to23,106,103,007,622tokens and the computed maximum cumulative epoch equivalent is about7.0198, below the declared cap8. [Claim `claim-marin-phase-cap`](../governance/claim-ledger.md#claim-marin-phase-cap).

This is **configuration arithmetic**, not a scan proving that we possess23.1Tunique, decontaminated tokens. The initial/main/cooldown budgets are the inspected schedule's targets; the JSON and log distinguish configuration from deployment. A useful checker must fail on a positive-weight empty cell, a changed tokenizer/store generation, a misnormalized vector or an exceeded cumulative cap.

## Design the mixture experiment before fitting a surrogate

| Item | Hold fixed initially | What to record |
|---|---|---|
| Model and optimizer | Same shape, initialization convention, schedule and token batch | Per-group LRs, seed, routing/drop behavior |
| Physical proxy cost | Same token horizon and compatible hardware treatment | Actual tokens, updates, useful FLOPs, wall time |
| Store generation | Same corpus/tokenizer/taxonomy/scorer | Availability and full artifact lineage |
| Evaluation | Fixed independent task versions, masks and context | Per-task coverage, loss sums and denominators |
| Experimental axis | Mixture weights or one declared curriculum intervention | Phase budgets, boundaries and sampler realization |
| Repetition policy | Same simulated target exposure/cap rule | Physical versus simulated epochs separately |

Start with proportional sampling, a quality-biased control and a small number of mechanistic interventions. For cyber, separate source inclusion from source weight: adding new documents changes supply, whereas reweighting existing cells changes exposure. Keep both controls if both interventions matter.

A shared-prefix cooldown branch saves compute but shares history. Its outcome is not an independent complete run. The [public116-row audit](../../knowledge/receipts/hf-mixture-records.json) explicitly distinguishes72fresh and44resumed-cooldown observations. Use that lineage in uncertainty estimation and train/validation splits.

## Evaluate the target, not each run's own training distribution

Training loss on mixture $w$ averages a different target than training loss on mixture $w'$. Lower own-mixture loss can mean easier data. Rank candidates on one predeclared held-out distribution, with task-level guardrails. The objective can weight cybersecurity capability more heavily while preserving broad-language/math/code constraints, but the weights and guardrails must be declared before selecting the winner.

A surrogate should carry observation noise, coverage and source lineage. Separate the target swarm's incumbent from historical transfer observations. [PR8633](../../sources/prs/marin/PR-8633.md) implements one concrete two-phase transfer method; its closed-pool development replay is not a prospective hero-run validation.

## Scale-up and rejection criteria

Reserve an untouched larger rung and compare the chosen mixture with proportional/control sampling at a matched recipe. Retain both continuous losses and downstream capability metrics. The reported [d1536comparison](../governance/claim-ledger.md#claim-marin-transfer-d1536) supports transfer in one experiment; code-related gains differed across sizes and Wikipedia regressed. That is a reason to inspect subsets, not to replace them with a single macro.

Reject a mixture for this stage if its empirical sampler diverges materially from the declared weights, if positive-weight caches are inaccessible/empty, if it violates exposure caps, or if it crosses a predeclared evaluation guardrail. Threshold magnitudes and statistical power must come from the team's objective and observed noise; they are not established by the recipe above.

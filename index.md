---
title: "Pretraining Science Knowledge Base"
---

A source-pinned knowledge base for designing data mixtures, architectures,
optimizers, scaling experiments and evaluation. The original literature library
and long-form manuals remain; structured source cards and canonical synthesis
pages add retrieval and evidence contracts.

**Read:** [schema and retrieval contract](CLAUDE.md) ·
[PDF reading index](https://github.com/ZhuoranYang/scaling-ladder-knowledge/tree/main/pdf) ·
[complete literature library](references/SOURCES.md) ·
[current coverage and limits](wiki/governance/coverage.md).

## Start from a decision

| Decision | Canonical explanation | Concrete next artifact |
|---|---|---|
| How much model/data can our budget support? | [Compute and parameter accounting](wiki/foundations/compute-accounting.md) | Resolved tensor/FLOP ledger and measured useful throughput |
| How do we build and allocate training data? | [Mixture experiment design](wiki/techniques/data-mixture-design.md) | Retained-count, phase-exposure and sampler manifests |
| How do width, depth, batch and LR transfer? | [Hyperparameter protocol](wiki/techniques/hyperparameter-transfer.md) | Group-wise optimizer contract and controlled grid |
| What grid supports a scaling forecast? | [Identifiable fits and larger holdouts](wiki/techniques/scaling-fit.md) | Fit-ready observations, diagnostics and untouched holdout |
| How do we evaluate checkpoints/stages? | [Evaluation contract](wiki/techniques/evaluation-contract.md) | Frozen task/runtime config and per-item/numerator records |
| What should we inspect when a result fails? | [Failure diagnosis](wiki/patterns/failure-diagnosis.md) | Controlled hypothesis, intervention and before/after receipt |
| What exactly can we reproduce from Marin? | [Marin case study](wiki/recipes/marin-reproduction.md) | Explicit reproduction lane, input inventory and acceptance gates |

The [question index](queries/by-problem.md) distinguishes documented answers from
conditional plans and unresolved inputs. The hero architecture, accessible data
supply, measured H100 throughput and cyber transfer remain experimental decisions.

## Inspect the evidence

Follow **wiki page → claim ID → source card → original paper/code/data/result**.
A source card indexes the retained original; it does not replace it or certify a
paper-wide review. Confidence and reproducibility are separate fields.

- [Knowledge map and prerequisites](wiki/foundations/topic-map.md).
- [Evidence standards](wiki/governance/evidence-standard.md).
- [Scoped claim ledger](wiki/governance/claim-ledger.md).
- Browse [topics](queries/by-topic.md), [stages](queries/by-stage.md),
  [architectures](queries/by-architecture.md), [sources](queries/by-source.md),
  [evidence kinds](queries/by-evidence.md), and
  [reproducibility](queries/by-reproducibility.md).

## Run the small checks before proposing large training

```bash
python scripts/kb.py query "muP batch" --type technique
python scripts/kb.py get technique-hyperparameter-transfer --follow-sources
python scripts/kb.py claim claim-marin-transfer-d1536
python scripts/kb_workbench.py --all --check
python scripts/kb.py validate --verify-artifacts --check-generated
```

[The offline workbench](wiki/recipes/offline-workbench.md) contains seven CPU
recipes for pinned public records and analytical fixtures. They are not GPU
training reproductions. No claim that downloading a result reproduces its model
is permitted by the schema.

## Keep the literature and the detailed manuals

The [saved Jiaxuan blog](doc/reading/scientific-scaling-ladder.md),
[supplied notes](scaling_ladder_notes.md),
[annotated notes](doc/reading/deep-dive-notes.qmd),
[Step Law](doc/papers/step-law.qmd), [Farseer](doc/papers/farseer.qmd),
[Power Lines](doc/papers/power-lines.qmd), and
[OLMo](doc/efforts/olmo-pretraining.qmd)/[Marin](doc/efforts/marin-pretraining.qmd)
manuals remain available. [The original guide portal](doc/index.qmd) preserves the
full reading and experiment sequence.

Downloaded PDFs, extracted text, LaTeX, figures, code archives and snapshots stay
under `references/`. The preservation baseline protects the existing collection.
New evidence should be appended with its version and scope, not overwrite history.

---
id: governance-coverage
title: Knowledge coverage, unresolved inputs and review dates
type: wiki-governance
tags:
- governance
- provenance
- reproducibility
architectures:
- not-applicable
architecture_scope: discussion and stated limits; not empirical transfer certification
confidence: inferred
reproducibility: concept
reproducibility_scope: Evidence synthesis and navigation; not an executable training
  recipe
prerequisites:
- governance-evidence-standard
related:
- recipe-offline-workbench
sources:
- doc-local-workbench
- doc-team-plan-96h100
claims:
- claim-budget-96x30
reviewed_at: '2026-11-05'
version_sensitive:
- pretraining-library
---

## Current coverage, with explicit limits

The original library is retained. Structured pages and claim records are a new layer; old guides remain searchable companions. This is an initial reviewed slice, not a claim of KernelWiki-wide audit parity.

| Quantity | Count |
|---|---:|
| guide | 51 |
| source-blog | 1 |
| source-dataset | 2 |
| source-doc | 86 |
| source-issue | 4 |
| source-model | 5 |
| source-pr | 34 |
| wiki-case-study | 1 |
| wiki-foundation | 2 |
| wiki-governance | 3 |
| wiki-pattern | 1 |
| wiki-recipe | 1 |
| wiki-technique | 4 |

## Claim verification

- `cpu_replayed`: 8 claims.
- `source_read`: 14 claims.

**GPU training reproductions: 0.** Seven CPU recipes check public observations/configuration arithmetic or analytical fixtures; they do not reproduce Marin training.

## Next scientific work

1. Materialize one accessible, pinned real-source subset and qualify normalization, dedup/decon and scorer compatibility.
2. Qualify one trainer/optimizer/evaluator on intended hardware, then measure throughput and resume parity.
3. Run matched mixture/HP controls with seed handling and a predeclared larger holdout.
4. Add semantic claim coverage to OLMo/Nemotron/Kimi guides and source-specific trainer/eval contracts.
5. Treat cyber transfer, recurrence and very-long-context choices as conditional experiments.

## Version-sensitive contexts

| Context | Frozen version | Checked | Review due |
|---|---|---|---|
| pretraining-library | `fbba519 plus appended sources` | 2026-11-05 | 2026-12-05 |
| steplaw-v3 | `2503.04715v3` | 2026-11-01 | 2026-12-05 |
| steplaw-release | `32a8f4cc50247695fb56cc6c9117abdf67c97763` | 2026-11-02 | 2026-12-05 |
| power-lines-v2 | `2505.13738v2` | 2026-11-01 | 2026-12-05 |
| mup-v2 | `2203.03466v2` | 2026-11-01 | 2026-12-05 |
| marin-baseline | `1d274b52c636b6f2a9177b1d4c14b2f74795a8a6` | 2026-11-02 | 2026-12-05 |
| marin-pr-snapshot | `captured-2026-11-04` | 2026-11-04 | 2026-12-05 |
| harrier-export | `7aa59d2158a6299bde95d24dd1b1b9c98f6e4d5a` | 2026-11-02 | 2026-12-05 |

Dates are review reminders, not proof that upstream remains unchanged. Refresh by appending a new snapshot and evaluating affected claims.

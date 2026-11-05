---
id: technique-evaluation-contract
title: 'Evaluation contracts: losses, capabilities, contexts and failures'
type: wiki-technique
tags:
- evaluation
- long-context
- tokenizer
- uncertainty
architectures:
- not-applicable
architecture_scope: discussion and stated limits; not empirical transfer certification
confidence: inferred
reproducibility: runnable
reproducibility_scope: Offline CPU record/configuration checks or analytical fixtures;
  not model training
prerequisites:
- technique-data-mixture-design
related:
- recipe-offline-workbench
sources:
- doc-local-workbench
- doc-marin-code-baseline
- issue-marin-8813
- pr-marin-8656
claims:
- claim-evaluation-denominators
- claim-long-context-treatment
reviewed_at: '2026-11-05'
code_examples:
- path: scripts/kb_workbench.py
  symbol: evaluation
  command: python scripts/kb_workbench.py --all --check
  scope: Offline CPU record/configuration checks or analytical fixtures; not model
    training
version_sensitive:
- marin-pr-snapshot
- pretraining-library
---

## An evaluation name is not a protocol

“GSM8K”, “MRCR” or “Paloma” leaves many decisions unspecified: dataset revision/split, prompt, few-shot examples, tokenizer/chat template, context/windowing, generation budget, sampling, extractor, metric, routing mode and treatment of failures. Freeze those choices and their resolved values before ranking models.

The [Marin evaluation manual](../../doc/evaluation/marin-evaluation.qmd) anchors actual configurations and records. This page provides the contract needed to compare runs from a different trainer or dataset extension.

## Loss sums and denominators

Let $\ell_i=-\log p_\theta(x_i\mid x_{<i})$ and $m_i\in\{0,1\}$ be the declared score mask. Record sums, not just averages:

$$
S_\ell=\sum_i m_i\ell_i,\quad S_t=\sum_i m_i,\quad
\mathrm{NLL}_{token}=S_\ell/S_t.
$$

For the compatible scored UTF-8 byte count $S_b$,

$$
\mathrm{BPB}=S_\ell/(S_b\ln2).
$$

EOS, padding, prompt-only tokens, overlapping windows and document boundaries affect the mask and byte attribution. A tokenizer change requires a new cache identity and a verified mapping to the same raw text before interpreting cross-tokenizer BPB. Router regularization is a training diagnostic, not part of next-token evaluation NLL.

A pooled corpus estimate sums numerators/denominators across subsets. An equal-subset macro averages the declared subset values. They answer different target-distribution questions. The fixture uses loss sums100/900 and token counts100/300: pooled NLL2.5, macro NLL2.0. [Claim](../governance/claim-ledger.md#claim-evaluation-denominators).

```bash
python scripts/kb_workbench.py evaluation-denominators
```

The [receipt](../../knowledge/receipts/evaluation-denominators.json) is synthetic. It is a regression fixture for denominator semantics, not a language-model score.

## Keep evaluation cohorts identifiable

| Cohort | Purpose | Essential control |
|---|---|---|
| Native fixed-distribution loss | Compare recipe/mixture trajectories | Same raw text, tokenizer/cache, packing length and routing/drop mode |
| Benchmark likelihood | Continuous signals when tiny-model accuracy is near chance | Same choices/answers, shots, extraction and normalization |
| Generated-answer capability | Measure usable answers | Same template, decoding, token budget, extractor and verifier |
| Long-context retrieval/reasoning | Test access to distant information | Supported context, length/needle cells, truncation policy and coverage |
| Agent/environment tasks | Measure task completion with tools | Same environment/image/agent budget, verifier, retries and infrastructure policy |

A54-task HF macro, a16-subset Paloma macro and a20-response-task surrogate objective are separate cohorts. A log-probability GSM8K task is not generated-answer GSM8K accuracy. Do not merge these under a shared dashboard label.

## Context changes require two curves

When training context increases, retain validation at the old fixed length for comparability and add separately named longer-context evaluation. More conditioning can improve likelihood even without a better model. The [context-switch proposal](../../sources/prs/marin/PR-9639.md) preserves a canonical4K series; [multi-context proposal10711](../../sources/prs/marin/PR-10711.md) adds explicit length-scoped metrics. Their retrieved PR state is not proof every GPU path was rehearsed.

For served generation, require

$$
S_{prompt}+S_{generation}\le S_{served}.
$$

Use the served model's tokenizer to enforce the gate, even if the benchmark bins examples under another official tokenizer. Do not left-truncate a long-context prompt silently and report the score as if the distant information remained available. Publish supported/attempted/scored counts per length cell.

MRCR reference-answer likelihood with full-context versus final-user-only conditioning asks a different question than MRCR generation with a nonce-prefix check and string-similarity scorer. Preserve both definitions. Neither one is a universal long-context capability metric.

## Exports are part of the evaluator

Before comparing native loss with served task scores, verify token IDs, padding, special-token rows, chat rendering, representative logits/loss, cache/full-forward agreement and stop-token behavior. A correct weight tensor with a mismatched template can be unusable. Conversely, a new template can improve a score without a change in pretrained weights.

Post-training additionally requires preserving assistant-only loss masks and the weights-only versus optimizer-resume distinction. The generic SFT pipeline's partially green smoke does not qualify a different architecture's tied-embedding optimizer state. Follow the exact model-source branch and recorded validation outcome.

## Uncertainty and failure handling

Store per-item predictions and scores, not only aggregate metrics. For paired model comparisons, resample the relevant independent task/example units while preserving pairings. Four attempts from one task are not four independent task samples. Repositories or generated task families may also cluster examples; report that dependency when evaluating cyber or synthetic curricula.

Distinguish incorrect answers, extraction failures, unsupported context, environment errors and model-serving failures. Decide which enter the denominator and publish coverage. Marin's concrete record contract marks infrastructure-error runs below90%coverage as `infra_failed`; adopting that exact threshold is an implementation choice, not a universal statistical rule.

## Minimum result receipt

Record checkpoint/HF SHA; consumed tokens and training lineage; resolved evaluation/runtime commit; data revision/split/checksum; prompts/masks/template; shot/seed settings; context/generation/decoding; task-level score sums/denominators; predictions/traces; hardware and failure coverage. Keep base, mid-trained, SFT and RL model roles distinct.

For a cyber extension, create an independent task version with held-out repositories, time ranges or families as appropriate. Benchmark decontamination, verifier correctness and environment determinism must be tested before using scores to select a mixture or synthetic curriculum. Those tasks and acceptance thresholds remain project inputs, not achievements of this repository.

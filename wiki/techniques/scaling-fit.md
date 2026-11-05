---
id: technique-scaling-fit
title: Identifiable scaling fits and independent larger holdouts
type: wiki-technique
tags:
- scaling
- identifiability
- holdouts
- uncertainty
architectures:
- not-applicable
architecture_scope: discussion and stated limits; not empirical transfer certification
confidence: inferred
reproducibility: runnable
reproducibility_scope: Offline CPU record/configuration checks or analytical fixtures;
  not model training
prerequisites:
- technique-hyperparameter-transfer
related:
- recipe-offline-workbench
sources:
- doc-ai2-task-ladder-v2
- doc-farseer-v3
- doc-local-workbench
- doc-step-law-v3
claims:
- claim-fixed-tpp-identifiability
- claim-steplaw-law
reviewed_at: '2026-11-05'
code_examples:
- path: scripts/kb_workbench.py
  symbol: identifiability
  command: python scripts/kb_workbench.py --all --check
  scope: Offline CPU record/configuration checks or analytical fixtures; not model
    training
version_sensitive:
- pretraining-library
- steplaw-v3
---

## Decide what the fit is supposed to predict

An HP optimum law, a final language-model loss law, a task-accuracy predictor and a throughput model have different dependent variables and data requirements. Do not fit a loss-allocation law to untuned runs and interpret the residual as architecture quality. Do not use a task-accuracy curve to determine a token budget without the intermediate assumptions.

The primary reading companions are [Step Law](../../doc/papers/step-law.qmd), [Farseer](../../doc/papers/farseer.qmd), and [the AI2 task ladder](../../sources/papers/2024-ai2-task-scaling-model-ladders.md). Their reported coefficients remain conditional on their training and evaluation recipes.

## A simple loss surface and its allocation implication

An illustrative separable loss model is

$$
L(N,D)=L_\infty+aN^{-\alpha}+bD^{-\beta},
$$

where $N$ is the **declared** parameter convention, $D$ exposure tokens, $a,b>0$ and $\alpha,\beta>0$. With a dense compute proxy $C=\kappa ND$, substitution gives

$$
L(N,C/(\kappa N))=L_\infty+aN^{-\alpha}+b(C/\kappa)^{-\beta}N^\beta.
$$

Differentiating with respect to $\log N$ at an interior optimum yields

$$
\alpha aN^{-\alpha}=\beta bD^{-\beta}.
$$

This balances marginal reducible losses under that model. It does not prove that a sparse or recurrent model obeys $C=\kappa ND$, that data can be repeated indefinitely, or that serving-optimal allocation equals training-compute-optimal allocation. Use the explicit [compute ledger](../foundations/compute-accounting.md) and retained-data constraints before solving our target problem.

The user's preference for heavy overtraining is a deployment/design constraint. A200TPP stored-parameter heuristic can shortlist smaller models; it is not a measured optimum for our MoE. Keep it outside the empirical claim registry unless labeled as a proposal.

## Why a fixed-TPP ladder can be insufficient

Consider an HP law

$$
\log\eta=c+u\log N+v\log D.
$$

If every training point satisfies $D=kN$, then

$$
\log\eta=(c+v\log k)+(u+v)\log N.
$$

Only the combined slope and intercept are determined. Many $(c,u,v)$triples explain the same ray. More rungs on that ray do not create the missing independent direction. [Claim `claim-fixed-tpp-identifiability`](../governance/claim-ledger.md#claim-fixed-tpp-identifiability).

```bash
python scripts/kb_workbench.py identifiability
```

The [synthetic receipt](../../knowledge/receipts/identifiability.json) computes rank2 for the fixed-TPP design and rank3 for a crossed size/horizon grid. This is a design-matrix demonstration, not a new empirical fit. A more constrained scientific model can identify fewer quantities; its constraints must be stated rather than silently supplied by the optimizer.

## Collect a fit-ready observation table

Each row should identify model tensors/count convention, data/tokenizer/store generation, optimizer/parameterization/group LRs, batch, warmup/decay/final endpoint, seed, full checkpoint lineage, actually consumed tokens, computed and measured costs, and evaluation version/context/masks/coverage. Tag censored, unstable, interrupted and resumed branches explicitly.

Repeated checkpoints from one training trajectory are correlated. A cooldown fork shares its prefix with siblings. Treating these as independent observations understates uncertainty and can leak run-specific information into both fit and holdout. Retain trajectory/family IDs and resample independent experimental units, not arbitrary rows, when that matches the inferential target.

## Fit in stages, inspect failure modes

1. Fix the metric and units before choosing a functional form. Token NLL, BPB and task accuracy are different outcomes.
2. Establish HP selection for each size/horizon or explicitly model optimization error. Label interpolated optima and finite-grid minima.
3. Fit at least one simpler alternative and inspect conditioning, parameter covariance and boundary solutions.
4. Plot residuals against size, horizon, mixture, schedule phase, depth and precision. A structured residual often identifies an omitted variable rather than random noise.
5. Separate interpolation checks from genuine extrapolation checks. Holding out a middle grid point does not test the hero-size forecast.
6. Quantify sensitivity to the loss floor, model family, data-repetition interpretation and run exclusions.

Log-transforming loss directly is inappropriate when the model includes an unknown additive floor unless that floor is handled consistently. Constrained nonlinear fits can trade off $L_\infty$and exponents over a narrow range. A small residual on the fit set does not establish stable extrapolation.

## Reserve the larger holdout before selection

The holdout must be excluded from HP/mixture/model-form choices used to assess the forecast. Specify its model size, token horizon, recipe and evaluation in advance. Report a prediction interval conditional on the chosen model, plus sensitivity across plausible model forms. This interval does not automatically cover an untested change in tokenizer, architecture or trainer.

If the holdout fails, diagnose the discrepancy before another launch: count/compute mismatch, incomplete annealing, shifted data distribution, optimizer transfer failure, precision issues, token drops, evaluator/export mismatch or model-form error. Once used to revise the recipe, that run becomes development evidence. Reserve a fresh independent check.

## What constitutes acceptance here?

A fit is ready for a budget decision when observations have compatible definitions, identifiable parameters for the question, explicit uncertainty, sensible residuals, stable conclusions under reasonable alternatives, and a successful untouched larger check. The team must choose numerical tolerances from the decision cost and observed noise. No tolerance is established merely by borrowing a published exponent.

A useful research artifact includes the raw observation table, exclusions with reasons, exact fit code/environment, seeds/splits, fitted parameters/covariance, diagnostic plots and the predeclared holdout prediction with its eventual outcome. That is the object future source cards should point to.

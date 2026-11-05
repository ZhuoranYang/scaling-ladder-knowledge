---
id: governance-claim-ledger
title: Scoped scientific claim ledger
type: wiki-governance
tags:
- governance
- provenance
- literature
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
- dataset-marin-harrier-export
- doc-ai2-task-ladder-v2
- doc-farseer-v3
- doc-local-workbench
- doc-marin-code-baseline
- doc-marin-historical-datakit
- doc-mup-v2
- doc-power-lines-v2
- doc-step-law-v3
- doc-team-plan-96h100
- issue-marin-8734
- issue-marin-8790
- issue-marin-8813
- issue-marin-9126
- pr-marin-10623
- pr-marin-7250
- pr-marin-8303
- pr-marin-8656
- pr-marin-9162
- pr-marin-9694
claims:
- claim-steplaw-widths
- claim-steplaw-release-rows
- claim-steplaw-batch-units
- claim-steplaw-law
- claim-power-lines-timescale
- claim-mup-scope
- claim-marin-normalized-id
- claim-marin-quality-alignment
- claim-marin-quality-compatibility
- claim-harrier-luxical-separation
- claim-marin-hf-records
- claim-marin-phase-cap
- claim-marin-transfer-d1536
- claim-long-context-treatment
- claim-long-context-completions
- claim-sft-smoke-boundary
- claim-rsi-tradeoff
- claim-fixed-tpp-identifiability
- claim-decay-only-fixture
- claim-evaluation-denominators
- claim-looped-compute-accounting
- claim-budget-96x30
reviewed_at: '2026-11-05'
version_sensitive:
- harrier-export
- marin-baseline
- marin-pr-snapshot
- mup-v2
- power-lines-v2
- pretraining-library
- steplaw-release
- steplaw-v3
---

## Claim-level evidence ledger

Each entry is scoped. `source_read` means inspected source evidence; `cpu_replayed` means only the named receipt was regenerated locally. No GPU training reproduction is claimed.

## claim-steplaw-widths

**Step Law v3 reports non-power-of-two widths, including 960 and 1280.**

Kind: `reported_configuration` · verification: `source_read`.

Scope: model: Step Law Transformer family; data: Paper data recipe; optimizer: AdamW in paper; horizon: Reported Table 4 experiments; evaluation: Published configuration table.

Evidence: [Predictable Scale: Part I, Step Law](<../../sources/papers/2025-step-law-hyperparameter-scaling.md>).

Locator: Table 4; released dense CSV h column.

Limit: These configurations establish permissibility, not optimal aspect ratio or hardware throughput.

## claim-steplaw-release-rows

**The pinned Step Law fitting release contains 1911 dense and 708 MoE observation rows.**

Kind: `artifact_check` · verification: `cpu_replayed`.

Scope: model: Released dense and MoE cohorts; data: Pinned official fitting CSVs; optimizer: As recorded; no training executed; horizon: Multiple released token horizons; evaluation: Row count and grouped observed minima.

Evidence: [Predictable Scale: Part I, Step Law](<../../sources/papers/2025-step-law-hyperparameter-scaling.md>).

Locator: Released dense_lr_bs_loss.csv and moe_lr_bs_loss.csv.

Limit: Observation counts are not the paper headline experiment count or proof of independent full runs.

[CPU receipt](<../../knowledge/receipts/step-law-release.json>).

## claim-steplaw-batch-units

**Released Step Law bs values count sequences; the 2048-token context must be applied before comparison with token-batch laws.**

Kind: `reported_configuration` · verification: `source_read`.

Scope: model: Studied release families; data: Published fitting release; optimizer: Paper AdamW convention; horizon: Reported release; evaluation: Batch-unit conversion.

Evidence: [Predictable Scale: Part I, Step Law](<../../sources/papers/2025-step-law-hyperparameter-scaling.md>).

Locator: Section 3.2; release seq_len and bs columns.

Limit: Do not assume another tokenizer/context or release uses this conversion.

## claim-steplaw-law

**Step Law v3 fits LR and token batch jointly as conditional power laws in its declared parameter and token units.**

Kind: `reported_configuration` · verification: `source_read`.

Scope: model: Paper dense baseline with tested transfers; data: Paper mixture/tokenizer; optimizer: AdamW, specified warmup/final LR; horizon: Paper search/holdout domain; evaluation: Final losses used to locate HP optima.

Evidence: [Predictable Scale: Part I, Step Law](<../../sources/papers/2025-step-law-hyperparameter-scaling.md>).

Locator: Equation 1 and Table 2.

Limit: Coefficients are recipe-conditional; neither width-only muP nor an unqualified recurrent-MoE prescription.

## claim-power-lines-timescale

**For constant actual group LR, the nominal AdamW normalized decay timescale is token_batch / (LR * decay * horizon_tokens).**

Kind: `analytical_derivation` · verification: `source_read`.

Scope: model: Weights subject to decoupled decay; data: Not needed for decay-only derivation; optimizer: Constant-LR decoupled AdamW decay component; horizon: D/B updates; evaluation: Shrinkage accounting.

Evidence: [Power Lines: Scaling Laws for Weight Decay and Batch Size in LLM Pre-training](<../../sources/papers/2025-power-lines-batch-size-weight-decay.md>).

Locator: Weight-decay timescale definition; decay-only recurrence.

Limit: This formula is an accounting relation; an empirically optimal timescale need not remain constant across size or horizon. MuonH norm constraints are different.

## claim-mup-scope

**Width transfer requires the complete parameterization, initialization and per-parameter update convention; fixed-depth width evidence is not depth-transfer evidence.**

Kind: `reported_configuration` · verification: `source_read`.

Scope: model: Source-specific width families; data: Source-specific; optimizer: Declared muP implementation; horizon: Source-specific; evaluation: Transfer conditioned on unchanged conventions.

Evidence: [Tensor Programs V: Tuning Large Neural Networks via Zero-Shot Hyperparameter Transfer ($\mu$-Transfer)](<../../sources/papers/2022-mup-zero-shot-hyperparameter-transfer.md>), [Establishing Task Scaling Laws via Compute-Efficient Model Ladders (OLMo Task Ladder)](<../../sources/papers/2024-ai2-task-scaling-model-ladders.md>).

Locator: Tensor Programs V width-transfer construction; AI2 fixed-family ladders.

Limit: No universal per-group LR multiplier is inferred for a different optimizer or recurrent architecture.

## claim-marin-normalized-id

**The pinned Marin normalizer uses xxh3_128 of normalized UTF-8 text for a 32-hex-character content ID.**

Kind: `code_behavior` · verification: `source_read`.

Scope: model: No model; preprocessing; data: Normalized source text; optimizer: Not applicable; horizon: Not applicable; evaluation: Content identity and join contract.

Evidence: [Marin replication code audit: optimizer searches, MoE ladder and Datakit](<../../sources/repositories/2026-marin-replication-code-audit.md>).

Locator: lib/marin/src/marin/datakit/normalize.py generate_id and normalization.

Limit: The upstream record ID and registry source identity remain separate provenance fields.

## claim-marin-quality-alignment

**PR 8303 reports a 292-source row-alignment census and a bucket pass over 18710478349 documents.**

Kind: `reported_measurement` · verification: `source_read`.

Scope: model: Historical Harrier + Nemotron fusion scorer; data: 292 normalized sources; 162535 shards; optimizer: Scorer inference, not LM optimizer; horizon: Single reported corpus pass; evaluation: ID/row alignment and calibrated bucket outputs.

Evidence: [[datakit] Register the hero quality data as Datakit steps](<../../sources/prs/marin/PR-8303.md>).

Locator: PR description: census and bucket production pass.

Limit: Author-reported production counters. We did not scan the cloud corpus or independently time the pass.

## claim-marin-quality-compatibility

**The current token-only reference scorer and historical fusion/content-type bucketing are different compatible-input contracts.**

Kind: `code_behavior` · verification: `source_read`.

Scope: model: Current token-only versus historical fusion; data: Pinned compatible tokenize/normalize/content-type leaves; optimizer: Scoring only; horizon: Preprocessing; evaluation: Input compatibility and calibrated bucket assignment.

Evidence: [Marin replication code audit: optimizer searches, MoE ladder and Datakit](<../../sources/repositories/2026-marin-replication-code-audit.md>), [[datakit] Register the hero quality data as Datakit steps](<../../sources/prs/marin/PR-8303.md>), [[datakit] Score quality from the tokenize stage's token ids](<../../sources/prs/marin/PR-9694.md>).

Locator: fast_transformer score.py, bucket.py and Calibration.apply.

Limit: Per-type calibration cannot be substituted into the token-only caller without a content type; downloading a scorer path does not establish access.

## claim-harrier-luxical-separation

**Historical Harrier and the newer Luxical reference DAG use different embedding bases; equal bucket numbers do not imply equal content.**

Kind: `code_behavior` · verification: `source_read`.

Scope: model: Harrier 1024D versus Luxical 192D; data: Different embedding/centroid snapshots; optimizer: Not applicable; horizon: Preprocessing generation; evaluation: Taxonomy compatibility.

Evidence: [Marin Data Pipeline Overview](<../../sources/repositories/2026-marin-data-pipeline-overview.md>), [Marin replication code audit: optimizer searches, MoE ladder and Datakit](<../../sources/repositories/2026-marin-replication-code-audit.md>).

Locator: Historical report embedding section; current reference_pipeline.py.

Limit: Weights cannot be ported by cell number without a taxonomy mapping or new mixture search.

## claim-marin-hf-records

**The legacy Harrier HF export has 116 experiment rows: 72 fresh_full and 44 resumed_cooldown.**

Kind: `artifact_check` · verification: `cpu_replayed`.

Scope: model: d768 proxy cohort; data: HF revision 7aa59d2158a6299bde95d24dd1b1b9c98f6e4d5a; optimizer: Recorded recipe; not executed here; horizon: Full and branched/cooldown modes; evaluation: Public record/schema/simplex audit.

Evidence: [Marin Datakit released mixture experiment records: audited snapshot](<../../sources/releases/2026-datakit-proxy-run-records.md>).

Locator: harrier_18t75_d768.parquet training_mode column.

Limit: Not training text; resumed branches are not independent full runs. Different registry generations have different counts.

[CPU receipt](<../../knowledge/receipts/hf-mixture-records.json>).

## claim-marin-phase-cap

**The inspected hero JSON has three phase vectors over 200 cells and satisfies the eight-epoch cumulative cap under the documented target budgets.**

Kind: `artifact_check` · verification: `cpu_replayed`.

Scope: model: Later hero mixture contract; data: Historical Harrier store metadata; optimizer: Not executed; horizon: 18.75T target exposure; evaluation: Simplex, positivity and cumulative exposure accounting.

Evidence: [Marin replication code audit: optimizer searches, MoE ladder and Datakit](<../../sources/repositories/2026-marin-replication-code-audit.md>), [[grug] Switch the hero mixture after checkpoint 108000](<../../sources/prs/marin/PR-9162.md>).

Locator: harrier_mix_2026_08_18.json; initial 108000/390251; 15T plus 3.75T phase allocation.

Limit: Availability values are published metadata, not independently measured unique-token supply; this does not establish deployment of planned phases.

[CPU receipt](<../../knowledge/receipts/phase-exposure.json>).

## claim-marin-transfer-d1536

**Issue 9126 reports final d1536 macro BPB 0.91844, 0.72% lower than the older ladder, with 15/16 subsets improving.**

Kind: `reported_measurement` · verification: `source_read`.

Scope: model: d1536 mixture-swap rung; data: Three-phase Harrier-store comparison; optimizer: Recipe linked in issue; not independently qualified; horizon: 90767 completed updates; evaluation: Paloma 16-subset final macro BPB.

Evidence: [Compare the mixture-swap scaling ladder for Monday's data swap](<../../sources/issues/marin-9126.md>).

Locator: Issue body and completion comment 5688777500.

Limit: Reported final, not our rerun. 1.20x is a fitted compute equivalent assuming equal throughput; no final-rung confidence interval retrieved.

## claim-long-context-treatment

**The June context-extension experiment changes 65536 to 262144 context for 1000 updates at sequence batch 256 while controlling checkpoint and recipe.**

Kind: `reported_configuration` · verification: `source_read`.

Scope: model: June 67B-A2B Grug; data: Length-partitioned June store; optimizer: MuonH; qk multiplier 1.75; horizon: step156000 to157000; evaluation: 250-update cadence; long-context capability outcomes require separate scores.

Evidence: [Add 2x long-context treatment](<../../sources/prs/marin/PR-8656.md>), [Test 8x long-context skew at qk=1.75](<../../sources/issues/marin-8813.md>).

Locator: Launch contract and pinned context-extension launcher.

Limit: A TPU v4-2048 run; not a directly qualified 96-H100 recipe or proof of the winning long-document skew.

## claim-long-context-completions

**Captured discussions report completed 2x and 4x long-document treatments; the captured 8x discussion establishes launch, not a final winner.**

Kind: `source_status` · verification: `source_read`.

Scope: model: Matched June context-extension treatments; data: Same base store with length skew; optimizer: Controlled launch contract; horizon: 1000 continuation updates; evaluation: Reported completion versus launch, not comparative outcome.

Evidence: [Agent MoE Experiment: 2x long-context skew at qk=1.75](<../../sources/issues/marin-8734.md>), [Test 4x long-context skew at qk=1.75](<../../sources/issues/marin-8790.md>), [Test 8x long-context skew at qk=1.75](<../../sources/issues/marin-8813.md>).

Locator: Completion comments 5482519122 and5482519627; 8x launch5481810328.

Limit: Status as captured 2026-11-04. We did not retrieve private checkpoint bytes or a complete paired final benchmark table.

## claim-sft-smoke-boundary

**PR 7250 reports a 64-H100 eight-step native Grug SFT smoke ending at loss0.712 and a saved checkpoint.**

Kind: `reported_measurement` · verification: `source_read`.

Scope: model: Grug 67B-A2B, native step42150 weights-only initialization; data: Chat cache; WildChat stage; optimizer: AdamH first-pass recipe; horizon: 8 smoke updates; evaluation: Reported training loss, save success and memory fit.

Evidence: [Generalize chat SFT into a shared sft_step + ModelSource (Grug 67B backend)](<../../sources/prs/marin/PR-7250.md>).

Locator: PR description: end-to-end validation and geometry.

Limit: A systems smoke, not a completed SFT benchmark or demonstrated optimum. The target geometry uses AdamH because the considered Muon workspace did not fit.

## claim-rsi-tradeoff

**The RSI Snowball example reports improved synthesized-family probes alongside lower Smartie pool validation score.**

Kind: `reported_measurement` · verification: `source_read`.

Scope: model: Snowball67B-A2B,60 updates; data: Pool-only control versus pool+synthesized treatment; optimizer: Reported post-training recipe; horizon: 60 updates; evaluation: 214 probes and300 Smartie tasks; paired task bootstrap.

Evidence: [[post-training] RSI evaluation, audit and results](<../../sources/prs/marin/PR-10623.md>).

Locator: PR result table: Snowball rows.

Limit: Author-reported task means with four attempts/task. The probe gain does not establish broad-task improvement; held-out family definitions matter.

## claim-fixed-tpp-identifiability

**A fixed-TPP log-linear design cannot independently identify intercept, size exponent and token-horizon exponent.**

Kind: `analytical_derivation` · verification: `cpu_replayed`.

Scope: model: Synthetic size/horizon design; data: No empirical training data; optimizer: Not applicable; horizon: Fixed D/N ray versus crossed grid; evaluation: Design-matrix rank.

Evidence: [Local CPU record replays and analytical fixtures](<../../sources/repositories/local-workbench.md>), [Predictable Scale: Part I, Step Law](<../../sources/papers/2025-step-law-hyperparameter-scaling.md>), [Predictable Scale: Part II, Farseer: A Refined Scaling Law in Large Language Models](<../../sources/papers/2025-predictable-scale-part-ii-farseer-a-refined-scaling-law-in-large-language-models.md>).

Locator: scripts/kb_workbench.py and named execution receipt; Design matrix columns 1,logN,logD with D=kN.

Limit: Exact rank argument for this log-linear model; a more constrained model may identify fewer quantities.

[CPU receipt](<../../knowledge/receipts/identifiability.json>).

## claim-decay-only-fixture

**Doubling batch and applying the exact decay-only compensation preserves total constant-LR shrinkage in the analytical fixture.**

Kind: `analytical_derivation` · verification: `cpu_replayed`.

Scope: model: One decayed scalar weight with zero gradient; data: Synthetic; optimizer: Decoupled decay component only; horizon: D=1e9; batch1e6 versus2e6; evaluation: Exact shrinkage equality to floating-point tolerance.

Evidence: [Local CPU record replays and analytical fixtures](<../../sources/repositories/local-workbench.md>), [Power Lines: Scaling Laws for Weight Decay and Batch Size in LLM Pre-training](<../../sources/papers/2025-power-lines-batch-size-weight-decay.md>).

Locator: scripts/kb_workbench.py and named execution receipt; Gradient-free multiplicative recurrence.

Limit: This is not an optimizer-training comparison and does not transfer AdamW rules to MuonH.

[CPU receipt](<../../knowledge/receipts/optimizer-timescale.json>).

## claim-evaluation-denominators

**The fixture yields pooled token NLL2.5 and equal-subset macro NLL2.0 for the same supplied loss sums.**

Kind: `analytical_derivation` · verification: `cpu_replayed`.

Scope: model: No model; supplied log-loss sums; data: Synthetic 100/300-token subsets; optimizer: Not applicable; horizon: Fixed scored tokens; evaluation: Token-pooled versus equal-subset macro.

Evidence: [Local CPU record replays and analytical fixtures](<../../sources/repositories/local-workbench.md>), [Marin replication code audit: optimizer searches, MoE ladder and Datakit](<../../sources/repositories/2026-marin-replication-code-audit.md>).

Locator: scripts/kb_workbench.py and named execution receipt; Explicit two-subset aggregation fixture.

Limit: Synthetic data. Real BPB requires consistent raw bytes, masks, tokenizer and context; task macro cannot be equated to corpus-pool BPB.

[CPU receipt](<../../knowledge/receipts/evaluation-denominators.json>).

## claim-looped-compute-accounting

**Reusing weights changes executed visits and attention work without duplicating the stored weight matrices.**

Kind: `analytical_derivation` · verification: `cpu_replayed`.

Scope: model: Illustrative two-visit16-blockMoE; data: No training data; context4096; optimizer: Backward cost approximated by3x forward; horizon: Per-token analytical accounting; evaluation: Stored matrices versus routed matrix visits and attention FLOPs.

Evidence: [Local CPU record replays and analytical fixtures](<../../sources/repositories/local-workbench.md>), [Marin replication code audit: optimizer searches, MoE ladder and Datakit](<../../sources/repositories/2026-marin-replication-code-audit.md>).

Locator: scripts/kb_workbench.py and named execution receipt; Explicit illustrative matrix counter in kb_workbench.compute.

Limit: Matrix-only count excludes norms/biases/nonlinearities. Routing can visit different experts; executed work is not a unique-active-parameter count.

[CPU receipt](<../../knowledge/receipts/compute-ledger.json>).

## claim-budget-96x30

**The current all-in planning ledger allocates 576 prehero and2304 hero GPU-days within96 GPUs times30days.**

Kind: `proposal` · verification: `cpu_replayed`.

Scope: model: No chosen hero architecture; data: Not yet materialized; optimizer: Not yet qualified; horizon: 6 preparation days plus24 hero days; evaluation: GPU-day accounting; not measured throughput.

Evidence: [Current 96-H100 planning proposal](<../../sources/repositories/team-plan-96h100.md>), [Local CPU record replays and analytical fixtures](<../../sources/repositories/local-workbench.md>).

Locator: Team planning constraint; configs/industry/budget-96-h100-30d.json.

Limit: A resource proposal. H100 SKU/topology, measured throughput, data supply and trainer qualification remain unresolved.

[CPU receipt](<../../knowledge/receipts/compute-ledger.json>).

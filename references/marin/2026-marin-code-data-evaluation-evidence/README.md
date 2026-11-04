# Marin code, data, evaluation and continuation evidence

Retrieved 2026-11-04, using GitHub connector reads and public Hugging Face downloads. This bundle makes code/configuration evidence distinguishable from reported results and independently retrieved artifacts.

- [PR ledger](PR-LEDGER.md): explicit merge state and full head SHA. [Metadata](pr-metadata.json) preserves descriptions and commit/status fields. An unmerged PR can describe a completed experiment; a merged PR can still document an incomplete smoke.
- [Artifact audit](audit.json): URLs, revisions, byte counts and SHA-256 hashes; public campaign artifacts were checked against their embedded manifest hashes.
- `pr-head-files.json` and `pr-heads/`: selected frozen implementations for mixture search, length-partitioned stores, context-extension samplers, MRCR, RL probes and RSI evaluation.
- `baseline-code/`: selected evaluation/dataset/SFT/report files from `1d274b52c636b6f2a9177b1d4c14b2f74795a8a6`. The complete tracked-tree archive is in [the earlier audit](../2026-marin-replication-code-audit/README.md).
- `issues/9126.json` and `9126-timeline.json`: mixture-transfer comparison, measured final result and an earlier unfinished-analysis concern.
- `issues/{8734,8790,8813}*.json`: 2×/4×/8× long-context launch contracts. Completion comments are present for 2× and 4×; retrieved 8× comments establish launch, not a final evaluation table.
- `pr-comments-8656.json`: sampler review, including discrete-weight rounding concerns. Compare review timing to the saved head implementation.
- `huggingface/`: five model API/card/config snapshots (weights excluded), pinned campaign manifest and referenced observations/buckets/content/basis artifacts. These are experiment records/features, **not training text**.

## HF pins

| Repository | Revision |
|---|---|
| marin-community/marin-8b-base | e1a2021fd607dfba5086e2cbe916c160d03870f1 |
| marin-community/marin-8b-instruct | 0378f9c932bd64ca189d2f2ca5bd2fb076cba61d |
| marin-community/marin-32b-base | f19b346615212ff9a6d92c10861a9cdb100cbf97 |
| laion/delphi-1e22-p33m67-32p07b-lr0.67-54770ae7 | 56cc5aaf65cd59d6632962cee636a0423abfbf66 |
| laion/delphi-9e19-p33m67-coldstart-magpie_lr1e5 | 8be0758421b6ec928bd4d7a8fab0e8035430abb6 |
| marin-community/grug-moe-mix-swarm campaign | 283eacf18b66b7888b59fd8f889d6be134aee879 |

The campaign manifest SHA-256 is `5ed5fb024590dd4707b802caf8fe728be1b8d73375c100139f884b0728f0cca2`. Referenced files resolve beneath this pinned campaign root, as in PR #8633's loader. Informational URI fields can have older names; embedded relative paths and expected hashes determine the bytes used.

## Reproduction scope

`python scripts/collect_marin_stage_evidence.py` downloads small public HF snapshots and verifies campaign dependencies. It does not install the trainer or run the GP candidate search, evaluation, SFT, RL or cloud training. The collector explicitly retains the five model revisions and verifies the local Marin checkout against the baseline SHA. The campaign dependencies comprise 19 files (~7.8 MB); observation tables have 804, 56, 115 and 3 rows in their respective registry scopes.

No cloud training stores, historical scoring leaves, raw training corpora or model weight tensors were fetched. A path in a PR is evidence of a dependency, not proof that we have access to it. Published scores remain author-reported unless explicitly described as a local record/schema/hash verification.

## Authored guides

- [PR/code/data replication chain](../../../doc/data/marin-artifact-lineage.qmd).
- [Marin evaluation by stage](../../../doc/evaluation/marin-evaluation.qmd).
- [Mid-training and post-training experiment account](../../../doc/training/marin-midtraining-posttraining.qmd).

# Understanding scientific pretraining ladders

**[Read the rendered PDFs](pdf/README.md)** — all 51 Quarto pages, with equations, figures and flowcharts. Start with [Marin data processing](pdf/doc/data/marin-artifact-lineage.pdf), [evaluation](pdf/doc/evaluation/marin-evaluation.pdf), or [mid/post-training](pdf/doc/training/marin-midtraining-posttraining.pdf).

Start with the [Jiaxuan blog reading guide](doc/reading/jiaxuan-reading-guide.qmd). It maps the original blog, supplied notes, section protocols, and deeper explanations.

- **Saved blog:** [doc/reading/scientific-scaling-ladder.md](doc/reading/scientific-scaling-ladder.md), with local figures in `doc/assets/`.
- **Supplied notes:** [scaling_ladder_notes.md](scaling_ladder_notes.md).
- **Annotated Quarto notes:** [doc/reading/deep-dive-notes.qmd](doc/reading/deep-dive-notes.qmd), generated from the supplied notes with companion links.
- **Source housekeeping:** [doc/sources/source-guide.qmd](doc/sources/source-guide.qmd).
- **Complete paper/report list:** [references/SOURCES.md](references/SOURCES.md).
- **Full experiment workflow:** [doc/workflow/workflow.qmd](doc/workflow/workflow.qmd).

The `doc/experiments/` guides explain each blog section. The `doc/deep-dives/` companions unpack equations, experimental controls, worked examples and inference pitfalls. The [architecture evidence guide](doc/architecture/architecture-evidence.qmd) and [Nemotron case study](doc/efforts/nemotron-pretraining.qmd) give concrete empirical practices. Checked claims and qualifications are recorded in [the notes review](doc/reading/notes-review.qmd).

The [beginning-to-end pretraining design](doc/workflow/from-data-to-pretraining.qmd) explains the path from an available corpus to a validated training run, drawing on the [OLMo](doc/efforts/olmo-pretraining.qmd) and [Marin](doc/efforts/marin-pretraining.qmd) effort deep dives.

The earlier [128-H100 candidate plan](doc/plans/hero-h100-candidate.qmd) and [SMELT review](doc/architecture/smelt-looped-moe.qmd) give numerical architecture/data/compute choices for a smaller overtrained MoE. Specifications are in `configs/hero-h100/`; regenerate arithmetic with `python scripts/hero_budget.py`. These are not an already qualified training launcher.

## Replicate Marin and extend the data

The concrete evidence chain is in [Marin PRs, code, data and results](doc/data/marin-artifact-lineage.qmd). Separate guides cover [evaluation during pretraining, mid-training and post-training](doc/evaluation/marin-evaluation.qmd), and [long-context continuation, SFT and RL experiments](doc/training/marin-midtraining-posttraining.qmd). The [evidence ledger](references/marin/2026-marin-code-data-evaluation-evidence/PR-LEDGER.md) records exact PR heads and merge status; pinned HF cards and hash-verified mixture-campaign artifacts are saved alongside it.

Use [the code-level Datakit manual](doc/data/marin-code-walkthrough.qmd) and [optimizer-search manual](doc/optimizers/marin-hyperparameter-search.qmd) as the replication entry points. The [MoE comparison](doc/architecture/moe-families.qmd) distinguishes Qwen3, OLMoE and Marin recipe generations. Dedicated deep dives cover [Step Law](doc/papers/step-law.qmd), [Farseer](doc/papers/farseer.qmd) and [Power Lines](doc/papers/power-lines.qmd). The [cyber-data plan](doc/data/cyber-data.qmd) defines a controlled domain extension after the broad baseline is reproduced.

```text
doc/
  reading/        preserved blog, annotated notes and reading map
  workflow/       scientific workflow and industry-practice audit
  plans/          current 96-GPU and historical 128-GPU scenarios
  architecture/   architecture evidence, MoE comparison, SMELT
  data/           Marin processing, code walkthrough and cyber extension
  optimizers/     Marin search and transfer procedures
  training/       trainer implementation playbook
  evaluation/     checkpoint/evaluation protocol
  efforts/        OLMo, Marin and Nemotron effort guides
  papers/         Step Law, Farseer and Power Lines deep dives
  deep-dives/     mathematical companions
  experiments/    section-by-section protocols
  sources/        generated source housekeeping
  artifacts/      generated counts, run tables and reading-map JSON
  assets/         figures
```

`doc/path-migration.json` records old/new paths. Links, generators and Quarto navigation have been updated. Root conversation/technical notes are preserved. Regenerate replication/search contracts with `python scripts/build_marin_replication_specs.py`; these are inspectable specifications, not submitted jobs.

## Current industry-practice review

The latest constraint is **96 GPUs for 30 days**, provisionally H100 SXM 80GB. Start with:

- [Evidence audit of the Jiaxuan conversation](doc/workflow/industry-practice-audit.qmd); the supplied [conversation notes](scaling_ladder_industry_practice.md) are preserved.
- [Marin data engineering and released experiment audit](doc/data/marin-data-engineering.qmd).
- [TorchTitan and Megatron-LM training/tuning playbook](doc/training/trainer-playbook.qmd).
- [Checkpoint evaluation protocol](doc/evaluation/checkpoint-evaluation.qmd).
- [Revised budget, corpus requirements and finite run queue](doc/plans/plan-96-h100.qmd).

Source trees are downloaded under ignored `tmp/`; pinned archives are in `references/systems/` and `references/evaluation/`. `configs/industry/source-pins.json` identifies inspected revisions. The Step Law official fitting code is now archived in its paper folder. Downloaded Marin Parquet files are mixture experiment records, not training documents.

Regenerate numerical plans with `python scripts/industry_budget.py` followed by `python scripts/industry_run_matrix.py` and `python scripts/industry_mixture_screen.py`. These scripts do not submit training or download corpus shards. The earlier 128×40 plan is retained for comparison and is superseded for the current allocation.

## Read the HTML site

```bash
quarto preview
```

To build without serving:

```bash
quarto render
```

The rendered home page is `_site/doc/index.html`. Quarto renders LaTeX math with MathJax. Generated site output and the Marin checkout under `tmp/` are Git-ignored.

## Update the reading material

```bash
python scripts/build_notes_quarto.py
python scripts/summarize_references.py
python scripts/build_reference_catalog.py
python scripts/build_source_guide.py
quarto render
```

The original blog and supplied Markdown remain identifiable source documents. Edit generated notes through their input or generator; put source corrections in `doc/reading/notes-review.qmd`. See [AGENTS.md](AGENTS.md) for evidence and writing conventions.

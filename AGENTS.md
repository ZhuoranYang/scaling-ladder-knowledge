# Project instructions

## Purpose

Build a source-grounded learning resource for the science and practice of pretraining scaling ladders. The first applied guides will cover data-mixture design, model architecture, and optimizer/hyperparameter design. Favor explanations that let a reader derive and plan an experiment, not a catalogue of model recipes.

## Repository map

- `doc/` contains Quarto Markdown (`.qmd` or `.md`) intended to render as HTML.
- `doc/reading/scientific-scaling-ladder.md` is a locally saved copy of the Jiaxuan Zou overview; its figures are in `doc/assets/`.
- Each paper has its own `references/<topic>/<year-readable-title>/` folder containing `paper.pdf`, `paper.txt`, `metadata.json`, the source archive and extracted `source/`, and discovered repository archives in `code/`. ArXiv identifiers and consulted versions remain in metadata; `references/directory-map.json` maps legacy names to current paths. Non-arXiv works use the same topic layout.
- Web-first references have their own `references/<topic>/<year-readable-title>/article.md` snapshot.
- `references/SOURCES.md` maps local copies to source URLs; `references/download-manifest.json` records collection results. Add new sources to the inventory.
- `doc/workflow/workflow.qmd` is the workflow overview; `doc/experiments/` explains the 12 blog sections and appendix separately. Clearly label the blog as a synthesis of cited experiments.
- `tmp/` is an ignored checkout of Marin. It is reference material, not part of this project's authored documentation.

## Evidence and citation rules

1. Base technical claims on primary papers, official technical reports, or reproducible experiment artifacts. Prefer an original paper over a secondary summary.
2. Cite claims close to where they appear. Include author/team, year, a stable URL or arXiv identifier, and the relevant section, table, or figure when available. Use citations in prose and provide a references section for each guide.
3. Distinguish measured results, theoretical claims, author recommendations, and our own synthesis. Attribute empirical values to the exact model, data, compute range, optimizer, and evaluation protocol that produced them.
4. Do not turn one lab's recipe into a universal rule. Report applicability limits, conflicting evidence, uncertainty, and what experiment would resolve it.
5. Preserve parameter-count, token, loss, compute, and data-mixture definitions. State whether counts include embeddings/head, whether tokens are unique or repeated, and how FLOPs and validation loss are measured.
6. For rapidly changing reports, record the version/date consulted. Never imply a local snapshot is current without checking the source.

## Guide design

Write the three guides as complementary experiment-design workflows:

### Data mixture

Walk from objective and target distribution to corpus inventory, provenance/licensing, filtering and deduplication, tokenizer and token accounting, domain/quality features, mixture hypotheses, proxy experiments, fixed-distribution evaluation, repetition/epoch controls, mixture optimization, and scale-up/holdout validation. Explain why training loss on each run's own mixture cannot rank mixtures. Include reproducible mixture manifests and data-lineage checks.

### Architecture

Walk from deployment constraints and target workload to a frozen baseline, architecture family, width/depth and aspect-ratio ladder, attention/context choices, normalization/position/MLP invariants, dense-vs-MoE experimental axes, parameter/FLOP/memory accounting, proxy fidelity, ablations, stability and systems-throughput checks, and target-scale holdouts. Separate active from total MoE parameters and distinguish theoretical compute from wall-clock cost.

### Optimizers and schedules

Walk from optimizer implementation and numerical conventions to a reference scale, fair tuning budget, parameterization and initialization, learning-rate/batch/weight-decay search, schedule and warmup/annealing choices, optimizer-state and precision accounting, cross-scale transfer fits, seed/selection-bias controls, high-learning-rate stability stress tests, implementation parity, and out-of-sample validation. Compare optimizers only after tuning each to a comparable frontier and report full training trajectories, not just endpoints.

Each guide should include: (a) a step-by-step protocol, (b) decision tables with measured quantities and controls, (c) equations in LaTeX with definitions and units, (d) common failure modes, (e) a minimal run-matrix template, and (f) a pre-registered acceptance/holdout checklist. Keep data, architecture, and optimizer changes orthogonal in initial experiments; test combinations only after individual effects are measured.

## Quarto and writing

- Write in Quarto Markdown with YAML front matter. Keep math in standard `$...$` and `$$...$$` delimiters and define every symbol on first use.
- Render to HTML using the repository `_quarto.yml`; use the shared styles in `doc/styles.css`. Keep typography readable and equations legible.
- Use descriptive headings, concise paragraphs, accessible figure alt text, and captions that cite the figure's source.
- Put large source documents and figures in `doc/` and `doc/assets/`; avoid embedding remote-only figures when a local image is available.
- Keep generated HTML, `_site/`, Quarto cache, and `tmp/` out of version control.
- Do not alter the meaning of imported source material silently. Mark editorial notes and local adaptations as such.

## Empirical evidence and supplied notes

- Preserve `scaling_ladder_notes.md` and the imported Jiaxuan blog. Build the annotated notes using `python scripts/build_notes_quarto.py`, then render `doc/reading/deep-dive-notes.qmd`; put corrections and audit status in `doc/reading/notes-review.qmd`.
- Begin architecture questions with `doc/architecture/architecture-evidence.qmd`. Whenever proposing a scaling rule, cite concrete published runs or sweeps: configurations, what was fixed, horizon, optimizer/parameterization, numerical outcome, and exact figure/table or code locator.
- Distinguish a reported configuration, a measured optimum, a theoretical scaling consequence, and our proposed experiment. Do not infer optimal depth from a fixed-depth ladder.
- Distinguish μP base LR from actual parameter-group LRs, width transfer from depth transfer, and token batches from sequence batches. State the paper version for numerical coefficients.

- Use `python scripts/build_reference_catalog.py` after adding or reorganizing references. The catalogue is grouped by topic with readable titles. Collection scripts must discover references recursively and preserve metadata identifiers when folders move.
- The architecture decision chart is in `doc/architecture/architecture-evidence.qmd`; the Nemotron pretraining comparison is in `doc/efforts/nemotron-pretraining.qmd`. Keep curriculum transitions, LR decay boundaries, base-model evaluations and post-training results distinct.

## Reading structure and housekeeping

- `doc/reading/jiaxuan-reading-guide.qmd` is the entry point and crosswalk between the blog and supplied notes; their section numbers differ.
- Preserve `scaling_ladder_notes.md`. Its annotated Quarto edition is generated by `scripts/build_notes_quarto.py`; this keeps prose/equations while adding navigation and emitting `doc/artifacts/notes-reading-map.json`.
- `doc/deep-dives/` contains focused derivations, worked examples and inference details complementing the section protocols. New companions should link back to the reading guide and be mapped from the appropriate notes subsection.
- `doc/sources/source-guide.qmd` is generated by `scripts/build_source_guide.py` from reference metadata. The complete list remains `references/SOURCES.md`. Regenerate the housekeeping page after changing collection metadata.
- `README.md` identifies the saved blog, supplied notes, generated Quarto edition, source list and preview/build commands. Keep these entry points and sidebar navigation synchronized.

- `doc/efforts/olmo-pretraining.qmd` and `doc/efforts/marin-pretraining.qmd` explain the teams’ distinct corpus, proxy, ladder and training efforts. `doc/workflow/from-data-to-pretraining.qmd` is the detailed project-design path from an available corpus to final pretraining. Keep reported configurations distinct from proposed numerical defaults.

## Earlier 128-GPU numerical candidate (historical)

- The user's earlier hero budget was 128 H100 GPUs for 40 days, with hardware topology and whether R&D is additional still awaiting confirmation. State both budget interpretations; never count the same GPU-days twice.
- The user requested a smaller model overtrained around 10× the Chinchilla rule. Current screening uses at least 200 tokens per stored parameter, including embeddings; this is a dense-rule proxy rather than a measured MoE optimum. The candidate is about 20B stored / 4.5T tokens, superseding the earlier 67B proposal.
- `configs/hero-h100/candidate.json` is the earlier complete design specification, not an executable trainer config. `experiments.json` records the work queue. `scripts/hero_budget.py` generates analytical compute, mixture exposure and GPU-ledger outputs; update them whenever dimensions or horizons change.
- `doc/plans/hero-h100-candidate.qmd` distinguishes primary evidence, candidate choices and unvalidated hardware/trainer assumptions. `doc/architecture/smelt-looped-moe.qmd` reviews the pinned v3 paper; its proprietary stack/internal corpus prevent claiming an exact reproduction.
- The public CC index is in `configs/data/nemotron-cc-index/`. Only index/pilot URL manifests have been fetched, not corpus shards. `hf-pins.json` records source revisions and gates; do not claim StarCoder access has been accepted or corpus ingestion completed.

- The conditional all-in variant is `configs/hero-h100/all-in-40days-candidate.json`: 10 preparation/contingency days plus 30 hero days, about 16.65B/3.4T. The main 20B/4.5T plan retains 40 hero days plus separately budgeted R&D. Current R&D hard cap is 1,280 GPU-days including contingency.

## Current industry-practice review and 96-GPU allocation

- The latest requested budget is 96 GPUs for 30 days, provisionally the earlier H100 SXM 80GB assumption. `doc/plans/plan-96-h100.qmd` is the current plan. Keep separate 30 hero days and 30 total days; all-in uses 576 pre-hero GPU-days and 24 hero days. Earlier 128×40 documents are historical scenarios, not current launch instructions.
- Preserve `scaling_ladder_industry_practice.md` as supplied testimony. `doc/workflow/industry-practice-audit.qmd` audits it against Step Law v3, Farseer v3, Power Lines v2 and Marin artifacts. Width need not be a power of two; do not universally invalidate all HP laws after any mixture change; revalidate transfer first. Unique tokens, exposures, and fitted effective-data quantities are distinct.
- `doc/data/marin-data-engineering.qmd` distinguishes the report's pinned `64a9483...` pipeline from the newer local checkout. The downloaded `harrier_18t75_d768.parquet` contains 116 experiment records, including 72 fresh and 44 resumed-cooldown rows, not training text. Never treat shared-prefix branches as independent full runs or equate historical report counts with present exports.
- `doc/training/trainer-playbook.qmd` and `doc/evaluation/checkpoint-evaluation.qmd` describe downloaded TorchTitan, Megatron-LM and LM Evaluation Harness implementations. Exact revisions are in `configs/industry/source-pins.json`; trees in `tmp/` are ignored, persistent archives are in `references/`. No trainer is qualified for the proposed custom recurrence; no GPU experiment has run here.
- Regenerate current arithmetic with `python scripts/industry_budget.py` then `python scripts/industry_run_matrix.py`. The 80-run queue and GPU ledger are proposals; absolute HP centers, trainer recipes, real throughput, bucket pools and control-family comparisons still require qualification. Do not call these trainer-executable configs.

## Folder structure and Marin replication priority

- Documents now live in topic folders: `doc/reading`, `workflow`, `plans`, `architecture`, `data`, `optimizers`, `training`, `evaluation`, `efforts`, `papers`, `deep-dives`, `experiments`, and `sources`. Generated tables/maps are in `doc/artifacts`; shared figures remain `doc/assets`. `doc/path-migration.json` maps historical paths. `scripts/doc_paths.py` keeps generated links valid; do not reintroduce root-level guide paths.
- Preserve supplied root Markdown notes. The imported blog is `doc/reading/scientific-scaling-ladder.md`; only its local links/assets were mechanically relocated. Quarto generators now write their moved destinations.
- The team wants to replicate Marin before adding high-quality cyber data. Prioritize `doc/data/marin-code-walkthrough.qmd`, `doc/optimizers/marin-hyperparameter-search.qmd` and `doc/data/cyber-data.qmd`. Direct Marin replication and a TorchTitan/Megatron port are different experiments. Existing looped-MoE resource examples are not Marin replicas.
- `doc/architecture/moe-families.qmd` compares pinned official Qwen3/OLMoE configs and Marin code. Qwen3's query-head projection width can exceed residual width; never enforce `num_heads * head_dim == hidden_size` as a universal counter assumption. Powers of two are a convenient shortlist, not a requirement.
- Marin reference BO (`reference_hyperparameter_sweep.py`: 10 rounds x 4 suggestions) is distinct from May/August multiplier grids and systems tuning. Issue bodies can be stale; use dated comments and pinned code, including the May fit's parameter/token accounting correction. A fixed sqrt(batch) exponent does not fit a batch-optimum law.
- The inspected current reference DAG uses Luxical 192D int8 embeddings; the historical report used Harrier 1024D. The token-only quality caller refuses type-conditioned calibration; a separate fusion/content-type bucketing path supports it. The later hero mixture file validates three phase vectors and an eight-epoch cumulative cap. Do not apply historical weights to renumbered new buckets.
- Dedicated paper deep dives: `doc/papers/step-law.qmd`, `farseer.qmd`, `power-lines.qmd`. Evidence/code/issue/config snapshots are in `references/marin/2026-marin-replication-code-audit/`. Search/replication/cyber contracts are generated by `scripts/build_marin_replication_specs.py`; heavier searches replace or require funding beyond the earlier bounded queue, never count as free additions.

## Marin PR, HF and stage-specific evidence

- `doc/data/marin-artifact-lineage.qmd` links the pipeline to PR heads, input/output contracts, HF campaign replay and issue #9126 measured finals. Historical Harrier adoption and current Luxical reconstruction are separate replication lanes.
- `doc/evaluation/marin-evaluation.qmd` records native loss, mixture-task log probabilities, long-context likelihood/generation, capability/agent runtime and result records. Keep their denominators, task universes and evaluation contexts separate.
- `doc/training/marin-midtraining-posttraining.qmd` covers length-partitioned stores, matched 2×/4×/8× continuations, SFT and RL evidence. A closed issue or launcher does not prove a final scored result. Runtime launch SHAs can differ from retrieved PR heads.
- `references/marin/2026-marin-code-data-evaluation-evidence/` preserves PR metadata/status, selected files/discussions, HF cards and hash-verified campaign dependencies. Model cards can contain base-model tables even in instruct repositories. Do not attribute these rows to instruct checkpoints.
- `scripts/collect_marin_stage_evidence.py` fetches small public evidence only; it does not fetch model weights/training corpora or launch training/evaluation.

- The saved blog retains GitHub-style section links. `python scripts/fix_blog_anchor_aliases.py` adds explicit navigation aliases for Quarto without changing imported prose, math, headings or figures; it is idempotent. Run it after refreshing the imported blog.

## Published PDF reading collection

- `pdf/` contains a tracked PDF for every configured Quarto source page, mirroring the source path, plus a readable index and checksummed manifest. Keep `_site/` and browser/virtualenv artifacts in ignored `tmp/`.
- Run `quarto render` before `scripts/render_pdfs.py`; see `pdf/README.md` and `scripts/requirements-pdf.txt` for the isolated Chromium setup. The exporter checks MathJax, Mermaid, figures and text extraction before indexing outputs. Update PDFs when their sources change.
- Root README links to the PDF index so GitHub readers can view rendered pages without opening `.qmd` source.

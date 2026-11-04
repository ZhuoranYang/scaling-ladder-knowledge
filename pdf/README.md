# Read the rendered PDFs

These PDFs are printed from the Quarto HTML pages, including rendered equations, figures and flowcharts. Click a title to open GitHub’s PDF viewer; use **Download raw file** to save it.

**Suggested starting points:** [Jiaxuan reading guide](doc/reading/jiaxuan-reading-guide.pdf), [Marin data pipeline](doc/data/marin-artifact-lineage.pdf), [Marin evaluation](doc/evaluation/marin-evaluation.pdf), [mid/post-training](doc/training/marin-midtraining-posttraining.pdf), and [96-H100 plan](doc/plans/plan-96-h100.pdf).

**51 documents · 204 PDF pages.** Each PDF mirrors its source path. Dense tables use landscape pages. Source files and the original references remain in the main repository.

| Document | PDF pages | Editable source |
|---|---:|---|
| [Understanding scientific pretraining ladders](<doc/index.pdf>) | 2 | [Source](<../doc/index.qmd>) |
| [The science of pretraining: annotated deep-dive notes](<doc/reading/deep-dive-notes.pdf>) | 18 | [Source](<../doc/reading/deep-dive-notes.qmd>) |
| [Reading Jiaxuan’s scientific scaling ladder blog](<doc/reading/jiaxuan-reading-guide.pdf>) | 2 | [Source](<../doc/reading/jiaxuan-reading-guide.qmd>) |
| [Review of the deep-dive notes against primary evidence](<doc/reading/notes-review.pdf>) | 2 | [Source](<../doc/reading/notes-review.qmd>) |
| [How to Build a Scientific Scaling Ladder](<doc/reading/scientific-scaling-ladder.pdf>) | 32 | [Source](<../doc/reading/scientific-scaling-ladder.md>) |
| [Starting with Nemotron-CC or Marin data: the complete pretraining design](<doc/workflow/from-data-to-pretraining.pdf>) | 7 | [Source](<../doc/workflow/from-data-to-pretraining.qmd>) |
| [Industry workflow: auditing the Jiaxuan conversation](<doc/workflow/industry-practice-audit.pdf>) | 6 | [Source](<../doc/workflow/industry-practice-audit.qmd>) |
| [The complete workflow for scaling-law experiments](<doc/workflow/workflow.pdf>) | 2 | [Source](<../doc/workflow/workflow.qmd>) |
| [Candidate v1: a smaller overtrained looped MoE on 128 H100s](<doc/plans/hero-h100-candidate.pdf>) | 10 | [Source](<../doc/plans/hero-h100-candidate.qmd>) |
| [Data-first candidate plan: 96 H100s for 30 days](<doc/plans/plan-96-h100.pdf>) | 4 | [Source](<../doc/plans/plan-96-h100.qmd>) |
| [Width, depth, μP, and training hyperparameters: what actual ladders do](<doc/architecture/architecture-evidence.pdf>) | 10 | [Source](<../doc/architecture/architecture-evidence.qmd>) |
| [MoE architecture choices: Qwen3, OLMoE and Marin](<doc/architecture/moe-families.pdf>) | 4 | [Source](<../doc/architecture/moe-families.qmd>) |
| [SMELT v3: what two-pass MoE looping actually establishes](<doc/architecture/smelt-looped-moe.pdf>) | 2 | [Source](<../doc/architecture/smelt-looped-moe.qmd>) |
| [Adding high-quality cyber data to a Marin-style corpus](<doc/data/cyber-data.pdf>) | 4 | [Source](<../doc/data/cyber-data.qmd>) |
| [Marin replication: PRs, code, data and result receipts](<doc/data/marin-artifact-lineage.pdf>) | 5 | [Source](<../doc/data/marin-artifact-lineage.qmd>) |
| [Replicating Marin Datakit: a code-level data-processing manual](<doc/data/marin-code-walkthrough.pdf>) | 6 | [Source](<../doc/data/marin-code-walkthrough.qmd>) |
| [Building our corpus with Marin’s data-engineering approach](<doc/data/marin-data-engineering.pdf>) | 7 | [Source](<../doc/data/marin-data-engineering.qmd>) |
| [Replicating Marin’s optimizer tuning and transfer](<doc/optimizers/marin-hyperparameter-search.pdf>) | 5 | [Source](<../doc/optimizers/marin-hyperparameter-search.qmd>) |
| [Marin mid-training and post-training: concrete experiments](<doc/training/marin-midtraining-posttraining.pdf>) | 4 | [Source](<../doc/training/marin-midtraining-posttraining.qmd>) |
| [Training and tuning with TorchTitan and Megatron-LM](<doc/training/trainer-playbook.pdf>) | 5 | [Source](<../doc/training/trainer-playbook.qmd>) |
| [Checkpoint evaluation: from ladder loss to usable-model evidence](<doc/evaluation/checkpoint-evaluation.pdf>) | 4 | [Source](<../doc/evaluation/checkpoint-evaluation.qmd>) |
| [Marin evaluation: pretraining, mid-training and post-training](<doc/evaluation/marin-evaluation.pdf>) | 5 | [Source](<../doc/evaluation/marin-evaluation.qmd>) |
| [Marin in depth: corpus pipelines, mixture proxies, and Delphi](<doc/efforts/marin-pretraining.pdf>) | 3 | [Source](<../doc/efforts/marin-pretraining.qmd>) |
| [Nemotron pretraining: Nano, Super, Ultra, and Nemotron-CC](<doc/efforts/nemotron-pretraining.pdf>) | 4 | [Source](<../doc/efforts/nemotron-pretraining.qmd>) |
| [OLMo in depth: from corpus construction to validated training](<doc/efforts/olmo-pretraining.pdf>) | 3 | [Source](<../doc/efforts/olmo-pretraining.qmd>) |
| [StepFun Part II: Farseer’s loss surface and allocation experiments](<doc/papers/farseer.pdf>) | 3 | [Source](<../doc/papers/farseer.qmd>) |
| [Power Lines: batch size, weight decay and long-horizon training](<doc/papers/power-lines.pdf>) | 3 | [Source](<../doc/papers/power-lines.qmd>) |
| [StepFun Part I: Step Law, experiment by experiment](<doc/papers/step-law.pdf>) | 3 | [Source](<../doc/papers/step-law.qmd>) |
| [From predicted loss to a validated capability forecast](<doc/deep-dives/capabilities-and-validation.pdf>) | 2 | [Source](<../doc/deep-dives/capabilities-and-validation.qmd>) |
| [Turn mixture weights into auditable data exposure](<doc/deep-dives/data-and-repetition.pdf>) | 2 | [Source](<../doc/deep-dives/data-and-repetition.qmd>) |
| [Design a ladder that identifies the question you ask](<doc/deep-dives/grid-and-inference.pdf>) | 2 | [Source](<../doc/deep-dives/grid-and-inference.qmd>) |
| [From a loss law to a model-size decision](<doc/deep-dives/loss-and-allocation.pdf>) | 2 | [Source](<../doc/deep-dives/loss-and-allocation.qmd>) |
| [Count parameters, tokens, and executed training work](<doc/deep-dives/measurement-and-compute.pdf>) | 2 | [Source](<../doc/deep-dives/measurement-and-compute.qmd>) |
| [Learning-rate schedules, batch size, and optimizer memory](<doc/deep-dives/schedules-and-timescales.pdf>) | 2 | [Source](<../doc/deep-dives/schedules-and-timescales.qmd>) |
| [Scope: what a scaling ladder predicts](<doc/experiments/01-scope.pdf>) | 1 | [Source](<../doc/experiments/01-scope.qmd>) |
| [Objectives, evaluation, and acceptance criteria](<doc/experiments/02-objectives.pdf>) | 1 | [Source](<../doc/experiments/02-objectives.qmd>) |
| [Measurement: parameters, FLOPs, tokens, and loss](<doc/experiments/03-measurement.pdf>) | 1 | [Source](<../doc/experiments/03-measurement.qmd>) |
| [Architecture: a controlled baseline and structural ladders](<doc/experiments/04-architecture.pdf>) | 2 | [Source](<../doc/experiments/04-architecture.qmd>) |
| [Experimental grid, checkpoints, and compute budget](<doc/experiments/05-grid-budget.pdf>) | 1 | [Source](<../doc/experiments/05-grid-budget.qmd>) |
| [Optimizers, hyperparameter transfer, and annealed comparisons](<doc/experiments/06-optimizers.pdf>) | 2 | [Source](<../doc/experiments/06-optimizers.qmd>) |
| [Data experiments: source value, mixture weights, and repetition](<doc/experiments/07-data-mixture.pdf>) | 2 | [Source](<../doc/experiments/07-data-mixture.qmd>) |
| [Fitting loss surfaces and diagnosing extrapolation](<doc/experiments/08-fitting.pdf>) | 2 | [Source](<../doc/experiments/08-fitting.qmd>) |
| [Predicting downstream capabilities](<doc/experiments/09-downstream.pdf>) | 1 | [Source](<../doc/experiments/09-downstream.qmd>) |
| [Holdouts, stability, and production decisions](<doc/experiments/10-validation.pdf>) | 1 | [Source](<../doc/experiments/10-validation.qmd>) |
| [Staged training and long-context ladders](<doc/experiments/11-specialized.pdf>) | 1 | [Source](<../doc/experiments/11-specialized.qmd>) |
| [Execution records, deviations, and ladder maintenance](<doc/experiments/12-execution.pdf>) | 1 | [Source](<../doc/experiments/12-execution.qmd>) |
| [Public examples: Chinchilla, optimizer grids, and Delphi](<doc/experiments/13-public-ladders.pdf>) | 1 | [Source](<../doc/experiments/13-public-ladders.qmd>) |
| [Source housekeeping: what we have and where to find it](<doc/sources/source-guide.pdf>) | 3 | [Source](<../doc/sources/source-guide.qmd>) |
| [1 Reference collection status](<references/README.pdf>) | 2 | [Source](<../references/README.md>) |
| [1 Source catalogue](<references/SOURCES.pdf>) | 4 | [Source](<../references/SOURCES.md>) |
| [1 Marin reading map](<references/MARIN-READING.pdf>) | 1 | [Source](<../references/MARIN-READING.md>) |

## Regenerate

Install Quarto and the Python/browser dependencies, then run from the repository root:

```bash
python -m venv tmp/pdf-tools
tmp/pdf-tools/bin/pip install -r scripts/requirements-pdf.txt
PLAYWRIGHT_BROWSERS_PATH="$PWD/tmp/pdf-browser" tmp/pdf-tools/bin/python -m playwright install --with-deps chromium --only-shell
quarto render
PLAYWRIGHT_BROWSERS_PATH="$PWD/tmp/pdf-browser" tmp/pdf-tools/bin/python scripts/render_pdfs.py
```

The exporter checks that equations, diagrams and figures render, verifies readable PDF text, and records page counts and SHA-256 hashes in [manifest.json](manifest.json). Internet access is needed for the HTML’s MathJax and web-font resources. No model weights or training text are downloaded.

# Marin reading map

The Marin checkout is under the ignored `tmp/marin/` directory. The repository evolves quickly; check its current commit and source files before quoting implementation details in a guide.

## Start with these reports and recipes

- [`docs/recipes/add_scaling_heuristic.md`](https://github.com/marin-community/marin/blob/1d274b52c636b6f2a9177b1d4c14b2f74795a8a6/docs/recipes/add_scaling_heuristic.md): workflow for selecting a reference configuration, defining a scaling heuristic, running IsoFLOP sweeps, and validating a ladder.
- [`experiments/references/reference_scaling_suite.py`](https://github.com/marin-community/marin/blob/1d274b52c636b6f2a9177b1d4c14b2f74795a8a6/experiments/references/reference_scaling_suite.py): executable scaling-suite pattern.
- [`experiments/references/completed_adamh.py`](https://github.com/marin-community/marin/blob/1d274b52c636b6f2a9177b1d4c14b2f74795a8a6/experiments/references/completed_adamh.py): dense AdamH scaling heuristic.
- [`experiments/grug/moe/heuristic.py`](https://github.com/marin-community/marin/blob/1d274b52c636b6f2a9177b1d4c14b2f74795a8a6/experiments/grug/moe/heuristic.py): current MoE heuristic; inspect its run context and date before treating formulas as defaults.
- [`docs/reproducibility/pretraining-source-pool.md`](https://github.com/marin-community/marin/blob/1d274b52c636b6f2a9177b1d4c14b2f74795a8a6/docs/reproducibility/pretraining-source-pool.md): source-pool accounting and provenance.
- [`docs/reproducibility/delphi-seed-repeats.md`](https://github.com/marin-community/marin/blob/1d274b52c636b6f2a9177b1d4c14b2f74795a8a6/docs/reproducibility/delphi-seed-repeats.md): seed-repeat methodology for the Delphi ladder.
- [`docs/reports/hero-mixture-log.md`](https://github.com/marin-community/marin/blob/1d274b52c636b6f2a9177b1d4c14b2f74795a8a6/docs/reports/hero-mixture-log.md): a record of mixture decisions and observed results.
- [`lib/levanter/src/levanter/data/mixture.py`](https://github.com/marin-community/marin/blob/1d274b52c636b6f2a9177b1d4c14b2f74795a8a6/lib/levanter/src/levanter/data/mixture.py): implementation of mixture sampling behavior.
- [`lib/marin/src/marin/scaling_laws/isoflop_analysis.py`](https://github.com/marin-community/marin/blob/1d274b52c636b6f2a9177b1d4c14b2f74795a8a6/lib/marin/src/marin/scaling_laws/isoflop_analysis.py): IsoFLOP fitting and optimal-configuration analysis.

## Local web reports

- [Delphi scaling suite](marin/2026-delphi-an-open-scaling-suite/article.md)
- [Marin data pipeline overview](marin/2026-marin-data-pipeline-overview/article.md)
- [Marin pretraining efficiency follow-up](marin/2026-marin-pretraining-efficiency/article.md)

Treat the reports as evidence about particular configurations and as pointers to reproducible code. A current implementation heuristic is not automatically a recommendation for another architecture, optimizer, data mix, or scale range.

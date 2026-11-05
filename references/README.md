# Reference collection status

73 technical-report/paper folders, plus 12 web/code/data-artifact reference folders.

LaTeX source results: {'downloaded': 72, 'not_arxiv': 1}.
Code archive results (per reference; shared repositories can appear more than once): {'downloaded': 162, 'unavailable': 37}.

References are grouped by topic, then readable year/title folder names. Identifiers remain in metadata and directory-map.json. ArXiv folders contain `paper.pdf`, extracted `paper.txt`, `metadata.json`, an `arxiv-source.tar` download, extracted `source/`, and discovered code archives under `code/`. Source archives may be gzip-compressed despite the `.tar` suffix. Unversioned arXiv requests resolve at collection time; do not assume they match an earlier paper version.

Code discovery uses paper text, abstracts, and LaTeX links. These can include baselines, evaluation suites, and data tooling. An archive is evidence of code availability, not evidence of a complete training reproduction. Default-branch archives are current snapshots; inspect experiment-specific revisions before running them. Large downloads are capped by the collector and explicitly reported below.

[Source inventory](SOURCES.md) · [Machine-readable manifest](download-manifest.json) · [Marin reading map](MARIN-READING.md)

## Remaining code download failures

- `data/2024-nemotron-cc`: [https://github.com/EleutherAI/lm-evaluation-](https://github.com/EleutherAI/lm-evaluation-) — 404 Client Error: Not Found for url: https://codeload.github.com/EleutherAI/lm-evaluation-/zip/HEAD
- `data/2024-nemotron-cc`: [https://github.com/NVIDIA/TensorRT-LLM](https://github.com/NVIDIA/TensorRT-LLM) — exceeds 30000000 byte collection limit
- `evaluation/2024-ruler-whats-the-real-context-size-of-your-long-context-language-models`: [https://github.com/gkamradt/LLMTest](https://github.com/gkamradt/LLMTest) — 404 Client Error: Not Found for url: https://codeload.github.com/gkamradt/LLMTest/zip/HEAD
- `model-reports/2024-deepseek-v3-technical-report`: [https://github.com/NVIDIA/TransformerE](https://github.com/NVIDIA/TransformerE) — 404 Client Error: Not Found for url: https://codeload.github.com/NVIDIA/TransformerE/zip/HEAD
- `model-reports/2024-deepseek-v3-technical-report`: [https://github.com/NVIDIA/cutlas](https://github.com/NVIDIA/cutlas) — 404 Client Error: Not Found for url: https://codeload.github.com/NVIDIA/cutlas/zip/HEAD
- `model-reports/2024-deepseek-v3-technical-report`: [https://github.com/WildEval/ZeroEval](https://github.com/WildEval/ZeroEval) — exceeds 30000000 byte collection limit
- `model-reports/2024-deepseek-v3-technical-report`: [https://github.com/meta-llama/llama-m](https://github.com/meta-llama/llama-m) — 404 Client Error: Not Found for url: https://codeload.github.com/meta-llama/llama-m/zip/HEAD
- `model-reports/2024-olmoe-open-mixture-of-experts`: [https://github.com/allenai/OLMo](https://github.com/allenai/OLMo) — exceeds 150000000 byte collection limit
- `model-reports/2024-olmoe-open-mixture-of-experts`: [https://github.com/databricks/dbrx](https://github.com/databricks/dbrx) — 404 Client Error: Not Found for url: https://codeload.github.com/databricks/dbrx/zip/HEAD
- `model-reports/2024-olmoe-open-mixture-of-experts`: [https://github.com/mlfoundations/dclm](https://github.com/mlfoundations/dclm) — exceeds 30000000 byte collection limit
- `model-reports/2024-the-llama-3-herd-of-models`: [https://github.com/meta-llama/PurpleLlama](https://github.com/meta-llama/PurpleLlama) — exceeds 30000000 byte collection limit
- `model-reports/2024-the-llama-3-herd-of-models`: [https://github.com/meta-llama/llama-agentic-system](https://github.com/meta-llama/llama-agentic-system) — exceeds 30000000 byte collection limit
- `model-reports/2025-kimi-k2-technical-report`: [https://github.com/laude-institute/terminal-bench](https://github.com/laude-institute/terminal-bench) — exceeds 30000000 byte collection limit
- `model-reports/2025-kimi-k2-technical-report`: [https://github.com/promptfoo/promptfoo](https://github.com/promptfoo/promptfoo) — exceeds 30000000 byte collection limit
- `model-reports/2025-nemotron-3-nano`: [https://github.com/NVIDIA-NeMo/Gym](https://github.com/NVIDIA-NeMo/Gym) — exceeds 30000000 byte collection limit
- `model-reports/2025-nemotron-3-nano`: [https://github.com/NVIDIA-NeMo/Nemotron](https://github.com/NVIDIA-NeMo/Nemotron) — exceeds 30000000 byte collection limit
- `model-reports/2025-nemotron-3-nano`: [https://github.com/laude-institute/terminal-bench](https://github.com/laude-institute/terminal-bench) — exceeds 30000000 byte collection limit
- `model-reports/2025-olmo-2-technical-report`: [https://github.com/allenai/OLMo](https://github.com/allenai/OLMo) — exceeds 150000000 byte collection limit
- `model-reports/2025-olmo-2-technical-report`: [https://github.com/pytorch/pytorch](https://github.com/pytorch/pytorch) — exceeds 30000000 byte collection limit
- `model-reports/2025-olmo-3-technical-report`: [https://github.com/marin-community/marin](https://github.com/marin-community/marin) — exceeds 30000000 byte collection limit
- `model-reports/2025-olmo-3-technical-report`: [https://github.com/tatsu-lab/alpaca_eval](https://github.com/tatsu-lab/alpaca_eval) — exceeds 30000000 byte collection limit
- `model-reports/2025-olmo-3-technical-report`: [https://github.com/ShishirPatil/gorilla](https://github.com/ShishirPatil/gorilla) — exceeds 30000000 byte collection limit
- `model-reports/2026-nemotron-3-super`: [https://github.com/NVIDIA-NeMo/Gym](https://github.com/NVIDIA-NeMo/Gym) — exceeds 30000000 byte collection limit
- `model-reports/2026-nemotron-3-super`: [https://github.com/NVIDIA-NeMo/Nemotron](https://github.com/NVIDIA-NeMo/Nemotron) — exceeds 30000000 byte collection limit
- `model-reports/2026-nemotron-3-ultra`: [https://github.com/NVIDIA-NeMo/Gym](https://github.com/NVIDIA-NeMo/Gym) — exceeds 30000000 byte collection limit
- `model-reports/2026-nemotron-3-ultra`: [https://github.com/NVIDIA-NeMo/Nemotron](https://github.com/NVIDIA-NeMo/Nemotron) — exceeds 30000000 byte collection limit
- `model-reports/2026-nemotron-3-ultra`: [https://github.com/harbor-framework/harbor](https://github.com/harbor-framework/harbor) — exceeds 30000000 byte collection limit
- `model-reports/2026-olmo-core-3-technical-report`: [https://github.com/NVIDIA/cutlass](https://github.com/NVIDIA/cutlass) — exceeds 30000000 byte collection limit
- `model-reports/2026-olmo-core-3-technical-report`: [https://github.com/allenai/open-instruct](https://github.com/allenai/open-instruct) — exceeds 30000000 byte collection limit
- `model-reports/2026-olmo-core-3-technical-report`: [https://github.com/pytorch/pytorch](https://github.com/pytorch/pytorch) — exceeds 30000000 byte collection limit
- `optimization/2018-an-empirical-model-of-large-batch-training`: [https://github.com/tensorflow/models](https://github.com/tensorflow/models) — exceeds 30000000 byte collection limit
- `optimization/2025-fantastic-pretraining-optimizers`: [https://github.com/marin-community/marin](https://github.com/marin-community/marin) — exceeds 30000000 byte collection limit
- `optimization/2026-weight-decay-improves-language-model-plasticity`: [https://github.com/allenai/OLMo](https://github.com/allenai/OLMo) — exceeds 150000000 byte collection limit
- `optimization/2026-weight-decay-improves-language-model-plasticity`: [https://github.com/th789/wd-plasticity](https://github.com/th789/wd-plasticity) — exceeds 30000000 byte collection limit
- `scaling-laws/2022-chinchilla-compute-optimal-training`: [https://github.com/google/BIG-bench](https://github.com/google/BIG-bench) — exceeds 30000000 byte collection limit
- `scaling-laws/2024-a-hitchhikers-guide-to-scaling-law-estimation`: [https://github.com/IBM/ColPret](https://github.com/IBM/ColPret) — exceeds 30000000 byte collection limit
- `scaling-laws/2025-gemstones-width-depth-scaling`: [https://github.com/mcleish7/gemstone-scaling-laws](https://github.com/mcleish7/gemstone-scaling-laws) — exceeds 30000000 byte collection limit

## Recollecting

From the repository root, run `python scripts/collect_references.py`, then `python scripts/collect_reference_code.py`, then `python scripts/summarize_references.py` and `python scripts/build_reference_catalog.py`. The source-code pass searches extracted LaTeX for links lost in PDF text extraction. Existing downloads are reused. Review metadata before replacing or updating snapshots.

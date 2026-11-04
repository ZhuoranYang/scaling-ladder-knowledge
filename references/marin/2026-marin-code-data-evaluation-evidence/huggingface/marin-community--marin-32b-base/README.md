---
license: apache-2.0
datasets:
- allenai/dolmino-mix-1124
- allenai/olmo-mix-1124
- bigcode/starcoderdata
- EleutherAI/proof-pile-2
- hltcoe/megawika
- nvidia/Nemotron-CC
- HuggingFaceTB/finemath
- marin-community/ar5iv-warning-markdown
- marin-community/datashop-science-qa
- marin-community/stackexchange-markdown
- marin-community/wikipedia-markdown
- common-pile/stackv2_edu_filtered
- marin-community/megamath
language:
- en
tags:
- text-generation
library_name: transformers
---

<img alt="Marin Logo" src="https://huggingface.co/datasets/marin-community/blog-images/resolve/main/marin-boat.jpg" width="96" style="margin-left:'auto' margin-right:'auto' display:'block'">


# Model Card for Marin 32B

This is the model card for the Marin 32B base model. [The Marin Project](https://marin.community) is a collaborative effort to develop open-source foundation models.

## Datasets

### Datasets used in Marin 32B Base

Marin 32B Base was trained in multiple phases that reused our 8B recipe and introduced new high-quality cooldown data:

- [Nemotron-CC](https://data.commoncrawl.org/contrib/Nemotron/Nemotron-CC/index.html) (medium, medium_low, medium_high, low_actual, low_synth, hq_actual, hq_synth)
- [Starcoder Data](https://huggingface.co/datasets/bigcode/starcoderdata)
- [Proofpile 2](https://huggingface.co/datasets/EleutherAI/proof-pile-2)
- [FineMath](https://huggingface.co/datasets/HuggingFaceTB/finemath) 3+
- [Dolma](https://huggingface.co/datasets/allenai/dolma) components accessed via Dolmino, including:
  - [peS2o](https://huggingface.co/datasets/allenai/peS2o)
  - [FLAN](https://arxiv.org/abs/2109.01652)
  - StackExchange mixtures
  - Wikipedia slices
- [Marin Markdownified StackExchange](https://huggingface.co/datasets/marin-community/stackexchange-markdown)
- [Marin Markdownified Wikipedia](https://huggingface.co/datasets/marin-community/wikipedia-markdown)
- [Marin Markdownified Ar5iv](https://huggingface.co/datasets/marin-community/ar5iv-warning-markdown)
- [Marin Datashop Science QA](https://huggingface.co/datasets/marin-community/datashop-science-qa)
- [MegaMath](https://arxiv.org/abs/2504.02807) (web, text_code_block, web_pro, translated_code, QA splits)
- [Common Pile Stack V2 EDU (filtered Python)](https://huggingface.co/datasets/common-pile/stackv2_edu_filtered)

The `Markdownified` datasets are licensed under the original licenses of the individual documents.
Please refer to [StackExchange](https://stackoverflow.com/help/licensing),
[Wikipedia](https://en.wikipedia.org/wiki/Wikipedia:Database_download),
and [arXiv](https://arxiv.org/help/license) for more information.

The Datashop Science QA dataset is licensed under [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).

## Checkpoints

### Base Model Checkpoints

Main Page: [marin-community/marin-32b-base](https://huggingface.co/marin-community/marin-32b-base)

`main` currently refers to the `mantis` revision.

## Installation

Marin 32B follows a Llama-style transformer architecture with QK-Norm attention (matching the Qwen3 32B backbone) and works out-of-the-box with the [Hugging Face Transformers](https://huggingface.co/docs/transformers/index) library and other libraries that support Llama/Qwen-style causal language models.

We use the [stanford-crfm/marin-tokenizer](https://huggingface.co/stanford-crfm/marin-tokenizer/) tokenizer.

## Inference

You can use Marin 32B with the standard Hugging Face Transformers library:

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
marin = AutoModelForCausalLM.from_pretrained("marin-community/marin-32b-base", device_map="auto")
tokenizer = AutoTokenizer.from_pretrained("marin-community/marin-32b-base")
message = ["The Marin wind is"]
inputs = tokenizer(message, return_tensors="pt", return_token_type_ids=False)
response = marin.generate(**inputs, max_new_tokens=100, do_sample=True, top_k=50, top_p=0.95)
print(tokenizer.batch_decode(response, skip_special_tokens=True)[0])
```

### Model Description

- **Developed by:** The Marin community team.
- **Model type:** Transformer-style autoregressive language model.
- **Knowledge Cutoff:** To the best of our knowledge, the base model has no data from later than July 2024.
- **Language(s) (NLP):** English
- **License:** The code and model are released under Apache 2.0.
- **Contact:** `dlwh at stanford.edu`

### Model Sources

- **Project Page:** https://marin.community
- **Repositories:**
    - Core repo (data and experiment management): https://github.com/marin-community/marin
    - Training code: https://github.com/stanford-crfm/levanter
- **Retrospective:** https://marin.readthedocs.io/en/latest/reports/marin-32b-retro/
- **W&B Logs:** [Marin 32B](https://wandb.ai/marin-community/marin/reports/32B-Figures--VmlldzoxNDg0MDM2NQ)


## Evaluation

We evaluate with EleutherAI's [LM Eval Harness](https://github.com/EleutherAI/lm-evaluation-harness) defaults across a standard suite. Numbers may differ from model cards or other evaluation harnesses due to prompt/format differences. “Average” is a simple mean over the shown tasks.

| Model                                | Average | AGI Eval LSAT-AR | ARC Easy | ARC Challenge | BoolQ | CommonSense QA | COPA | HellaSwag | lambada_openai | OpenBookQA | PIQA | WinoGrande | WSC | MMLU | GPQA | BBH | MMLU Pro | HumanEval | GSM8K | MATH |
|--------------------------------------|--------:|-----------------:|---------:|--------------:|------:|---------------:|-----:|----------:|---------------:|-----------:|-----:|-----------:|----:|-----:|-----:|----:|---------:|---------:|------:|-----:|
| **Marin 32B (Mantis)**               |   65.2 |            24.8 |    88.0 |          65.7 |  89.4 |           82.8 | 93.0 |     86.9 |           77.2 |       46.4 | 85.9 |      79.3 | 79.5 | 74.7 | 34.0 | 59.6 |     45.1 |     42.7 |  69.1 | 15.3 |
| Marin 32B (Bison)                    |   63.0 |            23.4 |    87.8 |          65.8 |  88.9 |           82.3 | 94.0 |     86.6 |           77.4 |       46.6 | 86.1 |      78.6 | 82.4 | 72.9 | 32.1 | 55.2 |     41.9 |     29.3 |  54.7 | 10.4 |
| OLMo 2 32B Base                      |   63.2 |            22.6 |    85.9 |          61.9 |  83.0 |           78.6 | 93.0 |     85.9 |           78.3 |       47.2 | 83.1 |      78.9 | 86.8 | 71.9 | 32.2 | 56.1 |     42.0 |     23.8 |  76.4 | 12.7 |
| Qwen 2.5 32B Base                    |   68.1 |            30.4 |    80.8 |          55.9 | 87.7 |           88.5 | 87.0 |     84.1 |           77.6 |       44.4 | 82.4 |      75.7 | 81.0 | 80.8 | 39.0 | 67.4 |     57.9 |     48.8 |  89.3 | 36.3 |
| Gemma 3 27B PT                       |   65.1 |            22.2 |    88.2 |          65.4 | 87.1 |           73.4 | 93.0 |     83.0 |           78.1 |       45.0 | 84.1 |      79.0 | 91.9 | 75.3 | 35.7 | 61.4 |     49.4 |     17.6 |  82.0 | 25.8 |
| NVIDIA Nemotron Nano 12B v2 Base     |   68.6 |            28.7 |    83.6 |          60.6 | 84.8 |           76.1 | 85.0 |     81.4 |           72.9 |       45.8 | 82.8 |      74.4 | 85.4 | 77.9 | 36.6 | 62.0 |     53.1 |     59.2 |  84.1 | 68.3 |

The Mantis cooldown improves coding (HumanEval) and math (GSM8K, MATH) performance dramatically compared with the earlier Bison cooldown while maintaining competitive accuracy across general-language benchmarks.

## Model Details

Please see [our technical retrospective](https://marin.readthedocs.io/en/latest/reports/marin-32b-retro.html) for more details on the pretraining process.

### Architecture Details

- **Architecture:** Qwen3-style 32B with QK-Norm attention
- **Hidden size:** 5120
- **Feedforward size:** 27648
- **Number of layers:** 64
- **Number of attention heads:** 40
- **Number of KV heads:** 8
- **Sequence length:** 4096

### Tokenizer Details

Marin 32B uses the [stanford-crfm/marin-tokenizer](https://huggingface.co/stanford-crfm/marin-tokenizer/). It has the same vocabulary as Llama 3 but bundles a chat template into the base tokenizer for convenience.

### Training Phases

- Phase 1 \- Baseline: [#1295](https://github.com/marin-community/marin/issues/1295) [`exp1295_32b`](https://github.com/marin-community/marin/blob/5e88b5253975ffd13e63a5db0b946883c8660e1b/experiments/tootsie/exp1295_32b.py) [Data Browser Link](https://marin.community/data-browser/experiment/?path=gs%3A//marin-us-central2/experiments/exp859_big_tootsies-e9092f.json)
- Phase 2a \- Necromancy Restart: [#1390](https://github.com/marin-community/marin/issues/1390) [`exp1390_32b_necro`](https://github.com/marin-community/marin/blob/fe373c233ee7288cbf8e7600765c3fc6fb6fa3ac/experiments/tootsie/exp1390_32b_necro.py) [Data Browser Link](https://marin.community/data-browser/experiment/?path=gs%3A//marin-us-central2/experiments/exp1380_32b_necro-51ba55.json)
- Phase 2b \- Optimizer Swap (Muon): [#1380](https://github.com/marin-community/marin/issues/1380) [`exp1380_muon32b`](https://github.com/marin-community/marin/blob/fe373c233ee7288cbf8e7600765c3fc6fb6fa3ac/experiments/tootsie/exp1380_muon32b.py) [Data Browser Link](https://marin.community/data-browser/experiment/?path=gs%3A//marin-us-central2/experiments/exp1380_muon32b-898f42.json)
- Phase 3 \- QK\-Norm Switch: [#1395](https://github.com/marin-community/marin/issues/1395) [`exp1395_qwen3_32b`](https://github.com/marin-community/marin/blob/fe373c233ee7288cbf8e7600765c3fc6fb6fa3ac/experiments/tootsie/exp1395_qwen3_32b.py) [Data Browser Link](https://marin.community/data-browser/experiment/?path=gs%3A//marin-us-central2/experiments/exp1395_qwen3_32b-de6f47.json)
- Phase 4a \- Bison Cooldown: [#1529](https://github.com/marin-community/marin/issues/1529) [`exp1529_32b_bison_cooldown`](https://github.com/marin-community/marin/blob/main/experiments/tootsie/exp1529_32b_bison_cooldown.py) [Data Browser Link](https://marin.community/data-browser/experiment/?path=gs%3A//marin-us-central2/experiments/exp1529_32b_bison_cooldown-48ddfe.json)
- Phase 4b \- Mantis Cooldown: [#1581](https://github.com/marin-community/marin/issues/1681) [`exp1529_32b_mantis_cooldown`](https://github.com/marin-community/marin/blob/main/experiments/tootsie/exp1529_32b_mantis_cooldown.py) [Data Browser Link](https://marin.community/data-browser/experiment/?path=gs%3A//marin-us-central2/experiments/exp1529_32b_mantis_cooldown-c6f4b0.json)

- Total tokens trained in final artifact: ≈6.437T
- Phase 1: 2.679T
- Phase 3/QK‑Norm: 2.684T
- Phase 4b/Mantis cooldown: 1.074T; excludes diagnostic restarts and the abandoned Bison cooldown attempt.

## Bias, Risks, and Limitations

Like any base language model or fine-tuned model without safety filtering, these models can be prompted to generate harmful or sensitive content. Such content may also be produced unintentionally, especially in cases involving bias, so users should consider the risks when applying this technology. Additionally, many statements from Marin or any LLM can be inaccurate, so responses should be verified.

Marin 32B has not undergone safety tuning or evaluation. We strongly recommend using this model with caution and considering the risks when applying this technology.
In particular, this model is not intended for fully autonomous use.

## Model Card Contact

For errors in this model card, please open an issue in this repository. For technical inquiries, please contact `dlwh at stanford.edu`.

## Acknowledgements

The compute for this model was generously provided by Google's [TPU Research Cloud](https://sites.research.google/trc/about/).
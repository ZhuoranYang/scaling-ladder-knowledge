---
library_name: transformers
license: other
tags:
- llama-factory
- full
- generated_from_trainer
model-index:
- name: sft__magpie-delphi_warmup__delphi-9e19-p33m67__delphi-1e-05__delphi-3e18-p33m67-k
  results: []
---

<!-- This model card has been generated automatically according to the information the Trainer had access to. You
should probably proofread and complete it, then remove this comment. -->

# sft__magpie-delphi_warmup__delphi-9e19-p33m67__delphi-1e-05__delphi-3e18-p33m67-k

This model was trained from scratch on the magpie and the delphi_warmup datasets.

## Model description

More information needed

## Intended uses & limitations

More information needed

## Training and evaluation data

More information needed

## Training procedure

### Training hyperparameters

The following hyperparameters were used during training:
- learning_rate: 1e-05
- train_batch_size: 1
- eval_batch_size: 8
- seed: 42
- distributed_type: multi-GPU
- num_devices: 16
- total_train_batch_size: 16
- total_eval_batch_size: 128
- optimizer: Use OptimizerNames.ADAMW_TORCH_FUSED with betas=(0.9,0.98) and epsilon=1e-08 and optimizer_args=No additional optimizer arguments
- lr_scheduler_type: cosine
- lr_scheduler_warmup_ratio: 0.1
- num_epochs: 1.0

### Training results



### Framework versions

- Transformers 4.57.6
- Pytorch 2.9.1+cu128
- Datasets 4.4.1
- Tokenizers 0.22.2

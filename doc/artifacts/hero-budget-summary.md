## Derived candidate accounting

| Quantity | Looped candidate | Unlooped control |
|---|---:|---:|
| Unique stored parameters (B) | 19.875 | 20.097 |
| One physical traversal active body (B) | 1.953 | 2.876 |
| Executed matrix-equivalent count (B) | 2.929 | 2.876 |
| Training model FLOPs/token (G) | 20.606 | 20.599 |
| KV bytes/token in BF16 | 98,304.000 | 98,304.000 |

These are analytical projections from the candidate JSON, not profiler measurements. FLOPs assume 4,096-token full causal contexts with skipped masked triangles, no activation recomputation or optimizer overhead, and every-layer SwiGLU MoE. Stored parameter counts assume per-channel QK norm and untied embeddings. The matrix-equivalent count is an arithmetic counter, not a unique-parameter count.

## Throughput sensitivity

| Sustained model TFLOP/s/GPU | Productive compute over hero window | Supported looped tokens |
|---:|---:|---:|
| 150 | 5.972e+22 | 2.90T |
| 200 | 7.963e+22 | 3.86T |
| 250 | 9.953e+22 | 4.83T |
| 300 | 1.194e+23 | 5.80T |
| 350 | 1.393e+23 | 6.76T |

The scenarios use the GPU count, hero duration and productive wall-clock fraction from the selected JSON. They are capacity projections, not measured rates.

## Proposed mixture and capacity requirements

| Bucket | Phase 1 | Phase 2 | Total exposures (B tokens) | Epoch cap | Minimum unique pool (B tokens) |
|---|---:|---:|---:|---:|---:|
| cc_medium_actual | 25% | 15% | 1035.0 | 1 | 1035.0 |
| cc_medium_low_actual | 10% | 0% | 360.0 | 1 | 360.0 |
| cc_low_actual_ablation_only | 0% | 0% | 0.0 | 1 | 0.0 |
| cc_medium_high_actual | 15% | 10% | 630.0 | 2 | 315.0 |
| cc_high_actual | 20% | 30% | 990.0 | 3 | 330.0 |
| cc_high_synthetic | 10% | 15% | 495.0 | 2 | 247.5 |
| code_starcoderdata | 15% | 20% | 720.0 | 4 | 180.0 |
| math_proof_pile_2 | 5% | 10% | 270.0 | 6 | 45.0 |

Weights and caps are proposals for testing, not published optimal settings. Totals assume 4.50T tokens and an 80/20 phase split. All minimum pools must be checked after our tokenizer, global deduplication, decontamination and splits.

## Proposed pre-hero GPU ledger

| Experiment stage | Projected GPU-days |
|---|---:|
| trainer qualification reserve | 64.0 |
| reference LR/batch/decay search: 14 S0 + 6 S1 runs x 10B | 18.3 |
| long-horizon LR brackets: 4 S0 x 160B | 28.5 |
| data screen: 8 recipes x 2 seeds x 20B | 14.3 |
| shape/expert screen: 8 x 20B at S1 | 32.3 |
| core ladder with shared stable trunks | 533.1 |
| fresh paired S1 high-TPP holdouts: 2 x 720B | 290.5 |
| fresh finalist replication: 4 x 40B S1 | 32.3 |
| hero-shaped holdout/rehearsal: 10B | 10.6 |
| **Total** | **1023.8** |

Pre-hero estimates use the same 250 model-TFLOP/s/GPU and 90% duty assumptions; small jobs can be slower. The hard cap is 1,280 GPU-days, including contingency. Stop or prune before exceeding it.

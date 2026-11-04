# Tuning LR on MuonH Recipe

Source: https://github.com/marin-community/marin/issues/5951

🤖 ## Goal

Establish an LR scaling law for the MuonH May Recipe of the form

```
LR = m · tokens^(−a) · hidden_dim^(−b) · batch_size^(0.5)
```

so that follow-up experiments (gate 1 / gate 2 ablations) can be launched at the heuristic-optimal LR rather than re-sweeping at every (dim, R).

## Sweeps launched so far

| Sweep group (wandb) | Hidden dim | R (TPP) | LR multipliers | Batch | TPU | Status |
|---|---|---:|---|---:|---|---|
| `muonh-may-recipe-lr-sweep` (main 4-size grid) | 512 | 4, 10, 20, 60, 120, 240 | 0.4, 0.7, 1.0, 1.3, 1.6 | 32 | v5p-? | 30 finished / 30 |
| `muonh-may-recipe-lr-sweep` | 768 | 4, 10, 20, 60, 120, 240 | 0.4, 0.7, 1.0, 1.3, 1.6 | 64 | v5p-? | 23 finished / 5 crashed / 2 running |
| `muonh-may-recipe-lr-sweep` | 1024 | 4, 10, 20, 60, 120, 240 | 0.4, 0.7, 1.0, 1.3, 1.6 | 128 | v5p-? | 15 finished / 13 crashed / 2 running |
| `muonh-may-recipe-lr-d1280-sweep` (incl. R=120/R=240 resubmit) | 1280 | 4, 10, 20, 60, 120, 240 | 0.4, 0.7, 1.0, 1.3, 1.6 | 256 | v5p-32 | 25 finished / 3 crashed / 2 running |
| `muonh-may-recipe-lr-tpp5k-d512-d768-sweep` | 512 | TPP=5000 | 0.2, 0.6, 1.0, 1.5, 2.5 | 256 | v5p-32 | 5 running |
| `muonh-may-recipe-lr-tpp5k-d512-d768-sweep` | 768 | TPP=5000 | 0.2, 0.6, 1.0, 1.5 | 512 | v5p-32 | 3 running / 1 missing |

Total: ~150 runs (R values × LR multipliers × dim).

## Current fit (using cells where all 5 lr_mults finished)

Excluded from the fit: (d=512, R=4), (d=768, R=4) — bowls extrapolate above lr_mult=1.6. All cells with any non-finished run are also dropped.

```
LR = 26.9 · tokens^(−0.395) · dim^(−0.121) · batch_size^(0.5)
```

R² = **0.996** on 17 fit points. See `experiments/grug/moe/may_recipe_lr_law_fit.png` and `experiments/grug/moe/may_recipe_lr_sweep_grid.png` (per-cell sweep grid).

## Next

- Wait for in-flight d=768/1024/1280 cells to clear so we can re-evaluate with more data points.
- TPP=5000 sweep adds two longer-trained points (d512 bs=256, d768 bs=512) — primarily to extend the tokens axis and check that the −0.395 exponent holds under longer training at fixed dim.


## Comment 4546832033 (2026-05-26T17:22:56Z)

In progress fit: 

<img width="2380" height="1392" alt="Image" src="https://github.com/user-attachments/assets/5ca4b036-13f0-4c6d-954c-69177d7f3fb3" />

<img width="2442" height="767" alt="Image" src="https://github.com/user-attachments/assets/d2d16963-ec68-4a35-98b2-a6d113197f5a" />

## Comment 4546975078 (2026-05-26T17:37:08Z)

🤖 New fit landed on `grug_moe_may_recipe` @ `8c09bfac1`.

## Heuristic change (`experiments/grug/moe/heuristic.py`)

| Field | Old (v16 sweep, R²=0.995) | New (May Recipe refit, R²=0.996) |
|---|---|---|
| `lr_coeff` | 0.02547 | **0.09700** |
| `lr_tokens_exp` | −0.2813 | **−0.395** |
| `lr_dim_exp` | −0.3678 | **−0.121** |
| `adamh_ratio` | 13/3 | 13/3 (unchanged) |

Fit form (muonh LR, after `adamh_ratio · adam_lr`):
```
muonh_lr = 26.9 · tokens^-0.395 · dim^-0.121 · batch_size^0.5
```

## Predicted muonh_lr at the README compute-optimal points

| Point | bs | tokens | Old muonh_lr | New muonh_lr | New/Old |
|---|---:|---:|---:|---:|---:|
| d512 / 2.19e17 | 32 | 8.37e8 | 0.01245 | **0.02138** | **1.72×** |
| d768 / 1.70e18 | 64 | 2.71e9 | 0.01090 | **0.01810** | **1.66×** |
| d1024 / 9.00e18 | 128 | 6.63e9 | 0.01078 | **0.01736** | **1.61×** |
| d1280 / 2.83e19 | 256 | 1.24e10 | 0.01178 | **0.01866** | **1.58×** |

The bump shrinks with dim because the new dim exponent (−0.121) is shallower than the old (−0.368) — the old heuristic over-discounted LR for larger models. Token exponent steepens (−0.281 → −0.395), so the per-cell LR drops faster with R, consistent with the bowl-minima trend in the sweep grid.

Anything launched off `grug_moe_may_recipe` now picks up the bumped LR by default.


## Comment 4546990431 (2026-05-26T17:39:05Z)

This is surprising to me that the new fit is changing LR by 60%. When I had ablated the MuonH LR individually, the old LR had seemed better than +-30%. The architecture has seen a couple changes since then such as normalizing the contribution of the routed experts. I'll rerun these sizes under the new LR and see if it performs better.

## Comment 4549326686 (2026-05-26T21:56:59Z)

🤖 Correction: previous fit had a units bug

The earlier post (`lr = 26.9 · tokens^-0.395 · dim^-0.121 · bs^0.5`) used an `_active_params` formula in the fit script that set `intermediate_dim = d * 4`, while the actual `MoeAdamHHeuristic.build_model_config` uses `intermediate_dim ≈ d/2`. So the `tokens = R · p_active` fed to the regression were ~4× too large. With `tokens^-0.395`, that inflated the coefficient `m` by ~`4^0.395 ≈ 1.74×` to compensate.

## Corrected fit

```
muonh_lr = 18.31 · tokens^-0.395 · dim^-0.150 · bs^0.5    (R² = 0.996, 17 fit cells)
```

(`tokens_exp` unchanged at -0.395; `dim_exp` -0.121 → -0.150; `m` 26.9 → 18.31.)

## Verification

Per-cell `new_pred / old_base_lr` should equal observed `opt_lr_mult`:

| d | R | observed `opt_mult` | corrected `new/old` |
|---:|---:|---:|---:|
| 512 | 10 | 1.199 | 1.146 |
| 512 | 20 | 1.032 | 1.059 |
| 512 | 60 | 0.904 | 0.935 |
| 512 | 120 | 0.849 | 0.864 |
| 512 | 240 | 0.811 | 0.799 |
| 768 | 10 | 1.106 | 1.113 |
| 768 | 20 | 1.036 | 1.028 |
| 768 | 60 | 0.921 | 0.908 |
| 1024 | 10 | 1.029 | 1.071 |
| 1024 | 20 | 0.947 | 0.990 |
| 1280 | 10 | 1.036 | 1.052 |
| 1280 | 20 | 0.943 | 0.972 |
| 1280 | 60 | 0.858 | 0.858 |
| 1280 | 120 | 0.817 | 0.793 |

Matches within ~5% across the included cells (vs 1.7–2.2× overshoot before).

## Compute-optimal-point predictions (vs old recipe)

| Point | Old muonh_lr | New (corrected) | new/old |
|---|---:|---:|---:|
| d512 / 2.19e17 | 0.01245 | 0.01214 | 0.98× |
| d768 / 1.70e18 | 0.01090 | 0.01016 | 0.93× |
| d1024 / 9.00e18 | 0.01078 | 0.00967 | 0.90× |
| d1280 / 2.83e19 | 0.01178 | 0.01032 | 0.88× |

So at compute-optimal the new recipe is **slightly below** the old — consistent with the observed `opt_mult ≈ 0.95–1.05` at low-R cells. The earlier "1.6–1.7× bump" claim was an artifact of the units bug.

## Heuristic update

`experiments/grug/moe/heuristic.py` will be updated to:
```
lr_coeff: float = 0.06602   # was 0.09700 (buggy), original 0.025469
lr_tokens_exp: float = -0.395
lr_dim_exp: float = -0.150   # was -0.121 (buggy), original -0.3678
```

(`adamh_ratio = 13/3` unchanged.)

The compute-optimal runs kicked off in `/larry/iris-run-job-20260526-174529` were running with the *buggy* (~1.7× too high) LR — those will be killed and resubmitted with the corrected heuristic.


## Comment 4550305186 (2026-05-27T00:56:05Z)

Corrected chart
<img width="2442" height="767" alt="Image" src="https://github.com/user-attachments/assets/6c678279-48ac-4514-9299-b8bea1a80ced" />

## Comment 4627127660 (2026-06-05T00:33:17Z)

the chart above is a bit deceptive because it does not normalize for batch size, which makes the dependence on model size look stronger than it actually is. Here is the updated plot:

<img width="960" height="660" alt="Image" src="https://github.com/user-attachments/assets/7b96e5e7-f848-4641-80d2-7f869ef686bb" />

## Comment 5434814099 (2026-08-27T05:32:54Z)

This issue has been inactive for 83 days and is marked as stale.
If there is no further activity within 7 days, it will be automatically closed.
If you believe this issue is still relevant, please add a comment to keep it open.

## Comment 5534518936 (2026-09-04T01:48:36Z)

This issue has been automatically closed due to inactivity.
If you believe this issue is still relevant, please reopen it or create a new issue with updated information.
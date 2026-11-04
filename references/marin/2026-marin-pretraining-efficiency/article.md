---
title: "openathena.ai/blog/pretraining-speedup"
source: "https://openathena.ai/blog/pretraining-speedup/"
---

<div class="nav-padding-global">

<div class="nav-inner">

<div class="nav-container">

<a href="/" class="nav-brand" aria-label="Open Athena Home"></a>

<div class="nav-logo">

</div>

<div class="nav-links">

<a href="/projects/" class="nav-link">Projects</a> <a href="/blog/" class="nav-link">Blog</a> <a href="/about/" class="nav-link">About</a>

</div>

<span class="burger-lines"> <span class="burger-line"></span> <span class="burger-line"></span> </span>

</div>

</div>

</div>

<div class="section blog-post">

<div class="blog-post-header">

# Improving our LLM Pretraining Efficiency

<div class="blog-post-meta">

June 3, 2026 · Larry Dial ·

<div class="resource-type-tag">

MARIN

</div>

</div>

</div>

<div class="blog-post-body">

<div class="blog-toc-title">

Contents

</div>

Contents

<div class="blog-post-content project-detail-body">

In [our last post](/blog/delphi/) we covered the Delphi Scaling Suite, where we trained dense models up to 1e23 FLOPs. Since then we've scaled up our Mixture of Experts (MoE) recipe to beyond 100B parameters and 1e23 FLOPs and added several architecture and optimizer improvements. This post first covers the MoE transition, then each subsequent improvement, and closes with several promising future directions.

## Key terms<a href="#key-terms" class="heading-anchor" aria-label="Link to section: Key terms"></a>

- **Theoretical speedup** — counts only model FLOPs, ignoring MFU.
- **Realized speedup** — reflects wall-clock time, accounting for MFU.

Speedups are written as **theoretical** (realized).

## Summary<a href="#summary" class="heading-anchor" aria-label="Link to section: Summary"></a>

Starting from our Dense Baseline, we achieve the following speedups:

- **6.7×** (3.6×) Moving from dense to Marin MoE V1.
- **1.4×** (1.3×) Increasing expert sparsity by raising total experts from 64 to 256.
- **1.3×** (1.25×) Updating our optimizer from AdamH to MuonH.
- **1.2×** (1.2×) Adding partial key offset (PKO).
- **1.04×** (1.04×) Adding routed expert normalization + scaling.

The dense → MoE V1 transition was validated at 1e23 FLOPs. The four subsequent improvements were each measured against MoE V1. We then tested the stacked recipe at 3e19 FLOPs, observing a 2.1× theoretical speedup over MoE V1.

## From Scaling Dense Models to Scaling MoEs<a href="#from-scaling-dense-models-to-scaling-moes" class="heading-anchor" aria-label="Link to section: From Scaling Dense Models to Scaling MoEs"></a>

The primary goal when we transitioned to MoEs was to demonstrate stability and predictability of scaling to over 100 billion parameters. We incorporated the following techniques to accomplish this:

- Added quantile balancing<sup>[1](#fn-1)</sup> to maintain similar token counts across 64 routed experts per layer, 4 of which are active per token. We detail the impact of QB in an earlier post [here](/blog/quantile-balancing/).
- Kept AdamH<sup>[2](#fn-2)</sup> as the optimizer, which constrains the matrix Frobenius norms explicitly instead of relying on weight decay.
- Added a light z-loss on the router logits and final logits.
- Added attention gates<sup>[3](#fn-3)</sup> and gated norms<sup>[4](#fn-4)</sup>, which reduce outlier activations and give a slight speedup.
- Added Exclusive Self Attention<sup>[5](#fn-5)</sup>, which adds another speedup and cleanly lets tokens no-op via a self-attend.

We put extra emphasis on Adam LR tuning, to ensure that future optimizer ablations compare against a tuned baseline. We sweep over model size, token count, and lr in order to fit the form \$lr = A \cdot \text{tokens}^b \cdot \text{dim}^c \cdot \text{bs}^{0.5}\$, derived in Figures 1 and 2. We scale layer count roughly linearly with hidden dim.

<figure>
<img src="/assets/images/blog/pretraining-speedup/lr-bpb-grid.png" alt="Per-cell BPB vs Adam LR with log-quadratic fits across hidden dims and token horizons" />
<figcaption><strong>Figure 1:</strong> The d768 row of the LR sweep, one panel per token horizon. Each panel plots BPB vs Adam LR with a log-quadratic fit. We swept d512, d1024, and d1280 too; their optima feed into Figure 2. (<a href="https://github.com/marin-community/marin/issues/4225">Issue 4225</a>)</figcaption>
</figure>

<figure>
<img src="/assets/images/blog/pretraining-speedup/lr-formula-fit.png" alt="Optimal Adam LR vs tokens fitted to lr = A · tokens^tx · dim^dx · bs^0.5" />
<figcaption><strong>Figure 2:</strong> The 19 per-cell optima fit the form $lr = 1.680 \cdot \text{tokens}^{-0.282} \cdot \text{dim}^{-0.372} \cdot \text{bs}^{0.5}$ with $R^2 = 0.994$. Left: optimal Adam LR (normalized to bs=32) vs tokens, colored by hidden dim, with each dim's slice of the fit shown as a dashed line. Middle: collapsing by hidden dim — multiplying LR by $\text{dim}^{0.372}$ — pulls every dim onto a single $\text{tokens}^{-0.282}$ trend. Right: predicted vs measured optimal LR across all 19 cells. (<a href="https://github.com/marin-community/marin/issues/4225">Issue 4225</a>)</figcaption>
</figure>

An isoFLOP sweep then gives us an optimal 62:1 token:active_parameter ratio for scaling and a pre-registered loss target for a 1e23 run: a 129B-A16B model trained on 1T tokens, which we call Marin MoE V1.

<figure>
<img src="/assets/images/blog/pretraining-speedup/isoflop-curves.png" alt="isoFLOP curves from the baseline sweep: paloma macro loss vs tokens at six compute budgets" />
<figcaption><strong>Figure 3:</strong> isoFLOP curves from sweeping six compute budgets (1e18 to 3e20 FLOPs). Each curve plots paloma macro_loss against tokens for runs at different hidden dims; the dashed line is the per-budget log-token parabolic fit, and the star marks its minimum. (<a href="https://github.com/marin-community/marin/issues/4447">Issue 4447</a>)</figcaption>
</figure>

These choices result in a training run with a smooth loss curve across the entire trajectory.

<figure>
<img src="/assets/images/blog/pretraining-speedup/loss-curve.png" alt="Train cross-entropy loss vs tokens for the 1e23 MoE run" />
<figcaption><strong>Figure 4:</strong> Train cross-entropy loss for the 1e23 MoE run across 1T tokens. The linear trajectory comes from linear LR decay with hyperball after a 10% warmup. (<a href="https://github.com/marin-community/marin/issues/4697">Issue 4697</a>)</figcaption>
</figure>

The final loss of the 1e23 run comes within 1% of our [preregistered prediction](https://github.com/marin-community/marin/issues/4697).

<figure>
<img src="/assets/images/blog/pretraining-speedup/baseline-scaling-curve.png" alt="Baseline scaling curve: paloma macro loss vs compute, with held-out 1e21 and 1e23 runs landing on the fit" />
<figcaption><strong>Figure 5:</strong> Baseline MoE scaling suite. Six isoFLOP-optimal points from 1e18 to 3e20 FLOPs fit $\text{loss} = 1.6 + 95.18 \cdot C^{-0.0941}$. The pre-registered forecast extrapolates 300× past the fit: at 1e21 the predicted 2.598 matches the measured 2.599 to 0.001, and at 1e23 the measured 2.234 lands 0.8% below the predicted 2.252. (<a href="https://github.com/marin-community/marin/issues/4697">Issue 4697</a>)</figcaption>
</figure>

The MoE V1 recipe showed consistent gains over the dense recipe, growing to a speedup of **6.7×** (3.6×) at 1e23.

<figure>
<img src="/assets/images/blog/pretraining-speedup/dense-vs-moe.png" alt="Dense baseline scaling law with MoE points overlaid; horizontal arrows mark the compute the dense law would need to match each MoE loss" />
<figcaption><strong>Figure 6:</strong> Dense vs MoE FLOP efficiency. The dense baseline (blue) is the Delphi AdamH scaling law $\text{loss} = 1.65 + 117.8 \cdot C^{-0.0966}$, fit on the dense isoFLOP optima plus the 1e21/1e22/1e23 held-out runs. MoE points (red) are the isoFLOP optima at 1e18–3e20 and the measured 1e21 and 1e23 runs. Each horizontal arrow extends to the compute the dense law would need to reach the same loss — a ~4× FLOP-efficiency gain across isoFLOP scales that widens to 6.7× at 1e23.</figcaption>
</figure>

## Building on Marin MoE V1<a href="#building-on-marin-moe-v1" class="heading-anchor" aria-label="Link to section: Building on Marin MoE V1"></a>

Now that we had demonstrated predictable scaling, we turned our focus to speeding up learning. We assessed changes across 4 compute scales, comparing to the MoE V1 scaling law, with an emphasis on gains that did not diminish at scale. Runs defaulted to the MoE V1 recipe's compute-optimal budgets and tuned learning rates, making the bar for inclusion conservative. We measured loss as cross-entropy across 16 equally weighted Paloma<sup>[6](#fn-6)</sup> categories including code, wikitext, and general web.

### Expert Sparsity<a href="#expert-sparsity" class="heading-anchor" aria-label="Link to section: Expert Sparsity"></a>

Going from 64 → 128 → 256 routed experts (4 active) shows consistent gains. More experts give the model more capacity to absorb information from the training data, without raising per-token FLOPs.

<figure>
<img src="/assets/images/blog/pretraining-speedup/expert-sparsity.png" alt="Expert sparsity speedup: 128 and 256 expert variants vs the 64-expert baseline across four compute scales" />
<figcaption><strong>Figure 7:</strong> Going from 64 → 128 → 256 routed experts (4 active) at four compute scales. 256 experts gives up to a 1.38× theoretical speedup; the gain grows with compute. (<a href="https://github.com/marin-community/marin/issues/5387">Issue 5387</a>)</figcaption>
</figure>

### MuonH<a href="#muonh" class="heading-anchor" aria-label="Link to section: MuonH"></a>

Adam can be loosely described as "take an equal step size on each parameter, then reactively slow down on unstable ones." Muon<sup>[7](#fn-7)</sup> takes a different approach: for each matrix, it orthogonalizes the gradient before applying it, bounding how much that matrix can change its output for any input. One perspective (of many) on why this helps: layer updates happen simultaneously, so each layer's gradient is computed assuming the others are static. If an earlier layer's update substantially shifts the activations flowing into a later layer, the later layer's gradient was estimated against a distribution that no longer exists.

Similar to the baseline, we apply the hyperball wrapper on the matrices and language-model head as a replacement for weight decay.

<figure>
<img src="/assets/images/blog/pretraining-speedup/muonh.png" alt="MuonH speedup vs AdamH baseline across four compute scales" />
<figcaption><strong>Figure 8:</strong> Swapping AdamH for MuonH yields a 1.29–1.41× theoretical speedup across the four compute scales. We note that the first three scales appear to show decreasing gains. MuonH is included in the recipe because the gain appears to stabilize from the 3rd to 4th scale. Realized speedup is excluded from the chart, as these MuonH tests actually ran faster than the baseline due to being incidentally paired with a kernel improvement. We anticipate roughly a 5% gap between theoretical and realized speedup due to MuonH's lower MFU at scale. (<a href="https://github.com/marin-community/marin/issues/5619">Issue 5619</a>)</figcaption>
</figure>

### Partial Key Offset<a href="#partial-key-offset" class="heading-anchor" aria-label="Link to section: Partial Key Offset"></a>

PKO is a zero-parameter preprocessing of attention keys that gives a 20% gain across all 4 tested compute scales on our evals.

<figure>
<img src="/assets/images/blog/pretraining-speedup/pko.png" alt="PKO + partial RoPE + last-layer variant speedup across four compute scales" />
<figcaption><strong>Figure 9:</strong> PKO (with partial RoPE, last-layer aligned) gives a 1.19–1.24× theoretical speedup across compute scales. (<a href="https://github.com/marin-community/marin/issues/4976">Issue 4976</a>)</figcaption>
</figure>

MoE V1 uses Rotary Positional Embeddings (RoPE). Half of the gain of PKO is attributed to partial RoPE, which limits RoPE to only the first half of the head dims on both queries and keys. Before describing how PKO extends partial RoPE, I will first show examples where the PKO model over- and underperforms partial RoPE at 1e19.

![Wikipedia bio: PKO predicts the d of d'état after the second occurrence of coup](/assets/images/blog/pretraining-speedup/pko-example-wiki.svg)

![LaTeX paper: PKO predicts the open-brace after textit](/assets/images/blog/pretraining-speedup/pko-example-latex.svg)

![C++ switch: PKO loses on predicting Draw after result.WinnerName =](/assets/images/blog/pretraining-speedup/pko-example-cpp.svg)

The motivation for PKO (first used in [modded-nanogpt](https://github.com/KellerJordan/modded-nanogpt/pull/169)) is that a single attention layer can't do "retrieve the continuation of X from earlier context": mechanically the query matches on a key at position \$t\$ but should read the value at \$t+1\$. Forward-shifting all keys by one position fixes this, but breaks classical "find and retrieve X" attention. Under sliding-window attention with partial RoPE, we observe that pattern-matching inductive behavior emerges in the stationary dimensions of the long-window layers, so we restrict the key shift to those dims on only every 4th layer. PKO's gain is much larger on evals than on training loss, suggesting its pattern matching behavior is more robust to distribution shift.

### Routed Expert Normalization and Rescaling<a href="#routed-expert-normalization-and-rescaling" class="heading-anchor" aria-label="Link to section: Routed Expert Normalization and Rescaling"></a>

Marin is open-development: anyone can follow experiments and contribute. Elie Bakouch, a community member, recently noticed a difference between our expert weighting and DeepSeek's<sup>[8](#fn-8)</sup>. Within hours of his suggestion to renormalize and scale the routed expert outputs, we confirmed the small boost and added it to the recipe. Without his recommendation, this improvement would not have made it into our next large scale run. When evaluating the change, we compared to the in-progress recipe indicated by the blue dots below.

<figure>
<img src="/assets/images/blog/pretraining-speedup/routed-expert-norm.png" alt="Routing renorm with X=2.5 vs combined-feature baseline across three compute scales" />
<figcaption><strong>Figure 10:</strong> Renormalizing and rescaling routed expert outputs (X=2.5) over the combined-feature baseline gives a 1.025–1.052× theoretical speedup. (<a href="https://github.com/marin-community/marin/issues/5797">Issue 5797</a>)</figcaption>
</figure>

### Combining all 4<a href="#combining-all-4" class="heading-anchor" aria-label="Link to section: Combining all 4"></a>

Running the same isoFLOP sweep on the new recipe (solid bowls below) shows the compute-optimal point at each budget shifting to more tokens and fewer active parameters, when compared to the Marin MoE V1 recipe. The shift is likely driven by Expert Sparsity: 4× more routed experts giving the model more sparse capacity to absorb information from extra training tokens.

<figure>
<img src="/assets/images/blog/pretraining-speedup/isoflop-compare.png" alt="isoFLOP bowls at four budgets, baseline (dashed) vs combined recipe (solid)" />
<figcaption><strong>Figure 11:</strong> isoFLOP bowls at four shared budgets, baseline (dashed, hollow markers) vs combined recipe (solid, filled markers). Stars mark the parabola-fit minimum of each bowl; arrows show how the optimum shifts toward more tokens and fewer active parameters under the new recipe. (<a href="https://github.com/marin-community/marin/issues/6074">Issue 6074</a>)</figcaption>
</figure>

Stacking all four improvements gives a roughly 2× combined theoretical speedup, compared to the Marin MoE V1 recipe.

<figure>
<img src="/assets/images/blog/pretraining-speedup/combined-speedup.png" alt="Combined-recipe optima vs the baseline scaling curve across four compute budgets" />
<figcaption><strong>Figure 12:</strong> Combined-recipe isoFLOP optima (1e18 → 3e19 FLOPs) sit ~2× to the left of the baseline scaling curve. Each bronze dot is the per-budget loss minimum from a fresh isoFLOP parabolic fit; the horizontal arrow extends to the compute the baseline would need to reach the same loss. (<a href="https://github.com/marin-community/marin/issues/6074">Issue 6074</a>)</figcaption>
</figure>

Recapping the changes:

1.  Moving from dense to MoE V1 gave a **6.7×** (3.6×) speedup at 1e23 FLOPs.
2.  Treating MoE V1 as the baseline, stacking the four subsequent improvements gives a **2.1×** theoretical speedup at 3e19 FLOPs. We don't have data on the exact realized speedup due to shifting hardware mid-experiment, but conservatively estimate it at 1.8×, with slight slowdowns from MuonH and higher expert sparsity.

## Promising Future Directions<a href="#promising-future-directions" class="heading-anchor" aria-label="Link to section: Promising Future Directions"></a>

### Residual Bottleneck<a href="#residual-bottleneck" class="heading-anchor" aria-label="Link to section: Residual Bottleneck"></a>

The standard transformer progressively adds to a single residual stream, slowly transitioning it from single token, to token context, to prediction. A large number of techniques have shown improvements upon this, including attention residuals<sup>[9](#fn-9)</sup>, per-layer embeddings<sup>[10](#fn-10)</sup>, MUDD skip connections<sup>[11](#fn-11)</sup>, manifold hyperconnection<sup>[12](#fn-12)</sup>, and engram<sup>[13](#fn-13)</sup>. Our experiments suggest over 15% speedup is possible, but we're holding off to control the amount of complexity we add to the architecture at each iteration.

A trivial example of caching the residual stream at the 3rd to last layer and feeding it into all subsequent attention modules is shown, to indicate just how many ways it's possible to outperform the standard residual stream behavior. Block attention residuals is included as well.

<figure>
<img src="/assets/images/blog/pretraining-speedup/gate2-speedups.png" alt="Cached attention and block attention residuals (size 4) vs baseline at four compute scales" />
<figcaption><strong>Figure 13:</strong> Two variants vs baseline. Left: cached attention reuses attention output and skips norm computation on cached layers, holding throughput steady and giving a 1.02–1.10× realized speedup. Right: block attention residuals with block size 4 add a softmax-weighted sum over block representations, costing 4–7% throughput but giving a 1.06–1.12× realized speedup. (<a href="https://github.com/marin-community/marin/issues/4987">Issue 4987</a>, <a href="https://github.com/marin-community/marin/issues/5110">Issue 5110</a>)</figcaption>
</figure>

### Inference Efficiency<a href="#inference-efficiency" class="heading-anchor" aria-label="Link to section: Inference Efficiency"></a>

So far the focus has been pretraining intelligence, but another critical axis is inference efficiency, which is important for downstream use and RL. As we grow our RL stack, it will be advantageous to go beyond our current recipe of 4:1 Grouped Query Attention (GQA) with local/global Sliding Window Attention at 3:1 ratio. Promising candidates include multihead latent attention<sup>[14](#fn-14)</sup>, gated delta net<sup>[15](#fn-15)</sup>, LatentMoE<sup>[16](#fn-16)</sup>, multi-token prediction<sup>[17](#fn-17)</sup>, and quantization.

Below: the speedup from reverting 4:1 GQA to full multihead attention. Mechanisms like multihead latent attention may close the quality gap GQA opens while still shrinking the KV cache.

<figure>
<img src="/assets/images/blog/pretraining-speedup/mha-no-gqa.png" alt="MHA (no GQA) vs baseline at four compute scales" />
<figcaption><strong>Figure 14:</strong> Full multihead attention (no GQA) vs the 4:1 GQA baseline at four compute scales. Removing GQA costs 2–4% throughput but improves quality at every scale, giving a 1.10–1.18× realized speedup. (<a href="https://github.com/marin-community/marin/issues/5151">Issue 5151</a>)</figcaption>
</figure>

## Compute Resources<a href="#compute-resources" class="heading-anchor" aria-label="Link to section: Compute Resources"></a>

These experiments were made possible through the generosity of the Google TPU Research Cloud.

<div class="section footnotes">

1.  <div id="fn-1">

    Jianlin Su, [*Quantile Balancing*](https://kexue.fm/archives/11619).<a href="#fnref-1" class="footnote">↩︎</a>

    </div>

2.  <div id="fn-2">

    Wen et al., [*Fantastic Pretraining Optimizers and Where to Find Them — Hyperball Optimization*](https://psychedelic-sunstone-851.notion.site/Fantastic-Pretraining-Optimizers-and-Where-to-Find-Them-2-1-Hyperball-Optimization-2e924306e6f280e7a5ffee00eb40a0dd).<a href="#fnref-2" class="footnote">↩︎</a>

    </div>

3.  <div id="fn-3">

    Qiu et al., [*Gated Attention for Large Language Models: Non-linearity, Sparsity, and Attention-Sink-Free*](https://arxiv.org/abs/2505.06708), 2025.<a href="#fnref-3" class="footnote">↩︎</a>

    </div>

4.  <div id="fn-4">

    Qiu et al., [*A Unified View of Attention and Residual Sinks: Outlier-Driven Rescaling is Essential for Transformer Training*](https://arxiv.org/abs/2601.22966), 2026.<a href="#fnref-4" class="footnote">↩︎</a>

    </div>

5.  <div id="fn-5">

    Zhai, [*Exclusive Self Attention*](https://arxiv.org/abs/2603.09078), 2026.<a href="#fnref-5" class="footnote">↩︎</a>

    </div>

6.  <div id="fn-6">

    Magnusson et al., [*Paloma: A Benchmark for Evaluating Language Model Fit*](https://arxiv.org/abs/2312.10523), 2023.<a href="#fnref-6" class="footnote">↩︎</a>

    </div>

7.  <div id="fn-7">

    Keller Jordan, [*Muon: An optimizer for hidden layers in neural networks*](https://kellerjordan.github.io/posts/muon/), 2024.<a href="#fnref-7" class="footnote">↩︎</a>

    </div>

8.  <div id="fn-8">

    DeepSeek-AI, [*DeepSeek-V3 Technical Report*](https://arxiv.org/abs/2412.19437), 2024.<a href="#fnref-8" class="footnote">↩︎</a>

    </div>

9.  <div id="fn-9">

    Kimi Team, [*Attention Residuals*](https://arxiv.org/abs/2603.15031), 2026.<a href="#fnref-9" class="footnote">↩︎</a>

    </div>

10. <div id="fn-10">

    Google, [*Gemma 4 model card*](https://ai.google.dev/gemma/docs/core/model_card_4).<a href="#fnref-10" class="footnote">↩︎</a>

    </div>

11. <div id="fn-11">

    Xiao et al., [*MUDDFormer: Breaking Residual Bottlenecks in Transformers via Multiway Dynamic Dense Connections*](https://arxiv.org/abs/2502.12170), 2025.<a href="#fnref-11" class="footnote">↩︎</a>

    </div>

12. <div id="fn-12">

    Xie et al., [*mHC: Manifold-Constrained Hyper-Connections*](https://arxiv.org/abs/2512.24880), 2025.<a href="#fnref-12" class="footnote">↩︎</a>

    </div>

13. <div id="fn-13">

    Cheng et al., [*Conditional Memory via Scalable Lookup: A New Axis of Sparsity for Large Language Models*](https://arxiv.org/abs/2601.07372), 2026.<a href="#fnref-13" class="footnote">↩︎</a>

    </div>

14. <div id="fn-14">

    DeepSeek-AI, [*DeepSeek-V2: A Strong, Economical, and Efficient Mixture-of-Experts Language Model*](https://arxiv.org/abs/2405.04434), 2024.<a href="#fnref-14" class="footnote">↩︎</a>

    </div>

15. <div id="fn-15">

    Yang et al., [*Gated Delta Networks: Improving Mamba2 with Delta Rule*](https://arxiv.org/abs/2412.06464), 2024.<a href="#fnref-15" class="footnote">↩︎</a>

    </div>

16. <div id="fn-16">

    Elango et al., [*LatentMoE: Toward Optimal Accuracy per FLOP and Parameter in Mixture of Experts*](https://arxiv.org/abs/2601.18089), 2026.<a href="#fnref-16" class="footnote">↩︎</a>

    </div>

17. <div id="fn-17">

    Gloeckle et al., [*Better & Faster Large Language Models via Multi-token Prediction*](https://arxiv.org/abs/2404.19737), 2024.<a href="#fnref-17" class="footnote">↩︎</a>

    </div>

</div>

<div class="section blog-post-citation" aria-labelledby="cite-heading">

## Cite this post

<div class="blog-post-citation-wrap">

``` blog-post-citation-bibtex
@misc{dial2026_pretraining_speedup,
  author = {Dial, Larry},
  title = {Improving our LLM Pretraining Efficiency},
  year = {2026},
  month = {jun},
  howpublished = {\url{https://www.openathena.ai/blog/pretraining-speedup/}},
  note = {Open Athena Blog}
}
```

<img src="data:image/svg+xml;base64,PHN2ZyBhcmlhLWhpZGRlbj0idHJ1ZSIgY2xhc3M9Imljb24tY29weSIgZmlsbD0iY3VycmVudENvbG9yIiBoZWlnaHQ9IjE2IiB2aWV3Ym94PSIwIDAgMTYgMTYiIHdpZHRoPSIxNiIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cGF0aCBkPSJNNCAyYTIgMiAwIDAgMSAyLTJoOGEyIDIgMCAwIDEgMiAydjhhMiAyIDAgMCAxLTIgMkg2YTIgMiAwIDAgMS0yLTJ6bTItMWExIDEgMCAwIDAtMSAxdjhhMSAxIDAgMCAwIDEgMWg4YTEgMSAwIDAgMCAxLTFWMmExIDEgMCAwIDAtMS0xek0yIDVhMSAxIDAgMCAwLTEgMXY4YTEgMSAwIDAgMCAxIDFoOGExIDEgMCAwIDAgMS0xdi0xaDF2MWEyIDIgMCAwIDEtMiAySDJhMiAyIDAgMCAxLTItMlY2YTIgMiAwIDAgMSAyLTJoMXYxeiIgZmlsbC1ydWxlPSJldmVub2RkIiAvPjwvc3ZnPg==" class="icon-copy" /> <img src="data:image/svg+xml;base64,PHN2ZyBhcmlhLWhpZGRlbj0idHJ1ZSIgY2xhc3M9Imljb24tY2hlY2siIGZpbGw9ImN1cnJlbnRDb2xvciIgaGVpZ2h0PSIxNiIgdmlld2JveD0iMCAwIDE2IDE2IiB3aWR0aD0iMTYiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHBhdGggZD0iTTEzLjg1NCAzLjY0NmEuNS41IDAgMCAxIDAgLjcwOGwtNyA3YS41LjUgMCAwIDEtLjcwOCAwbC0zLjUtMy41YS41LjUgMCAxIDEgLjcwOC0uNzA4TDYuNSAxMC4yOTNsNi42NDYtNi42NDdhLjUuNSAwIDAgMSAuNzA4IDAiIC8+PC9zdmc+" class="icon-check" />

</div>

</div>

</div>

</div>

</div>


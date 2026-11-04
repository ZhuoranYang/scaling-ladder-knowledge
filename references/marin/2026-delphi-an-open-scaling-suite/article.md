---
title: "openathena.ai/blog/delphi"
source: "https://openathena.ai/blog/delphi/"
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

# Scaling Laws That Extrapolate 300× Past the Fit

<div class="blog-post-meta">

May 11, 2026 · Will Held ·

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

In this post, I'll describe the process of developing Delphi, the Marin team's first open scaling suite, inspired by [Pythia](https://www.eleuther.ai/papers-blog/pythia-a-suite-for-analyzing-large-language-modelsacross-training-and-scaling). Delphi has three parts: a scaling recipe that maps compute budgets to model configurations, a scaling suite trained from that recipe on the [Google TPU Research Cloud](https://sites.research.google/trc/about/), and a scaling law that uses the smaller Delphi models to predict the larger ones. We release the checkpoints, training mixture, and recipe so Delphi can serve as a new resource for scaling studies. A pre-registered forecast from the scaling law predicted the final loss of the largest Delphi run (1e23 FLOPs, 25B parameters, 600B tokens) within 0.2%, extrapolating 300× past the largest run used in the fit.

<figure class="plotly-figure-block" style="margin:1.75rem 0;">
<div class="plotly-frame-outer" style="background-color:#d0c1b3;padding: 1rem;border-radius:14px;">
<div class="plotly-frame-title" style="font-family:var(--font-heading);color:var(--text);font-size:1.05rem;font-weight:600;letter-spacing:0.01em;text-align:center;">
Delphi's scaling law, from small runs to frontier-scale compute
</div>
<div class="plotly-frame-inner" style="background-color:#f1e8df;padding: 0;border-radius:10px;">
<div class="plotly-figure" aria-label="Delphi&#39;s scaling law, from small runs to frontier-scale compute. The Delphi scaling law was fit on seven IsoFLOP optima at 3e18 to 3e20 FLOPs; held-out runs at 1e21, 1e22, and 1e23 land within 0.5% of the fit. Past 1e23 the dashed curve is pure extrapolation — where it places Marin 32B, Kimi K2.5, DeepSeek V4, GPT-4, Opus, and GPT-5 is just the same law continued forward. Compute estimates for closed-weight models are drawn from Epoch AI&#39;s large-scale AI models database." data-plotly-src="/assets/images/blog/delphi/extrapolation.json" role="img" style="min-height:460px;">

</div>
</div>
</div>
<figcaption>The Delphi scaling law was fit on seven IsoFLOP optima at 3e18 to 3e20 FLOPs; held-out runs at 1e21, 1e22, and 1e23 land within 0.5% of the fit. Past 1e23 the dashed curve is pure extrapolation — where it places Marin 32B, Kimi K2.5, DeepSeek V4, GPT-4, Opus, and GPT-5 is just the same law continued forward. Compute estimates for closed-weight models are drawn from Epoch AI's large-scale AI models database.</figcaption>
</figure>

**Summary**

- Our first attempt produced a scaling law that looked clean on the small runs but diverged when extrapolated 30× past them.
- The fix to our recipe was a token-horizon correction to the learning rate and other hyperparameters, along with a new optimizer that removed weight decay from the hyperparameter search.
- With this updated recipe, the fit predicted the loss of a 1e23 FLOP run within 0.2%, and smaller held-out runs at 1e21 and 1e22 landed within 0.5% across multiple random seeds.
- The same process forecast downstream benchmarks—MMLU, HumanEval, and GSM8K—via a two-step regression procedure combining compute and observational scaling laws.
- All checkpoints, fit coefficients, and the recipe are publicly released, along with scripts that deterministically reproduce the training mixture (Nemotron-CC, StarCoderData, and ProofPile 2) from public sources.

## How do you decide what to train at scale?<a href="#how-do-you-decide-what-to-train-at-scale" class="heading-anchor" aria-label="Link to section: How do you decide what to train at scale?"></a>

Suppose you have one year and a couple thousand accelerators to train a language model. What model should you train?

This is not one decision, but many. You need an architecture, a data mixture, a batch size, learning rates, momentum terms, parameter initializations, and a host of other details. Even with a large allocation, you cannot afford to test all of your options by running full-scale experiments.

Instead, if you want these decisions to be empirically grounded, you have to use smaller-scale runs as proxies. There is good news and bad news here. The bad news is that performance is scale-dependent: the best configuration at small scale is not necessarily the best configuration at large scale. The good news is that performance is often surprisingly predictable as a function of compute. A **scaling law** is an empirical relationship between a resource, such as training FLOPs, and an outcome, such as validation loss. With a stable scaling law, small runs can tell us something about larger runs we have not trained yet.<sup>[1](#fn-1)</sup>

But a scaling law by itself does not solve our problem. It does not tell us how to train models; it only tells us what happens after we have chosen a way of assigning models and hyperparameters at each compute budget. That assignment is a **scaling recipe**: a mapping from compute to a full training configuration. A recipe says, for example, how model width, depth, batch size, learning rate, and training duration should change as compute increases.

This shifts the experimental question. Instead of asking whether one particular model configuration is good, we ask whether a recipe produces good models across scale. A recipe is useful when it is both competitive and predictable: competitive because the models it trains have low loss, and predictable because the scaling law fit on smaller runs continues to describe larger ones. Building such a recipe means combining theory, empirical tuning, and judgment where the theory is incomplete.

With a recipe in hand, we can produce a **scaling suite**: a set of models trained with the same recipe at increasing compute budgets. A scaling suite is a reusable research resource. It lets the community study the effects of model, data, and compute scaling without doing their own training. Pythia and other open scaling suites have already been used this way for a range of downstream scientific questions, including memorization ([Carlini et al., 2022](https://arxiv.org/abs/2202.07646)), training-trajectory analysis ([Xia et al., 2023](https://aclanthology.org/2023.acl-long.767/)), the emergence of downstream evaluations ([Michaud, 2023](https://ericjmichaud.com/quanta/)), how next-token predictions form layer by layer ([Belrose et al., 2023](https://arxiv.org/abs/2303.08112)), and model provenance ([Kuditipudi et al., 2025](https://arxiv.org/abs/2510.19796)).

Delphi expands on three axes for open-scaling suites: scale, capability, and comparison. It raises the top range in compute, model size, and training tokens; brings meaningful in-context learning capabilities into view; and makes the recipe itself a falsifiable baseline that other groups can compare against at whatever scale they can afford.

## Scaling recipe procedure<a href="#scaling-recipe-procedure" class="heading-anchor" aria-label="Link to section: Scaling recipe procedure"></a>

A scaling recipe starts with a reference model, a small model which you can exhaustively tune, and aims to generalize its hyperparameters in a functional form. The inputs are model size and token budget. The output is the full training configuration: architecture, batch size, learning rate, optimizer settings, schedule, and initialization. This makes hyperparameter transfer part of the experiment. If every run in the suite comes from the same recipe, then a misbehaving run points back to the recipe itself, rather than to a single table entry.

The symbols used throughout the recipe are summarized below. Quantities without subscripts describe the run being generated; quantities with a \$0\$ subscript come from the reference model.

Symbols and Fields

| Quantity | Symbol / field |
|----|----|
| **Input** |  |
| Compute budget | \$C\$ |
| Sequence length | \$\ell\$ |
| Model width | \$H\$ |
| **Reference tuning** |  |
| Reference batch size | \$B_0\$ |
| Reference duration | \$T_0\$ |
| Reference projection learning rate | \$\eta_0\$ |
| Reference scalar learning rate | \$\eta\_{0,\mathrm{Adam}}\$ |
| Reference epsilon | \$\varepsilon_0\$ |
| **Derived scale** |  |
| Parameter count | \$N\$ |
| Training duration | \$T\$ |
| **Output** |  |
| Training steps | steps |
| Model depth | layers |
| Attention shape | heads |
| Batch size | \$B\$ |
| Learning rate | \$\eta\$ |
| Momentum terms | \$\beta_1\$, \$\beta_2\$ |
| Numerical stability | \$\varepsilon\$ |
| Gradient clipping | max grad norm |
| Regularization | weight decay |
| Initialization | init std |
| **Held fixed across the suite** |  |
| Architecture family | Qwen 3 |
| Tokenizer | Llama 3 |
| Data mixture | Nemotron-CC + StarCoderData + ProofPile 2 |
| LR schedule | WSD, 10% warmup, 0 floor |
| Mixed precision | f32 params, bf16 compute |
| Parallelism | FSDP |

The recipe is then tested through IsoFLOP sweeps. An IsoFLOP sweep trains several models at the same compute budget, changing the tradeoff between model size and training duration throughout. For example, one point in the grid might be a smaller model trained on more tokens, while another is a larger model trained on fewer tokens. For each budget from 3e18 to 3e20 FLOPs, Delphi trains [Qwen 3](https://arxiv.org/abs/2505.09388) architecture models on a mixture of [Nemotron-CC](https://data.commoncrawl.org/contrib/Nemotron/Nemotron-CC/index.html), [StarCoderData](https://huggingface.co/datasets/bigcode/starcoderdata), and [ProofPile 2](https://huggingface.co/datasets/EleutherAI/proof-pile-2), sweeping model size while adjusting token count to keep compute fixed. The best configuration at each budget is called "compute-optimal." From the compute-optimal points, we can fit a power law between compute and performance and use it to forecast larger runs.<sup>[2](#fn-2)</sup>

## Delphi attempt 1: How can scaling laws go wrong?<a href="#delphi-attempt-1-how-can-scaling-laws-go-wrong" class="heading-anchor" aria-label="Link to section: Delphi attempt 1: How can scaling laws go wrong?"></a>

The first Delphi attempt followed published scaling recipes where they existed. The basic pattern was to start from an existing model in Marin, tuned via grid search,<sup>[3](#fn-3)</sup> then transfer outward through prescriptions that depend on hidden dimension \$H\$, batch size \$B\$, and training duration \$T\$. In that first recipe, learning rate scaled with batch size and width per [muP (Yang et al., 2022)](https://arxiv.org/abs/2203.03466), depth followed a log-corrected ratio from the depth-to-width scaling literature ([Levine et al., 2020](https://arxiv.org/abs/2006.12467)), and batch size targeted a fixed step count.

Inside that grid, the seven IsoFLOP buckets from 3e18 to 3e20 FLOPs looked healthy. Each traced a parabola with a relatively clear minimum, and the asymptotic power law through those minima fit cleanly. Then the 1e22 held-out run missed the forecast by 2.5%, and the 1e23 run diverged. Scale-dependence and predictability can coexist, but only if the recipe captures the right scale-dependence. This initial attempt did not!

<figure class="plotly-figure-block" style="margin:1.75rem 0;">
<div class="plotly-frame-outer" style="background-color:#d0c1b3;padding: 1rem;border-radius:14px;">
<div class="plotly-frame-title" style="font-family:var(--font-heading);color:var(--text);font-size:1.05rem;font-weight:600;letter-spacing:0.01em;text-align:center;">
The initial Cautious AdamC recipe
</div>
<div class="plotly-frame-inner" style="background-color:#f1e8df;padding: 0;border-radius:10px;">
<div class="plotly-figure" aria-label="The initial Cautious AdamC recipe. Left: at each compute budget, I train a range of (model size, training duration) pairs totaling the same FLOPs and fit a parabola in (log tokens, loss). Its minimum (×) is the compute-optimal point for that budget. Right: the scaling-law fit on those optima (left of the vertical divider in the panel) extrapolated to held-out 1e21, 1e22, and 1e23 runs (right of the divider). The 1e22 miss and the diverged 1e23 run are what forced the rewrite in the next section." data-plotly-src="/assets/images/blog/delphi/first-ladder.json" data-plotly-src-mobile="/assets/images/blog/delphi/first-ladder-mobile.json" role="img" style="min-height:380px;">

</div>
</div>
</div>
<figcaption>Left: at each compute budget, I train a range of (model size, training duration) pairs totaling the same FLOPs and fit a parabola in (log tokens, loss). Its minimum (×) is the compute-optimal point for that budget. Right: the scaling-law fit on those optima (left of the vertical divider in the panel) extrapolated to held-out 1e21, 1e22, and 1e23 runs (right of the divider). The 1e22 miss and the diverged 1e23 run are what forced the rewrite in the next section.</figcaption>
</figure>

## Delphi attempt 2: How do you fix a broken scaling suite?<a href="#delphi-attempt-2-how-do-you-fix-a-broken-scaling-suite" class="heading-anchor" aria-label="Link to section: Delphi attempt 2: How do you fix a broken scaling suite?"></a>

When a single run fails, especially partway through, it often makes sense to rescue it, like we did with [Marin 32B](https://marin.readthedocs.io/en/latest/reports/marin-32b-retro/). When a scaling suite fails, though, you have to suppress this instinct! Instead you want to identify which part of the recipe to change, and you need a way to tell whether the new recipe works using only your small-scale runs. Here the 1e22 miss and the 1e23 divergence both showed up at longer training durations than anything inside the IsoFLOP grid. That pushed me to focus on the parts of the recipe most likely to break as the token horizon increased.

The main problem was likely the learning rate. A common prescription is to scale learning rate up with the square root of batch size ([Malladi et al., 2022](https://arxiv.org/abs/2205.10287)), often alongside retuning optimizer settings like \$\beta_2\$ as batch size changes ([Marek et al., 2025](https://arxiv.org/abs/2507.07101)). To try and diminish step count as a confound, I had the suite configured to try to keep step count roughly constant by scaling batch size unless the learning rate grew beyond 0.01. This meant that the larger, data-heavy runs used very large batch sizes and, correspondingly, relatively large learning rates.

Those learning rates already looked too large to me, meaning that either the batch size was too large or there was a missing scaling factor on the learning rate. Marin 32B—where hyperparameters were tuned more by eye—used even larger batch sizes with a learning rate more than 10× lower, and it was largely spike free once we swapped to the Qwen 3 architecture. As such, I felt that finding the right adjustment to the learning rate scaling recipe was the right intervention to pursue.

A second problem was weight decay, the critical regularizer in LLM training. I had left it pinned at 0.1 across every run, so it scaled with neither training length nor model width. In retrospect, this was probably not the cause of the loss spikes, but it was clearly suboptimal.

With those two red flags in view, I set out to replace the recipe with one that had more principled prescriptions for both, especially for models trained over longer token horizons. When I reran the small-scale IsoFLOPs, I was less focused on improving the compute-optimal point itself than on improving the extremes, since those were the runs most likely to reveal whether I had actually fixed the token-scaling problem.

### AdamH and a token-horizon LR recipe<a href="#adamh-and-a-token-horizon-lr-recipe" class="heading-anchor" aria-label="Link to section: AdamH and a token-horizon LR recipe"></a>

The final recipe combines two ideas and one process change. First, I changed the optimizer to reduce the number of parameters we needed to tune. Second, I adopted a method for transferring hyperparameters. Finally, I used a more efficient process to search for optimal hyperparameters.

For the optimizer, I replaced Cautious AdamC<sup>[4](#fn-4)</sup> with **[AdamH](https://whenwen.github.io/wd_blog/public/hyperball-part-1.html)** (Adam with Hyperball), developed in Marin by [Kaiyue Wen](https://whenwen.github.io/). AdamH constrains every projection weight to stay on the Frobenius-norm sphere it was initialized on, so weight decay has nothing to regularize away and falls out of the recipe. Kaiyue had already shown inside Marin that AdamH transfers hyperparameters across width and depth better than Adam—width-stability is also why Delphi's learning rate recipe has no \$\frac{1}{H}\$ factor.

AdamH Update Rule

Given the standard Adam update direction \$u_t = \frac{m_t}{\sqrt{v_t} + \varepsilon}\$ for projection weight \$W\$, AdamH replaces the \$W \leftarrow W - \eta\\u_t\$ step with

<div class="math-block">

\$\$ \begin{aligned} \widetilde{W} &= W - \eta\\u_t\\\frac{\\W\\\_F}{\\u_t\\\_F}, \\ W &\leftarrow \frac{\\W\\\_F}{\\\widetilde{W}\\\_F}\\\widetilde{W}. \end{aligned} \$\$

</div>

The first line takes a step whose Frobenius norm matches \$\eta\\W\\\_F\$ regardless of \$\\u_t\\\_F\$, and the second line projects back onto the sphere of radius \$\\W\\\_F\$ so the weight norm is preserved exactly.

The figure below replicates Kaiyue's width-scaling sweep at fixed depth: each curve is one hidden dimension from 128 to 1024, swept across learning rates. Under Adam, the best learning rate drifts left as width grows. Under AdamH, the best learning rate stays more bounded, which is the property that lets the recipe keep \$\eta_0\$ fixed across the widths in our IsoFLOP buckets.

<figure class="plotly-figure-block" style="margin:1.75rem 0;">
<div class="plotly-frame-outer" style="background-color:#d0c1b3;padding: 1rem;border-radius:14px;">
<div class="plotly-frame-title" style="font-family:var(--font-heading);color:var(--text);font-size:1.05rem;font-weight:600;letter-spacing:0.01em;text-align:center;">
Optimal learning rate under Adam vs AdamH
</div>
<div class="plotly-frame-inner" style="background-color:#f1e8df;padding: 0;border-radius:10px;">
<div class="plotly-figure" aria-label="Optimal learning rate under Adam vs AdamH. Loss vs learning rate at fixed depth (num_layers=4) for hidden dimensions from 128 to 1024, on Kaiyue Wen&#39;s small-model sweep over C4-en. Stars mark the per-width optimum and the dashed line connects them in width order. Under Adam the optimum slides toward smaller learning rates as width grows; under AdamH it stays near the same learning rate across the sweep." data-plotly-src="/assets/images/blog/delphi/hparam-transfer.json" data-plotly-src-mobile="/assets/images/blog/delphi/hparam-transfer-mobile.json" role="img" style="min-height:400px;">

</div>
</div>
</div>
<figcaption>Loss vs learning rate at fixed depth (num_layers=4) for hidden dimensions from 128 to 1024, on Kaiyue Wen's small-model sweep over C4-en. Stars mark the per-width optimum and the dashed line connects them in width order. Under Adam the optimum slides toward smaller learning rates as width grows; under AdamH it stays near the same learning rate across the sweep.</figcaption>
</figure>

For hyperparameter transfer across training duration, I revisited recent work from Apple that gives a set of prescriptions I have seen referred to as Complete(d)P.<sup>[5](#fn-5)</sup> Unlike our initial recipe, which focused mostly on width and batch-size scaling, Complete(d)P adds prescriptions for how hyperparameters should change with training duration. In particular, it says learning rate should decrease as the number of tokens seen during training increases. Delphi uses a \$\left(\frac{T_0}{T}\right)^{0.3}\$ correction, which matched my intuitions: it prescribes a lower learning rate for our largest runs without contradicting the widely used \$\sqrt{B}\$ prescription for a fixed token count.<sup>[6](#fn-6)</sup>

While weight decay and the token-horizon term are the load-bearing changes, I also used this opportunity to retune the reference model with [Vizier](https://oss-vizier.readthedocs.io/en/latest/), Google's Gaussian-process-based optimizer. Vizier suggests new hyperparameter settings by fitting a model to the trials it has already seen, which makes it more efficient for modeling several interacting hyperparameters at once. The full recipe and a side-by-side calculator are below.

Full Recipe Comparison and Hyperparameter Calculator

The table below lists the full scaling recipe side by side with the earlier one. For the reference run, \$B_0 = 64\$, \$T_0 = 2.5\text{B}\$ tokens, \$\eta_0 = 0.00630\$, \$\eta\_{0,\mathrm{Adam}} = 0.000656\$, and \$\varepsilon_0 = 1.85\times 10^{-8}\$. For initialization, \$d\_{\mathrm{in}}\$ is the input dimension of each linear map: \$H\$ for attention and MLP up/gate projections, and \$4H\$ for the MLP down projection.

| Hyperparameter | Delphi attempt 1: initial recipe | Delphi attempt 2: updated recipe |
|----|----|----|
| weight decay | \$0.1\$ | removed by AdamH |
| learning rate (projections) | \$\frac{0.33\sqrt{B}}{H}\$ | \$\eta_0\\\sqrt{\frac{B}{B_0}}\\\left(\frac{T_0}{T}\right)^{0.3}\$ |
| learning rate (scalars, embeddings) | same as projections | \$\eta\_{0,\mathrm{Adam}}\\\sqrt{\frac{BT_0}{B_0T}}\$ |
| \$\beta_1\$ | \$0.95\$ | \$0.9\$ |
| \$\beta_2\$ | \$0.98^{B/B_0}\$ | \$\mathrm{clip}\\\left(0.9999^{B/B_0},\\ 0.9,\\ 0.9999\right)\$ |
| \$\varepsilon\$ | \$10^{-15}\$ | \$\varepsilon_0\\\sqrt{\frac{B_0T}{BT_0}}\$ |
| max grad norm | \$1.0\$ | \$0.1\$ |
| depth | \$\frac{H}{64 + 4\log_2 H - 9}\$ | \$\frac{H}{64 + 4\log_2 H - 9}\$ |
| heads | \$\frac{H}{128}\$ | \$\frac{H}{128}\$ |
| batch size | \$\frac{T}{\ell \cdot 2^{16}}\$ | \$\frac{T}{\ell \cdot 2^{16}}\$ |
| init std (projections) | \$\frac{1}{\sqrt{d\_{\mathrm{in}}}}\$ | \$\frac{1}{\sqrt{d\_{\mathrm{in}}}}\$ |
| init std (embeddings) | \$\frac{1}{H}\$ | \$\frac{1}{H}\$ |

The calculator below instantiates both recipes for any hidden dimension, token budget, and batch size. The reference constants stay fixed to the tuned Delphi values above.

<div id="delphi-recipe-calculator" class="recipe-calculator">

| Model width \$H\$ | Training duration \$T\$ | Batch size \$B\$ |
|----|----|----|
| <span class="small"></span> | <span class="small"></span> | <span class="small"></span> |

| Hyperparameter                 | Delphi attempt 1 | Delphi attempt 2 |
|--------------------------------|------------------|------------------|
| weight decay                   |                  |                  |
| \$\eta\$ (proj)                |                  |                  |
| \$\eta\$ (scalar)              |                  |                  |
| \$\beta_1\$                    |                  |                  |
| \$\beta_2\$                    |                  |                  |
| \$\varepsilon\$                |                  |                  |
| max grad norm                  |                  |                  |
| layers                         |                  |                  |
| heads                          |                  |                  |
| steps                          |                  |                  |
| init (\$d\_{\mathrm{in}}=H\$)  |                  |                  |
| init (\$d\_{\mathrm{in}}=4H\$) |                  |                  |
| init (embed)                   |                  |                  |

</div>

At fixed batch size, the \$\left(\frac{T_0}{T}\right)^{0.3}\$ term lowers the projection learning rate for longer training runs. When batch size grows with token count, the batch-size and token-horizon terms trade off, which is the interaction the recipe is meant to make explicit.

The remaining constants are shared across both recipes. Delphi uses a Qwen 3 architecture with MLP ratio 4, sequence length 4096, a 10% linear warmup, and a 20% linear decay to zero. If you'd rather read code than formulas, the two recipes live side by side in the Marin repo: [c_adamc.py](https://github.com/marin-community/marin/blob/main/experiments/scaling_law_sweeps/c_adamc.py) for the first recipe and [completed_adamh.py](https://github.com/marin-community/marin/blob/main/experiments/scaling_law_sweeps/completed_adamh.py) for Delphi.

### An empirical sanity check on the new recipe<a href="#an-empirical-sanity-check-on-the-new-recipe" class="heading-anchor" aria-label="Link to section: An empirical sanity check on the new recipe"></a>

In order to empirically validate that this recipe led to near-optimal configurations at multiple scales, I ran experiments to find tuned hyperparameters across two hidden dimensions, four batch sizes, and three token horizons. These 24 settings serve as a "test set" for our recipe, allowing us to see how well the recipe's configuration maps to costly hyperparameter tuning at each setup. Here, I visualize the results for each hyperparameter with a Gaussian-process partial-dependence curve<sup>[7](#fn-7)</sup> with the goal of observing how close the empirical optimal is to the recipe recommendation.

<figure class="plotly-figure-block" style="margin:1.75rem 0;">
<div class="plotly-frame-outer" style="background-color:#d0c1b3;padding: 1rem;border-radius:14px;">
<div class="plotly-frame-title" style="font-family:var(--font-heading);color:var(--text);font-size:1.05rem;font-weight:600;letter-spacing:0.01em;text-align:center;">
Vizier sanity check on the AdamH scaling recipe
</div>
<div class="plotly-frame-inner" style="background-color:#f1e8df;padding: 0;border-radius:10px;">
<div class="plotly-figure" aria-label="Vizier sanity check on the AdamH scaling recipe. The blue curve is the Gaussian-process partial-dependence estimate for one hyperparameter after averaging over the others. The shaded band is its posterior uncertainty. The blue rug at the bottom shows which values Vizier actually sampled in that cell. The black &lt;code&gt;x&lt;/code&gt; marks the Complete(d)P AdamH heuristic value. Use the dropdowns to choose the batch size, hidden dimension, and token horizon." data-plotly-src="/assets/images/blog/delphi/hparam-scaling.json" data-plotly-src-mobile="/assets/images/blog/delphi/hparam-scaling-mobile.json" role="img" style="min-height:560px;">

</div>
</div>
</div>
<figcaption>The blue curve is the Gaussian-process partial-dependence estimate for one hyperparameter after averaging over the others. The shaded band is its posterior uncertainty. The blue rug at the bottom shows which values Vizier actually sampled in that cell. The black <code>x</code> marks the Complete(d)P AdamH heuristic value. Use the dropdowns to choose the batch size, hidden dimension, and token horizon.</figcaption>
</figure>

If the recipe is scaling well, the × should land inside the low-loss region of each curve. Since Delphi largely follows Complete(d)P, this grid acts as a sanity check that its prescription agrees reasonably well with what we measure at the scales we can actually run.

## Delphi attempt 2 forecasts 1e23 to within 0.2%<a href="#delphi-attempt-2-forecasts-1e23-to-within-02" class="heading-anchor" aria-label="Link to section: Delphi attempt 2 forecasts 1e23 to within 0.2%"></a>

The second Delphi attempt scaling law was fit on the same 3e18 to 3e20 FLOP IsoFLOP budgets as first Delphi attempt, then used to forecast held-out runs at 1e21, 1e22, and 1e23 FLOPs. At 1e21, the run landed +0.5% over the forecast. At 1e22, the miss dropped from 2.5% under Delphi attempt 1 to +0.2%. At 1e23, the run that diverged under the first recipe now ran to completion and landed at +0.2%.

The figure shows both parts of the result. In the right panel, all three held-out points sit on the continuation of the fit, even though the fitted IsoFLOP budgets stop at 3e20 FLOPs. In the left panel, Delphi attempt 2 sits below the first recipe at every overlapping point on every IsoFLOP parabola, with gaps ranging from about 0.01 to 0.15 loss. The parabola shapes are otherwise similar, which suggests the main effect is not a new compute-optimal allocation but a recipe that transfers more cleanly across scale. At the 3e20 bucket, Delphi attempt 2 still beats a compute-optimal Delphi attempt 1 run even when it trains at about 0.51× or 1.97× its own compute-optimal token count.

<figure class="plotly-figure-block" style="margin:1.75rem 0;">
<div class="plotly-frame-outer" style="background-color:#d0c1b3;padding: 1rem;border-radius:14px;">
<div class="plotly-frame-title" style="font-family:var(--font-heading);color:var(--text);font-size:1.05rem;font-weight:600;letter-spacing:0.01em;text-align:center;">
The Delphi (AdamH) recipe
</div>
<div class="plotly-frame-inner" style="background-color:#f1e8df;padding: 0;border-radius:10px;">
<div class="plotly-figure" aria-label="The Delphi (AdamH) recipe. Left: at each compute budget, I train a range of (model size, training duration) pairs totaling the same FLOPs and fit a parabola in (log tokens, loss). Its minimum (×) is the compute-optimal point for that budget. Right: the scaling-law fit on those optima (left of the divider) extrapolated to held-out 1e21, 1e22, and 1e23 runs (right of the divider)." data-plotly-src="/assets/images/blog/delphi/delphi-ladder.json" data-plotly-src-mobile="/assets/images/blog/delphi/delphi-ladder-mobile.json" role="img" style="min-height:380px;">

</div>
</div>
</div>
<figcaption>Left: at each compute budget, I train a range of (model size, training duration) pairs totaling the same FLOPs and fit a parabola in (log tokens, loss). Its minimum (×) is the compute-optimal point for that budget. Right: the scaling-law fit on those optima (left of the divider) extrapolated to held-out 1e21, 1e22, and 1e23 runs (right of the divider).</figcaption>
</figure>

### Predictions are accurate for downstream evals as well<a href="#predictions-are-accurate-for-downstream-evals-as-well" class="heading-anchor" aria-label="Link to section: Predictions are accurate for downstream evals as well"></a>

There is reasonable consensus that pretraining loss follows predictable power laws with compute. Downstream metrics are less settled. Some studies find clean aggregate scaling ([Gadre et al., 2024](https://arxiv.org/abs/2403.08540)), while others report individual tasks that look erratic, emergent, or noisy ([Lourie, Hu, and Cho, 2025](https://arxiv.org/abs/2507.00885)). Delphi gives us a way to study this question at the same ablation scale used for loss: hold the recipe fixed, vary compute, and ask whether benchmark performance can be forecast from the smaller runs.

The main issue is that the usual benchmark scores are discrete summaries of a continuous model. A language model assigns probabilities to sequences. A benchmark score first converts those probabilities into an answer, and then marks the answer right or wrong. For a multiple-choice task such as MMLU, this conversion chooses the option with the highest probability. For a generative task such as HumanEval, it decodes a program and then asks whether that program passes all the tests.

This conversion can hide progress. On a four-choice MMLU question, the score changes only when the correct answer becomes more probable than every distractor. A model may steadily move probability mass toward the right answer, but accuracy will not change until that ordering flips. On HumanEval, pass@1<sup>[8](#fn-8)</sup> stays near zero until the model assigns enough probability to a complete passing program that one appears in a single decoding attempt. In both cases, the underlying probabilities can improve smoothly while the reported score remains flat ([Schaeffer, Miranda, and Koyejo, 2023](https://arxiv.org/abs/2304.15004)).

We therefore fit the scaling law to a soft version of each benchmark. For multiple-choice tasks, we use the log-probability of the correct answer relative to the alternatives. For generative tasks, we use the bits-per-byte assigned to the reference completion, which measures how well the model's distribution compresses the target output. These quantities are still benchmark-specific, but they vary continuously with compute. With a prompt format that reduces surface-form competition ([Holtzman et al., 2021](https://arxiv.org/abs/2104.08315))<sup>[9](#fn-9)</sup>, they give a usable signal across the whole Delphi budget range.

To report the more familiar benchmark scores, we add a second step: an observational projection ([Ruan, Maddison, and Hashimoto, 2024](https://arxiv.org/abs/2405.10938); [Llama 3 technical report, 2024](https://arxiv.org/abs/2407.21783)). We fit a sigmoid that maps soft score to hard score on a pool of public models, then compose that mapping with the Delphi soft-metric scaling law. This lets strong open-weight models establish the empirical relationship between the two measurements, while the Delphi runs determine how the soft measurement changes with compute. The figure below shows the resulting two-step forecast for broad knowledge (MMLU), code generation (HumanEval), and math word problems (GSM8K).

<figure class="plotly-figure-block" style="margin:1.75rem 0;">
<div class="plotly-frame-outer" style="background-color:#d0c1b3;padding: 1rem;border-radius:14px;">
<div class="plotly-frame-title" style="font-family:var(--font-heading);color:var(--text);font-size:1.05rem;font-weight:600;letter-spacing:0.01em;text-align:center;">
Downstream evals across the Delphi suite
</div>
<div class="plotly-frame-inner" style="background-color:#f1e8df;padding: 0;border-radius:10px;">
<div class="plotly-figure" aria-label="Downstream evals across the Delphi suite. Left: soft metric vs compute — per-choice log-prob for MMLU, bits-per-byte for HumanEval and GSM8K. Right: hard metric (accuracy, pass@1, exact-match) vs soft metric, with a sigmoid fit on the external model pool. The hollow &lt;code&gt;×&lt;/code&gt; at 1e25 FLOPs is the two-step forecast (scaling law + sigmoid). All numbers are for pure base models without midtraining, SFT, or RL. Dropdown switches between MMLU 0-shot / 5-shot, HumanEval 10-shot, and GSM8K 5-shot." data-plotly-src="/assets/images/blog/delphi/mmlu-emergence.json" data-plotly-src-mobile="/assets/images/blog/delphi/mmlu-emergence-mobile.json" role="img" style="min-height:460px;">

</div>
</div>
</div>
<figcaption>Left: soft metric vs compute — per-choice log-prob for MMLU, bits-per-byte for HumanEval and GSM8K. Right: hard metric (accuracy, pass@1, exact-match) vs soft metric, with a sigmoid fit on the external model pool. The hollow <code>×</code> at 1e25 FLOPs is the two-step forecast (scaling law + sigmoid). All numbers are for pure base models without midtraining, SFT, or RL. Dropdown switches between MMLU 0-shot / 5-shot, HumanEval 10-shot, and GSM8K 5-shot.</figcaption>
</figure>

The left panel shows the soft-metric scaling law. Across all three evals, the seven IsoFLOP optima trace a reasonably clean power law, and the 1e21, 1e22, and 1e23 held-out runs land on its continuation. The fits are noisier than the pretraining-loss fit because the downstream targets are smaller and less matched to the training distribution, leaving more room for sampling variance and recency effects.

The right panel shows the observational projection. A sigmoid fit on the external Llama, Qwen, and OLMo pool maps the soft metric into the hard metric. Under that fit, every Delphi checkpoint below roughly 1e21 FLOPs remains near chance: 25% on four-choice MMLU, essentially zero pass@1 on HumanEval, and a few percent exact match on GSM8K. Once the soft metric crosses the task's effective threshold, the hard metric rises to around 60% on MMLU, 19% on HumanEval, and 27% on GSM8K by 1e23 FLOPs. Seen only through the hard metric, the curve looks sudden. Seen through the soft metric underneath, the change is continuous.

This is useful because small pretraining ablations often sit below the scale where the canonical downstream score moves. A 1e19 or 1e20 FLOP experiment may show no visible gain in accuracy or pass@1, even when the model is learning the task better. The soft metric preserves that signal, and the observational projection translates it back into the hard metric at the larger scale where the score becomes interpretable. This allows you to use these benchmarks to guide your experiments, even if you are only training models below the emergence threshold.

## Some side quests<a href="#some-side-quests" class="heading-anchor" aria-label="Link to section: Some side quests"></a>

### Quantifying the cost of leaving compute-optimal<a href="#quantifying-the-cost-of-leaving-compute-optimal" class="heading-anchor" aria-label="Link to section: Quantifying the cost of leaving compute-optimal"></a>

Model configurations were originally termed as compute-optimal if they were configured at a ratio of parameters to tokens that achieve the lowest test loss for a fixed number of training FLOPs, and Delphi inherits that definition. However, broader notions of compute-optimality depend on which costs you choose to include. The most obvious addition is inference cost ([Sardana and Frankle, 2024](https://arxiv.org/abs/2401.00448)). In an increasingly RL-driven world, rollout inference is also part of training cost, and the calculation becomes messier and more organization-specific. Both additions push most teams to "overtrain" by our definition, especially when they train smaller models. Llama 3 8B on 15T tokens is roughly 90× past the compute-optimal ratio, and OLMo 3 7B is roughly 40×. Delphi quantifies the penalty for moving away from compute-optimal, so you can weigh that penalty against the rest of your value function (cf. [McLeish et al., 2025](https://arxiv.org/abs/2502.06857), which makes a parallel argument on a different suite).

<figure class="plotly-figure-block" style="margin:1.75rem 0;">
<div class="plotly-frame-outer" style="background-color:#d0c1b3;padding: 1rem;border-radius:14px;">
<div class="plotly-frame-title" style="font-family:var(--font-heading);color:var(--text);font-size:1.05rem;font-weight:600;letter-spacing:0.01em;text-align:center;">
How much do you pay to move off the optima? (drag the slider)
</div>
<div class="plotly-frame-inner" style="background-color:#f1e8df;padding: 0;border-radius:10px;">
<div class="plotly-figure" aria-label="How much do you pay to move off the optima? (drag the slider). Each AdamH IsoFLOP parabola in gold, with × at the measured compute-optimal point $T^*$ and ○ at the same parabola evaluated at scale·$T^*$. The solid blue line is the compute-optimal regression (asymptotic power-law fit on the × losses); the dashed blue line is the sub-optimal regression, produced by adding an extrapolated overtraining penalty $\Delta(C)$ (fit as a power law on the per-bucket ○−× gaps) to the compute-optimal curve, extended past 1e23 until it reaches the compute-optimal forecast loss. The slider ranges from 0.2× (5× undertrained) to 10× overtrained; the label reports the extra compute an at-scale run would need to match what compute-optimal achieves at 1e23." data-plotly-src="/assets/images/blog/delphi/overtraining-forecast.json" role="img" style="min-height:460px;">

</div>
</div>
</div>
<figcaption>Each AdamH IsoFLOP parabola in gold, with × at the measured compute-optimal point $T^*$ and ○ at the same parabola evaluated at scale·$T^*$. The solid blue line is the compute-optimal regression (asymptotic power-law fit on the × losses); the dashed blue line is the sub-optimal regression, produced by adding an extrapolated overtraining penalty $\Delta(C)$ (fit as a power law on the per-bucket ○−× gaps) to the compute-optimal curve, extended past 1e23 until it reaches the compute-optimal forecast loss. The slider ranges from 0.2× (5× undertrained) to 10× overtrained; the label reports the extra compute an at-scale run would need to match what compute-optimal achieves at 1e23.</figcaption>
</figure>

The dashed line is that penalty extrapolated to 1e23 FLOPs. I fit a power law to the per-bucket ○−× gaps and add it to the compute-optimal curve, using the same asymptotic family and the same seven IsoFLOP buckets as the compute-optimal fit. At 10× overtrained, the dashed line sits at a loss that a compute-optimal configuration would only reach with roughly 6× the compute.

That number deserves less trust than the compute-optimal one. The compute-optimal forecast has held-out validation at 1e21, 1e22, and 1e23, while the suboptimal forecast has none. The ○ points feeding the penalty fit also only reach 2× across the IsoFLOP data, so the 10× column is reading from parabolas well past their data.

Even with that caveat, the figure gives some sense of the penalties labs accept in order to ship strong models at small parameter counts, and by proxy, the benefits open-weights inference providers receive from that investment in overtraining<sup>[10](#fn-10)</sup>.

### Seed spread is 10× tighter than the forecast CI<a href="#seed-spread-is-10-tighter-than-the-forecast-ci" class="heading-anchor" aria-label="Link to section: Seed spread is 10× tighter than the forecast CI"></a>

While the cost of experiment often precludes the study of random seed noise for pretraining, we wanted to follow the best practice established by Pythia of controlling for seeds. We trained three seeds at both 1e21 and 1e22, and all of them landed inside the bootstrap 95% confidence interval of the scaling-law forecast. Their seed-to-seed spread is about 0.1%, which is roughly ten times tighter than the interval itself.

To see how this compares to our expected error, we bootstrap over the compute budgets used to estimate the scaling law. The confidence interval widens as the extrapolation gets longer, growing from ±0.5% at 1e21 to ±4% at 1e23. The observed residual still stays between +0.2% and +0.5% across all three budgets. In that sense, it is promising that the results diverge less than we might expect.

<figure class="plotly-figure-block" style="margin:1.75rem 0;">
<div class="plotly-frame-outer" style="background-color:#d0c1b3;padding: 1rem;border-radius:14px;">
<div class="plotly-frame-title" style="font-family:var(--font-heading);color:var(--text);font-size:1.05rem;font-weight:600;letter-spacing:0.01em;text-align:center;">
Bootstrap forecast CI vs held-out seed observations
</div>
<div class="plotly-frame-inner" style="background-color:#f1e8df;padding: 0;border-radius:10px;">
<div class="plotly-figure" aria-label="Bootstrap forecast CI vs held-out seed observations. The shaded band is the 95% CI of the scaling-law forecast, obtained by resampling the seven AdamH IsoFLOP bucket optima with replacement and refitting the asymptotic power law on each resample. Dots are the individual held-out seed observations at each budget. Both are expressed as percent deviation from the point forecast. Runs within an isoFLOP are correlated, so the bootstrap resamples bucket optima rather than individual runs." data-plotly-src="/assets/images/blog/delphi/lucky-seeds.json" role="img" style="min-height:320px;">

</div>
</div>
</div>
<figcaption>The shaded band is the 95% CI of the scaling-law forecast, obtained by resampling the seven AdamH IsoFLOP bucket optima with replacement and refitting the asymptotic power law on each resample. Dots are the individual held-out seed observations at each budget. Both are expressed as percent deviation from the point forecast. Runs within an isoFLOP are correlated, so the bootstrap resamples bucket optima rather than individual runs.</figcaption>
</figure>

## What's next<a href="#whats-next" class="heading-anchor" aria-label="Link to section: What&#39;s next"></a>

Delphi is meant to be useful beyond the particular results in this post. The checkpoints, fit data, and training mixture make it a standard scaling-suite artifact, and the released recipe adds something more directly editable. Other groups should be able to fork it, vary one part of it, and compare against the baseline recipe at the budgets they can afford.

Delphi is meant to build on the template of Pythia: open checkpoints across many scales, trained under one recipe, so other researchers can study scale without repeating the whole training run. For new studies that would otherwise start from Pythia by default, we hope Delphi is a useful modernized resource: it keeps the same artifact shape while adding a newer architecture, a stronger data mixture, a larger top-end run, and a parametric scaling recipe that can be inspected and modified directly.

As with all of Marin's work, everything is released openly:

- **Checkpoints** for every run, released on Hugging Face at [marin-community/delphi](https://huggingface.co/collections/marin-community/delphi-69f93cbd09845c03b070bae9)
- **Training mixture pipelines** that deterministically reproduce the mix from the public Nemotron-CC, StarCoderData, and ProofPile 2 in the [Marin repo](https://github.com/marin-community/marin/blob/67099b9aa5aa468155f0ce430276be72b39a3bd2/experiments/pretraining_datasets/nemotron.py)
- **Recipe code** as a forkable [`CompletedAdamHParams` class](https://github.com/marin-community/marin/blob/78ae89a5324e09ddd9d0bc39af8565da40cfb3e9/experiments/scaling_law_sweeps/completed_adamh.py#L96) in the Marin repo
- **Development methodology** as the [`add_scaling_heuristic` agent skill](https://github.com/marin-community/marin/blob/main/docs/recipes/add_scaling_heuristic.md) in the Marin repo
- **Plot-ready data** behind every figure in this post, with one config per figure and a `wandb_url` on every row, at [marin-community/delphi-blog-data](https://huggingface.co/datasets/marin-community/delphi-blog-data)

If there's a resource you'd like shared for study that we haven't yet released, let us know on [Discord](https://discord.com/invite/J9CTk7pqcM).

This release was only possible because of the [Google TPU Research Cloud](https://sites.research.google/trc/about/). Open scaling suites require much more compute than a single training run because the IsoFLOP grids, recipe iterations, held-out runs, and seed checks are all part of the artifact. Each is scientifically valuable, but hard to justify as the direct path to the best possible model in the short term. That is part of what made Pythia so valuable, and part of the reason open scaling suites remain rare. TRC made it possible for us to make this investment in Marin's own scaling research and release it as a public resource that we hope helps pay down the open research community's collective science debt.

Delphi fits dense decoder-only transformers, and extending our recipes to MoEs is the next target. Follow [marin#4697](https://github.com/marin-community/marin/issues/4697) to track that work. MoEs are where most frontier compute now goes, and openly released scaling suites should cover them too.

<div class="section footnotes">

1.  <div id="fn-1">

    I like the framing of scaling laws as wind tunnels, which I first saw from the OpenBMB team's [MiniCPM](https://openbmb.vercel.app/minicpm-en) work. Nobody flies a newly designed plane without testing it inside increasingly realistic simulators first. A bad wind tunnel doesn't help you build better planes, it helps you build better toys. Get it right, though, and you can test risky designs before committing to the real flight.<a href="#fnref-1" class="footnote">↩︎</a>

    </div>

2.  <div id="fn-2">

    I used this parabolic IsoFLOP fitting following Approach 2 from Chinchilla. OpenAthena's own Eric Czech did concurrent work on [Approach 2 biases](https://openathena.ai/blog/problems-with-chinchilla-approach-2) which identified subtle issues with this method. If I were to retrain Delphi, I would use his direct parametric fitting instead.<a href="#fnref-2" class="footnote">↩︎</a>

    </div>

3.  <div id="fn-3">

    Kaiyue Wen did a grid search of critical hparams in [Fantastic Pretraining Optimizers and Where to Find Them](https://arxiv.org/abs/2509.02046), which I cargo culted.<a href="#fnref-3" class="footnote">↩︎</a>

    </div>

4.  <div id="fn-4">

    Cautious AdamC is AdamW with two stability patches: AdamC rescales the weight-decay term so it stops inflating gradient norms late in training, and Caution zeros out momentum updates that disagree with the current gradient. Both smooth training, but needing them at all is a tell that the base recipe isn't stable on its own.<a href="#fnref-4" class="footnote">↩︎</a>

    </div>

5.  <div id="fn-5">

    [Complete(d)P](https://machinelearning.apple.com/research/completed-hyperparameter) factorizes stable hyperparameter transfer across width, depth, batch size, and training duration. Its derivation assumes a decoder-only transformer with prenorm and QK-norm, a cosine schedule, and an AdamW-style optimizer, and context-length scaling is explicitly out of scope. Calling those assumptions out matters because Delphi violates some of them — WSD instead of cosine, AdamH instead of AdamW — so the prescriptions aren't guaranteed to transfer, and that is why we modify and empirically revalidate the pieces we change rather than adopting the full recipe wholesale.<a href="#fnref-5" class="footnote">↩︎</a>

    </div>

6.  <div id="fn-6">

    The 0.3 is what a small Vizier hyperparameter grid at my scales pointed to. The per-point basis is weak. While it diverges from Complete(d)P, it agrees with prior empirical results on AdamW from [Bjorck et al.](https://arxiv.org/abs/2407.06324). After Delphi was complete, [Ren et al.](https://arxiv.org/abs/2603.28743) independently found \$\eta \propto T^{-0.320}\$ on MuonH, which corroborates the number on a different Hyperball optimizer.<a href="#fnref-6" class="footnote">↩︎</a>

    </div>

7.  <div id="fn-7">

    I used [Moosbauer et al.](https://proceedings.neurips.cc/paper/2021/file/12ced2db6f0193dda91ba86224ea1cd8-Paper.pdf)'s setup and fit a Gaussian process to the grid samples, then marginalized the posterior over every hyperparameter except one. The resulting curve is the expected loss as a function of that hyperparameter after averaging out the others, and the shaded band is the GP's posterior uncertainty. This lets me show a single curve per cell even though the grid sampled each cell at different combinations of the other axes.<a href="#fnref-7" class="footnote">↩︎</a>

    </div>

8.  <div id="fn-8">

    pass@\$k\$ is the fraction of HumanEval tasks for which at least one of \$k\$ independently sampled completions passes all of the task's unit tests. pass@1 is the single-sample case, equivalent to the probability that one greedy or sampled generation solves the problem. The metric was introduced alongside HumanEval by [Chen et al.](https://arxiv.org/abs/2107.03374).<a href="#fnref-8" class="footnote">↩︎</a>

    </div>

9.  <div id="fn-9">

    Holtzman et al. showed that in multiple-choice evaluation, probability mass on the correct answer gets split across paraphrases and synonyms that aren't in the choice set. Prompt formats that anchor the distribution on the choice strings (e.g., label+option) leak less mass and produce cleaner signal. You can measure how badly a format suffers by checking what fraction of the model's total probability mass falls on the answer choices.<a href="#fnref-9" class="footnote">↩︎</a>

    </div>

10. <div id="fn-10">

    Mike Lewis, who led Llama 3 pretraining at Meta, was direct about this [on Twitter](https://x.com/ml_perception/status/1781021776597942587). "Yes, both the 8B and 70B are trained way more than is Chinchilla optimal - but we can eat the training cost to save you inference cost! One of the most interesting things to me was how quickly the 8B was improving even at 15T tokens."<a href="#fnref-10" class="footnote">↩︎</a>

    </div>

</div>

<div class="section blog-post-citation" aria-labelledby="cite-heading">

## Cite this post

<div class="blog-post-citation-wrap">

``` blog-post-citation-bibtex
@misc{held2026_delphi,
  author = {Held, Will},
  title = {Scaling Laws That Extrapolate 300× Past the Fit},
  year = {2026},
  month = {may},
  howpublished = {\url{https://www.openathena.ai/blog/delphi/}},
  note = {Open Athena Blog}
}
```

<img src="data:image/svg+xml;base64,PHN2ZyBhcmlhLWhpZGRlbj0idHJ1ZSIgY2xhc3M9Imljb24tY29weSIgZmlsbD0iY3VycmVudENvbG9yIiBoZWlnaHQ9IjE2IiB2aWV3Ym94PSIwIDAgMTYgMTYiIHdpZHRoPSIxNiIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cGF0aCBkPSJNNCAyYTIgMiAwIDAgMSAyLTJoOGEyIDIgMCAwIDEgMiAydjhhMiAyIDAgMCAxLTIgMkg2YTIgMiAwIDAgMS0yLTJ6bTItMWExIDEgMCAwIDAtMSAxdjhhMSAxIDAgMCAwIDEgMWg4YTEgMSAwIDAgMCAxLTFWMmExIDEgMCAwIDAtMS0xek0yIDVhMSAxIDAgMCAwLTEgMXY4YTEgMSAwIDAgMCAxIDFoOGExIDEgMCAwIDAgMS0xdi0xaDF2MWEyIDIgMCAwIDEtMiAySDJhMiAyIDAgMCAxLTItMlY2YTIgMiAwIDAgMSAyLTJoMXYxeiIgZmlsbC1ydWxlPSJldmVub2RkIiAvPjwvc3ZnPg==" class="icon-copy" /> <img src="data:image/svg+xml;base64,PHN2ZyBhcmlhLWhpZGRlbj0idHJ1ZSIgY2xhc3M9Imljb24tY2hlY2siIGZpbGw9ImN1cnJlbnRDb2xvciIgaGVpZ2h0PSIxNiIgdmlld2JveD0iMCAwIDE2IDE2IiB3aWR0aD0iMTYiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHBhdGggZD0iTTEzLjg1NCAzLjY0NmEuNS41IDAgMCAxIDAgLjcwOGwtNyA3YS41LjUgMCAwIDEtLjcwOCAwbC0zLjUtMy41YS41LjUgMCAxIDEgLjcwOC0uNzA4TDYuNSAxMC4yOTNsNi42NDYtNi42NDdhLjUuNSAwIDAgMSAuNzA4IDAiIC8+PC9zdmc+" class="icon-check" />

</div>

</div>

</div>

</div>

</div>


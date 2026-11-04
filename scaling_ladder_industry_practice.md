# Running a Scaling Ladder in Practice: Notes from a Conversation

*Distilled from a conversation with the author of "How to Build a Scientific Scaling Ladder." It records how an industry pretraining team runs a ladder, and clears up several points that are easy to misread from papers. Statements are the practitioner's views unless marked **[Note]**, which are my clarifications or caveats.*

---

## 1. The key clarification: two ladders, two different dependent variables

A complete study has **two experimental stages that answer different questions**. Treating them as one stage causes most of the confusion.

| Stage | Dependent variable | Question answered | Needed for the hero run? |
|---|---|---|---|
| **A. Hyperparameter ladder** | $\eta_{\text{opt}}$, $B_{\text{opt}}$ | What are the best LR and batch size at a given $(N, D)$? | **Yes, always** |
| **B. Loss ladder (IsoFLOP)** | Final loss $L$ | How should $N$ and $D$ be split for a given compute, and what loss will we reach? | **Usually no** |

- **The order matters.** The hyperparameter scaling laws come first. Small models are very sensitive to hyperparameters, so if the points in Stage B are not near their optimal LR and batch size, the inflated losses distort the fitted loss law.
- **Stage A alone is enough for industry.** In practice, knowing $\eta_{\text{opt}}(N,D)$ and $B_{\text{opt}}(N,D)$ is sufficient to set up the hero run.
- **Stage B is research on allocation.** It is only needed to find the compute-optimal frontier or to forecast loss. When it is run, it reuses the Stage A laws so that every point is already near-optimally tuned. Re-tuning each IsoFLOP point from scratch would repeat the same work at every point.

### Cheaper alternative (less accurate)

Skip Stage A. Fix the batch size and transfer LR with a $\mu$P-style rule (e.g., $\eta \propto 1/d$ in width $d$), then run the IsoFLOP sweep directly. This gives a usable IsoFLOP curve, but the loss predictions are less trustworthy than with properly tuned points.

---

## 2. Fixed ratio vs. fixed compute: two different slices of $L(N,D)$

There are two distinct ways to slice the loss surface, and they are easy to conflate:

$$
L(N,D) = E + \frac{A}{N^{\alpha}} + \frac{B}{D^{\beta}}, \qquad C \approx 6ND .
$$

**(i) Fixed ratio $r = D/N$ (a ray through the grid).** Then $N = \sqrt{C/(6r)}$ and $D = \sqrt{rC/6}$. The loss becomes a function of $C$ alone:
$$
L = E + A\left(\tfrac{6r}{C}\right)^{\alpha/2} + B\left(\tfrac{6}{rC}\right)^{\beta/2}.
$$
This is the sense in which "the $(N,D)$ law reduces to a compute law."

**[Note]** The result is a single power law $E + G(r)\,C^{-\gamma}$ only if $\alpha = \beta$. Otherwise it is a sum of two powers of $C$, and the term with the smaller exponent dominates asymptotically. Also, runs on a single ray cannot separately identify $\alpha$ and $\beta$ (§4.1 of the main notes).

**(ii) Fixed compute $C$ (an IsoFLOP curve).** Vary $N$ and set $D = C/(6N)$. Loss against $\log N$ is approximately a parabola, and its minimum gives $(N_{\text{opt}}(C), D_{\text{opt}}(C))$. Each IsoFLOP curve is one level set of compute, and different curves correspond to different budgets.

**[Note] Resolving "a fixed size ladder can't give IsoFLOP curves."** It can. With a fixed set of sizes $\{N_i\}$, choose the token count per size as $D_i = C/(6N_i)$. You get one point per size on the IsoFLOP curve at budget $C$. What changes is only that the token horizons are no longer round multiples of Chinchilla. A second option is to fit the full $L(N,D)$ surface on a Cartesian grid and minimize it analytically along $6ND = C$. Both need enough sizes ($\ge 4$–$5$) to locate the parabola's minimum.

---

## 3. How the hyperparameter ladder is built

1. **Fix the size ladder first.** Each ladder version uses a fixed, small set of model sizes. An example progression is 130M → 300M → 520M → ~700M → 2B.
2. **Define sizes through width.** Width is usually chosen from a constrained set of hardware-friendly values (powers of 2 or similar multiples). Depth is then derived to hit the target parameter count. Width is not swept freely the way depth sometimes is.
3. **Fix the token horizons.** For each size, use roughly $0.5\times$, $1\times$, $2\times$, $4\times$ Chinchilla, covering both under- and over-training.
4. **Search in order of sensitivity.** Fit the LR law first, since LR is the most sensitive hyperparameter. Then fit the batch-size law at the fitted LR.
5. **Fit power laws in both $N$ and $D$.** The optimal value depends on both model size and token horizon, e.g. $\eta_{\text{opt}} \propto N^{-a} D^{\pm b}$ and $B_{\text{opt}} \propto D^{c}$.
6. **Re-run when data changes.** Every change of data mixture requires re-searching the hyperparameter laws, because the optima shift with the corpus.

**References.** Step Law (StepFun) and Power Lines (Cerebras). Every lab ends up with its own constants, and published values may not transfer to your setup.

**[Note] Which quantity scales as $D^{0.4\text{–}0.5}$.** In the conversation, the token-horizon exponent of about 0.4–0.5 was attributed to the learning rate. In the published laws, that range belongs to **batch size**: $B_{\text{opt}} \propto D^{0.4}$ in Power Lines and $\propto D^{0.571}$ in Step Law. LR's dependence on $D$ is weaker, and its sign depends on whether $B$ is co-scaled. Fit both on your own ladder rather than assuming either exponent.

---

## 4. Choosing $N$ and $D$ for the hero run

**Industry rarely derives the hero run from an IsoFLOP search.** $(N, D)$ is the solution of a constrained problem, not the unconstrained compute optimum:

- **$D$ is set by data availability.** It depends on what the data team has released, not on a free choice.
- **$N$ is set by product needs and hardware.** Serving cost and deployment constraints decide it, along with training throughput.
- **The ladder is aligned to the hero run.** Ladder runs are placed at the hero run's own $D/N$ ratio, which reduces how much has to be searched.

**Typical regimes:**

- **Very large models sit near $1\times$ Chinchilla.** The token requirement is the binding constraint: a 3T-parameter model would need about 60T tokens at 20 TPP.
- **Small and medium models are heavily over-trained.** gpt-oss is an example; this trades training compute for cheaper inference.

**A practical recipe for a small model** (as discussed for the ~10B-and-below scale):

1. Start from the unique tokens available, $U$. For example, take a downloaded open corpus with its stated token count.
2. Pick an over-training factor $m$, e.g. $m = 10\times$ Chinchilla, giving $\text{TPP} = 20m$.
3. Solve $N \approx U_{\text{eff}} / \text{TPP}$ and check that this $N$ is trainable on your GPUs in acceptable wall-clock.
4. Align the ladder's token horizons to that TPP.

**[Note]** Use effective tokens $U_{\text{eff}}$, after deduplication and with any planned repetition counted, not the corpus's headline count. Headline counts often include synthetic rewrites that overlap with the raw text.

---

## 5. Lessons from Marin's Delphi

- **The first attempt failed.** The large-scale extrapolation diverged.
- **The second attempt succeeded.** The changes described were:
  - adding an LR scaling law in the **token horizon**, i.e. total training tokens;
  - switching optimizers;
  - adding further stability measures.
- **Takeaway:** an extrapolation of about $300\times$ is achievable, but not with a naive recipe. It requires hyperparameter laws in both $N$ and $D$, plus stability work.

**[Note]** The conversation described the optimizer switch as "AdamC → MuonH." The blog post lists Delphi's final optimizer as **AdamH**. Check the Delphi write-up before citing either.

---

## 6. Optimizer: Muon + weight decay vs. MuonH

**Recommendation: use Muon with weight decay ("MuonW").** As of the conversation, large labs had not committed to MuonH.

**Why MuonH can still win (practitioner's explanation, via the River Valley view):**

- **Weight decay is a soft norm constraint.** Early in training the weight norm grows quickly. Since the effective (angular) learning rate scales roughly like $\eta / \lVert W\rVert$, a growing norm makes the effective LR collapse.
- **MuonH constrains the norm to a fixed set.** This keeps the effective LR, i.e. the angular speed of the weights, high through the early and middle phases.
- **Consequence:**
  - *Early phase.* Higher variance gives higher loss, so MuonH appears to lag behind.
  - *After annealing.* A larger annealing gain lets MuonH overtake MuonW at the end.
- **Geometric reading:** MuonH travels farther along the "river" direction and pays for it with more oscillation across the valley walls, which annealing then removes.

**Practical consequence:** a mid-training comparison will favor MuonW. Only compare optimizers at the fully annealed endpoint.

---

## 7. Data for a research ladder

- **Open corpora tried in research ladders:** DCLM (the Fantastic Optimizers configuration), Nemotron-CC, Nemotron-CC-Math, and FineWeb.
- **None is clearly better for loss-based research.** The ladder compares a candidate's final loss against a baseline under a fixed data strategy, so the choice of corpus matters little for that purpose.
- **Data mixture design is a separate job.** It belongs to the data team. The pretraining team's ladder is a research instrument, not a product.
- **The binding rule:** a new mixture means new hyperparameter laws.
- **Marin's pipeline** includes a sophisticated global deduplication step. It is what makes epoch counts meaningful when combining sources.

---

## 8. Evaluation

- Every evaluation checkpoint automatically runs a standard benchmark suite (HellaSwag, math benchmarks, etc.) alongside pretraining loss.
- This harness is built once and runs on every ladder run, not as a separate effort.
- Decisions in the research ladder still rest primarily on pretraining loss.

---

## 9. Infrastructure

- **Do not train with hand-rolled native PyTorch.** Use an established trainer. Megatron-LM is a solid choice; torchtitan is an alternative.

---

## 10. Workflow at a glance

```
1. Fix constraints: available unique tokens U, GPU budget, target serving size
          ↓
2. Choose hero-run (N, D) under those constraints  → target TPP
          ↓
3. Fix ladder sizes (width from a hardware-friendly set, depth derived)
   and token horizons bracketing the target TPP (≈0.5×–4× Chinchilla)
          ↓
4. Hyperparameter ladder: fit LR law, then batch-size law, in (N, D)
          ↓
5. Predict hero-run LR and batch size        ← industry usually stops here
          ↓
6. (Optional research) IsoFLOP / loss ladder using fitted HPs
   → compute-optimal frontier and loss forecast
          ↓
7. On any data-mixture change: return to step 4
```

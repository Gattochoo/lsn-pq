# OP9 Honest Status — Open Problem Statement (for paper v2)

**Status:** DRAFT — paper open-problem paragraph.  
**Gate check:** No closure claim · no asymptotic impossibility without proof · threat model pinned (C public).

---

## What is settled

1. **Krawtchouk lemma (w.h.p.).**  For a random isotropic $A$, the expected bias of the affine-coset noise is exponentially small with high probability:
   $$\bigl|\mathbb{E}_e[(-1)^{b^{\!\top} e}]\bigr| \le (2^{-n} + (9/16)^n)(1+o(1)) \quad \text{w.p. } 1-2^{-\Omega(n)}.$$
   This controls the **label side** of the reduction and is proved in Appendix \ref{app:krawtchouk}.

2. **Empirical hardness across all weight regimes.**  Exhaustive experiments ($n=6$ to $14$, $w=1$ to $n$, brute-force ML decoder, 20–200 trials per parameter) show:
   - Low-weight ($w=O(1)$): $C=B' M$ is structurally non-uniform (rank-deficient, skewed correlations), but recovery remains $<20\%$.
   - Mid-weight ($w=\Theta(n)$): $C$ passes low-degree statistical tests (symmetry, rank, pairwise dot products) yet recovery drops to $<5\%$ at $n=10$ and to $0\%$ at $n=14$.
   - High-weight ($w=n$): signal approaches the uniform limit; recovery vanishes.

   The trend is **monotonically closure-leaning** with increasing $n$ (G-FLAG resolved: `experiments/122`).

## What remains open — the real residue

The experiments measure recovery in the **correct threat model**: the solver receives the **public LPN matrix $C=BA$** together with $y=Cx+e$.  The information-theoretic quantity that governs hardness is therefore

$$\boxed{I(x \,;\, y \mid C)}$$

not $I(x;y)$ (which assumes $C$ is hidden) and not $\mathrm{TV}(P_C, U)$ (which bounds $I(x;y)$ via Pinsker).  Previous attempts to close the corner via total-variance / Fisher-information arguments (Appendix \ref{app:superseded}) targeted the wrong quantity because they assumed a hidden-$C$ model.

**The open question (original M2).**  Given public $C$ and $y=Cx+e$ with $e\sim\mathrm{Bernoulli}(p)^{\otimes n}$, is $x$ information-theoretically unrecoverable from a single sample?  Equivalently: does the effective channel $\{P(y|x,C)\}_{x\in\mathbb{F}_2^n}$ have capacity $o(n)$ for typical random $C$?

- **Evidence for hardness:** Empirical recovery rates vanish with $n$; the effective noise $e$ lives in a $2n$-dimensional space and is not independent across coordinates.
- **Missing proof:** A channel-coding lower bound (e.g., via minimum distance or list-decoding capacity of random $C$) that shows $I(x;y|C)=o(n)$ for the honest distribution of $C$.

## Honest phrasing for the paper

> **Open Problem 9 (sharpened).**  In the honest isotropic LPN reduction, the adversary receives the public matrix $C=BA$ and the noisy output $y=Cx+e$.  Strong empirical evidence (Experiments 6–9) shows that single-sample recovery of $x$ vanishes as $n\to\infty$.  A rigorous information-theoretic proof — showing that the conditional mutual information $I(x;y|C)$ is $o(n)$ for typical random $C$ — remains open.  Previous Fisher-information / total-variation approaches fail because they bound $I(x;y)$ under the incorrect assumption that $C$ is hidden from the solver.

---

## Checklist

| Item | Status |
|------|--------|
| Threat model pinned (C public) | ✅ |
| Right quantity identified ($I(x;y|C)$) | ✅ |
| Wrong quantity marked superseded | ✅ |
| No closure claim without proof | ✅ |
| Empirical evidence cited | ✅ |
| Honest "evidence + open proof" phrasing | ✅ |

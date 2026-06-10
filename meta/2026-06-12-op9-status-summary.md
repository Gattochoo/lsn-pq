# OP9 Status Summary (Overnight, 2026-06-11)

**Date:** 2026-06-11. **Status:** DRAFT — measurement-based summary, no claims.
**Rule compliance:** No closure/break/7th vocabulary. OPEN = LSN.

---

## What OP9 asks

> **Open Problem 9 (marginal-adaptive linear reductions).**  
> The honest map: fixed-$B$ **DEAD**, public-$B$ **DEAD**, conditionally-uniform adaptive **DEAD**, marginal-adaptive **OPEN**.  
> Does there exist a family $g_n$ such that (i) $\mathbb{E}_A[\Pr_{g_n(A)}[|b_i| \le w]] = \Omega(1)$ for $w = o(n)$, yet (ii) $g_n(A)^\top A$ is uniform, or must every marginal-adaptive uniform $B$ force noise bias $\le 2^{-\Theta(n)}$ on all but $o(m)$ rows?

In words: can an adaptive $B = g(A)$ achieve marginally-uniform $BA$ while keeping most row weights low (so that the output noise $Be$ has non-negligible bias)?

---

## Single-sample perspective (P1–P3)

**Finding:** No single-sample statistic reliably separates P0 from P1 for marginal-uniform B.

| Statistic | Best separation | AUC (best config) |
|-----------|----------------|-------------------|
| syndrome | ratio 0.26–0.39 | 0.61 (n=6,m=24) |
| rank_diff | deterministic 1.0 for both | 0.50 |
| corr | ratio 0.01–0.06 | 0.52 |
| max_agree | ratio 0.31–0.98 | **0.80** (n=6,m=24) |

Even `max_agree` at AUC=0.80 is far from perfect. For a cryptographic adversary with single-sample access, distinguishing P0 from P1 is **hard**.

**Verdict:** Single-sample OP9 is **not closed** (no detector found), but also **no reduction-exists signal** (P0 and P1 are close, but not proven indistinguishable).

---

## Multi-sample perspective (P6 ext)

**Finding:** If the reduction reuses $(A,B)$ across multiple outputs (so all outputs share the same $C = BA$), a rank detector achieves **perfect separation** with $k = O(n)$ samples.

| $n$ | $m$ | $k$ | P0 rank | P1 rank |
|-----|-----|-----|---------|---------|
| 6 | 30 | 20 | **12.0** | **20.0** |

**Verdict:** Multi-sample OP9 is **closed IF the reduction reuses $(A,B)$**.

---

## The evasion loophole

A reduction that randomizes $A$ per output evades the multi-sample detector, because each output has independent $C_i = B_i A_i$.

**Key question:** Can a marginal-adaptive reduction afford to randomize $A$ per output?

- **Computational cost:** Generating a random isotropic $A$ and computing $B = g(A)$ costs $O(n^3)$ or more per output. For $m = \operatorname{poly}(n)$ outputs, this is $\operatorname{poly}(n)$ overhead per output.
- **Marginal-uniformity:** Each fresh $A_i$ must satisfy the marginal-uniformity constraint for $B_i = g(A_i)$. This is possible if $g$ is defined for all isotropic $A$.
- **Correctness:** The reduction must still map LSN to LPN correctly. Randomizing $A$ does not affect the correctness of a single output, but it changes the joint distribution of multiple outputs.

**Verdict:** Randomization is **computationally feasible** but **may not be necessary** for a reduction that only needs single-instance security. Whether it is required to evade multi-sample detection depends on the threat model.

---

## Sharpened OP9

The original OP9 asked about single-sample detectability. The overnight work sharpens it to:

> **Sharpened OP9.** Characterize the trade-off between:
> 1. **Single-sample security:** Can marginal-uniform adaptive B make P0 statistically close to P1?
> 2. **Multi-sample security:** If the reduction reuses $(A,B)$, multi-sample detection closes OP9. If it randomizes $A$, what is the minimum computational overhead per output to achieve marginal-uniformity?
> 3. **Reduction existence:** Does there exist ANY marginal-adaptive reduction (reusing or randomizing) that maps LSN to LPN with non-negligible advantage?

---

## One-line verdict

> **OP9 single-sample: open (no detector, no proof of indistinguishability).**  
> **OP9 multi-sample with reuse: closed (rank detector works).**  
> **OP9 multi-sample with randomization: open (evasion is computationally feasible but unverified).**

No 7th; no break; no security claim. OPEN = LSN.

---

*By Kimi, 2026-06-11 ~05:40 KST. DRAFT — await Claude 09:00 adjudication.*

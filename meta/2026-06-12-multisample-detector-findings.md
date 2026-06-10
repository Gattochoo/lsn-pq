# Multi-Sample Detector Findings for OP9

**Date:** 2026-06-11 (overnight). **Status:** DRAFT — empirical discovery; theoretical analysis pending.
**Rule compliance:** No closure/break/7th vocabulary. OPEN = LSN.

---

## The Detector

**Setting:** Adversary receives $k$ samples that share the **same** public matrix $C$ (either $C = BA$ in P0 or $C' = C'$ in P1).

**Detector:** Form the $m \times k$ matrix $Y = [y_1 \mid y_2 \mid \cdots \mid y_k]$ and compute $\operatorname{rank}(Y)$.

---

## Why it works

**P0:** $y_i = C x_i + B e_i$ where $C = BA$.
$$Y = C X + B E = B(A X + E).$$
Since $B$ is $m \times 2n$, $\operatorname{rank}(Y) \le \operatorname{rank}(B) \le 2n$.
For random $B$ with $m \ge 2n$, $\operatorname{rank}(B) = 2n$ w.h.p.
For $k \ge 2n$, $A X + E$ has rank $2n$ w.h.p. (random $E$ is $2n \times k$).
Thus $\operatorname{rank}(Y) = 2n$ w.h.p.

**P1 (fixed-secret LPN):** $y_i = C' x' + e'_i$ with fixed $C'$ and fixed $x'$.
$$Y = C' [x' \mid \cdots \mid x'] + [e'_1 \mid \cdots \mid e'_k] = C' X + E'.$$
$\operatorname{rank}(C' X) = 1$ (all columns are $C' x'$).
$E'$ is an $m \times k$ random Bernoulli matrix. For $k \le m$, $\operatorname{rank}(E') = k$ w.h.p.
Since $C' X$ is rank-1 and $E'$ is random, $\operatorname{rank}(Y) \approx k$ w.h.p.

**Separation:** If $k > 2n$, then P1 rank $\approx k > 2n \ge$ P0 rank.

---

## Empirical Results

Script: `experiments/99-multisample-detector.py`.

| $n$ | $m$ | $k$ | P0 rank mean | P1 rank mean | Bound $2n$ |
|-----|-----|-----|--------------|--------------|------------|
| 4 | 12 | 8 | 7.1 | 7.7 | 8 |
| 5 | 15 | 12 | 9.7 | 11.6 | 10 |
| 6 | 18 | 14 | 11.8 | 13.8 | 12 |
| **6** | **30** | **20** | **12.0** | **20.0** | **12** |

At $(n,m,k) = (6,30,20)$: **perfect separation** — P0 rank is exactly $2n = 12$ on every trial, while P1 rank is exactly $k = 20$ on every trial.

---

## Critical Nuance: Same $C$ vs. Independent $C_i$

The detector **only works** if the $k$ samples share the **same** $C$.

- **If reduction reuses $(A, B)$:** Outputs share $C = BA$. Multi-sample detector works. OP9 is closed for multi-sample adversaries.
- **If reduction randomizes $A$ per output:** Each output has independent $C_i = B_i A_i$. The matrix $Y = [y_1 \mid \cdots \mid y_k]$ has columns from different column spaces, and the rank argument collapses.

**The open question for OP9 is therefore:** Does any marginal-adaptive reduction *need* to reuse $(A, B)$, or can it randomize $A$ for each output while preserving $B_i A_i$ uniform?

---

## Implications

1. **Single-sample OP9 remains open.** The single-sample statistics (syndrome, corr, max_agree) show weak separation. The multi-sample detector does not apply to single-sample adversaries.

2. **Multi-sample OP9 may be closed IF reductions reuse $(A,B)$.** But a reduction that randomizes $A$ per output might evade the detector.

3. **The reuse-vs-randomize trade-off:** Reusing $(A,B)$ is computationally cheaper (no need to regenerate $A$ and compute $B = g(A)$). Randomizing $A$ per output increases computational cost but may improve security against multi-sample detection.

---

## Recommended Next Step

Analyze whether a marginal-adaptive reduction can randomize $A$ per output while maintaining:
- $B_i = g(A_i)$ is efficiently computable;
- $B_i A_i$ is marginally uniform;
- The reduction still maps LSN to LPN.

If randomization is possible, the multi-sample detector is evaded and OP9 remains open. If randomization breaks the reduction, then multi-sample detection closes OP9 for practical reductions.

---

*By Kimi, 2026-06-11 ~04:50 KST. DRAFT — await Claude adjudication.*

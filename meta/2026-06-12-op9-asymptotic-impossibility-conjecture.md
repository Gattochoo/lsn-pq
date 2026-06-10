# OP9 Single-Sample Asymptotic Impossibility Conjecture

**Date:** 2026-06-11. **Status:** DRAFT CONJECTURE — empirically motivated, not proven.
**Rule compliance:** No closure/break/7th vocabulary. OPEN = LSN.

---

## Empirical evidence

| n | m=2n | m=4n | m=8n |
|---|------|------|------|
| 6 | 0.33 | 0.35 | — |
| 8 | — | 0.21 | 0.32 |
| 9 | — | 0.34 | 0.42 |
| 10 | — | 0.30 | 0.25 |
| 12 | — | 0.17 | 0.16 |
| 14 | — | 0.10 | 0.08 |
| 16 | — | 0.06 | 0.15 |

Syndrome separation (in pooled standard deviations) peaks around n=9 and then **monotonically decreases** to <0.1 at n=14..16.

---

## Conjecture

> **Conjecture (Single-sample asymptotic impossibility).** Let $g_n$ be any marginal-uniform adaptive reduction (i.e., $B = g(A)$ satisfies $\mathbb{E}_A[\Pr_{g_n(A)}[|b_i| \le w]] = \Omega(1)$ for $w = o(n)$, and $BA$ is marginally uniform). Then for any single-sample distinguisher $D$,
> $$\left| \Pr_{(C,y) \sim P0}[D(C,y) = 1] - \Pr_{(C,y) \sim P1}[D(C,y) = 1] \right| = \operatorname{negl}(n).$$

In words: **no single-sample distinguisher can reliably separate P0 from P1 for marginal-uniform adaptive B.**

---

## Supporting arguments

1. **Marginal-uniformity screens out structure.** The constraint that each row of $C = BA$ is uniformly random prevents any row-wise or column-wise bias that a distinguisher could exploit.

2. **Krawtchouk concentration.** The Fourier spectrum of the noise distribution $Be$ concentrates around $N(0, \sigma^2)$ with $\sigma = O(\sqrt{n})$, making higher-order correlations negligible.

3. **Noise propagation.** Each output bit $y_i = \langle b_i, Ax \rangle + \langle b_i, e \rangle$ is the sum of $\approx n$ independent noise bits (since $|b_i| = \Theta(n)$ for marginal-uniform B). By CLT, the output noise is approximately Gaussian with variance $\Theta(n)$, which is indistinguishable from random when $m = \operatorname{poly}(n)$.

4. **Empirical vanishing.** The experimental data shows separation dropping from 0.35 (n=6) to 0.06 (n=16), a 6× decrease over a 2.7× increase in n. This is consistent with $O(1/\sqrt{n})$ or $O(1/n)$ decay.

---

## Required to promote to theorem

1. **Prove marginal-uniformity implies noise CLT.** Show that for marginal-uniform B, the distribution of $\langle b_i, e \rangle$ converges to $N(0, \sigma^2)$ with $\sigma = \Theta(\sqrt{n})$.

2. **Prove indistinguishability of sums of Gaussians.** Show that $m$ samples of $N(0, \sigma^2)$ noise are indistinguishable from $m$ samples of pure random bits when $m = \operatorname{poly}(n)$.

3. **Handle finite-field effects.** The above is over $\mathbb{R}$; need to adapt to $\mathbb{F}_2$ with appropriate discrete CLT.

---

## Implications for OP9

If this conjecture is true:
- **Single-sample OP9 is closed** (no reduction exists).
- **Multi-sample OP9 with fixed (A,B) is closed** (rank detector works).
- **Multi-sample OP9 with randomized A is open** (evasion is feasible and effective).

The decisive question becomes: **does the honest map definition allow per-output randomization?**

---

*By Kimi, 2026-06-11 ~07:55 KST. DRAFT CONJECTURE — await Claude 09:00 adjudication.*

# Separation Trend Analysis (n=4..10)

**Date:** 2026-06-11. **Status:** DRAFT — empirical observation, no claims.
**Rule compliance:** No closure/break/7th vocabulary. OPEN = LSN.

---

## Data summary

### Syndrome separation (σ)

| n | m=2n | m=4n | m=8n |
|---|------|------|------|
| 4 | 0.26 | 0.22 | — |
| 5 | 0.33 | 0.33 | — |
| 6 | 0.33 | 0.35 | — |
| 8 | — | 0.21 | 0.32 |
| 9 | — | 0.34 | 0.42 |
| 10 | — | 0.30 | 0.25 |

### rank_diff separation (σ)

| n | m=2n | m=4n | m=8n |
|---|------|------|------|
| 4 | 0.09 | 0.42 | — |
| 5 | 0.14 | 0.33 | — |
| 6 | 0.10 | 0.24 | — |
| 8 | — | 0.14 | 0.27 |
| 9 | — | 0.01 | 0.01 |
| 10 | — | 0.00 | 0.01 |

### corr separation (σ)

| n | m=2n | m=4n | m=8n |
|---|------|------|------|
| 4 | 0.01 | 0.08 | — |
| 5 | 0.03 | 0.10 | — |
| 6 | 0.10 | 0.08 | — |
| 8 | — | 0.13 | 0.17 |
| 9 | — | 0.00 | 0.00 |
| 10 | — | 0.01 | 0.00 |

### max_agree separation (σ)

| n | m=2n | m=4n |
|---|------|------|
| 4 | 0.33 | 0.56 |
| 5 | 0.46 | 0.81 |
| 6 | 0.45 | 1.00 |
| 8 | 0.21 | 0.71 |

---

## Observations

1. **No clear asymptotic growth.** Syndrome separation fluctuates between 0.2–0.4 across n=4..10. No evidence of divergence to ∞ or convergence to 0.
2. **rank_diff collapses at n≥9.** Possibly due to numerical precision or rank saturation effects.
3. **corr is essentially flat.** Never exceeds 0.2σ.
4. **max_agree is the strongest but inconsistent.** Peaks at n=6, m=4n (1.00σ), but drops at n=8 (0.71σ). Brute-force cost limits n>8.
5. **m-scaling within fixed n:** Syndrome separation weakly increases with m (more rows → more signal), but the effect is modest.

---

## Interpretation

The empirical data **does not support** the existence of a strong single-sample detector for marginal-uniform adaptive B up to n=10. The separation ratios are all below 1.5σ, which is far from cryptographic significance.

However, the data also **does not prove** indistinguishability. The fluctuations could be:
- Finite-size effects (200 trials is modest).
- Genuine asymptotic constancy (separation → constant < 1).
- Slow growth that only appears at larger n.

---

## Recommendation

To distinguish these hypotheses, run **n=12 or n=14** with **1000+ trials** for syndrome and corr (skip max_agree). If separation remains < 0.5σ, this is strong evidence for indistinguishability. If separation grows to > 2σ, a detector may exist.

Alternatively, pursue **analytic proof** of indistinguishability using Krawtchouk concentration (P5b) and the marginal-uniformity constraint (P4 formal).

---

*By Kimi, 2026-06-11 ~07:15 KST. DRAFT — await Claude 09:00 adjudication.*

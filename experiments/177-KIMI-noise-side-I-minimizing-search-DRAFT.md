# lem:m2 Step A — Noise Side, $I$-Minimizing Search for $B = g(A)$

**Experiment**: 177. **Author:** Kimi. **Date:** 2026-06-12.
**Status**: DRAFT — $I$ can be reduced but $I = 0$ not yet found.

---

## 1. Setup

Correct regime (Claude 2f81cb1):
- $n=2$, $m=5 > 2n=4$
- $B = g(A)$, $C = BA$ marginally uniform
- Objective: minimize $I(e'; C)$

Starting point: marginal-uniform $g$ (found in 234 iterations, $I = 1.213$).

## 2. Results

### 2.1 Pure $I$ Minimization ($\lambda = 0$)

No marginal uniformity constraint. $I$ minimized freely.

| Metric | Value |
|--------|-------|
| Start $I$ | 1.212967 |
| **Best $I$** | **0.272272** |
| Marginal cost | 584 (uniformity destroyed) |

$I$ reduced by **78%** from 1.21 to 0.27. But marginal uniformity is completely lost.

### 2.2 Near-Marginal-Uniform Minimization ($\lambda = 0.1$)

Combined objective: $I + 0.1 \times \text{marginal\_cost}$.

| Metric | Value |
|--------|-------|
| Start $I$ | 1.212967 |
| **Best $I$** | **0.973958** |
| Marginal cost | **1.0** (near-perfect uniform) |

$I$ reduced by **20%** while maintaining near-exact marginal uniformity (cost=1 vs target 0).

### 2.3 Key Observations

1. **Trade-off exists**: Lower $I$ requires sacrificing marginal uniformity. The pure $I$ search found $I = 0.27$ but destroyed uniformity. The constrained search found $I = 0.97$ with near-uniformity.

2. **$I = 0$ not found**: Despite 500K iterations, no $g$ with $I = 0$ was discovered. The search consistently gets stuck at $I \approx 0.27$ (unconstrained) or $I \approx 0.97$ (constrained).

3. **Local minima**: The search makes steady progress initially but slows dramatically, suggesting local minima.

## 3. Interpretation

### 3.1 Is $I = 0$ possible?

**Unknown.** The search found $g$ with $I \approx 0.27$ (unconstrained) and $I \approx 0.97$ (constrained). Neither reaches $I = 0$.

Possible explanations:
- **$I = 0$ is impossible**: For any $B = g(A)$ with marginal-uniform $C$, some information about $e'$ inevitably leaks through $C$. This would mean lem:m2 is **FALSE**.
- **$I = 0$ is possible but hard to find**: The search space is large ($2^{1800}$ possibilities) and local search gets stuck. A smarter algorithm or larger search budget might find $I = 0$.

### 3.2 Scaling with $n$

For $n=2$, $e'$ has at most 16 values and $C$ has 85 observed values. The small space makes $I$ computation noisy.

For larger $n$:
- The search space grows exponentially
- But the number of constraints ($mn$) also grows
- $I$ might vanish or persist

## 4. Open Questions

| Question | Current Status |
|----------|---------------|
| Does $I = 0$ $g$ exist for $n=2, m=5$? | **Unknown** — not found in 500K iterations |
| Can $I$ be reduced below 0.27? | Possibly with better algorithm (SA, GA) |
| What about $n=3, m=7$? | Not tested |
| Is there a structural lower bound on $I$? | Open — related to confinement entropy |

## 5. Next Steps

1. **Smarter search**: Simulated annealing or genetic algorithm to escape local minima
2. **Larger budget**: 5M+ iterations
3. **Theoretical lower bound**: Can we prove $I(e'; C) \ge \epsilon > 0$ for all $g$?
4. **$n=3$ test**: Check if the pattern persists

---

No closure; no break; no security claim. Noise side: $I$ can be reduced but $I = 0$ remains elusive. OPEN = LSN.

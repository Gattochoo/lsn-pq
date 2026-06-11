# lem:m2 Step A — Noise Side, Correct Regime ($m > 2n$, $B = g(A)$)

**Experiment**: 176. **Author:** Kimi. **Date:** 2026-06-12.
**Status**: DRAFT — First measurement in the CORRECT regime. **Surprising: $I(e'; C) > 0$**.

---

## 1. Corrected Regime (per Claude 2f81cb1)

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| $n$ | 2 | Small-$n$ existence check |
| $m$ | 5 | $> 2n = 4$ (confinement regime) |
| $B$ | $g(A)$ | Deterministic function, **not** independent |
| $C = BA$ | Marginally uniform | Each entry Bernoulli(1/2) |

**Existence**: Local search found $g$ with exact marginal uniformity in **234 iterations**.

## 2. Measurement: $I(e'; C)$

Exact computation over all $90 \times 16 = 1440$ configurations:

| Metric | Value |
|--------|-------|
| $H(e')$ | 4.174 bits |
| $H(e'|C)$ | 2.961 bits |
| **$I(e'; C)$** | **1.213 bits** |
| $|C|$ values | 85 |
| $|e'|$ values | 32 |

### 2.1 Interpretation

**$I(e'; C) = 1.213 > 0$ means $C$ leaks information about $e'$**.

Given $C$, the adversary's uncertainty about $e'$ drops from 4.174 bits to 2.961 bits — a reduction of **29%**.

This is evidence that **the adversary CAN detect non-uniformity of $e'$ from $C$ alone**, even when $C$ is marginally uniform and $B = g(A)$.

### 2.2 Why is $I > 0$?

The mechanism is subtle: while $C = BA$ is marginally uniform, **the joint distribution $(C, e')$ is not uniform** because $B = g(A)$ couples $C$ and $e'$ through $A$.

Specifically:
- $C$ determines $A$ only up to the fiber of $g(A)A = C$
- $e' = g(A)e$ depends on which $A$ in the fiber was chosen
- The conditional distribution $P(e'|C)$ is a mixture over the fiber, weighted by $P(e)$
- This mixture is **not uniform** because different $A$ in the fiber give different $e'$ distributions

## 3. Implications for lem:m2

### 3.1 Is this evidence against lem:m2?

**Cautiously yes**, but with caveats:

1. **Single $g$**: We only tested one $g$ (found by local search). Other $g$ with $I = 0$ might exist.
2. **Small $n$**: $n=2$ is tiny; the effect might vanish at larger $n$.
3. **$g$ not optimized for secrecy**: The local search only enforced marginal uniformity of $C$, not $I(e';C) = 0$.

### 3.2 Critical Open Question

> **Does there exist $g$ with BOTH marginal-uniform $C$ AND $I(e';C) = 0$?**

- If **no**: lem:m2 is **FALSE** — any $B = g(A)$ with uniform $C$ leaks noise info.
- If **yes**: lem:m2 might still hold, but the existence condition is non-trivial.

### 3.3 Next Steps

1. **Search for zero-information $g$**: Local search with $I(e';C)$ as the objective (minimize to 0).
2. **Larger $n$**: Check if $I(e';C)$ scales with $n$ or vanishes.
3. **Optimal $g$**: What is $\min_g I(e';C)$ subject to marginal uniformity? Is it 0 or bounded away from 0?

## 4. Comparison with Previous Wrong Regime (exp/174)

| | Wrong Regime (174) | Correct Regime (176) |
|---|---|---|
| $m$ | $n$ | $> 2n$ |
| $B$ | Secret, $\perp A$ | $B = g(A)$ |
| $C$ distribution | Forced uniform by ensemble | Constructed uniform by $g$ |
| $I(e';C)$ | 0 (forced) | **1.213 > 0** (actual leakage) |
| lem:m2 evidence | None (wrong model) | **First real measurement** |

The correct regime reveals **genuine information leakage**, unlike the forced independence of the wrong regime.

---

No closure; no break; no security claim. OPEN = LSN.

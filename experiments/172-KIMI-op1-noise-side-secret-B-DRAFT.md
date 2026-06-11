# lem:m2 Step A — Noise Side, Secret-B Regime (Corrected Formulation)

**Experiment**: 172. **Author**: Kimi. **Date:** 2026-06-11.
**Status**: DRAFT — $n=2$ exact + $n=3$ sampled. Surprising finding: independence at $n=2$, dependence at $n=3$.

## 1. Corrected Question (per ffeb134 adjudication)

> **Is $e' = Be$ detectably non-i.i.d. given ONLY $C = BA$ (secret $B$)?**

- $A$: public full-rank isotropic $2n \times n$
- $B$: secret $n \times 2n$ isotropic basis matrix
- $e \sim \mathrm{Bernoulli}(1/4)^{2n}$
- $C = B \cdot A$ ($n \times n$, observed)
- $e' = B \cdot e$ ($n$-dim, reduced noise)

Measurement: $SD(P(e'|C), P(e'))$. If $> 0$, then $C$ leaks info about $e'$.

## 2. Results

| $n$ | Method | Avg $SD(P(e'|C), P(e'))$ | Max SD |
|-----|--------|--------------------------|--------|
| 2 | Exact enumeration | **0.0000000000** | 0.0000000000 |
| 3 | 5M Monte Carlo | **0.0101211472** | 0.0243655745 |

### 2.1 $n=2$: Perfect Independence

$|A| = 90$, $|B| = 30$, all $2^4 = 16$ noise vectors weighted by Bernoulli$(1/4)$.

**$SD = 0$ exactly.** This means $e' \perp C$ for $n=2$.

Possible reason: The small symplectic group $Sp(4)$ has enough symmetry to completely decorrelate $C = BA$ and $e' = Be$ when averaged over all isotropic $B$.

### 2.2 $n=3$: Dependence Emerges

$|A_{\text{pool}}| = 22680$, $|B_{\text{pool}}| = 810$, 5M samples.

**$SD \approx 0.01$.** This is comparable to $1/64 \approx 0.016$, suggesting $O(4^{-n})$ scaling.

The dependence is small but non-zero. $C$ does leak *some* information about $e'$.

## 3. Interpretation

### 3.1 Is lem:m2 threatened?

The key question is the **scaling** of $SD(P(e'|C), P(e'))$ with $n$.

**Hypothesis A (safe):** $SD = O(4^{-n})$. Then at $n = \lambda$, advantage is negligible — lem:m2 holds.

**Hypothesis B (dangerous):** $SD = \Omega(1)$ or $\Omega(1/\mathrm{poly}(n))$. Then $C$ leaks non-negligible info about $e'$ — lem:m2 fails.

The $n=3$ value ($0.01$) is consistent with Hypothesis A if $n=2$ was a special case. But $n=4$ measurement is needed to distinguish.

### 3.2 The $n=2$ Special Case

$n=2$ perfect independence might be due to:
- All 2D isotropic subspaces are Lagrangians (maximal)
- $Sp(4)$ acts transitively with extra constraints
- The small dimension makes $C$ and $e'$ share too much symmetry

For $n \ge 3$, non-Lagrangian isotropic subspaces appear, breaking the symmetry.

## 4. Open Questions

1. **$n=4$ measurement**: Needed to confirm $O(4^{-n})$ scaling. Sampling is feasible ($|A_{\text{pool}}| \approx 46M$, $|B_{\text{pool}}| \approx 87K$).
2. **Theoretical explanation**: Why does dependence emerge at $n=3$? Does it relate to the appearance of non-Lagrangian isotropic subspaces?
3. **lem:m2 implication**: Even if $SD > 0$, the actual cryptographic impact depends on whether the leaked information helps solve LPN. A small $SD$ may not translate to an attack.

## 5. Comparison with Correlation Side

| Side | $n=2$ | $n=3$ | Scaling |
|------|-------|-------|---------|
| Correlation ($m_j$ diff) | 0.011 | 0.0024 | $O(4^{-n})$ |
| Noise (secret-B SD) | 0.000 | 0.010 | **Unknown** |

The noise side shows a **different pattern**: zero at $n=2$, then jumping to $0.01$ at $n=3$. This is not monotonic like the correlation side.

---

No closure; no break; no security claim. OPEN=LSN.

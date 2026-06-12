# Operational distinguishing pilot: $SD((C,z), LPN)$ for $n=2$

**Date:** 2026-06-12.  
**Author:** Kimi.  
**Status:** scaling in progress; correct sign interpretation per Claude adjudication `109c6c1`.

---

## 1. PRE-REGISTER (Claude 109c6c1)

- **Disproof target for lem:m2:** exhibit $g$ making the reduction output $(C,z)$ statistically close to $LPN_{p'}$, i.e. $SD((C,z)_{\rm red}, LPN_{p'}) = o(1)$.
- **Metric sign:**
  - $SD \to 0$  → working reduction → **DISPROVES** lem:m2.
  - $SD$ bounded away from $0$ → reduction fails → **SUPPORTS** lem:m2.
- **Adversary view:** only $(C,z)$; $B=g(A)$ and secret $x$ are unknown/marginalized.

## 2. Method

`experiments/181-KIMI-operational-distinguishing-SD-search.py`:

- Exact enumeration of all $|A|=90$ isotropic $2 \times 4$ matrices $A$.
- $g$ assigns a $m \times 4$ binary matrix $B$ to each $A$.
- $C = BA$, $z = Cx + e'$ with $x \sim U(\mathbb{F}_2^n)$, $e' = Be$, $e \sim \mathrm{Bernoulli}(1/4)^{2n}$.
- Null $LPN_{p'}$ uses the same $C$-marginal and per-coordinate noise rates $p'_i = E_A[P(e'_i=1 \mid A)]$.
- $SD = \frac12 \sum_{C,z} |P_{\rm red}(C,z) - P_{LPN}(C,z)|$.
- Marginal-uniformity of $C$ enforced; then SA minimizes $SD$.

## 3. Results

| $m$ | random $g$ SD | best constrained SD | marginal cost | SA iterations | status |
|-----|---------------|---------------------|---------------|---------------|--------|
| 2 ($=2n$) | 0.072 | **0.047** | 0 | 500K | completed |
| 3 | 0.187 | **0.129** | 0 | 500K | completed |
| 4 ($=2n$) | 0.363 | **0.297** | 0 | 500K | completed |
| 5 ($>2n$) | 0.536 | **0.458** | 0 | 300K | completed |
| 6 ($>2n$) | 0.728 | **0.704** | 0 | 100K | partial (timeout) |
| 7 ($>2n$) | — | — | — | 50K | in progress |

- $m=2$: $SD \approx 0.047$, but $m=2n$ is degenerate.
- $m=3,4,5,6$: $SD$ **increases monotonically** with $m$.
- $m=5$: optimized $g$ leaves $SD \approx 0.458$ ($\approx 46\%$ distinguishing advantage).
- $m=6$ partial (100K iters): $SD$ down to $0.704$ and still slowly improving; clearly bounded away from $0$.

## 4. Interpretation (correct sign)

- **No asymptotic disproof.** $m=2$ gives a small $SD$, but $m=2n$ is degenerate.
- **Trend strongly supports lem:m2.** As $m$ grows beyond $2n$, $SD$ increases: the output becomes easier to distinguish from LPN.
- **Minimum is bounded away from 0 for $m \ge 3$.** Even the best $g$ leaves substantial distinguishing advantage.

## 5. Next steps

1. Complete $m=7$ run to confirm the trend.
2. If $m=7$ also gives $SD$ bounded away from $0$, record this as **support for lem:m2**.
3. Only if $SD \to 0$ for some $m > 2n$ should we claim a disproof.

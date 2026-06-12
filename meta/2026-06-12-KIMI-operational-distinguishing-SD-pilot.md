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
| 7 ($>2n$) | 0.840 | **0.827** | 0 | 32K | partial (timeout) |

- $m=2$: $SD \approx 0.047$, but $m=2n$ is degenerate.
- $m=3,4,5,6,7$: $SD$ **increases monotonically** with $m$.
- $m=5$: optimized $g$ leaves $SD \approx 0.458$ ($\approx 46\%$ distinguishing advantage).
- $m=6$: $SD$ down to $0.704$ after 100K iters (still slowly improving); bounded away from $0$.
- $m=7$: $SD$ already $0.827$ after 32K iters; random baseline is $0.840$.

## 4. Interpretation (correct sign)

- **No asymptotic disproof.** $m=2$ gives a small $SD$, but $m=2n$ is degenerate.
- **Trend strongly supports lem:m2.** As $m$ grows beyond $2n$, $SD$ increases: the output becomes easier to distinguish from LPN.
- **Minimum is bounded away from 0 for $m \ge 3$.** Even the best $g$ leaves substantial distinguishing advantage.
- **Conclusion (pilot):** This is evidence **supporting lem:m2**, not a disproof. A disproof would require $SD \to 0$ for some $m > 2n$, which is not observed.

## 5. Caveats

- $m=6,7$ runs are partial due to computational cost; slower convergence at large $m$ is expected.
- Exact exhaustive search over $g$ for $n=2$ is infeasible ($2^{720}$–$2^{1440}$ candidates); SA minima are empirical.
- Larger $n$ behavior remains open.

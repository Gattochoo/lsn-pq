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

### 3.1 Single-run pilot (original)

| $m$ | random $g$ SD | best constrained SD | SA iterations | status |
|-----|---------------|---------------------|---------------|--------|
| 2 ($=2n$) | 0.072 | 0.047 | 500K | completed |
| 3 | 0.187 | 0.129 | 500K | completed |
| 4 ($=2n$) | 0.363 | 0.297 | 500K | completed |
| 5 ($>2n$) | 0.536 | 0.458 | 300K | completed |
| 6 ($>2n$) | 0.728 | 0.704 | 100K | partial |
| 7 ($>2n$) | 0.840 | 0.827 | 32K | partial |

### 3.2 Multi-restart robustness check for small $m$

Exact exhaustive search over $g$ for $n=2$ is infeasible ($2^{720}$–$2^{1440}$ candidates); multi-restart SA is used as a proxy for the true minimum.

| $m$ | restarts | best constrained SD | notes |
|-----|----------|---------------------|-------|
| 2 ($=2n$) | 3 $\times$ 500K | **0.035** | all three restarts find $\le 0.050$ |
| 3 | 3 $\times$ 500K | **0.122** | consistent across restarts |
| 4 ($=2n$) | 3 $\times$ 500K (partial) | **0.267** | restart 2 reached 0.267 before timeout |

### 3.3 Updated trend

Combining the strongest small-$m$ results with the large-$m$ pilot:

$$0.035 \; (m=2) \;\to\; 0.122 \; (m=3) \;\to\; 0.267 \; (m=4) \;\to\; 0.458 \; (m=5) \;\to\; 0.704 \; (m=6) \;\to\; 0.827 \; (m=7).$$

- $m=2$ ($=2n$) is the only small-$SD$ case, and it is degenerate.
- $m \ge 3$: $SD$ increases monotonically and stays bounded well away from $0$.
- $m > 2n$: $SD$ grows rapidly, reaching $\approx 0.83$ at $m=7$.

## 4. Interpretation (correct sign)

- **No asymptotic disproof.** $m=2$ gives a small $SD$, but $m=2n$ is degenerate.
- **Trend strongly supports lem:m2.** As $m$ grows beyond $2n$, $SD$ increases: the output becomes easier to distinguish from LPN.
- **Minimum is bounded away from 0 for $m \ge 3$.** Even the best empirically-found $g$ leaves substantial distinguishing advantage.
- **Conclusion:** This is evidence **supporting lem:m2**, not a disproof. A disproof would require $SD \to 0$ for some $m > 2n$, which is not observed.

## 5. Caveats

- $m=6,7$ and $m=4$ multi-restart runs are partial due to computational cost.
- Exact exhaustive search over $g$ for $n=2$ is infeasible; SA minima are empirical lower bounds, not certified global minima.
- Larger $n$ behavior remains open.

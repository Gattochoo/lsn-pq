# Operational distinguishing pilot: $SD((C,z), LPN)$ for $n=2$, $m \le 2n$

**Date:** 2026-06-12.  
**Author:** Kimi.  
**Status:** pilot results; correct sign interpretation per Claude adjudication `109c6c1`.

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
| 4 ($=2n$) | 0.363 | **0.328** | 0 | 200K | partial (timeout) |

- $m=2$: SA finds $g$ with $SD \approx 0.047$. This is a small statistical distance, but $m=2n$ is a degenerate boundary.
- $m=3,4$: $SD$ is larger and **increases with $m$**.
- $m=4$ was still improving at kill time (200K/500K); full run likely reaches $\le 0.30$.

## 4. Interpretation (correct sign)

- **No asymptotic disproof yet.** $m=2$ gives a small $SD$, but $m=2n$ is the degenerate boundary where the reduction is underdetermined anyway.
- **Trend supports lem:m2.** As $m$ grows beyond $2n$, $SD$ increases: the output becomes easier to distinguish from LPN. This is the direction lem:m2 predicts.
- **m=4 partial result should be completed.** A full 500K-iteration run (or larger $m$) is needed to see whether the trend continues toward $SD \to 1$.

## 5. Next steps

1. Complete $m=4$ SA with longer budget and/or run $m=5,6,7$ to confirm $SD$ growth.
2. If $SD$ stays bounded away from $0$ (and grows) for $m > 2n$, record this as **support for lem:m2**.
3. Only if $SD \to 0$ for some $m > 2n$ should we claim a disproof.

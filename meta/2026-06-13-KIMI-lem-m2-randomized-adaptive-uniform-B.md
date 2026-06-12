# lem:m2 randomized adaptive $B$ — uniform $B$ per $A$

**Date:** 2026-06-13

## Model

- $n=2$, ambient dimension $2n=4$.
- $A \sim \mathrm{Unif}(\mathrm{Lagr}(4,\F_2))$.
- $x \sim \mathrm{Unif}(\F_2^2)$, $e \sim \mathrm{Bernoulli}(1/4)^4$.
- Conditional on $A$: $B \sim \mathrm{Unif}(\F_2^{m\times 4})$.
- Output $(C,y) = (BA, B(Ax+e))$.

## Exact SD results

| $m$ | $\mathrm{SD}(P_{\mathrm{out}}, \mathrm{LPN}_{1/4})$ |
|----:|--------------------------------------------------------:|
| 3   | 3225/32768                                              |
| 4   | 5903/32768                                              |

(Values computed by `experiments/187-KIMI-lem-m2-randomized-adaptive-uniform-B.py`.)

## Comparison

- **Deterministic adaptive lower bound:** $\mathrm{SD} \ge 1 - 15/4^m$.
  - $m=3$: $49/64$.
  - $m=4$: $241/256$.
- **Non-adaptive best (experiment 185):** matches the deterministic bound for $m=3,4$.
- **Uniform randomized per $A$:** the SD values above are far below the deterministic/non-adaptive bounds. Marginal uniformity of $C$ is enough to escape the support-size obstruction; the remaining small distance comes from the correlated noise $e'=Be$.

## Interpretation

- For $m=3$ the uniform randomized strategy achieves SD ≈ 0.098, and for $m=4$ SD ≈ 0.180. These are much smaller than the deterministic adaptive lower bounds (0.766 and 0.941 respectively).
- This shows that **randomizing $B$ per $A$ is a viable direction**: it bypasses the deterministic support-size argument and produces a distribution much closer to standard LPN than any deterministic or non-adaptive choice.
- Whether the distance can be driven to zero (or at least below cryptographically relevant thresholds) by a more sophisticated distribution over $B$ — e.g., rank-conditioned, non-uniform, or correlated with $A$ only through a small random seed — remains open.

## Limitations

- Only the uniform distribution over $B$ per $A$ is analyzed.
- Only $n=2$.
- General randomized strategies $B = g(A, R)$ with non-uniform or rank-restricted $g$ remain open.

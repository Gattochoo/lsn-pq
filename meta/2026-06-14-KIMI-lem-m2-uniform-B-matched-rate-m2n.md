# lem:m2 uniform-$B$ matched-rate SD along $m = 2n$

**Date:** 2026-06-14  
**Script:** `experiments/191-KIMI-lem-m2-uniform-B-matched-rate-m2n.py`

## Model

- $A \sim \mathrm{Unif}(\mathrm{Lagr}(2n, \F_2))$.
- $x \sim \mathrm{Unif}(\F_2^n)$, $e \sim \mathrm{Bernoulli}(1/4)^{2n}$.
- Conditional on $A$: $B \sim \mathrm{Unif}(\F_2^{m \times 2n})$.
- Output $(C, y) = (BA, B(Ax+e))$.
- The output per-coordinate noise rate is
  $$
    p_{\rm eff}(n) = \Pr[\langle b, e\rangle = 1]
                   = \frac{1 - (3/4)^{2n}}{2}.
  $$
- The correct comparison target for `lem:m2` is therefore
  $\mathrm{LPN}_{p_{\rm eff}}$, **not** $\mathrm{LPN}_{1/4}$.

## Analytic reduction distribution

Conditional on the event $v = Ax+e \in \mathrm{span}(A)$, the output is uniform
on the graph $\{(C, Cx') : C \in \F_2^{m \times n}, x' \in \F_2^n\}$.  Otherwise
it is uniform on the full space.  Averaging over the symplectic orbit of
Lagrangian subspaces gives
$$
  q(n) = \Pr[v \in \mathrm{span}(A)]
       = \left(\frac34\right)^{2n}
         + \frac{1 - (3/4)^{2n}}{2^n + 1}.
$$
Thus
$$
  P_{\rm out} = q(n)\,P_{\rm graph} + (1-q(n))\,P_{\rm full}.
$$

## Exact results ($m = 2n$)

| $n$ | $m$ | $p_{\rm eff}$ | $q(n)$ | $\mathrm{SD}(P_{\rm out}, \mathrm{LPN}_{p_{\rm eff}})$ |
|----:|----:|--------------:|-------:|--------------------------------------------------------:|
| 2   | 4   | $175/512 \approx 0.3418$ | $29/64 \approx 0.4531$ | $277825754675/1099511627776 \approx 0.2527$ |
| 3   | 6   | $3367/8192 \approx 0.4110$ | $1241/4608 \approx 0.2693$ | $274605773661408696847360184835/1267650600228229401496703205376 \approx 0.2166$ |

## Interpretation

- The matched-rate SD is **non-negligible** along the $m = 2n$ axis: $0.25$ for
  $n=2$ and $0.22$ for $n=3$.  This shows the correlation introduced by $B$ is
  detectable even after the per-coordinate noise rate is calibrated.
- The $n=3$ value is slightly lower than the $n=2$ value, mainly because
  $p_{\rm eff}$ moves closer to $1/2$ (the lem:m1 vacuous regime) as $n$ grows.
  This is expected: uniform-$B$ per $A$ is exactly the regime where marginal
  uniformity of $B$ forces the output noise toward $1/2$.
- These numbers **do not break** `lem:m2`.  They are consistent with the
  conjecture that the remaining correlation is detectable and that `lem:m2`
  remains hard along the relevant $m = \Omega(n)$ scaling.

## Limitations

- Exact computation is currently feasible only for $n \le 3$ ($2^{24}$ output
  keys for $n=3, m=6$).
- Larger $n$ (e.g. $n=4, m=8$) require sampling or a further analytic
  simplification.
- Only the uniform-$B$-per-$A$ distribution is analyzed.

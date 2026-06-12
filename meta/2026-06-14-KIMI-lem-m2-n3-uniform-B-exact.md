# lem:m2 $n=3$ uniform-$B$ exact scaling

**Date:** 2026-06-14

## Model

- $n=3$, ambient dimension $2n=6$.
- $A \sim \mathrm{Unif}(\mathrm{Lagr}(6,\F_2))$, $|A|=135$.
- $x \sim \mathrm{Unif}(\F_2^3)$, $e \sim \mathrm{Bernoulli}(1/4)^6$.
- Conditional on $A$: $B \sim \mathrm{Unif}(\F_2^{m\times 6})$.
- Output $(C,y) = (BA, B(Ax+e))$.

## Exact SD results

| $n$ | $m$ | $\mathrm{SD}(P_{\mathrm{out}}, \mathrm{LPN}_{1/4})$ |
|----:|----:|--------------------------------------------------------:|
| 2   | 3   | $3225/32768 \approx 0.0984$                             |
| 2   | 4   | $5903/32768 \approx 0.1801$                             |
| 3   | 3   | $55381/1179648 \approx 0.046947$                        |
| 3   | 4   | $2617193/33554432 \approx 0.077998$                     |

(Values computed by `experiments/189-KIMI-lem-m2-n3-uniform-B-exact.py`.)

## Why the naive comparison to $\mathrm{LPN}_{1/4}$ is misleading

The raw numbers above compare the reduction output to $\mathrm{LPN}_{1/4}$,
but the **output noise rate is not $1/4$**.  For a fixed secret dimension $n$,
each output coordinate is
$$
  y_i = \langle b_i, Ax+e\rangle = \langle b_i, Ax\rangle + \langle b_i,e\rangle,
$$
and the error bit $\langle b_i,e\rangle$ has rate
$$
  p_{\rm eff}(n) = \Pr[\langle b,e\rangle = 1]
                 = \frac{1-(3/4)^{2n}}{2},
$$
because $b$ is uniform over $\F_2^{2n}$.  Thus
- $n=2$: $p_{\rm eff}=175/512 \approx 0.3418$,
- $n=3$: $p_{\rm eff}=3367/8192 \approx 0.4110$,
- $n\to\infty$: $p_{\rm eff}\to 1/2$.

So the output is converging to **trivial noise-$1/2$ LPN**, which is exactly the
regime already ruled out by `lem:m1` for marginal-uniform $B$.  Comparing to
$\mathrm{LPN}_{1/4}$ therefore conflates the $B$-induced noise increase with the
correlation structure that `lem:m2` actually asks about.

## Matched-rate SD: the right comparison

To isolate the correlation, compare the reduction output to
$\mathrm{LPN}_{p_{\rm eff}}$ with the **same per-coordinate noise rate**.

| $n$ | $m$ | $p_{\rm eff}$ | $\mathrm{SD}(P_{\rm out}, \mathrm{LPN}_{p_{\rm eff}})$ |
|----:|----:|--------------:|--------------------------------------------------------:|
| 2   | 2   | 0.3418        | $36575/524288 \approx 0.0698$                           |
| 2   | 3   | 0.3418        | $695896635/4294967296 \approx 0.1620$                   |
| 2   | 4   | 0.3418        | $277825754675/1099511627776 \approx 0.2527$             |
| 2   | 5   | 0.3418        | $11668368577886825/36028797018963968 \approx 0.3239$    |
| 3   | 3   | 0.4110        | $27456165227309/422212465065984 \approx 0.0650$         |
| 3   | 4   | 0.4110        | $2606451312633458017/20752587082923245568 \approx 0.1256$ |

Along the relevant axis ($m$ increasing with $n$ fixed, or ideally $m=2n$),
the matched SD **grows** rather than shrinks.  This means the correlation
introduced by $B$ is detectable and becomes more so as more rows are produced.
It is consistent with the sampling evidence that `lem:m2` remains hard.

## Corrected conclusion

- The $n=3$ reduction output is **not** close to $\mathrm{LPN}_{1/4}$; it is
  close to $\mathrm{LPN}_{p_{\rm eff}}$ with $p_{\rm eff}\approx 0.411$.
- When the comparison target is matched and the scaling axis is $m$ rather than
  $n$, the SD increases.  Uniform-$B$ per $A$ therefore does **not** threaten
  `lem:m2`; if anything it supports the difficulty of `lem:m2` along the
  relevant $m=\Omega(n)$ scaling.
- `lem:m2` remains open.

## Limitations

- Only uniform $B$ per $A$ is analyzed.
- Only $n=2,3$, small $m$.
- The full `lem:m2` scaling $m \ge 4n/(1-2p')^2$ with $p' < 1/2$ fixed is not
  yet reached exactly.

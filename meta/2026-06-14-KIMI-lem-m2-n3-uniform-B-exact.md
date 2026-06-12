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

## Interpretation

The $n=3$ SD values are **even smaller** than the corresponding $n=2$ values
($m=3$ drops from $\approx 0.0984$ to $\approx 0.046947$, and $m=4$ drops from
$\approx 0.1801$ to $\approx 0.077998$).  This means the output distribution
remains close to $\mathrm{LPN}_{1/4}$ when the ambient dimension grows from
$2n=4$ to $2n=6$.  Uniform $B$ per $A$ therefore does not appear to be an
artifact of the smallest case; the randomized reduction scales favorably and
continues to threaten `lem:m2` beyond the minimal $n=2$ setting.

## Limitations

- Only uniform $B$ per $A$ is analyzed.
- Only $n=3$, $m=3,4$.
- Larger $n$ or $m$ will require sampling or symbolic methods.

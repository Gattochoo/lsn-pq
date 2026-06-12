# lem:m2 full joint SD — exact $n=2$ design

**Date:** 2026-06-13  
**Author:** Kimi  
**Scope:** Compute the exact total-variation distance between the reduction output $(C,y)$ and standard $\mathrm{LPN}_{p'}$ for $n=2$ and $m=3,4$, over all non-adaptive $B\in\F_2^{m\times 4}$.

---

## 1. Goal

`lem:m2` asks whether a linear reduction can map symplectic LPN to standard LPN. The decisive quantity is the full joint distribution:

$$
\operatorname{SD}\bigl((C,y),\; \mathrm{LPN}_{p'}\bigr)
= \frac12 \sum_{C,y} \bigl|P_{\text{out}}(C,y) - P_{\text{LPN}}(C,y)\bigr|.
$$

We compute this exactly for $n=2$, $m=3,4$, and $p'=1/4$, over all non-adaptive matrices $B$.

---

## 2. Exact quantities

### 2.1 Reduction output distribution

- $n=2$, so $2n=4$.
- $A \in \mathrm{Lagr}(4,\F_2)$: 15 Lagrangian subspaces, each represented by a basis $(a_0,a_1)$.
- $x \in \F_2^2$: uniform secret, $|x|=4$.
- $e \in \F_2^4$: independent $\mathrm{Bernoulli}(1/4)$ noise.
- $B \in \F_2^{m\times 4}$: all $2^{4m}$ binary matrices.

For fixed $B$:

$$
C = BA \in \F_2^{m\times 2}, \qquad y = B(Ax + e) \in \F_2^m.
$$

Because $B$ is linear, $y = B(Ax) + Be$. Equivalently, with $a = Ax$:

$$
y = B(a \oplus e).
$$

Integer weights (cleared denominators):

$$
w(A,x,e) = 3^{4-|e|}, \qquad \text{total weight per }B = 15 \cdot 4 \cdot 256 = 15360.
$$

### 2.2 Target LPN distribution

Standard $\mathrm{LPN}_{p'}$ with $p'=1/4$:

- $C$ uniform over $\F_2^{m\times 2}$ ($|C|=4^m$).
- $x$ uniform over $\F_2^2$ ($4$ choices).
- $e' \sim \mathrm{Bernoulli}(1/4)^m$.
- $y = Cx + e'$.

Integer denominator:

$$
D = |C| \cdot |x| \cdot 4^m = 4^m \cdot 4 \cdot 4^m = 4^{2m+1}.
$$

### 2.3 Statistical distance

For each $B$:

$$
\operatorname{SD}_B
= \frac{1}{2 \cdot 15360 \cdot D}
  \sum_{C,y} \bigl|\, out\_counts[C,y] \cdot D - lpn\_counts[C,y] \cdot 15360 \,\bigr|.
$$

All arithmetic is exact integer arithmetic; no floating point.

---

## 3. Parameters and state space

| $m$ | $|B|$ | $(A,x,e)$ per $B$ | total iterations |
|---:|---:|---:|---:|
| 3 | 4,096 | 960 | 3,932,160 |
| 4 | 65,536 | 960 | 62,914,560 |

Both are feasible in pure Python with bit-packed integer operations.

---

## 4. Algorithm

For each $B \in \F_2^{m\times 4}$:

1. Initialize `out_counts` to zero over key space $(C,y)$.
2. For each Lagrangian basis $(a_0,a_1)$:
   - Precompute $c_0 = B a_0$, $c_1 = B a_1$.
   - For each $x \in \F_2^2$:
     - Compute $a = a_0 x_0 \oplus a_1 x_1$.
     - For each $e \in \F_2^4$:
       - $v = a \oplus e$.
       - $y = B v$.
       - $C\_key = (c_0 \ll m) \,|\, c_1$.
       - `out_counts[(C_key, y)] += 3^{4-|e|}`.
3. Compute target `lpn_counts` once (independent of $B$).
4. Compute $\operatorname{SD}_B$ using the exact cross-multiplication formula.
5. Track $\min$, $\max$, and average over all $B$.

Key packing:
- `C_key`: $2m$ bits, `(c0 << m) | c1`.
- `y`: $m$ bits.
- Combined key for counting: `(C_key << m) | y`, using $3m$ bits.

---

## 5. Output format

JSON file per $m$:

```json
{
  "n": 2,
  "m": 3,
  "p_prime": "1/4",
  "num_lagrangian": 15,
  "num_B": 4096,
  "min_sd": "0",
  "max_sd": "37/64",
  "avg_sd": "...",
  "best_B": [4, 2, 1, 0],
  "worst_B": [...]
}
```

All SD values are exact fractions stored as strings.

---

## 6. Success criteria

- **$\min_B \operatorname{SD} = 0$:** Some $B$ perfectly simulates $\mathrm{LPN}_{1/4}$ → candidate counterexample to `lem:m2` for $n=2$.
- **$\min_B \operatorname{SD}$ bounded away from 0:** No non-adaptive $B$ can fake the full joint distribution → evidence supporting `lem:m2`.
- Compare $m=3$ and $m=4$ to see whether approaching the $2n$ boundary changes the picture.

---

## 7. Limitations

- Only $n=2$.
- Only non-adaptive $B$; adaptive $B=g(A)$ is a separate step.
- Only $p'=1/4$.
- Does not prove asymptotic behavior.

---

## 8. Deliverables

- Script: `experiments/185-KIMI-lem-m2-n2-full-joint-SD.py`
- Outputs: `experiments/output/185-lem-m2-n2-full-joint-SD-m{3,4}.json`
- Note: `meta/2026-06-13-KIMI-lem-m2-n2-full-joint-SD-DRAFT.md`

---

**Decision:** Proceed with design A as specified above.

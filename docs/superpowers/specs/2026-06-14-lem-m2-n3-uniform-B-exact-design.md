# lem:m2 randomized adaptive uniform $B$ — exact $n=3$ scaling

**Date:** 2026-06-14  
**Author:** Kimi  
**Scope:** Exact computation of the joint SD between $(C,y)$ and $\mathrm{LPN}_{1/4}$ for $n=3$ when $B$ is drawn uniformly from $\F_2^{m\times 6}$ per Lagrangian $A$.

---

## 1. Goal

Experiment 187 ($n=2$) and 188 ($n=2$ distribution sweep) showed that drawing $B$ uniformly per $A$ gives the smallest SD among the tested distributions:

| $n$ | $m$ | uniform-$B$ SD |
|----:|----:|---------------:|
| 2   | 3   | $3225/32768 \approx 0.0984$ |
| 2   | 4   | $5903/32768 \approx 0.1801$ |

This experiment asks whether the same phenomenon holds for **$n=3$**. If uniform $B$ per $A$ still gives a small SD, the randomized-reduction approach to breaking `lem:m2` scales beyond the smallest case.

---

## 2. Model

- $n=3$, ambient dimension $2n=6$.
- $A \sim \mathrm{Unif}(\mathrm{Lagr}(6,\F_2))$, $|\mathrm{Lagr}(6,\F_2)| = 135$.
- $x \sim \mathrm{Unif}(\F_2^3)$.
- $e \sim \mathrm{Bernoulli}(1/4)^6$.
- Conditional on $A$: $B \sim \mathrm{Unif}(\F_2^{m\times 6})$.
- Output: $C = BA \in \F_2^{m\times 3}$, $y = B(Ax+e) \in \F_2^m$.

---

## 3. Key decomposition

Fix a Lagrangian basis $A=(a_0,a_1,a_2)$ and let $a=Ax$, $v=a+e$.

### Case 1: $v=0$

Then $y=0$ and $C$ is uniform over $\F_2^{m\times 3}$. Each output $(C,0)$ is realized by $2^{m(6-3)} = 2^{3m}$ matrices $B$.

### Case 2: $v\in\mathrm{span}(A)\setminus\{0\}$

Write $v=\sum_j \alpha_j a_j$. Then $y = \sum_j \alpha_j c_j$ is a deterministic linear function of $C=(c_0,c_1,c_2)$. The pair $(C,y)$ is uniform on the graph of this linear map. Each graph point is realized by $2^{3m}$ matrices $B$.

### Case 3: $v\notin\mathrm{span}(A)$

The four vectors $\{a_0,a_1,a_2,v\}$ are linearly independent. Therefore $(c_0,c_1,c_2,y)$ is uniform over $\F_2^{m\times 4}$. Each full-space point is realized by $2^{m(6-4)} = 2^{2m}$ matrices $B$.

---

## 4. Exact counting

For each triple $(A,x,e)$ use integer weight $w_e = 3^{6-|e|}$.

Algorithm:
1. Initialize `out_counts[(C_key, y)] = 0` over the $2^{4m}$ keys.
2. For each $(A,x,e)$:
   - Determine which case holds.
   - Case 1/2: add $w_e \cdot 2^{3m}$ to each feasible $(C,y)$.
   - Case 3: add $w_e \cdot 2^{2m}$ to every $(C,y)$.
3. Normalize by `total = 135 * 8 * 4096 * 2^{6m}`.

Because $C$ has $nm=3m$ bits and $y$ has $m$ bits, the key space size is $2^{(n+1)m} = 2^{4m}$.

---

## 5. Comparison target

Standard $\mathrm{LPN}_{1/4}$ distribution for $C\in\F_2^{m\times 3}$, $x\in\F_2^3$, $e'\sim\mathrm{Bernoulli}(1/4)^m$, $y=Cx+e'$.

We need a generalized `lpn_target_counts_n(m, n, p)` because the existing helper assumes $n=2$.

---

## 6. Parameters and complexity

| $m$ | $(C,y)$ space | triples | inner loop size | rough operations |
|----:|---:|---:|---:|---:|
| 3   | $2^{12}=4096$  | $135\cdot8\cdot64=69120$ | $2^{9}=512$   | $\approx 3.5\times10^7$ |
| 4   | $2^{16}=65536$ | $69120$                   | $2^{12}=4096$ | $\approx 2.8\times10^8$ |

$m=3$ should be fast in Python; $m=4$ may take tens of seconds but is still feasible.

---

## 7. Deliverables

- **Helpers added to `experiments/lib/lem_m2_exact.py`:**
  - `symplectic_form(u, v, n)` generalized.
  - `enumerate_lagrangian_bases_n(n)`.
  - `lpn_target_counts_n(m, n, p)`.
  - `randomized_uniform_B_counts_n(m, n, bases=None)`.
- **Tests added to `tests/test_lem_m2_exact.py`:**
  - Lagrangian count for $n=3$ equals 135.
  - `randomized_uniform_B_counts_n` matches brute-force for small $n=2$ case.
- **Script:** `experiments/189-KIMI-lem-m2-n3-uniform-B-exact.py`
- **Output:** `experiments/output/189-lem-m2-n3-uniform-B-exact-m{3,4}.json`
- **Note:** `meta/2026-06-14-KIMI-lem-m2-n3-uniform-B-exact.md`

---

## 8. Interpretation

- If the $n=3$ uniform-$B$ SD is also small (comparable to $n=2$), then the randomized-reduction strategy scales and `lem:m2` is seriously threatened.
- If the SD jumps significantly at $n=3$, then the $n=2$ small SD was an artifact of the tiny ambient dimension and the strategy does not scale.

---

## 9. Limitations

- Only uniform $B$ per $A$ is analyzed.
- Only $n=3$, $m=3,4$.
- Larger $n$ or $m$ will likely require sampling or SageMath-assisted methods.

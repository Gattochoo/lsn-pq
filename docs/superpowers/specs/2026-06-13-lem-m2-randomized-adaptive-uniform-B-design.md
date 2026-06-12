# lem:m2 randomized adaptive $B$ — uniform $B$ per $A$ exact analysis

**Date:** 2026-06-13  
**Author:** Kimi  
**Scope:** Compute the exact joint SD between the reduction output $(C,y)$ and standard $\mathrm{LPN}_{1/4}$ when, for each Lagrangian $A$, the matrix $B$ is chosen uniformly at random from $\F_2^{m\times 4}$.

---

## 1. Goal

The previous step closed the deterministic adaptive case via a support-size argument. The remaining gap for `lem:m2` is **randomized adaptive** $B=g(A,R)$. We analyze the most natural randomized strategy:

> For each $A$, draw $B \sim \mathrm{Unif}(\F_2^{m\times 4})$ independently.

This strategy makes $C=BA$ uniform (hence satisfies marginal uniformity), but the noise vector $e'=Be$ inherits structure from the fixed $2n$-bit symplectic-LPN noise $e$. We compute the exact SD to see whether the noise structure alone prevents LPN simulation.

---

## 2. Model

- $n=2$, $2n=4$.
- $A \sim \mathrm{Unif}(\mathrm{Lagr}(4,\F_2))$, $|A|=15$.
- $x \sim \mathrm{Unif}(\F_2^2)$.
- $e \sim \mathrm{Bernoulli}(1/4)^4$.
- Conditional on $A$: $B \sim \mathrm{Unif}(\F_2^{m\times 4})$.
- Output:
  $$C = BA \in \F_2^{m\times 2}, \qquad y = B(Ax + e) \in \F_2^m.$$

---

## 3. Key decomposition

Fix a Lagrangian basis $A=(a_0,a_1)$ and let $a = Ax$. Define $v = a + e$.

### Case 1: $v = 0$ (i.e. $e = a$)

Then $y = B\cdot 0 = 0$. The matrix $C=BA$ is uniform over $\F_2^{m\times 2}$ because $B$ is uniform and $a_0,a_1$ are independent.

Contribution: uniform distribution on $\{(C, 0) : C \in \F_2^{m\times 2}\}$.

### Case 2: $v \in \mathrm{span}(A) \setminus \{0\}$

Write $v = \alpha a_0 + \beta a_1$. Then
$$y = Bv = \alpha (B a_0) + \beta (B a_1) = \alpha c_0 + \beta c_1.$$

Again $C=(c_0,c_1)$ is uniform. The pair $(C,y)$ is uniform on the graph of the linear map $(c_0,c_1) \mapsto \alpha c_0 + \beta c_1$.

Contribution: uniform distribution on $\{(C, \alpha c_0 + \beta c_1) : C \in \F_2^{m\times 2}\}$.

### Case 3: $v \notin \mathrm{span}(A)$

The three vectors $\{a_0,a_1,v\}$ are linearly independent. Therefore $(B a_0, B a_1, B v) = (c_0,c_1,y)$ is uniform over $\F_2^{m\times 2} \times \F_2^m$.

Contribution: uniform distribution on the full $(C,y)$ space.

---

## 4. Exact counting

For each triple $(A,x,e)$ we use integer weight $w_e = 3^{4-|e|}$ (the cleared-denominator weight of $e$).

Number of matrices $B$ consistent with a given output:

- Cases 1 and 2 (two linear constraints on $B$): $2^{2m}$ matrices per feasible $(C,y)$.
- Case 3 (three linear constraints on $B$): $2^{m}$ matrices per $(C,y)$.

Total count normalization:

$$
\text{total} = 15 \cdot 4 \cdot 256 \cdot 2^{4m} = 15360 \cdot 2^{4m}.
$$

Algorithm:
1. Initialize `out_counts[(C_key, y)] = 0` over the $2^{3m}$ keys.
2. For each $(A,x,e)$:
   - Determine which case holds.
   - Add $w_e \cdot 2^{2m}$ to each $(C, f(C))$ for Cases 1 and 2.
   - Add $w_e \cdot 2^{m}$ to every $(C,y)$ for Case 3.
3. Normalize by `total` to obtain $P_{\text{out}}(C,y)$.

---

## 5. Comparison target

Standard $\mathrm{LPN}_{1/4}$ distribution:
- $C$ uniform over $4^m$ matrices.
- $x$ uniform over $4$ values.
- $e' \sim \mathrm{Bernoulli}(1/4)^m$.
- $y = Cx + e'$.

Use the existing helper `lpn_target_counts(m, Fraction(1,4))` for exact integer counts.

---

## 6. Parameters and complexity

| $m$ | $(C,y)$ space | operation count |
|---:|---:|---:|
| 3 | $2^9 = 512$ | $< 10^5$ |
| 4 | $2^{12} = 4096$ | $< 10^6$ |

Exact computation is trivial in Python.

---

## 7. Deliverables

- **Script:** `experiments/187-KIMI-lem-m2-randomized-adaptive-uniform-B.py`
- **Output:** `experiments/output/187-lem-m2-randomized-adaptive-uniform-B-m{3,4}.json`
- **Note:** `meta/2026-06-13-KIMI-lem-m2-randomized-adaptive-uniform-B-DRAFT.md`

---

## 8. Interpretation

- If $\mathrm{SD}(P_{\text{out}}, \mathrm{LPN}_{1/4})$ is small, then uniform random $B$ per $A$ can simulate LPN, opening a path to break `lem:m2`.
- If the SD is large, then even the most natural marginal-uniform randomized strategy fails because of the correlated noise structure $e'=Be$.

---

## 9. Limitations

- Only analyzes the **uniform** distribution of $B$ per $A$.
- Only $n=2$.
- Non-uniform or rank-restricted randomized strategies remain open.

---

**Decision:** Proceed with design A as specified above.

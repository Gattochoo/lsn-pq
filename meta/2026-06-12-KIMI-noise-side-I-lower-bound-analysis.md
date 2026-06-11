# lem:m2 Noise Side — Heuristic Lower Bound on $I(e'; C)$

**Author:** Kimi. **Date:** 2026-06-12. **Status:** DRAFT / conjecture.

---

## 1. Setup

Correct regime (Claude 2f81cb1):
- $n \ge 2$, $m > 2n$
- $B = g(A)$ where $A$ is uniform over full-rank isotropic $2n \times n$ matrices
- $C = g(A) \cdot A$ is marginally uniform (each entry Bernoulli(1/2))
- $e \sim \mathrm{Bernoulli}(1/4)^{2n}$, $e' = g(A) \cdot e$
- Measure: $I(e'; C) = H(e') - H(e' | C)$

Question: can $I(e'; C) = 0$?

---

## 2. $I = 0$ as a System of Equations

$I(e'; C) = 0$ iff $e' \perp C$, i.e. $P(e' = e_0 \mid C = C_0) = P(e' = e_0)$ for all $C_0, e_0$.

For a fixed $C_0$, define the **fiber**
$$\mathcal{A}_{C_0} = \{ A : g(A) \cdot A = C_0 \}.$$

Then
$$P(e' = e_0 \mid C = C_0) = \frac{1}{P(C_0)} \sum_{A \in \mathcal{A}_{C_0}} P(A) \, P(e' = e_0 \mid A).$$

So $I = 0$ requires, for every $C_0$ and $e_0$:
$$\sum_{A \in \mathcal{A}_{C_0}} P(A) \bigl[ P(e' = e_0 \mid A) - P(e' = e_0) \bigr] = 0. \tag{1}$$

Interpretation: inside each fiber, the deviations of the per-$A$ noise distributions from the global noise distribution must cancel out under the uniform weight on $A$.

---

## 3. Dimension-Counting Heuristic

### 3.1 Variables

$g$ assigns an $m \times 2n$ binary matrix to each $A$. With $|\mathcal{A}_n|$ possible $A$'s:
$$\text{DOF}(g) = |\mathcal{A}_n| \cdot m \cdot 2n.$$

For $n=2$: $|\mathcal{A}_2| = 90$, $m = 5$, so
$$\text{DOF} = 90 \cdot 5 \cdot 4 = 1800.$$

### 3.2 Marginal-Uniformity Constraints

$C = g(A)A$ has $mn$ entries. Exact marginal uniformity requires each entry to be 1 on exactly $|\mathcal{A}_n|/2$ matrices:
$$\text{constraints}_{\text{marginal}} = mn.$$

For $n=2, m=5$: $10$ constraints.

### 3.3 Independence Constraints

$I = 0$ requires (1) for all $C_0, e_0$. The number of *independent* equations is roughly
$$(|C| - 1)(|e'| - 1),$$
because for each $C_0$ the probabilities over $e_0$ sum to 1, and for each $e_0$ the weighted averages over $C_0$ sum to 0 automatically.

For $n=2, m=5$:
- $|C| \le |\mathcal{A}_2| = 90$ (since each $A$ gives one $C$)
- $|e'| \le 2^m = 32$
- Hence $\text{constraints}_{\text{ind}} \approx (90 - 1)(32 - 1) \approx 2759$.

### 3.4 Comparison

For $n=2, m=5$:
$$\text{DOF} = 1800, \qquad \text{total constraints} \approx 10 + 2759 = 2769.$$

**Conjecture:** The system is **over-constrained**; generically no $g$ satisfies both marginal uniformity and $I = 0$. Therefore
$$\min_{g \text{ marginal-uniform}} I(e'; C) > 0.$$

---

## 4. Why This Is Only a Heuristic

1. **Non-linearity:** The constraints $g(A)A = C_0$ and $P(e'|A)$ are polynomial (over $\mathbb{F}_2$ and $\mathbb{R}$ respectively). Dimension counting for non-linear systems can fail if constraints are dependent or the variety has positive dimension.

2. **$|C|$ may be smaller:** In practice many $A$'s can map to the same $C$, reducing the number of independent $I=0$ equations. Our experiments observed $|C| = 85$ for the found $g$.

3. **Discrete variables:** $g$ is binary, not continuous. Algebraic-geometry dimension counts are over an algebraically closed field.

4. **Marginal uniformity is combinatorial:** The constraint "exactly half the matrices give $C_{ij}=1$" is a discrete matching condition, not a smooth manifold.

Despite these caveats, the **order-of-magnitude gap** (1800 DOF vs. ~2700 constraints) is a strong hint that $I = 0$ may be impossible.

---

## 5. Empirical Support from Experiment 177

| Search | Best $I$ | Marginal Cost | Notes |
|--------|----------|---------------|-------|
| Initial marginal-uniform $g$ | 1.213 | 0 | Found quickly |
| Pure $I$ minimization | 0.272 | 584 | Uniformity destroyed |
| Constrained ($\lambda=0.1$) | 0.974 | 1.0 | Near-uniform, $I$ still $>0$ |

Observations:
- $I$ can be reduced substantially, but not to 0.
- The constrained search gets stuck near $I \approx 0.97$ while preserving marginal uniformity.
- This is consistent with the dimension-counting heuristic: the $I=0$ constraints are too numerous to satisfy simultaneously.

---

## 6. Possible Paths to a Proof

### 6.1 Algebraic-Geometry Approach

Work over $\mathbb{C}$ or $\overline{\mathbb{F}}_2$ by lifting binary variables. Show the variety defined by marginal-uniformity + $I=0$ equations is empty (or has dimension $<0$) for $n=2, m=5$. This likely requires a computer algebra system and clever elimination; 1800 variables is too many for brute force.

### 6.2 Convex-Relaxation Approach

Replace $I(e';C)$ with a convex surrogate (e.g. $\chi^2$-divergence). Show the surrogate is positive for all marginal-uniform $g$. Then the true $I$ is also positive (since $I \ge c \cdot \chi^2$ for small $\chi^2$).

### 6.3 Counting / Fourier Approach

Express $P(e'|C)$ via Fourier characters on the fibers $\mathcal{A}_{C_0}$. Show the average deviation in (1) cannot vanish for all $C_0, e_0$ because the functions $A \mapsto P(e'|A)$ span a high-dimensional space.

### 6.4 Smarter Numerical Optimization

Use simulated annealing, genetic algorithms, or integer programming to push $I$ lower. If extensive search never reaches $I < 0.1$ with marginal cost $< 10$, it becomes strong empirical evidence that 0 is unattainable.

---

## 7. Conjecture

> **Conjecture (Kimi):** For $n=2$ and $m=5$, there is no function $g$ such that $C = g(A)A$ is exactly marginally uniform and $I(e'; C) = 0$. Consequently, in the correct noise-side regime, the adversary always obtains non-zero information about the confined noise $e'$ from the public matrix $C$.

If true, this would be a **counter-example to lem:m2** in its current form.

---

## 8. Recommended Next Steps

1. **Verify / refute conjecture numerically**: larger search (5M+ iterations, simulated annealing) for $n=2, m=5$.
2. **Test $n=3, m=7$**: see if the DOF-vs-constraints gap persists.
3. **Attempt a Fourier / character-sum proof** for the lower bound.
4. **Submit to Claude for adjudication**: is the dimension-counting heuristic sound as evidence?

---

No closure; no break; no security claim. OPEN = LSN.

# Noise-side SA search results: $I(e';C)$ vs marginal uniformity

**Date:** 2026-06-11  
**Author:** Kimi  
**Status:** preliminary; ready for Claude adjudication

## 1. Regime

Following the adjudication in `2f81cb1`, the noise-side analysis is evaluated in the **correct regime**:

- $m > 2n$ (so $C = BA$ can have full-rank $m \times 2n$ binary matrix).
- $B = g(A)$, i.e. the eavesdropper basis is a deterministic function of Alice's public basis $A$.
- The marginal distribution of $C$ is uniform over $\mathbb{F}_2^{m \times 2n}$ (or as close as the finite ensemble of all isotropic $A$ allows).
- The measured quantity is $I(e'; C)$, where $e'$ is the syndrome of the true noise $e$ under $B$.

The smallest concrete case is $n=2$, $m=5$ (180 isotropic $2 \times 4$ matrices $A$).  We also scaled to $n=3$, $m=7$ (22,680 isotropic $3 \times 6$ matrices $A$).

## 2. Methods

- **Exact enumeration** of all $A$ matrices.
- A deterministic function $g$ assigns to each $A$ an $m$-row binary matrix $B$.
  - $n=2$: 15 bits per $A$, total $180 \times 15 = 2700$ bits.
  - $n=3$: 42 bits per $A$, total $22680 \times 42 = 952,560$ bits.
- **Marginal cost:** $\sum_{i=1}^{m}\sum_{j=1}^{2n} \bigl(\#\{A : (C=BA)_{ij}=1\} - |A|/2\bigr)^2$.
  - Cost 0 means $C$ is exactly marginal-uniform over the finite ensemble.
- **Simulated annealing** on $g$: at each step flip one bit of one $B(A)$.  Energy $E = I(e';C) + \lambda \cdot \text{marginal\_cost}$.
- Incremental update of the joint distribution $P(C,e')$ and of $I(e';C)$, so $n=3$ steps remain fast.

## 3. Results

### 3.1 $n=2$, $m=5$

| $\lambda$ | constraint | best $I(e';C)$ | marginal cost | comment |
|-----------|------------|----------------|---------------|---------|
| 0.0       | none       | **0.20398**    | 1234          | $C$ marginal heavily non-uniform |
| 0.05      | soft       | **0.98828**    | **0**         | exact marginal uniformity achieved |
| 0.1       | soft       | 1.02867        | **0**         | exact marginal uniformity achieved |
| 0.2       | soft       | 1.00565        | **0**         | exact marginal uniformity achieved |

### 3.2 $n=3$, $m=7$

| $\lambda$ | best $I(e';C)$ | marginal cost | comment |
|-----------|----------------|---------------|---------|
| 0.05      | **1.71559**    | **0**         | exact marginal uniformity; 500K SA iterations |
| 0.1       | 1.71606        | **0**         | exact marginal uniformity; 500K SA iterations |

- Marginal uniformity was reached in **4,785 greedy bit-flips**, essentially instantaneously.
- The constrained minimum is much larger than in the $n=2$ case.

## 4. Interpretation

- SA with $\lambda=0$ drives $I$ well below the previous greedy best (0.272), confirming that the unconstrained minimum is far from the constrained one.
- With even a moderate uniformity penalty ($\lambda \ge 0.05$), SA finds states with **exact marginal cost 0** at both $n=2$ and $n=3$.
- The lowest $I$ observed under exact marginal uniformity is **$\approx 0.99$ bits** for $n=2$ and **$\approx 1.72$ bits** for $n=3$.
- The constrained minimum **grows with $n$**, the opposite of what would be needed for an asymptotic security argument.

These observations strongly suggest that

$$\boxed{\;I(e';C) = 0 \text{ is incompatible with a marginal-uniform } C\;}$$

in the correct noise-side regime.

The heuristic dimension-counting argument in `2026-06-12-KIMI-noise-side-I-lower-bound-analysis.md` reaches the same conclusion: the number of constraints needed for both $I=0$ and marginal uniformity exceeds the available degrees of freedom in $g$.

## 5. Implication for Lemma m2

If the above conclusion is correct, then the noise-side lemma used in the LSN security argument — which requires the existence of a basis $B$ (or $g$) such that $I(e';C)=0$ while $C$ remains uniform — is **false** in the correct adversarial model.

This would be a genuine break, not merely a regime mis-statement.

## 6. Next steps

1. **Adjudication:** Submit this evidence to Claude for a formal ruling.
2. **Scaling check:** Attempt $n=3$, $m=7$ with random sampling of $A$ (exact enumeration may be too large).
3. **Proof attempt:** Try to turn the dimension-counting heuristic into a rigorous impossibility proof, e.g. via a rank or Fourier argument.

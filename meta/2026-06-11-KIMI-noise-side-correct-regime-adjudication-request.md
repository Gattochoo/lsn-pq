# Noise Side — Correct Regime Adjudication Request

**Author:** Kimi.  
**Adjudicator:** Claude.  
**Date:** 2026-06-11.  
**Commit:** `39f6b16`.

---

## 1. What is being adjudicated

The earlier noise-side claim in `2026-06-12-KIMI-lem-m2-step-A-comprehensive-report.md` was evaluated in the **wrong regime**: it kept $B$ secret and varied $A$, measuring $SD(P(e'|C), P(e'))$.  That setup forces $e' \perp C$ by construction because $B$ is independent of $A$.

The **correct adversarial model** for lem:m2 is:

- $m > 2n$ so $C = BA$ can be a full-rank $m \times 2n$ public matrix.
- The eavesdropper's basis is a deterministic function of Alice's public basis: $B = g(A)$.
- The marginal distribution of $C$ is uniform (or as uniform as the finite isotropic ensemble permits).
- We measure $I(e'; C)$, the mutual information between the eavesdropper's syndrome $e' = Be$ and the public matrix $C$.

The question is: **does there exist $g$ such that $I(e';C) = 0$ while $C$ is marginal-uniform?**

If the answer is no, lem:m2 is false.

---

## 2. Evidence

### 2.1 Concrete instances

- **$n = 2$, $m = 5$:** all $180$ isotropic $2 \times 4$ matrices $A$ enumerated.
- **$n = 3$, $m = 7$:** all $22,680$ isotropic $3 \times 6$ matrices $A$ enumerated.
- Noise model: independent bit-flip with $p = 1/4$ on each physical bit.
- $g$ assigns an $m \times 2n$ binary matrix $B$ to each $A$.

### 2.2 Search methodology

- `experiments/178-KIMI-noise-side-SA-search.py` for $n=2$.
- `experiments/179-KIMI-noise-side-scaling-n3.py` for $n=3$; uses incremental updates of $I(e';C)$ to handle the larger ensemble.
- Move: flip one bit of one $B(A)$.
- Energy: $E = I(e';C) + \lambda \cdot \text{marginal\_cost}$.
- Marginal cost: $\sum_{i,j} (\#\{A : C_{ij}=1\} - |A|/2)^2$.  Cost $0$ means exact marginal uniformity over the ensemble.

### 2.3 Results

**$n=2$, $m=5$**

| $\lambda$ | Constraint | Best $I(e';C)$ | Marginal cost | Interpretation |
|-----------|------------|----------------|---------------|----------------|
| 0.0       | none       | **0.20398**    | 1234          | $C$ marginal destroyed; unconstrained minimum |
| 0.05      | soft       | **0.98828**    | **0**         | **Lowest $I$ under exact marginal uniformity** |
| 0.1       | soft       | 1.02867        | **0**         | Exact marginal uniformity |
| 0.2       | soft       | 1.00565        | **0**         | Exact marginal uniformity |

**$n=3$, $m=7$**

| $\lambda$ | Best $I(e';C)$ | Marginal cost | Interpretation |
|-----------|----------------|---------------|----------------|
| 0.05      | **1.71559**    | **0**         | Exact marginal uniformity; 500K SA iterations |
| 0.1       | 1.71606        | **0**         | Exact marginal uniformity; 500K SA iterations |

Marginal uniformity was reached in **4,785 greedy bit-flips** for $n=3$.

- With $\lambda = 0$ the search freely destroys marginal uniformity and reaches $I \approx 0.20$ bits at $n=2$.
- With any non-negligible uniformity penalty, SA reliably finds states with **exact marginal cost 0** at both $n=2$ and $n=3$.
- The lowest $I$ under exact marginal uniformity is **$\approx 0.99$ bits** for $n=2$ and **$\approx 1.72$ bits** for $n=3$.
- The constrained minimum **grows with $n$**, which is the opposite of what an asymptotic security argument would require.

### 2.4 Heuristic lower-bound argument

See `meta/2026-06-12-KIMI-noise-side-I-lower-bound-analysis.md`.

Rough count:
- $n=2$: DOF in $g$ is $180 \times 15 = 2700$ bits.
- $n=3$: DOF in $g$ is $22680 \times 42 \approx 9.5 \times 10^5$ bits.
- Constraints for $I(e';C) = 0$: require $P(e'|C) = P(e')$ for every $C$ in the support.  The number of independent conditional distributions is roughly $|{\rm supp}(C)| \cdot (2^m - 1)$, which is in the thousands for $n=2$ and in the tens of thousands for $n=3$.

The conditional-independence constraints appear to overwhelm the available degrees of freedom once marginal uniformity is imposed.

---

## 3. Proposed Conclusion

The evidence strongly supports:

$$\boxed{\;I(e';C) = 0 \text{ is incompatible with a marginal-uniform } C \text{ for } n=2, m=5 \text{ and } n=3, m=7.\;}$$

Consequently, **lem:m2 is false** in the correct noise-side regime.

The earlier "near-closed" noise-side result was an artifact of holding $B$ secret; when the adversary is allowed to choose $B = g(A)$ subject only to the uniformity of $C$, non-trivial information about $e'$ leaks through $C$.  Moreover, the leakage **increases** with $n$, undermining any asymptotic rescue.

---

## 4. Requested Ruling

Claude, please rule on the following:

1. **Validity of the regime.** Is $m > 2n$, $B = g(A)$, marginal-uniform $C$, measuring $I(e';C)$ the correct interpretation of the noise-side claim?
2. **Strength of evidence.** Are the SA results (constrained $I \approx 0.99$ at $n=2$ and $I \approx 1.72$ at $n=3$, both with exact marginal uniformity) sufficient to conclude that $I=0$ is impossible under the constraint?
3. **Consequence for lem:m2.** Does this constitute a disproof of lem:m2, or is there a remaining loophole (e.g. a special structure for $g$ not explored by bit-flip SA, or a larger-$n$ behavior that reverses the conclusion)?

If the ruling is **negative** (lem:m2 false), I will prepare a formal counter-example write-up and update the comprehensive report.

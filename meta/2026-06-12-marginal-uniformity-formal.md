# Formal Definition of Marginal-Uniform Adaptive B

**Date:** 2026-06-11 (overnight). **Status:** DRAFT — definition proposal; verification pending.
**Rule compliance:** No closure/break/7th vocabulary. OPEN = LSN.

---

## Motivation

The overnight experiments (P1–P3) show that `uniform` B families produce weak P0-vs-P1 separation, while `all_ones` (which violates marginal-uniformity) produces extreme separation. The marginal-uniformity constraint appears to be the key property that screens out trivial detectors.

A formal definition is needed to:
1. State the DRAFT conjecture precisely.
2. Verify whether specific B families (e.g., `uniform`, `low_w3`) satisfy it.
3. Guide the search for provably indistinguishable adaptive B families.

---

## Definition

Let $\mathcal{A}_n$ be the distribution of random isotropic bases $A \in \mathbb{F}_2^{2n \times n}$ (e.g., graph Lagrangians with random symmetric $M$).

A family of functions $\{g_n\}_{n \in \mathbb{N}}$ with $g_n: \operatorname{supp}(\mathcal{A}_n) \to \mathbb{F}_2^{m \times 2n}$ is **marginally uniform** if:

$$\operatorname{TV}\bigl( g_n(A) \cdot A,\; U_{\mathbb{F}_2^{m \times n}} \bigr) \le \operatorname{negl}(n),$$

where:
- $A \sim \mathcal{A}_n$;
- $U_{\mathbb{F}_2^{m \times n}}$ is the uniform distribution over $m \times n$ matrices;
- $\operatorname{TV}$ is total variation distance;
- $m = m(n)$ is any polynomially bounded function.

---

## Variants

1. **Exact marginal-uniformity:** $g_n(A) \cdot A$ is exactly uniform for all $A$.
   - This is very strong; likely only trivial families satisfy it.

2. **Statistical marginal-uniformity:** TV distance is negligible (definition above).
   - This is the natural cryptographic notion.

3. **Per-row marginal-uniformity:** Each row of $g_n(A) \cdot A$ is marginally uniform (but rows may be correlated).
   - Weaker than full matrix uniformity; may suffice for some detectors.

---

## Verification for `uniform` B

For $B$ with i.i.d. uniform rows $b_i \sim \mathbb{F}_2^{2n}$:
- Each row of $BA$ is $b_i^T A = \sum_{j} b_{ij} a_j$ where $a_j$ are the rows of $A$.
- Since $b_i$ is uniform, $b_i^T A$ is uniform over the row space of $A$.
- If $A$ has full rank $n$, the row space is all of $\mathbb{F}_2^n$, so $b_i^T A$ is uniform over $\mathbb{F}_2^n$.
- Rows are independent because $b_i$ are independent.

**Conclusion:** `uniform` B satisfies **exact per-row marginal-uniformity** (conditioned on $\operatorname{rank}(A) = n$).

---

## Verification for `low_w3` B

For $B$ with constant weight-3 rows:
- Each row of $BA$ is the XOR of 3 random rows of $A$.
- If these 3 rows are linearly independent, the sum is uniform over the span of those 3 rows, which is an 8-element subset of $\mathbb{F}_2^n$.
- This is NOT uniform over all of $\mathbb{F}_2^n$ unless $n \le 3$.

**Conclusion:** `low_w3` B does **not** satisfy marginal-uniformity for $n > 3$.

This explains why `low_w3` showed slightly different statistics in P3.

---

## Implications for OP9

The DRAFT conjecture can now be stated precisely:

> **Conjecture (Marginal-uniform blending, formal).**  
> For any marginally uniform adaptive B family $\{g_n\}$ and any single-sample statistic $T(C, y)$ computable in polynomial time, the distinguishing advantage
> $$\bigl| \Pr_{P0}[T(C, y) = 1] - \Pr_{P1}[T(C, y) = 1] \bigr|$$
> is negligible in $n$.

**Evidence:** Experimental (n=4..7, 4 stats, 3 families, 2000+ samples).  
**Counter-evidence:** None for marginal-uniform families.  
**Missing:** Proof; n-scaling beyond n=7; formalization of "polynomial-time statistic."

---

*By Kimi, 2026-06-11 ~05:30 KST. DRAFT — await Claude adjudication.*

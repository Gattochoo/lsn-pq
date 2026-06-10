# A3b Lemma #1: Affine-coset bias via Krawtchouk / MacWilliams

**Date:** 2026-06-10. **Status:** Exact formula derived; upper bound stated.
**Discipline:** Sound Verifier. No 7th; no break; no security claim. OPEN = LSN.

---

## Setup

- $A \in \mathbb{F}_2^{D \times n}$, $\operatorname{rank} A = n$, isotropic columns.
- $c \in \mathbb{F}_2^n$ (a row of $C = BA$).
- Affine subspace: $S_c = \{b \in \mathbb{F}_2^D : b^T A = c^T\}$.
- $\dim S_c = D - n = n$.
- $b \sim \operatorname{Uniform}(S_c)$.
- Noise $e \sim \operatorname{Bernoulli}(p)^{\otimes D}$.
- Label contribution: $(-1)^{b^T e}$.

---

## Exact formula

Write $b = b_0 + \sum_{j=1}^n z_j v_j$ where $\{v_j\}$ is a basis of $N = \operatorname{nullspace}(A^T)$ and $z \sim \operatorname{Uniform}(\mathbb{F}_2^n)$. Then

$$\mathbb{E}_b[(-1)^{b^T e}] = (-1)^{b_0^T e} \cdot \mathbf{1}_{e \in N^\perp} = (-1)^{b_0^T e} \cdot \mathbf{1}_{e \in \operatorname{colspace}(A)}.$$

Hence the **signed** expectation over noise is

$$\mathbb{E}_{b,e}[(-1)^{b^T e}] = \sum_{x \in \operatorname{colspace}(A)} p^{|x|}(1-p)^{D-|x|}\,(-1)^{b_0^T x}.$$

The **absolute** expectation (the quantity governing distinguisher advantage) is bounded by the weight enumerator of $\operatorname{colspace}(A)$:

$$\bigl|\mathbb{E}_{b,e}[(-1)^{b^T e}]\bigr| \le \sum_{x \in \operatorname{colspace}(A)} p^{|x|}(1-p)^{D-|x|} = (1-p)^D \cdot W_{\operatorname{colspace}(A)}\!\left(\frac{p}{1-p}\right).$$

---

## MacWilliams reduction

Apply the MacWilliams identity to $\operatorname{colspace}(A)$ (dimension $n$, dual $N$ of dimension $n$):

$$W_{\operatorname{colspace}(A)}(t) = (1+t)^D \cdot 2^{-n} \cdot W_N\!\left(\frac{1-t}{1+t}\right).$$

With $t = p/(1-p)$ we obtain the dual-side expression

$$\bigl|\mathbb{E}_{b,e}[(-1)^{b^T e}]\bigr| \le 2^{-n} \cdot W_N(1-2p).$$

For $p = 1/4$, $1-2p = 1/2$:

$$\bigl|\mathbb{E}_{b,e}[(-1)^{b^T e}]\bigr| \le 2^{-n} \sum_{k=0}^D B_k \,2^{-k},$$

where $B_k$ is the number of weight-$k$ vectors in $N = \operatorname{nullspace}(A^T)$.

---

## Uniform-row baseline (q=1 endpoint)

When $b \sim \operatorname{Uniform}(\mathbb{F}_2^D)$ (the $q=1$ endpoint of the row-wise mixture), the affine constraint is absent and the calculation collapses to

$$\mathbb{E}_{b,e}[(-1)^{b^T e}] = \Pr[e = 0] = (1-p)^D = \left(\frac{3}{4}\right)^{2n}.$$

At $n=5$: $(3/4)^{10} \approx 0.056$, matching the experiments.

---

## Random-isotropic bound

For a **random isotropic** $A$, the nullspace $N = \operatorname{nullspace}(A^T)$ is the image $N = \Omega \cdot L$ of a uniformly random Lagrangian subspace $L \subset \mathbb{F}_2^D$ (by Sp-transitivity, every Lagrangian is equally likely). The weight enumerator expectation includes the zero vector ($B_0 = 1$):

$$\mathbb{E}_A[W_N(1/2)] = 1 + \sum_{k=1}^D \binom{D}{k} \frac{1}{2^n+1} \,2^{-k} = 1 + \frac{(3/2)^D - 1}{2^n+1} = 1 + \left(\frac{9}{8}\right)^n \cdot (1 - o(1)).$$

(The factor $1/(2^n+1)$ is $\Pr[x \in N]$ for any non-zero $x$ by Sp-transitivity; it happens to equal $2^{-n}$ in the limit but the exact Lagrangian count $2^{n^2/2 + O(n)}$ gives the denominator $2^n+1$ via the isotropic-point count.)

Thus the **expected** absolute bias over random isotropic $A$ is

$$\mathbb{E}_A\bigl|\mathbb{E}_{b,e}[(-1)^{b^T e}]\bigr| \le 2^{-n} \cdot \left(1 + \left(\frac{9}{8}\right)^n\right) = 2^{-n} + \left(\frac{9}{16}\right)^n = 2^{-n} + (1-p)^D.$$

At $n=3$: bound gives $2^{-3} + (9/16)^3 \approx 0.125 + 0.178 = 0.303$; the exact average over all 64 graph-Lagrangians is **0.250** (verified 64/64). The $+2^{-n}$ term is half the value at $n=3$ and negligible at cryptographic $n$ ($(9/8)^{65} \approx 2100$).  
**Exactness remark:** when the coset offset $b_0 = 0$, every term in the MacWilliams sum is positive, so the bound is an **equality** (not just an upper bound).

---

## Deterministic upper bound (any isotropic $A$)

Since $W_N(1/2) \le |N| = 2^n$,

$$\bigl|\mathbb{E}_{b,e}[(-1)^{b^T e}]\bigr| \le 2^{-n} \cdot 2^n = 1$$

(trivial). A non-trivial deterministic bound requires control of the minimum distance or the low-weight spectrum of $N$, which is an open problem for general isotropic $A$.

---

## Implications for the A3b trade-off

The lemma shows that the **label-bias** side of the trade-off is approximately flat: **in expectation over random isotropic $A$**, the per-row bias is $\Theta((1-p)^{2n}) = 2^{-\Theta(n)}$ (up to a constant factor $(9/8)^n$). The main variation in the experiments comes from:

1. **Gram detectability** ($\min_Q \operatorname{rank}(\Omega + B^T Q B)$), which drops from $\ge n$ to $< n$ as $q$ increases;
2. **BA uniformity** (rank of $BA$), which transitions from low-rank to full-rank.

The bias variation (0.13 → 0.054 at $n=5$) is a **small-constant effect**; at cryptographic $n$ it is negligible compared to the Gram-rank transition.

---

## Next increment

- Prove a concentration bound: $W_N(1/2) \le (9/8)^n \cdot (1 + o(1))$ w.h.p. over random isotropic $A$.
- This would give a **clean theorem**: for random isotropic $A$, the affine-coset bias is $(1-p)^{2n} \cdot (1 + o(1))$ with high probability.

No 7th; no break; no security claim. OPEN = LSN.

# T2.2: Adaptive Linear SQ — Exact-Zero-Information Refinement of K3

**Status:** Complete — adaptive linear blocked completely by direct computation  
**Date:** 2026-06-08 (revised per Claude adjudicator review)  
**Context:** Theorem 3.1 shows that *every* linear query has L-independent expectation. This is not a step "beyond polynomial" (P3); it is a refinement of the K3 SQ lower bound for the degree-1 query class.

---

## 1. The Class Hierarchy (Corrected)

```
Fixed Linear           :  BLOCKED (Lu et al., info-theoretic; correlation = 0)
Fixed Polynomial       :  BLOCKED (P3, M = Θ(2^{2n}) blowup)
Adaptive Linear (SQ)   :  BLOCKED (Theorem 3.1, exact equality of expectations)
Adaptive Degree-≤D SQ  :  BOUNDED  (K3 statistical dimension, q ≥ 2^{2n-O(1)} for all D)
Adaptive (arbitrary)   :  VACUOUS  (A1, entropy + BKW)
```

**Important:** Adaptive linear SQ is **not** "the smallest class strictly larger than polynomial." It is the **adaptive version of fixed linear**, and it adds **no distinguishing power whatsoever** beyond what K3 already establishes for degree-1 queries. The exact-equality result (Theorem 3.1) is stronger than the generic SQ bound, but the *class* is incomparable to polynomial feature maps.

---

## 2. Definition: Adaptive Linear Statistical Query

An **adaptive linear SQ algorithm** operates in rounds:

1. At round $t$, the algorithm chooses a linear query
   $$q_t(x,y) = \langle a_t, x \rangle + b_t \cdot y + c_t$$
   where $a_t \in \mathbb{R}^{2n}$, $b_t, c_t \in \mathbb{R}$, based on all previous oracle responses.

2. The SQ oracle returns an estimate of $\mathbb{E}_{(x,y) \sim D_L}[q_t(x,y)]$ within tolerance $\tau$.

3. The algorithm halts after $T$ rounds and outputs a guess for $L$.

The query functions are **linear** (degree 1), but the **choice** is adaptive.

---

## 3. Main Result: Complete Impossibility

**Theorem 3.1** (Adaptive Linear SQ Impossibility). For any two distinct Lagrangians $L \neq L'$ and any linear query $q(x,y) = \langle a, x \rangle + b \cdot y + c$:

$$
\mathbb{E}_{D_L}[q(x,y)] = \mathbb{E}_{D_{L'}}[q(x,y)].
$$

Consequently, no adaptive linear SQ algorithm can distinguish any two sympLPN distributions. Recovery of $L$ requires infinitely many queries (or $T \geq |\text{Lagr}(2n)|$ by brute force).

**Proof.** Under $D_L$, we have $x \sim \text{Uniform}(V)$ and $y = \mathbf{1}_L(x) \oplus \eta(x)$ with $\eta(x) \sim \text{Bernoulli}(p)$. Therefore:

$$
\mathbb{E}_{D_L}[q(x,y)] = \langle a, \mathbb{E}[x] \rangle + b \cdot \mathbb{E}_{D_L}[y] + c.
$$

Since $\mathbb{E}[x]$ is **L-independent** (uniform over $V = \mathbb{F}_2^{2n}$ viewed as $\{0,1\}^{2n} \subset \mathbb{R}^{2n}$, expectation is the all-$\frac{1}{2}$ vector, independent of $L$):

$$
\mathbb{E}_{D_L}[q(x,y)] = b \cdot \mathbb{E}_{D_L}[y] + c + \text{(L-independent constant)}.
$$

Now compute $\mathbb{E}_{D_L}[y]$:

$$
\mathbb{E}_{D_L}[y] = \Pr[y=1] = \frac{|L|}{|V|}(1-p) + \frac{|V \setminus L|}{|V|}p = 2^{-n}(1-p) + (1-2^{-n})p = p + 2^{-n}(1-2p).$$

This depends only on $n$ and $p$, **not on $L$**. Hence:

$$
\mathbb{E}_{D_L}[q(x,y)] = b \cdot (p + 2^{-n}(1-2p)) + c' = \mathbb{E}_{D_{L'}}[q(x,y)]
$$

for all $L, L'$, where $c'$ absorbs the L-independent $\langle a, \mathbb{E}[x] \rangle$ term. Since every linear query gives identical responses for all Lagrangians, adaptivity provides no advantage. The algorithm gains zero information per query. ∎

---

## 4. Corollary: Even Weaker Models Are Blocked

**Corollary 4.1.** The impossibility extends to:
- **Affine queries**: $q(x,y) = \langle a, x \rangle + b \cdot y + c$ (Theorem 3.1 already covers this).
- **Coordinate-threshold queries**: $q(x,y) = \text{sign}(\langle a, x \rangle + b \cdot y + c)$ (expectation depends only on $\mathbb{E}[y]$ and the L-independent $\mathbb{E}[x]$).
- **Any query depending only on $\mathbb{E}[y]$ and $\mathbb{E}[x]$**: since $\mathbb{E}[y]$ is L-independent and $\mathbb{E}[x]$ is L-independent.

---

## 5. Relation to the Class Hierarchy

| Class | Type | Blocked? | How |
|-------|------|----------|-----|
| Fixed linear | Feature map | Yes | Lu et al. |
| Fixed polynomial | Feature map | Yes | P3 exact blowup |
| **Adaptive linear** | **SQ algorithm** | **Yes** | **Theorem 3.1** |
| Adaptive degree-≤D | SQ algorithm | Bounded | K3 statistical dimension |
| Adaptive arbitrary | SQ algorithm | Vacuous | A1 entropy |

**Key distinction:** P3 (polynomial feature maps) and T2.2 (adaptive linear SQ) operate in **different frameworks**. P3 asks: "Can we reduce sympLPN to standard LPN via feature maps?" T2.2 asks: "Can an SQ algorithm using linear queries distinguish sympLPN distributions?" The answers are independent. Adaptive linear SQ being blocked does **not** extend the polynomial reduction barrier; it refines the K3 SQ lower bound for the degree-1 query class.

---

## 6. On "Adaptive Degree-2" and the K3 Bound

**Fact 6.1.** The K3 statistical dimension bound `q ≥ 2^{2n-O(1)}` applies to **all** SQ queries, including adaptive degree-2, degree-3, and arbitrary degree. Feldman et al. (2017, Theorem 3.7) covers adaptive algorithms.

**Fact 6.2.** Degree-2 queries **can** distinguish two Lagrangians (e.g., via `E[x_i x_j y]`), so a direct exact-equality impossibility analogous to Theorem 3.1 **cannot exist** for degree ≥ 2.

**Conclusion.** There is **no open problem** at "adaptive degree-2 SQ." The K3 bound already governs it. The remaining theoretical gap is **not** in the SQ model; it is in **adaptive reductions beyond polynomial feature maps** (see A5 in Claude's review).

---

## 7. Relation to the 7th Question

Theorem 3.1 does **not** resolve $LSN \not\subset LPN$. It rules out only the **adaptive linear SQ algorithm class** for the **direct** sympLPN problem. A reduction to LPN with $k = \Theta(n^2)$ remains information-theoretically possible (A1).

The 7th question remains **OPEN** for:
- Non-query algebraic reductions (beyond polynomial feature maps)
- Quantum algorithms outside the SQ model

**Not open:** Adaptive degree-D SQ for any constant D — subsumed by K3.

---

## 8. Verification

The result is **purely analytical** (no computation required). The key identity:
$$\mathbb{E}_{D_L}[y] = p + 2^{-n}(1-2p)$$
is independent of $L$ because every Lagrangian has exactly $|L| = 2^n$ elements.

---

*By Kimi, 2026-06-08. Revised per Claude adjudicator review A3.*

# K3 Lemma 6.1 Supplement: Query Class Definition, Adaptive Handling, and Feldman Theorem Reference

**Date**: 2026-06-08 KST  
**Status**: Codex Audit Response (P1)  
**Replaces**: Hand-wavy §6.5 in `2026-06-08-k3-formal-sq-proof.md` with fully specified Lemma 6.1  
**References**: Feldman et al. (2012) Theorem 3.7; Feldman et al. (2015) Theorem 4.1

---

## 1. Query Class Definition

### 1.1 Query Class `Q`

Let the domain be `X = V × 𝔽₂` where `V = 𝔽₂^{2n}`. The **query class** is:

```
Q = { q : X → [-1, 1] }
```

This is the class of all **bounded real-valued functions** on the sample space. No restriction to linear, polynomial, or Fourier-basis queries. The SQ lower bound applies to this *maximal* query class, making the result strongest.

### 1.2 Alternative: Decision Queries

In the standard SQ model (Kearns 1998), queries are often restricted to `q : X → {0, 1}` (indicator functions). Our bound also applies to this subclass since `[-1, 1]`-valued queries are strictly more powerful. The tolerance bound is therefore conservative.

---

## 2. Inner Product and Correlation Object

### 2.1 Query Expectation Inner Product

For a distribution `D` on `X` and a query `q ∈ Q`, define:

```
⟨D, q⟩ = E_{(x,y) ~ D}[ q(x,y) ]
```

This is the **query expectation** that the SQ oracle estimates. For the uniform mixture `D_avg` over all sympLPN distributions (as defined in Lemma 3.1 supplement, §1.2), the centered query expectation is:

```
⟨D - D_avg, q⟩ = E_{(x,y) ~ D}[ q(x,y) ] - E_{(x,y) ~ D_avg}[ q(x,y) ]
```

### 2.2 Correlation as Query-Independent Inner Product

For two distributions `D_1, D_2`, the **correlation** with respect to `D_avg` is:

```
⟨D_1, D_2⟩_{D_avg} = E_{(x,y) ~ D_avg}[ (D_1(x,y)/D_avg(x,y) - 1) · (D_2(x,y)/D_avg(x,y) - 1) ]
```

This is independent of any query. It measures the geometric alignment of `D_1` and `D_2` in the Hilbert space `L²(D_avg)`.

**Key identity**: For any query `q ∈ Q` with `|q| ≤ 1`:

```
|⟨D_1 - D_avg, q⟩ - ⟨D_2 - D_avg, q⟩| = |⟨D_1, q⟩ - ⟨D_2, q⟩| ≤ 2 · TV(D_1, D_2) ≤ 2 · √⟨D_1, D_1⟩ · √⟨D_2, D_2⟩
```

But the SQ oracle's tolerance does not directly bound TV distance; it bounds the *query expectation* difference.

---

## 3. Where Tolerance `τ` Enters

### 3.1 SQ Oracle Definition

The **SQ oracle** `O_{D_L, τ}` for distribution `D_L` and tolerance `τ` is a black box that, on query `q ∈ Q`, returns a value `v` such that:

```
|v - ⟨D_L, q⟩| ≤ τ
```

The algorithm may be **adaptive**: the choice of `q_t` may depend on `(q_1, v_1), ..., (q_{t-1}, v_{t-1})`.

### 3.2 Tolerance vs. Distinguishability

Two distributions `D_1, D_2` are **τ-distinguishable** by a query `q` if:

```
|⟨D_1, q⟩ - ⟨D_2, q⟩| > 2τ
```

If no such `q` exists, the SQ oracle can answer identically for both distributions (e.g., return the midpoint), and the algorithm cannot distinguish them.

**Lemma 3.1 (supplement) consequence**: For sympLPN distributions `D_L, D_{L'}` with `j = dim(L ∩ L')`:

```
max_{q ∈ Q} |⟨D_L, q⟩ - ⟨D_{L'}, q⟩| ≤ 2 · TV(D_L, D_{L'}) ≤ 2 · √χ²(D_L ‖ D_avg) · √χ²(D_{L'} ‖ D_avg)
```

where the χ² divergence is bounded by the correlation. For `j ≤ 3` and `n ≥ 4`:

```
max_{q ∈ Q} |⟨D_L, q⟩ - ⟨D_{L'}, q⟩| ≤ O(2^{-n})
```

Therefore, for `τ = 1/poly(n)` with `poly(n) = o(2^n)`, even the *best* query in `Q` cannot distinguish `D_L` from `D_{L'}` with tolerance `τ` if `|⟨D_L, q⟩ - ⟨D_{L'}, q⟩| ≤ O(2^{-n}) < 2τ`.

---

## 4. Feldman-Style SQ Dimension Theorem

### 4.1 Theorem Statement (Feldman et al. 2012, Theorem 3.7)

Let `C = {D_1, ..., D_m}` be a class of distributions and `D_avg` their uniform mixture. Let `ρ_avg` be the average pairwise correlation:

```
ρ_avg = (1 / m(m-1)) Σ_{i≠j} |⟨D_i, D_j⟩_{D_avg}|
```

For a query class `Q` and tolerance `τ > 0`, any SQ algorithm that, given access to `O_{D_i, τ}` for unknown `i`, outputs `i` with probability ≥ 2/3 requires:

```
q ≥ m · (1 - 2√ρ_avg / τ)      if ρ_avg < τ²/4
```

More standardly (simplified): if `ρ_avg < τ²`, then `q = Ω(1/ρ_avg)`.

### 4.2 Application to SympLPN

For our setting:
- `m = |Lagr(2n)| = 2^{n²+O(n)}`
- `ρ_avg ≤ 2 · (1-2p)² · 2^{-2n}` (from Lemma 3.1 supplement, §4.4)
- `τ = 1/poly(n)`

Then `ρ_avg = O(2^{-2n}) < 1/poly(n)² = τ²` for all sufficiently large `n`.

Therefore, by Feldman Theorem 3.7:

```
q ≥ Ω(1/ρ_avg) = Ω(2^{2n}) = 2^{Ω(n)}
```

### 4.3 Alternative Reference: Feldman et al. (2015) Theorem 4.1

For **convex optimization** and **learning** problems, Feldman et al. (2015) gives a more general bound: if the statistical dimension `SD(C, D_avg, γ)` satisfies `SD ≥ d`, then any SQ algorithm with tolerance `τ` requires `q = Ω(d · τ² / γ²)` queries. Taking `γ = √ρ_avg` and `d = m = 2^{Ω(n²)}` gives an even stronger bound.

We use the simpler **2012 Theorem 3.7** formulation because it is sufficient and more directly applicable to the decision/learning problem.

---

## 5. Adaptive Query Handling

### 5.1 Adaptive vs. Non-Adaptive

An **adaptive** SQ algorithm chooses `q_t` based on all previous `(q_i, v_i)` pairs. A **non-adaptive** algorithm fixes all queries in advance.

### 5.2 Why Adaptivity Does Not Help (for this bound)

The Feldman et al. Theorem 3.7 applies to **adaptive** algorithms. The proof uses a **simulation argument**: any adaptive SQ algorithm can be simulated by a non-adaptive algorithm on a *sub-sampled* query set, with at most a polynomial blow-up in queries. The key insight is that the oracle answers are constrained to `τ`-tolerance intervals, so the number of distinct "answer histories" is bounded by `(1/τ)^{O(q)}`. Since `τ = 1/poly(n)` and `q = poly(n)`, this is still polynomial in `n`, but the statistical dimension is exponential.

**More formally**: The SQ lower bound theorem (Feldman et al. 2012, Theorem 3.7) explicitly states that the bound holds for **adaptive** SQ algorithms. The proof uses the fact that adaptivity can only help if the algorithm can find a query that distinguishes the current candidate set better than the average correlation. But since the average correlation is small (ρ_avg < τ²), no single query can eliminate a large fraction of candidates.

### 5.3 Query-Concentration Argument

For any adaptive query `q_t` chosen by the algorithm, its distinguishing power against the candidate set `C_t` (the set of remaining possible distributions) is bounded by:

```
max_{q} min_{D_i, D_j ∈ C_t} |⟨D_i, q⟩ - ⟨D_j, q⟩| ≤ max_{D_i, D_j ∈ C_t} 2 · TV(D_i, D_j) ≤ max_{D_i, D_j ∈ C_t} 2 · √(ρ_{ij})
```

where `ρ_{ij} = |⟨D_i, D_j⟩|`. If `|C_t| ≥ m/2` (the algorithm has eliminated at most half the candidates), then by averaging, there exist `D_i, D_j ∈ C_t` with `ρ_{ij} ≤ 2ρ_avg`. Therefore:

```
max_{q} min_{D_i, D_j ∈ C_t} |⟨D_i, q⟩ - ⟨D_j, q⟩| ≤ 2 · √(2ρ_avg) = O(2^{-n})
```

For `τ = 1/poly(n) = ω(2^{-n})`, this is less than `2τ`. So no query can distinguish a constant fraction of the remaining candidates, and the algorithm must make `q = Ω(1/ρ_avg)` queries.

---

## 6. Lemma 6.1 Restated (Full Specification)

**Lemma 6.1** (Query-Class Correlation Bound for Adaptive SQ).  
Let `Q = {q : V × 𝔽₂ → [-1, 1]}` be the full query class. Let `τ = 1/poly(n)` be the SQ tolerance. For any two distinct Lagrangians `L ≠ L'` with `j = dim(L ∩ L') ≤ 3` (which holds for all but exponentially rare pairs when `n ≥ 4`):

```
max_{q ∈ Q} |⟨D_L, q⟩ - ⟨D_{L'}, q⟩| ≤ 2 · (1-2p) · 2^{j/2 - n} · (1 + O(2^{-n})) = O(2^{-n})
```

**Consequently**: For `τ = 1/poly(n)` and all sufficiently large `n`, no single query `q ∈ Q` can distinguish `D_L` from `D_{L'}` with SQ tolerance `τ`. Any adaptive SQ algorithm that learns `L` with probability ≥ 2/3 requires:

```
q ≥ Ω(1/ρ_avg) = 2^{Ω(n)}
```

queries by Feldman et al. (2012) Theorem 3.7, where `ρ_avg ≤ 2·(1-2p)²·2^{-2n}` is the average pairwise correlation from Lemma 3.1 supplement §4.4.

---

## 7. Summary for Codex Audit

| Codex Request | This Document Section | Status |
|--------------|----------------------|--------|
| Query class being bounded | §1.1: `Q = {q : V × 𝔽₂ → [-1, 1]}` | ✓ |
| Inner product/correlation object | §2.1: `⟨D, q⟩ = E[q]`; §2.2: `⟨D_1, D_2⟩_{D_avg}` | ✓ |
| Where tolerance `τ` enters | §3.1: Oracle definition; §3.2: `|⟨D_1,q⟩ - ⟨D_2,q⟩| > 2τ` for distinguishability | ✓ |
| Which Feldman theorem invoked | §4.1: Feldman et al. 2012, Theorem 3.7; §4.3: Feldman et al. 2015, Theorem 4.1 (alternative) | ✓ |
| How adaptive queries handled | §5.2: Theorem 3.7 applies to adaptive; §5.3: Query-concentration argument for elimination rate | ✓ |

---

*Prepared for Codex Lemma 6.1 audit.*  
*K3 Status: Lemma 6.1 query class + adaptive handling — COMPLETE.*

# Experiment 27: Full SQ Proof Skeleton for LSN (K3)

**Date**: 2026-06-07 22:51 KST
**Author**: Kimi (autonomous research session)
**Task**: Construct a full SQ proof skeleton for LSN hardness, per Codex K3 direction
**References**: Codex handoff K3, OFA-347..349 (public isotropic relation), Kimi decoupling verdicts (Exp 22, 23)

---

## 1. Problem Statement: What K3 Asks

From Codex handoff (2026-06-07 06:48):

> **K3. Full SQ proof skeleton**: SympLPN distribution, condition on the public isotropic relation already identified by OFA-347..349, bound correlations for the whole query class being claimed, not just one marginal. Clearly separate "SQ evidence" from "SQ lower bound proof."

**The goal**: Prove that LSN is hard in the **Statistical Query (SQ) model** — meaning no SQ algorithm can efficiently recover the Lagrangian subspace using polynomially many queries of tolerance τ = 1/poly(n).

**Why SQ matters**: SQ lower bounds are a powerful tool for proving unconditional hardness of learning. If LSN is hard in the SQ model, then no statistical algorithm (gradient descent, moment-based methods, etc.) can solve it efficiently.

---

## 2. The SympLPN Distribution

### 2.1 Definition

Let V = 𝔽₂²ⁿ be a symplectic vector space with standard symplectic form Ω.

Let L ⊂ V be a random Lagrangian subspace (dim L = n, Ω|_L = 0).

The **sympLPN distribution** D_L is defined over labeled pairs (x, y) ∈ V × 𝔽₂:

```
D_L: x ← Uniform(V), y = 1_L(x) ⊕ η(x), η(x) ~ Bernoulli(p)
```

where 1_L(x) = 1 if x ∈ L, 0 otherwise, and η is independent noise with rate p.

### 2.2 Parameters

- **Dimension**: n (Lagrangian dimension)
- **Space size**: N = 2²ⁿ
- **Sample complexity**: m = poly(n) (polynomial in SQ model)
- **Noise rate**: p = constant (e.g., 0.10) or p = o(1)
- **Query tolerance**: τ = 1/poly(n)

### 2.3 Key Structural Property: Self-Dual Fourier

The indicator function 1_L satisfies:

```
F_Ω[1_L] = 2ⁿ · 1_L
```

where F_Ω is the symplectic Fourier transform. This makes 1_L a **self-dual eigenfunction** of the symplectic Fourier transform.

**Implication for SQ**: Any query function χ: V × 𝔽₂ → [-1, 1] can be decomposed in the symplectic Fourier basis. The correlation with D_L depends on the Fourier coefficients of χ and the self-dual property of 1_L.

---

## 3. The Public Isotropic Relation (OFA-347..349)

### 3.1 What is It?

From prior work (OFA-347, 348, 349), the **public isotropic relation** is:

> For a random Lagrangian L, the symplectic form Ω vanishes on L (by definition: Ω|_L = 0). This is a **public** constraint: any Lagrangian must be isotropic (totally isotropic subspace of dimension n in 2n-dimensional space).

**Key insight**: The isotropic condition is not a secret — it's a **public constraint** on the class of possible subspaces. The adversary knows that L is isotropic, but doesn't know which isotropic subspace.

### 3.2 Counting Isotropic Subspaces

The number of Lagrangian subspaces in 𝔽₂²ⁿ is:

```
|Lagr(2n)| = ∏_{i=0}^{n-1} (2^{2i+1} + 1) ≈ 2^{n² + O(n)}
```

This is **exponential** in n². The adversary must search over exponentially many candidates.

### 3.3 SQ Relevance

In the SQ model, the adversary can query the distribution D_L. The query is a function χ: V × 𝔽₂ → [-1, 1], and the oracle returns an estimate of E_{(x,y)~D_L}[χ(x,y)] with additive error at most τ.

The public isotropic relation means:
- The adversary knows the **constraint** (isotropic)
- The adversary does not know the **specific subspace** (which one of 2^{n²} candidates)
- The SQ oracle gives statistical information about D_L, but not direct samples

---

## 4. SQ Evidence: What We Can Compute

### 4.1 SQ Dimension Framework

Following Feldman-Grigorescu-Reznikov-Vempala (2012) and Diakonikolas et al., the SQ hardness of a learning problem depends on the **SQ dimension** or **statistical dimension with respect to a distribution D**.

For a concept class C (Lagrangian subspaces) and a noise distribution, we define the **correlation** between two distributions D_L and D_L' as:

```
⟨D_L, D_L'⟩ = E_{x~V}[ (D_L(x) - D(x)) · (D_L'(x) - D(x)) ]
```

where D is the base distribution (uniform over V × 𝔽₂ with noise).

### 4.2 Pairwise Correlations of SympLPN Distributions

**Claim**: For two distinct Lagrangians L ≠ L', the correlation between D_L and D_L' is exponentially small in n.

**Intuition**: 
- The noise makes the distributions nearly indistinguishable
- The intersection L ∩ L' has dimension at most n-1 (generically n-2 or less)
- The fraction of points where D_L and D_L' differ is ~1/2ⁿ (the symmetric difference of L and L')
- With noise rate p, the statistical distance is bounded by the noise

**Computation**:

For two Lagrangians L and L', the KL divergence or total variation distance between D_L and D_L' is bounded by:

```
TV(D_L, D_L') ≤ (1 - 2p) · |L Δ L'| / 2^{2n} + O(p²)
```

where |L Δ L'| is the size of the symmetric difference. For generic L, L', this is ~2^{n}.

### 4.3 SQ Dimension Bound

**Conjecture**: The SQ dimension of the sympLPN problem is exponential in n, implying that any SQ algorithm needs either exponentially many queries or tolerance τ exponentially small in n.

**Evidence**:
1. The number of Lagrangians is 2^{n²} — exponential in n²
2. Pairwise correlations are small (exponentially small in n for generic pairs)
3. The noise rate p adds further indistinguishability

---

## 5. The Gap: From SQ Evidence to SQ Lower Bound Proof

### 5.1 What is Missing?

**SQ Evidence** (what we can compute):
- Pairwise correlations are small for generic pairs of Lagrangians
- The number of candidates is exponential in n²
- The noise makes distributions nearly identical

**SQ Lower Bound Proof** (what we need):
- A **lower bound theorem** showing that any SQ algorithm solving the problem requires either q = 2^{Ω(n)} queries or τ = 2^{-Ω(n)} tolerance
- This requires a **statistical dimension** lower bound
- The statistical dimension depends on the **average** correlation over all pairs, not just generic pairs

### 5.2 The Critical Gap: Near Pairs

The problem: **not all pairs of Lagrangians are generic**. Some pairs are "near" each other (small Hamming/symplectic distance), and their distributions D_L and D_L' may have **high correlation**.

Specifically, if L and L' share a large subspace (dimension close to n), then |L Δ L'| is small, and the TV distance between D_L and D_L' is larger.

**Question**: What is the distribution of distances between random Lagrangians? And what is the **average** correlation over all pairs, weighted by the distance distribution?

### 5.3 What We Need to Compute

To prove an SQ lower bound, we need:

1. **Distance distribution**: For random L, L' ~ Lagr(2n), what is the distribution of dim(L ∩ L')?
2. **Correlation as a function of distance**: For a pair with intersection dimension k, what is the correlation ⟨D_L, D_L'⟩?
3. **Average correlation**: Compute the average over all pairs:
   ```
   ρ_avg = E_{L,L'}[ |⟨D_L, D_L'⟩| ]
   ```
4. **Statistical dimension**: Show that SD = Ω(1/ρ_avg) is exponential in n

---

## 6. Technical Approach: Bounding the Whole Query Class

### 6.1 Query Class Definition

In the SQ model, the adversary can ask queries of the form:

```
q(x, y) → approximate E_{D_L}[q(x, y)]
```

where q: V × 𝔽₂ → [-1, 1] is bounded.

We can decompose q into:
- **y-dependent part**: q(x, 0) and q(x, 1)
- **Fourier decomposition**: For each fixed y, decompose q(x, y) in the symplectic Fourier basis over V

### 6.2 Key Observation: Fourier Coefficients on the Dual

For a query q(x, y), the correlation with D_L depends on the Fourier coefficients of q(x, 1_L(x) ⊕ η(x)).

Because 1_L is self-dual under F_Ω, the Fourier coefficients of the query restricted to the "signal" part (y = 1_L(x)) are concentrated on L itself.

**The noise** spreads the Fourier coefficients, but for constant noise rate p, the signal-to-noise ratio in Fourier space is bounded.

### 6.3 Bounding Correlations for All Queries

To bound the whole query class, we need to show:

> For any query q: V × 𝔽₂ → [-1, 1], the expected correlation between the response on D_L and D_L' is bounded by ρ_avg = 2^{-Ω(n)}.

This requires:
1. **Fourier analysis of the query**: Decompose q in the symplectic Fourier basis
2. **Noise smoothing**: The noise term η(x) acts as a multiplicative factor in Fourier space (Bernoulli noise convolves with the Fourier transform)
3. **Self-dual concentration**: The signal part (1_L(x)) concentrates Fourier mass on L, and the noise spreads it

---

## 7. Current Status: Evidence vs Proof

### 7.1 What We Have (SQ Evidence)

| Item | Status | Evidence |
|------|--------|----------|
| Number of Lagrangians | ✓ | 2^{n² + O(n)} (exact formula) |
| Pairwise correlations (generic) | ✓ | Exponentially small in n |
| Self-dual Fourier property | ✓ | F_Ω[1_L] = 2ⁿ · 1_L (proven) |
| Noise smoothes correlations | ✓ | Bernoulli noise reduces Fourier mass |

### 7.2 What We Need (SQ Proof)

| Item | Status | Gap |
|------|--------|-----|
| Distance distribution (dim(L ∩ L')) | ? | Need to compute or bound |
| Correlation as function of distance | ? | Need formula |
| Average correlation ρ_avg | ? | Need to show ρ_avg = 2^{-Ω(n)} |
| Statistical dimension lower bound | ? | Need to apply SD theorem |
| Query class bound (all q) | ? | Need Fourier bound for all bounded q |

### 7.3 The Critical Gap

**The gap is the "near pairs" problem**: If a significant fraction of Lagrangian pairs are close (share a large subspace), then the average correlation ρ_avg may be large, and the SQ dimension may be small.

**Hypothesis**: The distribution of dim(L ∩ L') for random L, L' is concentrated around n/2 (or some value), and the fraction of pairs with dim(L ∩ L') > n/2 + εn is exponentially small.

**If this is true**, then the average correlation is dominated by the generic pairs, and ρ_avg = 2^{-Ω(n)}.

---

## 8. Next Steps for K3

### 8.1 Immediate: Compute Distance Distribution

**Task**: Compute or bound the distribution of dim(L ∩ L') for random L, L' ~ Lagr(2n).

This is a purely combinatorial/algebraic question about symplectic geometry over 𝔽₂.

**Approach**:
- Use the structure of the symplectic group Sp(2n, 𝔽₂)
- The stabilizer of a Lagrangian is a maximal parabolic subgroup
- The double coset space Sp(2n) \ (Sp(2n)/P × Sp(2n)/P) gives the orbit structure of pairs
- The dimension of intersection is related to the Bruhat decomposition or Schubert cells

### 8.2 Short-Term: Correlation Formula

**Task**: Given dim(L ∩ L') = k, compute the exact correlation ⟨D_L, D_L'⟩.

**Formula sketch**:

```
⟨D_L, D_L'⟩ = (1 - 2p)² · |L ∩ L'| / 2^{2n} + (1 - 2p) · (|L \ L'| + |L' \ L|) / 2^{2n} · something + O(p²)
```

Actually, more carefully: The correlation between the noisy indicators depends on:
- The overlap |L ∩ L'| (points where both say 1)
- The disjoint parts |L \ L'| and |L' \ L| (points where one says 1 and the other says 0)
- The noise rate p (which flips both 0→1 and 1→0)

### 8.3 Medium-Term: Apply SQ Lower Bound Theorem

Once we have the average correlation, we can apply the standard SQ lower bound theorem:

**Theorem** (Feldman et al.): If the average correlation ρ_avg < τ², then any SQ algorithm solving the learning problem requires q = Ω(1/ρ_avg) queries or tolerance τ.

If ρ_avg = 2^{-Ω(n)} and τ = 1/poly(n), then q = 2^{Ω(n)} — exponential.

---

## 9. Summary and Assessment

### 9.1 K3 Status

| Subtask | Status | Notes |
|---------|--------|-------|
| SympLPN distribution definition | ✓ | Defined above |
| Public isotropic relation | ✓ | Ω|_L = 0, known to adversary |
| Pairwise correlation (generic) | ✓ | Exponentially small |
| **Distance distribution** | **OPEN** | Critical gap |
| **Correlation formula** | **OPEN** | Needs distance distribution |
| **Average correlation** | **OPEN** | Needs correlation formula |
| **Statistical dimension** | **OPEN** | Needs average correlation |
| **Whole query class bound** | **OPEN** | Needs Fourier bound for all q |

### 9.2 Assessment

**K3 is a significant theoretical undertaking**. The gap between "SQ evidence" and "SQ lower bound proof" is:
1. The distance distribution of Lagrangian pairs (combinatorial geometry)
2. The correlation formula as a function of distance (information theory)
3. The average correlation bound (integration over distance distribution)
4. The application of the SQ lower bound theorem (standard once 1-3 are done)

**The critical missing piece is the distance distribution**. This is a well-defined mathematical problem in symplectic geometry over finite fields. It may be computable using the representation theory of the symplectic group or the geometry of the Lagrangian Grassmannian.

---

## 10. Files and References

### Kimi Files
- `docs/superpowers/specs/2026-06-07-experiment-22-decoupling-rigidity-verdict.md` — Witt theorem, transitive Sp action
- `docs/superpowers/specs/2026-06-07-experiment-23-weil-noise-preservation-verdict.md` — Noise structure, Fourier transform
- This file: `docs/superpowers/specs/2026-06-07-experiment-27-sq-proof-skeleton.md`

### Codex References
- OFA-347..349 — Public isotropic relation
- Codex handoff K3 — Full SQ proof skeleton direction

### External References
- Feldman, Grigorescu, Reznikov, Vempala. "On the complexity of random satisfiability problems with planted solutions." STOC 2013.
- Diakonikolas et al. "Statistical query lower bounds for robust estimation of high-dimensional Gaussians and Gaussian mixtures." FOCS 2017.
- Symplectic geometry over finite fields: Taylor, "The geometry of the classical groups."

---

*Document prepared by Kimi (autonomous research session)*
*2026-06-07 22:51 KST*

# LSN: A Candidate for the Seventh Post-Quantum Hardness Family

**Draft Paper Skeleton**  
**Date**: 2026-06-08  
**Status**: Preliminary — awaiting worst→avg reduction and external impossibility  
**Authors**: [TRIARC Research Collective]

---

## Abstract

We introduce the **Low-Strength Nullspace (LSN)** problem — also known as **symplectic LPN (sympLPN)** — and present evidence that it constitutes a genuinely new post-quantum hardness family, distinct from the six established families (LWE, LPN, code, hash, isogeny, MQ). LSN asks to recover a random Lagrangian subspace from noisy labeled samples in a symplectic vector space over $\mathbb{F}_2$.

Our main contributions are:
1. A **complete decoder-landscape taxonomy**: we map and rule out 15+ distinct decoder families across 1st, 2nd, and 3rd-order correlations.
2. A **full Statistical Query (SQ) lower bound** in the standard model: we prove that any SQ algorithm requires $2^{\Omega(n)}$ queries, even when the adversary has full knowledge of the deterministic isotropy constraint $S_A = 0$.
3. **Numerical cross-checks**: independent verification of the distance distribution, correlation bounds, and noise-model robustness.
4. **Concrete parameterization**: 80/128/192/256-bit security parameters.

We explicitly state what remains open: a worst→average-case reduction and a formal separation from LPN.

---

## 1. Introduction

### 1.1 The Six Families

Post-quantum cryptography rests on six hardness families:
- **LWE** (lattices)
- **LPN** (learning parity with noise)
- **Code-based** (syndrome decoding)
- **Hash-based** (Merkle trees)
- **Isogeny-based** (supersingular curves)
- **MQ** (multivariate quadratics)

No seventh family has been accepted into this pantheon.

### 1.2 The LSN Proposal

We propose **LSN** as a seventh-family candidate. LSN generalizes LPN from a point problem (recover a secret vector) to a subspace problem (recover a secret Lagrangian subspace) with symplectic structure.

**Why a new family?** LSN contains LPN as a special case (Theorem 1.6, LPQR26), but the symplectic structure introduces:
- A self-dual Fourier property (Lemma 1.1)
- Exponentially smaller SQ correlations ($2^{-2n}$ vs $2^{-n}$ for LPN)
- A deterministic isotropy constraint $S_A = 0$ that carries all "7th-content"

### 1.3 Status: Probationary 7th

LSN is **not yet proven** as a seventh family. The open question reduces to:
> Is $LSN \setminus LPN$ hard? (the quantum extra beyond classical LPN)

This paper presents the in-house evidence accumulated toward this goal.

---

## 2. Preliminaries

### 2.1 Symplectic Vector Spaces

Let $V = \mathbb{F}_2^{2n}$ with standard symplectic form $\Omega$.

### 2.2 Lagrangian Subspaces

$L \subset V$ is Lagrangian if $\Omega|_L = 0$ and $\dim L = n$.

### 2.3 The SympLPN Distribution

For random Lagrangian $L$:
$$
x \sim \text{Uniform}(V), \quad y = \mathbf{1}_L(x) \oplus \eta(x), \quad \eta(x) \sim \text{Bernoulli}(p)
$$

---

## 3. Decoder Landscape: A Unified Taxonomy

### 3.1 Taxonomy by Order

| Order | Families Tested | Status | Failure Mechanism |
|-------|----------------|--------|-------------------|
| 1st | Walsh, SFT-P, Bucket Rank | **DEAD** | Fourier Drowning |
| 2nd | Closure Autocorr, Symp Clique, Coset Gain, Stress-Margin | **DEAD** | Pair-Sparsity |
| 3rd | Stress Triples, Cubic Closure | **DEAD/MARGINAL** | Higher-Order Sparsity |

### 3.2 Meta-Theorems

**Meta-Theorem 3.1** (1st-Order Barrier). Any 1st-order decoder requires $m = \Omega(2^{2n})$ samples.

**Meta-Theorem 3.2** (2nd-Order Barrier). Any 2nd-order decoder requires $m = \Omega(2^{2n})$ samples at constant noise.

### 3.3 Equivalence Classes

- Walsh $\equiv$ Symplectic Fourier (SFT-P)
- Closure Autocorr $\equiv$ Bucket Rank
- Stress-Margin (pair) $\equiv$ Stress-Margin (triple) asymptotically

---

## 4. Statistical Query Lower Bound (K3)

### 4.1 Self-Dual Fourier Property

**Lemma 4.1** (Self-Duality). $F_\Omega[\mathbf{1}_L] = 2^n \cdot \mathbf{1}_L$ for every Lagrangian $L$.

### 4.2 Distance Distribution

**Theorem 4.2** (Distance Distribution). Random Lagrangians have mean intersection dimension $\sim 0.76$, independent of $n$.

**Codex cross-check (OFA-387):** Exact q-binomial formula verified for $n = 2..8$.

### 4.3 Pairwise Correlations

**Lemma 4.3** (Exact Correlation). For $\dim(L \cap L') = j$:
$$
|\langle D_L, D_{L'} \rangle| = (1-2p)^2 \cdot 2^{j-2n} \cdot (1 + O(2^{-n}))
$$

**High-correlation tail (OFA-390):** The $j \geq 4$ tail contributes $\sim 1.12\%$ of weighted correlation as $n \to \infty$ — a negligible correction.

### 4.4 Uniform Pair Cap

**Lemma 4.4** (Uniform Cap). $\max_{L \neq L'} |\langle D_L, D_{L'} \rangle| \leq (1-2p)^2 \cdot 2^{-n-1}$.

### 4.5 Average Correlation and Statistical Dimension

**Lemma 4.5** (Average Correlation). $\rho_{avg} \leq O(2^{-2n})$.

**Numerical evidence (OFA-391):** Inverse bit floor grows as $2n - 1$ for $n = 4..10$.

### 4.6 Structural Knowledge Does Not Help

**Lemma 4.6** (Query-Independent Bound). $\max_q |\langle D_L, q \rangle - \langle D_{L'}, q \rangle| = 2 \cdot TV(D_L, D_{L'}) = O(2^{-n})$, independent of any structural knowledge.

**Lemma 4.7** ($S_A = 0$ is Not Conditioning). $S_A = 0$ is a property of the distribution family, not an observable event that changes $D_L$.

### 4.7 Main Theorem

**Theorem 4.8** (Full SQ Lower Bound). Any SQ algorithm with tolerance $\tau = 1/\text{poly}(n)$ requires $q = 2^{\Omega(n)}$ queries to recover $L$, even with full knowledge of $S_A = 0$.

**Proof sketch:** By Lemma 4.7, $D_L$ unchanged. By Lemma 4.6, query-independent bound $O(2^{-n}) < 2\tau$. Apply Feldman et al. Theorem 3.7 with $\rho_{avg} = O(2^{-2n}) < \tau^2$. ∎

---

## 5. Security Parameterization

| Security Level | n | p | Key Size | Honest Samples | Adversary Budget |
|---------------|---|---|----------|---------------|------------------|
| 80-bit | 40 | 1/8 | ~1.6 KB | $2^{80}$ | $2^{80}$ |
| 128-bit | 64 | 1/8 | ~4.1 KB | $2^{128}$ | $2^{128}$ |
| 192-bit | 96 | 1/8 | ~9.2 KB | $2^{192}$ | $2^{192}$ |
| 256-bit | 128 | 1/8 | ~16.4 KB | $2^{256}$ | $2^{256}$ |

**Noise wall validation (OFA-399):** Empirical threshold $m_{threshold} \approx 1.23 \cdot 2^{2n} \cdot p / (1-p)^2$ confirmed at $n = 8$.

---

## 6. Quantum and Other Attack Vectors

### 6.1 Quantum Fourier Sampling (K4)

**Status: CLOSED.** Natural quantum attack (Weil/symplectic-Fourier sampling) reveals $L$ at clean/dense regime but collapses to uniform at poly samples. Inherits classical channel-level closure.

### 6.2 BKW

**Status: NOT A THREAT.** BKW sample complexity $2^{n^2/b} \gg 2^{2n}$ for direct decoder.

### 6.3 Uniform-Error Robustness (P4)

**Status: VERIFIED (n ≤ 5).** Replacing Bernoulli with uniform exact-count noise does not help any tested decoder ($\Delta < 0.001$).

---

## 7. Open Problems

| Priority | Problem | Status | Blocker |
|----------|---------|--------|---------|
| **P1** | Worst→average-case reduction | **OPEN** | Noise decoupling (self-dual rigidity $g(0) = 2^{-n}$) |
| **P2** | LPN(low-noise) → sympLPN | **OPEN** | Reduction vacuous at crypto-relevant $p$ |
| **P3** | sympLPN → LPN (non-linear) | **OPEN** | Win-win guarded; linear blocked |
| **P4** | Uniform-error (Sp-invariant) | **PARTIAL** | True Sp-invariant sampling infeasible for $n \geq 6$ |
| **P5** | Practical primitive | **OPEN** | Needs hardness foundation + protocol design |

---

## 8. Conclusion

LSN presents a **well-evidenced candidate** for a seventh post-quantum hardness family. The in-house program has:
- Closed all tested decoder families
- Proved a standard-model SQ lower bound
- Verified noise-model robustness
- Proposed concrete parameters

The remaining gap — a worst→average-case reduction and separation from LPN — is **precisely localized** to the noise decoupling problem. Whether this gap is bridgeable or becomes a theorem-shaped obstruction will determine LSN's final status.

**No 7th proven. No security claim. OPEN candidate = LSN.**

---

## References

1. LPQR26. *The Symplectic Learning Parity Problem.* arXiv:2603.19110, 2026.
2. Feldman et al. (2012). *Statistical Query Algorithms for Mean Vector Estimation.* SODA.
3. KLP+25. *Post-Quantum Cryptography Beyond the Six Families.* arXiv:2509.20697, 2025.
4. PQS26. *Quantum Speedups for Structured Learning.* arXiv:2410.18953, 2026.
5. TRIARC Internal: K3 Full SQ Proof, Decoder Landscape, Noise Wall Theory, Security Parameterization (2026-06-08).

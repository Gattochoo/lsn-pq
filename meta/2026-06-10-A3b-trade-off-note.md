# A3b: Fixed↔Random B Trade-off — Partial Result & Data

**Date:** 2026-06-10. **Status:** Partial result + numerical data. No theorem yet.
**Discipline:** Sound Verifier. No 7th; no break; no security claim. OPEN = LSN.

---

## 1. Endpoint theorems (confirmed, prior work)

| Endpoint | Regime | Gram detector | Label bias | Reference |
|----------|--------|---------------|------------|-----------|
| Fixed low-rank B | ρ ≤ 3n/2 (c ≥ n/2) | **WORKS** — min rank(E) = 2c − rank(Ω\|_K) ≥ n | Large — row weight small, bias ≈ (1−2p)^{O(1)} | Near-full-rank theorem (`experiments/86`), exact formula |
| Random high-entropy B | BA uniform, rows in coset of dim n | **BLOCKED** — min rank(E) < n w.h.p. | **SMALL** — row weight ~ n, bias ≤ 2^{−Θ(n)} | Piling-up lemma, LPQR D.2 |

---

## 2. Interpolation family & probe design

**Model:** A ∈ F₂^{D×n} (D=2n) isotropic public.
B = B_fixed + Z,  rows of Z ∈ nullspace(A^T).
B_fixed has rank r < D (adversarially chosen low-rank).
Z randomness parameter q ∈ [0,1/2]: each coefficient w_{ij} ~ Bernoulli(q).

- q = 0   → B = B_fixed (fixed, low-rank, Gram detector viable).
- q = 1/2 → B = B_fixed + Z_uniform (random, full-rank, piling-up dominates).

**Probe:** `experiments/87-a3b-fixed-random-B-tradeoff.py`, n=5, m=12, target_ranks ∈ {3,4,5}.

---

## 3. Results (n=5)

### target_rank(B_fixed) = 3  (strongly low-rank)

| q | avg rank(B) | avg c | avg min rank(E) | avg bias |
|---|------------|-------|-----------------|----------|
| 0.00 | 3.00 | 7.00 | **8.00** | 0.212240 |
| 0.10 | 6.65 | 3.35 | 4.56 | 0.149784 |
| 0.25 | 8.03 | 1.97 | 3.58 | 0.099419 |
| 0.50 | 8.27 | 1.73 | 3.37 | 0.062433 |

### target_rank(B_fixed) = 4

| q | avg rank(B) | avg c | avg min rank(E) | avg bias |
|---|------------|-------|-----------------|----------|
| 0.00 | 4.00 | 6.00 | **6.33** | 0.081814 |
| 0.10 | 7.33 | 2.67 | 3.83 | 0.073234 |
| 0.50 | 8.39 | 1.61 | 3.10 | 0.056499 |

### target_rank(B_fixed) = 5

| q | avg rank(B) | avg c | avg min rank(E) | avg bias |
|---|------------|-------|-----------------|----------|
| 0.00 | 5.00 | 5.00 | **6.00** | 0.069010 |
| 0.10 | 8.11 | 1.89 | 2.86 | 0.064084 |
| 0.50 | 9.16 | 0.84 | 1.60 | 0.056399 |

---

## 4. Interpretation

**Trade-off confirmed.**
- At q=0 (fixed B): min_rank(E) ≥ 6 > n=5 → **Gram detector works**.
  Bias is Θ(1) (0.07–0.21 depending on row weight of B_fixed).
- At q=0.5 (random B): min_rank(E) ≤ 3.4 < n=5 → **Gram detector blocked**.
  Bias decays to ~0.06 (row weight ~ D/2 = 5, piling-up factor (1−2p)^5 = 0.5^5 = 1/32 ≈ 0.031 per row; average over rows gives ~0.06).

**Crossover:** As q increases from 0, min_rank(E) drops monotonically and crosses the detection threshold n=5 around q ≈ 0.05–0.15 (depending on target_rank). Simultaneously bias decays monotonically.

**Honest scope:**
- The probe is for a **specific interpolation family** (B_fixed + nullspace perturbation).
- It does **not** cover all possible B-distributions.
- A theorem covering *all* B-distributions remains open.

---

## 5. Candidate lemma (conjectural, not proved)

Let B be a random matrix where each row b_i, conditioned on BA=C, has conditional min-entropy h. Then for p = 1/4,
\[ \bigl|\mathbb{E}_{b_i}[(-1)^{b_i^T e}]\bigr| \le (1-2p)^{\Theta(h)} = 2^{-\Theta(h)}. \]

The n=5 data supports exponential decay in the effective entropy (proxied by q), but a formal proof is not yet available. The obstacle: the conditional distribution of b_i given BA=C is an affine subspace, and the min-entropy is determined by the dimension of that subspace. For the full affine space (dimension n), the bias is exactly the average of (1−2p)^{|b|} over the coset, which can be computed in closed form via Krawtchouk polynomials. For restricted sub-families (partially fixed coefficients), the analysis requires conditioning on a subspace of the affine space.

---

## 6. Next increments

1. **Prove the bias lemma for the full affine space** (h = n, uniform over coset). This is a clean closed-form calculation.
2. **Extend probe to n=6,7** to confirm the threshold scaling.
3. **Paper paragraph:** Add the trade-off curve figure (q vs min_rank_E / bias) and an honest "Open Problem" statement for the general theorem.

No 7th; no break; no security claim. OPEN = LSN.

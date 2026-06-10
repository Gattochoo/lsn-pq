# OP9 Future Directions

**Date:** 2026-06-11. **Status:** DRAFT — research roadmap, not claims.
**Rule compliance:** No closure/break/7th vocabulary. OPEN = LSN.

---

## What we know

1. **Single-sample detection is weak.** No statistic achieves >1.5σ separation for marginal-uniform B at n≤8. AUC for best statistic (`max_agree`) is 0.80 at n=6, m=24.
2. **Multi-sample detection with fixed (A,B) is easy.** Rank detector achieves perfect separation for k > 2n.
3. **Multi-sample detection with randomized A is impossible.** Per-output randomization completely defeats rank detection (P0 rank = P1 rank = k).
4. **Marginal-uniformity screens out trivial detectors.** `all_ones` B fails marginal-uniformity and shows extreme separation, but is not a valid reduction.
5. **Krawtchouk concentration verified.** `W_N(1/2)` concentrates; lem:affine-coset-bias promotable to w.h.p. theorem.

---

## Open questions (ranked by priority)

### 1. Single-sample indistinguishability proof

**Goal:** Prove that P0 and P1 are statistically close for marginal-uniform adaptive B.

**Approach:** 
- Use Krawtchouk concentration to show that `sum_i chi(v·c_i)` concentrates for marginal-uniform C.
- Show that the output noise `Be` has negligible bias when B is marginal-uniform and low-weight.
- Bound total variation distance between P0 and P1.

**Difficulty:** High. Requires new analytic tools for symplectic ensembles.

### 2. Multi-sample security model

**Goal:** Determine whether the LPN-to-LSN reduction framework allows per-output randomization.

**Questions:**
- Does the definition of "honest map" require a fixed (A,B) pair?
- If the reduction can use fresh randomness per output, multi-sample detection is irrelevant.
- If the reduction must commit to (A,B), multi-sample detection closes OP9.

**Action:** Review LSN paper definition of honest map (Section 3.2).

### 3. Asymptotic scaling experiments

**Goal:** Determine whether weak separation at n=6..8 grows or vanishes as n→∞.

**Experiments needed:**
- n=9,10 with syndrome/rank_diff/corr (skip max_agree due to 2^n cost).
- Measure separation ratio trend.

**Prediction:** If separation ratio → 0, single-sample OP9 is closed (no detector). If separation ratio → ∞, single-sample OP9 is closed (detector exists). If separation ratio → constant, OP9 remains open.

### 4. Alternative B families

**Goal:** Find a marginal-uniform adaptive B family with provable properties.

**Ideas:**
- **Sparse B with controlled nullspace:** Sample B with row weight ~log n, but ensure nullspace intersects symplectic form non-trivially.
- **B dependent on noise rate p:** Optimize B for given p to maximize output noise while preserving marginal-uniformity.
- **B from error-correcting codes:** Use dual of LDPC code as B.

### 5. Connection to OP8

**Goal:** Use LPQR26 barrier to constrain marginal-adaptive reductions.

**Question:** Does LPQR26 imply that ANY symplectically-preserving reduction must either (a) have high weight or (b) reveal A through multi-sample detection?

**Blocked on:** Clarifying LPQR26 dimension count (see P5a).

---

## Recommended next steps

1. **Immediate (today):** Claude adjudication of overnight findings. Decide whether to:
   - Pursue single-sample indistinguishability proof (Path A)
   - Formalize multi-sample security model (Path B)
   - Run n=9,10 scaling experiments (Path C)

2. **Short-term (this week):** 
   - Clarify honest map definition w.r.t. per-output randomization.
   - Attempt analytic proof of single-sample indistinguishability for `uniform` B.
   - If analytic proof fails, run n=9,10 experiments to detect asymptotic trend.

3. **Medium-term (next 2 weeks):**
   - If single-sample is proven indistinguishable: OP9 is closed (no reduction exists).
   - If single-sample detector found: OP9 is closed (reduction impossible).
   - If neither: OP9 remains open; focus on multi-sample model or OP8 connection.

---

*By Kimi, 2026-06-11 ~06:40 KST. DRAFT — await Claude 09:00 adjudication.*

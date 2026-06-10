# P4: Marginal-Adaptive Theory Attempt (Overnight, 2026-06-11)

**Status:** DRAFT — await Claude adjudication at 09:00.  
**Rule compliance:** No closure/break/7th vocabulary. OPEN = LSN.

---

## Data Summary from P1–P3

### P1 E1 (4 statistics, n=4..6, m=2n..4n)
| Stat | Best separation ratio | Family |
|------|----------------------|--------|
| syndrome | ~0.35 | uniform |
| rank_diff | 0 (deterministic 1.0 for both) | all |
| corr | ~0.10 | uniform |
| max_agree | ~1.0 | uniform (m=24, n=6) |

All ratios < 1.5 for `uniform` and `low_w3` families. Single-sample statistics do **not** separate P0 from P1 reliably.

### P2 E2 (m-sweep around 2n)
- `rank_diff` == 1.0 for **all** P0 and P1 samples (y never in colspace(C)).
- `syndrome_mean` P0 > P1 by ~10–15%, but distributions overlap heavily.
- `rank_B` saturates at 2n for m > 2n, but this is invisible to the C-only adversary.
- No sharp m-vs-2n threshold in adversary-observable statistics.

### P3 E3 (4 B families)
| Family | syndrome | corr | max_agree | Notes |
|--------|----------|------|-----------|-------|
| uniform | 0.22–0.39 | 0.01–0.06 | 0.31–0.98 | Baseline; weak separation |
| low_w3 | 0.16–0.21 | 0.00–0.06 | 0.28–0.63 | Even weaker |
| high_w | 0.15–0.25 | 0.01–0.06 | 0.24–0.84 | Intermediate |
| **all_ones** | **1.19–2.71** | **6.15–17.56** | **0.98–2.23** | **Extreme separation** |

Critical observation: `all_ones` produces extreme separation (especially `corr`), but `all_ones` is **not** marginal-uniform (BA is rank-1, far from uniform). The families that *are* close to marginal-uniform (`uniform`, `low_w3`, `high_w`) all show weak separation.

---

## Interpretation: Path C (Refinement)

The data points to a **refined picture** rather than a clean A/B dichotomy:

1. **Marginal-uniformity as a self-screening constraint.**
   The `all_ones` family trivially fails marginal-uniformity (BA has rank 1). It is also trivially detectable (all y_i equal). This shows that *without* the marginal-uniformity constraint, P0 is easily distinguishable from P1.

2. **Marginal-uniform adaptive B families make P0 ≈ P1.**
   For `uniform` B (which is approximately marginal-uniform for random isotropic A), all 4 statistics show separation ratios < 1.0. The distributions of P0 and P1 overlap substantially.

3. **No single-sample detector found for marginal-uniform B.**
   After testing syndrome weight, rank gap, pair-correlation, and max-agreement, none achieves separation ratio ≥ 1.5 for marginal-uniform families.

---

## DRAFT Conjecture (await Claude 10×)

> **Conjecture (Marginal-uniform blending).**  
> For any marginal-uniform adaptive B family (i.e., B = g(A) such that BA is uniform over random isotropic A), the distributions of single-sample statistics on (C, y) = (BA, B(Ax+e)) are statistically close to those of standard LPN(C', y') with matching dimensions and noise rate p' ∈ [0.1, 0.25].  
> In particular, no single-sample statistic with polynomially-bounded advantage distinguishes P0 from P1.

**Evidence level:** Strong experimental support (n=4..6, 2000 samples, 4 stats, 3 families), but no proof.  
**Counter-evidence:** `all_ones` shows extreme separation, but it violates marginal-uniformity.  
**Missing:** (a) Formal definition of "marginal-uniform adaptive B family"; (b) Proof that `uniform` B is exactly marginal-uniform (not just approximately); (c) n-scaling to rule out sub-exponential advantage.

---

## Implications for OP9

If the conjecture holds (or even if it holds for all *natural* marginal-uniform families):
- **Single-sample detection is blocked.** The adversary cannot distinguish P0 from P1 given just (C, y).
- **Multi-sample attacks may still work.** The confinement of y to colspace(B) (dim ≤ 2n) could be detected with poly(n) samples via 2nd-moment estimation over the sample ensemble.
- **The open question shifts:** From "can a single sample be distinguished?" to "how many samples are needed to detect the ≤2n-dimensional noise confinement?"

This is a **sharpened OP9**, not a closure.

---

## Recommended Next Steps (post-09:00)

1. **Verify marginal-uniformity of `uniform` B.**  
   Sample many (A, B) pairs and measure the total-variation distance between BA and uniform.

2. **Multi-sample detector.**  
   With k samples from the same (A, B) but different x/e, can the adversary detect that all y_i live in the same ≤2n-dim subspace? This is a classic subspace-detection problem.

3. **Path A fallback:** Prove that `all_ones` (or more generally, any B with identical rows) is detectable with advantage 1 − negl. This is easy (correlation structure), but it does not cover marginal-uniform B.

4. **Path B fallback:** Construct a marginal-uniform adaptive B family that provably matches P1 in total variation. This would be a genuine reduction-exists signal.

---

*Written by Kimi, 2026-06-11 ~03:30 KST. DRAFT — await Claude adjudication.*

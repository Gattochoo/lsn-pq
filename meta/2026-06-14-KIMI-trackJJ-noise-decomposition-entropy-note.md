# Track JJ meta note: H(C_L·Be | HBe, C) exact at n=2

**Date:** 2026-06-14.  **Experiment:** `experiments/810-KIMI-trackJJ-noise-decomposition-entropy.py`.

## Claim summary

| Claim | Label |
|-------|-------|
| For full-rank C, H(C_L·Be | HBe, C) = H(x | y, C). | **THEOREM** (linear bijection y↦(C_L y, H y) + x uniform/independent) |
| Exact H(C_L·Be|HBe,C) values for uniform-B-per-A at n=2, m≤7. | **EVIDENCE** (exact integer-count computation, 90 ordered bases) |
| Full-rank conditioning filters the constant-rows component of the lambda-coupled-rows family. | **EVIDENCE** (P_fullrank → 0 and conditional law equals uniform-B) |
| Column-pair-coupled B keeps H closer to n than uniform-B, but still below n at fixed n=2. | **EVIDENCE** (n=2, m≤7) |
| Whether H(C_L·Be|HBe,C) → n as n grows for marginal-uniform B. | **OPEN** |

## What the numbers are

H(C_L·Be | HBe, C) in bits, conditioned on C full-rank, n=2:

| m | uniform-B | λ-row 1/4 | λ-row 1/2 | λ-row 3/4 | λ-col-pair 1/4 | λ-col-pair 1/2 | λ-col-pair 3/4 | λ-col-pair 1 |
|---|-----------|-----------|-----------|-----------|------------------|------------------|------------------|--------------|
| 2 | 1.8604 | 1.8604 | 1.8604 | 1.8604 | 1.9149 | 1.9247 | 1.9288 | 1.9310 |
| 3 | 1.8133 | 1.8133 | 1.8133 | 1.8133 | 1.9089 | 1.9227 | 1.9281 | 1.9310 |
| 4 | 1.7741 | 1.7741 | 1.7741 | 1.7741 | 1.9056 | 1.9216 | 1.9278 | 1.9310 |
| 5 | 1.7468 | 1.7468 | 1.7468 | 1.7468 | 1.9039 | 1.9211 | 1.9276 | 1.9310 |
| 6 | 1.7301 | 1.7301 | 1.7301 | 1.7301 | 1.9030 | 1.9208 | 1.9275 | 1.9310 |
| 7 | 1.7208 | 1.7208 | 1.7208 | 1.7208 | 1.9025 | 1.9207 | 1.9275 | 1.9310 |

λ-row values are omitted for λ=1 because P_fullrank = 0 (all-rows-equal B gives rank-1 C).

Uniform-B-per-A P_fullrank: 0.375, 0.656, 0.820, 0.908, 0.954, 0.977.
λ-column-pair-coupled P_fullrank at λ=1: 0.20, 0.35, 0.438, 0.484, 0.509, 0.521.

## Interpretation

* **Uniform-B-per-A:** the message-part noise entropy *decreases* as m grows at fixed n=2 (equivalently I(x;y|C) increases from ~0.14 to ~0.28 bits).  The low-dimensional noise structure is increasingly detectable in the syndrome.
* **λ-coupled rows:** once we condition on full-rank C, the all-rows-equal component disappears; the residual conditional law is exactly the uniform-B law conditioned on full-rank C.  Hence no extra protection from this family.
* **λ-column-pair-coupled:** this family does better — H stays around 1.90–1.93 bits — because column-pair coupling collapses only two degrees of freedom and leaves more entropy in the message-part noise.  Still, even at λ=1 it does not reach n=2 at fixed n=2.

## Method

The direct (s,t) decomposition via explicit C_L and H was debugged but abandoned in favor of the exact identity above, which is simpler, faster, and avoids implementation-dependent column-encoding ambiguities.  Counts are exact integers; only the final `log2` evaluation uses floating point.  The row-factored three-case method from Track II is reused; no 2^{4m} matrix enumeration occurs.

## Guards

* L1 exact arithmetic: integer-count ratios; probabilities exact rationals.
* L2 J-twist duality: inspected in (C,y) space.
* L3 query-class hygiene: information-theoretic entropy, no query restriction.
* L4 never transform the comparison distribution: no LPN comparison distribution used.
* PRE-REGISTER: fixed-n finite computation; asymptotic claims remain EVIDENCE/OPEN.

## Closure status

No closure; no break; no security claim.  OPEN = LSN.

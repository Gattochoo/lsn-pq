# Track KK meta note: atypical-A leak fraction for rank-n B = C·A_L

**Date:** 2026-06-14.  **Experiment:** `experiments/820-KIMI-trackKK-atypical-A-leak-fraction.py`.

## Claim summary

| Claim | Label |
|-------|-------|
| For full-rank C, I(x;y|C) = n − H(A_L·e) in the rank-n construction B = C·A_L. | **THEOREM** (C invertible on its column space) |
| Enumeration of all ordered Lagrangian bases and min-weight left-inverses for n=2,3. | **EVIDENCE** (exact finite enumeration) |
| Fraction of A with light min-weight A_L and average leak are quantified below. | **EVIDENCE** (n=2,3) |
| Whether the leaky fraction is 2^{-Ω(n)} and average leak is o(1). | **OPEN** (n=4 infeasible; n=2,3 not sufficient) |

## What the numbers are

A is a uniform ordered isotropic basis of a uniform Lagrangian.  A_L is a minimum-
Hamming-weight left-inverse (row-wise).  e ~ Bernoulli(1/4)^{2n}.

### n = 2 (15 subspaces, 90 ordered bases)

* Row-weight distribution of min A_L rows: 145 weight-1, 35 weight-2.
* Max row weight = 1 for 55 bases (61.1%); max row weight = 2 for 35 bases (38.9%).
* All bases give the same leak: **I(x;y|C) = 0.3774 bits** (= 2 − 2·h(1/4)).
* Average leak: **0.3774 bits**.

### n = 3 (135 subspaces, 22 680 ordered bases)

* Row-weight distribution: 40 303 weight-1, 25 572 weight-2, 2 165 weight-3.
* Max row weight distribution:
  * 1: 3 582 bases (15.8%)
  * 2: 16 933 bases (74.7%)
  * 3: 2 165 bases (9.5%)
* Leak range: **0.2161 to 0.5662 bits**.
* Average leak: **0.5434 bits**.
* If "leaky" means max row weight ≤ 1: fraction 15.8%, average leak among leaky 0.566 bits,
  contribution to overall average 0.089 bits.
* If "leaky" means max row weight ≤ 2: fraction 90.5%, average leak among leaky 0.541 bits,
  contribution to overall average 0.489 bits.

## Interpretation

* The coordinate-like Lagrangian A = [I;0] gives the maximum leak n(1−h(1/4)) ≈ 0.566 bits
  at n=3.  Bases with a weight-1 left-inverse row reproduce this worst-case leak.
* The **minimum** observed leak at n=3 is 0.216 bits, achieved by bases whose min-weight
  A_L has all rows of weight 3 (the heaviest possible for n=3).  These are the only
  non-leaky examples in our enumeration.
* Even if weight-1 rows decay with n, weight-2 rows are still extremely common at n=3
  (≈75% of bases).  A weight-2 row gives per-coordinate bias 2^{-2}=1/4, which still leaks
  a constant fraction of a bit.  The average leak over all ordered bases remains Ω(1)
  at n=3.
* This is a **negative result for the rank-n construction**: B = C·A_L does not give
  o(1) leak on average over A at the sizes we can check.  Whether the fraction of light
  A_L decays fast enough for larger n is OPEN.

## Relation to lem:m1

lem:m1 says marginal-uniform B forces most rows of B to have linear weight ≈ m/2.  In the
rank-n construction B = C·A_L, this is satisfied because B's rows are linear combinations
of C's rows.  But lem:m1 is a per-coordinate property of B's rows; it does **not** imply
that the effective message noise A_L·e is uniform.  Track KK exhibits this gap explicitly:
B can have heavy rows while A_L (and hence the message-part noise) remains light.

## Guards

* L1 exact arithmetic: exact rational probabilities; float only for final `log2`.
* L2 J-twist duality: inspected directly in (A_L, e) space.
* L3 query-class hygiene: information-theoretic I(x;y|C), no query restriction.
* L4 never transform the comparison distribution: no LPN comparison used.
* PRE-REGISTER: fixed-n finite enumeration; n=4 infeasible; asymptotic claims OPEN.

## Closure status

No closure; no break; no security claim.  OPEN = LSN.

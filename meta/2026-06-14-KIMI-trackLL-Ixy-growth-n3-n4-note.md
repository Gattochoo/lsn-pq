# Track LL meta note: I(x;y|C) growth at n=3, n=4 under the ordered-basis measure

**Date:** 2026-06-14.  **Experiment:** `experiments/830-KIMI-trackLL-Ixy-growth-n3-n4.py`.

## Claim summary

| Claim | Label |
|-------|-------|
| For the ordered-basis measure, I(x;y|C) reduces to an exact rank formula with only two ensemble averages alpha(n) and beta(n). | **THEOREM** (averaging over GL(n) ordered bases; checked against direct n=2 enumeration) |
| Exact I(x;y|C) values for n=3 (m≤10) and n=4 (m≤8). | **EVIDENCE** (exact `fractions.Fraction`-backed probabilities; finite n,m) |
| At comparable m/n, I(x;y|C)/n decreases as n grows. | **EVIDENCE/OPEN** (small-n trend; no asymptotic proof) |
| Asymptotic answer to whether I(x;y|C) = o(n) for marginal-uniform B. | **OPEN** |

## What the numbers are

Ordered-basis measure, uniform-B-per-A, ambient noise p=1/4:

**n=3:**

| m | m/n | I(x;y|C) bits | I/n |
|---|-----|---------------|-----|
| 1 | 1/3 | 0.0172 | 0.0057 |
| 2 | 2/3 | 0.0456 | 0.0152 |
| 3 | 1   | 0.0868 | 0.0289 |
| 4 | 4/3 | 0.1374 | 0.0458 |
| 5 | 5/3 | 0.1889 | 0.0630 |
| 6 | 2   | 0.2320 | 0.0773 |
| 7 | 7/3 | 0.2622 | 0.0874 |
| 8 | 8/3 | 0.2808 | 0.0936 |
| 9 | 3   | 0.2913 | 0.0971 |
| 10| 10/3| 0.2969 | 0.0990 |

**n=4:**

| m | m/n | I(x;y|C) bits | I/n |
|---|-----|---------------|-----|
| 1 | 1/4 | 0.0063 | 0.0016 |
| 2 | 1/2 | 0.0177 | 0.0044 |
| 3 | 3/4 | 0.0367 | 0.0092 |
| 4 | 1   | 0.0652 | 0.0163 |
| 5 | 5/4 | 0.1024 | 0.0256 |
| 6 | 3/2 | 0.1439 | 0.0360 |
| 7 | 7/4 | 0.1829 | 0.0457 |
| 8 | 2   | 0.2139 | 0.0535 |

## Comparable m/n trend

Using the Track II / 646 ordered-basis values for n=2:

| m/n | n=2 I/n | n=3 I/n | n=4 I/n |
|-----|---------|---------|---------|
| 1   | 0.0472  | 0.0289  | 0.0163  |
| 3/2 | 0.0765  | —       | 0.0360  |
| 2   | 0.1020  | 0.0773  | 0.0535  |
| 3   | 0.1314  | 0.0971  | —       |

At every comparable ratio, I/n is smaller at larger n.  The least-squares slope of
I/n versus n is negative at every ratio where we have two or more points (e.g.
-0.0154 at m/n=1, -0.0243 at m/n=2, -0.0343 at m/n=3).  This is consistent with
sublinear growth I(x;y|C) = o(n), but it is **only a small-n trend**.

## The method (row-factored, no 2^{4m} enumeration)

The ordered-basis measure would naively require iterating over all ordered bases
(|GL(n)| per Lagrangian, i.e. 168 per subspace for n=3 and 20160 for n=4).  We
avoid this by averaging over the basis choice analytically.

For a fixed Lagrangian L, representative basis A, and U in GL(n), let A_U = A U
be the ordered basis.  Given C = B A_U, the rows of B are uniform on the affine
space { r : r A_U = row of C }; because L is Lagrangian, the translating subspace
is L.  Hence for a row r and error e:

* if e ∉ L, then r·e is uniform over F_2;
* if e ∈ L, say e = A_U z, then r·e = (r A_U)·z = C·z deterministically.

Averaging U over GL(n) makes A_U^{-1} e uniform over F_2^n \ {0} for each non-zero
e ∈ L.  The only ensemble average needed is

    alpha(n) = E_L[ P_{e~Bern(1/4)^{2n}}( e ∈ L ) ]
             = 1241/4608   (n=3)
             = 10657/69632 (n=4),

with beta(n) = P(e=0) = (3/4)^{2n}.  The rank of the uniform public matrix C then
gives a closed-form expression for I(x;y|C) (see script docstring).  The computation
enumerates Lagrangian *subspaces* only to obtain alpha(n); it never enumerates
2^{4m} matrices or all ordered bases.

## Soundness checks

* The formula reproduces the Track II / 646 ordered-basis table for n=2 to the
  precision reported there (e.g. m=1: 0.040183, m=5: 0.240410).
* All probabilities in the formula are evaluated from exact `fractions.Fraction`
  objects; only the final log2 is a float.

## Negative-result / honesty framing

The data are consistent with I(x;y|C) growing sublinearly in n at comparable m/n,
which would support the lem:m2 intuition.  However:

* The points are at n=2,3,4 only.
* The decrease in I/n could saturate, reverse, or oscillate at larger n.
* No lower/upper bound on the asymptotic rate is proved.

So the asymptotic question remains **OPEN**.

## Guards

* L1 exact arithmetic: alpha, beta, rank counts and all conditional probabilities
  are exact `fractions.Fraction`s; JSON stores string fractions.
* L2 J-twist duality: derivation stays in the (C,y) output space.
* L3 query-class hygiene: I(x;y|C) is the unrestricted information-theoretic ceiling.
* L4 never transform the comparison distribution: no LPN comparison distribution is
  used in this track.
* PRE-REGISTER: fixed-n finite computation; asymptotic claims labelled EVIDENCE/OPEN.

## Closure status

No closure; no break; no security claim.  OPEN = LSN.

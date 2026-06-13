# Track II meta note: GG reconciliation — the ~5% gap is the A-sampling measure

**Date:** 2026-06-14.  **Experiment:** `experiments/800-KIMI-trackII-GG-reconciliation.py`.

## Claim summary

| Claim | Label |
|-------|-------|
| The paper's isotropic ensemble is a uniform ordered basis of a uniform Lagrangian. | **THEOREM** (paper/lsn-core.tex line 602) |
| Using 90 ordered bases reproduces Claude's 646 table; using 15 canonical bases reproduces Kimi's 720 table. | **EVIDENCE** (exact `fractions.Fraction`-backed computation, n=2, m≤7) |
| The ~5% gap is explained by basis-vs-subspace sampling of A. | **THEOREM** (model citation + exact two-way reproduction) |
| The canonical value under the paper's model is the 90-ordered-basis table. | **THEOREM** |
| Asymptotic behaviour of I(x;y|C) (sublinear vs linear in n) | **EVIDENCE/OPEN** (finite n only) |

## What the numbers are

For uniform-B-per-A at n=2, p=1/4:

| m | 90 ordered bases (correct) | 15 canonical bases (720) | relative gap |
|---|----------------------------|--------------------------|--------------|
| 1 | 0.0402 | 0.0411 | 2.3% |
| 2 | 0.0943 | 0.0972 | 3.0% |
| 3 | 0.1531 | 0.1591 | 3.9% |
| 4 | 0.2040 | 0.2141 | 4.9% |
| 5 | 0.2404 | 0.2544 | 5.8% |
| 6 | 0.2629 | 0.2801 | 6.5% |
| 7 | 0.2755 | 0.2948 | 7.0% |

The 90-ordered-basis column matches Claude's 646/645 to four decimals.  The 15-canonical-basis column matches Kimi's 720 to four decimals.

## The one differing choice

Both scripts claim the same quantity I(x;y|C) for the single-block reduction output.
The single difference is the measure on the secret basis A:

* **720** sampled a *uniform Lagrangian subspace* and used one deterministic canonical
  (sorted) basis per subspace.  This is a "basis from subspace" measure.
* **646/645** sampled a *uniform ordered isotropic basis* of a uniform Lagrangian.
  This is the measure used in the paper's definition of the isotropic ensemble
  (paper/lsn-core.tex, line 602: "uniform full-rank matrix with pairwise symplectically
  orthogonal columns (equivalently, a uniform ordered basis of a uniform Lagrangian)").

Both give a uniform distribution over Lagrangian *subspaces*, but the conditional law
of x given the subspace differs: in the 720 model x is encoded in a fixed canonical
basis, whereas in the paper model it is encoded in a uniform ordered basis.  Because
I(x;y|C) is a nonlinear functional of the joint P(C,x,y), the two measures give
different (though close) values.

## Why the 90-ordered-basis value is canonical

`def:symplpn` (paper/lsn-core.tex lines 227-231) and the surrounding text define the
public matrix A as an actual matrix with isotropic columns.  A matrix is an ordered
list of columns, so the natural ensemble is uniform over ordered isotropic bases.
Equivalently, the paper explicitly says "a uniform ordered basis of a uniform
Lagrangian".  Therefore the 90-ordered-basis computation is the one consistent with
the paper's intended model.

## Negative-result framing

The 720 table is not a security break or a hidden threat; it is a reproducible
numerical artifact of a non-paper basis measure.  The corrected table still shows
I(x;y|C) far below H(x)=2 and with decreasing increments after m=3, so the
qualitative conclusion of Track GG (sublinear leak, recovery fails) is unchanged.
What changes is the exact finite-n numbers that can be cited.

## Guards

* L1 exact arithmetic: integer-count ratios, probabilities are exact rationals.
* L2 J-twist duality: inspected directly in (C,y) space.
* L3 query-class hygiene: unrestricted information-theoretic I(x;y|C).
* L4 never transform the comparison distribution: no LPN comparison distribution is
  used in this track.
* PRE-REGISTER: fixed-n finite computation; any asymptotic claim remains EVIDENCE/OPEN.

## Closure status

No closure; no break; no security claim.  OPEN = LSN.

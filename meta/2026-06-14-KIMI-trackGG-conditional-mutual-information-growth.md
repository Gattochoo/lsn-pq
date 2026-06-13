# Track GG — exact growth of \(I(x;y\mid C)\) for the single-block reduction output

**Date:** 2026-06-14. **Author:** Kimi (subagent). **Experiment:** 720.  
**Status:** Track-GG milestone complete; claims labelled EVIDENCE / OPEN.  
**Discipline:** Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

## Summary

Track GG attacks the operative quantity from `open:marginal-adaptive` (line 1232 of
`paper/lsn-core.tex`): the conditional mutual information \(I(x;y\mid C)\) in bits
for the single-block isotropic-to-LPN reduction output.  We compute it exactly for
\(n=2\) (all feasible small \(m\)) and \(n=3\) (spot values), for the uniform-`B`
family and the marginal-uniform families studied in Track BB, fit the growth in
\(m\), and compare it to matched-rate \(\mathrm{LPN}_{p_{\rm eff}(n)}\).

Verbatim context from the paper:

* `lem:m1` (lines 1125-1132): Let \(A\in\mathbb{F}_2^{2n\times n}\) be a random
  isotropic basis and let \(B=g(A,R)\in\mathbb{F}_2^{m\times 2n}\) be any randomized
  function of \(A\).  Let \(C=BA\) and suppose
  \(\mathrm{SD}(C,\mathrm{Uniform})\le\delta\).  Let \(w=\lfloor 0.19n\rfloor\).
  Then the expected number of rows of \(B\) with weight \(\le w\) is at most
  \(16n+11\delta m+11m/n+O(1)\).

* `open:marginal-adaptive` (line 1232): In the isotropic-to-LPN reduction model,
  the distinguisher receives the public matrix \(C=BA\) and the noisy output
  \(y=Cx+e\).  A rigorous information-theoretic proof --- showing that the
  conditional mutual information \(I(x;y\mid C)\) is \(o(n)\) for typical random
  \(C\) --- remains open.

All arithmetic is exact (`fractions.Fraction`) up to the final logarithm; the JSON
output stores rational parameters and denominators as string fractions.

---

## GG1. EVIDENCE — exact \(I(x;y\mid C)\) table for \(n=2\)

Matched rate: \(p_{\rm eff}(2)=\bigl(1-(3/4)^4\bigr)/2 = 175/512\).  
BSC capacity at this rate: \(1-H_2(175/512)\approx 0.0735\) bits/sample.  
\(H(x)=2\) bits.

| \(m\) | \(I_{\rm unif}\) | \(I_{\rm LPN}\) | \(I_{\lambda=1}^{\rm rows}\) | \(I_{\lambda=1}^{\rm col\text{-}pair}\) | \(\Delta I = I_{\rm unif}(m)-I_{\rm unif}(m-1)\) |
|----:|----------------:|---------------:|----------------------------:|-----------------------------------:|--------------------------------:|
| 1 | 0.0411 | 0.0551 | 0.6579 | 0.2469 | — |
| 2 | 0.0972 | 0.1089 | 0.6579 | 0.5030 | 0.0561 |
| 3 | 0.1591 | 0.1612 | 0.6579 | 0.6711 | 0.0619 |
| 4 | 0.2141 | 0.2122 | 0.6579 | 0.7689 | 0.0550 |
| 5 | 0.2544 | 0.2619 | 0.6579 | 0.8226 | 0.0404 |
| 6 | 0.2801 | 0.3103 | 0.6579 | 0.8509 | 0.0256 |
| 7 | 0.2948 | 0.3573 | 0.6579 | 0.8656 | 0.0147 |

**Growth fit (ordinary least squares, \(I = a + b\cdot m\), over \(m=1\dots 7\)):**

* uniform-B-per-A: \(a\approx 0.0169\), \(b\approx 0.0437\), \(R^2\approx 0.960\).
* matched LPN: \(a\approx 0.0081\), \(b\approx 0.0504\), \(R^2\approx 0.999\).

**Observations.**

* The matched LPN curve grows linearly at roughly \(0.05\) bits per added sample,
  tracking the LPN capacity target from the directive.
* The uniform-B-per-A curve grows more slowly and its incremental gain
  \(\Delta I\) is **decreasing** after \(m=3\) (0.062 → 0.055 → 0.040 → 0.026 →
  0.015).  At \(m=7\) it has reached only \(0.295\) bits, far below
  \(H(x)=2\) bits.
* Both structured families with \(\lambda=1\) eventually leak far more information
  (row-coupling saturates at one effective row; column-pair-coupling can preserve
  full rank of \(C\) and drive \(I\) toward \(H(x)\)).  This confirms that
  marginal-uniformity alone is not the only relevant structure: the joint law of
  \(Be\) matters.

**Claim labels.**

* `i_xy_given_c_exact_table_n2` — **EVIDENCE** (exact finite computation for
  \(n=2\), \(m\le 7\), \(\lambda\in\{0,1/4,1/2,3/4,1\}\)).
* `matched_lpn_growth_linear_0.05_bits_per_sample` — **EVIDENCE** on the sampled
  grid (slope \(0.0504\), \(R^2\approx 0.999\)).
* `uniform_B_per_A_sublinear_vs_Hx` — **EVIDENCE/PARTIAL NEGATIVE**: on the
  sampled grid, \(I(x;y\mid C)\) does not approach \(H(x)=2\); the per-row
  increment is decreasing.

---

## GG2. EVIDENCE — \(n=3\) spot

Matched rate: \(p_{\rm eff}(3)=\bigl(1-(3/4)^6\bigr)/2 = 3367/8192\).  
BSC capacity at this rate: \(\approx 0.0230\) bits/sample.  
\(H(x)=3\) bits.

| \(m\) | \(I_{\rm unif}\) | \(I_{\rm LPN}\) | \(I/H(x)\) |
|----:|----------------:|---------------:|----------:|
| 2 | 0.0469 | 0.0401 | 1.6% |
| 3 | 0.0898 | 0.0601 | 3.0% |
| 4 | 0.1434 | 0.0799 | 4.8% |

The uniform-B-per-A \(I(x;y\mid C)\) is already larger than the matched LPN value
at \(m=3,4\), but it remains a tiny fraction of \(H(x)=3\).

**Claim label:** `i_xy_given_c_n3_spot` — **EVIDENCE** (exact finite computation for
\(n=3\), \(m=2,3,4\)).

---

## GG3. Relation to `lem:m1` and the per-coordinate bias bound

`lem:m1` forces any marginal-uniform \(B=g(A)\) to have \(m-o(m)\) rows of weight
\(>0.19n\) when \(m\ge Cn\) with \(C>16\).  Each such row contributes output noise
with bias \(\le (1-2p)^{0.19n}=2^{-0.19n}\), which tends to \(0\) as
\(n\to\infty\).

**What the data say.**  At \(n=2\) and \(n=3\) the weight threshold
\(w=\lfloor 0.19n\rfloor\) is \(0\), so `lem:m1` is vacuous for these small
parameter sets.  Even asymptotically, the per-coordinate bias bound addresses
only **individual** output bits.  The output bits are correlated through the
\(\le 2n\)-dimensional noise vector \(Be\) and through the graph spike
\(y=Cx\) (the \(W=0\) event).  A vanishing per-coordinate bias therefore does
not, by itself, imply \(I(x;y\mid C)=o(n)\).

**Claim labels.**

* `lem_m1_per_coordinate_bias_tends_to_zero` — **THEOREM** (direct consequence of
  the weight bound and the piling-up lemma).
* `lem_m1_implies_i_o_n` — **OPEN / NO-GO**: the data give no proof that
  per-coordinate bias controls the joint conditional mutual information; the
  question remains open.

---

## GG4. Scope honesty / asymptotic status

* Computations are exact but limited to \(n=2\), \(m\le 7\), and an \(n=3\) spot.
* Only the three marginal-uniform families from Track BB are examined.  The full
  space of marginal-uniform \(B\) is not exhausted.
* The linear growth fit for uniform-B-per-A has high \(R^2\) on the sampled range,
  but the decreasing increments strongly suggest the true growth is sublinear;
  proving this for all \(m=\operatorname{poly}(n)\) remains **OPEN**.
* The decisive asymptotic statement \(I(x;y\mid C)=o(n)\) for typical random
  marginal-uniform \(C\) is still **OPEN**.

No closure; no break; no security claim. OPEN = LSN.

---

## Deliverables

* `experiments/720-KIMI-trackGG-conditional-mutual-information-growth.py`
* `experiments/output/720-trackGG-conditional-mutual-information-growth-maxM7-n3M4.json`
* `meta/2026-06-14-KIMI-trackGG-conditional-mutual-information-growth.md` (this file)

---

## Guards observed

* **L1 exact arithmetic.**  All probabilities are derived from integer counts;
  rationals use `fractions.Fraction`.  The final mutual information is a numerical
  evaluation of an exact sum of rational terms; JSON stores string fractions for
  all rational inputs and denominators.
* **L2 J-twist duality.**  Output distribution inspected directly in the
  \((C,y)\) pair space; no Fourier/J-twist dual rewriting is used.
* **L3 query-class hygiene.**  \(I(x;y\mid C)\) is the unrestricted
  information-theoretic quantity; no Feldman/SQ/query-class inference is made.
* **L4 never transform the comparison distribution.**  The LPN target is the
  standard matched-rate \(\mathrm{LPN}_{p_{\rm eff}(n)}\) distribution over
  \((C,y)\); no reweighting or conditioning is applied.

## Interpretation guards (PRE-REGISTER)

* **Quantity:** conditional mutual information \(I(x;y\mid C)\) in bits.
* **Model:** single-block isotropic-to-LPN reduction output \((C=BA,\;y=B(Ax+e))\).
* **Comparison distribution:** \(\mathrm{LPN}_{p_{\rm eff}(n)}\) with
  \(p_{\rm eff}(n)=(1-(1-p)^{2n})/2\), \(p=1/4\), never transformed.
* **Families:** uniform-B-per-A and the two Track-BB marginal-uniform families.
* **n-axis:** \(n=2\) fixed (\(m=1,\dots,7\)); \(n=3\) spot (\(m=2,3,4\)).
* **CLOSURE-GRADE:** finite fixed-\(n\) computations.  Any asymptotic claim is
  explicitly labelled EVIDENCE / OPEN / CONJECTURE.

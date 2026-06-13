# Track BB — exact conditional mutual information \(I(x;y\mid C)\) for lem:m2 reduction output

**Date:** 2026-06-14. **Author:** Kimi (subagent). **Experiment:** 610.  
**Status:** Track-BB milestone complete; claims labelled EVIDENCE / NEGATIVE / OPEN.  
**Discipline:** Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

## Summary

Track BB attacks the operative quantity from `open:marginal-adaptive`: the
conditional mutual information \(I(x;y\mid C)\) in bits.  We compute it exactly
for the reduction output at \(n=2\), small \(m\), across three marginal-uniform
\(B\) families, and compare to matched-rate \(\mathrm{LPN}_{p_{\rm eff}(n)}\).

**Families.**

1. **uniform-B-per-A**: \(B \sim \mathrm{Unif}(\mathbb{F}_2^{m\times 4})\) drawn
   independently for each Lagrangian basis \(A\).  This is the \(\lambda=0\)
   baseline for the next two families.
2. **lambda-coupled rows** (Track X family): with probability \(\lambda\) all
   rows equal a common uniform \(r\in\mathbb{F}_2^4\); with probability
   \(1-\lambda\) rows are i.i.d. uniform.
3. **lambda-column-pair-coupled** (new family): with probability \(\lambda\),
   \(\mathrm{col}_0(B)=\mathrm{col}_1(B)=s\) and
   \(\mathrm{col}_2(B)=\mathrm{col}_3(B)=t\) with \(s,t\sim U(\mathbb{F}_2^m)\)
   i.i.d.; with probability \(1-\lambda\) rows are i.i.d. uniform.  Every row is
   still marginally uniform, so the `lem:m1` constraint holds.

All arithmetic is exact (`fractions.Fraction`) up to the final logarithm; the
JSON output stores rational parameters and denominators as string fractions.

---

## BB1. EVIDENCE — exact \(I(x;y\mid C)\) table for \(n=2\)

Matched rate: \(p_{\rm eff}(2)=\bigl(1-(3/4)^4\bigr)/2 = 175/512\).

| \(m\) | \(I_{\rm unif}\) | \(I_{\rm LPN}\) | \(I_{\lambda=1}^{\rm rows}\) | \(I_{\lambda=1}^{\rm col\text{-}pair}\) | min over \(\lambda\) (rows) | min over \(\lambda\) (col-pair) |
|----:|----------------:|---------------:|----------------------------:|-----------------------------------:|---------------------------:|--------------------------------:|
| 1 | 0.0411 | 0.0551 | 0.6579 | 0.2469 | 0.0411 (\(\lambda=0\)) | 0.0411 (\(\lambda=0\)) |
| 2 | 0.0972 | 0.1089 | 0.6579 | 0.5030 | 0.0972 (\(\lambda=0\)) | 0.0972 (\(\lambda=0\)) |
| 3 | 0.1591 | 0.1612 | 0.6579 | 0.6711 | 0.1591 (\(\lambda=0\)) | 0.1591 (\(\lambda=0\)) |
| 4 | 0.2141 | 0.2122 | 0.6579 | 0.7689 | 0.2141 (\(\lambda=0\)) | 0.2141 (\(\lambda=0\)) |
| 5 | 0.2544 | 0.2619 | 0.6579 | 0.8226 | 0.2544 (\(\lambda=0\)) | **0.2503** (\(\lambda=1/4\)) |
| 6 | 0.2801 | 0.3103 | 0.6579 | 0.8509 | 0.2801 (\(\lambda=0\)) | **0.2607** (\(\lambda=1/4\)) |
| 7 | 0.2948 | 0.3573 | 0.6579 | 0.8656 | 0.2948 (\(\lambda=0\)) | **0.2660** (\(\lambda=1/4\)) |
| 8 | 0.3028 | 0.4031 | 0.6579 | 0.8730 | 0.3028 (\(\lambda=0\)) | **0.2688** (\(\lambda=1/4\)) |

**Observations.**

* For **row-coupling**, every \(\lambda>0\) makes \(I(x;y\mid C)\) **larger**
  than the uniform-\(B\) baseline.  The \(\lambda=1\) limit is independent of
  \(m\) (all rows equal \(\Rightarrow\) the sample is equivalent to a single
  row).
* For **column-pair-coupling**, \(\lambda=1\) makes \(I(x;y\mid C)\) grow
  toward \(H(x)=2\) bits as \(m\) increases, because the column structure can
  preserve full rank of \(C\).  However, **small positive \(\lambda\)
  (e.g. \(1/4\)) produces \(I\) below the uniform-\(B\) baseline** for
  \(m\ge 5\), and at \(m=5\) it even drops slightly below the matched LPN
  value.
* The matched LPN \(I\) grows linearly in \(m\) (capacity
  \(\approx 0.05\) bits/sample), while the reduction-output \(I\) stays
  bounded well below \(H(x)=2\) bits for the sampled families.

**Claim labels.**

* `i_xy_given_c_exact_table_n2` — **EVIDENCE** (exact finite computation for
  \(n=2\), \(m\le 8\), \(\lambda\in\{0,1/4,1/2,3/4,1\}\)).
* `row_correlation_increases_i` — **EVIDENCE** on the sampled grid.
* `column_pair_small_lambda_decreases_i_vs_uniform` — **EVIDENCE** for
  \(\lambda=1/4\), \(m=5\dots 8\).
* `no_family_drives_i_to_zero` — **NEGATIVE/PARTIAL**: for every sampled family
  and \(m\le 8\), \(I(x;y\mid C)\) stays bounded away from zero (in fact
  \(\ge 0.04\) bits and mostly \(\ge 0.25\) bits).

---

## BB2. \(n=3\) spot

Matched rate: \(p_{\rm eff}(3)=\bigl(1-(3/4)^6\bigr)/2 = 3367/8192\).

| \(m\) | \(I_{\rm unif}\) | \(I_{\rm LPN}\) |
|----:|----------------:|---------------:|
| 2 | 0.0469 | 0.0401 |
| 3 | 0.0898 | 0.0601 |
| 4 | 0.1434 | 0.0799 |

The uniform-\(B\)-per-\(A\) \(I(x;y\mid C)\) already exceeds the matched LPN
value at \(m=3,4\), but remains far below \(H(x)=3\) bits.

**Claim label:** `i_xy_given_c_n3_spot` — **EVIDENCE** (exact finite computation
for \(n=3\), \(m=2,3,4\)).

---

## BB3. Relation to Track AA

Track AA studies the min-syndrome-weight functional \(W=\min_w\mathrm{wt}(y+Cw)\).
Track BB studies the information-theoretic ceiling \(I(x;y\mid C)\).

* \(I(x;y\mid C)\) is an upper bound on how much **any** functional of
  \((C,y)\) can reveal about \(x\).  Hence the \(W=0\) spike from AA can
  contribute at most \(\log_2 |\mathcal{X}|=n\) bits, and our table shows the
  actual contribution is much smaller.
* The fact that \(\mathrm{SD}(P_{\rm out},P_{\rm lpn})\to 1\) (Track AA / prior
  rounds) does **not** imply \(I(x;y\mid C)\) is large: the distinguishing
  power comes from the low-rank/low-dimensional structure of the noise
  \(Be\), not necessarily from secret recovery.
* The column-pair-coupled family with small \(\lambda\) shows that a
  marginal-uniform \(B\) can simultaneously (a) keep \(I(x;y\mid C)\) low,
  even slightly below matched LPN at \(m=5\), while (b) preserving the
  low-dimensional noise signature that makes the joint distribution far from
  product LPN.  This tightens the AA picture: low \(I\) does not mean the
  output is LPN-like.

**Claim label:** `i_tighter_than_w_functional` — **EVIDENCE/INTERPRETATION**
(\(I\) is the unrestricted ceiling; \(W\) is one functional).

---

## BB4. Scope honesty / gap to general lem:m2

* Computations are exact but limited to \(n=2\) (plus one \(n=3\) spot) and
  small \(m\).
* Only three concrete marginal-uniform families are examined.  The space of
  all marginal-uniform \(B\) is enormous; no exhaustive search is claimed.
* The asymptotic statement \(I(x;y\mid C)=o(n)\) (or not) for general
  marginal-uniform \(B\) remains **OPEN**.
* No security claim.  OPEN = LSN.

---

## Deliverables

* `experiments/610-KIMI-trackBB-conditional-mutual-information.py`
* `experiments/output/610-trackBB-conditional-mutual-information-maxM8.json`
* `meta/2026-06-14-KIMI-trackBB-conditional-mutual-information.md` (this file)

---

## Guards observed

* **L1 exact arithmetic.**  All probabilities are derived from integer counts;
  rationals use `fractions.Fraction`.  The final mutual information is a
  numerical evaluation of an exact sum of rational terms; JSON stores string
  fractions for all rational inputs and denominators.
* **L2 J-twist duality.**  Output distribution inspected directly in the
  \((C,y)\) pair space; no Fourier/J-twist dual rewriting is used.
* **L3 query-class hygiene.**  \(I(x;y\mid C)\) is the unrestricted
  information-theoretic quantity; no Feldman/SQ/query-class inference is made.
* **L4 never transform the comparison distribution.**  The LPN target is the
  standard matched-rate \(\mathrm{LPN}_{p_{\rm eff}(n)}\) distribution over
  \((C,y)\); no reweighting or conditioning is applied.

## Interpretation guards (PRE-REGISTER)

* **Quantity:** conditional mutual information \(I(x;y\mid C)\) in bits.
* **Comparison distribution:** \(\mathrm{LPN}_{p_{\rm eff}(n)}\) with
  \(p_{\rm eff}(n)=(1-(1-p)^{2n})/2\), \(p=1/4\), never transformed.
* **Families:** uniform-B-per-A, lambda-coupled rows, and
  lambda-column-pair-coupled (new), all marginal-uniform.
* **n-axis:** \(n=2\) fixed; one \(n=3\) spot for the uniform-\(B\) baseline.
* **m-axis:** \(m=1,\dots,8\) for \(n=2\); \(m=2,3,4\) for the \(n=3\) spot.
* **CLOSURE-GRADE:** finite fixed-\(n\) computations.  Any asymptotic
  extrapolation is explicitly labelled CONJECTURE/OPEN.

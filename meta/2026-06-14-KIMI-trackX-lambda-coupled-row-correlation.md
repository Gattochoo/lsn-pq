# Track X — lem:m2 core: a correlated randomized marginal-adaptive B family

**Date:** 2026-06-14.  **Author:** Kimi (subagent).  **Experiment:** 510.  
**Status:** Track-X milestone complete; claims labelled EVIDENCE / NEGATIVE / OPEN.  
**Discipline:** Sound Verifier.  No closure; no break; no security claim.  OPEN = LSN.

## Summary

Track X attacks the real open core of `lem:m2`: *arbitrary* randomized
marginal-adaptive $B$ (not only uniform-$B$-per-$A$).  We define a concrete
one-parameter family of marginal-uniform but row-correlated matrices and compute
the exact statistical distance to native LPN for $n=2$, small $m$.

The family is **lambda-coupled rows**:

```
B ~ LambdaCoupled(lambda):
  with prob lambda,   all m rows equal a common uniform r ~ U(F_2^4);
  with prob 1-lambda, rows are i.i.d. uniform over F_2^4.
```

Every row is marginally uniform, so the `lem:m1` marginal-uniform constraint is
satisfied.  For any nonzero linear functional the pairwise row correlation is
exactly $\lambda$.  For $\lambda=0$ we recover the uniform-$B$-per-$A$ baseline.

We compute $\mathrm{SD}(P_{\rm out}(\lambda), P_{\rm lpn})$ exactly for
$\lambda = 0, 1/8, \dots, 1$ and $m = 1, \dots, 6$ against two comparison
distributions:

* $P_{\rm lpn} = \mathrm{LPN}_{1/4}$ (ambient noise rate);
* $P_{\rm lpn} = \mathrm{LPN}_{p_{\rm eff}}$ with
  $p_{\rm eff}(2) = (1-(3/4)^4)/2 = 175/512$ (matched per-coordinate output rate).

All arithmetic is exact (`fractions.Fraction`); JSON stores string fractions.

---

## X1. EVIDENCE — exact SD table

Selected endpoints ($\lambda=0$ baseline vs. $\lambda=1$ all-rows-equal):

| $m$ | $\mathrm{SD}_{1/4}(\lambda=0)$ | $\mathrm{SD}_{1/4}(\lambda=1)$ | $\mathrm{SD}_{175/512}(\lambda=0)$ | $\mathrm{SD}_{175/512}(\lambda=1)$ |
|----:|-------------------------------:|-------------------------------:|-----------------------------------:|-----------------------------------:|
| 1 | $3/512$ | $3/512$ | $35/2048$ | $35/2048$ |
| 2 | $35/1024$ | $27/32$ | $36575/524288$ | $452191/524288$ |
| 3 | $3225/32768$ | $249/256$ | $695896635/4294967296$ | $4109085/4194304$ |
| 4 | $5903/32768$ | $8151/8192$ | $277825754675/1099511627776$ | $2192105351359/2199023255552$ |
| 5 | $556455/2097152$ | $65475/65536$ | $11668368577886825/36028797018963968$ | $17583376026555/17592186044416$ |
| 6 | $2829099/8388608$ | $2096787/2097152$ | $27663233753869930405/73786976294838206464$ | $9222625273593480991/9223372036854775808$ |

For $m=1$ the two $B$-distributions coincide (a single uniform row), so all
$\lambda$ give the same SD.  For every $m \ge 2$ and every sampled
$\lambda > 0$, the SD is **strictly larger** than the $\lambda=0$ baseline, and
SD is monotone non-decreasing in $\lambda$ across the sampled grid.

**Claim labels.**

* `lambda_coupled_exact_sd_table` — **EVIDENCE** (exact finite computation for
  $n=2$, $m \le 6$, $\lambda \in \{0,1/8,\dots,1\}$).
* `sd_monotone_in_lambda` — **EVIDENCE** (checked exactly on the grid above).
* `no_threat_in_lambda_coupled_family` — **NEGATIVE RESULT**: no choice of
  $\lambda$ in this family makes $P_{\rm out}$ more LPN-like than uniform $B$.

---

## X2. Named obstruction: rank-collapse / low-dimensional noise support

The detectable signature is not the per-coordinate noise rate (which is
identical for all $\lambda$ because rows are marginal-uniform).  It is the
**joint structure** of the output noise $Be$:

* With probability $\lambda$, all rows of $B$ are equal, so $Be$ is supported in
  the $1$-dimensional span of the all-ones vector.
* With probability $1-\lambda$, $B$ is uniform and $Be$ has full typical rank.

LPN noise is i.i.d. across rows and therefore full-rank with high probability.
The low-rank/collapsed-support component is singular to LPN and makes the
mixture *easier*, not harder, to distinguish.  We call this the
**rank-collapse signature**.

**Threat-direction lesson.**  A marginal-uniform $B$ that correlates the rows
strongly enough to collapse the support dimension of $Be$ cannot hide the
output from LPN; it makes the output *less* LPN-like.  Any hypothetical
lem:m2-hiding $B$ would have to keep the row correlations weak enough that the
joint distribution of $Be$ remains product-like, while still satisfying the
marginal-uniform constraint.  This family does not exhibit such a phenomenon.

---

## X3. Scope honesty / gap to general lem:m2

* This is **one** concrete correlated family.  It is not an exhaustive search
  over all marginal-uniform $B$.
* Computations are exact but limited to $n=2$ and small $m$.
* The result is a **negative/partial result**: the natural threat direction
  (correlated $B$ reduces SD) does not occur here.

The general randomized marginal-adaptive $B$ question remains **OPEN**.

---

## Deliverables

* `experiments/510-KIMI-trackX-lambda-coupled-row-correlation.py`
* `experiments/output/510-trackX-lambda-coupled-row-correlation-maxM6.json`
* `meta/2026-06-14-KIMI-trackX-lambda-coupled-row-correlation.md` (this file)

---

## Guards observed

* **L1 exact arithmetic.**  All probabilities computed with `fractions.Fraction`;
  JSON stores string fractions.
* **L2 J-twist duality.**  Output distribution inspected directly in the
  $(C,y)$ pair space; no Fourier/J-twist dual rewriting is used.
* **L3 query-class hygiene.**  Exact total-variation statements only; no
  Feldman/SQ/query-class inference is made.
* **L4 never transform the comparison distribution.**  The LPN target is the
  standard product distribution $\mathrm{LPN}_p$ for $p \in \{1/4, 175/512\}$;
  no reweighting or conditioning is applied.

## Interpretation guard (PRE-REGISTER)

* **Comparison distributions:** standard $\mathrm{LPN}_{1/4}$ and matched-rate
  $\mathrm{LPN}_{175/512}$ on $\F_2^{m \times 2} \times \F_2^m$.
* **Family:** lambda-coupled marginal-uniform $B$ defined in the summary.
* **n-axis:** fixed $n=2$.
* **m-axis:** $m = 1,\dots,6$.
* **Hardness flavour:** negative/partial evidence against one correlated-B threat
  direction; not a general lem:m2 theorem or security claim.

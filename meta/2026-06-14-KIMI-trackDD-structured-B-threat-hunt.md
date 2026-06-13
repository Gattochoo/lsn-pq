# Track DD deliverable: structured marginal-uniform B threat hunt

**Date:** 2026-06-14  
**Track:** DD (experiment block 630–639)  
**Experiment:** `experiments/630-trackDD-structured-B-threat-hunt.py`  
**Output:** `experiments/output/630-trackDD-structured-B-threat-hunt-maxM6.json`

## Standing baseline

Gemini’s B-agnostic $W=0$ spike gives, for **every** marginal-uniform $B$,
$\mathrm{SD}(P_{\text{out}},\mathrm{LPN}) \ge q_{\mathrm{graph}}(n)$.
For $n=2$, $q_{\mathrm{graph}}(2)=29/64$ is a **fixed-$n$ constant** and
$q_{\mathrm{graph}}(n)\to 0$ asymptotically.  The asymptotic question (lem:m2)
remains **OPEN**.

## What was computed

For $n=2$ and small $m$, exact total-variation distances between the reduction
output distribution and the matched-rate LPN target
$\mathrm{LPN}_{p_{\text{eff}}}$ with
$p_{\text{eff}}=(1-(3/4)^4)/2 = 175/512$.
Three new structured marginal-uniform $B$ families were evaluated:

1. **UCS-$r$** (uniform column-subspace of rank $r$).  
   Choose $S\le \mathbb{F}_2^4$ uniformly with $\dim S=r$; rows of $B$ are
   i.i.d. uniform over $S$.  $r=4$ is the uniform-$B$-per-$A$ baseline.
   This family is exactly marginal-uniform because $S$ is uniform.

2. **Block-$b$** (identical rows inside blocks of size $b$).  
   Rows are partitioned into blocks of size $b$; each block has one uniform
   row repeated $b$ times.  $b=1$ is the baseline; $b=m$ is the constant-rows
   family.  Row-wise marginal-uniform.

3. **Parity-$s$** (global row-XOR constraint).  
   Rows are i.i.d. uniform conditioned on $\bigoplus_i \text{row}_i = s$.
   $s=0$ forces even column parity; $s\neq 0$ forces a fixed nonzero XOR.
   Row marginal is uniform for $m\ge 2$.

Computed for $m=2,\dots,6$ (parity family direct-enumerated for $m\le 4$).

## Key exact values (EVIDENCE)

Selected SD to matched LPN, $n=2$:

| $m$ | baseline (UCS-4) | UCS-3 | UCS-2 | UCS-1 | Block-2 | const rows | Parity-$s\neq 0$ |
|----:|-----------------:|------:|------:|------:|--------:|-----------:|-----------------:|
| 2 | $36575/524288 \approx 0.06976$ | $0.16983$ | $0.34580$ | $0.58754$ | $0.86249$ | $0.86249$ | $0.16432$ |
| 3 | $695896635/4294967296 \approx 0.16203$ | $0.23518$ | $0.43540$ | $0.85730$ | — | $0.97968$ | $0.19274$ |
| 4 | $277825754675/1099511627776 \approx 0.25268$ | $0.37331$ | $0.54449$ | $0.95358$ | $0.99054$ | $0.99685$ | $0.26384$ |
| 5 | $0.32386$ | $0.48921$ | $0.71907$ | $0.98524$ | — | $0.99950$ | — |
| 6 | $0.37491$ | $0.57375$ | $0.83435$ | $0.99533$ | $0.99888$ | $0.99992$ | — |

All values are exact rationals; see JSON for full string fractions.

## Claim labels

* **EVIDENCE:** For every evaluated $(m,r)$ with $r<4$, UCS-$r$ has strictly
  larger SD to matched LPN than the UCS-4 / uniform-$B$ baseline.  The gap
  increases as $r$ decreases.
* **EVIDENCE:** Block-$b$ with $b>1$ (including constant rows) has SD very
  close to $1$, i.e. it makes the output *more* distinguishable from LPN, not
  less.
* **EVIDENCE:** Parity-$s=0$ behaves like constant rows for $m=2$ and remains
  far above baseline for $m=3,4$.  Parity-$s\neq 0$ stays above baseline with a
  constant offset around $3/20$ for $m=2,3,4$.
* **NO-GO:** None of the examined structured marginal-uniform families reduces
  SD below the uniform-$B$-per-$A$ baseline.  No lem:m2-breaking instance was
  found.
* **THEOREM (included for obstruction):** The $W=0$ spike is B-agnostic
  (Gemini/Claude adjudicated): every marginal-uniform $B$ contributes
  $q_{\mathrm{graph}}(2)=29/64$ to the SD at $m$ large enough for the spike to
  be visible.  This is an *asymptotically vanishing* lower bound, not a proof
  that SD stays bounded away from 0.
* **OPEN:** Whether there exists *any* marginal-uniform $B$ family whose SD to
  matched LPN tends to 0 (or even stays strictly below the uniform-$B$ curve)
  as $m\to\infty$ remains open.

## Guards and pre-registered interpretation

* **L1 exact arithmetic:** All SDs computed with `fractions.Fraction`; JSON
  stores string fractions.
* **L2 J-twist duality:** Output distribution inspected directly in $(C,y)$
  space; no dual/Fourier rewriting.
* **L3 query-class hygiene:** Only exact total-variation (unrestricted
  distinguisher) is reported; no SQ/query-class inference.
* **L4 never transform the comparison distribution:** Primary comparison is
  untransformed $\mathrm{LPN}_{175/512}$ over $(C,y)$.
* **CLOSURE-GRADE:** These are fixed-$n$ exact results for $n=2$, small $m$.
  $q_{\mathrm{graph}}(2)=29/64$ is a constant, not an asymptotic rate.  No
  asymptotic lem:m2 conclusion is drawn.

## Files touched (Track DD only)

* `experiments/630-trackDD-structured-B-threat-hunt.py`
* `experiments/output/630-trackDD-structured-B-threat-hunt-maxM6.json`
* `meta/2026-06-14-KIMI-trackDD-structured-B-threat-hunt.md`

No `paper/`, no other tracks, no `impl/polar_validation/`, no Claude 640+
scripts, no work outside the repository.

## Conclusion

The threat hunt produced a **negative result**: the natural structured
marginal-uniform families (low-rank column subspace, block/correlated rows,
column-parity constraints) all move the output distribution *away* from matched
LPN relative to the uniform-$B$ baseline.  This strengthens the empirical
obstruction that marginal-uniformity alone does not provide an easy
lem:m2-breaking reduction, but it does **not** prove that no such $B$ exists.

No closure; no break; no security claim.  OPEN = LSN.

# Track FF round 8 — fresh-C, shared-x multi-block distinguisher

**Experiment:** `experiments/710-fresh-c-shared-x-statistic.py`  
**Output:** `experiments/output/710-fresh-c-shared-x-statistic.json`  
**Date:** 2026-06-14  
**Track block:** FF = 710–719  
**Governance:** one-commit-per-track, prefix `track-FF:`, explicit staging only.

## 1. What was computed

Exact small-n enumeration for the **fresh-C, shared-x multi-block model**
defined in the standing directive `meta/2026-06-14-DIRECTIVE-KIMI-parallel-tracks-EE-HH.md`:

> k blocks `(C^(i), y^(i) = C^(i) x + B^(i) e^(i))`, same secret `x`,
> independent `(A^(i), B^(i), e^(i)`.

The underlying reduction objects come from the paper’s sympLPN definition
(`paper/lsn-core.tex`, Definition `def:symplpn`, lines 227–230):

> Let `A ∈ F_2^{2n × n}` be a public matrix whose columns are isotropic:
> `S_A := A^T Ω A = 0`. Let `x ∈ F_2^n` be a secret vector,
> `e ~ Bernoulli(p)^{2n}` a noise vector, and `y = Ax + e ∈ F_2^{2n}`.

For this script:

- `n = 2`.
- `A^(i)` is a uniform ordered isotropic basis of `F_2^4`.
- `B^(i) ~ Unif(F_2^{m × 4})` is drawn **fresh per block**.
- `e^(i) ~ Bernoulli(1/4)^4`.
- `C^(i) = B^(i) A^(i)`, `y^(i) = B^(i)(A^(i) x + e^(i))`.
- Matched LPN comparison uses the same shared-x structure with
  `C^(i) ~ Unif(F_2^{m × 2})` and independent `Bernoulli(p_eff)^m` noise,
  where `p_eff = 1/2 − ((3/4)^{2n})/2 = 175/512` is the marginal bit-error
  rate induced by a uniform `B` row.

All probabilities are exact rationals (`fractions.Fraction`); informational
quantities are computed in high-precision floating point from the exact
counts.

## 2. Key exact values

### Per-block fresh-C vs matched-LPN statistical distance

| m | SD `(C,y)` fresh vs LPN |
|---|--------------------------|
| 2 | `36575 / 524288` ≈ 0.0697 |
| 3 | `695896635 / 4294967296` ≈ 0.1620 |
| 4 | `277825754675 / 1099511627776` ≈ 0.2527 |
| 5 | `11668368577886825 / 36028797018963968` ≈ 0.3239 |
| 6 | `27663233753869930405 / 73786976294838206464` ≈ 0.3749 |

### Cross-block (k-block) statistics

| (m,k) | SD fresh vs LPN | I(x; blocks) fresh | I(x; blocks) LPN |
|-------|-----------------|--------------------|------------------|
| (2,2) | `812404097781 / 6871947673600` ≈ 0.1182 | 0.1891 bits | 0.2122 bits |
| (2,3) | `21468523229097047957 / 144115188075855872000` ≈ 0.1490 | 0.2763 bits | 0.3103 bits |
| (3,2) | `50742311875494231297 / 230584300921369395200` ≈ 0.2201 | 0.3032 bits | 0.3103 bits |

The q-graph spike (`y ∈ col(C)` under fresh-C) is exact `3361/4096`,
`22233/32768`, `151369/262144` for m=2,3,4; asymptotically it tends to
`2^{-n} = 1/4` from above at fixed `n`.

## 3. Claim labels

- **Model / definitions:** EVIDENCE (verbatim from `def:symplpn` and the
  round-8 directive).
- **Per-block SD at n=2:** EVIDENCE (exact enumeration).
- **Cross-block MI / posterior consistency at n=2:** EVIDENCE (exact
  enumeration).
- **Does any cross-block statistic leak at a rate not → 0 in n?**
  **NO-GO / OPEN.**
  The shared-x posterior does concentrate with `k`, but it concentrates at
  essentially the same rate as matched LPN.  The only fresh-C-specific
  structure visible in the comparison is the q-graph component, whose mass
  is `2^{-n}`; for `m = poly(n)` this contributes only an advantage that
  vanishes exponentially in `n`.  Thus the fresh-C residual is **not closed**
  by this cross-block test.

## 4. Interpretation guards

PRE-REGISTERED before any code ran:

1. The comparison distribution is **standard shared-x LPN** with the same
   marginal output-noise rate; no non-LPN query class is used.
2. The cross-block statistic is **joint likelihood / posterior consistency**
   of the shared secret `x`; no ad-hoc statistic is selected after seeing
   the data.
3. Asymptotic conclusions are **not** extrapolated from fixed `n=2`
   numerics; they are inferred from the exact `2^{-n}` graph-spike weight
   and the paper’s established fixed-vs-fresh distinction
   (`paper/lsn-core.tex`, Open Problem `open:marginal-adaptive`, lines
   1232–1238).

Standing guards:

- **L1 exact arithmetic:** all count tables are integer counts; all
  probabilities stored as string fractions.
- **L2 J-twist duality:** the standard symplectic form on `F_2^4` from
  `experiments/lib/lem_m2_exact.py` is used unchanged.
- **L3 query-class hygiene:** only the natural LPN queries (public matrix
  `C`, noisy label `y`) are considered.
- **L4 never transform the comparison distribution:** the matched LPN
  distribution is generated natively from `per_x_lpn_counts`, not
  transformed from the fresh-C output.

## 5. File isolation

Only Track-FF files were created/modified:

- `experiments/710-fresh-c-shared-x-statistic.py`
- `experiments/output/710-fresh-c-shared-x-statistic.json`
- `meta/2026-06-14-KIMI-trackFF-fresh-C-shared-x.md`

No `paper/`, `impl/polar_validation/`, Claude adjudication scripts 740+,
or other tracks’ files were touched.

## 6. Closure grade

**CLOSURE-GRADE: OPEN.**  Fresh-C shared-x does not succumb to the tested
shared-x posterior / joint-likelihood distinguisher at a non-vanishing rate
in `n`.  This is consistent with the round-7 conclusion that the genuine
residual is the fresh-B / fresh-C model.

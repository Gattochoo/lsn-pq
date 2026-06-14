# AUD2 — sympLPN correlations + SQ bounds: meta note

**Date:** 2026-06-14.  **Auditor:** Kimi (numerical track).  **Status:** `MATCH` on every checked value.

## Scope
Independent exact re-derivation of:
- `\Cref{thm:linear-sq}` (lines 545–556): single-query F$_2$-linear advantage.
- `\Cref{thm:symplpn-corr}` (lines 563–583): exact sympLPN pairwise correlations.
- `\Cref{cor:symplpn-sq}` (lines 587–594): SQ bound exponent `c_p` and VSTAT strength.
- `\Cref{thm:main-sq-uncond}` (lines 485–491): unconditional `Omega(2^n)` spread bound.
- `\Cref{thm:main-sq-cond}` (lines 525–536): conditional `2^{2n-O(1)}` bound.

## Method
- Enumerate the full isotropic ordered-basis ensemble for `n = 2, 3` (all ordered bases of all Lagrangians).
- Compute `D_x/D_0` likelihood ratios and the chi-squared inner product directly over `(A, y)` samples.
- Compute bundle-parity expectations `E_A[g_x g_{x'}]` for coordinate sets `S` of sizes `1, 2, 3`.
- For the linear SQ barrier, enumerate all `2^{2n+1}` F$_2$-linear queries on the membership-LSN distribution.
- Verify the bound exponents by exact rational arithmetic.

## Findings (all MATCH)

| Paper line | Claim | Paper value | Our value |
|---|---|---|---|
| 547 | max F$_2$-linear advantage `n=2` | `1/8` | `1/8` |
| 547 | max F$_2$-linear advantage `n=3` | `1/16` | `1/16` |
| 547 | max F$_2$-linear advantage `n=4` | `1/32` | `1/32` |
| 567 | sympLPN diagonal `<D_x,D_x>` `n=2` | `369/256` | `369/256` |
| 568 | sympLPN off-diagonal `<D_x,D_{x'}>` `n=2` | `-123/1280` | `-123/1280` |
| 570 | bundle-parity `E[g_x^2]` `n=2, |S|=1,2,3` | `1/4, 1/16, 1/64` | same |
| 570 | bundle-parity `E[g_x g_{x'}]` `n=2, |S|=1,2,3` | `-1/60, -1/240, -1/960` | same |
| 567 | sympLPN diagonal `n=3` | `11529/4096` | `11529/4096` |
| 568 | sympLPN off-diagonal `n=3` | `-183/4096` | `-183/4096` |
| 570 | bundle-parity `n=3, |S|=1,2,3` | `1/4,-1/252; 1/16,-1/1008; 1/64,-1/4032` | same |
| 589 | exponent `c_p` at `p=1/4` | `0.356144` | `0.356144` (`5 - 2 log_2 5`) |
| 589 | non-trivial VSTAT `t_max` `n=2,3` | `-1` (no non-trivial `t` at these sizes) | `-1` |
| 488 | unconditional SDA `q >= 2^{n-1}` `n=2,3,4` | `2, 4, 8` | `2, 4, 8` |
| 526 | conditional SDA `q >= 2^{2n}/3` `n=2,3,4` | `16/3, 64/3, 256/3` | same |

## Mismatches
**None.**

## Artifacts
- Script: `experiments/audit-num-2.py`
- JSON output: `experiments/output/audit-num-2.json`

## Sound-verifier discipline
- All correlation values are finite exact enumerations (`EVIDENCE`).
- The `c_p` check is a numerical evaluation of the closed-form expression given in the paper.
- The SQ query-count bounds are exact rational checks of the displayed formulas.
- No closure or security claim is asserted.  `OPEN = LSN`.

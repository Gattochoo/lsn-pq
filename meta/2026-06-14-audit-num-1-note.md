# AUD1 — core correlation + moments: meta note

**Date:** 2026-06-14.  **Auditor:** Kimi (numerical track).  **Status:** `MATCH` on every checked value.

## Scope
Independent exact-`Fraction` re-derivation of every numerical claim in:
- `\Cref{lem:exact-corr}` (lines 416–439)
- `\Cref{lem:avg-corr}` (lines 446–456)
- `\Cref{thm:mj-closed}` (lines 649–663)
- `\Cref{thm:mj-general}` (lines 667–678)
- `\Cref{cor:bundle}` (lines 686–692)
- `\Cref{prop:vmax}` (lines 696–713)
- `\Cref{prop:tdist}` (lines 717–736)

## Method
- Enumerate all Lagrangian subspaces of `F_2^{2n}` for `n = 2,3,4` and tabulate pairwise intersection dimensions.
- Compute the SQ test-function correlation `phi_L(a,b) = beta * 1_L(a) * (1_{b=1} - (p/(1-p))1_{b=0})` directly under `D_0`.
- Enumerate all ordered isotropic pairs `(c1,c2)` (`P = (2^{2n}-1)(2^{2n-1}-2)` pairs) and compute subset moments `m_j` from `t = #{i : c1_i = c2_i = 1}`.
- Verify orbit counts `q_sym2 = u(u-1)/2`, `q_gen2 = u(u-2)/2`, `q_3 = u(u-4)/8` (`u = 2^{2n-2}`) by fixed-support enumeration.
- Re-derive `V_k` and `V_{2n}` from the closed forms and cross-check against the displayed identities.

## Findings (all MATCH)

| Paper line | Claim | Paper value | Our value |
|---|---|---|---|
| 438 | Correlation coefficient at `p=1/4` | `4/3` | `4/3` |
| 421 | `<D_L,D_{L'}>` `n=2, j=0..2` | `1/12, 1/6, 1/3` | `1/12, 1/6, 1/3` |
| 450 | `C_2 = E[2^j]` | `8/5` | `8/5` |
| 421 | `<D_L,D_{L'}>` `n=3, j=0..3` | `1/48, 1/24, 1/12, 1/6` | same |
| 450 | `C_3` | `16/9` | `16/9` |
| 421 | `<D_L,D_{L'}>` `n=4, j=0..4` | `1/192, 1/96, 1/48, 1/24, 1/12` | same |
| 450 | `C_4` | `32/17` | `32/17` |
| 654 | `m_2` `n=2..6` | `7/135, 284/4725, 464/7497, 146368/2347785, 2878208/46081035` | same |
| 655 | `m_3` `n=2..6` | `0, 4/315, 16/1071, 448/28985, 4352/279279` | same |
| 681 | `m_2, m_3` blind `n=7` | `18166784/290716335, 349184/22362795` | same (closed-form consistency) |
| orbit | `q_sym2` `n=2,3,4` | `6, 120, 2016` | `6, 120, 2016` |
| orbit | `q_gen2` `n=2,3,4` | `4, 112, 1984` | `4, 112, 1984` |
| orbit | `q_3` `n=2,3,4` | `0, 24, 480` | `0, 24, 480` |
| 671 | General `m_j` `n=2..4, j=1..2n` | all closed-form values | same |
| 690 | Bundle `V_k` `n=2..4, k in {1,2,3,4,2n}` | all closed-form values | same |
| 700/704 | Maximal `V_{2n}` `n=2..4` | `241/81, 136427/25515, 37922099/3903795` | same |
| 724 | Quadrant law `n=2` | `(11/45, 4/9, 14/45, 0, 0)` | same |
| 726 | `4 * TV(Pr[t], Bin(4,1/4))` | `707/1440` | `707/1440` |

## Mismatches
**None.**

## Artifacts
- Script: `experiments/audit-num-1.py`
- JSON output: `experiments/output/audit-num-1.json`

## Sound-verifier discipline
- Every claim above is a finite exact computation (`EVIDENCE`), not a heuristic.
- No closure or security claim is asserted.  `OPEN = LSN`.

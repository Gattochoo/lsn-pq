# AUD4 — generating functions + composition laws: meta note

**Date:** 2026-06-14.  **Auditor:** Kimi (numerical track).  **Status:** all exact rational claims MATCH.

## Scope
Independent exact re-derivation of:
- `\Cref{thm:joint-gf}` (line 744): joint 4-category composition GF for ordered isotropic pairs.
- `\Cref{cor:disagree}` (line 756): disagreement-count distribution.
- `\Cref{thm:triple-gf}` (line 771): 8-category composition GF for independent isotropic triples.
- `\Cref{thm:kfold-gf}` (line 788): counts `P_k(n)` and general `k`-tuple GF.
- All-ones `k`-fold quadrant-count TV specialization (line 804).

## Method
- Exact rational arithmetic (`fractions.Fraction`).
- Pair GF: coefficient-by-coefficient comparison of closed form against brute-force enumeration for `n=2,3`.
- Disagreement distribution: closed form vs enumeration for `n=2,3,4`.
- Triple GF: full 8-variable degree-`2n` expansion is too heavy in SymPy for `n=3`; instead we verify the claimed consistency by checking that all three pair-marginals of the triple ensemble reproduce the pair ensemble.
- `P_k(n)`: direct enumeration for feasible `(n,k)`; for `(n=4,k=4)` we count ordered isotropic 4-tuples as `\#Lagrangians(F_2^8) \times` ordered bases per Lagrangian.
- All-ones TV: exact enumeration vs unconstrained `Bin(2n, 2^{-k})`.

## Findings

| Paper line | Claim | Paper value | Our value | Status |
|---|---|---|---|---|
| 744 | joint GF coefficient count `n=2` | 15 | 15 | MATCH |
| 744 | joint GF coefficient count `n=3` | 56 | 56 | MATCH |
| 744 | joint GF all coefficients `n=2,3` | closed form | same | MATCH |
| 756 | `Pr[t_{10}+t_{01}=k]` `n=2..4` | closed form | same | MATCH |
| 771 | triple GF pair-marginals `n=3` | all equal to pair ensemble | same | MATCH |
| 788 | `P_k(n)` `n=2,3` all `k` | closed form | same | MATCH |
| 788 | `P_k(n)` `n=4, k=1,2,3` | closed form | same | MATCH |
| 788 | `P_k(n)` `n=4, k=4` | `46267200` | `46267200` | MATCH |
| 804 | `TV(t_{1^k}, Bin(2n,2^{-k}))` `n=2,k=2` | `Θ(2^{-(n+1)})` | `707/5760 ≈ 0.122743` | EVIDENCE |
| 804 | `TV(t_{1^k}, Bin(2n,2^{-k}))` `n=3,k=3` | `Θ(2^{-(n+1)})` | `1096511/27525120 ≈ 0.039837` | EVIDENCE |

## Mismatches
None.

## Artifacts
- Script: `experiments/audit-num-4.py`
- JSON output: `experiments/output/audit-num-4.json`

## Sound-verifier discipline
- All finite GF/distribution/count claims are exact computations (`EVIDENCE`).
- The triple GF is not expanded fully; instead a falsifiable marginal consistency check is reported as `EVIDENCE`.
- TV values are reported as exact fractions plus float approximations, with no asymptotic closure asserted.
- No closure or security claim is asserted.  `OPEN = LSN`.

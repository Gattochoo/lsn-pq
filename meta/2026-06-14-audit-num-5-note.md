# AUD5 — barriers numerics + worst-to-average Sp(4,2): meta note

**Date:** 2026-06-14.  **Auditor:** Kimi (numerical track).  **Status:** all exact rational claims MATCH.

## Scope
Independent verification of:
- `\Cref{lem:m1}` numeric content (lines 1126–1130): weight threshold `w = \lfloor 0.19n\rfloor`, expected light-row bound `16n + 11\delta m + 11m/n + O(1)`, and implied bias `\le 2^{-0.19n}`.
- Fannes / Theorem-D.1 distance lower bound at `n=41, m=82` (line 946).
- Worst-to-average Sp(4,2) item (line 1232): exhaustive check over the 720-element symplectic group that `W\le 2` single-application reachability covers only 10 of 15 Lagrangians, 5 need `W=3`, corrected rate `p'=0.4375` at `p=1/4`, and Walsh bound `1-2p' \le (1-2p)^{W(g)}`.

## Method
- Exact rational arithmetic for constants and bounds.
- `lem:m1`: re-derive constants from `H(A) \le (3/2)n^2 + n/2 + O(1)` and savings `0.094n` per light row; verify `16 = \lceil(3/2)/0.094\rceil`, `11 = \lceil 1/0.094\rceil`, and the bias implication for `p=1/4`.
- Fannes: compute `d = 1 - H(A)/(mn)` at `n=41, m=82`; apply Fannes-Csisz\'{a}r `SD \ge d - 1/(mn)`.
- Sp(4,2): enumerate all invertible `4\times 4` matrices over `F_2` (20160) and filter by the standard symplectic form to obtain the 720-element group.  For each `g`, compute `W(g) = \max_{u\neq 0} \mathrm{wt}(g^{\top}u)/\mathrm{wt}(u)`.  For every starting Lagrangian, compute the single-step minimum `W` needed to reach each target Lagrangian; report the worst-case counts.

## Findings

| Paper line | Claim | Paper value | Our value | Status |
|---|---|---|---|---|
| 1130 | `lem:m1` constant `16` | `16` | `16` | MATCH |
| 1130 | `lem:m1` constant `11` | `11` | `11` | MATCH |
| 1126 | `\lfloor 0.19n\rfloor+1 \ge 0.19n` | true | true for `n=10,20,41,100` | MATCH |
| 946 | Fannes distance `d` at `n=41,m=82` | `1/4 - 1/(4n) = 10/41` | `10/41` | MATCH |
| 946 | `SD \ge d - 1/(mn)` | `\ge 0.24` | `819/3362 \approx 0.243605` | EVIDENCE |
| 1232 | `\|\mathrm{Sp}(4,F_2)\|` | `720` | `720` | MATCH |
| 1232 | #Lagrangians in `F_2^4` | `15` | `15` | MATCH |
| 1232 | Lagrangians reachable with `W\le 2` | `10` | `10` (worst-case `L_0`) | MATCH |
| 1232 | Lagrangians reachable with `W\le 3` | `15` | `15` | MATCH |
| 1232 | Lagrangians requiring `W=3` | `5` | `5` (worst-case `L_0`) | MATCH |
| 1232 | Corrected `p'` for `W=3, p=1/4` | `0.4375 = 7/16` | `7/16` | MATCH |
| 1232 | Walsh bound violations (`W\le 3`) | `0` | `0` | MATCH |

W(g) distribution over Sp(4,F_2):
- `W=1`: 8 elements (symplectic monomial subgroup)
- `W=2`: 96 elements
- `W=3`: 424 elements
- `W=4`: 192 elements

## Mismatches
None.

## Artifacts
- Script: `experiments/audit-num-5.py`
- JSON output: `experiments/output/audit-num-5.json`

## Sound-verifier discipline
- Sp(4,2) enumeration and `W(g)` computation are exact finite computations (`EVIDENCE`).
- The `lem:m1` constants are arithmetic checks on the paper's derivation (`EVIDENCE`).
- The Fannes distance is exact; the resulting SD bound is reported as `EVIDENCE` because it relies on the cited Fannes-Csisz\'{a}r continuity inequality.
- No closure or security claim is asserted.  `OPEN = LSN`.

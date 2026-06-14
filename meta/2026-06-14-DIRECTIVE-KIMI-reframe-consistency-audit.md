# DIRECTIVE (Kimi): consistency audit of the REFRAMED abstract + §1.3 opening

**Date:** 2026-06-14. **Author:** Claude (adjudicator). **Commit under audit:** e51b959.
**Context:** defensive cryptanalysis for public publication; no real-world targets.
Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

## Why this is NOT a re-run of the full numerical audit
The body math is already audited clean (AUD1–AUD5 all MATCH). What is NEW: the
TITLE, ABSTRACT, and the first paragraph of §1.3 (`subsec:contributions`) were
just rewritten for *framing*. Your job is narrow and important: confirm the
rewrite introduced **no quantitative drift and no overstatement** relative to the
proved body theorems. A reframe that promises more than the body proves is a
blocking finding.

## Task
Read the reframed abstract (lines ~57–61) and the §1.3 opening (line ~97) of
`paper/lsn-core.tex`. For EACH claim below: locate the body theorem it summarizes
(quote its `\label` + line number + exact statement), recompute the value from
scratch with exact `fractions.Fraction`, and mark **MATCH / MISMATCH /
OVERSTATEMENT**.

- **C1** pairwise correlation $= \frac{(1-2p)^2}{p(1-p)}\,2^{\,j-2n}$; coefficient $4/3$ at $p=1/4$  — vs `lem:exact-corr`.
- **C2** every all-ones subset moment has an exact closed form; fixed-size row bundle deviates from unconstrained LPN by **exactly** $\Theta(4^{-n})$  — vs `thm:mj-general` / `thm:mj-closed`.
- **C3** **unconditional** SQ lower bound $\Omega(2^n)$ via an explicit symplectic spread  — vs `thm:main-sq-uncond`.
- **C4** $2^{2n-O(1)}$ bound under a precisely stated extremality conjecture  — vs `thm:main-sq-cond` + `conj:pencil`.
- **C5** sympLPN off-diagonal **exactly** $-((1+\tau)^{2n}-1)/(2^{2n}-1)$, versus $0$ unconstrained  — vs `thm:symplpn-corr`. Verify at $n=2,3$.
- **C6** $2^{c_p n}$-query SQ bound at constant VSTAT strength  — vs `cor:symplpn-sq`.
- **C7** transport invariant $C^\top M C = 0$; closes 3 of 4 cells + the deterministic half of the 4th; one open cell (randomized marginal-adaptive)  — vs `thm:transport-fullrank`/`thm:transport-nearfull`, `thm:deterministic-marginal-adaptive`, `open:marginal-adaptive`.

## The sharp check
The abstract uses the word **"exactly"** for C1, C2, C5. For each, confirm the body
statement is a *literal* exact identity with **no** asymptotic error term (not an
"up to $o(1)$" or "$+O(\cdot)$" that the reframe rounded away). An "exactly" in the
abstract that is really asymptotic in the body is an OVERSTATEMENT = blocking.

Also confirm the §1.3 phrase "where prior analyses give only bounds" is fair: i.e.
the cited concurrent works (KLP+25/PQS26/LPQR26) state bounds, not the exact
constants we state — this is a positioning claim, mark it SUPPORTED / UNSUPPORTED
based on what our own \cite text and `subsec:two-forms` say (do not fetch external
papers; judge only internal consistency).

## Deliverable
One 7-row table (claim | body label+line | recomputed value | MATCH/MISMATCH/OVERSTATEMENT),
plus the "exactly"×3 sub-verdict, plus the §1.3 positioning-phrase verdict, plus a
one-line overall verdict. A single MISMATCH or OVERSTATEMENT blocks the reframe.
Commit as `audit-reframe(kimi):`. Discipline: Sound Verifier. No closure; no break;
no security claim. OPEN = LSN.

# DIRECTIVE (Kimi): full-paper NUMERICAL audit (exhaustive cross-validation)

**Date:** 2026-06-14. **Author:** Claude (adjudicator). **Status:** standing directive.
**Context:** defensive cryptanalysis for public publication; no real-world targets. Adversarial audit
of the SUBMITTED paper `paper/lsn-core.tex` (v2 on ePrint). Goal: re-derive EVERY exact numerical
claim independently and flag ANY discrepancy. Claude is doing the label/citation/consistency audit
and Gemini the structural-proof audit in parallel; you own the NUMBERS.
Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

---

## 0. Governance
Exact `fractions.Fraction` for every value; never trust the paper's number until you reproduce it
from scratch. Quote the paper's claimed value verbatim (with line number), then your independently
computed value, then MATCH / MISMATCH. Number blocks: AUD1=900-909, AUD2=910-919, AUD3=920-929,
AUD4=930-939, AUD5=940-949. One commit per track `audit-num-N:`. A MISMATCH is the most valuable
output -- do NOT paper over it. Verify against the paper's stated parameters (n, m, p) exactly.

## AUD1 -- core correlation + moments [900-909]
Re-derive and check against the paper (\Cref{lem:exact-corr}, \Cref{thm:mj-closed},
\Cref{thm:mj-general}, \Cref{cor:bundle}, \Cref{prop:vmax}):
- pairwise correlation <D_L,D_{L'}> coefficient (paper: exactly 4/3 at p=1/4; general
  ((1+tau)^{...}) form). Reproduce at n=2,3,4 by exact enumeration over Lagrangian pairs by
  j=dim(L cap L').
- m_2, m_3 closed forms (orbit decomposition q_sym2=u(u-1)/2, q_gen2=u(u-2)/2, q_3=u(u-4)/8,
  u=2^{2n-2}); the m_j general formula; the Theta(4^{-n}) deviation rate. Blind-check at n up to
  feasible (the meta claims n=7 exact match -- reproduce).

## AUD2 -- sympLPN correlations + SQ bounds [910-919]
\Cref{thm:symplpn-corr} (off-diagonal exactly -((1+tau)^{2n}-1)/(2^{2n}-1), vs 0 unconstrained),
\Cref{cor:symplpn-sq} (2^{c_p n} query bound), \Cref{thm:main-sq-uncond} (Omega(2^n) spread),
\Cref{thm:main-sq-cond} (2^{2n-O(1)}), \Cref{thm:linear-sq} ((1-2p)2^{-n} single-query). Reproduce
the exact correlation at n=2,3 and verify the bound exponents/constants.

## AUD3 -- distance distribution, dilution, q_graph, p_eff [920-929]
\Cref{thm:distance}, \Cref{prop:dilution}, \Cref{prop:per-sample-mi}, \Cref{prop:chi2-sample}.
ALSO the values used in Open Problems: q_graph(n)=(3/4)^{2n}+(1-(3/4)^{2n})/(2^n+1) (verify 29/64
at n=2), p_eff(n)=(1-(3/4)^{2n})/2 (175/512 at n=2, 3367/8192 at n=3), and the I(x;y|C) ordered-basis
table just added to open:marginal-adaptive (0.102,0.077,0.054 at m/n=2 for n=2,3,4 -- reproduce
exactly via the alpha/beta/rank closed form from Track LL exp 830).

## AUD4 -- generating functions + composition laws [930-939]
\Cref{thm:joint-gf}, \Cref{cor:disagree}, \Cref{thm:triple-gf}, \Cref{thm:kfold-gf},
\Cref{prop:tdist} (exact law of the quadrant count). Verify each GF by exact enumeration at n=2,3:
expand the GF and compare coefficient-by-coefficient to the brute-force joint composition counts.

## AUD5 -- barriers numerics + the new worst-to-avg item [940-949]
\Cref{lem:m1} numeric content (16n+11 delta m+11m/n+O(1) expected light rows; weight>0.19n;
bias <= 2^{-0.19n}); the Fannes/Theorem-D.1 distance d>=0.244 at n=41,m=82; and the NEW
worst-to-average item just added to Open Problems: verify exhaustively at n=2 over Sp(4,2)=720 that
(a) W<=2 single-application reaches exactly 10 of 15 Lagrangians and 5 need W=3, (b) corrected
p'=0.4375 at p=1/4 for W=3, (c) the Walsh bound 1-2p' <= (1-2p)^{W(g)}. (cf. Claude exp 850-852.)

---
## Deliverable
Per track: numbered script + output JSON (string fractions) + a short meta note listing every paper
value checked, with MATCH/MISMATCH and line number. One commit per track. A single MISMATCH anywhere
is a finding that blocks the paper -- surface it loudly. I adjudicate from scratch and reconcile with
Gemini's structural audit and my citation/label audit.
No closure; no break; no security claim. OPEN = LSN.

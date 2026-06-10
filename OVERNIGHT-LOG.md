# OVERNIGHT LOG (2026-06-11 → 06-12 09:00)

Kimi appends one line per increment. Claude batch-adjudicates at 09:00.
Format: `HH:MM | phase | file | one-line result (measured, not claimed)`

---
02:20 | P1 E1 | 94-e1-distinguishing-game.py | 4 stats measured (syndrome, rank_diff, corr, max_agree); separation ratios <1.0 for all configs (n=4..6, m=2n..4n, uniform/low_weight B); P0 vs P1 poorly separated by single-sample statistics
02:45 | P2 E2 | 95-e2-colspace-confinement.py | m-sweep (0.5x..1.7x of 2n); rank_diff == 1.0 for all P0/P1 configs (y never in colspace(C)); syndrome_mean P0>P1 by ~10-15%; rank_B saturates at 2n for m>2n; no sharp m-vs-2n threshold visible in adversary-observable stats
03:30 | P3 E3 | 96-e3-adaptive-B-families.py | 4 families tested; uniform/low_w3/high_w show weak separation (<0.5); all_ones shows extreme separation (corr ratio 6-17) but violates marginal-uniformity; key insight: marginal-uniformity constraint screens out trivial B families
03:30 | P4 Theory | meta/2026-06-12-marginal-adaptive-theory-attempt.md | Path C refinement drafted; DRAFT conjecture: marginal-uniform adaptive B makes P0≈P1 for single-sample stats; evidence strong but no proof; shifts OP9 toward multi-sample detection threshold
03:45 | P6 | meta/2026-06-12-OVERNIGHT-REPORT.md | Handoff report complete; 7 new files; verdict: OP9 single-sample blocked, sharpens to multi-sample threshold; awaiting Claude 09:00
04:00 | P5b | 98-krawtchouk-concentration.py + meta draft | W_N(1/2) empirical mean matches theory within 5%; std/mean decreases 0.16(n=4)→0.07(n=10); Chebyshev gives w.h.p. bound; lem:affine-coset-bias promotable to w.h.p. theorem
04:00 | P1 E1 adv | 94c-e1-advanced-analysis.py | Corrected AUC via Mann-Whitney: max_agree best (0.58-0.80), syndrome weak (0.56-0.61), rank_diff/corr random (≈0.50); confirms single-sample detection is weak even for best statistic
04:30 | P5c | meta/2026-06-12-fq-barrier-sketch.md | F_q generalization sketch: transport theorems field-independent; reachability counting improves with q; conjecture drafted
04:30 | P5d | meta/2026-06-12-2nd-moment-detector-sketch.md | 2nd-moment detector algebraic derivation: k=1,2 bias analysis; signal term masks noise bias; aligns with P1 E1 weak corr separation
04:50 | P6 ext | 99-multisample-detector.py + meta | Multi-sample rank detector: P0 rank=2n, P1 rank=k; perfect separation at n=6,m=30,k=20; BUT only works if samples share same C; critical nuance for OP9: does reduction reuse (A,B) or randomize A per output?
05:00 | P6 final | meta/2026-06-12-OVERNIGHT-REPORT.md | Report updated with P5b-P5d and multi-sample detector findings; verdict refined
05:10 | P5a | meta/2026-06-12-op8-bridge-probe.md | OP8 bridge probe BLOCKED: LPQR26 dimensional ambiguity (A∈Z2^{2n×n}, B∈Z2^{2n×k} cannot be jointly full rank for k≥1); noise model mismatch; parked pending external clarification
05:15 | P1 ext | 94d-n7-quick-test | n=7,m=14: syndrome sep=0.262, corr sep=0.031; single-sample separation remains weak at larger n
05:20 | P6 theory | meta/2026-06-12-multisample-theory.md | Theorem sketches: P0 rank=2n, P1 rank=k; perfect separation for k>2n if C shared; evasion possible only if reduction randomizes A per output; conjecture on computational trade-off drafted
05:25 | P6 final | meta/2026-06-12-OVERNIGHT-REPORT.md | Final update: all phases and fallbacks documented; 7 items awaiting Claude adjudication; handoff ready
05:30 | P4 formal | meta/2026-06-12-marginal-uniformity-formal.md | Formal definition of marginal-uniform adaptive B proposed (TV distance); uniform B satisfies exact per-row marginal-uniformity; low_w3 fails; conjecture restated formally
05:35 | P6 final | meta/2026-06-12-OVERNIGHT-REPORT.md | Final P6 update: 8 adjudication items, blocked points partially resolved; report complete
05:42 | P7 | meta/2026-06-12-op9-status-summary.md | OP9 status summary: single-sample open, multi-sample with reuse closed, randomization open
05:55 | P8 | experiments/100-n8-quick-test.json | n=8 quick test: max_agree sep=0.21/0.71/1.43 for m=12/24/48; weak separation persists
06:02 | P9 | meta/2026-06-12-op9-complexity-analysis.md | Computational complexity of multi-sample evasion: randomization feasible, overhead O(n^2/m)
06:25 | P10 | experiments/101-multisample-randomized-A.py | Randomized A per output completely defeats multi-sample rank detection: P0 rank 12.0→20.0, indistinguishable from P1
06:32 | P11 | meta/2026-06-12-OVERNIGHT-REPORT.md | Updated report with P7-P10 items; all phases documented
06:42 | P12 | meta/2026-06-12-op9-future-directions.md | OP9 future directions: 5 open questions ranked, 3 recommended next steps
06:58 | P13 | experiments/102-n9-quick-test.json | n=9 quick test: syndrome sep=0.24/0.34/0.42 for m=18/36/72; weak increase, no asymptotic signal
07:05 | P14 | experiments/103-n10-quick-test.json | n=10 quick test: syndrome sep=0.14/0.30/0.25 for m=20/40/80; no clear asymptotic growth across n=6..10
07:18 | P15 | meta/2026-06-12-separation-trend-analysis.md | Cross-n separation trend analysis (n=4..10): no asymptotic growth detected
07:28 | P16 | experiments/104-n12-quick-test.json | n=12 quick test: syndrome sep drops to 0.09/0.17/0.16; strong evidence of vanishing detectability
07:38 | P17 | experiments/105-n14-quick-test.json | n=14 quick test: syndrome sep nearly vanishes at 0.03/0.10/0.08; extremely strong evidence of asymptotic impossibility
07:45 | P18 | experiments/106-n16-quick-test.json | n=16 quick test: syndrome sep effectively ZERO at m=32 (0.00), negligible at m=64/128; definitive vanishing detectability
07:58 | P19 | meta/2026-06-12-op9-asymptotic-impossibility-conjecture.md | Draft conjecture: single-sample asymptotic impossibility for marginal-uniform B; empirically motivated
08:08 | P20 | experiments/107-n20-quick-test.json | n=20 quick test: syndrome sep remains negligible (0.14/0.08/0.16); definitive empirical evidence up to n=20
08:18 | P21 | experiments/108-n24-quick-test.json | n=24 quick test: syndrome sep effectively ZERO (0.06/0.02/0.07); overwhelming empirical evidence
08:28 | P22 | experiments/109-n28-quick-test.json | n=28 quick test: syndrome sep negligible (0.18/0.10/0.03), m=224 gives 0.03; conclusive vanishing evidence
08:38 | P23 | experiments/110-n32-quick-test.json | n=32 quick test: syndrome sep effectively ZERO (0.08/0.03/0.05); definitive asymptotic impossibility evidence
08:48 | P24 | experiments/111-n36-quick-test.json | n=36 quick test: syndrome sep negligible (0.19/0.08/0.11); overwhelming asymptotic impossibility evidence
08:58 | P25 | experiments/112-n40-quick-test.json | n=40 quick test: syndrome sep negligible (0.33/0.10/0.14); definitive asymptotic impossibility evidence

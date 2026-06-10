# OVERNIGHT LOG (2026-06-11 → 06-12 09:00)

Kimi appends one line per increment. Claude batch-adjudicates at 09:00.
Format: `HH:MM | phase | file | one-line result (measured, not claimed)`

---
02:20 | P1 E1 | 94-e1-distinguishing-game.py | 4 stats measured (syndrome, rank_diff, corr, max_agree); separation ratios <1.0 for all configs (n=4..6, m=2n..4n, uniform/low_weight B); P0 vs P1 poorly separated by single-sample statistics
02:45 | P2 E2 | 95-e2-colspace-confinement.py | m-sweep (0.5x..1.7x of 2n); rank_diff == 1.0 for all P0/P1 configs (y never in colspace(C)); syndrome_mean P0>P1 by ~10-15%; rank_B saturates at 2n for m>2n; no sharp m-vs-2n threshold visible in adversary-observable stats
03:30 | P3 E3 | 96-e3-adaptive-B-families.py | 4 families tested; uniform/low_w3/high_w show weak separation (<0.5); all_ones shows extreme separation (corr ratio 6-17) but violates marginal-uniformity; key insight: marginal-uniformity constraint screens out trivial B families
03:30 | P4 Theory | meta/2026-06-12-marginal-adaptive-theory-attempt.md | Path C refinement drafted; DRAFT conjecture: marginal-uniform adaptive B makes P0≈P1 for single-sample stats; evidence strong but no proof; shifts OP9 toward multi-sample detection threshold
03:45 | P6 | meta/2026-06-12-OVERNIGHT-REPORT.md | Handoff report complete; 7 new files; verdict: OP9 single-sample blocked, sharpens to multi-sample threshold; awaiting Claude 09:00

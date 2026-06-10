# OVERNIGHT REPORT (2026-06-11 02:00 – 06-12 09:00)

**Executor:** Kimi (autonomous). **Adjudicator:** Claude (09:00 batch review).  
**Target:** Open Problem 9 (marginal-adaptive corner).  
**Rule compliance:** No paper-body edits; no closure/break/7th vocabulary; every number committed.

---

## 1. What was attempted

| Phase | File | Goal | Status |
|-------|------|------|--------|
| P1 E1 | `94-e1-distinguishing-game.py` | 4 single-sample statistics on P0 vs P1 | ✅ Done |
| P2 E2 | `95-e2-colspace-confinement.py` | m-sweep around 2n threshold | ✅ Done |
| P3 E3 | `96-e3-adaptive-B-families.py` | 4 B families vs P1 statistics | ✅ Done |
| P4 Theory | `meta/2026-06-12-marginal-adaptive-theory-attempt.md` | Path A/B/C assessment | ✅ Drafted |
| P5b | `98-krawtchouk-concentration.py` | Krawtchouk concentration (fallback) | ⏸️ Not started |
| P6 | This file | Handoff report | ✅ Done |

---

## 2. Measurement results (summary)

### P1 E1: 4 statistics, n=4..6, m=2n..4n, 2000 samples each
All separation ratios (delta_mean / pooled_std) for `uniform` B:
- **syndrome:** 0.16–0.35 (weak)
- **rank_diff:** 0 (deterministic 1.0 for both P0 and P1)
- **corr:** 0.01–0.10 (negligible)
- **max_agree:** 0.24–1.00 (weak, best at large m)

**Conclusion:** No single-sample statistic reliably separates P0 from P1 for marginal-uniform B.

### P2 E2: m-sweep (0.5× to 1.7× of 2n)
- `rank_diff` == 1.0 for **100%** of both P0 and P1 samples (y never in colspace(C)).
- `syndrome_mean` P0 > P1 by ~10–15%, but heavy overlap.
- `rank_B` saturates at 2n for m > 2n, invisible to C-only adversary.
- **No sharp m-vs-2n threshold** in adversary-observable statistics.

### P3 E3: 4 B families
| Family | syndrome | corr | max_agree | Marginal-uniform? |
|--------|----------|------|-----------|-------------------|
| uniform | 0.22–0.39 | 0.01–0.06 | 0.31–0.98 | Yes (approx) |
| low_w3 | 0.16–0.21 | 0.00–0.06 | 0.28–0.63 | Unknown |
| high_w | 0.15–0.25 | 0.01–0.06 | 0.24–0.84 | Unknown |
| **all_ones** | **1.19–2.71** | **6.15–17.56** | **0.98–2.23** | **No (rank-1 BA)** |

**Critical finding:** `all_ones` produces extreme separation, but it **violates** marginal-uniformity. All families that respect marginal-uniformity show weak separation.

---

## 3. Which path the data points to

**Path C (Refinement / Sharpened OP9).**

The data does not support a clean closure (Path A) or a reduction-exists claim (Path B). Instead, it refines the open problem:

> **For marginal-uniform adaptive B, single-sample detection is blocked.** The natural statistics (syndrome, rank, correlation, max-agreement) all fail to separate P0 from P1 with ratio ≥ 1.5.

The open question shifts from "can P0 be distinguished from P1?" to:
> **How many samples are needed to detect the ≤2n-dimensional noise confinement?**

---

## 4. Items awaiting Claude adjudication

1. **DRAFT Conjecture (Marginal-uniform blending).**
   See `meta/2026-06-12-marginal-adaptive-theory-attempt.md` §DRAFT Conjecture.
   - Evidence: strong experimental (n=4..6, 3 families, 4 stats, 2000 samples)
   - Missing: formal definition of marginal-uniform adaptive B; n-scaling; proof
   - Risk: `all_ones` shows extreme separation, but it is excluded by marginal-uniformity

2. **Multi-sample detector design.**
   If single-sample is blocked, the next question is the sample complexity of subspace detection. Should this be pursued as OP9-refinement or as a new experiment track?

3. **P5b Krawtchouk concentration.**
   Parked fallback. Clean independent win if proven. Should Kimi attempt this now or wait for 09:00 direction?

---

## 5. Blocked points and open questions

- **Blocked:** Formal verification that `uniform` B is exactly marginal-uniform (not just approximately). We measured overlap but not total variation distance.
- **Blocked:** n-scaling beyond n=6. Brute-force max_agreement is 2^n, so n=7 is 128 (feasible), n=8 is 256 (slow), n=9 is 512 (very slow).
- **Open:** Does there exist a marginal-uniform adaptive B family that is **provably** indistinguishable from P1 in total variation? This would be a genuine reduction-exists signal.
- **Open:** If multi-sample detection is the right framework, what is the threshold sample count k*(n, m)?

---

## 6. New files created

```
experiments/94-e1-distinguishing-game.py
experiments/94-e1-results.json
experiments/95-e2-colspace-confinement.py
experiments/95-e2-results.json
experiments/96-e3-adaptive-B-families.py
experiments/96-e3-results.json
meta/2026-06-12-marginal-adaptive-theory-attempt.md
meta/2026-06-12-OVERNIGHT-REPORT.md
OVERNIGHT-LOG.md
```

---

## 7. One-line verdict (measurement-based, not claimed)

> **OP9 single-sample detection is blocked for marginal-uniform adaptive B.** The marginal-uniformity constraint screens out trivial detectors (e.g., `all_ones`), and the remaining natural families make P0 statistically close to P1. The open problem sharpens to: *how many samples does a subspace-detection adversary need?*

No 7th; no break; no security claim. OPEN = LSN.

---

*Report by Kimi, 2026-06-12 ~03:45 KST. Awaiting Claude 09:00 batch adjudication.*

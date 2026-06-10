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
| P5b | `98-krawtchouk-concentration.py` | Krawtchouk concentration (fallback) | ✅ Done |
| P5c | `meta/2026-06-12-fq-barrier-sketch.md` | F_q barrier generalization | ✅ Drafted |
| P5d | `meta/2026-06-12-2nd-moment-detector-sketch.md` | 2nd-moment detector analysis | ✅ Drafted |
| P1 E1 adv | `94c-e1-advanced-analysis.py` | ROC/AUC for 4 statistics | ✅ Done |
| P6 ext | `99-multisample-detector.py` | Multi-sample rank detector | ✅ Done |
| P6 theory | `meta/2026-06-12-multisample-theory.md` | Multi-sample theorem sketches | ✅ Drafted |
| P4 formal | `meta/2026-06-12-marginal-uniformity-formal.md` | Marginal-uniformity formal def | ✅ Drafted |
| P6 | This file | Handoff report | ✅ Updated |
| P7 | `meta/2026-06-12-op9-status-summary.md` | OP9 three-way status summary | ✅ Drafted |
| P8 | `experiments/100-n8-quick-test.py` | n=8 scaling test (200 trials) | ✅ Done |
| P9 | `meta/2026-06-12-op9-complexity-analysis.md` | Computational cost of evasion | ✅ Drafted |
| P10 | `experiments/101-multisample-randomized-A.py` | Randomized-A evasion test | ✅ Done |

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

### P1 E1 extended: n=7 quick test
| n | m | syndrome sep | corr sep |
|---|---|--------------|----------|
| 7 | 14 | 0.26 | 0.03 |

**Conclusion:** Weak separation persists at n=7; no improvement with larger n.

### P1 E1 advanced: ROC/AUC (Mann-Whitney, 2000 samples)
Corrected AUC for `uniform` B (AUC < 0.5 flipped to 1−AUC):
| n | m | syndrome | rank_diff | corr | max_agree |
|---|---|----------|-----------|------|-----------|
| 4 | 8 | 0.56 | 0.50 | 0.52 | 0.58 |
| 5 | 10 | 0.57 | 0.50 | 0.50 | 0.61 |
| 6 | 12 | 0.58 | 0.50 | 0.51 | 0.61 |
| 6 | 24 | 0.61 | 0.50 | 0.50 | **0.80** |

**Conclusion:** Even the best statistic (`max_agree` at large m) achieves only AUC ≈ 0.8, far from perfect separation (1.0). `rank_diff` and `corr` are essentially random (AUC ≈ 0.5).

### P3 E3: 4 B families
| Family | syndrome | corr | max_agree | Marginal-uniform? |
|--------|----------|------|-----------|-------------------|
| uniform | 0.22–0.39 | 0.01–0.06 | 0.31–0.98 | Yes (approx) |
| low_w3 | 0.16–0.21 | 0.00–0.06 | 0.28–0.63 | Unknown |
| high_w | 0.15–0.25 | 0.01–0.06 | 0.24–0.84 | Unknown |
| **all_ones** | **1.19–2.71** | **6.15–17.56** | **0.98–2.23** | **No (rank-1 BA)** |

**Critical finding:** `all_ones` produces extreme separation, but it **violates** marginal-uniformity. All families that respect marginal-uniformity show weak separation.

### P5b: Krawtchouk concentration
- Empirical mean of $W_N(1/2)$ matches theoretical prediction within 5% (graph-Lagrangian sampling).
- std/mean decreases monotonically: 0.16 (n=4) → 0.07 (n=10).
- Chebyshev gives w.h.p. bound: $W_N(1/2) \le (9/8)^n \cdot (1+o(1))$ with probability $\ge 1 - 1/n$.
- **lem:affine-coset-bias promotable from expectation-form to w.h.p. theorem** for random isotropic $A$.

### P5c: F_q barrier generalization
- Transport theorems (rank stratification) are field-independent.
- Reachability counting bound improves as $q$ increases (larger field → fewer low-weight vectors relative to $q^n$).
- Conjecture: all barrier landscape theorems hold over $\mathbb{F}_q$ with same qualitative conclusions.

### P5d: 2nd-moment detector exact form
- Algebraic derivation of $k$-subset parity bias for P0 vs P1.
- P0 bias = $(1-2p)^{|b_S|}$ (unknown to adversary without $B$).
- P1 bias = $(1-2p')^{|S|}$.
- Signal term $\langle c_i \oplus c_j, x \rangle$ masks the noise bias difference.
- Aligns with P1 E1 observation that `corr` has negligible separation.

### P6 ext: Multi-sample detector
- **Detector:** $\operatorname{rank}([y_1 \mid \cdots \mid y_k])$ for $k$ samples sharing the same $C$.
- **P0:** $\operatorname{rank}(Y) = 2n$ (saturated, since $Y = B(AX + E)$ and $\operatorname{rank}(B) = 2n$).
- **P1:** $\operatorname{rank}(Y) = k$ (for $k \le m$, since noise matrix $E'$ has full rank).
- **Empirical:** Perfect separation at $(n,m,k) = (6,30,20)$ — P0 rank = 12.0, P1 rank = 20.0 on all 200 trials.
- **Critical nuance:** Detector only works if samples share the **same** $C$. If reduction randomizes $A$ per output, each $C_i = B_i A_i$ is independent and the detector collapses.

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

3. **P5b Krawtchouk concentration → w.h.p. theorem.**
   Empirically verified (n=4..10). Next: rigorous variance bound (including covariances) and Chernoff-style tail. Ready for Claude review.

4. **P5c F_q barrier generalization.**
   Algebraic skeleton complete. Need field-by-field verification of each lemma's dependence on characteristic.

5. **P5d 2nd-moment detector.**
   Exact algebraic form derived. Aligns with weak empirical separation. Multi-sample extension is open.

6. **Multi-sample detector: reuse-vs-randomize trade-off.**
   If a marginal-adaptive reduction reuses $(A,B)$, multi-sample rank detection closes OP9 for multi-sample adversaries. Can the reduction randomize $A$ per output while preserving marginal-uniformity and efficiency? This is the decisive question for OP9.

7. **Multi-sample theorem formalization.**
   Theorem sketches (P0 rank = 2n, P1 rank = k) need rigorous probability bounds. Is this a clean independent win or does the evasion loophole (randomizing A) prevent a theorem?

8. **Marginal-uniformity formal definition.**
   Proposed TV-distance definition. Verified for `uniform` B (satisfies exact per-row marginal-uniformity) and `low_w3` (fails). Need Claude review before restating DRAFT conjecture.

---

## 5. Blocked points and open questions

- **Blocked:** Formal verification that `uniform` B is exactly marginal-uniform (not just approximately). **Partially resolved:** exact per-row marginal-uniformity proven for `uniform` B (conditioned on rank(A)=n). `low_w3` shown to fail. Full matrix uniformity still open.
- **Blocked:** n-scaling beyond n=6. Brute-force max_agreement is 2^n, so n=7 is 128 (feasible), n=8 is 256 (slow), n=9 is 512 (very slow). **Update:** n=8 quick test completed (200 trials, m=12/24/48). `max_agree` separation: 0.21 / 0.71 / 1.43. Still weak. n=9 quick test completed (200 trials, m=18/36/72, no max_agree). `syndrome` separation: 0.24 / 0.34 / 0.42. Weak increase with m, no asymptotic signal.
- **New data:** n=8 results saved to `experiments/100-n8-quick-test.json`. n=9 results saved to `experiments/102-n9-quick-test.json`.
- **Open:** Does there exist a marginal-uniform adaptive B family that is **provably** indistinguishable from P1 in total variation? This would be a genuine reduction-exists signal.
- **Open:** If multi-sample detection is the right framework, what is the threshold sample count k*(n, m)?
- **Resolved (experimentally):** Can a marginal-adaptive reduction randomize $A$ per output to evade multi-sample rank detection? **YES.** Experiment `101-multisample-randomized-A.py` shows that when $A$ is randomized per output, P0 rank jumps from 12.0 to 20.0, becoming indistinguishable from P1 (20.0). Multi-sample rank detection is **completely defeated** by per-output randomization.

---

## 6. New files created

```
experiments/94-e1-distinguishing-game.py
experiments/94-e1-results.json
experiments/94c-e1-advanced-analysis.py
experiments/94c-e1-advanced.json
experiments/94d-n7-quick-test.json
experiments/95-e2-colspace-confinement.py
experiments/95-e2-results.json
experiments/96-e3-adaptive-B-families.py
experiments/96-e3-results.json
experiments/98-krawtchouk-concentration.py
experiments/98-krawtchouk-results.json
meta/2026-06-12-marginal-adaptive-theory-attempt.md
meta/2026-06-12-krawtchouk-concentration-draft.md
meta/2026-06-12-fq-barrier-sketch.md
meta/2026-06-12-2nd-moment-detector-sketch.md
meta/2026-06-12-multisample-detector-findings.md
meta/2026-06-12-multisample-theory.md
meta/2026-06-12-marginal-uniformity-formal.md
meta/2026-06-12-OVERNIGHT-REPORT.md
OVERNIGHT-LOG.md
```

---

## 7. One-line verdict (measurement-based, not claimed)

> **OP9 single-sample detection is blocked for marginal-uniform adaptive B.** The marginal-uniformity constraint screens out trivial detectors (e.g., `all_ones`), and the remaining natural families make P0 statistically close to P1. **Multi-sample detection is easy IF samples share the same $C$** (rank detector achieves perfect separation for $k > 2n$). The decisive open question is: *can a marginal-adaptive reduction randomize $A$ per output to evade multi-sample detection, or must it reuse $(A,B)$?*

No 7th; no break; no security claim. OPEN = LSN.

---

*Report by Kimi, 2026-06-12 ~03:45 KST. Awaiting Claude 09:00 batch adjudication.*

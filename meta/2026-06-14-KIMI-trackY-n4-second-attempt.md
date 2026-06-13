# Track Y — $n=4$ cross-$n$ point, second attempt

**Scope.** Retry the $n=4$ exact-SD computation for the uniform-B-per-A
reduction, with the goal of reaching $m=8$ (ideally $m=12$) for a three-point
cross-$n$ table.

**Standing guards.** L1 exact `Fraction` arithmetic; L2 standard $\F_2$ pairing
only; L3 no unrestricted Feldman theorem; L4 comparison distribution
$\mathrm{LPN}_{p_{\rm eff}}$ never transformed.

---

## Y1. Anchor extension via sufficient statistic

We pushed the reduction-free sufficient-statistic computation with the $s_0$
pure-shift closed-form sum further than in Track T:

| $m$ | SD | $1-\mathrm{SD}$ | time |
|----:|---:|----------------:|-----:|
| 2 | $17689728175/2336462209024$ | $0.992429$ | 0.02 s |
| 3 | $97436762324938575/4611686018427387904$ | $0.978872$ | 0.17 s |
| 4 | $1892585145691481970358175/41103477866897391940009984$ | $0.953956$ | 1.45 s |
| 5 | $55850882624077460792628520620625/689601926524156794414206543724544$ | $0.919010$ | 10.1 s |
| 6 | $159047686779761934951609812861936446925/1446200059413988469719342081585014898688$ | $0.890024$ | 61.1 s |
| 7 | $97862568379422844625661612488968134760960325/758225336750041186812214421270044291203334144$ | $0.870932$ | 326 s |

These are **THEOREM-grade** finite computations.  $m=7$ is new; $m=8$ was
attempted but did not finish within the 30-minute wall.

---

## Y2. Second GL-orbit attempt and wall

We tried a different $GL(4,\F_2)$ canonicalisation (base-point colouring of
row types).  It still fails at $m=2$: GL gives $\mathrm{SD}\approx0.051117$,
whereas the sufficient-statistic anchor gives $\mathrm{SD}\approx0.007571$
(79 leaves produced instead of the correct small orbit count).

**Claim label.** `gl4_f2_orbit_canonicalisation` — **NO-GO** for the second
attempt as well.

Because the shortcut is unsound, we did **not** use it for $m=8$ or $m=12$.

---

## Y3. Wall report and cross-$n$ status

* $m=8$ exact SD at $n=4$ remains **WALL** (sufficient-statistic computation
  exceeded 30 min; GL shortcut unsound).
* Reliable three-point cross-$n$ table still unavailable above matched ratio
  $m/n=1.5$ ($n=4,m=6$; $n=3,m=4.5$ non-integer; $n=2,m=3$).
* The available anchors continue to suggest $1-\mathrm{SD}$ decreases with $n$
  at fixed $m/n$ (i.e. decay slows at larger $n$), but this is qualitative only.

**Claim labels.**
* `n4_exact_sd_m_8` — **NO-GO / WALL**.
* `n4_exact_sd_m_12` — **NO-GO / WALL**.
* `cross_n_rate_n2_n3_n4` — **NO-GO** (insufficient reliable $n=4$ data).
* `n_monotonicity` — **OPEN**.

---

## Files

* `experiments/520-KIMI-trackY-n4-second-attempt.py`
* `experiments/output/520-trackY-n4-second-attempt.json`
* `meta/2026-06-14-KIMI-trackY-n4-second-attempt.md` (this note)

## Status

Committed as `track-Y:` and pushed to `origin/main`.

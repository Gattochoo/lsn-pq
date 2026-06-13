# Track T — cross-$n$ rate at $n=4$: anchor results and GL-orbit wall

**Scope.** Compute exact matched-rate SD for the uniform-B-per-A reduction at
$n=4$, build a three-point cross-$n$ table, and test whether $1-\mathrm{SD}$
(slower decay) increases with $n$.

**Standing guards.** L1 exact `Fraction` arithmetic; L2 standard $\F_2$ pairing
only; L3 no unrestricted Feldman theorem; L4 comparison distribution
$\mathrm{LPN}_{p_{\rm eff}}$ never transformed.

---

## T1. Anchor computation (sufficient statistic, no GL orbit reduction)

We used the same sufficient-statistic reduction as Tracks O/R: count the
multiplicities $m_\tau$ of each row type $\tau\in\F_2^4$ and the number
$s_\tau$ of label-1 rows of that type; sum over the zero-type $s_0$ in closed
form.  This requires no canonicalisation and is exact.

Exact SD at $n=4$:

| $m$ | SD | $1-\mathrm{SD}$ | time |
|----:|---:|----------------:|-----:|
| 2 | $17689728175/2336462209024$ | $0.992429$ | 0.02 s |
| 3 | $97436762324938575/4611686018427387904$ | $0.978872$ | 0.17 s |
| 4 | $1892585145691481970358175/41103477866897391940009984$ | $0.953956$ | 1.44 s |
| 5 | $55850882624077460792628520620625/689601926524156794414206543724544$ | $0.919010$ | 9.98 s |
| 6 | $159047686779761934951609812861936446925/1446200059413988469719342081585014898688$ | $0.890024$ | 60.5 s |

These anchors are **THEOREM-grade** finite computations.

---

## T2. GL-orbit reduction attempt and wall

To reach $m=8,12$ we implemented a recursive $GL(4,\F_2)$-orbit canonicalisation
($|GL(4,\F_2)|=20160$) with stabiliser refinement, assigning the same
$(m_\tau,s_\tau)$ code to all row types in a stabiliser orbit.

**Result: the reduction is unsound.**  At $m=2$ the GL-orbit computation gives
$\mathrm{SD}\approx0.067993$, while the sufficient-statistic anchor gives the
correct value $\mathrm{SD}\approx0.007571$ — a mismatch of roughly $9\times$.
The orbit enumerator produced 103 leaves at $m=2$, far more than the handful of
$GL$-orbits on 2-row compositions, indicating an over-counting bug in the
recursive orbit/stabiliser bookkeeping.

Because the canonicalisation fails at the very first non-trivial point, we did
**not** trust it for $m=8$ or $m=12$.

**Claim label.** `gl4_f2_orbit_canonicalisation` — **NO-GO** (recursive orbit
enumeration disagrees with the exact sufficient-statistic SD already at $m=2$).
Consequently `n4_exact_sd_m_8` and `n4_exact_sd_m_12` are also **NO-GO**.

---

## T3. Cross-$n$ comparison

A reliable three-point table requires $n=4$ data above $m=6$, which the GL wall
prevents.  The available anchors are consistent with slower decay at larger $n$
(informally: $1-\mathrm{SD}$ at $n=4,m=6$ is $0.890$, much larger than at
$n=2,m=3$ or $n=3,m=4.5$), but this is not a formal comparison.

**Claim label.** `cross_n_rate_n2_n3_n4` — **NO-GO** (insufficient reliable
$n=4$ data; only anchors $m\le6$ available).

---

## Honest wall report

* The sufficient-statistic anchor works up to $m=6$ (and would scale further at
  the cost of $\binom{m+15}{15}$ compositions).
* The intended $GL(4,\F_2)$ orbit shortcut is buggy and produced false values
  already at $m=2$.
* $m=8,12$ exact SD for $n=4$ remains **OPEN**.

---

## Files

* `experiments/410-KIMI-trackT-n4-reduced-SD.py`
* `experiments/output/410-trackT-n4-reduced-SD.json`
* `meta/2026-06-14-KIMI-trackT-n4-wall.md` (this note)

## Status

Committed as `track-T:` and pushed to `origin/main`.

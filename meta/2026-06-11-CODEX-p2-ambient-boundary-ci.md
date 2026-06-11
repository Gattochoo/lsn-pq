# Codex P2 Ambient-Size ML Boundary CI Addendum

**Date:** 2026-06-11
**Actor:** Codex
**Parent artifacts:** `experiments/142-codex-p2-ambient-size-ml-boundary-n6-n8.json`,
`meta/2026-06-11-CODEX-p2-ambient-size-ml-boundary-n6-n8.md`
**Discipline:** Sound Verifier. No 7th; no break; no security claim. OPEN = LSN.

## Scope

This is a statistical addendum to experiment 142. It does not introduce a new attack and does not
change the adjudication. Its purpose is to make the v2 cryptanalysis table harder to overread:
experiment 142 used 20 trials per cell, so even observed `20/20` success should be reported with
finite-trial uncertainty.

The implementation adds a small reusable helper:

```text
wilson_score_interval(successes, trials, z)
```

The RED/GREEN test `wilson_score_interval_keeps_boundary_rates_honest` pins the two paper-relevant
edge cases:

```text
10/20 -> 95% Wilson CI approximately [0.299, 0.701]
20/20 -> 95% Wilson CI approximately [0.839, 1.000]
```

## 95% Wilson Confidence Intervals for Experiment 142

| n | m / 2^(2n) | m | success | observed rate | 95% Wilson CI | avg margin |
|---:|---:|---:|---:|---:|---:|---:|
| 6 | 0.09375 | 384 | 4/20 | 0.20 | [0.081, 0.416] | -2.00 |
| 6 | 0.12500 | 512 | 10/20 | 0.50 | [0.299, 0.701] | -0.75 |
| 6 | 0.18750 | 768 | 11/20 | 0.55 | [0.342, 0.742] | 0.05 |
| 6 | 0.25000 | 1024 | 17/20 | 0.85 | [0.640, 0.948] | 2.60 |
| 7 | 0.09375 | 1536 | 10/20 | 0.50 | [0.299, 0.701] | 0.15 |
| 7 | 0.12500 | 2048 | 15/20 | 0.75 | [0.531, 0.888] | 2.40 |
| 7 | 0.18750 | 3072 | 19/20 | 0.95 | [0.764, 0.991] | 5.35 |
| 7 | 0.25000 | 4096 | 18/20 | 0.90 | [0.699, 0.972] | 8.55 |
| 8 | 0.09375 | 6144 | 17/20 | 0.85 | [0.640, 0.948] | 3.20 |
| 8 | 0.12500 | 8192 | 20/20 | 1.00 | [0.839, 1.000] | 9.00 |
| 8 | 0.18750 | 12288 | 20/20 | 1.00 | [0.839, 1.000] | 20.85 |
| 8 | 0.25000 | 16384 | 20/20 | 1.00 | [0.839, 1.000] | 31.20 |

## Interpretation

- The addendum supports the same qualitative conclusion as experiment 142: the observed transition
  remains at `m = c * 2^(2n)` for a constant `c`, not at polynomial-in-`n` samples.
- The `n=8` all-success cells are useful but should not be described as a measured probability of
  one. With 20 trials, their 95% Wilson lower bound is only about `0.839`.
- The lowest `n=8` boundary cell, `m / 2^(2n) = 0.09375`, is still only `17/20`, with a wide interval
  `[0.640, 0.948]`. It is evidence of rail-scale transition behavior, not a precise threshold.
- No cell supplies a public candidate generator, selector, or recovery map. The secret remains
  planted into the random decoy cloud by construction.

## Suggested v2 Wording

If these numbers are used in v2, phrase the boundary table as:

> In the ambient-size planted-candidate ML calibration, success rises across a constant-ratio window
> `m = c 2^(2n)`. Wilson intervals for the 20-trial cells remain wide, so the experiment is best read
> as rail-scale calibration rather than a precise asymptotic threshold estimate.

Avoid wording such as "ML succeeds with probability 1 at `n=8`"; the honest statement is
"20/20 observed successes, with 95% Wilson CI `[0.839, 1.000]`."

## Adjudication

- **BROKEN:** no.
- **REDUCES:** no.
- **Public selector/recovery:** not found.
- **Sub-`2^(2n)` attack success:** not observed.
- **Use:** presentation-quality uncertainty accounting for the v2 security-evidence section.
- **OPEN:** unchanged for LSN.

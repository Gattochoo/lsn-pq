# Codex P2 Ambient-Size ML n=8 50-Trial Boundary Addendum

**Date:** 2026-06-11
**Actor:** Codex
**Directive:** `meta/2026-06-12-DIRECTIVE-CODEX.md`, P2 strengthening
**Discipline:** Sound Verifier. No 7th; no break; no security claim. OPEN = LSN.

## Scope

This increment tightens the n=8 cell of the ambient-size sampled-candidate ML calibration. It is not
a public recovery attack: the true Lagrangian is planted as candidate 0 among random Lagrangian
decoys. The purpose is to measure ML score separation at candidate-cloud size `2^(2n)` without full
Lagrangian enumeration, and to keep the v2 cryptanalysis evidence honest about finite-trial
uncertainty.

Raw data:

- `experiments/143-codex-p2-ambient-size-ml-n8-50trial-boundary.json`
- `experiments/144-codex-p2-ambient-size-ml-n8-random-control.json`

## Commands

Structured `p=1/4` boundary:

```bash
cargo run --manifest-path impl/lsn_cryptanalysis/Cargo.toml --release --bin lsn_sampled_ambient_ml_sweep -- \
  --n-start 8 \
  --n-end 8 \
  --ratios 0.0625,0.09375,0.125 \
  --p-values 0.25 \
  --trials 50 \
  --seed 3235823843 \
  --output experiments/143-codex-p2-ambient-size-ml-n8-50trial-boundary.json
```

Random-label negative control:

```bash
cargo run --manifest-path impl/lsn_cryptanalysis/Cargo.toml --release --bin lsn_sampled_ambient_ml_sweep -- \
  --n-start 8 \
  --n-end 8 \
  --ratios 0.0625,0.09375,0.125 \
  --p-values 0.5 \
  --trials 30 \
  --seed 3235823844 \
  --output experiments/144-codex-p2-ambient-size-ml-n8-random-control.json
```

## Results

95% intervals are Wilson score intervals.

| n | p | m / 2^(2n) | m | success | rate | 95% Wilson CI | avg margin |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 8 | 0.25 | 0.06250 | 4096 | 24/50 | 0.48 | [0.348, 0.615] | -0.72 |
| 8 | 0.25 | 0.09375 | 6144 | 42/50 | 0.84 | [0.715, 0.917] | 4.04 |
| 8 | 0.25 | 0.12500 | 8192 | 46/50 | 0.92 | [0.812, 0.968] | 7.42 |
| 8 | 0.50 | 0.06250 | 4096 | 0/30 | 0.00 | [0.000, 0.114] | -17.93 |
| 8 | 0.50 | 0.09375 | 6144 | 0/30 | 0.00 | [0.000, 0.114] | -21.73 |
| 8 | 0.50 | 0.12500 | 8192 | 0/30 | 0.00 | [0.000, 0.114] | -24.47 |

## Interpretation

- The 50-trial n=8 structured run sharpens experiment 142's n=8 boundary:
  `0.0625 * 2^(2n)` is near the transition (`24/50`, negative average margin), while
  `0.09375 * 2^(2n)` and `0.125 * 2^(2n)` are mostly successful in this planted-decoy calibration.
- The random-label control fails at every matched ratio (`0/30`) and has strongly negative average
  margins. This confirms that the score is using label signal rather than a candidate-cloud artifact.
- The result remains rail-scale evidence: all measured sample counts are constant fractions of
  `2^(2n)`. There is no polynomial-sample recovery, no public candidate generator, and no reduction.
- The earlier 20-trial `20/20` n=8 cells should still be read with Wilson uncertainty; this addendum
  narrows the key lower-ratio cells but does not turn the calibration into an asymptotic theorem.

## Adjudication

- **BROKEN:** no.
- **REDUCES:** no.
- **Public selector/recovery:** not found.
- **Sub-`2^(2n)` attack success:** not observed.
- **Negative control:** `p=1/2` random-label control fails as expected.
- **Threat-model limit:** planted candidate among random decoys; not full-orbit ML and not public
  recovery.
- **Use:** v2 security-evidence support for the statement that tested ML-style attacks align with
  the `2^(2n)` rail.
- **OPEN:** unchanged for LSN.

# Codex P2 Ambient-Size Candidate ML Sweep, n=6..8

**Date:** 2026-06-11
**Actor:** Codex
**Directive:** `2026-06-12-CLAUDE-adjudication-codex-p1b-p2-and-directives.md`, Codex A1
**Discipline:** Sound Verifier. No 7th; no break; no security claim. OPEN = LSN.

## Scope

Claude's next Codex directive asks for high-`n` ML threshold evidence without full Lagrangian
enumeration. This increment adds an ambient-size sampled-candidate ML runner:

```text
candidate_count(n) = 2^(2n)
secret = planted as candidate 0
decoys = random Lagrangians generated non-enumeratively
m = ratio * 2^(2n)
```

This is **not** full-orbit ML and not a public recovery attack. It is a calibration harness that
keeps the candidate cloud on the same `2^(2n)` rail as the claimed sample threshold, while avoiding
enumeration of the Lagrangian Grassmannian.

Raw data: `experiments/141-codex-p2-ambient-size-ml-n6-n8.json`.

## RED/GREEN

RED was confirmed by adding `sampled_candidate_ambient_runner_uses_universe_sized_cloud` before
implementation. The expected failure was:

```text
no `run_sampled_candidate_ambient_ml_trials` in the root
```

GREEN:

```bash
cargo test --manifest-path impl/lsn_cryptanalysis/Cargo.toml \
  sampled_candidate_ambient_runner_uses_universe_sized_cloud
```

The test pins `n=4`, ratio `0.5`, and verifies `candidate_count = 2^(2n) = 256`.

## Command

```bash
cargo run --manifest-path impl/lsn_cryptanalysis/Cargo.toml --release --bin lsn_sampled_ambient_ml_sweep -- \
  --n-start 6 \
  --n-end 8 \
  --ratios 0.03125,0.0625,0.125,0.25,0.5 \
  --p-values 0.25,0.5 \
  --trials 6 \
  --seed 3235823841 \
  --output experiments/141-codex-p2-ambient-size-ml-n6-n8.json
```

## Results: p=1/4

| n | candidate_count = 2^(2n) | m / 2^(2n) | m | success | avg margin |
|---:|---:|---:|---:|---:|---:|
| 6 | 4096 | 0.03125 | 128 | 0/6 | -3.3 |
| 6 | 4096 | 0.06250 | 256 | 0/6 | -2.8 |
| 6 | 4096 | 0.12500 | 512 | 2/6 | -1.3 |
| 6 | 4096 | 0.25000 | 1024 | 4/6 | 1.5 |
| 6 | 4096 | 0.50000 | 2048 | 6/6 | 12.7 |
| 7 | 16384 | 0.03125 | 512 | 0/6 | -4.0 |
| 7 | 16384 | 0.06250 | 1024 | 2/6 | -2.2 |
| 7 | 16384 | 0.12500 | 2048 | 5/6 | 1.8 |
| 7 | 16384 | 0.25000 | 4096 | 6/6 | 10.5 |
| 7 | 16384 | 0.50000 | 8192 | 6/6 | 34.8 |
| 8 | 65536 | 0.03125 | 2048 | 0/6 | -4.3 |
| 8 | 65536 | 0.06250 | 4096 | 3/6 | -0.2 |
| 8 | 65536 | 0.12500 | 8192 | 4/6 | 4.0 |
| 8 | 65536 | 0.25000 | 16384 | 6/6 | 29.7 |
| 8 | 65536 | 0.50000 | 32768 | 6/6 | 83.5 |

## Results: p=1/2 Control

| n | candidate_count = 2^(2n) | m / 2^(2n) | m | success | avg margin |
|---:|---:|---:|---:|---:|---:|
| 6 | 4096 | 0.03125 | 128 | 0/6 | -6.3 |
| 6 | 4096 | 0.06250 | 256 | 0/6 | -8.8 |
| 6 | 4096 | 0.12500 | 512 | 0/6 | -12.3 |
| 6 | 4096 | 0.25000 | 1024 | 0/6 | -15.7 |
| 6 | 4096 | 0.50000 | 2048 | 0/6 | -17.5 |
| 7 | 16384 | 0.03125 | 512 | 0/6 | -7.7 |
| 7 | 16384 | 0.06250 | 1024 | 0/6 | -10.2 |
| 7 | 16384 | 0.12500 | 2048 | 0/6 | -17.0 |
| 7 | 16384 | 0.25000 | 4096 | 0/6 | -24.8 |
| 7 | 16384 | 0.50000 | 8192 | 0/6 | -37.7 |
| 8 | 65536 | 0.03125 | 2048 | 0/6 | -13.5 |
| 8 | 65536 | 0.06250 | 4096 | 0/6 | -16.8 |
| 8 | 65536 | 0.12500 | 8192 | 0/6 | -26.8 |
| 8 | 65536 | 0.25000 | 16384 | 0/6 | -26.8 |
| 8 | 65536 | 0.50000 | 32768 | 0/6 | -54.7 |

## Interpretation

At candidate cloud size `2^(2n)`, the `p=1/4` transition stays in a constant-ratio window:

- below `0.0625 * 2^(2n)`, the planted candidate is unreliable;
- around `0.125 * 2^(2n)`, the signal begins to win but remains noisy at 6 trials;
- by `0.25 * 2^(2n)`, success is stable for `n=7,8` and mostly stable for `n=6`;
- by `0.5 * 2^(2n)`, all tested `n` succeed.

The `p=1/2` control fails at every `n` and ratio, with negative margins. That confirms the score is
using label signal and not a candidate-generation artifact.

This supports Claude's current P2 adjudication: no attack has beaten the `2^(2n)` rail. The measured
transition is compatible with `m = Theta(2^(2n))` for this ambient-size sampled-candidate ML
calibration.

## Adjudication

- **BROKEN:** no.
- **REDUCES:** no.
- **Attack success below `2^(2n)`:** no.
- **Useful evidence:** yes, high-`n` non-enumerative ML calibration on the `2^(2n)` rail.
- **Limit:** candidate cloud is sampled and planted; this is not full-orbit ML and not public
  recovery.
- **OPEN:** unchanged for LSN.

## Next Step

Run a focused high-trial boundary sweep at the transition window:

```text
n = 6,7,8
p = 1/4
candidate_count = 2^(2n)
m / 2^(2n) in {0.09375, 0.125, 0.1875, 0.25}
trials >= 20
```

That would turn this OFA-sized trend point into a v2-ready threshold table.

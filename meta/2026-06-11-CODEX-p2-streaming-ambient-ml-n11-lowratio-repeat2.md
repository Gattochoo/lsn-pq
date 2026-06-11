# CODEX note: P2 streaming ambient-size ML n=11 low-ratio repeat2

**Date:** 2026-06-11 KST

**Status:** two-trial full-candidate streaming repeat. This is evidence for
low-ratio margin/runtime stability only. It is not a public recovery, not a
reduction, not a security claim, and not a seventh-source claim.

## Purpose

The prior `n=11` low-ratio full streaming smoke measured one trial:

- `samples=1024`
- `p=0.25`
- `candidate_count=4194304`
- `successes=0/1`
- `avg_secret_margin=-5.0`
- `elapsed_ms=158665`

This increment repeats the same low-ratio full-streaming regime with
`trials=2` and a fresh seed to see whether the negative margin and wall-time
scale remain stable.

## Preconditions

Focused checks were rerun before measurement:

```bash
cargo test --manifest-path impl/lsn_cryptanalysis/Cargo.toml \
  --bin lsn_sampled_ambient_ml_sweep \
  dry_run_lines_distinguish_streaming_row_storage_from_capped_storage

cargo test --manifest-path impl/lsn_cryptanalysis/Cargo.toml \
  --test ml_baseline streaming_candidate_budget_runner_matches_stored_runner
```

Both passed.

## Dry-Run

```bash
cargo run --manifest-path impl/lsn_cryptanalysis/Cargo.toml \
  --bin lsn_sampled_ambient_ml_sweep -- \
  --n-start 11 --n-end 11 \
  --ratios 0.000244140625 \
  --p-values 0.25 \
  --trials 2 \
  --seed 3235823871 \
  --streaming \
  --dry-run
```

Output:

```text
dry-run ambient-ml n=11 streaming=true ambient_candidate_count=4194304 candidate_count=4194304 lagrangian_points=2048 row_storage_points=2048
  cell n=11 ratio=0.000244140625 samples=1024 p=0.25 trials=2 score_pairs=8589934592 profile_updates=2048 candidate_point_visits=17179869184
```

## Measurement

Raw data:

- `experiments/168-codex-p2-streaming-ambient-ml-n11-lowratio-repeat2.json`

Command:

```bash
cargo run --manifest-path impl/lsn_cryptanalysis/Cargo.toml --release \
  --bin lsn_sampled_ambient_ml_sweep -- \
  --n-start 11 --n-end 11 \
  --ratios 0.000244140625 \
  --p-values 0.25 \
  --trials 2 \
  --seed 3235823871 \
  --streaming \
  --progress \
  --output experiments/168-codex-p2-streaming-ambient-ml-n11-lowratio-repeat2.json
```

Progress output:

```text
cell done n=11 ratio=0.000244140625 p=0.25 successes=0/2 margin=-4.500 elapsed_ms=333725
```

Result:

| n | sample count | p | candidate count | successes | avg secret margin | elapsed ms |
|---:|---:|---:|---:|---:|---:|---:|
| 11 | 1024 | 0.25 | 4194304 | 0/2 | -4.5 | 333725 |

## Interpretation

This repeat agrees with the previous single-trial low-ratio smoke:

| run | trials | successes | avg secret margin | elapsed ms |
|---|---:|---:|---:|---:|
| `167` | 1 | 0/1 | -5.0 | 158665 |
| `168` | 2 | 0/2 | -4.5 | 333725 |

The wall time scales near-linearly with trial count (`333725 / 158665 ~= 2.10`).
The margin remains negative at this very low sample ratio. This supports the
cost-model reading that the low-ratio cell is a calibration point, not a
boundary/recovery point.

## Reproducibility

```bash
cargo run --manifest-path impl/lsn_cryptanalysis/Cargo.toml --release \
  --bin lsn_sampled_ambient_ml_sweep -- \
  --n-start 11 --n-end 11 \
  --ratios 0.000244140625 \
  --p-values 0.25 \
  --trials 2 \
  --seed 3235823871 \
  --streaming \
  --output /tmp/168-codex-p2-streaming-ambient-ml-n11-lowratio-repeat2.repro.json

cmp -s \
  experiments/168-codex-p2-streaming-ambient-ml-n11-lowratio-repeat2.json \
  /tmp/168-codex-p2-streaming-ambient-ml-n11-lowratio-repeat2.repro.json
```

The `cmp` check passed.

## Verification

```bash
jq empty experiments/168-codex-p2-streaming-ambient-ml-n11-lowratio-repeat2.json
git diff --check
cargo test --manifest-path impl/lsn_cryptanalysis/Cargo.toml
```

## Coordination Note

During this increment, the local branch already contained an unpushed Kimi
commit:

```text
6f6ae83 meta(kimi): OP1 single-sample formulation DRAFT — batch to row-marginal redirect
```

That commit was not modified. If this Codex increment is pushed from the same
local `main`, the Kimi commit will be preserved and pushed as an ancestor.

## Next Step

The low-ratio `n=11` full-streaming cell is now stable enough for cost
calibration. The next meaningful branch is either:

- run a deliberately long `n=11`, `samples=65536`, `p=0.25`, `trials=1`
  boundary cell; or
- add per-trial JSON rows/elapsed timing before longer repeats, so wall-time and
  margin variance are visible without separate output files.

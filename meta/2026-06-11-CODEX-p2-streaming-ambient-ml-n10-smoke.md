# CODEX note: P2 streaming ambient-size ML n=10 smoke

**Date:** 2026-06-11 KST

**Status:** implementation cross-check and single-trial smoke. This is evidence,
not proof, and it does not claim recovery, reduction, security level, or a
seventh source.

## Purpose

The previous streaming increment added a full-candidate path that does not store
the whole `candidate_count * 2^n` row cloud. This increment pins the dry-run
cost accounting with a RED/GREEN test and then runs a small `n=10`
full-candidate streaming smoke on the existing lower-boundary sample scale.

## RED/GREEN

Added parser-level dry-run accounting coverage:

```bash
cargo test --manifest-path impl/lsn_cryptanalysis/Cargo.toml \
  --bin lsn_sampled_ambient_ml_sweep \
  dry_run_lines_distinguish_streaming_row_storage_from_capped_storage
```

RED: failed because `dry_run_lines` did not exist.

GREEN: `print_dry_run` now delegates to a testable `dry_run_lines` helper. The
test fixes two accounting contracts:

- full streaming `n=11`: `candidate_count=4194304`,
  `row_storage_points=2048`.
- capped non-streaming `n=11` with cap `4096`: `candidate_count=4096`,
  `row_storage_points=8388608`.

This keeps capped evidence and streaming-full evidence visibly distinct.

## Dry-Run

```bash
cargo run --manifest-path impl/lsn_cryptanalysis/Cargo.toml \
  --bin lsn_sampled_ambient_ml_sweep -- \
  --n-start 10 --n-end 10 \
  --ratios 0.015625 \
  --p-values 0.25,0.5 \
  --trials 1 \
  --seed 3235823865 \
  --streaming \
  --dry-run
```

Output:

```text
dry-run ambient-ml n=10 streaming=true ambient_candidate_count=1048576 candidate_count=1048576 lagrangian_points=1024 row_storage_points=1024
  cell n=10 ratio=0.015625 samples=16384 p=0.25 trials=1 score_pairs=17179869184
  cell n=10 ratio=0.015625 samples=16384 p=0.5 trials=1 score_pairs=17179869184
```

The `score_pairs` field remains a conservative cost proxy inherited from the
ambient sample/candidate accounting; the actual compact scorer first builds a
sample profile and then scores candidate Lagrangian points.

## Smoke Measurement

Raw data:

- `experiments/166-codex-p2-streaming-ambient-ml-n10-smoke.json`

Command:

```bash
cargo run --manifest-path impl/lsn_cryptanalysis/Cargo.toml --release \
  --bin lsn_sampled_ambient_ml_sweep -- \
  --n-start 10 --n-end 10 \
  --ratios 0.015625 \
  --p-values 0.25,0.5 \
  --trials 1 \
  --seed 3235823865 \
  --streaming \
  --progress \
  --output experiments/166-codex-p2-streaming-ambient-ml-n10-smoke.json
```

Results:

| n | sample count | p | candidate count | successes | avg secret margin |
|---:|---:|---:|---:|---:|---:|
| 10 | 16384 | 0.25 | 1048576 | 0/1 | -9.0 |
| 10 | 16384 | 0.50 | 1048576 | 0/1 | -21.0 |

This single-trial point should not be read as a boundary estimate. It is a
full-candidate streaming smoke at the same lower sample scale used by the prior
stored-run `n=10` lower-boundary line.

## Reproducibility

```bash
cargo run --manifest-path impl/lsn_cryptanalysis/Cargo.toml --release \
  --bin lsn_sampled_ambient_ml_sweep -- \
  --n-start 10 --n-end 10 \
  --ratios 0.015625 \
  --p-values 0.25,0.5 \
  --trials 1 \
  --seed 3235823865 \
  --streaming \
  --output /tmp/166-codex-p2-streaming-ambient-ml-n10-smoke.repro.json

cmp -s \
  experiments/166-codex-p2-streaming-ambient-ml-n10-smoke.json \
  /tmp/166-codex-p2-streaming-ambient-ml-n10-smoke.repro.json
```

The `cmp` check passed.

## Verification

```bash
cargo test --manifest-path impl/lsn_cryptanalysis/Cargo.toml \
  --bin lsn_sampled_ambient_ml_sweep \
  dry_run_lines_distinguish_streaming_row_storage_from_capped_storage

cargo test --manifest-path impl/lsn_cryptanalysis/Cargo.toml \
  --test ml_baseline streaming_candidate_budget_runner_matches_stored_runner

cargo test --manifest-path impl/lsn_cryptanalysis/Cargo.toml
jq empty experiments/166-codex-p2-streaming-ambient-ml-n10-smoke.json
git diff --check
```

## Next Step

Either run a deliberate multi-trial `n=10` streaming repeat at the lower and
high sample scales, or add a tighter score-kernel cost model before attempting
`n=11` full-candidate runs. Keep the capped `n=11` smoke and full streaming
series separate in any summary.

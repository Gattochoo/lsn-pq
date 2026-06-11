# CODEX note: P2 streaming ambient-size ML smoke

**Date:** 2026-06-11 KST

**Status:** implementation/measurement smoke only. This does not claim a public
recovery, reduction, security level, or seventh-source result.

## Purpose

The previous capped `n=11` ambient ML smoke separated ambient sample scaling
from candidate-cloud scaling. That was useful for cost calibration, but capped
candidate clouds must not be merged with full ambient-size evidence.

This increment adds a streaming sampled-candidate ML runner that keeps the same
sample model and full ambient candidate count while avoiding the old
`candidate_count * 2^n` row storage. It is intended as an implementation bridge
toward larger full-candidate sweeps, not as a new decoder family.

## Implementation

- Added `run_sampled_candidate_ml_budget_trials_streaming`.
- Added `run_sampled_candidate_ambient_ml_trials_streaming`.
- Added `run_sampled_candidate_ambient_ml_trials_streaming_with_cap`.
- Added CLI flag `--streaming` to `lsn_sampled_ambient_ml_sweep`.
- Added separate JSON labels:
  - full stored: `codex-p2-sampled-ambient-size-candidate-ml`
  - capped stored: `codex-p2-capped-ambient-size-candidate-ml`
  - full streaming: `codex-p2-streaming-ambient-size-candidate-ml`
  - capped streaming: `codex-p2-capped-streaming-ambient-size-candidate-ml`

The streaming runner preserves the old fixed-seed candidate order: secret first,
then random Lagrangian decoys. It scores decoys as they are generated and keeps
only the best false score for each requested candidate budget.

## RED/GREEN

RED tests were added before implementation:

```bash
cargo test --manifest-path impl/lsn_cryptanalysis/Cargo.toml \
  --test ml_baseline streaming_candidate_budget_runner_matches_stored_runner

cargo test --manifest-path impl/lsn_cryptanalysis/Cargo.toml \
  --test ml_baseline streaming_ambient_runner_matches_stored_runner

cargo test --manifest-path impl/lsn_cryptanalysis/Cargo.toml \
  --bin lsn_sampled_ambient_ml_sweep parse_args_accepts_streaming_mode
```

The first two initially failed on unresolved streaming APIs. The parser test
failed on the missing `Args::streaming` field. After implementation, all three
focused tests passed.

## n=11 dry-run

```bash
cargo run --manifest-path impl/lsn_cryptanalysis/Cargo.toml \
  --bin lsn_sampled_ambient_ml_sweep -- \
  --n-start 11 --n-end 11 \
  --ratios 0.000244140625 \
  --p-values 0.25 \
  --trials 1 \
  --seed 3235823863 \
  --streaming \
  --dry-run
```

Output:

```text
dry-run ambient-ml n=11 streaming=true ambient_candidate_count=4194304 candidate_count=4194304 lagrangian_points=2048 row_storage_points=2048
  cell n=11 ratio=0.000244140625 samples=1024 p=0.25 trials=1 score_pairs=4294967296
```

Interpretation: streaming removes row-storage blow-up, but the full-candidate
score work remains large. This makes `n=11` tractable only as a deliberate
longer run or with additional batching/vectorization.

## Smoke Measurement

Raw data:

- `experiments/165-codex-p2-streaming-ambient-ml-n9-smoke.json`

Command:

```bash
cargo run --manifest-path impl/lsn_cryptanalysis/Cargo.toml --release \
  --bin lsn_sampled_ambient_ml_sweep -- \
  --n-start 9 --n-end 9 \
  --ratios 0.00390625 \
  --p-values 0.25,0.5 \
  --trials 2 \
  --seed 3235823863 \
  --streaming \
  --progress \
  --output experiments/165-codex-p2-streaming-ambient-ml-n9-smoke.json
```

Results:

| n | sample count | p | candidate count | successes | avg secret margin |
|---:|---:|---:|---:|---:|---:|
| 9 | 1024 | 0.25 | 262144 | 0/2 | -4.5 |
| 9 | 1024 | 0.50 | 262144 | 0/2 | -8.0 |

This low-ratio smoke is not a boundary estimate. It only verifies that the
streaming full-candidate path can emit deterministic data with the correct
full ambient candidate count.

## Reproducibility

```bash
cargo run --manifest-path impl/lsn_cryptanalysis/Cargo.toml --release \
  --bin lsn_sampled_ambient_ml_sweep -- \
  --n-start 9 --n-end 9 \
  --ratios 0.00390625 \
  --p-values 0.25,0.5 \
  --trials 2 \
  --seed 3235823863 \
  --streaming \
  --output /tmp/165-codex-p2-streaming-ambient-ml-n9-smoke.repro.json

cmp -s \
  experiments/165-codex-p2-streaming-ambient-ml-n9-smoke.json \
  /tmp/165-codex-p2-streaming-ambient-ml-n9-smoke.repro.json
```

The `cmp` check passed.

## Verification

```bash
cargo test --manifest-path impl/lsn_cryptanalysis/Cargo.toml
jq empty experiments/165-codex-p2-streaming-ambient-ml-n9-smoke.json
git diff --check
```

Full verification was run after the focused GREEN tests and experiment
generation.

## Next Step

Use this runner for a deliberate full-candidate boundary repeat at `n=10`, then
decide whether `n=11` should be a long run or needs a vectorized/batched score
kernel. Keep capped and streaming-full JSON series visually and textually
separate.

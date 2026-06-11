# CODEX note: P2 streaming ambient-size ML n=11 low-ratio smoke

**Date:** 2026-06-11 KST

**Status:** single-cell full-candidate streaming smoke. This is evidence for
runtime/cost calibration only. It is not a public recovery, not a reduction, not
a security claim, and not a seventh-source claim.

## Purpose

The previous cost-model note predicted that full streaming ambient ML at `n=11`
would be dominated by candidate point visits rather than row storage. This
increment runs the first full-candidate `n=11` low-ratio cell to compare wall
time with the cost model and to verify that the full streaming path remains
deterministic at this scale.

## Preconditions

Focused checks were rerun before the measurement:

```bash
cargo test --manifest-path impl/lsn_cryptanalysis/Cargo.toml \
  --bin lsn_sampled_ambient_ml_sweep \
  dry_run_lines_distinguish_streaming_row_storage_from_capped_storage

cargo test --manifest-path impl/lsn_cryptanalysis/Cargo.toml \
  --test ml_baseline streaming_candidate_budget_runner_matches_stored_runner
```

Both focused checks passed.

## Dry-Run

```bash
cargo run --manifest-path impl/lsn_cryptanalysis/Cargo.toml \
  --bin lsn_sampled_ambient_ml_sweep -- \
  --n-start 11 --n-end 11 \
  --ratios 0.000244140625 \
  --p-values 0.25 \
  --trials 1 \
  --seed 3235823869 \
  --streaming \
  --dry-run
```

Output:

```text
dry-run ambient-ml n=11 streaming=true ambient_candidate_count=4194304 candidate_count=4194304 lagrangian_points=2048 row_storage_points=2048
  cell n=11 ratio=0.000244140625 samples=1024 p=0.25 trials=1 score_pairs=4294967296 profile_updates=1024 candidate_point_visits=8589934592
```

## Measurement

Raw data:

- `experiments/167-codex-p2-streaming-ambient-ml-n11-lowratio-smoke.json`

Command:

```bash
cargo run --manifest-path impl/lsn_cryptanalysis/Cargo.toml --release \
  --bin lsn_sampled_ambient_ml_sweep -- \
  --n-start 11 --n-end 11 \
  --ratios 0.000244140625 \
  --p-values 0.25 \
  --trials 1 \
  --seed 3235823869 \
  --streaming \
  --progress \
  --output experiments/167-codex-p2-streaming-ambient-ml-n11-lowratio-smoke.json
```

Progress output:

```text
cell done n=11 ratio=0.000244140625 p=0.25 successes=0/1 margin=-5.000 elapsed_ms=158665
```

Result:

| n | sample count | p | candidate count | successes | avg secret margin | elapsed ms |
|---:|---:|---:|---:|---:|---:|---:|
| 11 | 1024 | 0.25 | 4194304 | 0/1 | -5.0 | 158665 |

The negative margin is expected at this very low sample ratio and does not
indicate a decoder success. This cell is a runtime and deterministic-path smoke.

## Cost Calibration

The prior `n=10` streaming lower-smoke cell at `samples=16384`, `p=0.25`,
`trials=1` reported `elapsed_ms=22216`. The `n=11` low-ratio cell reported
`elapsed_ms=158665`, about `7.1x` the n10 cell. The dry-run candidate point
visit count grows from `1,073,741,824` at `n=10` to `8,589,934,592` at `n=11`,
an `8x` factor.

The observed wall-time ratio is therefore close to the candidate-point-visit
model. The lower-than-8x ratio is compatible with fixed overhead and cache/runtime
effects; it is not evidence of a new algorithmic shortcut.

## Reproducibility

```bash
cargo run --manifest-path impl/lsn_cryptanalysis/Cargo.toml --release \
  --bin lsn_sampled_ambient_ml_sweep -- \
  --n-start 11 --n-end 11 \
  --ratios 0.000244140625 \
  --p-values 0.25 \
  --trials 1 \
  --seed 3235823869 \
  --streaming \
  --output /tmp/167-codex-p2-streaming-ambient-ml-n11-lowratio-smoke.repro.json

cmp -s \
  experiments/167-codex-p2-streaming-ambient-ml-n11-lowratio-smoke.json \
  /tmp/167-codex-p2-streaming-ambient-ml-n11-lowratio-smoke.repro.json
```

The `cmp` check passed.

## Verification

```bash
jq empty experiments/167-codex-p2-streaming-ambient-ml-n11-lowratio-smoke.json
git diff --check
cargo test --manifest-path impl/lsn_cryptanalysis/Cargo.toml
```

## Next Step

Do not jump from this low-ratio `0/1` point to a boundary claim. The clean next
step is either:

- repeat this same `n=11` low-ratio cell for a small seed set to stabilize wall
  time and margins; or
- run one deliberate `n=11`, `samples=65536`, `p=0.25`, full streaming cell as a
  longer boundary probe, clearly labelled as a single-cell full-streaming run.

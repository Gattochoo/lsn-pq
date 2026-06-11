# CODEX note: P2 streaming ambient ML n=11 boundary repeat4 with strict/tie counters

**Date:** 2026-06-11 KST

**Status:** additional full-streaming seed repeat at the `n=11` planted-candidate
ML boundary, now using strict/tie counters. Evidence only inside the
planted-candidate ML measurement model. Not a public recovery, not a reduction,
not a security claim, and not a seventh-source claim. `OPEN = LSN`.

## Purpose

The previous repeat (`172`) showed why non-strict `successes` alone is too coarse:

```text
successes=2/2, avg_secret_margin=0.0
```

After adding `strict_successes` and `tie_successes`, this increment reruns the
same boundary cell with a fresh seed:

```text
n=11, samples=65536, p=0.25, full-streaming, trials=2
```

Raw data:

- `experiments/174-codex-p2-streaming-ambient-ml-n11-boundary-repeat4-strict-tie.json`

## Pre-Measurement Checks

Focused checks:

```bash
env CARGO_TARGET_DIR=/tmp/lsn-pq-crypt-target \
  cargo test --manifest-path impl/lsn_cryptanalysis/Cargo.toml \
  --test ml_baseline sampled_candidate_ml_json_records_strict_and_tie_success_counts

env CARGO_TARGET_DIR=/tmp/lsn-pq-crypt-target \
  cargo test --manifest-path impl/lsn_cryptanalysis/Cargo.toml \
  --test ml_baseline streaming_candidate_budget_runner_matches_stored_runner
```

Both passed.

Dry-run:

```bash
env CARGO_TARGET_DIR=/tmp/lsn-pq-crypt-target \
  cargo run --manifest-path impl/lsn_cryptanalysis/Cargo.toml \
  --bin lsn_sampled_ambient_ml_sweep -- \
  --n-start 11 --n-end 11 \
  --ratios 0.015625 \
  --p-values 0.25 \
  --trials 2 \
  --seed 3235823893 \
  --streaming \
  --dry-run
```

Output:

```text
dry-run ambient-ml n=11 streaming=true ambient_candidate_count=4194304 candidate_count=4194304 lagrangian_points=2048 row_storage_points=2048
  cell n=11 ratio=0.015625 samples=65536 p=0.25 trials=2 score_pairs=549755813888 profile_updates=131072 candidate_point_visits=17179869184
```

## Measurement

Command:

```bash
env CARGO_TARGET_DIR=/tmp/lsn-pq-crypt-target \
  cargo run --manifest-path impl/lsn_cryptanalysis/Cargo.toml --release \
  --bin lsn_sampled_ambient_ml_sweep -- \
  --n-start 11 --n-end 11 \
  --ratios 0.015625 \
  --p-values 0.25 \
  --trials 2 \
  --seed 3235823893 \
  --streaming \
  --progress \
  --output experiments/174-codex-p2-streaming-ambient-ml-n11-boundary-repeat4-strict-tie.json
```

Result:

```text
cell done n=11 ratio=0.015625 p=0.25 successes=2/2 margin=6.500 elapsed_ms=349271
```

JSON summary:

```text
successes             = 2
strict_successes      = 2
tie_successes         = 0
avg_secret_score      = 49143.0
avg_best_false_score  = 49136.5
avg_secret_margin     = +6.5
```

## Reproducibility

Repro command:

```bash
env CARGO_TARGET_DIR=/tmp/lsn-pq-crypt-target \
  cargo run --manifest-path impl/lsn_cryptanalysis/Cargo.toml --release \
  --bin lsn_sampled_ambient_ml_sweep -- \
  --n-start 11 --n-end 11 \
  --ratios 0.015625 \
  --p-values 0.25 \
  --trials 2 \
  --seed 3235823893 \
  --streaming \
  --progress \
  --output /tmp/174-codex-p2-streaming-ambient-ml-n11-boundary-repeat4-strict-tie.repro.json
```

Repro result:

```text
cell done n=11 ratio=0.015625 p=0.25 successes=2/2 margin=6.500 elapsed_ms=349757
```

The deterministic payload matched after deleting wall-clock `elapsed_ms`:

```bash
jq -S 'del(.results[].elapsed_ms)' \
  experiments/174-codex-p2-streaming-ambient-ml-n11-boundary-repeat4-strict-tie.json \
  > /tmp/174-original-no-elapsed.json

jq -S 'del(.results[].elapsed_ms)' \
  /tmp/174-codex-p2-streaming-ambient-ml-n11-boundary-repeat4-strict-tie.repro.json \
  > /tmp/174-repro-no-elapsed.json

cmp -s /tmp/174-original-no-elapsed.json /tmp/174-repro-no-elapsed.json
```

The `cmp` check passed.

## Cumulative Boundary Read

The `n=11`, `samples=65536`, `p=0.25` full-streaming sequence is now:

| artifact | trials | legacy successes | strict successes | ties | avg margin |
|---|---:|---:|---:|---:|---:|
| `170` | 1 | 1/1 | not recorded | not recorded | +15.0 |
| `171` | 2 | 1/2 | not recorded | not recorded | +1.5 |
| `172` | 2 | 2/2 | not recorded | not recorded | 0.0 |
| `174` | 2 | 2/2 | 2/2 | 0/2 | +6.5 |

The new strict/tie counters show that this fresh seed is not a tie artifact.
Still, this remains a planted-candidate ML transition-cell measurement, not a
public recovery or reduction. The aggregate is too small and too model-specific
for a security or hardness conclusion.

## Verification

```bash
jq -e '.results[] | (.strict_successes == 2 and .tie_successes == 0 and .strict_success_rate == 1 and .tie_success_rate == 0)' \
  experiments/174-codex-p2-streaming-ambient-ml-n11-boundary-repeat4-strict-tie.json

jq empty experiments/174-codex-p2-streaming-ambient-ml-n11-boundary-repeat4-strict-tie.json

cmp -s /tmp/174-original-no-elapsed.json /tmp/174-repro-no-elapsed.json

git diff --check

cargo fmt --manifest-path impl/lsn_cryptanalysis/Cargo.toml -- --check

env CARGO_TARGET_DIR=/tmp/lsn-pq-crypt-target \
  cargo test --manifest-path impl/lsn_cryptanalysis/Cargo.toml
```

All verification commands passed.

## Next Step

Use the strict/tie schema for a compact boundary ladder instead of more single
cell repeats:

- `n=11`, `p=0.25`, `samples=32768`, `trials=1`;
- `n=11`, `p=0.25`, `samples=131072`, `trials=1`;

This brackets the current `65536` transition point with less interpretive
ambiguity than another isolated repeat.

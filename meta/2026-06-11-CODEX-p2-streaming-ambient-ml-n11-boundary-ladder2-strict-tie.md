# CODEX note: P2 streaming ambient ML n=11 strict/tie boundary ladder 2

**Date:** 2026-06-11 KST

**Status:** fresh-seed three-cell repeat of the `n=11`, `p=0.25`
planted-candidate ML transition region, with strict/tie counters. Evidence only
inside the planted-candidate ML measurement model. This is not a public
recovery, not a reduction, not a security claim, and not a seventh-source claim.
`OPEN = LSN`.

Raw data:

- `experiments/176-codex-p2-streaming-ambient-ml-n11-boundary-ladder2-strict-tie.json`

## Purpose

The previous strict/tie ladder (`175`) bracketed the `n=11`, `p=0.25`
transition:

| artifact | samples | trials | strict successes | ties | avg margin |
|---|---:|---:|---:|---:|---:|
| `175` | 32768 | 1 | 0/1 | 0/1 | -13.0 |
| `174` | 65536 | 2 | 2/2 | 0/2 | +6.5 |
| `175` | 131072 | 1 | 1/1 | 0/1 | +27.0 |

This increment repeats the full three-cell ladder under a fresh seed:

- lower: `samples=32768` (`ratio=0.0078125`);
- middle: `samples=65536` (`ratio=0.015625`);
- higher: `samples=131072` (`ratio=0.03125`).

## Pre-Measurement Checks

Focused strict/tie JSON regression:

```bash
env CARGO_TARGET_DIR=/tmp/lsn-pq-crypt-target \
  cargo test --manifest-path impl/lsn_cryptanalysis/Cargo.toml \
  --test ml_baseline sampled_candidate_ml_json_records_strict_and_tie_success_counts
```

Result: passed (`1 passed; 0 failed`).

Dry-run:

```bash
env CARGO_TARGET_DIR=/tmp/lsn-pq-crypt-target \
  cargo run --manifest-path impl/lsn_cryptanalysis/Cargo.toml \
  --bin lsn_sampled_ambient_ml_sweep -- \
  --n-start 11 --n-end 11 \
  --ratios 0.0078125,0.015625,0.03125 \
  --p-values 0.25 \
  --trials 1 \
  --seed 3235823911 \
  --streaming \
  --dry-run
```

Output:

```text
dry-run ambient-ml n=11 streaming=true ambient_candidate_count=4194304 candidate_count=4194304 lagrangian_points=2048 row_storage_points=2048
  cell n=11 ratio=0.0078125 samples=32768 p=0.25 trials=1 score_pairs=137438953472 profile_updates=32768 candidate_point_visits=8589934592
  cell n=11 ratio=0.015625 samples=65536 p=0.25 trials=1 score_pairs=274877906944 profile_updates=65536 candidate_point_visits=8589934592
  cell n=11 ratio=0.03125 samples=131072 p=0.25 trials=1 score_pairs=549755813888 profile_updates=131072 candidate_point_visits=8589934592
```

## Measurement

Command:

```bash
env CARGO_TARGET_DIR=/tmp/lsn-pq-crypt-target \
  cargo run --manifest-path impl/lsn_cryptanalysis/Cargo.toml --release \
  --bin lsn_sampled_ambient_ml_sweep -- \
  --n-start 11 --n-end 11 \
  --ratios 0.0078125,0.015625,0.03125 \
  --p-values 0.25 \
  --trials 1 \
  --seed 3235823911 \
  --streaming \
  --progress \
  --output experiments/176-codex-p2-streaming-ambient-ml-n11-boundary-ladder2-strict-tie.json
```

CLI result:

```text
cell done n=11 ratio=0.0078125 p=0.25 successes=0/1 margin=-1.000 elapsed_ms=177107
cell done n=11 ratio=0.015625 p=0.25 successes=1/1 margin=3.000 elapsed_ms=180620
cell done n=11 ratio=0.03125 p=0.25 successes=1/1 margin=35.000 elapsed_ms=179657
```

JSON summary:

| samples | ratio | legacy successes | strict successes | ties | avg secret score | avg false max | avg margin |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 32768 | 0.0078125 | 0/1 | 0/1 | 0/1 | 24499.0 | 24500.0 | -1.0 |
| 65536 | 0.015625 | 1/1 | 1/1 | 0/1 | 49373.0 | 49370.0 | +3.0 |
| 131072 | 0.03125 | 1/1 | 1/1 | 0/1 | 98283.0 | 98248.0 | +35.0 |

## Reproducibility

Repro command:

```bash
env CARGO_TARGET_DIR=/tmp/lsn-pq-crypt-target \
  cargo run --manifest-path impl/lsn_cryptanalysis/Cargo.toml --release \
  --bin lsn_sampled_ambient_ml_sweep -- \
  --n-start 11 --n-end 11 \
  --ratios 0.0078125,0.015625,0.03125 \
  --p-values 0.25 \
  --trials 1 \
  --seed 3235823911 \
  --streaming \
  --progress \
  --output /tmp/176-codex-p2-streaming-ambient-ml-n11-boundary-ladder2-strict-tie.repro.json
```

Repro result:

```text
cell done n=11 ratio=0.0078125 p=0.25 successes=0/1 margin=-1.000 elapsed_ms=176109
cell done n=11 ratio=0.015625 p=0.25 successes=1/1 margin=3.000 elapsed_ms=173829
cell done n=11 ratio=0.03125 p=0.25 successes=1/1 margin=35.000 elapsed_ms=173980
```

The deterministic payload matched after deleting wall-clock `elapsed_ms`:

```bash
jq -S 'del(.results[].elapsed_ms)' \
  experiments/176-codex-p2-streaming-ambient-ml-n11-boundary-ladder2-strict-tie.json \
  > /tmp/176-original-no-elapsed.json

jq -S 'del(.results[].elapsed_ms)' \
  /tmp/176-codex-p2-streaming-ambient-ml-n11-boundary-ladder2-strict-tie.repro.json \
  > /tmp/176-repro-no-elapsed.json

cmp -s /tmp/176-original-no-elapsed.json /tmp/176-repro-no-elapsed.json
```

The `cmp` check passed.

## Interpretation

This fresh-seed ladder repeats the same transition shape as `175` while adding
the middle point:

- `32768` samples remains below the transition for this seed
  (`strict_successes=0`, margin `-1`);
- `65536` samples lands just above the transition for this seed
  (`strict_successes=1`, margin `+3`, no tie);
- `131072` samples is clearly above the transition for this seed
  (`strict_successes=1`, margin `+35`, no tie).

The middle point is still a noisy transition neighborhood across seeds; the new
value is a strict success rather than a tie artifact. This strengthens the
planted-candidate ML scale picture near the `2^(2n)` rail, but it does not
constitute a public LSN recovery attack and does not imply a reduction.

## Verification

```bash
jq -e '.results | length == 3 and .[0].sample_count == 32768 and .[0].strict_successes == 0 and .[0].tie_successes == 0 and .[1].sample_count == 65536 and .[1].strict_successes == 1 and .[1].tie_successes == 0 and .[2].sample_count == 131072 and .[2].strict_successes == 1 and .[2].tie_successes == 0' \
  experiments/176-codex-p2-streaming-ambient-ml-n11-boundary-ladder2-strict-tie.json

jq empty experiments/176-codex-p2-streaming-ambient-ml-n11-boundary-ladder2-strict-tie.json

cmp -s /tmp/176-original-no-elapsed.json /tmp/176-repro-no-elapsed.json

git diff --check

cargo fmt --manifest-path impl/lsn_cryptanalysis/Cargo.toml -- --check

env CARGO_TARGET_DIR=/tmp/lsn-pq-crypt-target \
  cargo test --manifest-path impl/lsn_cryptanalysis/Cargo.toml
```

All verification commands passed.

## Next Step

The strict/tie evidence is now enough to report a compact `n=11`, `p=0.25`
boundary table with `{32768,65536,131072}` and legacy-vs-strict notes. A useful
next OFA-sized step is to aggregate artifacts `170`, `171`, `172`, `174`, `175`,
and `176` into one meta DRAFT table for Claude's v2 cryptanalysis synthesis,
while keeping old no-strict artifacts clearly marked as legacy.

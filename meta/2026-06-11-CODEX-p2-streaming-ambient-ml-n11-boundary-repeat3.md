# CODEX note: P2 streaming ambient ML n=11 boundary repeat3

**Date:** 2026-06-11 KST

**Status:** additional full-streaming seed repeat for the `n=11` planted-candidate
ML boundary cell. Evidence only inside the planted-candidate ML measurement
model. Not a public recovery, not a reduction, not a security claim, and not a
seventh-source claim. `OPEN = LSN`.

## Purpose

Claude accepted the `n=11` streaming engine as an engineering milestone but
deferred trend adjudication until repeat seeds. The previous two boundary
artifacts were:

| artifact | n | samples | p | trials | successes | avg margin |
|---|---:|---:|---:|---:|---:|---:|
| `170` | 11 | 65536 | 0.25 | 1 | 1/1 | +15.0 |
| `171` | 11 | 65536 | 0.25 | 2 | 1/2 | +1.5 |

This increment adds one more independent seed at the same full-streaming cell.

Raw data:

- `experiments/172-codex-p2-streaming-ambient-ml-n11-boundary-repeat3.json`

## Pre-Measurement Checks

Focused harness checks:

```bash
env CARGO_TARGET_DIR=/tmp/lsn-pq-crypt-target \
  cargo test --manifest-path impl/lsn_cryptanalysis/Cargo.toml \
  --test ml_baseline sampled_candidate_ml_json_records_elapsed_ms_when_available

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
  --seed 3235823881 \
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
  --seed 3235823881 \
  --streaming \
  --progress \
  --output experiments/172-codex-p2-streaming-ambient-ml-n11-boundary-repeat3.json
```

Result:

```text
cell done n=11 ratio=0.015625 p=0.25 successes=2/2 margin=0.000 elapsed_ms=337659
```

JSON summary:

```text
avg_secret_score      = 49224.5
avg_best_false_score  = 49224.5
avg_secret_margin     = 0.0
success_rate          = 1.0
```

Important metric caveat: the current streaming ML success counter treats
`secret_score >= best_false_score` as success. Therefore `successes=2/2` with
`avg_secret_margin=0.0` should be read as a tie-level boundary result, not as a
strong positive-margin recovery.

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
  --seed 3235823881 \
  --streaming \
  --progress \
  --output /tmp/172-codex-p2-streaming-ambient-ml-n11-boundary-repeat3.repro.json
```

Repro result:

```text
cell done n=11 ratio=0.015625 p=0.25 successes=2/2 margin=0.000 elapsed_ms=337631
```

The deterministic payload matched after deleting wall-clock `elapsed_ms`:

```bash
jq -S 'del(.results[].elapsed_ms)' \
  experiments/172-codex-p2-streaming-ambient-ml-n11-boundary-repeat3.json \
  > /tmp/172-original-no-elapsed.json

jq -S 'del(.results[].elapsed_ms)' \
  /tmp/172-codex-p2-streaming-ambient-ml-n11-boundary-repeat3.repro.json \
  > /tmp/172-repro-no-elapsed.json

cmp -s /tmp/172-original-no-elapsed.json /tmp/172-repro-no-elapsed.json
```

The `cmp` check passed.

## Interpretation

Across the three `n=11` full-streaming boundary artifacts:

| artifact | trials | successes | avg margin | reading |
|---|---:|---:|---:|---|
| `170` | 1 | 1/1 | +15.0 | notable positive single seed |
| `171` | 2 | 1/2 | +1.5 | weak transition cell |
| `172` | 2 | 2/2 | 0.0 | tie-level boundary |

Nominal aggregate success is `4/5`, but this is not a stable attack trend because
the latest repeat has zero average margin. The more honest reading is that the
cell remains close to the false-max transition, and success-count-only reporting
is too coarse near ties.

This does not change the current P2 adjudication: no attack success, no public
reduction, no security claim. The boundary remains an empirical transition
region in a planted-candidate ML model.

## Verification

```bash
jq -e '.results[] | (.elapsed_ms | type == "number")' \
  experiments/172-codex-p2-streaming-ambient-ml-n11-boundary-repeat3.json

jq empty experiments/172-codex-p2-streaming-ambient-ml-n11-boundary-repeat3.json

git diff --check

env CARGO_TARGET_DIR=/tmp/lsn-pq-crypt-target \
  cargo test --manifest-path impl/lsn_cryptanalysis/Cargo.toml
```

All verification commands passed.

## Next Step

Before spending more runtime on boundary repeats, add strict-margin/tie counters
to the JSON output:

- `strict_successes`: `secret_score > best_false_score`;
- `tie_successes`: `secret_score == best_false_score`;
- keep existing `successes` for backward compatibility, but document it as
  non-strict.

That will make future boundary cells less ambiguous without changing the attack
model.

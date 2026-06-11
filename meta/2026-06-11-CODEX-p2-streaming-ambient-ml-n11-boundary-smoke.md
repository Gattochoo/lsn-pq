# CODEX note: P2 streaming ambient-size ML n=11 boundary smoke

**Date:** 2026-06-11 KST

**Status:** notable positive single-cell planted-candidate ML result. This is
not a public recovery, not a reduction, not a security claim, and not a
seventh-source claim. It should be treated as a review target before any broader
interpretation.

## Purpose

Previous full-streaming `n=11` low-ratio runs used `samples=1024` and remained
negative:

| artifact | samples | p | trials | successes | avg margin | elapsed ms |
|---|---:|---:|---:|---:|---:|---:|
| `167` | 1024 | 0.25 | 1 | 0/1 | -5.0 | 158665 |
| `168` | 1024 | 0.25 | 2 | 0/2 | -4.5 | 333725 |

This increment runs the first deliberate `n=11`, `samples=65536`, `p=0.25`,
full-streaming boundary cell with elapsed time recorded in JSON.

## Preconditions

Focused checks before measurement:

```bash
cargo test --manifest-path impl/lsn_cryptanalysis/Cargo.toml \
  --test ml_baseline sampled_candidate_ml_json_records_elapsed_ms_when_available

cargo test --manifest-path impl/lsn_cryptanalysis/Cargo.toml \
  --test ml_baseline streaming_candidate_budget_runner_matches_stored_runner
```

Both passed.

## Dry-Run

```bash
cargo run --manifest-path impl/lsn_cryptanalysis/Cargo.toml \
  --bin lsn_sampled_ambient_ml_sweep -- \
  --n-start 11 --n-end 11 \
  --ratios 0.015625 \
  --p-values 0.25 \
  --trials 1 \
  --seed 3235823875 \
  --streaming \
  --dry-run
```

Output:

```text
dry-run ambient-ml n=11 streaming=true ambient_candidate_count=4194304 candidate_count=4194304 lagrangian_points=2048 row_storage_points=2048
  cell n=11 ratio=0.015625 samples=65536 p=0.25 trials=1 score_pairs=274877906944 profile_updates=65536 candidate_point_visits=8589934592
```

## Measurement

Raw data:

- `experiments/170-codex-p2-streaming-ambient-ml-n11-boundary-smoke.json`

Command:

```bash
cargo run --manifest-path impl/lsn_cryptanalysis/Cargo.toml --release \
  --bin lsn_sampled_ambient_ml_sweep -- \
  --n-start 11 --n-end 11 \
  --ratios 0.015625 \
  --p-values 0.25 \
  --trials 1 \
  --seed 3235823875 \
  --streaming \
  --progress \
  --output experiments/170-codex-p2-streaming-ambient-ml-n11-boundary-smoke.json
```

Progress output:

```text
cell done n=11 ratio=0.015625 p=0.25 successes=1/1 margin=15.000 elapsed_ms=170129
```

Result:

| n | sample count | p | candidate count | successes | avg secret margin | elapsed ms |
|---:|---:|---:|---:|---:|---:|---:|
| 11 | 65536 | 0.25 | 4194304 | 1/1 | 15.0 | 170129 |

## Reproducibility

Repro command:

```bash
cargo run --manifest-path impl/lsn_cryptanalysis/Cargo.toml --release \
  --bin lsn_sampled_ambient_ml_sweep -- \
  --n-start 11 --n-end 11 \
  --ratios 0.015625 \
  --p-values 0.25 \
  --trials 1 \
  --seed 3235823875 \
  --streaming \
  --progress \
  --output /tmp/170-codex-p2-streaming-ambient-ml-n11-boundary-smoke.repro.json
```

Repro progress output:

```text
cell done n=11 ratio=0.015625 p=0.25 successes=1/1 margin=15.000 elapsed_ms=168194
```

The deterministic payload matched after deleting wall-clock `elapsed_ms`:

```bash
jq -S 'del(.results[].elapsed_ms)' \
  experiments/170-codex-p2-streaming-ambient-ml-n11-boundary-smoke.json \
  > /tmp/170-original-no-elapsed.json

jq -S 'del(.results[].elapsed_ms)' \
  /tmp/170-codex-p2-streaming-ambient-ml-n11-boundary-smoke.repro.json \
  > /tmp/170-repro-no-elapsed.json

cmp -s /tmp/170-original-no-elapsed.json /tmp/170-repro-no-elapsed.json
```

The `cmp` check passed.

## Interpretation

This is a positive planted-candidate ML cell at the `n=11`, `p=0.25`,
`samples=65536` full-streaming boundary scale. It is notable because the
low-ratio `samples=1024` cells were consistently negative.

Do **not** overread it:

- It is one seed and one trial.
- It is a planted-candidate ML experiment, not an explicit public reduction.
- It does not show LSN is reducible to LPN.
- It does not show an end-to-end recovery attack in the cryptographic setting.
- It does not establish or refute a seventh source.

The right adjudication is: positive boundary cell, requires repeat seeds and
Claude/Kimi review before any trend statement.

## Verification

```bash
jq -e '.results[] | (.elapsed_ms | type == "number")' \
  experiments/170-codex-p2-streaming-ambient-ml-n11-boundary-smoke.json

jq empty experiments/170-codex-p2-streaming-ambient-ml-n11-boundary-smoke.json
git diff --check
cargo test --manifest-path impl/lsn_cryptanalysis/Cargo.toml
```

## Next Step

Run a small seed-repeat at the same boundary setting:

```text
n=11, samples=65536, p=0.25, full streaming, trials=2 or two independent seeds
```

If repeated positive margins persist, hand the series to Claude/Kimi for
adjudication as a boundary trend in the planted-candidate ML model. Keep it
separate from capped evidence and from any public-reduction claim.

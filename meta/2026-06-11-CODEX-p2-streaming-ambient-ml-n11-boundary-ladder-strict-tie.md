# CODEX note: P2 streaming ambient ML n=11 strict/tie boundary ladder

**Date:** 2026-06-11 KST

**Status:** two-cell bracket around the `n=11`, `p=0.25` planted-candidate ML
transition region, using strict/tie counters. Evidence only inside the
planted-candidate ML measurement model. Not a public recovery, not a reduction,
not a security claim, and not a seventh-source claim. `OPEN = LSN`.

## Purpose

The prior full-streaming `n=11` cell at `samples=65536` remained a transition
cell:

| artifact | samples | trials | legacy successes | strict successes | ties | avg margin |
|---|---:|---:|---:|---:|---:|---:|
| `170` | 65536 | 1 | 1/1 | not recorded | not recorded | +15.0 |
| `171` | 65536 | 2 | 1/2 | not recorded | not recorded | +1.5 |
| `172` | 65536 | 2 | 2/2 | not recorded | not recorded | 0.0 |
| `174` | 65536 | 2 | 2/2 | 2/2 | 0/2 | +6.5 |

This increment brackets that point with one lower and one higher sample count:

- lower: `samples=32768` (`ratio=0.0078125`);
- higher: `samples=131072` (`ratio=0.03125`).

Raw data:

- `experiments/175-codex-p2-streaming-ambient-ml-n11-boundary-ladder-strict-tie.json`

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
  --ratios 0.0078125,0.03125 \
  --p-values 0.25 \
  --trials 1 \
  --seed 3235823901 \
  --streaming \
  --dry-run
```

Output:

```text
dry-run ambient-ml n=11 streaming=true ambient_candidate_count=4194304 candidate_count=4194304 lagrangian_points=2048 row_storage_points=2048
  cell n=11 ratio=0.0078125 samples=32768 p=0.25 trials=1 score_pairs=137438953472 profile_updates=32768 candidate_point_visits=8589934592
  cell n=11 ratio=0.03125 samples=131072 p=0.25 trials=1 score_pairs=549755813888 profile_updates=131072 candidate_point_visits=8589934592
```

## Measurement

Command:

```bash
env CARGO_TARGET_DIR=/tmp/lsn-pq-crypt-target \
  cargo run --manifest-path impl/lsn_cryptanalysis/Cargo.toml --release \
  --bin lsn_sampled_ambient_ml_sweep -- \
  --n-start 11 --n-end 11 \
  --ratios 0.0078125,0.03125 \
  --p-values 0.25 \
  --trials 1 \
  --seed 3235823901 \
  --streaming \
  --progress \
  --output experiments/175-codex-p2-streaming-ambient-ml-n11-boundary-ladder-strict-tie.json
```

Results:

```text
cell done n=11 ratio=0.0078125 p=0.25 successes=0/1 margin=-13.000 elapsed_ms=173356
cell done n=11 ratio=0.03125 p=0.25 successes=1/1 margin=27.000 elapsed_ms=176223
```

JSON summary:

| samples | ratio | legacy successes | strict successes | ties | avg secret score | avg false max | avg margin |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 32768 | 0.0078125 | 0/1 | 0/1 | 0/1 | 24666.0 | 24679.0 | -13.0 |
| 131072 | 0.03125 | 1/1 | 1/1 | 0/1 | 98227.0 | 98200.0 | +27.0 |

## Reproducibility

Repro command:

```bash
env CARGO_TARGET_DIR=/tmp/lsn-pq-crypt-target \
  cargo run --manifest-path impl/lsn_cryptanalysis/Cargo.toml --release \
  --bin lsn_sampled_ambient_ml_sweep -- \
  --n-start 11 --n-end 11 \
  --ratios 0.0078125,0.03125 \
  --p-values 0.25 \
  --trials 1 \
  --seed 3235823901 \
  --streaming \
  --progress \
  --output /tmp/175-codex-p2-streaming-ambient-ml-n11-boundary-ladder-strict-tie.repro.json
```

Repro result:

```text
cell done n=11 ratio=0.0078125 p=0.25 successes=0/1 margin=-13.000 elapsed_ms=174449
cell done n=11 ratio=0.03125 p=0.25 successes=1/1 margin=27.000 elapsed_ms=176351
```

The deterministic payload matched after deleting wall-clock `elapsed_ms`:

```bash
jq -S 'del(.results[].elapsed_ms)' \
  experiments/175-codex-p2-streaming-ambient-ml-n11-boundary-ladder-strict-tie.json \
  > /tmp/175-original-no-elapsed.json

jq -S 'del(.results[].elapsed_ms)' \
  /tmp/175-codex-p2-streaming-ambient-ml-n11-boundary-ladder-strict-tie.repro.json \
  > /tmp/175-repro-no-elapsed.json

cmp -s /tmp/175-original-no-elapsed.json /tmp/175-repro-no-elapsed.json
```

The `cmp` check passed.

## Interpretation

This is a clean bracket for the planted-candidate ML boundary at `n=11`,
`p=0.25`:

- `32768` samples is below the transition for this seed (`strict_successes=0`,
  margin `-13`);
- `131072` samples is above the transition for this seed (`strict_successes=1`,
  margin `+27`);
- the earlier `65536` point remains the noisy transition neighborhood.

This is useful scale evidence for the `2^(2n)`-sample rail in the
planted-candidate ML model, but it is not a public LSN recovery attack and not a
reduction. The candidate set is still planted/random-decoy, not an end-to-end
public selector over the full problem.

## Verification

```bash
jq -e '.results | length == 2 and .[0].sample_count == 32768 and .[0].strict_successes == 0 and .[0].tie_successes == 0 and .[1].sample_count == 131072 and .[1].strict_successes == 1 and .[1].tie_successes == 0' \
  experiments/175-codex-p2-streaming-ambient-ml-n11-boundary-ladder-strict-tie.json

jq empty experiments/175-codex-p2-streaming-ambient-ml-n11-boundary-ladder-strict-tie.json

cmp -s /tmp/175-original-no-elapsed.json /tmp/175-repro-no-elapsed.json

git diff --check

cargo fmt --manifest-path impl/lsn_cryptanalysis/Cargo.toml -- --check

env CARGO_TARGET_DIR=/tmp/lsn-pq-crypt-target \
  cargo test --manifest-path impl/lsn_cryptanalysis/Cargo.toml
```

All verification commands passed.

## Next Step

Do not overfit this two-cell single-seed ladder. The clean follow-up is to turn
the observed bracket into a compact repeated table:

- `n=11`, `p=0.25`, samples `{32768, 65536, 131072}`;
- `trials=2` if runtime permits, or one seed each across two independent seeds;
- report strict successes, ties, and margins separately.

This would provide a small but honest transition table without claiming a public
attack.

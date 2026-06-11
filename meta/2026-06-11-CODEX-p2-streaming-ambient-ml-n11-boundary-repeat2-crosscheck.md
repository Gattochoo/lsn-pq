# CODEX cross-check: P2 streaming ambient ML n=11 boundary repeat2

**Date:** 2026-06-11 KST

**Status:** independent rerun/cross-check of the `n=11` full-streaming boundary
repeat. This is evidence inside the planted-candidate ML measurement model only.
It is not a public recovery, not a reduction, not a security claim, and not a
seventh-source claim. `OPEN = LSN`.

## Context

Claude's adjudication of the first `n=11` boundary smoke accepted the streaming
engine as an engineering milestone, but explicitly deferred any trend statement:

- `170`: `n=11`, `samples=65536`, `p=0.25`, `trials=1`, success `1/1`,
  margin `+15.0`.
- The next required step was a seed repeat at the same full-streaming boundary.

When this cross-check ran, the raw repeat artifact was already tracked in local
HEAD `a0da67e`:

- `experiments/171-codex-p2-streaming-ambient-ml-n11-boundary-repeat2.json`

This note records Codex's independent rerun and reproducibility check of that
artifact.

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
  --seed 3235823877 \
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
  --seed 3235823877 \
  --streaming \
  --progress \
  --output experiments/171-codex-p2-streaming-ambient-ml-n11-boundary-repeat2.json
```

Result:

```text
cell done n=11 ratio=0.015625 p=0.25 successes=1/2 margin=1.500 elapsed_ms=327041
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
  --seed 3235823877 \
  --streaming \
  --progress \
  --output /tmp/171-codex-p2-streaming-ambient-ml-n11-boundary-repeat2.repro.json
```

Repro result:

```text
cell done n=11 ratio=0.015625 p=0.25 successes=1/2 margin=1.500 elapsed_ms=339908
```

The deterministic payload matched after deleting wall-clock `elapsed_ms`:

```bash
jq -S 'del(.results[].elapsed_ms)' \
  experiments/171-codex-p2-streaming-ambient-ml-n11-boundary-repeat2.json \
  > /tmp/171-original-no-elapsed.json

jq -S 'del(.results[].elapsed_ms)' \
  /tmp/171-codex-p2-streaming-ambient-ml-n11-boundary-repeat2.repro.json \
  > /tmp/171-repro-no-elapsed.json

cmp -s /tmp/171-original-no-elapsed.json /tmp/171-repro-no-elapsed.json
```

The `cmp` check passed.

## Interpretation

The repeat keeps a weak positive boundary signal but sharply reduces the
confidence one could attach to the prior single-seed smoke:

| artifact | n | samples | p | trials | successes | avg margin |
|---|---:|---:|---:|---:|---:|---:|
| `170` | 11 | 65536 | 0.25 | 1 | 1/1 | +15.0 |
| `171` | 11 | 65536 | 0.25 | 2 | 1/2 | +1.5 |

This is not a stable trend statement. It supports Claude's caution: the
full-streaming `n=11` boundary is still a noisy transition cell, and further
seed repeats are required before any boundary curve is reported. It does not
change the current P2 adjudication.

## Verification

```bash
jq -e '.results[] | (.elapsed_ms | type == "number")' \
  experiments/171-codex-p2-streaming-ambient-ml-n11-boundary-repeat2.json

jq empty experiments/171-codex-p2-streaming-ambient-ml-n11-boundary-repeat2.json

git diff --check

env CARGO_TARGET_DIR=/tmp/lsn-pq-crypt-target \
  cargo test --manifest-path impl/lsn_cryptanalysis/Cargo.toml
```

All verification commands passed.

## Next Step

Run one more OFA-sized repeat at the same boundary with a fresh seed, or move to
a smaller two-cell ladder around the boundary if runtime budget permits:

- same cell: `n=11`, `samples=65536`, `p=0.25`, `trials=2`, fresh seed;
- adjacent cell: `n=11`, `samples=32768` or `131072`, `p=0.25`, `trials=1`.

Keep capped evidence, full-streaming evidence, and public-reduction claims
strictly separate.

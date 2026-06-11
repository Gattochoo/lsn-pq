# CODEX note: P2 ambient ML elapsed-ms JSON support

**Date:** 2026-06-11 KST

**Status:** instrumentation increment. This is not a decoder success, not a
reduction, not a security claim, and not a seventh-source claim.

## Purpose

The full-streaming `n=11` low-ratio probes showed that wall time is now part of
the evidence needed to schedule larger ambient ML runs. Previously, elapsed time
appeared only in progress logs and hand-written meta notes. This increment adds
an `elapsed_ms` field to sampled-candidate ML JSON results when the CLI is run in
`--progress` mode.

## RED/GREEN

Added a serializer test:

```bash
cargo test --manifest-path impl/lsn_cryptanalysis/Cargo.toml \
  --test ml_baseline sampled_candidate_ml_json_records_elapsed_ms_when_available
```

RED: failed because `SampledCandidateMlTrialResult` had no `elapsed_ms` field.

GREEN:

- `SampledCandidateMlTrialResult` now has `elapsed_ms: Option<u128>`.
- Library runners populate `elapsed_ms: None`.
- `lsn_sampled_ambient_ml_sweep --progress` stamps each emitted cell with
  `Some(elapsed.as_millis())`.
- JSON writes a numeric `elapsed_ms` when available and `null` otherwise.

The existing streaming scorer equivalence test was rerun:

```bash
cargo test --manifest-path impl/lsn_cryptanalysis/Cargo.toml \
  --test ml_baseline streaming_candidate_budget_runner_matches_stored_runner
```

## Smoke Artifact

Raw data:

- `experiments/169-codex-p2-ambient-ml-elapsed-json-smoke.json`

Command:

```bash
cargo run --manifest-path impl/lsn_cryptanalysis/Cargo.toml --release \
  --bin lsn_sampled_ambient_ml_sweep -- \
  --n-start 8 --n-end 8 \
  --ratios 0.00390625 \
  --p-values 0.25 \
  --trials 1 \
  --seed 3235823873 \
  --streaming \
  --progress \
  --output experiments/169-codex-p2-ambient-ml-elapsed-json-smoke.json
```

Progress output:

```text
cell done n=8 ratio=0.00390625 p=0.25 successes=0/1 margin=-3.000 elapsed_ms=431
```

Result:

| n | sample count | p | candidate count | successes | avg secret margin | elapsed ms |
|---:|---:|---:|---:|---:|---:|---:|
| 8 | 256 | 0.25 | 65536 | 0/1 | -3.0 | 431 |

This is a schema/instrumentation smoke, not a boundary estimate.

## Reproducibility

Because `elapsed_ms` is wall-clock data, byte-for-byte JSON equality is no
longer the right reproducibility test. The deterministic payload should match
after deleting `elapsed_ms`, and the elapsed field should be present and numeric
in both runs.

Repro command:

```bash
cargo run --manifest-path impl/lsn_cryptanalysis/Cargo.toml --release \
  --bin lsn_sampled_ambient_ml_sweep -- \
  --n-start 8 --n-end 8 \
  --ratios 0.00390625 \
  --p-values 0.25 \
  --trials 1 \
  --seed 3235823873 \
  --streaming \
  --progress \
  --output /tmp/169-codex-p2-ambient-ml-elapsed-json-smoke.repro.json
```

Observed repro progress output:

```text
cell done n=8 ratio=0.00390625 p=0.25 successes=0/1 margin=-3.000 elapsed_ms=423
```

Checks:

```bash
jq -e '.results[] | (.elapsed_ms | type == "number")' \
  experiments/169-codex-p2-ambient-ml-elapsed-json-smoke.json

jq -e '.results[] | (.elapsed_ms | type == "number")' \
  /tmp/169-codex-p2-ambient-ml-elapsed-json-smoke.repro.json

jq -S 'del(.results[].elapsed_ms)' \
  experiments/169-codex-p2-ambient-ml-elapsed-json-smoke.json \
  > /tmp/169-original-no-elapsed.json

jq -S 'del(.results[].elapsed_ms)' \
  /tmp/169-codex-p2-ambient-ml-elapsed-json-smoke.repro.json \
  > /tmp/169-repro-no-elapsed.json

cmp -s /tmp/169-original-no-elapsed.json /tmp/169-repro-no-elapsed.json
```

All checks passed.

## Verification

```bash
cargo test --manifest-path impl/lsn_cryptanalysis/Cargo.toml
jq empty experiments/169-codex-p2-ambient-ml-elapsed-json-smoke.json
git diff --check
```

## Next Step

Use this instrumentation before any longer `n=11`, `samples=65536` boundary
cell. If longer repeats are needed, add per-trial rows or per-trial elapsed
fields instead of relying on one aggregate cell elapsed value.

# CODEX note: P2 ambient ML strict/tie counters

**Date:** 2026-06-11 KST

**Status:** harness instrumentation improvement for sampled/ambient ML boundary
cells. This changes reporting only; it does not change the attack model and does
not retroactively alter prior JSON artifacts. No public recovery, no reduction,
no security claim. `OPEN = LSN`.

## Motivation

The `n=11` full-streaming boundary repeat `172` reported:

```text
successes=2/2, avg_secret_margin=0.0
```

The existing `successes` counter is intentionally non-strict: it counts
`secret_score >= best_false_score`. That preserves the original scorer behavior
but is too coarse at the false-max boundary, where ties can look like full
successes. This increment adds explicit counters:

- `strict_successes`: `secret_score > best_false_score`;
- `tie_successes`: `secret_score == best_false_score`;
- `strict_success_rate` and `tie_success_rate`;
- existing `successes` and `success_rate` remain backward-compatible and
  non-strict.

## RED/GREEN

RED test added first:

```bash
env CARGO_TARGET_DIR=/tmp/lsn-pq-crypt-target \
  cargo test --manifest-path impl/lsn_cryptanalysis/Cargo.toml \
  --test ml_baseline sampled_candidate_ml_json_records_strict_and_tie_success_counts
```

Initial failure:

```text
struct `SampledCandidateMlTrialResult` has no field named `strict_successes`
struct `SampledCandidateMlTrialResult` has no field named `tie_successes`
```

GREEN after implementation:

```text
test sampled_candidate_ml_json_records_strict_and_tie_success_counts ... ok
```

## Implementation

Updated `SampledCandidateMlTrialResult` and all sampled-candidate ML runners:

- direct planted-candidate runner;
- stored budget runner;
- streaming budget runner.

The counters are accumulated per trial alongside the existing margin:

```text
strict if secret_score > best_false_score
tie    if secret_score == best_false_score
legacy success if the existing scorer regards the secret as winning
```

For streaming budget runs this makes the non-strict definition explicit:
`successes` remains `secret_score >= best_false_score`, while `strict_successes`
separates strictly positive margin from ties.

## Smoke Artifact

Raw JSON:

- `experiments/173-codex-p2-ambient-ml-strict-tie-json-smoke.json`

Command:

```bash
env CARGO_TARGET_DIR=/tmp/lsn-pq-crypt-target \
  cargo run --manifest-path impl/lsn_cryptanalysis/Cargo.toml --release \
  --bin lsn_sampled_ambient_ml_sweep -- \
  --n-start 4 --n-end 4 \
  --ratios 0.25 \
  --p-values 0.25 \
  --trials 3 \
  --seed 3235823889 \
  --streaming \
  --progress \
  --output experiments/173-codex-p2-ambient-ml-strict-tie-json-smoke.json
```

Output:

```text
cell done n=4 ratio=0.25 p=0.25 successes=0/3 margin=-4.000 elapsed_ms=1
```

JSON now includes:

```text
strict_successes      = 0
strict_success_rate   = 0.0
tie_successes         = 0
tie_success_rate      = 0.0
```

## Verification

```bash
jq -e '.results[] | has("strict_successes") and has("tie_successes") and has("strict_success_rate") and has("tie_success_rate")' \
  experiments/173-codex-p2-ambient-ml-strict-tie-json-smoke.json

jq empty experiments/173-codex-p2-ambient-ml-strict-tie-json-smoke.json

git diff --check

cargo fmt --manifest-path impl/lsn_cryptanalysis/Cargo.toml -- --check

env CARGO_TARGET_DIR=/tmp/lsn-pq-crypt-target \
  cargo test --manifest-path impl/lsn_cryptanalysis/Cargo.toml
```

All verification commands passed.

## Interpretation

This is not new cryptanalytic evidence. It is a measurement guardrail for future
boundary runs. The immediate benefit is that future `n=11` cells can distinguish:

- strict positive-margin wins;
- tie-level boundary outcomes;
- actual failures.

The prior `172` result should continue to be described as tie-level, because its
average secret score and best false score were equal. Future repeats should use
the new counters before any aggregate trend table is reported.

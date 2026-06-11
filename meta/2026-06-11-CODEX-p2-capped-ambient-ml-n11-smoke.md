# CODEX note: P2 capped ambient-size ML n=11 smoke

Date: 2026-06-11 KST

## Scope

This increment adds and tests a capped-candidate variant of
`lsn_sampled_ambient_ml_sweep`.

Important threat-model boundary:

- Full ambient-size calibration uses `candidate_count = 2^(2n)`.
- This capped smoke uses the ambient sample scale but only a capped candidate
  cloud.
- Therefore this is not evidence for the full `2^(2n)` ambient-size calibration
  and must not be merged into those plots or claims.

The purpose is operational: enable small n=11 smoke tests without accidentally
materializing the full n=11 candidate cloud.

## Implementation

Added:

- `run_sampled_candidate_ambient_ml_trials_with_cap(...)`,
- CLI flag `--candidate-cap <N>`,
- separate JSON experiment label:
  `codex-p2-capped-ambient-size-candidate-ml`.

The ordinary full ambient mode remains unchanged and still uses
`codex-p2-sampled-ambient-size-candidate-ml`.

## TDD

RED tests:

```bash
cargo test --manifest-path impl/lsn_cryptanalysis/Cargo.toml --test ml_baseline capped_ambient_runner_preserves_ambient_samples_but_caps_candidates
cargo test --manifest-path impl/lsn_cryptanalysis/Cargo.toml --bin lsn_sampled_ambient_ml_sweep parse_args_accepts_candidate_cap
```

Expected RED failures:

- missing `run_sampled_candidate_ambient_ml_trials_with_cap`,
- missing `Args.candidate_cap`.

GREEN:

- capped integration test passes and verifies that sample count is still based
  on ambient `2^(2n)`, while `candidate_count` is capped,
- parser accepts `--candidate-cap`.

## Dry-run preflight

Command:

```bash
cargo run --manifest-path impl/lsn_cryptanalysis/Cargo.toml --bin lsn_sampled_ambient_ml_sweep -- \
  --n-start 11 \
  --n-end 11 \
  --ratios 0.015625 \
  --p-values 0.25,0.5 \
  --trials 2 \
  --seed 3235823861 \
  --candidate-cap 4096 \
  --dry-run
```

Observed preflight:

```text
dry-run ambient-ml n=11 ambient_candidate_count=4194304 candidate_count=4096 lagrangian_points=2048 stored_points=8388608
  cell n=11 ratio=0.015625 samples=65536 p=0.25 trials=2 score_pairs=536870912
  cell n=11 ratio=0.015625 samples=65536 p=0.5 trials=2 score_pairs=536870912
```

The cap reduces stored Lagrangian points from the full n=11 dry-run's
`8589934592` to `8388608`, making a small smoke feasible. The score-pair count
is still large enough that this should remain a smoke path, not a broad sweep.

## Smoke artifact

Raw JSON:

- `experiments/164-codex-p2-capped-ambient-ml-n11-smoke.json`

Command:

```bash
cargo run --manifest-path impl/lsn_cryptanalysis/Cargo.toml --release --bin lsn_sampled_ambient_ml_sweep -- \
  --n-start 11 \
  --n-end 11 \
  --ratios 0.015625 \
  --p-values 0.25,0.5 \
  --trials 2 \
  --seed 3235823861 \
  --candidate-cap 4096 \
  --progress \
  --output experiments/164-codex-p2-capped-ambient-ml-n11-smoke.json
```

Repro check:

```bash
cargo run --manifest-path impl/lsn_cryptanalysis/Cargo.toml --release --bin lsn_sampled_ambient_ml_sweep -- \
  --n-start 11 \
  --n-end 11 \
  --ratios 0.015625 \
  --p-values 0.25,0.5 \
  --trials 2 \
  --seed 3235823861 \
  --candidate-cap 4096 \
  --progress \
  --output /tmp/164-codex-p2-capped-ambient-ml-n11-smoke.repro.json
cmp -s experiments/164-codex-p2-capped-ambient-ml-n11-smoke.json /tmp/164-codex-p2-capped-ambient-ml-n11-smoke.repro.json
```

The `cmp` check passed.

## Results

| n | candidate cap | p | samples | trials | successes | rate | avg margin |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 11 | 4096 | 0.25 | 65536 | 2 | 2 | 1.0 | 9.0 |
| 11 | 4096 | 0.50 | 65536 | 2 | 0 | 0.0 | -24.0 |

This is only a smoke. The small trial count and capped candidate cloud make it
unsuitable for any security or full-ambient conclusion.

## Verification

```bash
cmp -s experiments/164-codex-p2-capped-ambient-ml-n11-smoke.json /tmp/164-codex-p2-capped-ambient-ml-n11-smoke.repro.json
jq empty experiments/164-codex-p2-capped-ambient-ml-n11-smoke.json
cargo test --manifest-path impl/lsn_cryptanalysis/Cargo.toml
git diff --check
```

All passed. Full crate verification passed 5 bin parser tests and 25 integration
tests.

## Next useful step

If n=11 exploration remains useful, do not increase the cap blindly. First add
a streaming or batched scorer that avoids storing all candidate rows at once,
or explicitly keep future capped runs in a separate capped-candidate evidence
table.

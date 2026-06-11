# CODEX note: P2 ambient-size ML progress CLI

Date: 2026-06-11 KST

## Scope

This increment adds lightweight cell-level progress and timing output to
`lsn_sampled_ambient_ml_sweep` for future focused n=10/n=11 ambient-size ML
repeats.

No new security evidence is claimed here. The goal is operational: avoid long
silent runs when a single cell may require minutes of candidate-cloud scoring.

## Change

Implemented a value-free `--progress` flag for:

```bash
cargo run --manifest-path impl/lsn_cryptanalysis/Cargo.toml --bin lsn_sampled_ambient_ml_sweep -- \
  --n-start 10 \
  --n-end 10 \
  --ratios 0.03125 \
  --p-values 0.25,0.5 \
  --trials 8 \
  --seed 3235823857 \
  --progress \
  --output /tmp/out.json
```

When enabled, the CLI prints one `cell start` line and one `cell done` line per
`(n, ratio, p)` cell, including:

- `n`,
- ratio,
- rounded sample count,
- noise rate,
- trial count,
- success count,
- average secret margin,
- elapsed milliseconds for that cell.

The JSON output schema is unchanged.

## Verification

RED/GREEN:

```bash
cargo test --manifest-path impl/lsn_cryptanalysis/Cargo.toml --bin lsn_sampled_ambient_ml_sweep parse_args_
```

The RED failure was the expected missing `Args.progress` field. After the
minimal implementation, the focused parser tests passed:

- `parse_args_defaults_progress_off`,
- `parse_args_accepts_value_free_progress_flag`.

Progress/non-progress equivalence smoke:

```bash
cargo run --manifest-path impl/lsn_cryptanalysis/Cargo.toml --bin lsn_sampled_ambient_ml_sweep -- \
  --n-start 2 \
  --n-end 2 \
  --ratios 0.25 \
  --p-values 0.25,0.5 \
  --trials 1 \
  --seed 777 \
  --output /tmp/ambient-progress-off.json

cargo run --manifest-path impl/lsn_cryptanalysis/Cargo.toml --bin lsn_sampled_ambient_ml_sweep -- \
  --n-start 2 \
  --n-end 2 \
  --ratios 0.25 \
  --p-values 0.25,0.5 \
  --trials 1 \
  --seed 777 \
  --progress \
  --output /tmp/ambient-progress-on.json

cmp -s /tmp/ambient-progress-off.json /tmp/ambient-progress-on.json
jq empty /tmp/ambient-progress-off.json /tmp/ambient-progress-on.json
```

Both checks passed. This verifies that `--progress` changes stderr observability
without changing the measured JSON output.

Full crate verification:

```bash
cargo test --manifest-path impl/lsn_cryptanalysis/Cargo.toml
```

Passed: 2 bin parser tests and 24 integration tests.

## Next useful step

Use `--progress` on the next n=10 or n=11 focused cell before deciding whether
to spend more trials. This should make runtime budgeting explicit without
changing the planted-candidate ML threat model or output format.

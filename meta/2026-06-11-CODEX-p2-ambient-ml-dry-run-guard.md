# CODEX note: P2 ambient-size ML dry-run guard

Date: 2026-06-11 KST

## Scope

This increment adds a `--dry-run` preflight mode to
`lsn_sampled_ambient_ml_sweep`.

No new security evidence is claimed here. The goal is operational safety:
before attempting n=11 or broader ambient-size ML cells, the CLI should expose
candidate-cloud size and rough scoring/storage scale without allocating the
candidate cloud or writing an output JSON.

## Change

Implemented a value-free `--dry-run` flag. Unlike normal execution, dry-run mode
does not require `--output`; it prints a per-cell cost sketch and exits before
sampling or scoring.

Example:

```bash
cargo run --manifest-path impl/lsn_cryptanalysis/Cargo.toml --bin lsn_sampled_ambient_ml_sweep -- \
  --n-start 11 \
  --n-end 11 \
  --ratios 0.015625 \
  --p-values 0.25,0.5 \
  --trials 1 \
  --seed 3235823859 \
  --dry-run
```

Observed preflight output:

```text
dry-run ambient-ml n=11 candidate_count=4194304 lagrangian_points=2048 stored_points=8589934592
  cell n=11 ratio=0.015625 samples=65536 p=0.25 trials=1 score_pairs=274877906944
  cell n=11 ratio=0.015625 samples=65536 p=0.5 trials=1 score_pairs=274877906944
```

The key warning is not subtle: full ambient-size n=11 has about `8.59e9`
stored Lagrangian points and about `2.75e11` sample-candidate score pairs per
listed noise cell at this ratio and trial count. That makes a direct n=11
full-ambient run unsafe to launch casually with the current candidate-row
materialization strategy.

## TDD and Verification

RED/GREEN:

```bash
cargo test --manifest-path impl/lsn_cryptanalysis/Cargo.toml --bin lsn_sampled_ambient_ml_sweep parse_args_
```

The RED failure was the expected missing `Args.dry_run` field and the old
required `String` output type. After the minimal implementation, the focused
parser tests passed:

- `parse_args_defaults_progress_off`,
- `parse_args_accepts_value_free_progress_flag`,
- `parse_args_accepts_dry_run_without_output`,
- `parse_args_requires_output_without_dry_run`.

Smoke:

```bash
cargo run --manifest-path impl/lsn_cryptanalysis/Cargo.toml --bin lsn_sampled_ambient_ml_sweep -- \
  --n-start 11 \
  --n-end 11 \
  --ratios 0.015625 \
  --p-values 0.25,0.5 \
  --trials 1 \
  --seed 3235823859 \
  --dry-run
```

This exited successfully without an output file.

Full crate verification:

```bash
cargo test --manifest-path impl/lsn_cryptanalysis/Cargo.toml
```

Passed: 4 bin parser tests and 24 integration tests.

`git diff --check` also passed.

## Interpretation

- Do not treat the absence of n=11 full-ambient data as evidence. It is a
  current-harness cost boundary.
- The dry-run numbers explain why the next useful P2 implementation step should
  be a more memory-conscious sampled-candidate scorer or a capped-candidate
  threat-model variant, not a blind n=11 full-ambient launch.
- This does not change the planted-candidate ML threat model or any security
  claim. It only prevents accidental over-budget runs and makes future runtime
  decisions explicit.

## Next useful step

Add an explicit capped-candidate mode or streaming scorer if n=11 exploration is
still desired. Keep that mode labeled separately from the full `2^(2n)`
ambient-size calibration so that evidence does not drift across threat models.

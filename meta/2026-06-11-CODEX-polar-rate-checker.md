# CODEX note: polar-rate sweep checker

Date: 2026-06-11 KST

## Scope

This is a reproducibility increment for the Track 2 polar-rate sweep rail. It
adds a fixture checker to `polar_rate_sweep` so rate-sweep JSON files can be
regenerated and compared mechanically.

This note does not introduce a new rate recommendation. It is an implementation
and artifact-integrity check only.

## Change

`polar_rate_sweep` now supports:

```text
polar_rate_sweep [args...] --check PATH
```

The command computes the same JSON it would normally write and compares it
byte-for-byte against `PATH`. A mismatch exits nonzero and prints
`rate check failed`.

## New artifact

Smoke fixture:

- `experiments/155-codex-polar-rate-check-smoke.json`

Parameters:

- `N = 128`
- `p = 0.0343`
- `K in {8, 12, 16}`
- `target_log2_half_sum_bound = -40`

Observed smoke behavior:

- `K = 8`: passes the half-sum target
- `K = 12`: passes the half-sum target
- `K = 16`: fails the half-sum target

That gives a compact positive/negative fixture for the checker.

## Legacy artifact check

The existing full sweep
`experiments/148-codex-polar-rate-sweep-n2048.json` is not the current default
profile. It was generated with `--k-end 768`; the current CLI default is
`--k-end 512`.

The legacy artifact verifies with:

```text
polar_rate_sweep --k-end 768 --check experiments/148-codex-polar-rate-sweep-n2048.json
```

Observed best passing rows remain:

- `p = 0.0706`: `max_passing_K = 151`, rate `0.073730`
- `p = 0.0343`: `max_passing_K = 304`, rate `0.148438`

## Verification

Commands run with `CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target`:

```text
cargo test --manifest-path impl/polar_validation/Cargo.toml cli_check -- --nocapture
cargo run --manifest-path impl/polar_validation/Cargo.toml --release --bin polar_rate_sweep -- --n 128 --p-values 0.0343 --k-start 8 --k-end 16 --k-step 4 --target-log2 -40 --check experiments/155-codex-polar-rate-check-smoke.json
cargo run --manifest-path impl/polar_validation/Cargo.toml --release --bin polar_rate_sweep -- --k-end 768 --check experiments/148-codex-polar-rate-sweep-n2048.json
```

Observed result:

- CLI checker tests: `2 passed`
- smoke fixture: verified
- existing n=2048 rate sweep fixture: verified with `--k-end 768`

## Interpretation

This improves reproducibility and records the parameter profile behind the
existing full sweep. It is not a proof-level bound and not a security claim.

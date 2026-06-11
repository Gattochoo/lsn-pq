# CODEX note: P1b polar importance-sampling checker

Date: 2026-06-11 KST

## Scope

This is a reproducibility increment for the P1b polar importance-sampling rail.
It does not introduce a new polar-code claim or parameter recommendation. The
goal is only to make the `polar_importance` JSON artifacts mechanically
checkable by regenerating the selected profile and comparing against a fixture.

## Change

`polar_importance` now supports:

```text
polar_importance [args...] --check PATH
```

The command computes the same JSON it would normally write and compares it
byte-for-byte against `PATH`. A mismatch exits nonzero and prints
`importance check failed`.

## New artifact

Smoke fixture:

- `experiments/154-codex-p1b-polar-importance-check-smoke.json`

Parameters:

- `N = 128`
- `K = 16`
- `target_p = 0.4`
- `proposal_p = 0.4`
- `trials = 5`
- `seed = 5397`
- `list_size = 8`

Since `proposal_p == target_p`, this also keeps a small negative-control style
sanity check for the reweighting path:

- `proposal_errors = 5`
- `weighted_bler_estimate = 1.0`
- `mean_likelihood_ratio = 1.0`
- `effective_sample_size = 5.0`

## Verification

Commands run with `CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target`:

```text
cargo test --manifest-path impl/polar_validation/Cargo.toml cli_check -- --nocapture
cargo run --manifest-path impl/polar_validation/Cargo.toml --release --bin polar_importance -- --n 128 --k 16 --target-p 0.4 --proposal-values 0.4 --trials 5 --seed 5397 --list-size 8 --check experiments/154-codex-p1b-polar-importance-check-smoke.json
cargo run --manifest-path impl/polar_validation/Cargo.toml --release --bin polar_importance -- --check experiments/145-codex-p1b-polar-importance-pilot-n2048.json
```

Observed result:

- CLI checker tests: `2 passed`
- smoke fixture: verified
- existing n=2048 P1b pilot fixture: verified

## Interpretation

This improves artifact reproducibility only. It is not a stronger BLER estimate,
not a proof-level tail bound, and not a production implementation claim.

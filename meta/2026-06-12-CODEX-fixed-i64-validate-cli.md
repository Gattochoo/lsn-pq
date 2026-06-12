# Codex Fixed-I64 Polar Validate CLI

## Scope

This increment adds a small validation harness path for the fixed-i64 SCL rail:
`polar-validate --decoder fixed-i64`.

It is still an implementation/testing harness only. It does not change the
paper, the active decoder verdict, or the constant-time/security/PQ claim
surface.

## RED

Added `cli_writes_fixed_i64_baseline_fixture` in
`impl/polar_validation/tests/polar_validate_cli.rs`.

The first focused run failed because `polar-validate` did not recognize the
`fixed-i64` decoder:

```text
unknown decoder fixed-i64; expected sc, scl, or scl-fast
```

## GREEN

Added a `fixed-i64` decoder branch to `polar-validate` with:

- fixed `--list-size 8` dispatch;
- fixed metric scale `1024.0`;
- supported `N in {128,256,512,2048}`;
- JSON decoder label `scl_l8_fixed_i64_metric_scale_1024`;
- experiment label `codex-p1-rust-scl-fixed-i64-l8-<suite>`.

Also added a runtime-bounded `N=2048,K=256,p=0.5` fixed-i64 negative smoke in
`polar_baseline.rs`. The first run of that smoke passed immediately on the
existing fixed-i64 implementation, so it is a coverage guard rather than a
production-code RED/GREEN driver.

## Verification

Focused:

```text
env CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target cargo test --manifest-path impl/polar_validation/Cargo.toml cli_writes_fixed_i64_baseline_fixture
env CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target cargo test --manifest-path impl/polar_validation/Cargo.toml high_noise_fixed_i64_n2048_smoke_fails_when_channel_is_random
```

## Limits

- `fixed-i64` remains a validation harness path, not a production CT decoder.
- The dispatcher supports `--list-size 8` only.
- No generated-code, assembly, timing, cache, or microarchitectural audit was
  performed here.
- No CT/PQ/security/7th-source claim is implied.

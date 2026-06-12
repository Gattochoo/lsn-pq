# CODEX ct-003 fixed-i64 library dispatch

Status: GREEN, implementation plumbing only.

This increment moves the fixed-i64 L8 validation dispatch out of the
`polar-validate` binary and into `impl/polar_validation` as a shared library
surface:

```rust
pub const FIXED_I64_VALIDATION_METRIC_SCALE: f64 = 1024.0;
pub fn fixed_i64_l8_validation_dispatch(cfg: &SimulationConfig) -> SimulationResult;
```

The CLI now calls the same library dispatch used by tests, instead of carrying
a private duplicate match over supported lengths.

RED/GREEN:

- RED: `fixed_i64_l8_validation_dispatch_matches_generic_simulator` failed to
  compile because `fixed_i64_l8_validation_dispatch` did not exist.
- GREEN: added the library dispatch for `N in {128,256,512,2048}`, using the
  existing `simulate_bsc_scl_fixed_i64::<N,8,16>` rail and the public validation
  metric scale. The focused test confirms the `N=2048` dispatch output matches
  the generic simulator exactly.

Interpretation:

- This reduces drift between the CLI validation path and library-level tests.
- It is a small ct-003 implementation plumbing step toward wiring, not a
  production decoder.
- The active verdict remains `not_constant_time`.
- No production constant-time, security, PQ, or 7th-source claim is made.

Verification:

- `CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target cargo fmt --manifest-path impl/polar_validation/Cargo.toml -- --check`
- `CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target cargo test --manifest-path impl/polar_validation/Cargo.toml fixed_i64_l8_validation_dispatch_matches_generic_simulator`
- `CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target cargo test --manifest-path impl/polar_validation/Cargo.toml`
- `CARGO_TARGET_DIR=/tmp/lsn-pq-lsnref-target cargo test --manifest-path impl/lsn_ref/Cargo.toml`
- `CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target cargo run --manifest-path impl/polar_validation/Cargo.toml --bin polar-validate -- --decoder fixed-i64 --suite n2048 --trials 1 --seed 5397 --check experiments/188-codex-polar-rust-fixed-i64-n2048-smoke.json`
- `git diff --check`

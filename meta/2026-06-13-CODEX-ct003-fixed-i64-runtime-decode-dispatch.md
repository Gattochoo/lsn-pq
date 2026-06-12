# CODEX ct-003 fixed-i64 runtime decode dispatch

Status: GREEN, implementation plumbing only.

This increment adds a runtime L8 fixed-i64 decoder dispatch for supported
validation lengths:

```rust
pub fn decode_scl_fixed_i64_l8_validation(code: &PolarCode, llr: &[f64]) -> Vec<u8>;
pub fn simulate_bsc_scl_fixed_i64_l8_validation(
    n: usize,
    k: usize,
    p: f64,
    trials: usize,
    seed: u64,
) -> SimulationResult;
```

`fixed_i64_l8_validation_dispatch` now calls the runtime validation simulation
wrapper instead of matching directly to generic simulator instantiations. This
keeps the CLI-facing validation path and the future decode-entry wiring path on
the same runtime decode dispatch.

RED/GREEN:

- RED: `fixed_i64_l8_decode_dispatch_matches_generic_decoder` failed to compile
  because `decode_scl_fixed_i64_l8_validation` did not exist.
- GREEN: added the runtime decoder dispatch for `N in {128,256,512,2048}` and
  verified it matches `decode_scl_fixed_i64::<128,8,16>` on a deterministic
  noisy small fixture.

Interpretation:

- This is a ct-003 implementation step toward later `decode_scl` wiring.
- It is not a production decoder and does not change the active verdict.
- The SCL rail remains `not_constant_time`.
- No production constant-time, security, PQ, or 7th-source claim is made.

Verification:

- `CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target cargo test --manifest-path impl/polar_validation/Cargo.toml fixed_i64_l8_decode_dispatch_matches_generic_decoder`
- `CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target cargo fmt --manifest-path impl/polar_validation/Cargo.toml -- --check`
- `CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target cargo test --manifest-path impl/polar_validation/Cargo.toml fixed_i64_l8_validation_dispatch_matches_generic_simulator`
- `CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target cargo test --manifest-path impl/polar_validation/Cargo.toml`
- `CARGO_TARGET_DIR=/tmp/lsn-pq-lsnref-target cargo test --manifest-path impl/lsn_ref/Cargo.toml`
- `CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target cargo run --manifest-path impl/polar_validation/Cargo.toml --bin polar-validate -- --decoder fixed-i64 --suite n2048 --trials 1 --seed 5397 --check experiments/188-codex-polar-rust-fixed-i64-n2048-smoke.json`
- `git diff --check`

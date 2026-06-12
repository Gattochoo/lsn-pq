# CODEX ct-003 fixed-i64 decoded-bit agreement guard

Status: GREEN, correctness guard only.

This increment adds a deterministic noisy-sample agreement check between the
existing variable-shape `decode_scl_fast` rail and the active fixed-i64
validation rail:

```rust
compare_scl_fast_fixed_i64_decoded_bits::<N, L, CHILD_CAP>(...)
```

The helper runs both decoders on exactly the same generated message/noise
samples and counts decoded-bit mismatches, plus each rail's message errors.

RED/GREEN:

- RED: `fixed_i64_decoded_bits_match_fast_scl_on_noisy_samples` failed to
  compile because the agreement helper did not exist.
- GREEN: added `FixedI64DecoderAgreement` and the deterministic comparison
  helper. The focused test passes for `N=128, K=16, L=8, p=0.0706, trials=25`,
  with zero decoded-bit mismatches and matching error counts.

Interpretation:

- This is a ct-003 implementation correctness guard before wiring any fixed-i64
  path into a default decoder.
- It is not a production constant-time claim.
- It does not change the active verdict: the SCL rail remains
  `not_constant_time`.
- Generated-code, timing/leakage, N=2048 BLER equivalence, and inventory
  promotion remain pending.

Verification:

- `CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target cargo fmt --manifest-path impl/polar_validation/Cargo.toml -- --check`
- `CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target cargo test --manifest-path impl/polar_validation/Cargo.toml fixed_i64_decoded_bits_match_fast_scl_on_noisy_samples`
- `CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target cargo test --manifest-path impl/polar_validation/Cargo.toml`
- `CARGO_TARGET_DIR=/tmp/lsn-pq-lsnref-target cargo test --manifest-path impl/lsn_ref/Cargo.toml`
- `CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target cargo run --manifest-path impl/polar_validation/Cargo.toml --bin polar-validate -- --decoder fixed-i64 --suite n2048 --trials 1 --seed 5397 --check experiments/188-codex-polar-rust-fixed-i64-n2048-smoke.json`
- `git diff --check`

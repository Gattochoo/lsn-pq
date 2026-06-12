# CODEX ct-003 fixed-i64 integer LLR recursion

Status: GREEN, implementation step only.

This increment moves the active fixed-i64 validation decoder one layer farther
away from the floating-point reference rail. `decode_scl_fixed_i64` now
quantizes channel LLRs once at the decoder boundary and computes per-path
min-sum bit LLRs through an integer recursion:

```rust
sc_bit_llr_minsum_i64(&quantized_llr, 0, phi, &bits)
```

The path metric rail remains the existing fixed-i64 metric-delta and fixed
top-L rail. This does not replace `decode_scl`, does not close ct-003, and does
not claim production constant-time behavior.

RED/GREEN:

- RED: `fixed_i64_decoder_source_uses_integer_llr_recursion` failed because
  `decode_scl_fixed_i64` still called `sc_bit_llr_minsum(llr, 0, phi, &bits)`.
- GREEN: added integer channel quantization plus `sc_bit_llr_minsum_i64`,
  `f_llr_minsum_i64`, and `g_llr_i64`; the fixed-i64 decoder now uses the
  integer recursion and keeps existing decoded-bit agreement and n2048 smoke
  behavior.

Interpretation:

- This is a ct-003 decoder-body implementation step, not another audit-only
  classifier.
- The remaining rail still needs generated-code/timing audit and broader
  fixed-schedule wiring before any inventory upgrade.
- The active verdict remains `not_constant_time`.
- No production constant-time, security, PQ, or 7th-source claim is made.

Verification:

- `CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target cargo fmt --manifest-path impl/polar_validation/Cargo.toml -- --check`
- `CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target cargo test --manifest-path impl/polar_validation/Cargo.toml fixed_i64_decoder_source_uses_integer_llr_recursion`
- `CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target cargo test --manifest-path impl/polar_validation/Cargo.toml fixed_i64_decoded_bits_match_fast_scl_on_noisy_samples`
- `CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target cargo run --manifest-path impl/polar_validation/Cargo.toml --bin polar-validate -- --decoder fixed-i64 --suite n2048 --trials 1 --seed 5397 --check experiments/188-codex-polar-rust-fixed-i64-n2048-smoke.json`
- `CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target cargo test --manifest-path impl/polar_validation/Cargo.toml`
- `CARGO_TARGET_DIR=/tmp/lsn-pq-lsnref-target cargo test --manifest-path impl/lsn_ref/Cargo.toml`
- `git diff --check`

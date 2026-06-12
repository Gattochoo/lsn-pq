# CODEX ct-003 fixed-i64 LLR scratch buffers

Status: GREEN, implementation step only.

This increment removes the dynamic `Vec<i64>` recursion buffers from the
fixed-i64 min-sum bit-LLR rail. `decode_scl_fixed_i64` now:

- quantizes channel LLRs into a const-size `[i64; N]` buffer;
- allocates const-size `[i64; N]` and `[u8; N]` scratch buffers per public bit
  round;
- passes scratch slices through `sc_bit_llr_minsum_i64` instead of allocating
  `vec![0i64; half]` at each recursion level.

RED/GREEN:

- RED: `fixed_i64_integer_llr_recursion_uses_fixed_scratch_buffers` failed
  because `sc_bit_llr_minsum_i64` still allocated `vec![0i64; half]`.
- GREEN: changed the integer recursion to use caller-owned scratch slices and
  kept fixed-i64 decoded-bit agreement plus n2048 fixture smoke behavior.

Interpretation:

- This is another ct-003 decoder-body implementation step, not an audit-only
  classifier.
- The floating-point reference decoder remains unchanged.
- The active fixed-i64 rail still needs generated-code/timing audit and broader
  fixed-schedule wiring before any inventory upgrade.
- The active verdict remains `not_constant_time`.
- No production constant-time, security, PQ, or 7th-source claim is made.

Verification:

- `CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target cargo fmt --manifest-path impl/polar_validation/Cargo.toml -- --check`
- `CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target cargo test --manifest-path impl/polar_validation/Cargo.toml fixed_i64_integer_llr_recursion_uses_fixed_scratch_buffers`
- `CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target cargo test --manifest-path impl/polar_validation/Cargo.toml fixed_i64_decoded_bits_match_fast_scl_on_noisy_samples`
- `CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target cargo run --manifest-path impl/polar_validation/Cargo.toml --bin polar-validate -- --decoder fixed-i64 --suite n2048 --trials 1 --seed 5397 --check experiments/188-codex-polar-rust-fixed-i64-n2048-smoke.json`
- `CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target cargo test --manifest-path impl/polar_validation/Cargo.toml`
- `CARGO_TARGET_DIR=/tmp/lsn-pq-lsnref-target cargo test --manifest-path impl/lsn_ref/Cargo.toml`
- `git diff --check`

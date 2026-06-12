# CODEX Integer Wrapper Work Counts

Date: 2026-06-12

Scope: polar SCL audit rail only. This does not wire the fixed SCL prototypes into
`decode_scl`, does not change the active decoder verdict, and does not make a
constant-time, security, or 7th-source claim.

## Change

- Added `FixedSclPathBufferIntegerScheduleRun.work_counts` so the non-panicking
  integer schedule wrapper exposes the public fixed work shape it used.
- Valid integer and path domains report the public full-round work count.
- Invalid integer inputs or invalid public path domains return empty paths, sentinel
  `top` entries, and zero-round public work counts.
- Extended the SCL work-shape audit JSON wrapper map with
  `FixedSclPathBufferIntegerScheduleRun.work_counts`.

## RED/GREEN

- RED: `cargo test --manifest-path impl/polar_validation/Cargo.toml fixed_scl_path_buffer_try_integer_round_schedule`
  failed because `FixedSclPathBufferIntegerScheduleRun` had no `work_counts`
  field.
- GREEN: the same focused test passed after adding the wrapper work-count field.
- GREEN: `cargo test --manifest-path impl/polar_validation/Cargo.toml scl_work_shape_audit_records_non_constant_time_surfaces`
  passed after adding the audit map field.

## Verification

- `CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target cargo test --manifest-path impl/polar_validation/Cargo.toml fixed_scl_path_buffer_try_integer_round_schedule`
- `CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target cargo test --manifest-path impl/polar_validation/Cargo.toml scl_work_shape_audit_records_non_constant_time_surfaces`
- `CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target cargo fmt --manifest-path impl/polar_validation/Cargo.toml -- --check`
- `CARGO_TARGET_DIR=/tmp/lsn-pq-lsnref-target cargo fmt --manifest-path impl/lsn_ref/Cargo.toml -- --check`
- `CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target cargo test --manifest-path impl/polar_validation/Cargo.toml`
- `CARGO_TARGET_DIR=/tmp/lsn-pq-lsnref-target cargo test --manifest-path impl/lsn_ref/Cargo.toml`
- `CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target cargo run --manifest-path impl/polar_validation/Cargo.toml --release --bin polar_scl_audit -- --check experiments/186-codex-polar-scl-workshape-audit.json`
- `CARGO_TARGET_DIR=/tmp/lsn-pq-lsnref-target cargo run --manifest-path impl/lsn_ref/Cargo.toml --release --bin lsn_ct_inventory -- --check experiments/182-codex-lsn-ref-ct-inventory.json`
- `CARGO_TARGET_DIR=/tmp/lsn-pq-lsnref-target cargo build --manifest-path impl/lsn_ref/Cargo.toml --release --bin lsn_toy_kat`
- `/tmp/lsn-pq-lsnref-target/release/lsn_toy_kat --profile n2 --check experiments/152-codex-lsn-ref-toy-kat.json`
- `/tmp/lsn-pq-lsnref-target/release/lsn_toy_kat --profile n3-search --check experiments/153-codex-lsn-ref-n3-kat-search.json`
- `/tmp/lsn-pq-lsnref-target/release/lsn_toy_kat --profile n2-noisy --check experiments/180-codex-lsn-ref-n2-noisy-kat.json`
- `/tmp/lsn-pq-lsnref-target/release/lsn_toy_kat --profile n2-paper-r7-divergent --check experiments/181-codex-lsn-ref-n2-paper-r7-divergent-kat.json`
- `/tmp/lsn-pq-lsnref-target/release/lsn_toy_kat --profile n2-paper-r7-public --check experiments/185-codex-lsn-ref-n2-paper-r7-public-kat.json`

## Adjudication

This is an auditability increment, not a decoder claim. SCL remains
`not_constant_time`; SCL rails remain source-level prototypes pending generated-code
and timing/leakage audit.

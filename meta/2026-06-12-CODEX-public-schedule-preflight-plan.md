# CODEX Public Schedule Preflight Plan

Date: 2026-06-12

Scope: polar SCL audit rail only. This does not wire the fixed SCL prototypes into
`decode_scl`, does not change the active decoder verdict, and does not make a
constant-time, security, or 7th-source claim.

## Change

- Added `FixedSclPublicRoundSchedulePlan`, an execution-free public schedule
  preflight record containing:
  - `FixedSclPathBufferScheduleDomainCheck`
  - `FixedSclPublicRoundWorkCounts`
- Added `fixed_scl_public_round_schedule_plan(...)`.
- Valid public schedules report full public work counts.
- Invalid public path domains report zero-round public work counts.
- `try_expand_then_compact_public_rounds` now reuses the preflight plan instead
  of separately recomputing status and work counts.
- The SCL work-shape audit JSON records the new preflight building block.

## RED/GREEN

- RED: `cargo test --manifest-path impl/polar_validation/Cargo.toml fixed_scl_public_round_schedule_plan_reports_status_and_work_counts_without_running`
  failed because the plan type and function did not exist.
- GREEN: the same focused test passed after adding the type and function.
- GREEN: `fixed_scl_path_buffer_try_public_round_schedule` passed after wrapper
  reuse of the preflight plan.
- GREEN: `scl_work_shape_audit_records_non_constant_time_surfaces` passed after
  the audit text update.

## Verification

- `CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target cargo test --manifest-path impl/polar_validation/Cargo.toml fixed_scl_public_round_schedule_plan_reports_status_and_work_counts_without_running`
- `CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target cargo test --manifest-path impl/polar_validation/Cargo.toml fixed_scl_path_buffer_try_public_round_schedule`
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

This is an audit preflight convenience for source-level SCL rails. It executes no
decoder work and makes no production constant-time or security claim. SCL remains
`not_constant_time`.

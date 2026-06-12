# CODEX Dual-Status Wrapper Fields

Date: 2026-06-12

## Scope

This OFA-sized increment clarifies the fixed SCL audit map entry for
`try_expand_then_compact_integer_round_schedule`.

The wrapper reports two independent public failure surfaces:

- path-buffer schedule shape via `public_path_domain_failure_codes`;
- integer schedule inputs via `integer_schedule_domain_failure_codes`.

The audit JSON now names these explicitly as `path_status_field` and
`integer_status_field` instead of a combined status-field string.

## Adjudication Boundary

This is audit schema cleanup only. It does not change the active decoder, which
remains `not_constant_time`, and it makes no constant-time, security, or
7th-source claim.

## RED/GREEN

RED:

- Updated `scl_work_shape_audit_records_non_constant_time_surfaces` to require
  explicit `path_status_field` and `integer_status_field` entries for
  `try_expand_then_compact_integer_round_schedule`.
- Focused test failed because the audit JSON still used a combined
  `status_field`.

GREEN:

- Split the dual-status wrapper map entry in `scl_work_shape_audit_json()`.
- Regenerated `experiments/186-codex-polar-scl-workshape-audit.json`.

## Verification

Focused verification passed:

- `env CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target cargo test --manifest-path impl/polar_validation/Cargo.toml scl_work_shape_audit_records_non_constant_time_surfaces`

Default verification passed:

- `env CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target cargo fmt --manifest-path impl/polar_validation/Cargo.toml -- --check`
- `env CARGO_TARGET_DIR=/tmp/lsn-pq-lsnref-target cargo fmt --manifest-path impl/lsn_ref/Cargo.toml -- --check`
- `env CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target cargo test --manifest-path impl/polar_validation/Cargo.toml`
- `env CARGO_TARGET_DIR=/tmp/lsn-pq-lsnref-target cargo test --manifest-path impl/lsn_ref/Cargo.toml`
- `env CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target cargo run --manifest-path impl/polar_validation/Cargo.toml --release --bin polar_scl_audit -- --check experiments/186-codex-polar-scl-workshape-audit.json`
- `env CARGO_TARGET_DIR=/tmp/lsn-pq-lsnref-target cargo run --manifest-path impl/lsn_ref/Cargo.toml --release --bin lsn_ct_inventory -- --check experiments/182-codex-lsn-ref-ct-inventory.json`
- `/tmp/lsn-pq-lsnref-target/release/lsn_toy_kat --profile n2 --check experiments/152-codex-lsn-ref-toy-kat.json`
- `/tmp/lsn-pq-lsnref-target/release/lsn_toy_kat --profile n3-search --check experiments/153-codex-lsn-ref-n3-kat-search.json`
- `/tmp/lsn-pq-lsnref-target/release/lsn_toy_kat --profile n2-noisy --check experiments/180-codex-lsn-ref-n2-noisy-kat.json`
- `/tmp/lsn-pq-lsnref-target/release/lsn_toy_kat --profile n2-paper-r7-divergent --check experiments/181-codex-lsn-ref-n2-paper-r7-divergent-kat.json`
- `/tmp/lsn-pq-lsnref-target/release/lsn_toy_kat --profile n2-paper-r7-public --check experiments/185-codex-lsn-ref-n2-paper-r7-public-kat.json`

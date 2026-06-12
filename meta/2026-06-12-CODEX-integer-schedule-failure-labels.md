# CODEX Integer Schedule Failure Labels

Date: 2026-06-12

## Scope

This OFA-sized increment makes the audit-only fixed SCL integer schedule
domain checker report a public failure code, matching the existing path-domain
and child-write failure maps.

Added labels:

- `ok`: valid public integer schedule inputs
- `hard_bit`: hard decisions must be public bits
- `magnitude`: integer metric magnitudes must be non-negative

`FixedSclIntegerScheduleDomainCheck` now carries `failure_code`, and
`scl_work_shape_audit_json()` now exposes
`integer_schedule_domain_failure_codes`.

## Adjudication Boundary

This is a source-level audit/prototype rail only. It does not change the active
decoder, which remains `not_constant_time`, and it makes no security,
constant-time, or 7th-source claim.

## RED/GREEN

RED:

- Added `fixed_scl_integer_schedule_domain_failure_labels_cover_public_codes`
  and audit JSON assertions before implementing the constants, label lookup,
  `failure_code` field, or audit table.
- Focused test failed on unresolved imports/missing `failure_code`, as expected.

GREEN:

- Added the public failure-code constants and label table.
- Split invalid integer schedule inputs into `hard_bit` and `magnitude`.
- Regenerated `experiments/186-codex-polar-scl-workshape-audit.json`.

## Verification

Focused verification passed for:

- `fixed_scl_integer_schedule_domain_failure_labels_cover_public_codes`
- `fixed_scl_integer_schedule_domain_check`
- `try_fixed_scl_integer_round_schedule`
- `scl_work_shape_audit_records_non_constant_time_surfaces`

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

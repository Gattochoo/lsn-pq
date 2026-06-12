# CODEX Child-Write Slot Counts

Date: 2026-06-12

Scope: polar SCL audit rail only. This does not wire the fixed SCL prototypes into
`decode_scl`, does not change the active decoder verdict, and does not make a
constant-time, security, or 7th-source claim.

## Change

- Added `FixedSclBinaryChildWriteDomainCheck.child_slots_written` so the
  non-panicking child-write wrapper exposes its public fixed slot-write count.
- Valid child-write domains report two written child slots.
- Invalid parent-slot, destination-capacity, or bit-index domains report zero
  written child slots and skip writes.
- Extended the SCL work-shape audit wrapper map for
  `try_write_binary_children_from` with
  `FixedSclBinaryChildWriteDomainCheck.child_slots_written`.

## RED/GREEN

- RED: `cargo test --manifest-path impl/polar_validation/Cargo.toml fixed_scl_binary_child_write_domain_check`
  failed because `FixedSclBinaryChildWriteDomainCheck` had no
  `child_slots_written` field.
- GREEN: the child-write domain tests passed after adding valid=2 and invalid=0
  slot-count behavior.
- RED: `scl_work_shape_audit_records_non_constant_time_surfaces` failed before
  the audit JSON wrapper map exposed the child-write work-count field.
- GREEN: the audit JSON test passed after adding the field.

## Verification

- `CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target cargo test --manifest-path impl/polar_validation/Cargo.toml fixed_scl_binary_child_write_domain_check`
- `CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target cargo test --manifest-path impl/polar_validation/Cargo.toml fixed_scl_path_buffer_try_writes_binary_children_from_valid_parent`
- `CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target cargo test --manifest-path impl/polar_validation/Cargo.toml fixed_scl_path_buffer_try_write_rejects_invalid_parent_without_writing`
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

This is audit vocabulary alignment for the lowest fixed child-write wrapper. SCL
remains `not_constant_time`; these rails remain source-level prototypes pending
generated-code and timing/leakage audit.

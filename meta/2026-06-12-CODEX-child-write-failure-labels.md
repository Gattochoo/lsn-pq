# CODEX child-write failure labels

Date: 2026-06-12

## Scope

This increment adds a compact public failure-code label table for the fixed SCL
binary child-write domain checker.

The table covers:

- `ok`;
- `parent_slot`;
- `dst_capacity`;
- `bit_index`.

`fixed_scl_child_write_domain_failure_label` exposes the label lookup for audit
and test code. Unknown codes resolve to `unknown`.

## Boundary

This is metadata for the source-level SCL audit rail. It does not change
`decode_scl`, `decode_scl_fast`, child expansion behavior, path scoring, or
active decoding behavior.

The active decoder verdict remains `not_constant_time`. No constant-time,
production, security, or 7th-source claim is made.

## RED/GREEN

RED:

- `fixed_scl_child_write_domain_failure_labels_cover_public_codes` failed
  because the label struct, table, and lookup function were absent.

GREEN:

- the label table covers every public child-write failure code;
- unknown codes map to `unknown`;
- the SCL audit JSON now includes `public_child_write_failure_codes`.

## Verification

Focused verification:

- `cargo test --manifest-path impl/polar_validation/Cargo.toml fixed_scl_child_write_domain_failure_labels_cover_public_codes`
- `cargo test --manifest-path impl/polar_validation/Cargo.toml scl_work_shape_audit_records_non_constant_time_surfaces`

Default verification:

- `cargo fmt --manifest-path impl/polar_validation/Cargo.toml -- --check`
- `cargo fmt --manifest-path impl/lsn_ref/Cargo.toml -- --check`
- `cargo test --manifest-path impl/polar_validation/Cargo.toml`
- `cargo test --manifest-path impl/lsn_ref/Cargo.toml`
- `cargo run --manifest-path impl/polar_validation/Cargo.toml --release --bin polar_scl_audit -- --check experiments/186-codex-polar-scl-workshape-audit.json`
- `cargo run --manifest-path impl/lsn_ref/Cargo.toml --release --bin lsn_ct_inventory -- --check experiments/182-codex-lsn-ref-ct-inventory.json`
- `/tmp/lsn-pq-lsnref-target/release/lsn_toy_kat --profile n2 --check experiments/152-codex-lsn-ref-toy-kat.json`
- `/tmp/lsn-pq-lsnref-target/release/lsn_toy_kat --profile n3-search --check experiments/153-codex-lsn-ref-n3-kat-search.json`
- `/tmp/lsn-pq-lsnref-target/release/lsn_toy_kat --profile n2-noisy --check experiments/180-codex-lsn-ref-n2-noisy-kat.json`
- `/tmp/lsn-pq-lsnref-target/release/lsn_toy_kat --profile n2-paper-r7-divergent --check experiments/181-codex-lsn-ref-n2-paper-r7-divergent-kat.json`
- `/tmp/lsn-pq-lsnref-target/release/lsn_toy_kat --profile n2-paper-r7-public --check experiments/185-codex-lsn-ref-n2-paper-r7-public-kat.json`

## Next Step

The next bounded step is to add an audit table that cross-references each
non-panicking wrapper with the public failure-code family it returns, still
without touching active decoding.

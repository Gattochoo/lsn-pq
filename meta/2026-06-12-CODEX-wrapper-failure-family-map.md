# CODEX wrapper failure-family map

Date: 2026-06-12

## Scope

This increment adds `non_panicking_wrapper_failure_code_map` to the fixed SCL
audit JSON.

The table cross-references each source-level non-panicking wrapper with the
public failure-code family it surfaces:

- `try_write_binary_children_from` -> `public_child_write_failure_codes`;
- `try_expand_then_compact_one_bit` -> `public_path_domain_failure_codes`;
- `try_expand_then_compact_two_public_bits` -> `public_path_domain_failure_codes`;
- `try_expand_then_compact_public_rounds` -> `public_path_domain_failure_codes`;
- `try_expand_then_compact_integer_round_schedule` -> `public_path_domain_failure_codes`
  plus the existing `integer_schedule_domain_check` status.

## Boundary

This is audit metadata only. It does not change `decode_scl`,
`decode_scl_fast`, child writes, path expansion, path scoring, or active decoder
behavior.

The active decoder verdict remains `not_constant_time`. No constant-time,
production, security, or 7th-source claim is made.

## RED/GREEN

RED:

- `scl_work_shape_audit_records_non_constant_time_surfaces` failed because
  `non_panicking_wrapper_failure_code_map` was absent.

GREEN:

- the audit JSON names the wrapper/failure-family map;
- child-write wrappers point at `public_child_write_failure_codes`;
- path-buffer wrappers point at `public_path_domain_failure_codes`;
- the integer wrapper also names `integer_schedule_domain_check`.

## Verification

Focused verification:

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

The next bounded step is to use the map as a checklist for the remaining
panic-only source helpers, or add one targeted wrapper only where it removes a
specific audit gap.

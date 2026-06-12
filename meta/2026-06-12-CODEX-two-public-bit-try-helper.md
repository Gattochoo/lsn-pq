# CODEX two-public-bit try helper

Date: 2026-06-12

## Scope

This increment adds `try_expand_then_compact_two_public_bits`, an audit-only
non-panicking companion to the existing two-public-bit fixed SCL helper.

The wrapper maps the two tuple rounds into `FixedSclRound` values and delegates
to `try_expand_then_compact_public_rounds`, so it inherits the public schedule
domain check and sentinel-output behavior instead of calling the panicking
one-bit expansion rail directly.

## Boundary

This does not change `decode_scl`, `decode_scl_fast`, or any active decoder
path. It only removes one source-level convenience helper from the remaining
panic-only audit surface.

The active decoder verdict remains `not_constant_time`. No constant-time,
production, security, or 7th-source claim is made.

## RED/GREEN

RED:

- `fixed_scl_path_buffer_try_two_public_bits_*` failed because
  `try_expand_then_compact_two_public_bits` was absent.

GREEN:

- valid two-public-bit schedules match the existing panicking helper;
- invalid second-round bit indices return `FIXED_SCL_PATH_DOMAIN_BIT_INDEX`
  with `first_invalid_round = 1`;
- audit JSON names the new wrapper as source-level only and not wired into
  active decoding.

## Verification

Focused verification:

- `cargo test --manifest-path impl/polar_validation/Cargo.toml fixed_scl_path_buffer_try_two_public_bits`
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

The next bounded step is to add a compact public failure-code table to the SCL
audit JSON or continue collapsing tiny panic-only source helpers into explicit
domain-check wrappers, still without touching active decoding.

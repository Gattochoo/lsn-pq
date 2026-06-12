# CODEX path-buffer shape domain check

Date: 2026-06-12

## Scope

This increment adds `fixed_scl_path_buffer_schedule_domain_check`, an
audit-only public shape validator for the fixed SCL path-buffer rail. It checks:

- non-empty public round schedules;
- first expansion child capacity;
- repeated expansion child capacity;
- top-L selector width;
- public bit indices against the path bit width.

`try_expand_then_compact_integer_round_schedule` now returns this path-domain
check alongside the existing integer input-domain check. If either check fails,
the wrapper returns an empty fixed path buffer and sentinel top-L entries without
running path expansion.

## Boundary

This does not change `decode_scl`, `decode_scl_fast`, or any active decoder
path. It only separates invalid public-domain inputs from true invariant
violations in the source-level `ct-003` rail.

The active decoder verdict remains `not_constant_time`. No constant-time,
production, security, or 7th-source claim is made.

## RED/GREEN

RED:

- `fixed_scl_path_buffer_schedule_domain_check_*` failed because the path-domain
  validator and failure-code constants were absent.
- `fixed_scl_path_buffer_try_integer_round_schedule_reports_invalid_bit_index_without_expansion`
  failed because the wrapper did not return a path-domain check or guard
  invalid public bit indices before expansion.

GREEN:

- valid shape inputs report `FIXED_SCL_PATH_DOMAIN_OK`;
- small first-child capacity reports
  `FIXED_SCL_PATH_DOMAIN_FIRST_CHILD_CAPACITY`;
- out-of-width public bit indices report `FIXED_SCL_PATH_DOMAIN_BIT_INDEX` with
  the failing round index;
- invalid path-domain inputs skip expansion without panicking.

## Verification

Focused verification:

- `cargo test --manifest-path impl/polar_validation/Cargo.toml fixed_scl_path_buffer_schedule_domain_check`
- `cargo test --manifest-path impl/polar_validation/Cargo.toml fixed_scl_path_buffer_try_integer_round_schedule`
- `cargo test --manifest-path impl/polar_validation/Cargo.toml scl_work_shape_audit_records_non_constant_time_surfaces`

Default verification passed before commit:

- `cargo fmt --manifest-path impl/polar_validation/Cargo.toml -- --check`
- `cargo fmt --manifest-path impl/lsn_ref/Cargo.toml -- --check`
- `cargo test --manifest-path impl/polar_validation/Cargo.toml`
- `cargo test --manifest-path impl/lsn_ref/Cargo.toml`
- `polar_scl_audit --check experiments/186-codex-polar-scl-workshape-audit.json`
- `lsn_ct_inventory --check experiments/182-codex-lsn-ref-ct-inventory.json`
- `lsn_toy_kat --profile n2 --check experiments/152-codex-lsn-ref-toy-kat.json`
- `lsn_toy_kat --profile n3-search --check experiments/153-codex-lsn-ref-n3-kat-search.json`
- `lsn_toy_kat --profile n2-noisy --check experiments/180-codex-lsn-ref-n2-noisy-kat.json`
- `lsn_toy_kat --profile n2-paper-r7-divergent --check experiments/181-codex-lsn-ref-n2-paper-r7-divergent-kat.json`
- `lsn_toy_kat --profile n2-paper-r7-public --check experiments/185-codex-lsn-ref-n2-paper-r7-public-kat.json`

## Next Step

The next bounded step is to add non-panicking public-domain guards for the lower
single-bit child writer or to record a compact failure-code table in the SCL
audit JSON, still without wiring the rail into active decoding.

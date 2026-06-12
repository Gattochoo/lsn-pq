# CODEX integer round schedule audit

Date: 2026-06-12

## Scope

This increment adds `fixed_scl_integer_round_schedule`, an audit-only helper
for the `ct-003` polar SCL rail. It converts public arrays

- bit indices,
- frozen-bit flags,
- hard-bit decisions,
- integer magnitudes,

into a fixed-size `[FixedSclRound; ROUNDS]` schedule using the previously
introduced `fixed_scl_integer_metric_deltas` primitive.

## Boundary

The helper only builds `FixedSclRound` arrays. It is not wired into
`decode_scl`, `decode_scl_fast`, or any active decoder path. It does not remove
the current floating-point/reference SCL implementation.

The active decoder verdict remains `not_constant_time`. This note makes no
constant-time, production, security, or 7th-source claim.

## RED/GREEN

RED:

- `fixed_scl_integer_round_schedule_maps_public_arrays_to_rounds` initially
  failed because `fixed_scl_integer_round_schedule` was absent.

GREEN:

- the helper maps frozen and non-frozen positions into the expected
  `FixedSclRound` deltas;
- the frozen `1` branch is represented by
  `FIXED_SCL_FORBIDDEN_METRIC_DELTA`;
- the SCL work-shape audit JSON records the helper as audit-only and not wired
  into the decoder.

## Verification

Focused verification:

- `cargo test --manifest-path impl/polar_validation/Cargo.toml fixed_scl_integer_round_schedule_maps_public_arrays_to_rounds`
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

The next bounded step is an integration test that feeds this generated schedule
through `expand_then_compact_public_rounds` on a tiny fixed path buffer. That
still should not wire the rail into `decode_scl`; it should only prove the
schedule and fixed-buffer rail compose at source level.

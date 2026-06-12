# CODEX metric-domain assumptions audit

Date: 2026-06-12

## Scope

This increment pins the metric-domain assumptions for the `ct-003` polar SCL
audit rail inside the machine-checked SCL work-shape audit JSON.

The new `metric_domain_assumptions` section records:

- negative metric deltas are diagnostic-only in source-level rail tests;
- any future active integer SCL rail requires fixed-width non-negative
  penalties before decoder wiring;
- `FIXED_SCL_FORBIDDEN_METRIC_DELTA` must remain a terminal sentinel under
  parent-metric addition.

## Boundary

This is still an audit artifact. It does not wire any fixed-buffer prototype
into `decode_scl`, `decode_scl_fast`, or an active decoder path.

The active decoder verdict remains `not_constant_time`. No constant-time,
production, security, or 7th-source claim is made.

## RED/GREEN

RED:

- `scl_work_shape_audit_records_non_constant_time_surfaces` failed because the
  audit JSON did not contain `metric_domain_assumptions`.

GREEN:

- the audit JSON now records the metric-domain boundary;
- `experiments/186-codex-polar-scl-workshape-audit.json` was regenerated from
  the binary.

## Verification

Focused verification:

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

The next bounded step is a source-level metric-domain validator for generated
integer schedules. It should reject negative magnitudes for active integer SCL
inputs while preserving diagnostic tests that explicitly use signed deltas.

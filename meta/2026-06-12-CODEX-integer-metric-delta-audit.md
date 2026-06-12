# CODEX integer metric delta audit

Date: 2026-06-12

## Scope

This increment adds an audit-only integer metric delta primitive for the
`ct-003` polar SCL rail:

- `FixedSclMetricDeltas`
- `FIXED_SCL_FORBIDDEN_METRIC_DELTA`
- `fixed_scl_integer_metric_deltas`

The primitive maps a public frozen-bit flag, a hard bit, and a non-negative
integer magnitude into branch penalties for bit `0` and bit `1`. It forbids the
`1` branch for frozen positions with an explicit sentinel.

## Boundary

This is a source-level prototype only. It is not wired into `decode_scl` or
`decode_scl_fast`, and it does not replace the active floating-point/reference
decoder. The active decoder verdict remains `not_constant_time`.

No constant-time, production, security, or 7th-source claim is made.

## RED/GREEN

The RED test initially failed because the new API was absent:

- `fixed_scl_integer_metric_deltas_penalize_llr_mismatch`

The GREEN implementation then passed:

- hard bit `0` penalizes bit `1`
- hard bit `1` penalizes bit `0`
- frozen bit forbids the bit `1` branch
- large penalties preserve saturation boundary behavior
- the SCL work-shape audit JSON records the primitive as audit-only

## Verification

Focused verification:

- `cargo test --manifest-path impl/polar_validation/Cargo.toml fixed_scl_integer_metric_deltas_penalize_llr_mismatch`
- `cargo test --manifest-path impl/polar_validation/Cargo.toml fixed_scl_integer_metric_deltas_forbid_frozen_one_branch`
- `cargo test --manifest-path impl/polar_validation/Cargo.toml fixed_scl_integer_metric_deltas_saturate_large_penalty`
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

The next bounded step is to define a fixed-width integer metric domain and a
public schedule for feeding these deltas into the existing expand-then-compact
rail, still without wiring the rail into the active decoder until generated-code
and timing/leakage audits exist.

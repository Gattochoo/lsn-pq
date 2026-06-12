# CODEX integer schedule domain validator

Date: 2026-06-12

## Scope

This increment adds `fixed_scl_integer_schedule_domain_check`, an audit-only
validator for active integer SCL schedule inputs.

It checks:

- hard-bit decisions are bits (`0` or `1`);
- magnitudes are non-negative;
- the first invalid round is reported without panicking.

This separates active integer-schedule input validation from older diagnostic
source-level tests that intentionally use signed metric deltas.

## Boundary

The validator is not wired into `decode_scl`, `decode_scl_fast`, or any active
decoder path. It only strengthens the source-level `ct-003` audit rail.

The active decoder verdict remains `not_constant_time`. No constant-time,
production, security, or 7th-source claim is made.

## RED/GREEN

RED:

- `fixed_scl_integer_schedule_domain_check_accepts_active_inputs` failed
  because the validator API was absent.

GREEN:

- valid hard-bit/non-negative-magnitude schedules return `valid=true`;
- negative magnitudes return `valid=false` with the first invalid round;
- non-bit hard decisions return `valid=false` with the first invalid round;
- the SCL work-shape audit JSON records the validator as audit-only and not
  wired into `decode_scl`.

## Verification

Focused verification:

- `cargo test --manifest-path impl/polar_validation/Cargo.toml fixed_scl_integer_schedule_domain_check_accepts_active_inputs`
- `cargo test --manifest-path impl/polar_validation/Cargo.toml fixed_scl_integer_schedule_domain_check_rejects_negative_magnitude`
- `cargo test --manifest-path impl/polar_validation/Cargo.toml fixed_scl_integer_schedule_domain_check_rejects_non_bit_hard_decision`
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

The next bounded step is to add a non-panicking wrapper that first runs this
domain check before building an integer schedule. That wrapper should remain
audit-only and still must not be wired into the active SCL decoder.

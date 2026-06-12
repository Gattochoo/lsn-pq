# CODEX generated integer schedule composition

Date: 2026-06-12

## Scope

This increment adds `expand_then_compact_integer_round_schedule`, an
audit-only source-level composition helper for the `ct-003` polar SCL rail.
It composes:

- `fixed_scl_integer_metric_deltas`
- `fixed_scl_integer_round_schedule`
- `expand_then_compact_public_rounds`

into one fixed-buffer path expansion loop driven by public integer schedule
arrays.

## Boundary

The helper is not wired into `decode_scl`, `decode_scl_fast`, or any active
decoder path. It does not replace the current floating-point/reference decoder.
The active decoder verdict remains `not_constant_time`.

No constant-time, production, security, or 7th-source claim is made.

## RED/GREEN

RED:

- `fixed_scl_path_buffer_runs_generated_integer_round_schedule` initially
  failed because `FixedSclPathBuffer` had no
  `expand_then_compact_integer_round_schedule` method.

GREEN:

- the helper composes generated integer rounds with the fixed
  expand-then-compact rail;
- a frozen final round forbids the `1` branch through
  `FIXED_SCL_FORBIDDEN_METRIC_DELTA`;
- the SCL work-shape audit JSON records the helper as audit-only and not wired
  into the active decoder.

## Verification

Focused verification:

- `cargo test --manifest-path impl/polar_validation/Cargo.toml fixed_scl_path_buffer_runs_generated_integer_round_schedule`
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

The next bounded step is not to wire this helper into the active decoder.
Instead, audit the remaining gap between this fixed-buffer source-level rail and
a real integer SCL decoder: fixed-width metric scaling, generated-code review,
and timing/leakage measurement hooks.

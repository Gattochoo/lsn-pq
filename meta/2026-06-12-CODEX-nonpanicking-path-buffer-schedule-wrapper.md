# CODEX non-panicking path-buffer schedule wrapper

Date: 2026-06-12

## Scope

This increment adds `try_expand_then_compact_integer_round_schedule`, an
audit-only wrapper around the fixed SCL path-buffer schedule runner. It consumes
the non-panicking integer schedule builder and returns the domain check alongside
the path-buffer result.

For valid public integer inputs, the wrapper runs the same fixed path-buffer
rounds as `expand_then_compact_integer_round_schedule`.

For invalid public integer inputs, the wrapper returns:

- the failed `FixedSclIntegerScheduleDomainCheck`;
- an empty fixed path buffer;
- sentinel top-L entries;
- no path expansion.

## Boundary

The wrapper is not wired into `decode_scl`, `decode_scl_fast`, or any active
decoder path. It only closes the next source-level `ct-003` audit gap between
domain validation and fixed-capacity path-buffer expansion.

The active decoder verdict remains `not_constant_time`. No constant-time,
production, security, or 7th-source claim is made.

## RED/GREEN

RED:

- `fixed_scl_path_buffer_try_integer_round_schedule_matches_valid_schedule`
  failed because `FixedSclPathBufferIntegerScheduleRun` and
  `try_expand_then_compact_integer_round_schedule` were absent.

GREEN:

- valid inputs match the existing generated integer schedule path;
- invalid inputs report `valid=false` and skip expansion without panicking;
- the SCL work-shape audit JSON records the wrapper as audit-only and not wired
  into `decode_scl`.

## Verification

Focused verification:

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

The next bounded step is to audit the remaining panic surfaces in the source-level
SCL rails and separate "invalid public domain" failures from true invariant
violations, without changing active decoder wiring.

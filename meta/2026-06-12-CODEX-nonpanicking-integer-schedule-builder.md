# CODEX non-panicking integer schedule builder

Date: 2026-06-12

## Scope

This increment adds `try_fixed_scl_integer_round_schedule`, an audit-only
builder for active integer SCL schedule inputs. It first runs
`fixed_scl_integer_schedule_domain_check` and only builds `FixedSclRound`
arrays when the input domain is valid.

Invalid inputs return:

- the failed `FixedSclIntegerScheduleDomainCheck`;
- a zeroed placeholder round array;
- no panic.

## Boundary

The builder is not wired into `decode_scl`, `decode_scl_fast`, or any active
decoder path. It only strengthens the source-level `ct-003` audit rail.

The active decoder verdict remains `not_constant_time`. No constant-time,
production, security, or 7th-source claim is made.

## RED/GREEN

RED:

- `try_fixed_scl_integer_round_schedule_builds_valid_rounds` failed because
  the builder API was absent.

GREEN:

- valid inputs return `valid=true` and the expected `FixedSclRound` array;
- invalid inputs return `valid=false` and a zeroed placeholder schedule without
  calling the panicking schedule constructor;
- the SCL work-shape audit JSON records the builder as audit-only and not wired
  into `decode_scl`.

## Verification

Focused verification:

- `cargo test --manifest-path impl/polar_validation/Cargo.toml try_fixed_scl_integer_round_schedule_builds_valid_rounds`
- `cargo test --manifest-path impl/polar_validation/Cargo.toml try_fixed_scl_integer_round_schedule_reports_invalid_without_panicking`
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

The next bounded step is to add an audit-only path-buffer wrapper that consumes
this non-panicking builder result. It should return the domain check and avoid
path expansion when input validation fails.

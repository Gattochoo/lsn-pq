# CODEX child-write domain guard

Date: 2026-06-12

## Scope

This increment adds `fixed_scl_binary_child_write_domain_check`, an audit-only
public-domain validator for the lowest fixed SCL child-write rail. It checks:

- parent slot is inside the source path-buffer capacity;
- destination start has two available child slots;
- public bit index is inside the path bit width.

`try_write_binary_children_from` wraps the existing panicking
`write_binary_children_from`. For valid public inputs it performs the same
fixed-slot write. For invalid public inputs it returns the failed domain check
and leaves the destination path buffer untouched.

## Boundary

This does not change `decode_scl`, `decode_scl_fast`, or any active decoder
path. It only separates invalid public-domain inputs from true invariant
violations in the source-level `ct-003` rail.

The active decoder verdict remains `not_constant_time`. No constant-time,
production, security, or 7th-source claim is made.

## RED/GREEN

RED:

- `fixed_scl_binary_child_write_domain_check_*` failed because the validator,
  failure-code constants, and result struct were absent.
- `fixed_scl_path_buffer_try_write_*` failed because the non-panicking child
  writer wrapper was absent.

GREEN:

- valid child writes match the existing fixed-slot write behavior;
- invalid parent slots return `FIXED_SCL_CHILD_WRITE_DOMAIN_PARENT_SLOT` and do
  not mutate the child buffer;
- invalid destination capacity and bit indices return separate public failure
  codes;
- the SCL work-shape audit JSON records both new source-level building blocks as
  not wired into `decode_scl`.

## Verification

Focused verification:

- `cargo test --manifest-path impl/polar_validation/Cargo.toml fixed_scl_binary_child_write_domain_check`
- `cargo test --manifest-path impl/polar_validation/Cargo.toml fixed_scl_path_buffer_try_write`
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

The next bounded step is to thread `try_write_binary_children_from` into a
source-level non-panicking one-bit expansion helper, still keeping the rail
separate from active decoding.

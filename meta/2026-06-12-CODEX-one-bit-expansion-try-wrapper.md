# CODEX one-bit expansion try wrapper

Date: 2026-06-12

## Scope

This increment adds `try_expand_then_compact_one_bit`, an audit-only
non-panicking wrapper for one-bit fixed SCL expansion. It uses the public
path-buffer schedule domain check and the lower-level
`try_write_binary_children_from` child writer before computing the top-L view.

For valid public inputs it matches `expand_then_compact_one_bit`. For invalid
public shape inputs it returns:

- the failed `FixedSclPathBufferScheduleDomainCheck`;
- an empty child path buffer;
- sentinel top-L entries;
- no child expansion.

## Boundary

This does not change `decode_scl`, `decode_scl_fast`, or any active decoder
path. It only extends the source-level `ct-003` audit rail upward by one layer.

The active decoder verdict remains `not_constant_time`. No constant-time,
production, security, or 7th-source claim is made.

## RED/GREEN

RED:

- `fixed_scl_path_buffer_try_expand_then_compact_one_bit_*` failed because
  `FixedSclOneBitExpansionRun` and `try_expand_then_compact_one_bit` were
  absent.

GREEN:

- valid try expansion matches the existing panicking expansion result;
- invalid child capacity reports
  `FIXED_SCL_PATH_DOMAIN_FIRST_CHILD_CAPACITY`;
- invalid bit index reports `FIXED_SCL_PATH_DOMAIN_BIT_INDEX`;
- invalid public inputs do not expand child paths.

## Verification

Focused verification:

- `cargo test --manifest-path impl/polar_validation/Cargo.toml fixed_scl_path_buffer_try_expand_then_compact_one_bit`
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

The next bounded step is to thread the one-bit try wrapper into a non-panicking
multi-round public schedule runner, still source-level only and not wired into
active decoding.

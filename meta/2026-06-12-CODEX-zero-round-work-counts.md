# CODEX Zero-Round Work Counts

Date: 2026-06-12

## Scope

This OFA-sized increment fixes a work-count audit edge case in the fixed SCL
prototype rail.

`fixed_scl_public_round_work_counts_with_capacities(..., rounds = 0)` now
records zero compare exchanges, zero child-slot writes, and zero compacted-slot
writes. This is the right accounting for audit paths that stop before public
expansion, such as invalid integer schedule inputs.

The capacities remain recorded as public parameters, but no expansion work is
counted when there are no rounds.

## Adjudication Boundary

This is source-level audit/prototype accounting only. It does not change the
active decoder, which remains `not_constant_time`, and it makes no
constant-time, security, or 7th-source claim.

## RED/GREEN

RED:

- Added zero-round expectations to
  `fixed_scl_public_round_work_counts_are_public_parameters`.
- Focused test failed because the helper still counted first-round compare and
  child-write work when `rounds = 0`.

GREEN:

- Gated first-round compare and child-write work by `rounds > 0`.
- Added a `zero_rounds_no_expansion_work` audit fixture example.
- Regenerated `experiments/186-codex-polar-scl-workshape-audit.json`.

## Verification

Focused verification passed:

- `env CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target cargo test --manifest-path impl/polar_validation/Cargo.toml fixed_scl_public_round_work_counts_are_public_parameters`
- `env CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target cargo test --manifest-path impl/polar_validation/Cargo.toml scl_work_shape_audit_records_non_constant_time_surfaces`

Default verification passed:

- `env CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target cargo fmt --manifest-path impl/polar_validation/Cargo.toml -- --check`
- `env CARGO_TARGET_DIR=/tmp/lsn-pq-lsnref-target cargo fmt --manifest-path impl/lsn_ref/Cargo.toml -- --check`
- `env CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target cargo test --manifest-path impl/polar_validation/Cargo.toml`
- `env CARGO_TARGET_DIR=/tmp/lsn-pq-lsnref-target cargo test --manifest-path impl/lsn_ref/Cargo.toml`
- `env CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target cargo run --manifest-path impl/polar_validation/Cargo.toml --release --bin polar_scl_audit -- --check experiments/186-codex-polar-scl-workshape-audit.json`
- `env CARGO_TARGET_DIR=/tmp/lsn-pq-lsnref-target cargo run --manifest-path impl/lsn_ref/Cargo.toml --release --bin lsn_ct_inventory -- --check experiments/182-codex-lsn-ref-ct-inventory.json`
- `/tmp/lsn-pq-lsnref-target/release/lsn_toy_kat --profile n2 --check experiments/152-codex-lsn-ref-toy-kat.json`
- `/tmp/lsn-pq-lsnref-target/release/lsn_toy_kat --profile n3-search --check experiments/153-codex-lsn-ref-n3-kat-search.json`
- `/tmp/lsn-pq-lsnref-target/release/lsn_toy_kat --profile n2-noisy --check experiments/180-codex-lsn-ref-n2-noisy-kat.json`
- `/tmp/lsn-pq-lsnref-target/release/lsn_toy_kat --profile n2-paper-r7-divergent --check experiments/181-codex-lsn-ref-n2-paper-r7-divergent-kat.json`
- `/tmp/lsn-pq-lsnref-target/release/lsn_toy_kat --profile n2-paper-r7-public --check experiments/185-codex-lsn-ref-n2-paper-r7-public-kat.json`

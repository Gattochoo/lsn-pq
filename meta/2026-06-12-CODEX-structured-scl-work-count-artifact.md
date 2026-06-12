# CODEX structured SCL work-count artifact

Date: 2026-06-12

## Scope

This increment follows `2026-06-12-CODEX-public-round-work-count-audit.md`.
It promotes the public fixed-schedule SCL work-count example from an
implementation-only helper into the machine-readable SCL audit JSON artifact.

This remains an audit artifact. It is not wired into `decode_scl`,
`decode_scl_fast`, or any KAT path. It is not a constant-time implementation
or a security claim.

## RED/GREEN

RED tests added:

- extra `scl_work_shape_audit_records_non_constant_time_surfaces` assertions for
  `public_work_count_examples`, `top_l_compare_exchanges`,
  `child_slots_written`, and `compacted_slots_written`.

Initial RED behavior:

- the audit test failed because `scl_work_shape_audit_json()` did not yet
  include the structured `public_work_count_examples` field.

GREEN implementation:

- added a structured `public_work_count_examples` object to
  `scl_work_shape_audit_json()`.
- regenerated `experiments/186-codex-polar-scl-workshape-audit.json`.

## Verification

Commands used `CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target` for
`polar_validation` and `CARGO_TARGET_DIR=/tmp/lsn-pq-lsnref-target` for
`lsn_ref`.

Focused checks:

- `cargo test --manifest-path impl/polar_validation/Cargo.toml scl_work_shape_audit_records_non_constant_time_surfaces`
- `cargo test --manifest-path impl/polar_validation/Cargo.toml fixed_scl_public_round_work_counts_are_public_parameters`

Final verification:

- `cargo fmt --manifest-path impl/polar_validation/Cargo.toml -- --check`
- `cargo fmt --manifest-path impl/lsn_ref/Cargo.toml -- --check`
- `cargo test --manifest-path impl/polar_validation/Cargo.toml`
- `cargo test --manifest-path impl/lsn_ref/Cargo.toml`
- `cargo run --manifest-path impl/polar_validation/Cargo.toml --release --bin polar_scl_audit -- --check experiments/186-codex-polar-scl-workshape-audit.json`
- `cargo run --manifest-path impl/lsn_ref/Cargo.toml --release --bin lsn_ct_inventory -- --check experiments/182-codex-lsn-ref-ct-inventory.json`
- `cargo run --manifest-path impl/lsn_ref/Cargo.toml --release --bin lsn_toy_kat -- --profile n2 --check experiments/152-codex-lsn-ref-toy-kat.json`
- `cargo run --manifest-path impl/lsn_ref/Cargo.toml --release --bin lsn_toy_kat -- --profile n3-search --check experiments/153-codex-lsn-ref-n3-kat-search.json`
- `cargo run --manifest-path impl/lsn_ref/Cargo.toml --release --bin lsn_toy_kat -- --profile n2-noisy --check experiments/180-codex-lsn-ref-n2-noisy-kat.json`
- `cargo run --manifest-path impl/lsn_ref/Cargo.toml --release --bin lsn_toy_kat -- --profile n2-paper-r7-divergent --check experiments/181-codex-lsn-ref-n2-paper-r7-divergent-kat.json`
- `cargo run --manifest-path impl/lsn_ref/Cargo.toml --release --bin lsn_toy_kat -- --profile n2-paper-r7-public --check experiments/185-codex-lsn-ref-n2-paper-r7-public-kat.json`

Result: all checks passed.

## Interpretation

The audit fixture now carries one explicit public count example:

- parent capacity: 2
- child capacity: 4
- list size: 2
- rounds: 3
- compare-exchanges: 18
- child-slot writes: 12
- compacted-slot writes: 6

This makes the fixed-work shape easier to review mechanically. The active SCL
decoder remains `not_constant_time`.

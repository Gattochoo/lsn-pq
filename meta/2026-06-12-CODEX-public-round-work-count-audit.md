# CODEX public-round SCL work-count audit

Date: 2026-06-12

## Scope

This increment follows `2026-06-12-CODEX-public-round-schedule-prototype.md`.
It adds a public-parameter work-count helper for the audit-only fixed SCL
schedule rail. The helper exposes the number of source-level compare-exchanges,
child-slot writes, and compacted-slot writes implied by a fixed public round
schedule.

This is not wired into `decode_scl`, `decode_scl_fast`, or any KAT path. It is
not a constant-time claim; it only makes the fixed-shape accounting more
explicit before any generated-code or timing/leakage review.

## RED/GREEN

RED tests added:

- `fixed_scl_public_round_work_counts_are_public_parameters`
- extra audit assertions that `scl_work_shape_audit_json()` records
  `fixed_scl_public_round_work_counts` and `public work-count audit`.

Initial RED behavior:

- `polar_validation` failed to compile because
  `fixed_scl_public_round_work_counts` did not exist.

GREEN implementation:

- added `FixedSclPublicRoundWorkCounts`.
- added `fixed_scl_public_round_work_counts(parent_capacity, child_capacity,
  list_size, rounds)`.
- updated `scl_work_shape_audit_json()` and regenerated
  `experiments/186-codex-polar-scl-workshape-audit.json`.

## Verification

Commands used `CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target` for
`polar_validation` and `CARGO_TARGET_DIR=/tmp/lsn-pq-lsnref-target` for
`lsn_ref`.

Focused checks:

- `cargo test --manifest-path impl/polar_validation/Cargo.toml fixed_scl_public_round_work_counts_are_public_parameters`
- `cargo test --manifest-path impl/polar_validation/Cargo.toml scl_work_shape_audit_records_non_constant_time_surfaces`

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

The SCL audit rail now records not just the data-shape prototypes but also a
small public work-count model for the fixed round schedule. This helps separate
public fixed work from the still-unresolved constant-time obligations:
integer metrics, masking, generated-code inspection, and timing/leakage audit.

The active decoder verdict remains `not_constant_time`.

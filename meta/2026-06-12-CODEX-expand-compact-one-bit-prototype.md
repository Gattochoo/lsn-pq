# CODEX expand-compact one-bit prototype

Date: 2026-06-12

## Scope

This increment follows `2026-06-12-CODEX-fixed-child-expansion-prototype.md`.
It adds an audit-only one-bit expand-then-compact primitive for the fixed SCL
path buffer.  The primitive expands every fixed parent slot into two child
slots, then returns the fixed top-L view over the child buffer.  It is not wired
into `decode_scl`, `decode_scl_fast`, or any KAT path.  It is a source-level
layout prototype only; generated-code inspection and timing/leakage audit are
still required before any constant-time, production, or security claim.

## RED/GREEN

RED tests added:

- `fixed_scl_path_buffer_expands_then_compacts_one_bit`
- `fixed_scl_path_buffer_expand_then_compact_rejects_small_child_buffer`
- extra audit assertions that `scl_work_shape_audit_json()` records
  `expand_then_compact_one_bit` and `one-bit expand then compact`.

Initial RED behavior:

- `polar_validation` failed to compile because
  `FixedSclPathBuffer::expand_then_compact_one_bit` did not exist.

GREEN implementation:

- added `FixedSclPathBuffer::expand_then_compact_one_bit`.
- the method requires two child slots per parent slot.
- it expands each parent through `write_binary_children_from`.
- it returns both the child buffer and the child buffer's fixed top-L entries.
- updated `scl_work_shape_audit_json()` and regenerated
  `experiments/186-codex-polar-scl-workshape-audit.json`.

## Verification

Commands used `CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target` for
`polar_validation` and `CARGO_TARGET_DIR=/tmp/lsn-pq-lsnref-target` for
`lsn_ref`.

Focused checks:

- `cargo test --manifest-path impl/polar_validation/Cargo.toml fixed_scl_path_buffer_expands_then_compacts_one_bit`
- `cargo test --manifest-path impl/polar_validation/Cargo.toml fixed_scl_path_buffer_expand_then_compact_rejects_small_child_buffer`
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

This combines the fixed child expansion and fixed top-L selector into a single
small primitive, which is the shape needed for one fixed-schedule SCL bit step.
It still does not change the active decoder verdict: the current SCL path
remains `not_constant_time`.

Next useful step: add a tiny audit-only multi-round loop over two public bit
positions, still detached from active decoder/KAT paths, to expose the next
state-shape boundary before any generated-code review.

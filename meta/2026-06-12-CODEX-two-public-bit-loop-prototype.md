# CODEX two-public-bit SCL loop prototype

Date: 2026-06-12

## Scope

This increment follows `2026-06-12-CODEX-expand-compact-one-bit-prototype.md`.
It adds an audit-only two-round public-bit loop for the fixed SCL path buffer.
The loop expands a fixed parent buffer over one public bit position, compacts
the fixed top-L children into the next fixed parent buffer, then repeats once
for a second public bit position.

This remains a source-level workshape prototype. It is not wired into
`decode_scl`, `decode_scl_fast`, or any KAT path. It is not a production
constant-time implementation and makes no security claim.

## RED/GREEN

RED tests added:

- `fixed_scl_path_buffer_expands_then_compacts_two_public_bits`
- extra audit assertions that `scl_work_shape_audit_json()` records
  `expand_then_compact_two_public_bits` and `two-round public-bit loop`.

Initial RED behavior:

- `polar_validation` failed to compile because
  `FixedSclPathBuffer::expand_then_compact_two_public_bits` did not exist.

GREEN implementation:

- added an internal fixed-capacity compaction helper from top-L entries.
- added `FixedSclPathBuffer::expand_then_compact_two_public_bits`.
- the method performs two fixed source-level expand/compact rounds over
  caller-supplied public bit positions and integer metric deltas.
- updated `scl_work_shape_audit_json()` and regenerated
  `experiments/186-codex-polar-scl-workshape-audit.json`.

## Verification

Commands used `CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target` for
`polar_validation` and `CARGO_TARGET_DIR=/tmp/lsn-pq-lsnref-target` for
`lsn_ref`.

Focused checks:

- `cargo test --manifest-path impl/polar_validation/Cargo.toml fixed_scl_path_buffer_expands_then_compacts_two_public_bits`
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

The prototype now exposes the fixed-state shape needed for a tiny multi-round
integer SCL path update: fixed slots, fixed child expansion, fixed top-L view,
and fixed-capacity carry-forward into the next public-bit round.

It still does not change the active decoder verdict: the current SCL path
remains `not_constant_time`. Generated-code inspection, masking details,
integer metric design, and timing/leakage audit are still future work.

Next useful step: write a short fixed-schedule integer SCL design note that
maps each remaining `ct-003` surface to a concrete replacement before wiring
any prototype into an active decoder path.

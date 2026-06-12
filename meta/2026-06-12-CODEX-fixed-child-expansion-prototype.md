# CODEX fixed child expansion prototype

Date: 2026-06-12

## Scope

This increment follows `2026-06-12-CODEX-fixed-scl-path-buffer-prototype.md`.
It adds an audit-only binary child expansion primitive for the fixed SCL path
buffer.  The primitive copies one parent path, writes bit-0 and bit-1 children
to two fixed destination slots, and updates integer metrics by supplied deltas.
It is not wired into `decode_scl`, `decode_scl_fast`, or any KAT path.  It is a
source-level layout prototype only; generated-code inspection and timing/leakage
audit are still required before any constant-time, production, or security
claim.

## RED/GREEN

RED tests added:

- `fixed_scl_path_buffer_writes_binary_children_into_fixed_slots`
- `fixed_scl_path_buffer_rejects_child_slot_overflow`
- extra audit assertions that `scl_work_shape_audit_json()` records
  `write_binary_children_from` and `integer child expansion`.

Initial RED behavior:

- `polar_validation` failed to compile because
  `FixedSclPathBuffer::write_binary_children_from` did not exist.
- the audit test then failed because `write_binary_children_from` was not
  recorded in the audit JSON.

GREEN implementation:

- added `FixedSclPathBuffer::write_binary_children_from`.
- the method validates parent slot, two-slot destination room, and bit index.
- it writes bit-0 and bit-1 children into `dst_start` and `dst_start + 1`.
- it uses integer metric deltas with saturating addition.
- inactive parents clear both destination slots.
- updated `scl_work_shape_audit_json()` and regenerated
  `experiments/186-codex-polar-scl-workshape-audit.json`.

## Verification

Commands used `CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target` for
`polar_validation` and `CARGO_TARGET_DIR=/tmp/lsn-pq-lsnref-target` for
`lsn_ref`.

Focused checks:

- `cargo test --manifest-path impl/polar_validation/Cargo.toml fixed_scl_path_buffer_writes_binary_children_into_fixed_slots`
- `cargo test --manifest-path impl/polar_validation/Cargo.toml fixed_scl_path_buffer_rejects_child_slot_overflow`
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

This is another narrow CT-facing engineering primitive.  It sketches how a
future fixed-schedule SCL implementation can expand candidate paths without
dynamic `Vec<SclPath>` growth.  It does not change the active decoder verdict:
the current SCL path remains `not_constant_time`.

Next useful step: add a small fixed-round "expand then top-L compact" audit
function that combines `write_binary_children_from` with the existing top-L view
for one bit position, still without wiring into the active decoder.

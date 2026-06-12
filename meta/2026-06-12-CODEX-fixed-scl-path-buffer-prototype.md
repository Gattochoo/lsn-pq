# CODEX fixed SCL path buffer prototype

Date: 2026-06-12

## Scope

This increment follows `2026-06-12-CODEX-fixed-topl-selector-prototype.md`.
It adds an audit-only fixed-capacity SCL candidate buffer as the next small
building block for the `ct-003` replacement path.  The buffer is not wired into
`decode_scl`, `decode_scl_fast`, or any KAT path.  It is a source-level layout
prototype only; generated-code inspection and timing/leakage audit are still
required before any constant-time, production, or security claim.

## RED/GREEN

RED tests added:

- `fixed_scl_path_buffer_uses_fixed_capacity_slots_and_top_l_view`
- extra audit assertions that `scl_work_shape_audit_json()` records
  `FixedSclPathBuffer`.

Initial RED behavior:

- `polar_validation` failed to compile because `FixedSclPathBuffer` did not
  exist.

GREEN implementation:

- added `FixedSclCandidate<N>` with `metric`, fixed-width `bits`, and `active`.
- added `FixedSclPathBuffer<CAP, N>` with fixed slot storage.
- added slot operations: `new`, `capacity`, `bit_width`, `active_count`,
  `set_candidate`, `clear_slot`, `bits`, `metric_entries`, and
  `top_l_entries`.
- inactive slots expose `i64::MAX` in the metric view, so the existing fixed
  top-L selector naturally ignores them.
- updated `scl_work_shape_audit_json()` and regenerated
  `experiments/186-codex-polar-scl-workshape-audit.json`.

## Verification

Commands used `CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target` for
`polar_validation` and `CARGO_TARGET_DIR=/tmp/lsn-pq-lsnref-target` for
`lsn_ref`.

Focused checks:

- `cargo test --manifest-path impl/polar_validation/Cargo.toml fixed_scl_path_buffer_uses_fixed_capacity_slots_and_top_l_view`
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

This is another small CT-facing engineering primitive.  It removes one more
dependency on dynamic `Vec<SclPath>`-style thinking in the replacement design,
but it does not change the current decoder verdict: the active SCL path remains
`not_constant_time`.

Next useful step: add an audit-only integer path-expansion primitive that writes
two child candidates into fixed slots, then feed that into the fixed top-L view.

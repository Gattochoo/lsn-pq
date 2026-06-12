# CODEX fixed top-L selector prototype

Date: 2026-06-12

## Scope

This increment follows `2026-06-12-CODEX-polar-scl-workshape-audit.md`.
It adds a tiny fixed-width, integer-metric top-L selector prototype for the
`ct-003` polar SCL replacement path.  The selector is not wired into
`decode_scl`, `decode_scl_fast`, or any KAT path.  It is a source-level
fixed-schedule building block only; generated-code inspection and timing/leakage
audit are still required before any constant-time or production claim.

## RED/GREEN

RED tests added:

- `fixed_schedule_top_l_selects_lowest_metrics_with_stable_ties`
- `fixed_schedule_top_l_rejects_invalid_width`
- extra audit assertions that `scl_work_shape_audit_json()` records
  `fixed_schedule_top_l_i64`, `source-level fixed schedule only`, and
  `not wired into decode_scl`.

Initial RED behavior:

- `polar_validation` failed to compile because `FixedTopLEntry`,
  `fixed_schedule_top_l_i64`, and `fixed_schedule_top_l_compare_count` did not
  exist.

GREEN implementation:

- added `FixedTopLEntry { metric, index }`.
- added `fixed_schedule_top_l_i64<const WIDTH, const L>`.
- added `fixed_schedule_top_l_compare_count(width) = width * (width - 1) / 2`.
- used a fixed nested compare-exchange schedule over all pairs, with metric then
  index tie ordering.
- updated `scl_work_shape_audit_json()` and regenerated
  `experiments/186-codex-polar-scl-workshape-audit.json`.

## Verification

Commands used `CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target` for
`polar_validation` and `CARGO_TARGET_DIR=/tmp/lsn-pq-lsnref-target` for
`lsn_ref`.

- `cargo test --manifest-path impl/polar_validation/Cargo.toml fixed_schedule_top_l_selects_lowest_metrics_with_stable_ties`
- `cargo test --manifest-path impl/polar_validation/Cargo.toml scl_work_shape_audit_records_non_constant_time_surfaces`
- `cargo test --manifest-path impl/polar_validation/Cargo.toml fixed_schedule_top_l_rejects_invalid_width`

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

This is a narrow engineering step on the CT-facing rail.  It gives the polar SCL
replacement plan one small, testable component, but it does not change the
current decoder verdict: the SCL path remains `not_constant_time`.

Next useful step: add an audit-only fixed-capacity path buffer abstraction for
SCL candidates, again without wiring it into the decoder or KAT path.

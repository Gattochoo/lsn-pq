# CODEX forbidden metric sentinel guard

Date: 2026-06-12

## Scope

This increment fixes a source-level audit edge in the `ct-003` polar SCL rail:
`FIXED_SCL_FORBIDDEN_METRIC_DELTA` must remain a terminal sentinel when child
metrics are derived from parent metrics.

The prior `write_binary_children_from` implementation used plain
`saturating_add`. That was safe for non-negative parent metrics, but a negative
parent metric could lower the forbidden sentinel from `i64::MAX` to
`i64::MAX - |parent_metric|`.

## Boundary

The change is still audit-only. It affects the fixed-buffer SCL source-level
rail, not `decode_scl`, `decode_scl_fast`, or any active decoder path.

The active decoder verdict remains `not_constant_time`. No constant-time,
production, security, or 7th-source claim is made.

## RED/GREEN

RED:

- `fixed_scl_forbidden_delta_survives_negative_parent_metric` failed with
  `i64::MAX - 100` for the forbidden child branch.

GREEN:

- `fixed_scl_metric_add` now preserves `FIXED_SCL_FORBIDDEN_METRIC_DELTA`
  regardless of parent metric.
- Existing child expansion and generated integer schedule tests still pass.

## Verification

Focused verification:

- `cargo test --manifest-path impl/polar_validation/Cargo.toml fixed_scl_forbidden_delta_survives_negative_parent_metric`
- `cargo test --manifest-path impl/polar_validation/Cargo.toml fixed_scl_path_buffer_writes_binary_children_into_fixed_slots`
- `cargo test --manifest-path impl/polar_validation/Cargo.toml fixed_scl_path_buffer_runs_generated_integer_round_schedule`

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

The next bounded step is to pin metric-domain assumptions explicitly:
which source-level rail tests permit negative diagnostic deltas, and which
future integer SCL design expects non-negative path penalties only.

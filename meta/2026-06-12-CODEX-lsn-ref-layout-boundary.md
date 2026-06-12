# CODEX lsn_ref layout boundary note

Date: 2026-06-12

## Scope

This increment follows `2026-06-12-CODEX-lsn-ref-diagnostic-boundary.md`.
It tightens the `FixedLagrangian` scaffold by making its reference-only layout
bound explicit in code and in the CT inventory.  This is a toy/KAT boundary, not
a production constant-time claim, not a security claim, and not an L2 claim.

## RED/GREEN

RED tests added:

- `fixed_lagrangian_try_from_points_rejects_out_of_layout_inputs`
  expected a fallible constructor, a public layout bound, and explicit errors for
  oversized `n` and out-of-range points.
- `ct_inventory_marks_current_reference_as_non_production`
  expected the inventory to name the bounded reference layout and
  `LSN_REF_MAX_FIXED_LAGRANGIAN_N`.

Initial RED behavior:

- the first test failed to compile because `FixedLagrangianError`,
  `LSN_REF_MAX_FIXED_LAGRANGIAN_N`, and `try_from_points` did not exist.
- the inventory test failed because the bounded-layout text was absent.

GREEN implementation:

- added `LSN_REF_MAX_FIXED_LAGRANGIAN_N = 8`.
- added `FixedLagrangianError::{NTooLarge, PointOutOfRange}`.
- added `FixedLagrangian::try_from_points`, which rejects `n > 8` before
  allocating and rejects points outside the `2^(2n)` universe.
- preserved `from_points` as the panic-style convenience constructor on top of
  `try_from_points`.
- updated `ct-001` in the CT inventory to record the bounded reference layout.

The regenerated CT inventory fixture is
`experiments/182-codex-lsn-ref-ct-inventory.json` and is 3402 bytes.

## Verification

All commands used `CARGO_TARGET_DIR=/tmp/lsn-pq-lsnref-target`.

- `cargo fmt --manifest-path impl/lsn_ref/Cargo.toml -- --check`
- `cargo test --manifest-path impl/lsn_ref/Cargo.toml`
- `cargo run --manifest-path impl/lsn_ref/Cargo.toml --release --bin lsn_ct_inventory -- --check experiments/182-codex-lsn-ref-ct-inventory.json`
- `cargo run --manifest-path impl/lsn_ref/Cargo.toml --release --bin lsn_toy_kat -- --profile n2 --check experiments/152-codex-lsn-ref-toy-kat.json`
- `cargo run --manifest-path impl/lsn_ref/Cargo.toml --release --bin lsn_toy_kat -- --profile n3-search --check experiments/153-codex-lsn-ref-n3-kat-search.json`
- `cargo run --manifest-path impl/lsn_ref/Cargo.toml --release --bin lsn_toy_kat -- --profile n2-noisy --check experiments/180-codex-lsn-ref-n2-noisy-kat.json`
- `cargo run --manifest-path impl/lsn_ref/Cargo.toml --release --bin lsn_toy_kat -- --profile n2-paper-r7-divergent --check experiments/181-codex-lsn-ref-n2-paper-r7-divergent-kat.json`
- `cargo run --manifest-path impl/lsn_ref/Cargo.toml --release --bin lsn_toy_kat -- --profile n2-paper-r7-public --check experiments/185-codex-lsn-ref-n2-paper-r7-public-kat.json`

Result: all checks passed.

## Interpretation

This removes another ambiguity from the KAT rail: the current bitset scaffold is
now explicitly bounded and cannot silently allocate a much larger reference
layout.  It does not make the implementation constant-time.  The inventory still
marks the rail as `not_constant_time_reference`.

Next useful CT-facing step: isolate the polar SCL decoder surface (`ct-003`) with
a fixed-schedule decoder plan or generated-code audit harness, while preserving
the no-production-claim boundary.

# CODEX public-round SCL schedule prototype

Date: 2026-06-12

## Scope

This increment follows `2026-06-12-CODEX-two-public-bit-loop-prototype.md`.
It adds a small public-round schedule abstraction for the fixed SCL path buffer.
The new schedule repeats the existing audit-only expand/compact shape over a
compile-time number of public bit rounds.

This remains detached from `decode_scl`, `decode_scl_fast`, and all KAT paths.
It is a source-level fixed-shape prototype only. It is not a production
constant-time implementation, not a generated-code audit, and not a security
claim.

## RED/GREEN

RED tests added:

- `fixed_scl_path_buffer_runs_public_round_schedule`
- extra audit assertions that `scl_work_shape_audit_json()` records
  `FixedSclRound`, `expand_then_compact_public_rounds`, and
  `public round schedule`.

Initial RED behavior:

- `polar_validation` failed to compile because `FixedSclRound` and
  `FixedSclPathBuffer::expand_then_compact_public_rounds` did not exist.

GREEN implementation:

- added `FixedSclRound` with public bit index and integer metric deltas.
- added `FixedSclPathBuffer::expand_then_compact_public_rounds`.
- the method performs one first expansion from the caller's parent capacity,
  then repeats fixed-capacity compacted rounds over the public schedule.
- updated `scl_work_shape_audit_json()` and regenerated
  `experiments/186-codex-polar-scl-workshape-audit.json`.

## Verification

Commands used `CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target` for
`polar_validation` and `CARGO_TARGET_DIR=/tmp/lsn-pq-lsnref-target` for
`lsn_ref`.

Focused checks:

- `cargo test --manifest-path impl/polar_validation/Cargo.toml fixed_scl_path_buffer_runs_public_round_schedule`
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

The prototype now has a reusable public schedule boundary: fixed path slots,
fixed child slots, fixed top-L selection, and fixed carry-forward are all
visible over more than two rounds. This is still only a workshape rail for a
future fixed-schedule integer decoder plan.

The active decoder verdict remains `not_constant_time`. Required future work:
integer metric design, secret-masked operations, generated-code inspection,
and timing/leakage audit before any constant-time or production claim.

# CODEX polar SCL work-shape audit boundary

Date: 2026-06-12

## Scope

This increment starts the `ct-003` isolation path after
`2026-06-12-CODEX-lsn-ref-layout-boundary.md`.  It does not replace the polar
SCL decoder and does not claim constant-time behavior, production readiness, or
security.  It creates a machine-readable audit artifact that names the current
variable-shape surfaces and the fixed-schedule requirements for a later decoder
replacement.

## RED/GREEN

RED tests added:

- `scl_work_shape_audit_records_non_constant_time_surfaces` in
  `impl/polar_validation/tests/polar_baseline.rs`.
- `polar_scl_audit_cli_writes_and_checks_exact_json` in
  `impl/polar_validation/tests/polar_scl_audit_cli.rs`.
- extra `ct_inventory_marks_current_reference_as_non_production` assertions in
  `impl/lsn_ref/tests/ct_inventory.rs` requiring the new audit artifact link and
  fixed-schedule plan language.

Initial RED behavior:

- `polar_validation` failed to compile because `scl_work_shape_audit_json` did
  not exist.
- `lsn_ref` CT inventory failed because it did not mention
  `experiments/186-codex-polar-scl-workshape-audit.json`.

GREEN implementation:

- added `scl_work_shape_audit_json()` to `impl/polar_validation/src/lib.rs`.
- added `polar_scl_audit` write/check CLI.
- generated `experiments/186-codex-polar-scl-workshape-audit.json` (1249 bytes).
- linked the audit artifact from `ct-003` in
  `experiments/182-codex-lsn-ref-ct-inventory.json` (3506 bytes).

## Audit Content

The artifact records:

- current verdict: `not_constant_time`.
- no production constant-time claim.
- audited functions: `decode_scl`, `decode_scl_fast`, `scl_decode_node`,
  `prune_paths`.
- variable-shape surfaces: path metric sort, `Vec` growth/truncation,
  frozen-mask/candidate branching, floating-point path metrics, recursive path
  composition.
- fixed-schedule requirements: fixed-list arrays, integer/masked metrics,
  data-oblivious top-L selection, no secret-dependent allocation/sort/truncate
  or branch pruning, generated-code and timing/leakage audit.

## Verification

Commands used `CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target` for
`polar_validation` and `CARGO_TARGET_DIR=/tmp/lsn-pq-lsnref-target` for
`lsn_ref`.

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

This is a boundary-setting step.  It makes the current SCL decoder's
variable-shape work explicit and gives the next CT-facing increment a concrete
target.  The current implementation remains `not_constant_time_reference`.

Next useful step: prototype a tiny fixed-list integer top-L selection network
for a small public list size as a separately-tested building block, without
wire-in to production or KAT paths.

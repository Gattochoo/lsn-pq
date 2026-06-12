# CODEX ct-003 fixed-i64 entrypoint audit

Status: GREEN, audit metadata only.

This OFA-sized increment records `decode_scl_fixed_i64` as an active
fixed-i64 validation entrypoint in the SCL work-shape audit artifact.
It does not change the active adjudication:

- `current_verdict` remains `not_constant_time`.
- `production_constant_time_claim` remains `false`.
- The entrypoint is labelled
  `active_fixed_i64_reference_entrypoint_not_production_ct`.
- Generated-code and timing/leakage audit remain pending before any
  production constant-time claim.

RED/GREEN:

- RED: `polar_scl_audit_cli_writes_and_checks_exact_json` required the
  active fixed-i64 entrypoint fields and failed on the missing
  `active_decoder_entrypoints` metadata.
- GREEN: `scl_work_shape_audit_json()` now includes
  `decode_scl_fixed_i64` in `audited_functions`, adds the explicit
  active entrypoint record, and mirrors it into
  `experiments/186-codex-polar-scl-workshape-audit.json`.

Verification run:

- `CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target cargo run --manifest-path impl/polar_validation/Cargo.toml --release --bin polar_scl_audit -- --output experiments/186-codex-polar-scl-workshape-audit.json`
- `CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target cargo run --manifest-path impl/polar_validation/Cargo.toml --release --bin polar_scl_audit -- --check /tmp/codex-fixed-i64-audit.json`
- `CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target cargo fmt --manifest-path impl/polar_validation/Cargo.toml -- --check`
- `CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target cargo test --manifest-path impl/polar_validation/Cargo.toml polar_scl_audit_cli_writes_and_checks_exact_json`
- `CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target cargo test --manifest-path impl/polar_validation/Cargo.toml`
- `CARGO_TARGET_DIR=/tmp/lsn-pq-lsnref-target cargo test --manifest-path impl/lsn_ref/Cargo.toml`
- `git diff --check`


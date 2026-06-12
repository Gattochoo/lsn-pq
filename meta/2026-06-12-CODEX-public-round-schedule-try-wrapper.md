# CODEX public round schedule try wrapper

Date: 2026-06-12

## Scope

This increment adds `try_expand_then_compact_public_rounds`, an audit-only
non-panicking wrapper for multi-round public fixed SCL schedules. It lifts the
one-bit try expansion rail into the public `FixedSclRound` loop.

For valid public schedules it matches `expand_then_compact_public_rounds`.
For invalid public schedules it returns:

- the failed `FixedSclPathBufferScheduleDomainCheck`;
- an empty compacted fixed path buffer;
- sentinel top-L entries;
- no round expansion.

`try_expand_then_compact_integer_round_schedule` now delegates the valid integer
schedule case through this public schedule try wrapper, so the integer rail
inherits the same public path-domain guard.

## Boundary

This does not change `decode_scl`, `decode_scl_fast`, or any active decoder
path. It only extends the source-level `ct-003` audit rail upward to the
multi-round public schedule layer.

The active decoder verdict remains `not_constant_time`. No constant-time,
production, security, or 7th-source claim is made.

## RED/GREEN

RED:

- `fixed_scl_path_buffer_try_public_round_schedule_*` failed because
  `FixedSclPublicRoundScheduleRun` and `try_expand_then_compact_public_rounds`
  were absent.

GREEN:

- valid public schedules match the existing panicking public schedule runner;
- empty public schedules report `FIXED_SCL_PATH_DOMAIN_EMPTY_SCHEDULE`;
- invalid bit indices report `FIXED_SCL_PATH_DOMAIN_BIT_INDEX` with the failing
  round index;
- integer schedule try tests still pass after delegating through the public try
  runner.

## Verification

Focused verification:

- `cargo test --manifest-path impl/polar_validation/Cargo.toml fixed_scl_path_buffer_try_public_round_schedule`
- `cargo test --manifest-path impl/polar_validation/Cargo.toml fixed_scl_path_buffer_try_integer_round_schedule`
- `cargo test --manifest-path impl/polar_validation/Cargo.toml scl_work_shape_audit_records_non_constant_time_surfaces`

Default verification:

- `cargo fmt --manifest-path impl/polar_validation/Cargo.toml -- --check`
- `cargo fmt --manifest-path impl/lsn_ref/Cargo.toml -- --check`
- `cargo test --manifest-path impl/polar_validation/Cargo.toml`
- `cargo test --manifest-path impl/lsn_ref/Cargo.toml`
- `cargo run --manifest-path impl/polar_validation/Cargo.toml --release --bin polar_scl_audit -- --check experiments/186-codex-polar-scl-workshape-audit.json`
- `cargo run --manifest-path impl/lsn_ref/Cargo.toml --release --bin lsn_ct_inventory -- --check experiments/182-codex-lsn-ref-ct-inventory.json`
- `/tmp/lsn-pq-lsnref-target/release/lsn_toy_kat --profile n2 --check experiments/152-codex-lsn-ref-toy-kat.json`
- `/tmp/lsn-pq-lsnref-target/release/lsn_toy_kat --profile n3-search --check experiments/153-codex-lsn-ref-n3-kat-search.json`
- `/tmp/lsn-pq-lsnref-target/release/lsn_toy_kat --profile n2-noisy --check experiments/180-codex-lsn-ref-n2-noisy-kat.json`
- `/tmp/lsn-pq-lsnref-target/release/lsn_toy_kat --profile n2-paper-r7-divergent --check experiments/181-codex-lsn-ref-n2-paper-r7-divergent-kat.json`
- `/tmp/lsn-pq-lsnref-target/release/lsn_toy_kat --profile n2-paper-r7-public --check experiments/185-codex-lsn-ref-n2-paper-r7-public-kat.json`

## Next Step

The next bounded step is to thread this public schedule try wrapper into the
two-public-bit convenience helper or to add a compact public failure-code table
to the audit JSON, still source-level only and not wired into active decoding.

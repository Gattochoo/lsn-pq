# CODEX CT003 Round Wrapper Zero Select

Date: 2026-06-13

Scope: `impl/polar_validation` fixed-i64 SCL audit rail.

Change:
- Replaced the invalid-schedule early return in
  `try_fixed_scl_integer_round_schedule` with masked zero-round selection.
- Built candidate rounds through the non-panicking
  `try_fixed_scl_integer_metric_deltas` wrapper, avoiding the assert-based
  primitive on invalid public metric inputs.
- Added a source-shape regression test requiring masked `round_slots_written`
  and `select_round` zeroing.

Verification intent:
- This is audit-only source cleanup for fixed-i64 round schedule certificates.
- It does not make the active decoder constant-time.
- It does not support any security, PQ, or 7th-source claim.


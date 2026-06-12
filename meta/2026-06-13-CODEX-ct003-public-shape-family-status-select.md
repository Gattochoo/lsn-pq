# CODEX CT003 Public Shape Family Status Select

Date: 2026-06-13

Scope: `impl/polar_validation` fixed-i64 SCL audit rail.

Change:
- Replaced the direct branch ladder in
  `fixed_scl_public_round_schedule_shape_failure_family` with public
  status-bit masks and `select_u8` failure-family selection.
- Added a source-shape regression test requiring path-domain priority and
  work-shape fallback to be expressed through status selection.

Verification intent:
- This is audit-only source cleanup for fixed-i64 public schedule-shape
  certificates.
- It does not make the active decoder constant-time.
- It does not support any security, PQ, or 7th-source claim.

# CODEX CT003 Integer Shape Family Status Select

Date: 2026-06-13

Scope: `impl/polar_validation` fixed-i64 SCL audit rail.

Change:
- Replaced the direct branch ladder in
  `fixed_scl_integer_schedule_shape_failure_family` with public status-bit
  masks and `select_u8` failure-family selection.
- Added a source-shape regression test requiring the integer-domain,
  path-domain, and work-shape priority to be expressed through status
  selection.

Verification intent:
- This is audit-only source cleanup for fixed-i64 integer schedule-shape
  certificates.
- It does not make the active decoder constant-time.
- It does not support any security, PQ, or 7th-source claim.

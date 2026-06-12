# CODEX CT003 Round Build Plan Status Select

Date: 2026-06-13

Scope: `impl/polar_validation` fixed-i64 SCL audit rail.

Change:
- Replaced the public `domain_check.valid` branch in
  `fixed_scl_integer_round_schedule_build_plan` with `select_usize` status
  selection.
- Added an invalid-plan behavior check and a source-shape regression test for
  masked `round_slots_written` selection.

Verification intent:
- This is audit-only source cleanup for fixed-i64 round schedule plan
  certificates.
- It does not make the active decoder constant-time.
- It does not support any security, PQ, or 7th-source claim.


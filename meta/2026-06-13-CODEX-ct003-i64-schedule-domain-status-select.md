# CODEX CT003 i64 Schedule Domain Status Select

Date: 2026-06-13

Scope: `impl/polar_validation` fixed-i64 SCL audit rail.

Change:
- Replaced the early-return validation in `fixed_scl_integer_schedule_domain_check`
  with status accumulation over all public rounds.
- Preserved the previous adjudication order: first invalid round wins, and an
  invalid hard bit takes precedence over a negative magnitude in the same round.
- Added a source-shape regression test requiring `select_u8`/`select_usize`
  status selection plus a same-round dual-fault behavior check.

Verification intent:
- This is source-level cleanup for the audit-only fixed-i64 prototype surface.
- It does not make the active decoder constant-time.
- It does not support any security, PQ, or 7th-source claim.


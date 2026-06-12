# CODEX CT003 Public Plan Work Count Select

Date: 2026-06-13

Scope: `impl/polar_validation` fixed-i64 SCL audit rail.

Change:
- Replaced the `path_domain_check.valid` work-count branch in
  `fixed_scl_public_round_schedule_plan` with public invalid-mask selection
  between full-round and zero-round work-count certificates.
- Added a source-shape regression test requiring
  `select_public_round_work_counts` for this public schedule-plan path.

Verification intent:
- This is audit-only source cleanup for fixed-i64 public schedule plan
  certificates.
- It does not make the active decoder constant-time.
- It does not support any security, PQ, or 7th-source claim.

# CODEX OFA: Public Schedule Shape Certificate

Date: 2026-06-12

## Scope

- Added `FixedSclPublicRoundScheduleShapePlan`.
- Added `fixed_scl_public_round_schedule_shape_plan`.
- The helper pairs public path-domain status with first/repeated top-L shape preflights and public work counts.
- Invalid path-domain inputs produce a zero-round work-shape plan, matching the existing execution-free schedule preflight boundary.

## Discipline

- Audit-only source-level prototype.
- Not wired into `decode_scl`.
- Active decoder remains `not_constant_time`.
- No constant-time, security, PQ, or 7th-source claim.

## Verification Target

- RED: unresolved new API in the focused schedule-shape certificate test.
- GREEN: valid schedule produces matching top-L/work-count shape; invalid bit index preserves path failure and zeroes public work counts.

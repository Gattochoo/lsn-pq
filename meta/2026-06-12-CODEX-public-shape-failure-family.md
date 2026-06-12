# CODEX OFA: Public Shape Failure Family

Date: 2026-06-12

## Scope

- Added public schedule-shape failure-family constants.
- Added `FixedSclPublicRoundScheduleShapeFailureLabel`.
- Added `FIXED_SCL_PUBLIC_ROUND_SCHEDULE_SHAPE_FAILURE_LABELS`.
- Added `fixed_scl_public_round_schedule_shape_failure_label`.
- Added `fixed_scl_public_round_schedule_shape_failure_family`.
- The classifier reports which public status family fails first for an existing `FixedSclPublicRoundScheduleShapePlan`: `ok`, `path_domain`, or `work_shape`.

## Discipline

- Audit-only source-level classifier.
- Not wired into `decode_scl`.
- Active decoder remains `not_constant_time`.
- No constant-time, security, PQ, or 7th-source claim.

## Verification Target

- RED: unresolved classifier/label APIs in the focused test.
- GREEN: valid, path-domain-invalid, and work-shape-invalid plans map to distinct public failure families.

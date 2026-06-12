# CODEX OFA: Public Round Work-Shape Plan

Date: 2026-06-12

## Scope

- Added `FixedSclPublicRoundWorkShapePlan`.
- Added `fixed_scl_public_round_work_shape_plan`.
- The helper pairs first/repeated top-L selector preflights with public SCL round work counts.
- It takes only public capacities, list size, and round count.

## Discipline

- Audit-only source-level prototype.
- Not wired into `decode_scl`.
- Active decoder remains `not_constant_time`.
- No constant-time, security, PQ, or 7th-source claim.

## Verification Target

- RED: unresolved new API in the focused shape-plan test.
- GREEN: valid/invalid work-shape cases and audit JSON surface.

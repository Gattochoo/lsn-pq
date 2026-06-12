# CODEX OFA: Top-L Selection Preflight

Date: 2026-06-12

Scope:
- Added `FixedScheduleTopLSelectionPlan`.
- Added `fixed_schedule_top_l_selection_plan(width, list_size)`.
- The plan reports public top-L selector shape and compare-exchange count without sorting metrics.

Discipline:
- This is an audit-only/source-level prototype surface.
- It is not wired into `decode_scl`.
- The active decoder remains `not_constant_time`.
- This does not support a security, constant-time, PQ, or 7th-source claim.

Verification target:
- RED: `fixed_schedule_top_l_selection_plan_reports_public_shape_without_sorting` initially failed on missing API.
- GREEN: valid `width >= list_size` plans expose `fixed_schedule_top_l_compare_count(width)`, while invalid plans expose failure code and zero compare exchanges.

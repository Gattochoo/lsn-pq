# CODEX OFA: Integer Schedule Preflight Plan

Date: 2026-06-12

Scope:
- Added `FixedSclIntegerRoundSchedulePlan`, an execution-free preflight for fixed SCL integer schedules.
- The plan reports both integer-domain status and public path-domain status, plus the public work-count shape that would be allowed by those statuses.
- `try_expand_then_compact_integer_round_schedule` now reuses that plan instead of recomputing its own zero/full work-count branch.

Discipline:
- This is an audit-only/source-level prototype surface.
- It is not wired into `decode_scl`.
- The active decoder remains `not_constant_time`.
- This does not support a security, constant-time, PQ, or 7th-source claim.

Verification target:
- RED: `fixed_scl_integer_round_schedule_plan_reports_dual_status_and_work_counts_without_running` initially failed on missing API.
- GREEN: the new plan reports valid/full-work, invalid-integer/zero-work, and invalid-path/zero-work cases without running expansion.

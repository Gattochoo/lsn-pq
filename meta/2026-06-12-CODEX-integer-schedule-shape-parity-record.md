# CODEX OFA: Integer Schedule Shape Parity Record

Date: 2026-06-12

## Scope

- Added `FixedSclIntegerRoundScheduleShapePlan`.
- Added `FixedSclIntegerScheduleShapeParityCheck`.
- Added `fixed_scl_integer_round_schedule_shape_plan`.
- Added `fixed_scl_integer_round_run_shape_certificate`.
- Added `fixed_scl_integer_schedule_shape_parity_check`.
- The helpers compare a run-derived integer schedule-shape certificate with an execution-free integer schedule-shape preflight.
- The comparison is limited to public integer-domain status, public path-domain status, first/repeated top-L selection envelopes, and public work-count envelope.
- Invalid integer-domain inputs zero the work-shape envelope before any active decoder integration.

## Discipline

- Audit-only source-level consistency check.
- Not wired into `decode_scl`.
- Active decoder remains `not_constant_time`.
- No constant-time, security, PQ, or 7th-source claim.

## Verification Target

- RED: unresolved integer schedule-shape preflight/parity APIs in the focused test.
- GREEN: matching run-derived/execution-free shape certificates match; invalid integer-domain preflight reports mismatch against a valid run and carries a zero-round work-shape envelope.

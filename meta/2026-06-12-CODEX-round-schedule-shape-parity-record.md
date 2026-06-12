# CODEX OFA: Round Schedule Shape Parity Record

Date: 2026-06-12

## Scope

- Added `FixedSclRoundScheduleShapeParityCheck`.
- Added `fixed_scl_round_schedule_shape_plan`.
- Added `fixed_scl_round_schedule_shape_plan_certificate`.
- Added `fixed_scl_round_schedule_shape_parity_check`.
- The helpers compare a `FixedSclRound`-derived public schedule-shape plan with an explicit public bit-index shape preflight.
- The comparison is limited to public path-domain status, first/repeated top-L selection envelopes, and public work-count envelope.

## Discipline

- Audit-only source-level consistency check.
- Not wired into `decode_scl`.
- Active decoder remains `not_constant_time`.
- No constant-time, security, PQ, or 7th-source claim.

## Verification Target

- RED: unresolved round schedule-shape certificate/parity APIs in the focused test.
- GREEN: matching round-derived/public shape preflight pair matches; altered public bit-index shape preflight reports mismatch.

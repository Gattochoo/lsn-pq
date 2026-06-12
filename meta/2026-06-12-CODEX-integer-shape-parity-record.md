# CODEX OFA: Integer Shape Parity Record

Date: 2026-06-12

## Scope

- Added `FixedSclIntegerShapeParityCheck`.
- Added `fixed_scl_integer_round_run_plan_certificate`.
- Added `fixed_scl_integer_shape_parity_check`.
- The helpers compare a run-derived integer schedule certificate with the execution-free integer preflight plan.
- The comparison is limited to integer-domain status, public path-domain status, and public work-count envelope.

## Discipline

- Audit-only source-level consistency check.
- Not wired into `decode_scl`.
- Active decoder remains `not_constant_time`.
- No constant-time, security, PQ, or 7th-source claim.

## Verification Target

- RED: unresolved integer certificate/parity APIs in the focused test.
- GREEN: valid run/preflight pair matches; altered public work-count envelope reports mismatch.

# CODEX OFA: One-Bit Shape Parity Record

Date: 2026-06-12

## Scope

- Added `FixedSclOneBitShapeParityCheck`.
- Added `fixed_scl_one_bit_run_plan_certificate`.
- Added `fixed_scl_one_bit_shape_parity_check`.
- The helpers compare a one-bit wrapper run certificate with an execution-free public schedule preflight.
- The comparison is limited to public path-domain status and public work-count envelope.

## Discipline

- Audit-only source-level consistency check.
- Not wired into `decode_scl`.
- Active decoder remains `not_constant_time`.
- No constant-time, security, PQ, or 7th-source claim.

## Verification Target

- RED: unresolved one-bit certificate/parity APIs in the focused test.
- GREEN: valid run/preflight pair matches; altered public work-count envelope reports mismatch.

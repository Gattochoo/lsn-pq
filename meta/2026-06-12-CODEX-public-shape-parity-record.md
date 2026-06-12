# CODEX OFA: Public Shape Parity Record

Date: 2026-06-12

## Scope

- Added `FixedSclPublicRoundShapeParityCheck`.
- Added `fixed_scl_public_round_shape_parity_check`.
- The helper compares a run-derived public shape certificate with an expected execution-free public schedule-shape certificate.
- The record keeps both certificates and a public `matches` bit for audit/debug use.

## Discipline

- Audit-only source-level consistency check.
- Not wired into `decode_scl`.
- Active decoder remains `not_constant_time`.
- No constant-time, security, PQ, or 7th-source claim.

## Verification Target

- RED: unresolved parity function and record in the focused test.
- GREEN: valid run/preflight pair matches; altered public work-count envelope reports mismatch.

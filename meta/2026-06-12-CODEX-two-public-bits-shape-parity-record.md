# CODEX OFA: Two-Public-Bits Shape Parity Record

Date: 2026-06-12

## Scope

- Added `two_public_bits_run_shape_certificate`.
- Added `two_public_bits_shape_parity_check`.
- The helpers provide wrapper-specific names for comparing the two-public-bits run certificate with an execution-free public schedule-shape preflight.
- The comparison reuses the existing public-round shape certificate and parity record.

## Discipline

- Audit-only source-level consistency check.
- Not wired into `decode_scl`.
- Active decoder remains `not_constant_time`.
- No constant-time, security, PQ, or 7th-source claim.

## Verification Target

- RED: unresolved two-public-bits certificate/parity APIs in the focused test.
- GREEN: valid run/preflight pair matches; altered public work-count envelope reports mismatch.

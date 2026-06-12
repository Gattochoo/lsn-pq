# CODEX OFA: Round Schedule Public Parity Record

Date: 2026-06-12

## Scope

- Added `FixedSclRoundSchedulePlanParityCheck`.
- Added `fixed_scl_round_schedule_plan_certificate`.
- Added `fixed_scl_round_schedule_plan_parity_check`.
- The helpers compare a `FixedSclRound`-derived public schedule plan with an explicit public bit-index preflight.
- The comparison is limited to public path-domain status and public work-count envelope.

## Discipline

- Audit-only source-level consistency check.
- Not wired into `decode_scl`.
- Active decoder remains `not_constant_time`.
- No constant-time, security, PQ, or 7th-source claim.

## Verification Target

- RED: unresolved round schedule certificate/parity APIs in the focused test.
- GREEN: matching round-derived/public preflight pair matches; altered public bit-index preflight reports mismatch.

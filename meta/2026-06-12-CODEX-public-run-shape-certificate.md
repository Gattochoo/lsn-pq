# CODEX OFA: Public Run Shape Certificate Adapter

Date: 2026-06-12

## Scope

- Added `fixed_scl_public_round_run_shape_certificate`.
- The helper maps `FixedSclPublicRoundScheduleRun` back to a public schedule-shape certificate.
- It uses only public `path_domain_check` and `work_counts`.
- It does not inspect decoded path contents or top-entry metrics beyond the public run envelope.

## Discipline

- Audit-only source-level adapter.
- Not wired into `decode_scl`.
- Active decoder remains `not_constant_time`.
- No constant-time, security, PQ, or 7th-source claim.

## Verification Target

- RED: unresolved adapter import in the focused public-run parity tests.
- GREEN: valid and invalid public-round runs produce the same certificate as the execution-free schedule-shape preflight.

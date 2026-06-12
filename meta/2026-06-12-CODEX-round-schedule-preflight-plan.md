# CODEX OFA: Round Schedule Preflight Plan

Date: 2026-06-12

Scope:
- Added `fixed_scl_round_schedule_plan`, an execution-free preflight for `[FixedSclRound; ROUNDS]`.
- The helper extracts public `bit_index` fields and delegates to the existing public schedule preflight.
- `try_expand_then_compact_public_rounds` now reuses this helper before running fixed-slot expansion.

Discipline:
- This is an audit-only/source-level prototype surface.
- It is not wired into `decode_scl`.
- It does not change the active decoder verdict: `not_constant_time`.
- It does not support a security, constant-time, PQ, or 7th-source claim.

Verification target:
- RED: `fixed_scl_round_schedule_plan_reads_round_bit_indices_without_expansion` initially failed on missing API.
- GREEN: the helper reports the same path-domain status and public work counts for valid and invalid `FixedSclRound` schedules without running expansion.

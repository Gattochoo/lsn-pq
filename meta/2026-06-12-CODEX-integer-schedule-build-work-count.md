# CODEX OFA: Integer Schedule Build Work Count

Date: 2026-06-12

Scope:
- Added `round_slots_written` to `FixedSclIntegerRoundScheduleBuild`.
- Valid integer schedule builds now report `ROUNDS`; invalid hard-bit or magnitude inputs report `0`.
- The SCL work-shape audit map now records this field for `try_fixed_scl_integer_round_schedule`.

Discipline:
- This is an audit-only/source-level prototype surface.
- It is not wired into `decode_scl`.
- The active decoder remains `not_constant_time`.
- This does not support a security, constant-time, PQ, or 7th-source claim.

Verification target:
- RED: `try_fixed_scl_integer_round_schedule` focused tests initially failed because `round_slots_written` was absent.
- GREEN: valid schedule builds expose public round-slot writes, while invalid builds expose zero writes without constructing active rounds.

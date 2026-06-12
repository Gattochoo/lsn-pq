# CODEX OFA: Child-Write Parity Record

Date: 2026-06-12

## Scope

- Added `FixedSclChildWriteParityCheck`.
- Added `fixed_scl_child_write_parity_check`.
- The helper compares the public domain check returned by `try_write_binary_children_from` with an execution-free child-write preflight.
- The comparison is limited to public parent slot, destination capacity, bit index, validity, failure code, and child-slot work count.

## Discipline

- Audit-only source-level consistency check.
- Not wired into `decode_scl`.
- Active decoder remains `not_constant_time`.
- No constant-time, security, PQ, or 7th-source claim.

## Verification Target

- RED: unresolved child-write parity API in the focused test.
- GREEN: valid wrapper/preflight pair matches; altered public child-slot work count reports mismatch.

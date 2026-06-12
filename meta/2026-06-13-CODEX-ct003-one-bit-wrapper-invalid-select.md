# CODEX CT003 One-Bit Wrapper Invalid Select

Date: 2026-06-13

Scope: `impl/polar_validation` fixed-i64 SCL audit rail.

Change:
- Replaced the early return in `try_expand_then_compact_one_bit` with a fixed
  child-expansion loop followed by public invalid-mask selection of zero-run
  work counts, children, and top entries.
- Added source-shape coverage requiring masked invalid selection rather than a
  direct `path_domain_check.valid` branch.
- Added small select helpers for fixed path buffers, top-entry arrays, and
  public work-count certificates.

Verification intent:
- This is audit-only source cleanup for fixed-i64 one-bit expansion wrappers.
- It does not make the active decoder constant-time.
- It does not support any security, PQ, or 7th-source claim.

# CODEX CT003 Path Domain Status Select

Date: 2026-06-13

Scope: `impl/polar_validation` fixed SCL audit rail.

Change:
- Replaced early-return validation in `fixed_scl_path_buffer_schedule_domain_check`
  with public shape predicates, bit-index status accumulation, and
  `select_u8`/`select_usize` result selection.
- Preserved failure priority: empty schedule, first child capacity, top-L width,
  repeated child capacity, then first invalid bit index.
- Added source-shape tests and dual-fault priority checks for shape-vs-bit and
  top-L-vs-repeated-child failures.

Verification intent:
- This is audit-only source cleanup for fixed SCL preflight certificates.
- It does not make the active decoder constant-time.
- It does not support any security, PQ, or 7th-source claim.


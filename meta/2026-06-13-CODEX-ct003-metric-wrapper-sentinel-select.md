# CODEX CT003 Metric Wrapper Sentinel Select

Date: 2026-06-13

Scope: `impl/polar_validation` fixed-i64 SCL audit rail.

Change:
- Replaced the invalid-input early return in `try_fixed_scl_integer_metric_deltas`
  with masked sentinel selection.
- Preserved non-panicking behavior for invalid hard-bit or negative-magnitude
  public metric inputs.
- Avoided calling the assert-based primitive on invalid inputs by deriving a
  safe magnitude and selecting `FIXED_SCL_FORBIDDEN_METRIC_DELTA` with masks.

Verification intent:
- This is audit-only source cleanup for a non-panicking fixed-i64 wrapper.
- It does not make the active decoder constant-time.
- It does not support any security, PQ, or 7th-source claim.


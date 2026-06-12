# CODEX ct-003: masked fixed-SCL metric add

Date: 2026-06-13

## Scope

Small L2/ct-003 implementation refinement for `impl/polar_validation`.

`fixed_scl_metric_add` now propagates the forbidden sentinel through a masked `select_i64` path instead of an explicit `if parent_metric == i64::MAX || metric_delta == FIXED_SCL_FORBIDDEN_METRIC_DELTA` branch. This keeps the existing saturating integer metric semantics and preserves the fixed child expansion rail used by `decode_scl_fixed_i64`.

## RED/GREEN

- RED: added `fixed_scl_metric_add_source_uses_masked_forbidden_selection`, which failed on the previous branch-shaped sentinel propagation.
- GREEN: replaced the branch with a forbidden-bit mask and `select_i64(forbidden_mask, sum, FIXED_SCL_FORBIDDEN_METRIC_DELTA)`.
- Regression: `fixed_scl_forbidden_delta_survives_negative_parent_metric` still preserves the forbidden sentinel.

## Adjudication

This is a decoder-body implementation step only. It does not make a production constant-time, security, PQ, or 7th-source claim. The active decoder remains `not_constant_time` until the full fixed schedule, memory-access review, generated-code inspection, and platform timing story are closed.

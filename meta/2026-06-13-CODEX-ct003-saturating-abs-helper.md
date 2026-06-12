# CODEX ct-003: fixed-i64 saturating abs helper

Date: 2026-06-13

## Scope

Small L2/ct-003 implementation refinement for `impl/polar_validation`.

`llr_i64_metric_magnitude` still caps integer bit-LLR magnitudes at `i64::MAX / 4`, but its helper now uses `value.saturating_abs()` instead of an explicit `if value == i64::MIN` branch. This keeps the active fixed-i64 decoder's integer LLR, hard-decision, metric-delta, child expansion, and top-L rails unchanged.

## RED/GREEN

- RED: added `fixed_i64_magnitude_uses_saturating_abs_without_min_branch`, which failed while `i64_abs_saturating` special-cased `i64::MIN`.
- GREEN: replaced the explicit min-value branch with `value.saturating_abs()`.
- Regression: `fixed_i64_decoded_bits_match_fast_scl_on_noisy_samples` still matches the fast SCL reference on the focused noisy sample set.

## Adjudication

This is a decoder-body implementation step only. It is not a production constant-time, security, PQ, or 7th-source claim. The active decoder remains `not_constant_time` until the complete fixed schedule, generated-code review, memory-access review, and platform timing story are closed.

# CODEX ct-003: fixed-i64 metric domain status selection

Date: 2026-06-13

## Scope

Small L2/ct-003 implementation refinement for `impl/polar_validation`.

The single-round integer metric domain helper
`fixed_scl_integer_metric_domain_check` now computes hard-bit and magnitude
invalid flags and derives the failure code through `select_u8`. This removes
the explicit early-return branches from the fixed-i64 metric-domain rail while
preserving the existing precedence: invalid hard bits are reported before
negative magnitudes.

## RED/GREEN

- RED: added `fixed_scl_integer_metric_domain_check_uses_status_selection`,
  which failed while the helper used `if hard_bit > 1`, `if magnitude < 0`, and
  early returns.
- GREEN: replaced the early returns with `hard_invalid`, `magnitude_invalid`,
  masks, and `select_u8` status selection.
- Regression: `fixed_scl_integer_metric_domain_check_labels_single_round_inputs`
  and `try_fixed_scl_integer_metric_deltas_reports_invalid_without_panicking`
  still preserve the existing status and failure-code behavior.

## Adjudication

This is a source-level implementation cleanup on the fixed-i64 validation rail.
It is not a production constant-time, security, PQ, or 7th-source claim. The
active decoder remains `not_constant_time` until the complete fixed schedule,
memory-access review, generated-code inspection, and platform timing story are
closed.

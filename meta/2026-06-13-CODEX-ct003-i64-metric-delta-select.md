# CODEX ct-003: fixed-i64 metric delta selection

Date: 2026-06-13

## Scope

Small L2/ct-003 implementation refinement for `impl/polar_validation`.

The fixed integer metric helper `fixed_scl_integer_metric_deltas` now derives
hard-bit and frozen-bit masks, then selects bit-0 and bit-1 metric deltas
through `select_i64`. This removes the explicit source-level hard-bit and
frozen-bit branches from the active fixed-i64 metric-delta rail.

## RED/GREEN

- RED: added `fixed_scl_integer_metric_deltas_use_masked_selects`, which failed
  while the helper used `if hard_bit == 0`, `if frozen_bit`, and
  `else if hard_bit == 1`.
- GREEN: replaced those branches with `hard_bit_mask`, `frozen_mask`, and
  `select_i64` calls.
- Regression: existing metric-delta behavior tests still cover mismatch,
  frozen-one forbidding, large penalties, and invalid-input try-wrapper cases.
- Decoder regression: `fixed_i64_decoded_bits_match_fast_scl_on_noisy_samples`
  still matches the fast SCL reference on the focused noisy sample set.

## Adjudication

This is a decoder-body source-level implementation step only. It is not a
production constant-time, security, PQ, or 7th-source claim. The active decoder
remains `not_constant_time` until the complete fixed schedule, memory-access
review, generated-code inspection, and platform timing story are closed.

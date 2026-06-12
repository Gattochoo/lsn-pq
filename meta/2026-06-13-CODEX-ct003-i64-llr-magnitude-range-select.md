# CODEX ct-003: fixed-i64 LLR magnitude range selection

Date: 2026-06-13

## Scope

Small L2/ct-003 implementation refinement for `impl/polar_validation`.

The fixed-i64 quantization helper `llr_metric_magnitude_i64` now computes the
candidate rounded magnitude and derives `nonfinite` / `too_large` flags before
selecting between the candidate and `i64::MAX / 4` through `select_i64`. This
removes the explicit source-level saturation branch from the fixed-i64 LLR
quantization rail.

## RED/GREEN

- RED: added `fixed_i64_llr_metric_magnitude_uses_range_mask_selection`, which
  failed while `llr_metric_magnitude_i64` used the explicit range branch.
- GREEN: replaced the branch with `cap`, `out_of_range`, `range_mask`, and
  `select_i64(range_mask, candidate, cap)`.
- Regression: `fixed_i64_decoded_bits_match_fast_scl_on_noisy_samples` still
  matches the fast SCL reference on the focused noisy sample set.

## Adjudication

This is a decoder-body source-level implementation step only. It does not make
floating-point quantization a production constant-time interface, and it is not
a security, PQ, or 7th-source claim. The active decoder remains
`not_constant_time` until the complete fixed schedule, memory-access review,
generated-code inspection, and platform timing story are closed.

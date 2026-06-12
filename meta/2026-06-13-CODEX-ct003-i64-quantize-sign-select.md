# CODEX ct-003: fixed-i64 quantize sign selection

Date: 2026-06-13

## Scope

Small L2/ct-003 implementation refinement for `impl/polar_validation`.

The fixed-i64 LLR quantizer `quantize_llr_i64` now computes the non-negative
magnitude once, derives a sign mask from `(llr < 0.0)`, and selects between the
positive and negative signed magnitudes through `select_i64`. This removes the
explicit `if llr < 0.0` source branch from the fixed-i64 quantization rail.

## RED/GREEN

- RED: added `fixed_i64_quantize_llr_uses_sign_mask_selection`, which failed
  while `quantize_llr_i64` used the explicit sign branch.
- GREEN: replaced the branch with `negative`, `sign_mask`, and
  `select_i64(sign_mask, magnitude, magnitude.saturating_neg())`.
- Regression: `fixed_i64_decoded_bits_match_fast_scl_on_noisy_samples` still
  matches the fast SCL reference on the focused noisy sample set.

## Adjudication

This is a decoder-body implementation step only. It does not change the
publication/security status. It is not a production constant-time, security,
PQ, or 7th-source claim. The active decoder remains `not_constant_time` until
the complete fixed schedule, memory-access review, generated-code inspection,
and platform timing story are closed.

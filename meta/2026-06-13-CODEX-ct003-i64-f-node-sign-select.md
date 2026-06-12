# CODEX ct-003: fixed-i64 f-node sign selection

Date: 2026-06-13

## Scope

Small L2/ct-003 implementation refinement for `impl/polar_validation`.

The active integer min-sum f-node `f_llr_minsum_i64` now derives the output sign from `i64_negative_flag(a) ^ i64_negative_flag(b)` and selects between `min_abs` and `min_abs.saturating_neg()` through `select_i64`. This removes the explicit `if (a < 0) ^ (b < 0)` branch from the fixed-i64 LLR recursion rail.

## RED/GREEN

- RED: added `fixed_i64_minsum_f_uses_sign_flag_selection`, which failed while `f_llr_minsum_i64` used the explicit sign branch.
- GREEN: replaced the sign branch with a sign-bit flag, all-ones mask, and `select_i64`.
- Regression: `fixed_i64_decoded_bits_match_fast_scl_on_noisy_samples` still matches the fast SCL reference on the focused noisy sample set.

## Adjudication

This is a decoder-body implementation step only. It is not a production constant-time, security, PQ, or 7th-source claim. The active decoder remains `not_constant_time` until the complete fixed schedule, memory-access review, generated-code inspection, and platform timing story are closed.

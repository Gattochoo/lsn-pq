# CODEX ct-003: fixed-i64 sign-bit hard decision

Date: 2026-06-13

## Scope

Small L2/ct-003 implementation refinement for `impl/polar_validation`.

`decode_scl_fixed_i64` now derives the hard decision from the integer bit-LLR sign bit through `i64_negative_flag(bit_llr)` instead of `u8::from(bit_llr < 0)`. This keeps the existing min-sum integer LLR recursion, integer metric-delta rail, fixed child expansion, and top-L compact rail intact.

## RED/GREEN

- RED: added `fixed_i64_decoder_uses_sign_bit_hard_decision`, which failed while the active fixed-i64 decoder used `u8::from(bit_llr < 0)`.
- GREEN: added `i64_negative_flag(value)` using `((value as u64) >> 63) as u8` and wired it into `decode_scl_fixed_i64`.
- Regression: `fixed_i64_decoded_bits_match_fast_scl_on_noisy_samples` still matches the fast SCL reference on the focused noisy sample set.

## Adjudication

This is a decoder-body implementation step only. It is not a production constant-time, security, PQ, or 7th-source claim. The active decoder remains `not_constant_time` until the full fixed schedule, memory-access review, generated-code inspection, and platform timing story are closed.

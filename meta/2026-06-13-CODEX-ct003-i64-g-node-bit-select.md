# CODEX ct-003: fixed-i64 g-node bit selection

Date: 2026-06-13

## Scope

Small L2/ct-003 implementation refinement for `impl/polar_validation`.

The active integer min-sum g-node `g_llr_i64` now computes both `b + a` and
`b - a` with saturating arithmetic, then uses `u & 1` to derive an all-ones
mask and select through `select_i64`. This removes the explicit `if u == 0`
branch from the fixed-i64 LLR recursion rail.

## RED/GREEN

- RED: added `fixed_i64_g_node_uses_bit_mask_selection`, which failed while
  `g_llr_i64` used the explicit bit branch.
- GREEN: replaced the branch with `bit`, `bit_mask`, and
  `select_i64(bit_mask, add, sub)`.
- Regression: `fixed_i64_decoded_bits_match_fast_scl_on_noisy_samples` still
  matches the fast SCL reference on the focused noisy sample set.

## Adjudication

This is a decoder-body implementation step only. It is not a production
constant-time, security, PQ, or 7th-source claim. The active decoder remains
`not_constant_time` until the complete fixed schedule, memory-access review,
generated-code inspection, and platform timing story are closed.

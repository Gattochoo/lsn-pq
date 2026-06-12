# CODEX ct-001 exact point-count hardening

Date: 2026-06-12

Scope: `impl/lsn_ref` toy/reference Lagrangian membership scaffold.

## Change

`FixedLagrangian::try_from_points` now rejects inputs whose point count is not the
public Lagrangian size `2^n` before constructing the membership bitset. This keeps
the bounded toy construction from iterating over an arbitrary caller-provided
secret-length slice.

## RED/GREEN

RED: added `fixed_lagrangian_try_from_points_rejects_out_of_layout_inputs`
coverage for `PointCountMismatch`; it failed because `FixedLagrangianError` had
no such variant.

GREEN: added `PointCountMismatch` and enforced the exact point count after the
public `n <= LSN_REF_MAX_FIXED_LAGRANGIAN_N` guard and before point range scans.

## Adjudication

This is a real `ct-001` hardening step, not a production constant-time claim.
The inventory remains `not_constant_time_reference` because the bounded toy
layout, diagnostic selectors, generated-code review, and independent leakage
audit are still open.

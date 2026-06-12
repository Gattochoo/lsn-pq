# CODEX ct-001 public sample fixed boundary

Date: 2026-06-12

Scope: `impl/lsn_ref` public sample label generation in the toy/reference KAT
rail.

## Change

Changed `public_samples` to accept a `&FixedLagrangian` instead of a raw
`&Lagrangian`. The caller constructs the fixed layout once and then uses that
same boundary for public labels, clean labels, wrong-secret labels, and
diagnostic masks.

## RED/GREEN

RED: added `toy_public_sample_source_takes_fixed_lagrangian_boundary`, which
requires the public-sample generator to take a `FixedLagrangian` boundary and
rejects the old raw `Lagrangian` signature.

GREEN: updated the call site and function signature while keeping public label
generation byte-compatible through `contains_u8 -> contains_mask`.

## Adjudication

This is another source-level `ct-001` hardening increment. It does not close
`ct-001` and does not make a production constant-time or security claim; the
inventory remains `not_constant_time_reference`.

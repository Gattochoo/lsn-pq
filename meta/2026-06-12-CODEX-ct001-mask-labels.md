# CODEX ct-001 mask-derived toy labels

Date: 2026-06-12

Scope: `impl/lsn_ref` toy/reference Lagrangian membership scaffold.

## Change

Removed the `contains_u8_scanned` API and routed toy membership label generation
through `contains_u8`, which is a thin conversion from `contains_mask`.

This keeps one public membership-label path over the masked lookup surface and
removes the older scanned-u8 helper from the implementation.

## RED/GREEN

RED: extended `fixed_lagrangian_source_avoids_secret_dependent_word_indexing` to
reject `contains_u8_scanned` in the reference implementation source; it failed
against the previous implementation.

GREEN: removed the helper, updated toy label generation and tests, and kept
membership/KAT behavior compatible.

## Adjudication

This is another `ct-001` source-level hardening step, not a production
constant-time claim. The inventory remains `not_constant_time_reference` because
the scaffold is still bounded to toy `n <= 8`, diagnostic selector surfaces are
non-production, and generated-code/timing leakage audit remains open.

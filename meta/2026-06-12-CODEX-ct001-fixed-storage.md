# CODEX ct-001 fixed storage hardening

Date: 2026-06-12

Scope: `impl/lsn_ref` toy/reference Lagrangian membership scaffold.

## Change

`FixedLagrangian` now uses a fixed max-word backing array for the bounded toy
layout (`LSN_REF_FIXED_LAGRANGIAN_WORDS = 1024`) instead of storing the active
membership words in a public-`n` sized `Vec<u64>`.

The public active shape is still exposed by `word_count()`, while
`storage_word_count()` records the fixed backing layout used by the toy
membership scaffold.

## RED/GREEN

RED: added `fixed_lagrangian_uses_fixed_max_word_storage`; it failed because the
crate had no `LSN_REF_FIXED_LAGRANGIAN_WORDS` export and no
`storage_word_count()` method.

GREEN: added the fixed backing array, preserved the active public word count,
and kept scanned membership behavior byte-compatible with the existing KATs.

## Adjudication

This removes another `ct-001` scaffold gap, but it is not a production
constant-time claim. The inventory remains `not_constant_time_reference` because
the layout is still bounded to toy `n <= 8`, diagnostic selectors remain
non-production, and independent generated-code/timing leakage audit is still
open.

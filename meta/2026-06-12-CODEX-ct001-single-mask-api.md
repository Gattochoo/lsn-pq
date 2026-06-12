# CODEX ct-001 single mask membership API

Date: 2026-06-12

Scope: `impl/lsn_ref` fixed Lagrangian toy/reference membership scaffold.

## Change

Collapsed the fixed Lagrangian membership surface to one public masked lookup
path: `FixedLagrangian::contains_mask`. Toy labels now derive from
`contains_u8`, which delegates to `contains_mask`, and the diagnostic
wrong-secret mask boundary uses the same path.

The old `contains_mask_scanned` helper was removed so future audits only need to
inspect one masked membership API.

## RED/GREEN

RED: tightened `fixed_lagrangian_source_avoids_secret_dependent_word_indexing`
to reject any `contains_mask_scanned` source symbol. The focused test failed
against the previous split-helper implementation.

GREEN: moved the full fixed-storage scan into `contains_mask`, updated the
diagnostic mask boundary to call it, and kept the word-boundary membership test
passing through `contains_mask`/`contains_u8`.

## Adjudication

This is a source-level `ct-001` hardening increment, not a production
constant-time claim. The inventory remains `not_constant_time_reference` while
bounded toy sizing, diagnostic selectors, and the broader leakage audit are
still open.

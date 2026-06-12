# CODEX note: ct-001 source-level direct-index removal

Date: 2026-06-12 KST

## Scope

Directive: `meta/2026-06-12-DIRECTIVE-CODEX-L2-constant-time.md`, ct-001.

This increment tightens the existing `FixedLagrangian` membership rail by
removing the remaining source-level direct word indexing from the public
membership API and point-list construction path.

This is not an L2 closure claim, not a production constant-time claim, not a
generated-code audit, and not a security claim. The CT inventory classification
is intentionally not promoted in this increment.

## RED/GREEN

RED:

- Added `fixed_lagrangian_source_avoids_secret_dependent_word_indexing`.
- The test failed because `impl/lsn_ref/src/lib.rs` still contained direct
  `self.words[index >> 6]` and `words[index >> 6]` source patterns.

GREEN:

- `FixedLagrangian::contains_mask` now delegates to
  `contains_mask_scanned`.
- `FixedLagrangian::try_from_points` now builds the bitset through a
  public-layout scan over every word/bit slot and mask-selects matching input
  points, instead of writing `words[index >> 6]` directly.
- Existing KAT-facing membership paths continue to use scanned lookup.

## Interpretation

This closes one source-level ct-001 gap: the toy fixed-layout membership API no
longer exposes direct secret-dependent word indexing in the checked source.

Remaining limits:

- no compiler/assembly/timing/cache audit yet;
- secret Lagrangian generation still uses the experimental `Lagrangian`
  container before fixed-layout conversion;
- diagnostic rails remain test-only;
- `ct-003` polar SCL and `ct-004` RNG/KDF remain open;
- no production constant-time, security, PQ, or 7th-source claim.

## Next Step

Run the focused KAT and default `lsn_ref` verification set. If unchanged, move
to the next ct-001 slice or start ct-003 by wiring a real fixed-schedule decoder
entry point rather than adding more audit-only shape records.

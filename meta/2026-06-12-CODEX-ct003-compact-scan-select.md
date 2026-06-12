# CODEX note: ct-003 compact scan-select

Date: 2026-06-12 KST

## Scope

Directive: `meta/2026-06-12-DIRECTIVE-CODEX-L2-constant-time.md`, ct-003.

This increment tightens the fixed-i64 SCL prototype by removing the source-level
branch and direct indexed load in `FixedSclPathBuffer::from_top_entries`.

## RED/GREEN

RED:

- Added `fixed_scl_compact_source_avoids_entry_index_branch_and_load`.
- The focused test failed on the existing `if entry.index < SRC_CAP` branch.

GREEN:

- Replaced `source.slots[entry.index]` compaction with a full source-slot scan.
- Candidate selection now uses fixed-width mask helpers and public loop bounds.
- Selected inactive candidates are sanitized to `metric = i64::MAX`, zeroed bits,
  and `active = 0`.
- Focused expand/compact and fixed-i64 decoder smoke tests pass.

## Interpretation

This is a source-level fixed-path implementation tightening. It reduces another
ct-003 surface in the audit rail but does not change the production decoder.

Limits:

- no generated-code, optimizer, timing, branch-predictor, or cache audit;
- comparison operators and remaining fixed-path helpers still need review;
- `decode_scl`/`decode_scl_fast` remain the active non-constant-time decoders;
- N=2048 KAT/BLER gates are not run here;
- no inventory status change and no production constant-time, PQ, security, or
  7th-source claim.

## Next Step

Continue ct-003 by reviewing remaining fixed-path helper branches, or add a
fixed-i64 high-noise negative control before attempting larger-N comparison.

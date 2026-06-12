# CODEX note: ct-003 child-write active mask

Date: 2026-06-12 KST

## Scope

Directive: `meta/2026-06-12-DIRECTIVE-CODEX-L2-constant-time.md`, ct-003.

This increment removes the source-level inactive-parent early return from the
fixed SCL child expansion helper used by the fixed-i64 decoder path.

## RED/GREEN

RED:

- Added `fixed_scl_child_write_source_avoids_parent_active_branch`.
- The focused test failed because `write_binary_children_from` still contained
  `if parent.active == 0`.

GREEN:

- Replaced the inactive-parent branch with an `active` mask.
- Inactive parents now write candidate slots with `metric = i64::MAX`,
  zero-masked bits, and `active = 0`.
- Active parents preserve the previous child metrics and bits.
- Existing child-write and expand-then-compact tests pass.

## Interpretation

This is a source-level ct-003 implementation tightening for the fixed-i64
decoder path. It removes one secret-state-shaped branch from fixed child
expansion.

Limits:

- generated code, timing, and cache behavior are not audited;
- other fixed-buffer helper branches still exist and must be reviewed in later
  slices;
- `decode_scl`/`decode_scl_fast` are not replaced;
- N=2048 KAT/BLER gates are not run here;
- no inventory status change and no production constant-time, PQ, security, or
  7th-source claim.

## Next Step

Continue ct-003 by removing the next fixed-path source-level branch, or add the
fixed-i64 high-noise negative control before attempting N=2048 comparison.

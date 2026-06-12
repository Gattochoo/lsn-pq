# CODEX note: ct-003 effective metric mask

Date: 2026-06-12 KST

## Scope

Directive: `meta/2026-06-12-DIRECTIVE-CODEX-L2-constant-time.md`, ct-003.

This increment removes the source-level active branch in
`FixedSclCandidate::effective_metric`, which feeds the fixed SCL
`metric_entries` and top-L view.

## RED/GREEN

RED:

- Added `fixed_scl_effective_metric_source_avoids_active_branch`.
- The focused test failed on the existing `if self.active == 0` branch.

GREEN:

- Replaced the branch with an `active` mask and `select_i64`.
- Inactive candidates still expose `i64::MAX` as their effective metric.
- Focused top-L, compact, and fixed-i64 noisy smoke tests pass.

## Interpretation

This is a source-level fixed-path tightening for the audit rail. It removes one
more active-state branch from the fixed-i64 SCL prototype.

Limits:

- no generated-code, optimizer, timing, branch-predictor, or cache audit;
- boolean comparisons in sorting and public shape checks remain source-visible;
- `decode_scl`/`decode_scl_fast` remain active non-constant-time decoders;
- N=2048 KAT/BLER gates are not run here;
- no inventory status change and no production constant-time, PQ, security, or
  7th-source claim.

## Next Step

Continue ct-003 by reviewing remaining fixed-path comparisons and public/secret
classification, or add a fixed-i64 high-noise negative control before larger-N
comparison.

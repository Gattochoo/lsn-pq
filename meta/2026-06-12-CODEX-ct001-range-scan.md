# CODEX ct-001 full-slice range scan

Date: 2026-06-12

Scope: `impl/lsn_ref` toy/reference Lagrangian membership scaffold.

## Change

`FixedLagrangian::try_from_points` no longer exits immediately on the first
out-of-range point. After the public point-count check, it scans the whole
fixed-size point slice, accumulates an out-of-range mask, and mask-selects the
first invalid point for the existing error surface.

This keeps the invalid-input diagnostic behavior compatible while removing the
old range-validation early return inside the point scan.

## RED/GREEN

RED: extended `fixed_lagrangian_source_avoids_secret_dependent_word_indexing` to
reject the old `if index >= universe { return Err(PointOutOfRange ...) }` source
shape; it failed against the previous implementation.

GREEN: replaced the early-return range guard with a full-slice masked scan and
confirmed the existing `PointOutOfRange` behavior still reports the same point.

## Adjudication

This is another `ct-001` hardening step, not a production constant-time claim.
The inventory remains `not_constant_time_reference` because the scaffold is
still bounded to toy `n <= 8`, diagnostic selectors are non-production, and
generated-code/timing leakage audit remains open.

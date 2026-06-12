# CODEX ct-002 diagnostic mask boundary

Date: 2026-06-12

Scope: `impl/lsn_ref` toy divergent wrong-secret diagnostic selector.

## Change

Added `DiagnosticHonestOnlyMask` and
`diagnostic_honest_only_point_masks`, a fixed-shape diagnostic report that
records each candidate honest point with an include mask derived from the wrong
secret membership test.

The legacy `diagnostic_honest_only_points` list is now derived from that
explicit mask boundary. This keeps existing diagnostic behavior and KAT shape
stable while making the wrong-secret-dependent selector surface easier to audit.

## RED/GREEN

RED: added `diagnostic_honest_only_point_masks_keep_fixed_shape_boundary`; it
failed because the fixed-shape diagnostic mask type/helper did not exist.

GREEN: added the type/helper and kept the existing variable-length diagnostic
list output byte-compatible.

## Adjudication

This is not a production selector and not a public-distribution KAT path. It is
a diagnostic-only boundary hardening step; the CT inventory still marks this
surface as `diagnostic_only_not_public_distribution` and keeps
`production_constant_time_claim = false`.

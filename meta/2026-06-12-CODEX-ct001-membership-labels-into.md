# CODEX ct-001 membership labels into buffer

Date: 2026-06-12

Scope: `impl/lsn_ref` fixed Lagrangian label-generation boundary.

## Change

Added `FixedLagrangian::membership_labels_into`, a caller-owned output-buffer
variant for fixed Lagrangian membership labels. `membership_labels` now delegates
to this helper after allocating the public-size output vector.

## RED/GREEN

RED: added `fixed_lagrangian_membership_labels_into_fills_existing_buffer`,
which failed because the caller-buffer helper did not exist.

GREEN: added `membership_labels_into` and kept the existing
`membership_labels` behavior byte-compatible by routing it through the new
helper.

## Adjudication

This is source-level `ct-001` hardening only. It introduces a fixed-output
boundary useful for later production-sized layouts, but the implementation is
still a toy/reference scaffold and the inventory remains
`not_constant_time_reference`.

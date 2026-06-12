# CODEX ct-001 remove membership label helper

Date: 2026-06-12

Scope: `impl/lsn_ref` fixed Lagrangian label API.

## Change

Removed the allocating `FixedLagrangian::membership_labels` helper. The fixed
Lagrangian label API now exposes the caller-owned-buffer path
`membership_labels_into` only.

## RED/GREEN

RED: added `fixed_lagrangian_source_avoids_allocating_membership_label_helper`,
which failed while the public allocating helper was still present.

GREEN: removed the helper and updated the remaining unit coverage to validate
mask-derived labels through `membership_labels_into`.

## Adjudication

This is source-level `ct-001` hardening only. It reduces the toy/reference
allocation surface but does not close `ct-001`, does not upgrade the active
verdict, and makes no production constant-time, security, or 7th-source claim.

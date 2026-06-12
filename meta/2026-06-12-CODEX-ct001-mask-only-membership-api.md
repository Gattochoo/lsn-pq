# CODEX ct-001 mask-only membership API

Date: 2026-06-12

Scope: `impl/lsn_ref` fixed Lagrangian membership API.

## Change

Removed the `FixedLagrangian::contains_u8` convenience helper. Scalar
membership now exposes only `contains_mask`, and `membership_labels_into`
derives `u8` labels directly from `contains_mask`.

## RED/GREEN

RED: added `fixed_lagrangian_source_exposes_mask_membership_only`, which failed
while `pub fn contains_u8` was still present.

GREEN: removed `contains_u8`, updated fixed-Lagrangian unit coverage to assert
mask membership only, and kept `membership_labels_into` behavior unchanged.

## Adjudication

This is source-level `ct-001` hardening only. It narrows the membership API to
the mask primitive but does not close `ct-001`, does not upgrade the active
verdict, and makes no production constant-time, security, or 7th-source claim.

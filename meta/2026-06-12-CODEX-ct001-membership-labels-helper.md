# CODEX ct-001 membership labels helper

Date: 2026-06-12

Scope: `impl/lsn_ref` fixed Lagrangian label generation in toy/reference KAT
paths.

## Change

Added `FixedLagrangian::membership_labels` and routed public-label, clean-label,
wrong-secret-label, and divergent KAT clean-label generation through that helper.
The helper delegates to `contains_u8`, which delegates to the single
`contains_mask` path.

## RED/GREEN

RED: added `fixed_lagrangian_membership_labels_use_mask_path`, which failed
because the helper did not exist.

GREEN: added the helper and replaced repeated per-call-site membership mapping
with the shared fixed-layout label boundary while preserving KAT behavior.

## Adjudication

This is source-level `ct-001` hardening only. It centralizes the audit boundary
for toy label generation but does not close `ct-001`, replace the bounded toy
layout, or make a production constant-time/security claim.

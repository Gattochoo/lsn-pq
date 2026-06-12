# CODEX ct-001 toy label buffers

Date: 2026-06-12

Scope: `impl/lsn_ref` toy clean-label and wrong-secret label generation.

## Change

Routed the remaining toy/KAT clean-label and wrong-secret label generation
through `FixedLagrangian::membership_labels_into` with caller-owned output
buffers.

## RED/GREEN

RED: added `toy_clean_and_wrong_label_sources_use_membership_labels_into`,
which failed because `toy_kat_vector`, `toy_wrong_secret_control`,
`toy_divergent_wrong_secret_control`, and `toy_kat_from_parts` still used the
allocating `membership_labels` helper in those paths.

GREEN: replaced those call sites with explicit label buffers filled through
`membership_labels_into`, preserving the public KAT fixture behavior.

## Adjudication

This is another source-level `ct-001` hardening increment. It narrows the toy
membership label allocation surface but does not close `ct-001`, does not
upgrade the active verdict, and makes no production constant-time, security, or
7th-source claim.

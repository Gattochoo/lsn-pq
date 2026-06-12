# CODEX ct-001 public labels into buffer

Date: 2026-06-12

Scope: `impl/lsn_ref` public sample label generation.

## Change

Changed `public_samples` to allocate its public label vector once, fill the
membership labels with `FixedLagrangian::membership_labels_into`, and then xor
the public noise bits in place.

## RED/GREEN

RED: added `toy_public_sample_source_uses_membership_labels_into`, which failed
because `public_samples` still used the allocating `membership_labels` helper and
an intermediate membership-label vector.

GREEN: routed `public_samples` through `membership_labels_into` and kept the
public KAT fixture behavior byte-compatible.

## Adjudication

This is source-level `ct-001` hardening only. It reduces an internal allocation
surface in the toy/reference rail, but the implementation remains
`not_constant_time_reference`; no production constant-time or security claim is
made.

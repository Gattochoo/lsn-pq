# CODEX ct-001 KAT parts fixed boundary

Date: 2026-06-12

Scope: `impl/lsn_ref` divergent toy/reference KAT builder path.

## Change

Changed `toy_kat_from_parts` to accept a `&FixedLagrangian` instead of a raw
`&Lagrangian`. The divergent wrong-secret KAT path now constructs the honest
fixed layout once and passes that boundary into the part builder for clean
membership labels.

## RED/GREEN

RED: added `toy_kat_parts_source_takes_fixed_lagrangian_boundary`, which
requires the part builder to take a `FixedLagrangian` boundary and rejects the
old raw `Lagrangian` signature.

GREEN: threaded `fixed_honest_secret` through the divergent KAT builder and kept
the clean-majority separation test passing.

## Adjudication

This is source-level `ct-001` hardening only. It narrows membership call
surfaces but does not close `ct-001`, does not replace the bounded toy layout,
and does not make a production constant-time or security claim.

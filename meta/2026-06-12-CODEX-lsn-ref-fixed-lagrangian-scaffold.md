# CODEX note: ct-001 fixed Lagrangian scaffold

Date: 2026-06-12 KST

## Scope

This increment follows
`meta/2026-06-12-CODEX-lsn-ref-paper-r7-public-kat.md`.

Goal: start `ct-001` without making a production constant-time claim. The
change adds a fixed-layout bitset representation for toy Lagrangian membership
and routes toy KAT membership label generation through that representation.

This is a scaffold only. It does not close L2, does not claim production
constant-time behavior, does not replace the polar decoder, and does not make a
security claim.

## Implementation

Added `FixedLagrangian` in `impl/lsn_ref`:

- constructed from a public `n` and a point list;
- stores membership in a public-size `Vec<u64>` bitset;
- exposes `contains_mask(point) -> u64`, returning `0` or `u64::MAX`;
- exposes `contains_u8(point) -> u8` for the current toy KAT rail.

Toy membership-label paths now use `FixedLagrangian`:

- honest clean labels in `toy_kat_vector`;
- wrong-secret labels in `toy_wrong_secret_control`;
- wrong-secret labels in the divergent diagnostic;
- clean labels in `toy_kat_from_parts`;
- public sample label generation.

One intentionally remaining set-style membership is the divergent diagnostic's
`honest_only_points` construction. That selector is diagnostic-only and still
outside the public LSN distribution.

## Updated Artifact

Regenerated JSON:

- `experiments/182-codex-lsn-ref-ct-inventory.json`

Size:

- 3112 bytes

Updated `ct-001` classification:

| field | value |
|---|---|
| `classification` | `partial_fixed_layout_scaffold_not_production_ct` |
| `production_constant_time_claim` | `false` |
| `verdict` | `not_constant_time_reference` |

## RED/GREEN

1. Added `fixed_lagrangian_membership_matches_point_set_for_public_points`.
2. RED failed on missing `FixedLagrangian` export.
3. GREEN added `FixedLagrangian` and routed toy membership labels through it.
4. Added an inventory regression requiring the `ct-001` partial-scaffold
   classification.
5. RED failed on stale inventory classification.
6. GREEN updated `constant_time_inventory_json` and regenerated experiment
   `182`.

## Verification

Focused tests:

```bash
env CARGO_TARGET_DIR=/tmp/lsn-pq-lsnref-target \
  cargo test --manifest-path impl/lsn_ref/Cargo.toml \
  fixed_lagrangian_membership_matches_point_set_for_public_points
```

Result:

```text
1 passed
```

```bash
env CARGO_TARGET_DIR=/tmp/lsn-pq-lsnref-target \
  cargo test --manifest-path impl/lsn_ref/Cargo.toml \
  ct_inventory_marks_current_reference_as_non_production
```

Result:

```text
1 passed
```

Full `lsn_ref` suite:

```bash
env CARGO_TARGET_DIR=/tmp/lsn-pq-lsnref-target \
  cargo test --manifest-path impl/lsn_ref/Cargo.toml
```

Result:

```text
20 passed
```

Formatter:

```bash
env CARGO_TARGET_DIR=/tmp/lsn-pq-lsnref-target \
  cargo fmt --manifest-path impl/lsn_ref/Cargo.toml -- --check
```

Result: pass.

Exact checks:

```text
verified experiments/182-codex-lsn-ref-ct-inventory.json
verified experiments/152-codex-lsn-ref-toy-kat.json
verified experiments/153-codex-lsn-ref-n3-kat-search.json
verified experiments/180-codex-lsn-ref-n2-noisy-kat.json
verified experiments/181-codex-lsn-ref-n2-paper-r7-divergent-kat.json
verified experiments/185-codex-lsn-ref-n2-paper-r7-public-kat.json
```

## Interpretation

This is a narrow `ct-001` start: the toy membership surface no longer calls
`BTreeSet::contains` in the KAT label-generation path, and the inventory now
records that progress precisely.

Limits:

- `FixedLagrangian` is still reference scaffolding.
- Secret generation still uses the experimental `Lagrangian` container.
- The divergent diagnostic still contains a diagnostic-only set membership
  filter.
- No timing/leakage audit has been performed.
- No production constant-time claim is made.

## Next Step

Continue `ct-001` by freezing production-sized layout constraints and replacing
remaining diagnostic/set construction surfaces, or start `ct-003` by carving out
a fixed-schedule integer polar decoder plan without claiming production CT.

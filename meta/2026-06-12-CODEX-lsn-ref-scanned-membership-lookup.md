# CODEX note: ct-001 scanned membership lookup

Date: 2026-06-12 KST

## Scope

This increment follows
`meta/2026-06-12-CODEX-lsn-ref-fixed-lagrangian-scaffold.md`.

Goal: move the `FixedLagrangian` toy membership scaffold from direct word-index
lookup to a public-size scanned mask lookup for KAT label generation.

This remains a reference scaffold. It is not a production constant-time
implementation, not a leakage audit, not an L2 closure claim, and not a
security claim.

## Implementation

Added:

- `FixedLagrangian::contains_mask_scanned(point) -> u64`
- `FixedLagrangian::contains_u8_scanned(point) -> u8`

The scanned path iterates over every public-layout word and mask-selects the
target word before extracting the bit. Toy KAT membership label generation now
uses the scanned API:

- honest clean labels in `toy_kat_vector`;
- wrong-secret labels in `toy_wrong_secret_control`;
- wrong-secret labels in the divergent diagnostic;
- clean labels in `toy_kat_from_parts`;
- public sample label generation.

The direct `contains_mask` path remains available as a reference/equivalence
check.

## Updated Artifact

Regenerated JSON:

- `experiments/182-codex-lsn-ref-ct-inventory.json`

Size:

- 3182 bytes

Updated `ct-001` issue text:

```text
FixedLagrangian bitset scaffold now uses scanned mask lookup for toy membership
label generation, but secret construction, diagnostic selectors, and leakage
audit remain non-production
```

## RED/GREEN

1. Added `fixed_lagrangian_scanned_membership_matches_direct_membership`.
2. RED failed on missing `contains_mask_scanned` / `contains_u8_scanned`.
3. GREEN added scanned mask lookup and routed toy label generation through it.
4. Added an inventory regression requiring the phrase `scanned mask lookup`.
5. RED failed on stale inventory text.
6. GREEN updated `constant_time_inventory_json` and regenerated experiment
   `182`.

## Verification

Focused tests:

```bash
env CARGO_TARGET_DIR=/tmp/lsn-pq-lsnref-target \
  cargo test --manifest-path impl/lsn_ref/Cargo.toml \
  fixed_lagrangian_scanned_membership_matches_direct_membership
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
21 passed
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

This is a stricter `ct-001` scaffold than the direct bitset lookup: the toy KAT
membership-label path now uses a fixed public word-scan shape.

Limits:

- The implementation has not been audited at the compiler, assembly, timing, or
  cache level.
- Secret construction still uses the experimental `Lagrangian` container.
- The divergent diagnostic still has a diagnostic-only set-membership filter.
- The polar decoder remains `ct-003` / not constant-time.

## Next Step

Either continue `ct-001` by replacing remaining construction/diagnostic set
surfaces with explicit test-only boundaries, or start `ct-003` with a
fixed-schedule decoder plan and tests for deterministic work shape.

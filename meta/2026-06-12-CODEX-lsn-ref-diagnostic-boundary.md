# CODEX note: diagnostic membership boundary

Date: 2026-06-12 KST

## Scope

This increment follows
`meta/2026-06-12-CODEX-lsn-ref-scanned-membership-lookup.md`.

Goal: make the remaining divergent-selector membership dependency explicit as
diagnostic-only code, instead of leaving it as an inline set-style membership
filter inside the toy KAT path.

This remains reference scaffolding. It is not a production constant-time
implementation, not a leakage audit, not an L2 closure claim, and not a
security claim.

## Implementation

Added:

- `diagnostic_honest_only_points(honest_points, wrong_secret)`

The divergent wrong-secret diagnostic now constructs honest-only points through
that explicit boundary, using the `FixedLagrangian` scanned wrong-secret
membership path.

The `lsn_ref` membership-label paths remain on `contains_u8_scanned`. A grep
check found no remaining `secret.contains` / `wrong_secret.contains` membership
lookup in `impl/lsn_ref/src/lib.rs`; the remaining `points.contains` occurrence
is in a small test oracle.

## Updated Artifact

Regenerated JSON:

- `experiments/182-codex-lsn-ref-ct-inventory.json`

Size:

- 3280 bytes

Updated `ct-002` issue text:

```text
diagnostic selector depends on the wrong secret, is intentionally outside the
public LSN distribution, and is isolated behind an explicit
diagnostic_honest_only_points boundary
```

## RED/GREEN

1. Added `diagnostic_honest_only_points_uses_fixed_wrong_secret_boundary`.
2. RED failed on missing `diagnostic_honest_only_points`.
3. GREEN added the function and routed divergent diagnostic construction through
   it.
4. Added an inventory regression requiring
   `explicit diagnostic_honest_only_points boundary`.
5. RED failed on stale inventory text.
6. GREEN updated `constant_time_inventory_json` and regenerated experiment
   `182`.

## Verification

Focused tests:

```bash
env CARGO_TARGET_DIR=/tmp/lsn-pq-lsnref-target \
  cargo test --manifest-path impl/lsn_ref/Cargo.toml \
  diagnostic_honest_only_points_uses_fixed_wrong_secret_boundary
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
22 passed
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

Note: the `n3-search` exact check was rerun singly after one parallel run ended
without the verification line; the single rerun verified successfully.

## Interpretation

This narrows the `ct-001` bookkeeping surface: membership checks in the toy KAT
label path are now fixed-layout scanned lookups, while the wrong-secret
dependent divergent selector is clearly named and documented as diagnostic-only.

Limits:

- Secret construction still starts from the experimental `Lagrangian` container.
- No compiler/assembly/timing/cache audit has been run.
- The polar decoder remains `ct-003` / not constant-time.
- The divergent diagnostic remains outside the public LSN distribution by
  design.

## Next Step

Either freeze production-size layout constraints for `FixedLagrangian`, or start
`ct-003` with a fixed-schedule decoder work-shape test harness.

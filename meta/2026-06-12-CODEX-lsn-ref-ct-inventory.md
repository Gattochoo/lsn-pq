# CODEX note: lsn_ref constant-time inventory

Date: 2026-06-12 KST

## Scope

This increment follows
`meta/2026-06-12-CODEX-lsn-ref-paper-divergent-kat.md`.

It does not implement constant-time code. It adds a machine-readable inventory
that fixes the current status of the `impl/lsn_ref` toy KAT rail and the
`impl/polar_validation` decoder surface used by that rail.

Discipline: no paper edits, no production constant-time claim, no security
claim. OPEN = LSN.

## Artifact

Generated JSON:

- `experiments/182-codex-lsn-ref-ct-inventory.json`

Size:

- 2936 bytes

Top-level verdict:

| field | value |
|---|---|
| `verdict` | `not_constant_time_reference` |
| `production_constant_time_claim` | `false` |

Threat model recorded in the JSON:

- local timing/cache observer of encapsulation or decapsulation;
- public parameters and public samples are visible;
- Lagrangian membership, selected secret state, decoder paths, message bits,
  and noise bits are secret until explicitly serialized for KAT diagnostics.

## Inventory Items

| id | surface | classification |
|---|---|---|
| `ct-001` | Lagrangian membership representation | `not_constant_time` |
| `ct-002` | public-sample selection and toy divergent diagnostic selector | `diagnostic_only_not_public_distribution` |
| `ct-003` | polar SCL decoder | `not_constant_time` |
| `ct-004` | toy RNG and key derivation | `toy_only_not_cryptographic` |
| `ct-005` | KAT JSON serialization | `test_artifact_only` |

The important guard is `ct-002`: the `n2-paper-r7-divergent` KAT remains a
diagnostic artifact because its selector depends on the wrong secret. It is not
a public-distribution KAT.

## RED/GREEN

1. Added `ct_inventory_marks_current_reference_as_non_production` and
   `ct_inventory_cli_writes_and_checks_exact_json`.
2. RED failed on missing `constant_time_inventory_json`.
3. GREEN added `constant_time_inventory_json` and the `lsn_ct_inventory` writer
   / checker CLI.
4. Generated `experiments/182-codex-lsn-ref-ct-inventory.json`.

## Verification

Focused test:

```bash
env CARGO_TARGET_DIR=/tmp/lsn-pq-lsnref-target \
  cargo test --manifest-path impl/lsn_ref/Cargo.toml ct_inventory
```

Result:

```text
2 passed
```

Full `lsn_ref` suite:

```bash
env CARGO_TARGET_DIR=/tmp/lsn-pq-lsnref-target \
  cargo test --manifest-path impl/lsn_ref/Cargo.toml
```

Result:

```text
14 passed
```

Fixture checker:

```bash
env CARGO_TARGET_DIR=/tmp/lsn-pq-lsnref-target \
  cargo run --manifest-path impl/lsn_ref/Cargo.toml --release --bin lsn_ct_inventory -- \
  --check experiments/182-codex-lsn-ref-ct-inventory.json
```

Result:

```text
verified experiments/182-codex-lsn-ref-ct-inventory.json
```

## Interpretation

This closes only a bookkeeping gap: the current reference/KAT rail now carries a
machine-readable CT discipline statement. It does not close L2 and does not make
the implementation production-ready.

The next P3 implementation step remains one of:

- replace the diagnostic selector with a non-degenerate public-selection rule;
- or start `ct-001` with a fixed-layout Lagrangian representation and
  mask-based membership.

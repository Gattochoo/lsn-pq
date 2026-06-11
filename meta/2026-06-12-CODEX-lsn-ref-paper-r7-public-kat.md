# CODEX note: paper-r7 public-selection toy KAT

Date: 2026-06-12 KST

## Scope

This increment follows
`meta/2026-06-12-CODEX-lsn-ref-public-preflight-wrong16.md`.

Goal: turn the widened public-selection preflight seed tuple from experiment
`184` into an actual `lsn_toy_kat` profile and deterministic JSON fixture.

This uses `random-public-samples`. It is distinct from the divergent
wrong-secret diagnostic selector used by experiment `181`.

This is still `n = 2` toy reference scaffolding. It is not a production
constant-time implementation, not a security claim, not an L2 closure claim, and
not a 7th-source claim.

## Artifact

Generated JSON:

- `experiments/185-codex-lsn-ref-n2-paper-r7-public-kat.json`

Size:

- 190351 bytes

Top-level self-labels:

| field | value |
|---|---|
| `experiment` | `codex-lsn-ref-n2-paper-r7-public-kat` |
| `selection_mode` | `random-public-samples` |
| `diagnostic_only` | `false` |
| `roundtrip_ok` | `true` |
| `wrong_secret_roundtrip_ok` | `false` |

Profile:

| field | value |
|---|---:|
| symplectic half-dimension `n` | 2 |
| public sample count | 14336 |
| repetition | 7 |
| polar `N` | 2048 |
| polar `K` | 256 |
| public noise rate | 0.25 |
| decoder design `p` | 0.0706 |

Seeds:

| field | value |
|---|---:|
| honest secret seed | 659918 (`0xA11CE`) |
| wrong secret seed | 659920 (`0xA11D0`) |
| sample seed | 24301 (`0x5EED`) |
| noise seed | 49374 (`0xC0DE`) |
| encaps seed | 48879 (`0xBEEF`) |

## RED/GREEN

1. Added a `--describe` regression test for profile `n2-paper-r7-public`.
2. Added a generation/check regression test requiring public self-labels:
   `selection_mode = random-public-samples`, `diagnostic_only = false`, no
   `diagnostic_note`, and wrong-secret negative-control failure.
3. RED: focused test failed on unsupported profile `n2-paper-r7-public`.
4. GREEN: added public JSON metadata emission plus the new profile wired to the
   seed tuple found by experiment `184`.
5. Generated the deterministic public-distribution toy fixture.

## Verification

Focused test:

```bash
env CARGO_TARGET_DIR=/tmp/lsn-pq-lsnref-target \
  cargo test --manifest-path impl/lsn_ref/Cargo.toml public_paper_r7
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
19 passed
```

Formatter:

```bash
env CARGO_TARGET_DIR=/tmp/lsn-pq-lsnref-target \
  cargo fmt --manifest-path impl/lsn_ref/Cargo.toml -- --check
```

Result: pass.

Exact fixture checks:

```text
verified experiments/152-codex-lsn-ref-toy-kat.json
verified experiments/153-codex-lsn-ref-n3-kat-search.json
verified experiments/180-codex-lsn-ref-n2-noisy-kat.json
verified experiments/181-codex-lsn-ref-n2-paper-r7-divergent-kat.json
verified experiments/185-codex-lsn-ref-n2-paper-r7-public-kat.json
```

## Interpretation

This is the first paper-r7 public random-sample toy KAT candidate in
`impl/lsn_ref`. It supersedes the need to use experiment `181` for
public-distribution plumbing tests: `181` remains a useful divergent diagnostic,
while `185` is the public-selection fixture.

Limits:

- This is still an `n = 2` toy fixture.
- It is not a production constant-time KEM fixture.
- It does not close LSN-to-LPN or LSN worst-to-average.
- It is not a cryptographic security claim.

## Next Step

Use `185` as the public-distribution plumbing fixture while starting the next
implementation hardening slice: fixed-layout Lagrangian/reference data shapes
or the first constant-time inventory item (`ct-001`) in `impl/lsn_ref`.

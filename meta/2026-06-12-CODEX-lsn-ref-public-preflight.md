# CODEX note: public-selection paper-r7 preflight

Date: 2026-06-12 KST

## Scope

This increment follows
`meta/2026-06-12-CODEX-lsn-ref-ct-inventory.md`, especially `ct-002`.

Goal: add a bounded preflight scanner for the paper-r7 toy KAT profile that
uses only `random-public-samples`, not the divergent wrong-secret diagnostic
selector.

This is a scan report only. It does not generate a public-distribution KAT, does
not implement production constant-time code, and makes no security claim.

## Artifact

Generated JSON:

- `experiments/183-codex-lsn-ref-n2-paper-r7-public-preflight.json`

Size:

- 900 bytes

Top-level result:

| field | value |
|---|---|
| `selection_mode` | `random-public-samples` |
| `diagnostic_only` | `false` |
| `found_fixture` | `false` |
| `attempts` | `1` |
| `verdict` | `no_public_random_sample_negative_control_in_bounded_scan` |

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

Seed window:

| field | value |
|---|---:|
| honest secret seed | 659918 |
| sample seed start | 24301 |
| sample seed trials | 1 |
| wrong secret seed start | 659919 |
| wrong secret seed trials | 1 |
| noise seed | 49374 |
| encaps seed | 48879 |

## RED/GREEN

1. Added `public_preflight_scan_finds_small_random_sample_negative_control`
   and `public_preflight_cli_writes_and_checks_paper_r7_report`.
2. RED failed on missing `ToyPublicPreflightScanConfig`,
   `toy_public_wrong_secret_preflight_scan`, and
   `toy_public_wrong_secret_preflight_scan_to_json`.
3. GREEN added a bounded scan over public sample seeds and wrong-secret seeds.
   The small n=2 smoke case finds the existing random-sample negative control.
4. Added `lsn_public_preflight` writer/checker CLI.
5. Generated the paper-r7 bounded scan report.

## Verification

Focused test:

```bash
env CARGO_TARGET_DIR=/tmp/lsn-pq-lsnref-target \
  cargo test --manifest-path impl/lsn_ref/Cargo.toml public_preflight
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
16 passed
```

Formatter:

```bash
env CARGO_TARGET_DIR=/tmp/lsn-pq-lsnref-target \
  cargo fmt --manifest-path impl/lsn_ref/Cargo.toml -- --check
```

Result: pass.

Preflight checker:

```bash
env CARGO_TARGET_DIR=/tmp/lsn-pq-lsnref-target \
  cargo run --manifest-path impl/lsn_ref/Cargo.toml --release --bin lsn_public_preflight -- \
  --check experiments/183-codex-lsn-ref-n2-paper-r7-public-preflight.json
```

Result:

```text
verified experiments/183-codex-lsn-ref-n2-paper-r7-public-preflight.json
```

## Interpretation

The bounded `1 x 1` paper-r7 scan did not find a public random-sample
wrong-secret negative-control fixture. This is consistent with the earlier
preflight-only status of `n2-paper-r7`, but it is only a bounded scan, not a
no-go theorem and not a statement about larger seed windows.

The divergent `181` fixture remains the only paper-r7 KAT-like artifact, and it
remains diagnostic-only because it uses honest-only points chosen with knowledge
of the wrong secret.

## Next Step

Widen this scanner along one axis at a time:

1. wrong-secret seed window, then
2. sample seed window, then
3. if a public fixture is found, generate a separate public-distribution KAT
   candidate with the same self-labeling discipline.

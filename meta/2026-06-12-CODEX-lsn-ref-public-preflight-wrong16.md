# CODEX note: public-selection paper-r7 wrong-secret window 16

Date: 2026-06-12 KST

## Scope

This increment follows
`meta/2026-06-12-CODEX-lsn-ref-public-preflight.md`.

Goal: widen the bounded paper-r7 public-selection preflight along exactly one
axis: keep `sample_seed_trials = 1`, increase `wrong_secret_seed_trials` from
`1` to `16`.

This still uses `random-public-samples`; it does not use the divergent
wrong-secret diagnostic selector. It is a preflight scan report, not a production
constant-time implementation and not a security claim.

## Artifact

Generated JSON:

- `experiments/184-codex-lsn-ref-n2-paper-r7-public-preflight-wrong16.json`

Size:

- 906 bytes

Top-level result:

| field | value |
|---|---|
| `selection_mode` | `random-public-samples` |
| `diagnostic_only` | `false` |
| `found_fixture` | `true` |
| `attempts` | `2` |
| `verdict` | `found_public_random_sample_negative_control` |

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
| honest secret seed | 659918 (`0xA11CE`) |
| sample seed start | 24301 (`0x5EED`) |
| sample seed trials | 1 |
| wrong secret seed start | 659919 (`0xA11CF`) |
| wrong secret seed trials | 16 |
| found sample seed | 24301 (`0x5EED`) |
| found wrong secret seed | 659920 (`0xA11D0`) |
| noise seed | 49374 (`0xC0DE`) |
| encaps seed | 48879 (`0xBEEF`) |

## RED/GREEN

1. Added `public_preflight_cli_describes_wrong16_profile_without_running_scan`.
2. RED failed on unsupported `--describe`.
3. GREEN added `--describe` plus profile
   `n2-paper-r7-public-preflight-wrong16`.
4. Generated the widened preflight report.

## Verification

Focused test:

```bash
env CARGO_TARGET_DIR=/tmp/lsn-pq-lsnref-target \
  cargo test --manifest-path impl/lsn_ref/Cargo.toml \
  public_preflight_cli_describes_wrong16_profile_without_running_scan
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
17 passed
```

Formatter:

```bash
env CARGO_TARGET_DIR=/tmp/lsn-pq-lsnref-target \
  cargo fmt --manifest-path impl/lsn_ref/Cargo.toml -- --check
```

Result: pass.

Preflight checkers:

```text
verified experiments/183-codex-lsn-ref-n2-paper-r7-public-preflight.json
verified experiments/184-codex-lsn-ref-n2-paper-r7-public-preflight-wrong16.json
```

## Interpretation

The widened public-selection scan found a wrong-secret negative-control seed at
the second attempt. This is useful because it gives a concrete public random
sample candidate for replacing the diagnostic-only `181` artifact.

Limits:

- This is still `n = 2` toy scaffolding.
- It is not a production KAT yet; it only identifies the seed tuple.
- It is not constant-time.
- It is not a security claim and not a break.

## Next Step

Wire a separate `lsn_toy_kat` profile that uses the found public seed tuple:

- sample seed `0x5EED`
- wrong secret seed `0xA11D0`
- paper-r7 parameters

Then generate a self-labeled public-distribution KAT candidate distinct from
the divergent diagnostic `181`.

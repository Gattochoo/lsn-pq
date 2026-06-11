# CODEX note: paper-r7 divergent diagnostic KAT

Date: 2026-06-12 KST

## Scope

This increment follows
`meta/2026-06-11-CODEX-lsn-ref-paper-profile-preflight.md`.

The ordinary `n2-paper-r7` profile remains preflight-only because the current
small-`n` random public-sample majority rule did not provide a meaningful
wrong-secret negative control at the paper-polar setting.

This increment adds a separate diagnostic profile:

- `n2-paper-r7-divergent`

It uses the paper-polar parameters (`N=2048`, `K=256`, `r=7`, `p'=0.0706`)
but uses a **divergent wrong-secret diagnostic selector** on the toy LSN side.
The selector fills the selected repetition blocks with honest-only points
(`L_honest \ L_wrong`) so that the honest clean majority is 1 and the wrong
secret clean majority is 0.

This is useful for KAT plumbing and negative-control testing. It is **not** a
public-distribution LSN KAT, not a production KEM, not constant-time, not L2
closure, and not a security claim.

## Artifact

Generated JSON:

- `experiments/181-codex-lsn-ref-n2-paper-r7-divergent-kat.json`

Size:

- 192127 bytes

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

Observed fixture outcome:

- honest roundtrip: `true`
- wrong-secret roundtrip: `false`
- encapsulated/decapsulated key:
  `48cd31113acf4cfda7beac7d1dc9e4f4c760aae663d527958429d90874a91e54`
- wrong-secret decapsulated key:
  `8030b35377f479dc2e29394671d6f3535ff2ab33e2f26247f33b5f1ceb15deeb`

## RED/GREEN

1. Added `divergent_wrong_secret_control_forces_clean_majority_separation`.
   RED failed on missing `toy_divergent_wrong_secret_control`.
2. Implemented a diagnostic selector that uses honest-only points. Initial
   noisy unit-test parameters were too noisy for the tiny test polar code, so
   the unit test was narrowed to `public_noise_rate = 0.0` to test separation
   rather than paper-polar correction.
3. Added `cli_describes_divergent_paper_r7_diagnostic_profile`. RED failed on
   missing `n2-paper-r7-divergent`.
4. Added the profile, selection-mode metadata, and release fixture generation.
5. Generated and checked the JSON fixture.

## Verification

Focused tests:

```bash
env CARGO_TARGET_DIR=/tmp/lsn-pq-lsnref-target \
  cargo test --manifest-path impl/lsn_ref/Cargo.toml \
  divergent_wrong_secret_control_forces_clean_majority_separation

env CARGO_TARGET_DIR=/tmp/lsn-pq-lsnref-target \
  cargo test --manifest-path impl/lsn_ref/Cargo.toml \
  cli_describes_divergent_paper_r7_diagnostic_profile
```

Full `lsn_ref` suite:

```bash
env CARGO_TARGET_DIR=/tmp/lsn-pq-lsnref-target \
  cargo test --manifest-path impl/lsn_ref/Cargo.toml
```

Result:

```text
11 passed
```

Fixture generation:

```bash
env CARGO_TARGET_DIR=/tmp/lsn-pq-lsnref-target \
  cargo run --manifest-path impl/lsn_ref/Cargo.toml --release --bin lsn_toy_kat -- \
  --profile n2-paper-r7-divergent
```

Result:

```text
wrote experiments/181-codex-lsn-ref-n2-paper-r7-divergent-kat.json
```

Fixture checker:

```bash
env CARGO_TARGET_DIR=/tmp/lsn-pq-lsnref-target \
  cargo run --manifest-path impl/lsn_ref/Cargo.toml --release --bin lsn_toy_kat -- \
  --profile n2-paper-r7-divergent \
  --check experiments/181-codex-lsn-ref-n2-paper-r7-divergent-kat.json
```

Result:

```text
verified experiments/181-codex-lsn-ref-n2-paper-r7-divergent-kat.json
```

## Interpretation

This successfully connects the KAT rail to the real `impl/polar_validation`
decoder at `N=2048, K=256, r=7, p'=0.0706` while keeping a strong wrong-secret
negative control.

The result is still diagnostic. The selector deliberately uses knowledge of the
wrong secret to force a clean-majority split. Therefore it should be used only
as a regression/KAT plumbing artifact, not as evidence that the production
public-sample KEM distribution has been implemented or validated.

## Next P3 Step

Write the constant-time discipline inventory requested by Claude, or replace
the diagnostic selector with a non-degenerate public-selection rule that does
not depend on the wrong secret.

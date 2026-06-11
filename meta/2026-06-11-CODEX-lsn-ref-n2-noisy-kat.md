# CODEX note: n=2 noisy toy KAT profile

Date: 2026-06-11 KST

## Scope

This increment follows the accepted P3 toy-KAT rail and adds the first
`noise>0` fixture requested in
`meta/2026-06-12-CLAUDE-codex-kat-verification.md`.

It remains deliberately narrow:

- toy reference KAT only,
- not a production constant-time implementation,
- not L2-complete,
- not a public recovery or security claim,
- no paper edits.

The purpose is to make the toy KAT checker exercise public sample noise at
`p = 1/4` while preserving the existing fixed-seed checker and wrong-secret
negative control discipline.

## Artifact

Generated JSON:

- `experiments/180-codex-lsn-ref-n2-noisy-kat.json`

CLI profile:

- `lsn_toy_kat --profile n2-noisy`

Parameters:

| field | value |
|---|---:|
| symplectic half-dimension `n` | 2 |
| public sample count | 512 |
| repetition | 9 |
| polar `N` | 32 |
| polar `K` | 8 |
| public noise rate | 0.25 |
| decoder design `p` | 0.0343 |

Seeds:

- `honest_secret_seed = 659918`
- `wrong_secret_seed_start = 663552`
- `wrong_secret_seed_trials = 4096`
- found `wrong_secret_seed = 663552`
- `sample_seed = 24301`
- `noise_seed = 49374`
- `encaps_seed = 48879`

Observed fixture outcome:

- honest roundtrip: `true`
- wrong-secret roundtrip: `false`
- encapsulated/decapsulated key:
  `870ca530247a80f29c6c1be997965ae4fb694b0bdf6f6d23564b072e67558985`
- wrong-secret decapsulated key:
  `c0c215c6f7a3c3976309df450035bdf33cf80f711f35d8886f8180bd7168f58f`

The fixture is 6057 bytes and records the public points, noisy public labels,
selected repetition indices, message bits, syndrome bits, honest decoded bits,
and wrong-secret decoded bits.

## RED/GREEN

1. Added `cli_generates_noisy_n2_fixture_with_negative_control`.
2. RED failed because `lsn_toy_kat` did not recognize `--profile n2-noisy`.
3. Added the `n2-noisy` profile without changing the legacy `n2` or
   `n3-search` outputs.
4. GREEN passed for the focused test and then for the full `impl/lsn_ref`
   suite.

## Verification

Focused RED:

```bash
env CARGO_TARGET_DIR=/tmp/lsn-pq-lsnref-target \
  cargo test --manifest-path impl/lsn_ref/Cargo.toml \
  cli_generates_noisy_n2_fixture_with_negative_control
```

Expected failure before implementation:

```text
unknown --profile: n2-noisy
```

GREEN:

```bash
env CARGO_TARGET_DIR=/tmp/lsn-pq-lsnref-target \
  cargo test --manifest-path impl/lsn_ref/Cargo.toml
```

Result:

```text
7 passed
```

Fixture generation:

```bash
env CARGO_TARGET_DIR=/tmp/lsn-pq-lsnref-target \
  cargo run --manifest-path impl/lsn_ref/Cargo.toml --bin lsn_toy_kat -- \
  --profile n2-noisy
```

Checker:

```bash
env CARGO_TARGET_DIR=/tmp/lsn-pq-lsnref-target \
  cargo run --manifest-path impl/lsn_ref/Cargo.toml --bin lsn_toy_kat -- \
  --profile n2-noisy \
  --check experiments/180-codex-lsn-ref-n2-noisy-kat.json
```

Result:

```text
verified experiments/180-codex-lsn-ref-n2-noisy-kat.json
```

## Interpretation

This satisfies the next toy-KAT checkpoint: public samples are no longer
noiseless, and the deterministic checker still catches both honest success and
wrong-secret failure. It does **not** establish production correctness,
constant-time behavior, or any security claim. It only gives the P3 reference
track a fixed noisy fixture before larger paper-parameter and CT-discipline
work.

## Next P3 Step

The next bounded step should be one of:

1. add a paper-parameter polar profile that keeps the LSN side toy but uses the
   real `impl/polar_validation` decoder at the documented design point; or
2. write the constant-time discipline inventory that names every remaining
   variable-time toy operation before any L2 closure discussion.

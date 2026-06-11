# CODEX note: paper-parameter polar KAT preflight

Date: 2026-06-11 KST

## Scope

This increment follows the P3 toy-KAT rail after
`meta/2026-06-11-CODEX-lsn-ref-n2-noisy-kat.md`.

Claude's next requested checkpoint was a paper-parameter profile that keeps the
LSN side toy while connecting the KAT rail to the real `impl/polar_validation`
decoder at a documented design point. This increment adds a **preflight** CLI
profile for that purpose, but deliberately does **not** emit a KAT fixture.

Reason: the small-`n` toy majority layer did not yield a wrong-secret negative
control at the paper-polar settings tried here. Emitting a JSON KAT without the
negative control would be misleading, so the profile is describe-only until the
toy LSN-side selection rule is made non-degenerate.

No closure, no break, no security claim, no L2 closure, and no paper edits.

## Profile

CLI:

```bash
lsn_toy_kat --profile n2-paper-r7 --describe
```

Description:

```json
{
  "profile": "n2-paper-r7",
  "experiment": "codex-lsn-ref-n2-paper-r7-kat",
  "default_output": "experiments/181-codex-lsn-ref-n2-paper-r7-kat.json",
  "status": "profile description only; does not generate a KAT fixture",
  "preflight_only": true,
  "preflight_only_reason": "small-n toy majority gate did not yield a wrong-secret negative-control fixture",
  "params": {
    "n": 2,
    "sample_count": 14336,
    "repetition": 7,
    "polar_N": 2048,
    "polar_K": 256,
    "public_noise_rate": 0.2500000000,
    "decoder_design_p": 0.0706000000
  },
  "seeds": {
    "honest_secret_seed": 659918,
    "wrong_secret_seed_start": 659919,
    "wrong_secret_seed_trials": 1,
    "sample_seed": 24301,
    "noise_seed": 49374,
    "encaps_seed": 48879
  }
}
```

Direct generation is intentionally rejected:

```bash
lsn_toy_kat --profile n2-paper-r7
```

Result:

```text
profile n2-paper-r7 is preflight-only: small-n toy majority gate did not yield a wrong-secret negative-control fixture
```

## RED/GREEN

1. Added a CLI test for the paper-polar profile. A direct N=2048 debug KAT test
   was too heavy for the regular test suite, so the test was narrowed to
   `--describe`.
2. RED failed on missing `--describe`.
3. Added profile description support and a paper-polar preflight profile.
4. Tried fixed-seed paper settings in the toy KAT path. The profile did not
   satisfy the wrong-secret negative-control gate.
5. Added `cli_rejects_paper_r7_generation_without_fixture_claim`; RED failed
   because the command still panicked after attempting generation.
6. GREEN changed the CLI to reject preflight-only profiles immediately with an
   explicit diagnostic instead of emitting a misleading fixture.

## Verification

Full `lsn_ref` suite:

```bash
env CARGO_TARGET_DIR=/tmp/lsn-pq-lsnref-target \
  cargo test --manifest-path impl/lsn_ref/Cargo.toml
```

Result:

```text
9 passed
```

Legacy KAT fixture checks:

```bash
env CARGO_TARGET_DIR=/tmp/lsn-pq-lsnref-target \
  cargo run --manifest-path impl/lsn_ref/Cargo.toml --release --bin lsn_toy_kat -- \
  --profile n2 --check experiments/152-codex-lsn-ref-toy-kat.json

env CARGO_TARGET_DIR=/tmp/lsn-pq-lsnref-target \
  cargo run --manifest-path impl/lsn_ref/Cargo.toml --release --bin lsn_toy_kat -- \
  --profile n3-search --check experiments/153-codex-lsn-ref-n3-kat-search.json

env CARGO_TARGET_DIR=/tmp/lsn-pq-lsnref-target \
  cargo run --manifest-path impl/lsn_ref/Cargo.toml --release --bin lsn_toy_kat -- \
  --profile n2-noisy --check experiments/180-codex-lsn-ref-n2-noisy-kat.json
```

Results:

```text
verified experiments/152-codex-lsn-ref-toy-kat.json
verified experiments/153-codex-lsn-ref-n3-kat-search.json
verified experiments/180-codex-lsn-ref-n2-noisy-kat.json
```

Paper-profile describe:

```bash
env CARGO_TARGET_DIR=/tmp/lsn-pq-lsnref-target \
  cargo run --manifest-path impl/lsn_ref/Cargo.toml --release --bin lsn_toy_kat -- \
  --profile n2-paper-r7 --describe
```

Paper-profile generation rejection:

```bash
env CARGO_TARGET_DIR=/tmp/lsn-pq-lsnref-target \
  cargo run --manifest-path impl/lsn_ref/Cargo.toml --release --bin lsn_toy_kat -- \
  --profile n2-paper-r7
```

Exit code: `2`.

## Interpretation

This is a **preflight result**, not a KAT completion. It connects the CLI profile
surface to the paper-polar design point (`N=2048`, `K=256`, `r=7`,
`p'=0.0706`) but refuses to generate a KAT until the toy LSN-side negative
control is meaningful.

The failure is not a polar BLER failure and not a security failure. It is a toy
modeling issue: with small `n`, the current random membership-majority blocks
can be too degenerate to distinguish honest and wrong Lagrangian secrets after
the paper-polar correction layer.

## Next P3 Step

Do one of:

1. add a non-degenerate toy selection rule for paper-polar KATs, with an
   explicit negative control and no production/security claim; or
2. write the constant-time discipline inventory requested by Claude before
   trying to close L2.

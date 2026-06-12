# Codex Fixed-I64 N2048 Smoke Fixture

## Scope

This increment turns the `polar-validate --decoder fixed-i64 --check` path into
a repo-level reproducibility guard for a tiny `N=2048,K=256` smoke fixture.

New artifact:

- `experiments/188-codex-polar-rust-fixed-i64-n2048-smoke.json`

The fixture uses:

- decoder: `fixed-i64`;
- suite: `n2048`;
- list size: `8`;
- trials: `1`;
- seed: `5397`.

This is deliberately a small smoke/reproducibility artifact, not a BLER bound.

## RED

Added `cli_check_accepts_repo_fixed_i64_n2048_fixture` in
`impl/polar_validation/tests/polar_validate_cli.rs`.

The focused RED failed because the repo fixture did not exist:

```text
failed to read polar fixture: No such file or directory
```

## GREEN

Generated the fixture via:

```text
env CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target cargo run --manifest-path impl/polar_validation/Cargo.toml --bin polar-validate -- --decoder fixed-i64 --suite n2048 --trials 1 --seed 5397 --output experiments/188-codex-polar-rust-fixed-i64-n2048-smoke.json
```

The first GREEN check exposed a test cwd issue: integration tests run from the
crate context, so the repo fixture path needed to be absolute. The test now
derives the repo root from `CARGO_MANIFEST_DIR`.

Focused GREEN:

```text
env CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target cargo test --manifest-path impl/polar_validation/Cargo.toml cli_check_accepts_repo_fixed_i64_n2048_fixture
```

Default:

```text
env CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target cargo fmt --manifest-path impl/polar_validation/Cargo.toml -- --check
env CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target cargo test --manifest-path impl/polar_validation/Cargo.toml
env CARGO_TARGET_DIR=/tmp/lsn-pq-lsnref-target cargo test --manifest-path impl/lsn_ref/Cargo.toml
env CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target cargo run --manifest-path impl/polar_validation/Cargo.toml --release --bin polar_scl_audit -- --check experiments/186-codex-polar-scl-workshape-audit.json
env CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target cargo run --manifest-path impl/polar_validation/Cargo.toml --bin polar-validate -- --decoder fixed-i64 --suite n2048 --trials 1 --seed 5397 --check experiments/188-codex-polar-rust-fixed-i64-n2048-smoke.json
env CARGO_TARGET_DIR=/tmp/lsn-pq-lsnref-target cargo build --manifest-path impl/lsn_ref/Cargo.toml --release --bin lsn_toy_kat
/tmp/lsn-pq-lsnref-target/release/lsn_toy_kat --profile n2 --check experiments/152-codex-lsn-ref-toy-kat.json
/tmp/lsn-pq-lsnref-target/release/lsn_toy_kat --profile n3-search --check experiments/153-codex-lsn-ref-n3-kat-search.json
/tmp/lsn-pq-lsnref-target/release/lsn_toy_kat --profile n2-noisy --check experiments/180-codex-lsn-ref-n2-noisy-kat.json
/tmp/lsn-pq-lsnref-target/release/lsn_toy_kat --profile n2-paper-r7-divergent --check experiments/181-codex-lsn-ref-n2-paper-r7-divergent-kat.json
/tmp/lsn-pq-lsnref-target/release/lsn_toy_kat --profile n2-paper-r7-public --check experiments/185-codex-lsn-ref-n2-paper-r7-public-kat.json
git diff --check
```

## Limits

- This is not a production constant-time decoder.
- This is not a security, PQ, or 7th-source claim.
- The fixture has only one trial per target `p`; it is a deterministic
  reproducibility guard, not a statistical validation.
- The active decoder remains `not_constant_time`.

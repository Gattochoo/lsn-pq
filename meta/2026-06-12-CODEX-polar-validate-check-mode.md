# Codex Polar Validate Check Mode

## Scope

This increment adds `--check PATH` to `polar-validate`, matching the existing
`polar_rate_sweep`, `polar_importance`, and `polar_scl_audit` fixture-checking
pattern.

It is a validation-harness improvement only. It does not touch `paper/`, does
not change the active decoder verdict, and does not imply any
constant-time/PQ/security/7th-source claim.

## RED

Added `cli_check_accepts_matching_fixed_i64_fixture` in
`impl/polar_validation/tests/polar_validate_cli.rs`.

The focused RED failed because `polar-validate` did not recognize `--check`:

```text
unknown argument: --check
```

## GREEN

`polar-validate` now:

- parses `--check PATH`;
- regenerates the selected suite/decoder JSON;
- compares the generated JSON against the fixture byte-for-byte;
- prints `verified <path>` and exits without writing `--output` on match;
- exits with a diagnostic on mismatch.

The focused fixed-i64 baseline fixture test now generates a tiny fixture and
then checks it through the same CLI.

## Verification

Focused:

```text
env CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target cargo test --manifest-path impl/polar_validation/Cargo.toml cli_check_accepts_matching_fixed_i64_fixture
env CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target cargo test --manifest-path impl/polar_validation/Cargo.toml cli_writes_fixed_i64_baseline_fixture
```

Default:

```text
env CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target cargo fmt --manifest-path impl/polar_validation/Cargo.toml -- --check
env CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target cargo test --manifest-path impl/polar_validation/Cargo.toml
env CARGO_TARGET_DIR=/tmp/lsn-pq-lsnref-target cargo test --manifest-path impl/lsn_ref/Cargo.toml
env CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target cargo run --manifest-path impl/polar_validation/Cargo.toml --release --bin polar_scl_audit -- --check experiments/186-codex-polar-scl-workshape-audit.json
env CARGO_TARGET_DIR=/tmp/lsn-pq-lsnref-target cargo build --manifest-path impl/lsn_ref/Cargo.toml --release --bin lsn_toy_kat
/tmp/lsn-pq-lsnref-target/release/lsn_toy_kat --profile n2 --check experiments/152-codex-lsn-ref-toy-kat.json
/tmp/lsn-pq-lsnref-target/release/lsn_toy_kat --profile n3-search --check experiments/153-codex-lsn-ref-n3-kat-search.json
/tmp/lsn-pq-lsnref-target/release/lsn_toy_kat --profile n2-noisy --check experiments/180-codex-lsn-ref-n2-noisy-kat.json
/tmp/lsn-pq-lsnref-target/release/lsn_toy_kat --profile n2-paper-r7-divergent --check experiments/181-codex-lsn-ref-n2-paper-r7-divergent-kat.json
/tmp/lsn-pq-lsnref-target/release/lsn_toy_kat --profile n2-paper-r7-public --check experiments/185-codex-lsn-ref-n2-paper-r7-public-kat.json
git diff --check
```

## Limits

- This adds no new production decoder path.
- The fixed-i64 CLI dispatch remains list-size-8-only.
- Generated-code, timing, cache, and microarchitectural audits remain pending.
- The active decoder remains `not_constant_time`.

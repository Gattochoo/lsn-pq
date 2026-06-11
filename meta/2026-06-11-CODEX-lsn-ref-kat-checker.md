# CODEX note: toy KAT self-check CLI

Date: 2026-06-11 KST

## Scope

This is a small P3 reference-implementation increment for `impl/lsn_ref`.
It adds a deterministic KAT checker to the toy CLI so checked-in fixtures can
be regenerated and compared mechanically.

This remains only a toy reference rail:

- not production constant-time,
- not an L2-complete implementation,
- not a security claim,
- not evidence of a public recovery path.

## Change

`lsn_toy_kat` now supports:

```text
lsn_toy_kat [--profile n2|n3-search] --check PATH
```

The command regenerates the selected profile and compares it byte-for-byte with
the supplied fixture. A mismatch exits nonzero and prints `KAT check failed`.

## Negative control

Added integration tests in `impl/lsn_ref/tests/kat_cli.rs`:

- matching `n3-search` fixture generation + check must succeed,
- mismatched JSON fixture must fail and report `KAT check failed`.

## Verification

Commands run with `CARGO_TARGET_DIR=/tmp/lsn-pq-lsn-ref-target` to avoid writing
Cargo build artifacts into the repo:

```text
cargo fmt --manifest-path impl/lsn_ref/Cargo.toml -- --check
cargo test --manifest-path impl/lsn_ref/Cargo.toml cli_check -- --nocapture
cargo test --manifest-path impl/lsn_ref/Cargo.toml
cargo run --manifest-path impl/lsn_ref/Cargo.toml --release --bin lsn_toy_kat -- --profile n3-search --check experiments/153-codex-lsn-ref-n3-kat-search.json
```

Observed result:

- CLI checker tests: `2 passed`
- full `lsn_ref` tests: `6 passed`
- release fixture check: verified `experiments/153-codex-lsn-ref-n3-kat-search.json`

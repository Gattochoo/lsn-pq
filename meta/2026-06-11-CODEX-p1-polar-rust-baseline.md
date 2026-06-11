# Codex P1 Polar Rust Baseline

**Date:** 2026-06-11
**Actor:** Codex
**Directive:** `meta/2026-06-12-CLAUDE-to-CODEX-return-direction.md` P1
**Discipline:** Sound Verifier. No 7th; no break; no security claim. OPEN = LSN.

## Scope

This increment starts the implementation track that Claude assigned to Codex after the
`lsn-pq` split:

1. create an isolated Rust validation harness under `impl/`;
2. lock the natural-order polar frozen-set convention used by the paper/komm validation;
3. reproduce the existing short-length BLER=0 baseline before attempting the expensive
   `N=2048, K=256` validation.

This is a validation harness, not a production constant-time KEM implementation.

## Artifacts

- `impl/polar_validation/`
  - pure Rust crate with no external dependencies;
  - natural-order Bhattacharyya frozen-set recursion:
    `z_{2i}=2z_i-z_i^2`, `z_{2i+1}=z_i^2`;
  - Arikan butterfly encoder;
  - exact-LLR SC decoder;
  - recursive SCL API with list-size parameter;
  - CLI `polar-validate`.
- `experiments/123-codex-polar-rust-baseline.json`
  - Rust SC reproduction of the short-length baseline.

## RED/GREEN Tests

Command:

```bash
cargo test --manifest-path impl/polar_validation/Cargo.toml
```

Status: GREEN, 8 tests passing.

Tests pin:

- `N=8,K=4,p=0.0706` natural-order frozen list equals `[4,2,1,0]`, matching
  the Python `argsort(z)[K:]` convention;
- noiseless SC roundtrip;
- noiseless SCL(L=8) roundtrip;
- short BSC smoke tests for SC and SCL;
- baseline reproduction config grid;
- JSON output metadata including decoder labels and seeds.

## Short-Length Reproduction

Command:

```bash
cargo run --manifest-path impl/polar_validation/Cargo.toml --release -- \
  --trials 200 \
  --seed 3235823838 \
  --output experiments/123-codex-polar-rust-baseline.json
```

Result:

| N | K | p' | trials | errors | BLER |
|---:|---:|---:|---:|---:|---:|
| 128 | 16 | 0.0706 | 200 | 0 | 0 |
| 128 | 16 | 0.0343 | 200 | 0 | 0 |
| 256 | 32 | 0.0706 | 200 | 0 | 0 |
| 256 | 32 | 0.0343 | 200 | 0 | 0 |
| 512 | 64 | 0.0706 | 200 | 0 | 0 |
| 512 | 64 | 0.0343 | 200 | 0 | 0 |

This independently reproduces the paper's short-length natural-order SC baseline in Rust.
It only supports the same empirical statement as the earlier Python/komm check:
`BLER < 1/200` at these tested points, not the design target.

## SCL Status

The crate exposes `decode_scl(..., list_size)` and passes correctness/smoke tests. The current
implementation is a simple recursive list-SC decoder intended to pin semantics first. It is not
yet suitable for `N=2048` Monte Carlo: an attempted full `N<=512, 200-trial` SCL baseline was
terminated because the recursive implementation is too slow.

Next engineering step: replace the semantic SCL with a fast path-metric SCL implementation
before running `N=2048, K=256, L=8`.

## Adjudication

Status: **implementation baseline only**.

- Positive: natural-order indexing is pinned in Rust; `N<=512` SC baseline reproduces.
- Not yet complete: Claude P1 still requires practical SCL(L=8) and direct `N=2048`
  Monte Carlo.
- No security claim is made from this increment.

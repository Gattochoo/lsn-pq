# Codex P1 Fast SCL N=2048 Pilot

**Date:** 2026-06-11
**Actor:** Codex
**Directive:** `meta/2026-06-12-CLAUDE-to-CODEX-return-direction.md` P1
**Discipline:** Sound Verifier. No 7th; no break; no security claim. OPEN = LSN.

## Scope

This increment removes the immediate engineering blocker found in
`meta/2026-06-11-CODEX-p1-polar-rust-baseline.md`: the first recursive semantic SCL API was
correct on small tests but too slow for the short-length `N<=512` baseline.

The new implementation adds a phase-by-phase beam SCL variant:

- list size: `L=8`;
- LLR update: min-sum `f`;
- path metric: common min-sum hard-decision penalty;
- frozen-set convention: natural-order Bhattacharyya recursion
  `z_{2i}=2z_i-z_i^2`, `z_{2i+1}=z_i^2`.

The exact recursive SCL remains in the crate as a semantic cross-check for small tests. The
fast decoder is explicitly labeled `scl_l8_minsum_pathmetric`; it should not be reported as an
exact Tal-Vardy implementation.

## RED/GREEN Tests

Command:

```bash
cargo test --manifest-path impl/polar_validation/Cargo.toml
```

Status: GREEN, 11 tests passing.

New tests pin:

- noiseless fast-SCL roundtrip;
- short BSC fast-SCL smoke test;
- `N=2048,K=256` target config points for `p'=0.0706` and `p'=0.0343`.

## Short-Length SCL-Fast Baseline

Command:

```bash
cargo run --manifest-path impl/polar_validation/Cargo.toml --release -- \
  --decoder scl-fast \
  --list-size 8 \
  --trials 200 \
  --seed 3235823838 \
  --output experiments/124-codex-polar-rust-scl-fast-baseline.json
```

Result: all six `N<=512` baseline points returned `0/200` block errors.

| N | K | p' | trials | errors | BLER |
|---:|---:|---:|---:|---:|---:|
| 128 | 16 | 0.0706 | 200 | 0 | 0 |
| 128 | 16 | 0.0343 | 200 | 0 | 0 |
| 256 | 32 | 0.0706 | 200 | 0 | 0 |
| 256 | 32 | 0.0343 | 200 | 0 | 0 |
| 512 | 64 | 0.0706 | 200 | 0 | 0 |
| 512 | 64 | 0.0343 | 200 | 0 | 0 |

## First N=2048 Monte Carlo

Command:

```bash
cargo run --manifest-path impl/polar_validation/Cargo.toml --release -- \
  --suite n2048 \
  --decoder scl-fast \
  --list-size 8 \
  --trials 200 \
  --seed 3235823838 \
  --output experiments/125-codex-polar-rust-scl-fast-n2048.json
```

Result:

| N | K | p' | trials | errors | BLER |
|---:|---:|---:|---:|---:|---:|
| 2048 | 256 | 0.0706 | 200 | 0 | 0 |
| 2048 | 256 | 0.0343 | 200 | 0 | 0 |

## Interpretation

This is a positive implementation-data point for paper limitation L1: the target length has now
been directly exercised, and no block errors were observed in the initial 200-trial Monte Carlo.

Limits:

- `0/200` only supports the empirical statement `BLER < 1/200` at this sample size.
- It does not verify the design targets `2^-80` or `2^-128`.
- The decoder is an engineering validation SCL variant (`minsum_pathmetric`), not yet a constant-time
  production decoder.

## Next Step

Run higher-trial `N=2048` sweeps, then add a timing/throughput report and decide whether importance
sampling is needed for a meaningful upper-bound estimate beyond `1/trials`.

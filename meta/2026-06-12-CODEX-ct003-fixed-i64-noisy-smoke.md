# CODEX note: ct-003 fixed-i64 noisy smoke wrapper

Date: 2026-06-12 KST

## Scope

Directive: `meta/2026-06-12-DIRECTIVE-CODEX-L2-constant-time.md`, ct-003.

This increment extends the fixed-i64 SCL decoder from a noiseless direct
roundtrip to a deterministic noisy BSC simulation wrapper:

```rust
simulate_bsc_scl_fixed_i64<const N: usize, const L: usize, const CHILD_CAP: usize>
```

The wrapper uses the same message, channel, and LLR generation as
`simulate_bsc_scl_fast`, but decodes through `decode_scl_fixed_i64`.

## RED/GREEN

RED:

- Added `short_bsc_fixed_i64_scl_smoke_matches_fast_scl`.
- The focused test failed to compile because `simulate_bsc_scl_fixed_i64` did
  not exist.

GREEN:

- Added `simulate_bsc_scl_fixed_i64`.
- The focused test passes for `N=128`, `K=16`, `p=0.0706`, `25` trials, and
  fixed seed `0xF451C1`, matching the existing fast SCL error count exactly
  (`0/25`).

## Interpretation

This is a small implementation step toward ct-003: the fixed-i64 decoder now
has a simulation harness with the same public BSC inputs as the variable-time
fast SCL rail.

Limits:

- not wired into default `decode_scl`/`decode_scl_fast`;
- not yet checked on N=2048/K=256/r=7 KAT;
- not yet run through the full BLER gate or high-noise negative control;
- no inventory status change;
- no production constant-time, security, PQ, or 7th-source claim.

## Next Step

Add a high-noise negative control for the fixed-i64 wrapper and then move from
small deterministic smoke to N=2048/K=256 comparison before considering any
default decoder wiring.

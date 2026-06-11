# Codex P2 Rust ML Brute-Force Smoke

**Date:** 2026-06-11
**Actor:** Codex
**Directive:** `meta/2026-06-12-CLAUDE-to-CODEX-next-P1b-P2.md` P2
**Discipline:** Sound Verifier. No 7th; no break; no security claim. OPEN = LSN.

## Scope

This increment starts the P2 scale-cryptanalysis track with a reproducible Rust harness:

- enumerate `Sp(2n,F2)` Lagrangians by transvection orbit;
- generate noisy public membership samples `(a, b = 1_L(a) xor e)`;
- score every Lagrangian candidate by maximum agreement;
- emit raw JSON with explicit threat model and seed.

This is a harness smoke, not a new asymptotic claim. It does not yet improve on Kimi's
`n=3,4,5` Python curve; it creates the Rust path needed for stronger follow-up runs.

## RED/GREEN Tests

Command:

```bash
cargo test --manifest-path impl/lsn_cryptanalysis/Cargo.toml
```

Status: GREEN, 6 tests passing.

Pinned checks:

- `n=2` and `n=3` transvection-orbit counts match `15` and `135`;
- noiseless ML recovers the secret at `n=3`;
- random labels do not look like clean LSN;
- noisy sampler is seed-reproducible;
- trial runner and JSON output carry the threat model and success rate.

## Smoke Sweep

Command:

```bash
cargo run --manifest-path impl/lsn_cryptanalysis/Cargo.toml --release --bin lsn_ml_sweep -- \
  --n-start 3 \
  --n-end 4 \
  --ratios 0.5,1.0,2.0 \
  --p 0.25 \
  --trials 20 \
  --seed 3235823838 \
  --output experiments/128-codex-p2-rust-ml-bruteforce-smoke.json
```

Raw data: `experiments/128-codex-p2-rust-ml-bruteforce-smoke.json`.

| n | |Lagr| | m | m / 2^(2n) | p | trials | successes | success rate |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 | 135 | 32 | 0.5 | 0.25 | 20 | 2 | 0.10 |
| 3 | 135 | 64 | 1.0 | 0.25 | 20 | 11 | 0.55 |
| 3 | 135 | 128 | 2.0 | 0.25 | 20 | 16 | 0.80 |
| 4 | 2295 | 128 | 0.5 | 0.25 | 20 | 5 | 0.25 |
| 4 | 2295 | 256 | 1.0 | 0.25 | 20 | 12 | 0.60 |
| 4 | 2295 | 512 | 2.0 | 0.25 | 20 | 19 | 0.95 |

## Interpretation

The smoke data tracks the expected `2^(2n)` brute-force ML threshold shape at `n=3,4`, matching
the already-adjudicated Kimi trend direction. Because this run uses only 20 trials and stops at
`n=4`, it is only a Rust harness validation.

Honest status:

- **BROKEN:** no;
- **REDUCES / attack success:** no;
- **OPEN evidence:** unchanged; this is implementation groundwork only.

## Next Step

Optimize the ML scorer for `n=5` and then move to one genuinely new P2 item:

1. packed membership tables / bitset scoring to reproduce `n=5` at higher trials in Rust;
2. span-of-positives negative control at `p=1/4`;
3. BKW/ISD adaptation screen with low-noise sanity and constant-rate failure control.

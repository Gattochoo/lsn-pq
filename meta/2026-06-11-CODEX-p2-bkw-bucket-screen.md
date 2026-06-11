# Codex P2 BKW Bucket-Pair Screen

**Date:** 2026-06-11
**Actor:** Codex
**Directive:** P2 scale cryptanalysis harness; BKW/ISD adaptation screen
**Discipline:** Sound Verifier. No 7th; no break; no security claim. OPEN = LSN.

## Scope

This increment leaves the exhaustive Lagrangian/ISD scorer track and tests a non-enumerative
BKW-style observable.

Implementation:

- added `random_lagrangian(n, walk_steps, rng)`, a transvection-walk generator that avoids
  enumerating the Lagrangian orbit;
- added `bkw_bucket_observable`, which buckets samples by public coordinate bits, pairs samples
  inside each bucket, and measures label-xor and secret-delta diagnostic statistics;
- added `run_bkw_bucket_trials` and `lsn_bkw_sweep`;
- raw secret membership is used only for diagnostic enrichment measurement, not as an attacker input.

Threat model remains public points plus noisy membership labels.

## RED/GREEN Tests

RED was confirmed by adding tests for the new API before implementation:

- `random_lagrangian_walk_preserves_isotropic_subspace`;
- `bkw_bucket_runner_has_noiseless_positive_control`.

Initial failure:

```text
unresolved imports `lsn_cryptanalysis::random_lagrangian`,
`lsn_cryptanalysis::run_bkw_bucket_trials`
```

GREEN:

```bash
cargo test --manifest-path impl/lsn_cryptanalysis/Cargo.toml
```

Status: 16 tests passing.

## Sweep

Command:

```bash
cargo run --manifest-path impl/lsn_cryptanalysis/Cargo.toml --release --bin lsn_bkw_sweep -- \
  --n-start 4 \
  --n-end 8 \
  --ratios 1.0 \
  --p-values 0.0,0.25,0.5 \
  --trials 20 \
  --bucket-bits 6 \
  --pair-limit 512 \
  --seed 3235823838 \
  --output experiments/133-codex-p2-bkw-bucket-screen.json
```

Raw data: `experiments/133-codex-p2-bkw-bucket-screen.json`.

The main diagnostic is

```text
gap = Pr[delta in L | paired labels equal] - Pr[delta in L | paired labels unequal].
```

It is not an attack by itself, but it asks whether bucket pairing leaves a secret-aligned
signal that might plausibly feed a structural decoder.

| n | m | p | avg pairs | label-xor excess over matched random | delta gap |
|---:|---:|---:|---:|---:|---:|
| 4 | 256 | 0.00 | 514.2 | -0.029529 | 0.306641 |
| 5 | 1024 | 0.00 | 8174.6 | -0.002882 | 0.086720 |
| 6 | 4096 | 0.00 | 32768.0 | -0.000874 | 0.030545 |
| 7 | 16384 | 0.00 | 32768.0 | 0.000882 | 0.009674 |
| 8 | 65536 | 0.00 | 32768.0 | 0.000046 | 0.004536 |
| 4 | 256 | 0.25 | 512.9 | -0.004606 | 0.021488 |
| 5 | 1024 | 0.25 | 8196.4 | 0.002257 | 0.005040 |
| 6 | 4096 | 0.25 | 32768.0 | -0.001821 | 0.000625 |
| 7 | 16384 | 0.25 | 32768.0 | -0.003498 | 0.000211 |
| 8 | 65536 | 0.25 | 32768.0 | 0.008431 | 0.000074 |
| 4 | 256 | 0.50 | 511.5 | 0.004734 | 0.001731 |
| 5 | 1024 | 0.50 | 8180.1 | 0.000606 | 0.000712 |
| 6 | 4096 | 0.50 | 32768.0 | -0.000419 | -0.000505 |
| 7 | 16384 | 0.50 | 32768.0 | 0.001220 | 0.000180 |
| 8 | 65536 | 0.50 | 32768.0 | 0.000598 | -0.000111 |

## Interpretation

The p=0 positive control works: bucket pairing can create a secret-delta enrichment when labels are
clean. The enrichment falls quickly with n because the underlying membership event is sparse.

At p=1/4, the same diagnostic collapses toward the random-label p=1/2 control:

- n=4 shows a visible finite-size gap;
- n=5 is already small;
- n=6..8 are near the matched-random floor for this one-round observable;
- label-xor excess over a matched Bernoulli control is small and seed/noise-scale rather than a
  clear structural advantage.

This is **not** a REDUCES result and not an attack success:

- no secret recovery is attempted;
- no candidate Lagrangian enumeration is used;
- the only remaining signal is a rapidly decaying diagnostic enrichment;
- the p=1/4 layer does not preserve the p=0 BKW-style structure at this scale.

Honest status:

- **BROKEN:** no;
- **REDUCES / scalable attack success:** no;
- **positive control:** yes, at p=0;
- **constant-rate BKW one-round signal:** not found;
- **OPEN evidence:** modestly strengthened against this BKW bucket family.

## Next Step

Two useful follow-ups remain:

1. Write a small BKW noise-growth/cost model note: after one label-xor round,
   `p -> 2p(1-p)`, so `p=1/4` jumps to `3/8`; further rounds approach `1/2`.
2. If continuing implementation, test a multi-round bucket transform only as a negative control and
   report its noise blow-up explicitly, not as a recovery attack unless it beats the `2^(2n)` rail.

# Codex P2 BKW Noise-Growth Model

**Date:** 2026-06-11
**Actor:** Codex
**Directive:** Follow-up to `2026-06-11-CODEX-p2-bkw-bucket-screen.md`
**Discipline:** Sound Verifier. No 7th; no break; no security claim. OPEN = LSN.

## Scope

This increment pins the analytic noise-cost reason why the one-round BKW bucket screen did not
produce a constant-rate structural attack.

For independent Bernoulli noise bits, a BKW label-xor step has recurrence

```text
p_{r+1} = Pr[e1 xor e2 = 1] = 2 p_r (1 - p_r)
```

Equivalently, the bias `b_r = 1 - 2p_r` obeys

```text
b_{r+1} = b_r^2.
```

So after `r` rounds, the useful label bias is `(1-2p)^(2^r)`.

Implementation:

- added `bkw_xor_noise_rate`;
- added `bkw_noise_after_rounds`;
- added `bkw_noise_model` and JSON serialization;
- added `lsn_bkw_noise_model` CLI.

## RED/GREEN Tests

RED was confirmed by adding `bkw_xor_noise_recurrence_squares_bias` before implementation.
The expected unresolved imports were:

```text
no `bkw_noise_after_rounds` in the root
no `bkw_xor_noise_rate` in the root
```

GREEN:

```bash
cargo test --manifest-path impl/lsn_cryptanalysis/Cargo.toml bkw_xor_noise_recurrence_squares_bias
```

The test pins:

- `p=0 -> 0`;
- `p=1/2 -> 1/2`;
- `p=1/4 -> 3/8 -> 15/32 -> 255/512`.

## Model Run

Command:

```bash
cargo run --manifest-path impl/lsn_cryptanalysis/Cargo.toml --release --bin lsn_bkw_noise_model -- \
  --p-values 0.1,0.25,0.3,0.375 \
  --max-rounds 6 \
  --output experiments/134-codex-p2-bkw-noise-growth-model.json
```

Raw data: `experiments/134-codex-p2-bkw-noise-growth-model.json`.

Selected rows:

| p0 | rounds | xor width | effective p | bias | signal retention |
|---:|---:|---:|---:|---:|---:|
| 0.10 | 0 | 1 | 0.1000000000 | 0.8000000000 | 0.8000000000 |
| 0.10 | 1 | 2 | 0.1800000000 | 0.6400000000 | 0.6400000000 |
| 0.10 | 2 | 4 | 0.2952000000 | 0.4096000000 | 0.4096000000 |
| 0.10 | 3 | 8 | 0.4161139200 | 0.1677721600 | 0.1677721600 |
| 0.10 | 4 | 16 | 0.4859262512 | 0.0281474977 | 0.0281474977 |
| 0.25 | 0 | 1 | 0.2500000000 | 0.5000000000 | 0.5000000000 |
| 0.25 | 1 | 2 | 0.3750000000 | 0.2500000000 | 0.2500000000 |
| 0.25 | 2 | 4 | 0.4687500000 | 0.0625000000 | 0.0625000000 |
| 0.25 | 3 | 8 | 0.4980468750 | 0.0039062500 | 0.0039062500 |
| 0.25 | 4 | 16 | 0.4999923706 | 0.0000152588 | 0.0000152588 |

## Interpretation

This explains the previous bucket-pair experiment:

- clean labels (`p=0`) can preserve bucket-pair structure;
- at `p=1/4`, a single xor round already moves the effective noise to `3/8`;
- two rounds move it to `15/32`;
- three rounds leave only `1/256` label bias;
- four rounds leave only `1/65536` label bias.

Thus any multi-round BKW adaptation must overcome a bias-squaring wall before it can exploit
Lagrangian structure. The current one-round bucket observable found no such compensating structural
gain at n=6..8, and this model says further rounds get substantially harder, not easier.

Honest status:

- **BROKEN:** no;
- **REDUCES / scalable attack success:** no;
- **BKW cost/noise obstruction:** pinned for the standard label-xor transform;
- **OPEN evidence:** modestly strengthened against straightforward BKW adaptations.

## Next Step

The next implementation step should move away from straightforward label-xor BKW unless a new
observable avoids bias squaring. Two viable directions:

1. scale ML/brute-force threshold beyond n=5 using non-enumerative random-secret generation plus
   sampled candidate baselines;
2. test a disagreement/certificate map that does not xor labels and therefore does not immediately
   square the noise bias.

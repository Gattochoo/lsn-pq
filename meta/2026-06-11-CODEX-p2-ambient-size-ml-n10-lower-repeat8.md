# CODEX note: P2 ambient-size ML n=10 lower-cell repeat

Date: 2026-06-11 KST

## Scope

This repeats the likely lower/transitional n=10 cell identified in
`2026-06-11-CODEX-p2-ambient-size-ml-n10-cost-pilot.md`.

Threat model:

- attacker-visible input: public points and noisy membership labels,
- experimental helper: the true Lagrangian is planted as candidate 0 among
  random Lagrangian decoys,
- purpose: measure ML score separation against a random candidate cloud of size
  `2^(2n)` without full Lagrangian-orbit enumeration.

This remains a planted-candidate score-landscape calibration. It is not public
recovery, not a proof, and not a security claim.

## Artifact

Raw JSON:

- `experiments/162-codex-p2-ambient-size-ml-n10-lower-repeat8.json`

Command:

```bash
cargo run --manifest-path impl/lsn_cryptanalysis/Cargo.toml --release --bin lsn_sampled_ambient_ml_sweep -- \
  --n-start 10 \
  --n-end 10 \
  --ratios 0.015625 \
  --p-values 0.25,0.5 \
  --trials 8 \
  --seed 3235823855 \
  --output experiments/162-codex-p2-ambient-size-ml-n10-lower-repeat8.json
```

Repro check:

```bash
cargo run --manifest-path impl/lsn_cryptanalysis/Cargo.toml --release --bin lsn_sampled_ambient_ml_sweep -- \
  --n-start 10 \
  --n-end 10 \
  --ratios 0.015625 \
  --p-values 0.25,0.5 \
  --trials 8 \
  --seed 3235823855 \
  --output /tmp/162-codex-p2-ambient-size-ml-n10-lower-repeat8.repro.json
cmp -s experiments/162-codex-p2-ambient-size-ml-n10-lower-repeat8.json /tmp/162-codex-p2-ambient-size-ml-n10-lower-repeat8.repro.json
```

The `cmp` check passed.

## Repeat-8 result

Here `R_n = 2^(2n)`, so `R_10 = 1048576`. Wilson intervals use z=1.96.

| n | p | samples | samples / `R_n` | trials | successes | rate | avg margin |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 10 | 0.25 | 16384 | 0.015625 | 8 | 2 | 0.25 | -1.875 |
| 10 | 0.50 | 16384 | 0.015625 | 8 | 0 | 0.00 | -18.625 |

## Aggregate with experiment 161

This combines the earlier 4-trial n=10 lower pilot with this independent
8-trial repeat.

| n | p | samples | samples / `R_n` | trials | successes | rate | Wilson 95% CI | avg margin |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 10 | 0.25 | 16384 | 0.015625 | 12 | 3 | 0.25 | [0.089, 0.532] | -2.583 |
| 10 | 0.50 | 16384 | 0.015625 | 12 | 0 | 0.00 | [0.000, 0.243] | -18.250 |

## Interpretation

- The lower n=10 cell remains low-success after 12 total trials: `3/12` for
  structured `p=0.25`.
- The matched random-label control remains `0/12`, with strongly negative
  average margin.
- Together with the earlier `0.03125 * R_10` pilot cell (`4/4`), this keeps the
  tentative n=10 transition between `0.015625 * R_10` and `0.03125 * R_10`.
- The sample size is still small, and this is only a planted-candidate
  score-landscape calibration. It does not provide a public selector, a
  sub-rail recovery method, or a security claim.

## Next useful step

Before spending more n=10 runtime, add lightweight progress/cell timing output
to `lsn_sampled_ambient_ml_sweep` or run a focused repeat only at
`0.03125 * R_10` if the high-success pilot cell needs a nontrivial confidence
interval.

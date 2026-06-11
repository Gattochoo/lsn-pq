# CODEX note: P2 ambient-size ML n=10 high-cell repeat

Date: 2026-06-11 KST

## Scope

This repeats the high n=10 cell from
`2026-06-11-CODEX-p2-ambient-size-ml-n10-cost-pilot.md`, complementing the
lower-cell repeat in `2026-06-11-CODEX-p2-ambient-size-ml-n10-lower-repeat8.md`.

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

- `experiments/163-codex-p2-ambient-size-ml-n10-high-repeat8.json`

Command:

```bash
cargo run --manifest-path impl/lsn_cryptanalysis/Cargo.toml --release --bin lsn_sampled_ambient_ml_sweep -- \
  --n-start 10 \
  --n-end 10 \
  --ratios 0.03125 \
  --p-values 0.25,0.5 \
  --trials 8 \
  --seed 3235823857 \
  --output experiments/163-codex-p2-ambient-size-ml-n10-high-repeat8.json
```

Repro check:

```bash
cargo run --manifest-path impl/lsn_cryptanalysis/Cargo.toml --release --bin lsn_sampled_ambient_ml_sweep -- \
  --n-start 10 \
  --n-end 10 \
  --ratios 0.03125 \
  --p-values 0.25,0.5 \
  --trials 8 \
  --seed 3235823857 \
  --output /tmp/163-codex-p2-ambient-size-ml-n10-high-repeat8.repro.json
cmp -s experiments/163-codex-p2-ambient-size-ml-n10-high-repeat8.json /tmp/163-codex-p2-ambient-size-ml-n10-high-repeat8.repro.json
```

The `cmp` check passed.

## Repeat-8 result

Here `R_n = 2^(2n)`, so `R_10 = 1048576`. Wilson intervals use z=1.96.

| n | p | samples | samples / `R_n` | trials | successes | rate | avg margin |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 10 | 0.25 | 32768 | 0.03125 | 8 | 7 | 0.875 | 8.250 |
| 10 | 0.50 | 32768 | 0.03125 | 8 | 0 | 0.000 | -27.625 |

## Aggregate with experiment 160

This combines the earlier 4-trial n=10 high pilot with this independent
8-trial repeat.

| n | p | samples | samples / `R_n` | trials | successes | rate | Wilson 95% CI | avg margin |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 10 | 0.25 | 32768 | 0.03125 | 12 | 11 | 0.917 | [0.646, 0.985] | 7.833 |
| 10 | 0.50 | 32768 | 0.03125 | 12 | 0 | 0.000 | [0.000, 0.243] | -28.167 |

## Interpretation

- The high n=10 cell remains high-success after 12 total trials: `11/12` for
  structured `p=0.25`.
- The matched random-label control remains `0/12`, with strongly negative
  average margin.
- Together with the lower-cell aggregate (`3/12` at `0.015625 * R_10`), this
  keeps the tentative n=10 transition bracket between `0.015625 * R_10` and
  `0.03125 * R_10`.
- This is still a small-sample, planted-candidate score-landscape calibration.
  It does not provide a public selector, a sub-rail recovery method, or a
  security claim.

## Next useful step

The n=10 bracket is now balanced at 12 total trials per endpoint. The next
useful implementation step is not another broad sweep, but lightweight
cell-level timing/progress output in `lsn_sampled_ambient_ml_sweep` so future
n=10 or n=11 focused repeats can be budgeted without long silent runs.

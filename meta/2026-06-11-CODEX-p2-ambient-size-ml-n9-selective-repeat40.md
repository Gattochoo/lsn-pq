# CODEX note: P2 ambient-size ML n=9 selective repeat

Date: 2026-06-11 KST

## Scope

This is a selective repeat of the n=9 ambient-size sampled-candidate ML
boundary cells from `2026-06-11-CODEX-p2-ambient-size-ml-n9-lower-boundary.md`.

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

- `experiments/159-codex-p2-ambient-size-ml-n9-selective-repeat40.json`

Command:

```bash
cargo run --manifest-path impl/lsn_cryptanalysis/Cargo.toml --release --bin lsn_sampled_ambient_ml_sweep -- \
  --n-start 9 \
  --n-end 9 \
  --ratios 0.0234375,0.03125,0.0390625 \
  --p-values 0.25,0.5 \
  --trials 40 \
  --seed 3235823849 \
  --output experiments/159-codex-p2-ambient-size-ml-n9-selective-repeat40.json
```

Repro check:

```bash
cargo run --manifest-path impl/lsn_cryptanalysis/Cargo.toml --release --bin lsn_sampled_ambient_ml_sweep -- \
  --n-start 9 \
  --n-end 9 \
  --ratios 0.0234375,0.03125,0.0390625 \
  --p-values 0.25,0.5 \
  --trials 40 \
  --seed 3235823849 \
  --output /tmp/159-codex-p2-ambient-size-ml-n9-selective-repeat40.repro.json
cmp -s experiments/159-codex-p2-ambient-size-ml-n9-selective-repeat40.json /tmp/159-codex-p2-ambient-size-ml-n9-selective-repeat40.repro.json
```

The `cmp` check passed.

## Repeat-40 results

Here `R_n = 2^(2n)`, so `R_9 = 262144`. Wilson intervals use z=1.96.

| n | p | samples | samples / `R_n` | trials | successes | rate | avg margin |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 9 | 0.25 | 6144 | 0.0234375 | 40 | 9 | 0.225 | -3.45 |
| 9 | 0.50 | 6144 | 0.0234375 | 40 | 0 | 0.000 | -16.825 |
| 9 | 0.25 | 8192 | 0.03125 | 40 | 18 | 0.450 | -1.825 |
| 9 | 0.50 | 8192 | 0.03125 | 40 | 0 | 0.000 | -19.075 |
| 9 | 0.25 | 10240 | 0.0390625 | 40 | 26 | 0.650 | 0.925 |
| 9 | 0.50 | 10240 | 0.0390625 | 40 | 0 | 0.000 | -21.375 |

## Aggregate with experiment 158

This combines the earlier 20-trial run with this independent 40-trial repeat.

| n | p | samples | samples / `R_n` | trials | successes | rate | Wilson 95% CI | avg margin |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 9 | 0.25 | 6144 | 0.0234375 | 60 | 15 | 0.250 | [0.158, 0.372] | -2.983 |
| 9 | 0.50 | 6144 | 0.0234375 | 60 | 0 | 0.000 | [0.000, 0.060] | -17.017 |
| 9 | 0.25 | 8192 | 0.03125 | 60 | 26 | 0.433 | [0.316, 0.559] | -1.250 |
| 9 | 0.50 | 8192 | 0.03125 | 60 | 0 | 0.000 | [0.000, 0.060] | -18.983 |
| 9 | 0.25 | 10240 | 0.0390625 | 60 | 39 | 0.650 | [0.524, 0.758] | 1.300 |
| 9 | 0.50 | 10240 | 0.0390625 | 60 | 0 | 0.000 | [0.000, 0.060] | -21.483 |

## Interpretation

- The structured `p=0.25` cells still show a rising score-separation trend
  across the lower n=9 boundary window.
- The `p=0.5` random-label controls remain at `0/60` in all matched cells,
  with Wilson upper bound about `0.060` per cell.
- The lower boundary remains broad but now has a tighter aggregate read:
  `0.0234375 * R_9` is low-success, `0.03125 * R_9` is transitional, and
  `0.0390625 * R_9` is above the midpoint for this planted-candidate
  calibration.
- This is still rail-scale evidence only. It does not provide a public
  selector, a sub-rail recovery method, or a security claim.

## Next useful step

Use smaller focused cells next. The full six-cell repeat at n=9 is costly
enough that future repeats should either:

- increase trials only at the transitional `8192` sample cell, or
- run a narrow n=10 cost pilot with one structured cell and one matched
  `p=0.5` control.

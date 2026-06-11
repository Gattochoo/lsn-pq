# CODEX note: P2 ambient-size ML n=9 boundary replication

Date: 2026-06-11 KST

## Scope

This is a follow-up to `2026-06-11-CODEX-p2-ambient-size-ml-n9-pilot.md`.
It reruns the n=9 ambient-size sampled-candidate ML calibration with more
trials and one extra boundary ratio.

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

- `experiments/157-codex-p2-ambient-size-ml-n9-boundary.json`

Command:

```bash
cargo run --manifest-path impl/lsn_cryptanalysis/Cargo.toml --release --bin lsn_sampled_ambient_ml_sweep -- \
  --n-start 9 \
  --n-end 9 \
  --ratios 0.03125,0.046875,0.0625 \
  --p-values 0.25,0.5 \
  --trials 10 \
  --seed 3235823846 \
  --output experiments/157-codex-p2-ambient-size-ml-n9-boundary.json
```

Repro check:

```bash
cargo run --manifest-path impl/lsn_cryptanalysis/Cargo.toml --release --bin lsn_sampled_ambient_ml_sweep -- \
  --n-start 9 \
  --n-end 9 \
  --ratios 0.03125,0.046875,0.0625 \
  --p-values 0.25,0.5 \
  --trials 10 \
  --seed 3235823846 \
  --output /tmp/157-codex-p2-ambient-size-ml-n9-boundary.repro.json
cmp -s experiments/157-codex-p2-ambient-size-ml-n9-boundary.json /tmp/157-codex-p2-ambient-size-ml-n9-boundary.repro.json
```

The `cmp` check passed.

## Results

Here `R_n = 2^(2n)`, so `R_9 = 262144`. Wilson intervals use z=1.96.

| n | p | samples | samples / `R_n` | trials | successes | rate | Wilson 95% CI | avg margin |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 9 | 0.25 | 8192 | 0.03125 | 10 | 7 | 0.70 | [0.397, 0.892] | 1.20 |
| 9 | 0.50 | 8192 | 0.03125 | 10 | 0 | 0.00 | [0.000, 0.278] | -18.10 |
| 9 | 0.25 | 12288 | 0.046875 | 10 | 7 | 0.70 | [0.397, 0.892] | 1.00 |
| 9 | 0.50 | 12288 | 0.046875 | 10 | 0 | 0.00 | [0.000, 0.278] | -22.50 |
| 9 | 0.25 | 16384 | 0.06250 | 10 | 10 | 1.00 | [0.722, 1.000] | 12.10 |
| 9 | 0.50 | 16384 | 0.06250 | 10 | 0 | 0.00 | [0.000, 0.278] | -26.80 |

## Interpretation

- The structured `p=0.25` cells keep the same rail-scale shape seen at n=8 and
  in the n=9 pilot: separation appears at small constant fractions of
  `2^(2n)`.
- The matched `p=0.5` random-label controls fail in every cell and have strongly
  negative margins.
- The `0.03125` and `0.046875` ratios are still noisy at 10 trials, both at
  `7/10`; the `0.0625` cell is cleaner at `10/10`.
- No public candidate generator is supplied by this experiment. The secret is
  planted in the candidate cloud for score-landscape calibration only.

## Next useful step

If runtime permits, the next most useful refinement is a targeted repeat near
the lower boundary, for example n=9 at ratios `{0.0234375, 0.03125, 0.0390625}`
with 20 trials and matched `p=0.5` controls. That would sharpen the lower edge
without changing the threat-model caveat.

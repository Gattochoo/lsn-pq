# CODEX note: P2 ambient-size ML n=9 lower-boundary refinement

Date: 2026-06-11 KST

## Scope

This refines the lower edge of the n=9 ambient-size sampled-candidate ML
calibration after `2026-06-11-CODEX-p2-ambient-size-ml-n9-boundary.md`.

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

- `experiments/158-codex-p2-ambient-size-ml-n9-lower-boundary.json`

Command:

```bash
cargo run --manifest-path impl/lsn_cryptanalysis/Cargo.toml --release --bin lsn_sampled_ambient_ml_sweep -- \
  --n-start 9 \
  --n-end 9 \
  --ratios 0.0234375,0.03125,0.0390625 \
  --p-values 0.25,0.5 \
  --trials 20 \
  --seed 3235823847 \
  --output experiments/158-codex-p2-ambient-size-ml-n9-lower-boundary.json
```

Repro check:

```bash
cargo run --manifest-path impl/lsn_cryptanalysis/Cargo.toml --release --bin lsn_sampled_ambient_ml_sweep -- \
  --n-start 9 \
  --n-end 9 \
  --ratios 0.0234375,0.03125,0.0390625 \
  --p-values 0.25,0.5 \
  --trials 20 \
  --seed 3235823847 \
  --output /tmp/158-codex-p2-ambient-size-ml-n9-lower-boundary.repro.json
cmp -s experiments/158-codex-p2-ambient-size-ml-n9-lower-boundary.json /tmp/158-codex-p2-ambient-size-ml-n9-lower-boundary.repro.json
```

The `cmp` check passed.

## Results

Here `R_n = 2^(2n)`, so `R_9 = 262144`. Wilson intervals use z=1.96.

| n | p | samples | samples / `R_n` | trials | successes | rate | Wilson 95% CI | avg margin |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 9 | 0.25 | 6144 | 0.0234375 | 20 | 6 | 0.30 | [0.145, 0.519] | -2.05 |
| 9 | 0.50 | 6144 | 0.0234375 | 20 | 0 | 0.00 | [0.000, 0.161] | -17.40 |
| 9 | 0.25 | 8192 | 0.03125 | 20 | 8 | 0.40 | [0.219, 0.613] | -0.10 |
| 9 | 0.50 | 8192 | 0.03125 | 20 | 0 | 0.00 | [0.000, 0.161] | -18.80 |
| 9 | 0.25 | 10240 | 0.0390625 | 20 | 13 | 0.65 | [0.433, 0.819] | 2.05 |
| 9 | 0.50 | 10240 | 0.0390625 | 20 | 0 | 0.00 | [0.000, 0.161] | -21.70 |

## Interpretation

- The lower edge is between roughly `0.0234375 * R_9` and `0.0390625 * R_9`
  for this planted-candidate ML calibration.
- The structured `p=0.25` cells move from `6/20` to `8/20` to `13/20` as the
  sample ratio increases.
- The matched `p=0.5` random-label controls fail in all cells (`0/20`) and keep
  strongly negative margins.
- This continues the rail-scale pattern rather than introducing a public
  selector or a sub-rail recovery method.

## Next useful step

The next refinement would be a selective repeat of only the structured
`p=0.25` lower-edge cells with more trials, or a higher-n cost pilot. Avoid
starting a new attack family unless the threat model and controls are explicit.

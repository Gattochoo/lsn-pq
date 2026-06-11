# CODEX note: P2 ambient-size ML n=10 cost pilot

Date: 2026-06-11 KST

## Scope

This is a narrow n=10 cost pilot for the ambient-size sampled-candidate ML
calibration, following the n=9 lower-boundary repeats.

Threat model:

- attacker-visible input: public points and noisy membership labels,
- experimental helper: the true Lagrangian is planted as candidate 0 among
  random Lagrangian decoys,
- purpose: measure ML score separation against a random candidate cloud of size
  `2^(2n)` without full Lagrangian-orbit enumeration.

This remains a planted-candidate score-landscape calibration. It is not public
recovery, not a proof, and not a security claim.

## Artifacts

Raw JSON:

- `experiments/160-codex-p2-ambient-size-ml-n10-cost-pilot.json`
- `experiments/161-codex-p2-ambient-size-ml-n10-lower-cost-pilot.json`

Commands:

```bash
cargo run --manifest-path impl/lsn_cryptanalysis/Cargo.toml --release --bin lsn_sampled_ambient_ml_sweep -- \
  --n-start 10 \
  --n-end 10 \
  --ratios 0.03125 \
  --p-values 0.25,0.5 \
  --trials 4 \
  --seed 3235823851 \
  --output experiments/160-codex-p2-ambient-size-ml-n10-cost-pilot.json

cargo run --manifest-path impl/lsn_cryptanalysis/Cargo.toml --release --bin lsn_sampled_ambient_ml_sweep -- \
  --n-start 10 \
  --n-end 10 \
  --ratios 0.015625 \
  --p-values 0.25,0.5 \
  --trials 4 \
  --seed 3235823853 \
  --output experiments/161-codex-p2-ambient-size-ml-n10-lower-cost-pilot.json
```

Repro checks:

```bash
cargo run --manifest-path impl/lsn_cryptanalysis/Cargo.toml --release --bin lsn_sampled_ambient_ml_sweep -- \
  --n-start 10 \
  --n-end 10 \
  --ratios 0.03125 \
  --p-values 0.25,0.5 \
  --trials 4 \
  --seed 3235823851 \
  --output /tmp/160-codex-p2-ambient-size-ml-n10-cost-pilot.repro.json

cargo run --manifest-path impl/lsn_cryptanalysis/Cargo.toml --release --bin lsn_sampled_ambient_ml_sweep -- \
  --n-start 10 \
  --n-end 10 \
  --ratios 0.015625 \
  --p-values 0.25,0.5 \
  --trials 4 \
  --seed 3235823853 \
  --output /tmp/161-codex-p2-ambient-size-ml-n10-lower-cost-pilot.repro.json

cmp -s experiments/160-codex-p2-ambient-size-ml-n10-cost-pilot.json /tmp/160-codex-p2-ambient-size-ml-n10-cost-pilot.repro.json
cmp -s experiments/161-codex-p2-ambient-size-ml-n10-lower-cost-pilot.json /tmp/161-codex-p2-ambient-size-ml-n10-lower-cost-pilot.repro.json
```

Both `cmp` checks passed.

## Results

Here `R_n = 2^(2n)`, so `R_10 = 1048576`. Wilson intervals use z=1.96.
Because this is only a 4-trial pilot, the intervals are wide; read this as a
cost and direction check, not a stable boundary estimate.

| n | p | samples | samples / `R_n` | trials | successes | rate | Wilson 95% CI | avg margin |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 10 | 0.25 | 16384 | 0.015625 | 4 | 1 | 0.25 | [0.046, 0.699] | -4.00 |
| 10 | 0.50 | 16384 | 0.015625 | 4 | 0 | 0.00 | [0.000, 0.490] | -17.50 |
| 10 | 0.25 | 32768 | 0.03125 | 4 | 4 | 1.00 | [0.510, 1.000] | 7.00 |
| 10 | 0.50 | 32768 | 0.03125 | 4 | 0 | 0.00 | [0.000, 0.490] | -29.25 |

## Interpretation

- The n=10 pilot is computationally feasible at one or two focused cells, but
  the full six-cell n=9 repeat pattern should not be blindly scaled upward.
- The structured `p=0.25` cells separate between the two tested ratios:
  `0.015625 * R_10` is low-success in this seed, while `0.03125 * R_10` is
  high-success in this seed.
- The matched `p=0.5` random-label controls fail in both cells (`0/4`) and keep
  negative margins.
- This continues the rail-scale planted-candidate ML picture. It does not
  provide a public selector, a sub-rail recovery method, or a security claim.

## Next useful step

If more n=10 data is worth spending, repeat only the likely transitional
`0.015625 * R_10` cell and its `p=0.5` control with more trials. Do not broaden
to many ratios before that focused repeat is justified by runtime budget.

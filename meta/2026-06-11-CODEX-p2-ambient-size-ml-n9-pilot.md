# CODEX note: P2 ambient-size ML n=9 pilot

Date: 2026-06-11 KST

## Scope

This is a small high-n pilot for the P2 ambient-size sampled-candidate ML rail.
It extends the existing n=6..8 calibration by one dimension point, but with
only 3 trials per cell. It is a cost/shape probe, not a paper-ready statistical
table.

Threat model:

- attacker-visible input: public points and noisy membership labels,
- helper used by this experiment: the true Lagrangian is planted as candidate 0
  among random Lagrangian decoys,
- purpose: measure ML score separation against a random candidate cloud of size
  `2^(2n)` without full Lagrangian-orbit enumeration.

This is not a public recovery method, not a proof, and not a security claim.

## Artifact

Raw JSON:

- `experiments/156-codex-p2-ambient-size-ml-n9-pilot.json`

Command:

```bash
cargo run --manifest-path impl/lsn_cryptanalysis/Cargo.toml --release --bin lsn_sampled_ambient_ml_sweep -- \
  --n-start 9 \
  --n-end 9 \
  --ratios 0.03125,0.0625 \
  --p-values 0.25,0.5 \
  --trials 3 \
  --seed 3235823845 \
  --output experiments/156-codex-p2-ambient-size-ml-n9-pilot.json
```

Repro check:

```bash
cargo run --manifest-path impl/lsn_cryptanalysis/Cargo.toml --release --bin lsn_sampled_ambient_ml_sweep -- \
  --n-start 9 \
  --n-end 9 \
  --ratios 0.03125,0.0625 \
  --p-values 0.25,0.5 \
  --trials 3 \
  --seed 3235823845 \
  --output /tmp/156-codex-p2-ambient-size-ml-n9-pilot.repro.json
cmp -s experiments/156-codex-p2-ambient-size-ml-n9-pilot.json /tmp/156-codex-p2-ambient-size-ml-n9-pilot.repro.json
```

The `cmp` check passed.

## Results

Here `R_n = 2^(2n)`, so `R_9 = 262144`.

| n | p | samples | samples / `R_n` | trials | successes | success rate | avg margin |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 9 | 0.25 | 8192 | 0.03125 | 3 | 2 | 0.6667 | 1.6667 |
| 9 | 0.50 | 8192 | 0.03125 | 3 | 0 | 0.0000 | -18.6667 |
| 9 | 0.25 | 16384 | 0.06250 | 3 | 3 | 1.0000 | 14.0000 |
| 9 | 0.50 | 16384 | 0.06250 | 3 | 0 | 0.0000 | -21.6667 |

## Interpretation

- The structured `p=0.25` cells retain the same rail-scale shape seen at n=8:
  separation appears at small constant fractions of `2^(2n)`.
- The matched `p=0.5` random-label control fails in both cells and has strongly
  negative average margins.
- With only 3 trials per cell, this is not a stable threshold estimate. Its
  main value is that the existing Rust harness can reach the n=9 ambient-sized
  candidate cloud (`262144` candidates) and still produce reproducible data.

## Next useful step

If this lane continues, the useful upgrade is not a new attack family. It is a
larger n=9 boundary replication, for example trials 20 at ratios
`{0.03125, 0.046875, 0.0625}` plus a matched `p=0.5` control, subject to runtime
budget.

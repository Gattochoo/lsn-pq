# Codex P2 Sampled-Candidate False-Max Control

**Date:** 2026-06-11
**Actor:** Codex
**Directive:** Follow-up to `2026-06-11-CODEX-p2-sampled-candidate-131k-stress.md`
**Discipline:** Sound Verifier. No 7th; no break; no security claim. OPEN = LSN.

## Scope

Experiment 139 measured planted-candidate ML separation with the true Lagrangian inserted into a
random decoy set. This increment removes that planted candidate from the candidate set and scores it
only as an external reference:

```text
candidate set = all random decoy Lagrangians
secret score = computed only for comparison
false max = max score among decoys
margin = secret_score - false_max
```

This tests whether the observed finite-candidate separation is explained by the decoy false-max
distribution itself, rather than by an accidental artifact of including the secret in the candidate
array.

Raw data: `experiments/140-codex-p2-sampled-candidate-false-max-control.json`.

## RED/GREEN

RED was confirmed by adding `sampled_candidate_false_max_runner_excludes_secret_candidate` before
the implementation. The expected failure was:

```text
no `run_sampled_candidate_false_max_budget_trials` in the root
```

GREEN:

```bash
cargo test --manifest-path impl/lsn_cryptanalysis/Cargo.toml \
  sampled_candidate_false_max_runner_excludes_secret_candidate
```

The test pins nested decoy candidate counts and verifies the noiseless secret reference score remains
above the all-random false max.

## Command

```bash
cargo run --manifest-path impl/lsn_cryptanalysis/Cargo.toml --release --bin lsn_sampled_false_max_sweep -- \
  --n-start 10 \
  --n-end 10 \
  --ratios 0.0625,0.125 \
  --p-values 0.25,0.5 \
  --trials 3 \
  --candidate-values 32768,131072 \
  --seed 3235823840 \
  --output experiments/140-codex-p2-sampled-candidate-false-max-control.json
```

## Results

| n | m | p | decoy candidates | false-max control margin | 139 planted margin |
|---:|---:|---:|---:|---:|---:|
| 10 | 65536 | 0.25 | 32768 | 34.7 | 35.0 |
| 10 | 65536 | 0.25 | 131072 | 32.7 | 32.3 |
| 10 | 131072 | 0.25 | 32768 | 82.7 | 76.3 |
| 10 | 131072 | 0.25 | 131072 | 78.3 | 72.3 |
| 10 | 65536 | 0.50 | 32768 | -31.7 | -37.3 |
| 10 | 65536 | 0.50 | 131072 | -31.7 | -40.7 |
| 10 | 131072 | 0.50 | 32768 | -46.7 | -36.0 |
| 10 | 131072 | 0.50 | 131072 | -48.7 | -39.7 |

## Interpretation

The all-random false-max control closely tracks the planted-candidate experiment:

- at `p=1/4`, the external secret reference score remains above the decoy false max at both ratios
  and both candidate counts;
- increasing the decoy count from `32768` to `131072` lowers the margin, as expected from the
  extreme-value model;
- at `p=1/2`, the reference secret score falls below the false max, matching the random-label
  failure control;
- the similarity to experiment 139 suggests that the planted-candidate success is ordinary
  finite-candidate ML separation, not a candidate-array artifact.

This also clarifies the limitation: even if the reference secret score is separated from random
decoys, a public attacker is not given that reference Lagrangian. The experiment estimates a score
landscape, not a public search map.

## Adjudication

- **BROKEN:** no.
- **REDUCES:** no.
- **Public selector:** not found.
- **Control result:** positive; the false-max distribution explains the planted-candidate stress.
- **OPEN:** unchanged for LSN.

## Next Step

Move away from random-decoy calibration and toward a public search barrier:

```text
Estimate how many random decoy candidates would be required before the p=1/4 false max overtakes
the secret reference at n=10, using the extreme-value model plus a small empirical ladder.
```

If the extrapolated decoy count is exponential in `n`, it supports the current P2 reading that
random candidate search is not a public polynomial attack.

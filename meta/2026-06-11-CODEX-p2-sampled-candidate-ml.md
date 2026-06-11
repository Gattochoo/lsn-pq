# Codex P2 Sampled-Candidate ML Screen

**Date:** 2026-06-11
**Actor:** Codex
**Directive:** Follow-up to `2026-06-11-CODEX-p2-bucket-certificate-screen.md`
**Discipline:** Sound Verifier. No 7th; no break; no security claim. OPEN = LSN.

## Scope

This increment tests ML score separation beyond the full-orbit enumeration regime.

Instead of enumerating all Lagrangians, each trial:

1. samples a random secret Lagrangian by transvection walk;
2. plants that secret as candidate 0;
3. samples random Lagrangian decoys;
4. scores only this finite candidate cloud by compact ML.

This is **not** a recovery attack and not an LSN reduction. It measures whether random candidate
clouds show suspicious score behavior before full orbit enumeration becomes infeasible.

Implementation:

- optimized `random_lagrangian` from full-set transvection walks to basis transvection walks plus
  final span expansion;
- added `run_sampled_candidate_ml_trials`;
- added `sampled_candidate_ml_results_to_json`;
- added `lsn_sampled_ml_sweep`.

The candidate count includes the planted secret.

## RED/GREEN Tests

RED was confirmed by adding `sampled_candidate_ml_recovers_noiseless_planted_candidate` before
implementation. The expected unresolved import was:

```text
no `run_sampled_candidate_ml_trials` in the root
```

GREEN:

```bash
cargo test --manifest-path impl/lsn_cryptanalysis/Cargo.toml sampled_candidate_ml_recovers_noiseless_planted_candidate
```

The test verifies noiseless planted recovery for `n=4`, `m=2048`, `candidate_count=32`.

## Sweep

Command:

```bash
cargo run --manifest-path impl/lsn_cryptanalysis/Cargo.toml --release --bin lsn_sampled_ml_sweep -- \
  --n-start 6 \
  --n-end 10 \
  --ratios 0.25,1.0,4.0 \
  --p-values 0.0,0.25,0.5 \
  --trials 5 \
  --candidate-count 512 \
  --seed 3235823838 \
  --output experiments/136-codex-p2-sampled-candidate-ml.json
```

Raw data: `experiments/136-codex-p2-sampled-candidate-ml.json`.

Selected `p=1/4` rows:

| n | m / 2^(2n) | candidates | success rate | avg secret margin |
|---:|---:|---:|---:|---:|
| 6 | 0.25 | 512 | 0.80 | 4.4 |
| 6 | 1.00 | 512 | 1.00 | 37.6 |
| 6 | 4.00 | 512 | 1.00 | 186.2 |
| 7 | 0.25 | 512 | 1.00 | 14.0 |
| 7 | 1.00 | 512 | 1.00 | 95.4 |
| 7 | 4.00 | 512 | 1.00 | 439.6 |
| 8 | 0.25 | 512 | 1.00 | 39.8 |
| 8 | 1.00 | 512 | 1.00 | 216.8 |
| 8 | 4.00 | 512 | 1.00 | 906.0 |
| 9 | 0.25 | 512 | 1.00 | 89.2 |
| 9 | 1.00 | 512 | 1.00 | 446.6 |
| 9 | 4.00 | 512 | 1.00 | 1865.4 |
| 10 | 0.25 | 512 | 1.00 | 193.0 |
| 10 | 1.00 | 512 | 1.00 | 918.2 |
| 10 | 4.00 | 512 | 1.00 | 3910.6 |

Controls:

- p=0 succeeds for all n/ratios;
- p=1/2 fails for all n/ratios, with negative planted margin.

## Interpretation

The sampled-candidate cloud behaves as a clean sanity test:

- with only 512 decoys, the planted secret separates reliably at `p=1/4` once n is moderate;
- p=1/2 destroys the planted advantage, so the score is using the LSN label signal rather than a
  candidate-generation artifact;
- the margin grows with n at fixed `m / 2^(2n)` because the candidate cloud is fixed-size while the
  sampled ambient structure becomes easier to distinguish from random decoys.

This is **not** a REDUCES result:

- the secret is planted into the candidate set;
- candidate_count is fixed at 512, not the full Lagrangian orbit;
- no public candidate generator is shown to include the true secret with useful probability;
- no full recovery, selector, or reduction is claimed.

Honest status:

- **BROKEN:** no;
- **REDUCES / scalable attack success:** no;
- **sampled-cloud sanity:** passes;
- **sub-`2^(2n)` public recovery:** not tested and not found;
- **OPEN evidence:** unchanged for full LSN, but useful as a scalable ML harness component.

## Next Step

The next useful implementation increment is candidate-count scaling at fixed n and p:

- run `candidate_count` in `{512, 2048, 8192, 32768}`;
- use n=8 or n=10, p=1/4, ratios below and around `2^(2n)`;
- report work as candidate-cloud ML only, not a recovery attack.

This asks whether the observed easy partial-cloud behavior degrades with the expected extreme-value
pressure as the decoy set grows.

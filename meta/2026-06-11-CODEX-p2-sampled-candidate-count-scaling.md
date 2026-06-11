# Codex P2 Sampled-Candidate Count Scaling

**Date:** 2026-06-11
**Actor:** Codex
**Directive:** Follow-up to `2026-06-11-CODEX-p2-sampled-candidate-ml.md`
**Discipline:** Sound Verifier. No 7th; no break; no security claim. OPEN = LSN.

## Scope

The previous sampled-candidate ML screen used a fixed `candidate_count=512`. This increment tests
whether the planted-secret ML separation degrades as the decoy cloud grows.

Implementation refinements:

- added `run_sampled_candidate_ml_budget_trials`;
- the runner reuses the same secret/sample instance and the same random-decoy prefix across candidate
  counts, so only candidate-count pressure changes;
- extended `lsn_sampled_ml_sweep` with `--candidate-values`;
- kept `--candidate-count` as a single-count compatibility path.

This remains a planted-candidate experiment, not public recovery. The true secret is explicitly
included as candidate 0.

## RED/GREEN Tests

RED was confirmed by adding `sampled_candidate_budget_runner_preserves_candidate_counts` before
implementation. After fixing a seed typo in the test, the expected failure was:

```text
no `run_sampled_candidate_ml_budget_trials` in the root
```

GREEN:

```bash
cargo test --manifest-path impl/lsn_cryptanalysis/Cargo.toml sampled_candidate_budget_runner_preserves_candidate_counts
```

The test verifies same-run candidate-count outputs for `candidate_count in {16,64}` in a noiseless
sanity case.

## Sweep

Command:

```bash
cargo run --manifest-path impl/lsn_cryptanalysis/Cargo.toml --release --bin lsn_sampled_ml_sweep -- \
  --n-start 8 \
  --n-end 10 \
  --ratios 0.0625,0.125,0.25 \
  --p-values 0.25,0.5 \
  --trials 3 \
  --candidate-values 512,2048,8192,32768 \
  --seed 3235823838 \
  --output experiments/137-codex-p2-sampled-candidate-count-scaling.json
```

Raw data: `experiments/137-codex-p2-sampled-candidate-count-scaling.json`.

Selected `p=1/4`, `candidate_count=32768` rows:

| n | m / 2^(2n) | success rate | avg secret margin |
|---:|---:|---:|---:|
| 8 | 0.0625 | 0.00 | -4.3 |
| 8 | 0.1250 | 1.00 | 9.3 |
| 8 | 0.2500 | 1.00 | 23.3 |
| 9 | 0.0625 | 1.00 | 9.0 |
| 9 | 0.1250 | 1.00 | 24.7 |
| 9 | 0.2500 | 1.00 | 81.0 |
| 10 | 0.0625 | 1.00 | 32.7 |
| 10 | 0.1250 | 1.00 | 82.0 |
| 10 | 0.2500 | 1.00 | 179.3 |

`p=1/2`, `candidate_count=32768` control:

| n | m / 2^(2n) | success rate | avg secret margin |
|---:|---:|---:|---:|
| 8 | 0.0625 | 0.00 | -15.3 |
| 8 | 0.1250 | 0.00 | -24.7 |
| 8 | 0.2500 | 0.00 | -29.0 |
| 9 | 0.0625 | 0.00 | -22.3 |
| 9 | 0.1250 | 0.00 | -39.7 |
| 9 | 0.2500 | 0.00 | -56.3 |
| 10 | 0.0625 | 0.00 | -29.0 |
| 10 | 0.1250 | 0.00 | -60.0 |
| 10 | 0.2500 | 0.00 | -76.7 |

## Interpretation

Candidate-count pressure is visible but does not erase the planted signal at moderate n:

- n=8, `m/2^(2n)=0.0625`, and 32768 candidates fails: finite-size/low-sample pressure is visible;
- n=8 recovers by ratio 0.125;
- n=9 and n=10 succeed even at ratio 0.0625 for this planted 32768-candidate cloud;
- p=1/2 control always fails and has negative planted margin, so the score separation is label-signal
  driven, not a candidate-generation artifact.

This is still **not** a REDUCES result:

- the true secret is planted into the candidate cloud;
- candidate cloud size 32768 is far below the full Lagrangian orbit;
- no public method is shown for generating a cloud containing the true secret with useful probability;
- no recovery attack is claimed.

Honest status:

- **BROKEN:** no;
- **REDUCES / scalable attack success:** no;
- **sampled-cloud signal under 32768 decoys:** yes;
- **public recovery / selector:** not found;
- **OPEN evidence:** unchanged for full LSN, but the ML harness is now suitable for larger
  candidate-cloud stress tests.

## Next Step

Two useful follow-ups:

1. analytic extreme-value note for random decoy ML maxima, comparing observed margins with a
   binomial/Gaussian tail model;
2. n=10 candidate-count stress to `131072` at fewer ratios/trials, if memory remains acceptable,
   still reported strictly as planted-candidate ML.

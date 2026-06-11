# Codex P2 Sampled-Candidate Extreme-Value Model

**Date:** 2026-06-11
**Actor:** Codex
**Directive:** Follow-up to `2026-06-11-CODEX-p2-sampled-candidate-count-scaling.md`
**Discipline:** Sound Verifier. No 7th; no break; no security claim. OPEN = LSN.

## Scope

This increment adds a lightweight interpretation model for the planted-candidate ML sweeps.

For one random decoy Lagrangian `L'`, approximate the per-sample secret-vs-decoy ML score
difference as:

```text
D_i = (1 - 2e_i) * 1[1_L(x_i) != 1_L'(x_i)].
```

The model uses an independent-Lagrangian proxy:

```text
q = 2^-n
disagreement_rate ~= 2q(1-q)
E[D_i] = (1-2p) * disagreement_rate
Var[D_i] = disagreement_rate - E[D_i]^2
```

For `M = candidate_count - 1` random decoys, the best false candidate is approximated by a Gaussian
extreme-value penalty:

```text
predicted_margin = m * E[D_i] - sqrt(m * Var[D_i]) * sqrt(2 log M).
```

This is an interpretation model only. It does not generate candidates, recover secrets, or prove
hardness.

## RED/GREEN Tests

RED was confirmed by adding `sampled_candidate_extreme_value_model_has_noise_control` before
implementation. The expected failure was:

```text
no `sampled_candidate_ml_model_row` in the root
```

GREEN:

```bash
cargo test --manifest-path impl/lsn_cryptanalysis/Cargo.toml sampled_candidate_extreme_value_model_has_noise_control
```

The test pins:

- `p=1/4`, n=10, m=65536, candidate_count=32768 has positive predicted margin;
- `p=1/2` has negative predicted margin;
- increasing candidate_count lowers the predicted margin.

## Model Run

Command:

```bash
cargo run --manifest-path impl/lsn_cryptanalysis/Cargo.toml --release --bin lsn_sampled_ml_model -- \
  --n-start 8 \
  --n-end 10 \
  --ratios 0.0625,0.125,0.25 \
  --p-values 0.25,0.5 \
  --candidate-values 512,2048,8192,32768,131072 \
  --output experiments/138-codex-p2-sampled-candidate-ev-model.json
```

Raw data: `experiments/138-codex-p2-sampled-candidate-ev-model.json`.

## Comparison to Experiment 137

For `p=1/4`, `candidate_count=32768`:

| n | m / 2^(2n) | observed margin | predicted margin |
|---:|---:|---:|---:|
| 8 | 0.0625 | -4.3 | -9.8 |
| 8 | 0.1250 | 9.3 | -4.5 |
| 8 | 0.2500 | 23.3 | 12.3 |
| 9 | 0.0625 | 9.0 | -4.5 |
| 9 | 0.1250 | 24.7 | 12.4 |
| 9 | 0.2500 | 81.0 | 54.9 |
| 10 | 0.0625 | 32.7 | 12.4 |
| 10 | 0.1250 | 82.0 | 55.0 |
| 10 | 0.2500 | 179.3 | 152.6 |

The model is conservative: it underpredicts observed planted margins, especially near the boundary.
It still captures the qualitative transition:

- n=8 low ratio is negative in both model and experiment;
- larger ratios become positive;
- n=10 remains safely positive even at ratio 0.0625;
- increasing candidate_count decreases predicted margin.

For `p=1/2`, the model predicts negative margins, matching the observed all-fail control.

## 131072-Candidate Prediction

The model predicts the following `p=1/4` margins for `candidate_count=131072`:

| n | m / 2^(2n) | predicted margin |
|---:|---:|---:|
| 8 | 0.0625 | -11.4 |
| 8 | 0.1250 | -6.8 |
| 8 | 0.2500 | 9.0 |
| 9 | 0.0625 | -6.8 |
| 9 | 0.1250 | 9.0 |
| 9 | 0.2500 | 50.2 |
| 10 | 0.0625 | 9.1 |
| 10 | 0.1250 | 50.3 |
| 10 | 0.2500 | 146.0 |

This suggests a useful next stress run: n=10, p=1/4, candidate_count=131072, low ratios. It should
still be reported strictly as planted-candidate ML, not public recovery.

## Interpretation

This model supports the current reading of the sampled-candidate experiments:

- candidate-count pressure behaves like an extreme-value effect;
- the p=1/2 control remains negative;
- observed p=1/4 planted margins are compatible with an ordinary ML separation story rather than a
  new public selector.

Honest status:

- **BROKEN:** no;
- **REDUCES / scalable attack success:** no;
- **interpretation model:** useful and conservative;
- **public recovery / selector:** not found;
- **OPEN evidence:** unchanged for full LSN.

## Next Step

Run the predicted n=10 stress point:

```text
n=10, p=1/4, candidate_count=131072, ratios 0.0625 and 0.125, low trials.
```

If it succeeds, the result remains planted-candidate ML. If it fails, the boundary is lower than
the conservative model at that candidate count and should be recorded as finite-size pressure.

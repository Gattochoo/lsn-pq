# Codex P2 Sampled-Candidate 131k Stress

**Date:** 2026-06-11
**Actor:** Codex
**Directive:** Follow-up to `2026-06-11-CODEX-p2-sampled-candidate-ev-model.md`
**Discipline:** Sound Verifier. No 7th; no break; no security claim. OPEN = LSN.

## Scope

This increment runs the stress point predicted by the sampled-candidate extreme-value model:

```text
n = 10
p in {1/4, 1/2}
candidate_count in {32768, 131072}
m / 2^(2n) in {0.0625, 0.125}
trials = 3
```

The experiment still plants the true Lagrangian among random decoys. It measures ML score
separation under finite candidate pressure; it is not a public selector, not a structural reduction,
and not a full LSN recovery attack.

Raw data: `experiments/139-codex-p2-sampled-candidate-131k-stress.json`.

## Command

```bash
cargo run --manifest-path impl/lsn_cryptanalysis/Cargo.toml --release --bin lsn_sampled_ml_sweep -- \
  --n-start 10 \
  --n-end 10 \
  --ratios 0.0625,0.125 \
  --p-values 0.25,0.5 \
  --trials 3 \
  --candidate-values 32768,131072 \
  --seed 3235823839 \
  --output experiments/139-codex-p2-sampled-candidate-131k-stress.json
```

## Results

| n | m | p | candidates | success | observed margin | model margin |
|---:|---:|---:|---:|---:|---:|---:|
| 10 | 65536 | 0.25 | 32768 | 3/3 | 35.0 | 12.4 |
| 10 | 65536 | 0.25 | 131072 | 3/3 | 32.3 | 9.1 |
| 10 | 131072 | 0.25 | 32768 | 3/3 | 76.3 | 55.0 |
| 10 | 131072 | 0.25 | 131072 | 3/3 | 72.3 | 50.3 |
| 10 | 65536 | 0.50 | 32768 | 0/3 | -37.3 | -51.6 |
| 10 | 65536 | 0.50 | 131072 | 0/3 | -40.7 | -54.9 |
| 10 | 131072 | 0.50 | 32768 | 0/3 | -36.0 | -72.9 |
| 10 | 131072 | 0.50 | 131072 | 0/3 | -39.7 | -77.6 |

## Interpretation

The 131072-candidate stress confirms the qualitative prediction from the extreme-value proxy:

- at `p=1/4`, the planted candidate remains separated for `n=10` at both low ratios;
- increasing `candidate_count` from `32768` to `131072` lowers the planted margin, but does not erase
  it in this finite planted-candidate setting;
- at `p=1/2`, the random-label control remains negative and fails in every trial;
- the model remains conservative at `p=1/4`: observed margins exceed the predicted margins.

This is evidence about the planted-candidate ML score landscape only. It does not contradict the
P2/PQ reading: a public attacker is not given the planted candidate set, and this experiment still
does not produce a polynomial public recovery map from raw LSN samples.

## Adjudication

- **BROKEN:** no.
- **REDUCES:** no.
- **Public selector:** not found.
- **Artifact class:** planted-candidate ML calibration.
- **Useful result:** yes, as a finite-candidate score-separation baseline and model cross-check.
- **OPEN:** unchanged for LSN.

## Next Step

The immediate next stress should move one axis closer to the true public problem:

```text
n = 11 or candidate_count >= 2^18 is likely expensive;
instead vary sample ratio downward at n=10, candidate_count=131072,
or add an unplanted all-random candidate control to estimate false-positive maxima directly.
```

The cleaner OFA-sized follow-up is the unplanted all-random control, because it tests whether the
observed finite-candidate margins are fully explained by the false-max distribution without adding a
heavier scaling axis.

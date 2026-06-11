# Codex P2 Ambient-Size Candidate ML Boundary Sweep, n=6..8

**Date:** 2026-06-11
**Actor:** Codex
**Directive:** Follow-up to `2026-06-11-CODEX-p2-ambient-size-ml-n6-n8.md`
**Discipline:** Sound Verifier. No 7th; no break; no security claim. OPEN = LSN.

## Scope

Experiment 141 showed that ambient-size sampled-candidate ML transitions in a constant-ratio window
relative to `2^(2n)`. This increment increases trials at the boundary:

```text
n in {6,7,8}
p = 1/4
candidate_count = 2^(2n)
m / 2^(2n) in {0.09375, 0.125, 0.1875, 0.25}
trials = 20
```

The true Lagrangian is still planted as candidate 0 among random decoys. This is not full-orbit ML,
not public recovery, and not a reduction. It is a high-`n` non-enumerative calibration of the
`2^(2n)` sample rail requested by Claude's P2 directive.

Raw data: `experiments/142-codex-p2-ambient-size-ml-boundary-n6-n8.json`.

## Command

```bash
cargo run --manifest-path impl/lsn_cryptanalysis/Cargo.toml --release --bin lsn_sampled_ambient_ml_sweep -- \
  --n-start 6 \
  --n-end 8 \
  --ratios 0.09375,0.125,0.1875,0.25 \
  --p-values 0.25 \
  --trials 20 \
  --seed 3235823842 \
  --output experiments/142-codex-p2-ambient-size-ml-boundary-n6-n8.json
```

## Results

| n | candidate_count = 2^(2n) | m / 2^(2n) | m | success | success rate | avg margin |
|---:|---:|---:|---:|---:|---:|---:|
| 6 | 4096 | 0.09375 | 384 | 4/20 | 0.20 | -2.00 |
| 6 | 4096 | 0.12500 | 512 | 10/20 | 0.50 | -0.75 |
| 6 | 4096 | 0.18750 | 768 | 11/20 | 0.55 | 0.05 |
| 6 | 4096 | 0.25000 | 1024 | 17/20 | 0.85 | 2.60 |
| 7 | 16384 | 0.09375 | 1536 | 10/20 | 0.50 | 0.15 |
| 7 | 16384 | 0.12500 | 2048 | 15/20 | 0.75 | 2.40 |
| 7 | 16384 | 0.18750 | 3072 | 19/20 | 0.95 | 5.35 |
| 7 | 16384 | 0.25000 | 4096 | 18/20 | 0.90 | 8.55 |
| 8 | 65536 | 0.09375 | 6144 | 17/20 | 0.85 | 3.20 |
| 8 | 65536 | 0.12500 | 8192 | 20/20 | 1.00 | 9.00 |
| 8 | 65536 | 0.18750 | 12288 | 20/20 | 1.00 | 20.85 |
| 8 | 65536 | 0.25000 | 16384 | 20/20 | 1.00 | 31.20 |

## Interpretation

The boundary sweep strengthens the qualitative finding from experiment 141:

- the transition remains at `m = c * 2^(2n)` for a small constant `c`;
- no tested point gives recovery at polynomial-in-`n` samples or below the `2^(2n)` rail;
- success improves monotonically with sample ratio within each `n` except for small finite-trial
  fluctuation (`n=7`, `0.1875` vs `0.25`);
- larger `n` appears easier at the same ratio in this planted random-decoy calibration, consistent
  with previous sampled-candidate observations where random decoys become less confusable than the
  planted secret as the ambient dimension grows.

That last point is a limitation, not an attack: the candidate cloud is sampled and contains the
secret by construction. A public attacker is not given such a cloud. The result is best read as
calibration that an ambient-size random decoy cloud already follows the `2^(2n)` sample scale; it
does not supply a public candidate generator or selector.

## Adjudication

- **BROKEN:** no.
- **REDUCES:** no.
- **Sub-`2^(2n)` attack success:** no.
- **Useful evidence:** yes, boundary table for v2 security-evidence discussion.
- **Threat-model limit:** planted candidate among random decoys; not full-orbit ML.
- **OPEN:** unchanged for LSN.

## Next Step

For v2 integration, the next Codex deliverable should be a compact cryptanalysis synthesis table
rather than another raw sweep:

```text
attacks = ML full small-n, ambient-size ML n=6..8, ISD, BKW, span-positive, sampled-candidate controls
columns = threat model, n-range, budget, outcome, relation to 2^(2n), adjudication
```

That report can be handed to Claude for paper v2 insertion while keeping all claims within the
Sound Verifier line.

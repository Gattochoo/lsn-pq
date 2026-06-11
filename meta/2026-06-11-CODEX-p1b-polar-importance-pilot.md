# Codex P1b Polar Importance-Sampling Pilot

**Date:** 2026-06-11
**Actor:** Codex
**Directive:** `meta/2026-06-12-DIRECTIVE-CODEX-frontier-v2.md`, Track 1
**Discipline:** Sound Verifier. No 7th; no break; no security claim. OPEN = LSN.

## Scope

This increment implements a minimal tilted-BSC importance sampler for the existing Rust fast-SCL
polar validation harness. The target channel remains `BSC(target_p)`, the frozen set and decoder LLRs
are built for `target_p`, but the flip pattern is sampled from a proposal `BSC(proposal_p)` and then
reweighted by the exact likelihood ratio

```text
W(E) = (target_p / proposal_p)^wt(E)
       * ((1 - target_p) / (1 - proposal_p))^(N - wt(E)).
```

This is a pilot for whether naive global channel tilting can improve the N=2048 BLER upper-bound
evidence beyond ordinary Monte Carlo. It is not a production rare-event method and not a proof of
the design BLER.

Raw data:

- `experiments/145-codex-p1b-polar-importance-pilot-n2048.json`
- `experiments/146-codex-p1b-polar-importance-highproposal-n2048.json`
- `experiments/147-codex-p1b-polar-importance-high-noise-control.json`

Implementation:

- `impl/polar_validation/src/bin/polar_importance.rs`
- `simulate_bsc_scl_fast_importance`
- `importance_results_to_json`

## RED/GREEN

The sanity test `importance_sampler_matches_plain_mc_when_proposal_equals_target` pins the core
identity:

```text
proposal_p = target_p  =>  weighted BLER estimate equals ordinary Monte Carlo BLER,
                           mean likelihood ratio = 1,
                           ESS = trials.
```

The JSON test `importance_json_records_proposal_and_weight_diagnostics` pins the threat-model fields
and diagnostics (`proposal_p`, weighted estimate, mean likelihood ratio, effective sample size).

## Commands

Moderate proposals:

```bash
cargo run --manifest-path impl/polar_validation/Cargo.toml --release --bin polar_importance -- \
  --n 2048 \
  --k 256 \
  --target-p 0.0706 \
  --proposal-values 0.0706,0.08,0.10,0.12 \
  --trials 200 \
  --seed 1364271142 \
  --list-size 8 \
  --output experiments/145-codex-p1b-polar-importance-pilot-n2048.json
```

High proposals:

```bash
cargo run --manifest-path impl/polar_validation/Cargo.toml --release --bin polar_importance -- \
  --n 2048 \
  --k 256 \
  --target-p 0.0706 \
  --proposal-values 0.16,0.20,0.25 \
  --trials 100 \
  --seed 1364271143 \
  --list-size 8 \
  --output experiments/146-codex-p1b-polar-importance-highproposal-n2048.json
```

High-noise failure control:

```bash
cargo run --manifest-path impl/polar_validation/Cargo.toml --release --bin polar-validate -- \
  --suite high-noise \
  --decoder scl-fast \
  --list-size 8 \
  --trials 50 \
  --seed 1364271144 \
  --output experiments/147-codex-p1b-polar-importance-high-noise-control.json
```

## Results

### Importance-Sampling Pilot

| target p | proposal p | trials | proposal errors | proposal error rate | weighted BLER estimate | mean LR | ESS |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.0706 | 0.0706 | 200 | 0 | 0.000 | 0.000e+0 | 1.000e+0 | 200.00 |
| 0.0706 | 0.0800 | 200 | 0 | 0.000 | 0.000e+0 | 8.745e-1 | 36.95 |
| 0.0706 | 0.1000 | 200 | 0 | 0.000 | 0.000e+0 | 3.748e-1 | 1.19 |
| 0.0706 | 0.1200 | 200 | 0 | 0.000 | 0.000e+0 | 2.459e-8 | 2.24 |
| 0.0706 | 0.1600 | 100 | 0 | 0.000 | 0.000e+0 | 9.102e-20 | 1.00 |
| 0.0706 | 0.2000 | 100 | 0 | 0.000 | 0.000e+0 | 1.187e-56 | 1.00 |
| 0.0706 | 0.2500 | 100 | 8 | 0.080 | 3.550e-140 | 2.050e-107 | 1.02 |

### High-Noise Failure Control

| N | K | p | trials | errors | BLER |
|---:|---:|---:|---:|---:|---:|
| 2048 | 256 | 0.3000 | 50 | 48 | 0.96 |
| 2048 | 256 | 0.4000 | 50 | 50 | 1.00 |
| 2048 | 256 | 0.5000 | 50 | 50 | 1.00 |

## Interpretation

- The `proposal_p = target_p` row is a sanity check: it reproduces ordinary zero-error Monte Carlo
  with mean likelihood ratio `1` and ESS equal to the trial count.
- Moderate tilting (`proposal_p <= 0.12`) still produced zero proposal errors, so it does not improve
  the BLER upper bound over the existing zero-error Monte Carlo evidence.
- Aggressive tilting eventually produces proposal errors (`proposal_p = 0.25`, `8/100`), but the
  likelihood-ratio diagnostics collapse (`mean LR ~= 2e-107`, ESS `~= 1`). The resulting weighted
  estimate is not a useful certified design-point bound.
- The matched high-noise control fails when it should fail (`p >= 0.3`, BLER `0.96..1.00`), so the
  decoder comparison/noise injection path remains active.
- This is a negative result for naive global BSC tilting, not for the polar parameter set. The run did
  not observe a BLER failure at the design target.

## Adjudication

- **BLER-fail:** no.
- **CLOSURE-GRADE:** no.
- **Useful positive:** the implementation now has a reproducible tilted-BSC importance-sampling
  harness with target-channel LLRs and exact likelihood-ratio accounting.
- **Negative control:** high-noise N=2048 fast-SCL fails as expected.
- **Useful negative:** naive global tilting is not yet a good rare-event estimator here; it either
  sees no errors or collapses ESS when it forces errors.
- **Design claim:** unchanged. Existing N=2048 ordinary Monte Carlo remains `0/2000`; this pilot does
  not certify `2^-80`.
- **Next P1b direction:** a better rare-event method would need decoder-aware conditional sampling or
  a cross-entropy/adaptive proposal, not uniform global BSC tilting.

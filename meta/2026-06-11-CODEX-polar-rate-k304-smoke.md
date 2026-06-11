# Codex Polar Rate K=304 SCL Smoke

**Date:** 2026-06-11
**Actor:** Codex
**Directive:** `meta/2026-06-12-DIRECTIVE-CODEX-frontier-v2.md`, Track 2 follow-up
**Status:** DRAFT for Claude review
**Discipline:** Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

## Scope

This is a focused engineering follow-up to
`meta/2026-06-11-CODEX-polar-rate-sweep-n2048.md`. The rate sweep found that, under the conservative
half-sum Bhattacharyya convention, the `N=2048, p=0.0343` design point can increase from `K=256` to
`K=304` while keeping `log2(0.5 * sum_i Z_i) <= -128`.

This increment does **not** prove the decryption-failure probability. It only checks that the
existing Rust fast-SCL validation path runs at the candidate `K=304` point and that the same path
still fails under an elevated-noise negative control.

Raw data:

- `experiments/149-codex-polar-rate-k304-scl-smoke.json`
- `experiments/150-codex-polar-rate-k304-high-noise-control.json`

## Method

The existing `polar_importance` binary was used with `proposal_p = target_p`. The regression test
`importance_sampler_matches_plain_mc_when_proposal_equals_target` pins that this equals ordinary
Monte Carlo on the fast-SCL path:

```text
proposal_p = target_p
=> mean likelihood ratio = 1
=> effective sample size = trials
=> weighted BLER estimate = ordinary proposal error rate
```

Commands:

```bash
cargo run --manifest-path impl/polar_validation/Cargo.toml --release --bin polar_importance -- \
  --n 2048 \
  --k 304 \
  --target-p 0.0343 \
  --proposal-values 0.0343 \
  --trials 500 \
  --seed 1364271145 \
  --list-size 8 \
  --output experiments/149-codex-polar-rate-k304-scl-smoke.json
```

```bash
cargo run --manifest-path impl/polar_validation/Cargo.toml --release --bin polar_importance -- \
  --n 2048 \
  --k 304 \
  --target-p 0.3 \
  --proposal-values 0.3 \
  --trials 50 \
  --seed 1364271146 \
  --list-size 8 \
  --output experiments/150-codex-polar-rate-k304-high-noise-control.json
```

## Results

| N | K | target p | proposal p | trials | errors | observed BLER | mean LR | ESS |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2048 | 304 | 0.0343 | 0.0343 | 500 | 0 | 0.000 | 1.000 | 500.00 |
| 2048 | 304 | 0.3000 | 0.3000 | 50 | 50 | 1.000 | 1.000 | 50.00 |

For the zero-error smoke row, the one-sided 95% binomial upper bound is `0.005973552`. This is only
a small-sample smoke bound; it is not a `2^-128` empirical certificate.

## Interpretation

- The candidate `K=304, p=0.0343` point did not produce a fast-SCL block error in 500 trials.
- Because the run used `proposal_p = target_p`, the likelihood diagnostics are exactly healthy
  (`mean LR = 1`, `ESS = 500`), avoiding the collapsed-ESS issue from tilted proposals.
- The elevated-noise control at `p=0.3` failed in every trial, so the decoder/noise path is still
  capable of detecting failure for a clearly bad channel.
- This supports using `K=304` as a candidate for Claude review of the analytic bound convention, but
  it does not by itself strengthen the design-failure theorem.

## Adjudication

- **BLER-fail at candidate point:** no, `0/500`.
- **Negative control:** yes, `50/50` errors at `p=0.3`.
- **CLOSURE-GRADE:** no.
- **Attack success:** no.
- **Paper edit:** none.
- **Next if accepted:** either scale `K=304, p=0.0343` to the existing 2k-trial smoke size or move to
  Track 3 cryptanalysis synthesis, depending on Claude's preference for v2 evidence.

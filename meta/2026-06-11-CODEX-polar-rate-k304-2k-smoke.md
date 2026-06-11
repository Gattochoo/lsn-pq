# Codex Polar Rate K=304 2k SCL Smoke

**Date:** 2026-06-11 KST
**Actor:** Codex
**Directive:** `meta/2026-06-12-DIRECTIVE-CODEX-frontier-v2.md`, Track 2
**Status:** DRAFT for Claude review
**Discipline:** Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

## Scope

This increment scales the prior `N=2048, K=304, p=0.0343` fast-SCL smoke from
500 trials to 2000 trials. It follows the rate-sweep result in
`meta/2026-06-11-CODEX-polar-rate-sweep-n2048.md`, where `K=304` was the largest
passing value for the conservative half-sum Bhattacharyya target
`log2(0.5 * sum_i Z_i) <= -128` at `p=0.0343`.

This is an empirical smoke check only. It is not a proof of the decryption
failure rate, not a security claim, and not a parameter-table update.

Raw data:

- `experiments/178-codex-polar-rate-k304-scl-2k-smoke.json`

Prior companion controls:

- `experiments/149-codex-polar-rate-k304-scl-smoke.json` (`0/500` at `p=0.0343`)
- `experiments/150-codex-polar-rate-k304-high-noise-control.json` (`50/50` errors at `p=0.3`)

## Method

The existing `polar_importance` binary was used with `proposal_p = target_p`.
The regression test `importance_sampler_matches_plain_mc_when_proposal_equals_target`
pins this as ordinary Monte Carlo on the fast-SCL path:

```text
proposal_p = target_p
=> mean likelihood ratio = 1
=> effective sample size = trials
=> weighted BLER estimate = ordinary proposal error rate
```

Command:

```bash
env CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target \
  cargo run --manifest-path impl/polar_validation/Cargo.toml --release \
  --bin polar_importance -- \
  --n 2048 \
  --k 304 \
  --target-p 0.0343 \
  --proposal-values 0.0343 \
  --trials 2000 \
  --seed 1364271147 \
  --list-size 8 \
  --output experiments/178-codex-polar-rate-k304-scl-2k-smoke.json
```

## Result

| N | K | target p | proposal p | trials | errors | observed BLER | mean LR | ESS |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2048 | 304 | 0.0343 | 0.0343 | 2000 | 0 | 0.000 | 1.000 | 2000.00 |

For this zero-error row, the one-sided 95% binomial upper bound is:

```text
1 - 0.05^(1/2000) = 0.001496744895 ~= 2^-9.383956
```

This is only a smoke-test bound. It is far weaker than the analytic
`2^-128` half-sum design target and must not be reported as a failure theorem.

## Reproducibility

Fixture check:

```bash
env CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target \
  cargo run --manifest-path impl/polar_validation/Cargo.toml --release \
  --bin polar_importance -- \
  --n 2048 \
  --k 304 \
  --target-p 0.0343 \
  --proposal-values 0.0343 \
  --trials 2000 \
  --seed 1364271147 \
  --list-size 8 \
  --check experiments/178-codex-polar-rate-k304-scl-2k-smoke.json
```

Observed:

```text
N=2048 K=304 target_p=0.0343 proposal_p=0.0343 trials=2000 proposal_errors=0 weighted_bler=0.0000e0 mean_lr=1.0000e0 ess=2000.00
verified experiments/178-codex-polar-rate-k304-scl-2k-smoke.json
```

## Interpretation

- The candidate `K=304, p=0.0343` point again produced no fast-SCL block errors
  in this 2000-trial smoke run.
- Because `proposal_p = target_p`, the likelihood diagnostics are healthy
  (`mean LR = 1`, `ESS = 2000`).
- This extends the previous 500-trial smoke but does not turn the empirical
  evidence into a proof-level BLER certificate.
- The existing elevated-noise companion control at `K=304, p=0.3` still supplies
  the failure-side check (`50/50` errors).

## Verification

Commands run:

```bash
env CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target \
  cargo test --manifest-path impl/polar_validation/Cargo.toml cli_check -- --nocapture

env CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target \
  cargo test --manifest-path impl/polar_validation/Cargo.toml \
  importance_sampler_matches_plain_mc_when_proposal_equals_target

env CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target \
  cargo test --manifest-path impl/polar_validation/Cargo.toml \
  polar_rate_row_marks_target_bound_status

env CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target \
  cargo run --manifest-path impl/polar_validation/Cargo.toml --release \
  --bin polar_importance -- \
  --n 2048 --k 304 --target-p 0.0343 --proposal-values 0.0343 \
  --trials 2000 --seed 1364271147 --list-size 8 \
  --check experiments/178-codex-polar-rate-k304-scl-2k-smoke.json

jq -e '.results | length == 1 and .[0].K == 304 and .[0].target_p == 0.0343000000 and .[0].trials == 2000 and .[0].proposal_errors == 0 and .[0].effective_sample_size == 2000.000000' \
  experiments/178-codex-polar-rate-k304-scl-2k-smoke.json

git diff --check

cargo fmt --manifest-path impl/polar_validation/Cargo.toml -- --check

env CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target \
  cargo test --manifest-path impl/polar_validation/Cargo.toml
```

All verification commands passed.

## Adjudication

- **BLER-fail at candidate point:** no, `0/2000`.
- **Negative control:** inherited from `150`, `50/50` errors at `K=304, p=0.3`.
- **CLOSURE-GRADE:** no.
- **Attack success:** no.
- **Paper edit:** none.
- **Usable DRAFT output:** `K=304, p=0.0343` now has a 2000-trial fast-SCL smoke
  row with healthy ordinary-MC diagnostics.

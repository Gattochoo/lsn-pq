# Codex Polar Rate K=305 Analytic-Fail-Side Smoke

**Date:** 2026-06-11 KST
**Actor:** Codex
**Directive:** `meta/2026-06-12-DIRECTIVE-CODEX-frontier-v2.md`, Track 2
**Status:** DRAFT for Claude review
**Discipline:** Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

## Scope

This increment checks the immediate analytic failure-side row next to the
candidate `N=2048, p=0.0343, K=304` polar-rate point. In the exact rate sweep,
`K=304` is the largest row passing the conservative half-sum Bhattacharyya gate

```text
log2(0.5 * sum selected Z_i) <= -128,
```

while `K=305` fails that analytic gate.

This smoke does **not** test that `K=305` must show block errors in 500 trials.
The analytic bound failure is a conservative design-gate failure, not an
empirical small-sample BLER failure prediction.

Raw data:

- `experiments/179-codex-polar-rate-k305-analytic-fail-side-smoke.json`

Companion rows:

- `experiments/148-codex-polar-rate-sweep-n2048.json`
- `experiments/178-codex-polar-rate-k304-scl-2k-smoke.json`
- `meta/2026-06-11-CODEX-polar-rate-item5-v2-draft.md`

## Analytic Boundary

From `experiments/148-codex-polar-rate-sweep-n2048.json`:

| p | K | rate | log2 half-sum | target pass |
|---:|---:|---:|---:|:---:|
| 0.0343 | 304 | 0.148437500000 | -128.163128 | yes |
| 0.0343 | 305 | 0.148925781250 | -127.693137 | no |

## Smoke Result

Command:

```bash
env CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target \
  cargo run --manifest-path impl/polar_validation/Cargo.toml --release \
  --bin polar_importance -- \
  --n 2048 \
  --k 305 \
  --target-p 0.0343 \
  --proposal-values 0.0343 \
  --trials 500 \
  --seed 1364271148 \
  --list-size 8 \
  --output experiments/179-codex-polar-rate-k305-analytic-fail-side-smoke.json
```

Result:

| N | K | target p | proposal p | trials | errors | observed BLER | mean LR | ESS |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2048 | 305 | 0.0343 | 0.0343 | 500 | 0 | 0.000 | 1.000 | 500.00 |

For this zero-error row, the one-sided 95% binomial upper bound is:

```text
1 - 0.05^(1/500) = 0.005973551516 ~= 2^-7.387195
```

This empirical bound is intentionally weak and does not supersede the analytic
half-sum design gate.

## Reproducibility

Fixture check:

```bash
env CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target \
  cargo run --manifest-path impl/polar_validation/Cargo.toml --release \
  --bin polar_importance -- \
  --n 2048 \
  --k 305 \
  --target-p 0.0343 \
  --proposal-values 0.0343 \
  --trials 500 \
  --seed 1364271148 \
  --list-size 8 \
  --check experiments/179-codex-polar-rate-k305-analytic-fail-side-smoke.json
```

Observed:

```text
N=2048 K=305 target_p=0.0343 proposal_p=0.0343 trials=500 proposal_errors=0 weighted_bler=0.0000e0 mean_lr=1.0000e0 ess=500.00
verified experiments/179-codex-polar-rate-k305-analytic-fail-side-smoke.json
```

## Interpretation

- `K=305` remains outside the candidate row under the conservative half-sum
  `2^-128` analytic gate.
- The `0/500` smoke is not surprising and is not a counterexample to the
  analytic gate. It only says this small ordinary-Monte-Carlo run did not see a
  block error.
- The companion `K=304` row remains the largest passing analytic row in the
  current sweep, with a stronger `0/2000` smoke already recorded.
- No BLER-fail, no CLOSURE-GRADE event, and no parameter/security claim follows
  from this smoke.

## Verification

Commands run:

```bash
env CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target \
  cargo test --manifest-path impl/polar_validation/Cargo.toml \
  polar_rate_row_marks_target_bound_status

env CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target \
  cargo test --manifest-path impl/polar_validation/Cargo.toml \
  importance_sampler_matches_plain_mc_when_proposal_equals_target

env CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target \
  cargo test --manifest-path impl/polar_validation/Cargo.toml cli_check -- --nocapture

env CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target \
  cargo run --manifest-path impl/polar_validation/Cargo.toml --release \
  --bin polar_importance -- \
  --n 2048 --k 305 --target-p 0.0343 --proposal-values 0.0343 \
  --trials 500 --seed 1364271148 --list-size 8 \
  --check experiments/179-codex-polar-rate-k305-analytic-fail-side-smoke.json

jq -e '.results | length == 1 and .[0].K == 305 and .[0].target_p == 0.0343000000 and .[0].trials == 500 and .[0].proposal_errors == 0 and .[0].effective_sample_size == 500.000000' \
  experiments/179-codex-polar-rate-k305-analytic-fail-side-smoke.json

jq -e '[.rows[] | select(.p == 0.0343000000 and (.K == 304 or .K == 305))] | .[0].passes_half_sum_target == true and .[1].passes_half_sum_target == false' \
  experiments/148-codex-polar-rate-sweep-n2048.json

git diff --check

cargo fmt --manifest-path impl/polar_validation/Cargo.toml -- --check

env CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target \
  cargo test --manifest-path impl/polar_validation/Cargo.toml
```

All verification commands passed.

## Adjudication

- **Analytic gate:** `K=305` fails the conservative half-sum `2^-128` gate.
- **Empirical smoke:** `0/500`; no block error observed.
- **BLER-fail:** no.
- **CLOSURE-GRADE:** no.
- **Paper edit:** none.
- **Security/parameter claim:** none.

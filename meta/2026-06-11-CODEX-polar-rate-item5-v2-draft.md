# CODEX DRAFT: Polar Rate Item 5 v2 Summary

**Date:** 2026-06-11 KST
**Actor:** Codex
**Directive:** `meta/2026-06-12-DIRECTIVE-CODEX-frontier-v2.md`, Track 2
**Status:** DRAFT for Claude review
**Discipline:** Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

## Scope

This note consolidates Codex's Track 2 evidence for open item 5: maximize the
outer polar-code rate while keeping the conservative design bound below the
target. It is a meta-only synthesis for Claude; it does not edit `paper/`.

The analytic gate used here is the conservative SC half-sum Bhattacharyya
convention:

```text
log2(0.5 * sum selected Z_i) <= -128.
```

The empirical smoke rows are implementation checks only. They do not prove the
design BLER and do not certify a `2^-128` decryption-failure probability.

## Source Artifacts

- `experiments/148-codex-polar-rate-sweep-n2048.json`
- `experiments/149-codex-polar-rate-k304-scl-smoke.json`
- `experiments/150-codex-polar-rate-k304-high-noise-control.json`
- `experiments/178-codex-polar-rate-k304-scl-2k-smoke.json`
- `experiments/179-codex-polar-rate-k305-analytic-fail-side-smoke.json`

Supporting notes:

- `meta/2026-06-11-CODEX-polar-rate-sweep-n2048.md`
- `meta/2026-06-11-CODEX-polar-rate-k304-smoke.md`
- `meta/2026-06-11-CODEX-polar-rate-k304-2k-smoke.md`
- `meta/2026-06-11-CODEX-polar-rate-k305-analytic-fail-side-smoke.md`

## Analytic Half-Sum Boundary

Boundary rows from `experiments/148-codex-polar-rate-sweep-n2048.json`:

| p | K | rate | log2 raw sum | log2 half-sum | target pass |
|---:|---:|---:|---:|---:|:---:|
| 0.0706 | 151 | 0.073730468750 | -127.094067 | -128.094067 | yes |
| 0.0706 | 152 | 0.074218750000 | -126.328258 | -127.328258 | no |
| 0.0706 | 256 | 0.125000000000 | -79.933489 | -80.933489 | no |
| 0.0343 | 256 | 0.125000000000 | -148.499602 | -149.499602 | yes |
| 0.0343 | 304 | 0.148437500000 | -127.163128 | -128.163128 | yes |
| 0.0343 | 305 | 0.148925781250 | -126.693137 | -127.693137 | no |

Interpretation:

- For `p=0.0343`, `K=304` is the largest passing K in the exact sweep under
  this half-sum convention.
- `K=305` is the immediate analytic failure-side row and should remain outside
  the candidate set unless Claude changes the bound convention.
- For `p=0.0706`, `K=256` does not meet the `2^-128` half-sum target. The
  largest passing K is `151`; the existing `K=256` point is closer to the
  previously documented `2^-81` half-sum / `2^-80` raw-sum region.

## Empirical Smoke Rows

The K=304/K=305 smoke rows use `proposal_p = target_p`, so the importance
harness is ordinary Monte Carlo with healthy likelihood diagnostics. The K=305
row is included only as the immediate analytic-fail-side neighbor; it is not
expected to fail in a small Monte-Carlo budget.

| N | K | target p | trials | errors | observed BLER | mean LR | ESS | artifact |
|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 2048 | 304 | 0.0343 | 500 | 0 | 0.000 | 1.000 | 500.00 | `149` |
| 2048 | 304 | 0.0343 | 2000 | 0 | 0.000 | 1.000 | 2000.00 | `178` |
| 2048 | 305 | 0.0343 | 500 | 0 | 0.000 | 1.000 | 500.00 | `179` |
| 2048 | 304 | 0.3000 | 50 | 50 | 1.000 | 1.000 | 50.00 | `150` |

For the `0/2000` row, the one-sided 95% binomial upper bound is:

```text
1 - 0.05^(1/2000) = 0.001496744895 ~= 2^-9.383956.
```

This empirical upper bound is much weaker than `2^-128`. Its role is only to
check that the candidate K=304 row runs through the same fast-SCL validation
path without observed failures in a small smoke budget.

For the `K=305`, `0/500` row, the corresponding one-sided 95% binomial upper
bound is:

```text
1 - 0.05^(1/500) = 0.005973551516 ~= 2^-7.387195.
```

That row remains an analytic half-sum failure row despite this zero-error smoke.
The two statements are not in tension: the analytic gate is conservative and the
Monte-Carlo smoke is intentionally shallow.

## Recommended v2 Wording

Suggested text for Claude to adapt:

> Under the conservative SC half-sum Bhattacharyya convention
> `0.5 * sum_i Z_i`, the `N=2048, p=0.0343` design point admits `K=304`
> information bits while keeping `log2(0.5 * sum_i Z_i) <= -128`; the immediate
> next row `K=305` fails the same bound. We also ran the existing fast-SCL Rust
> validation path at `K=304, p=0.0343` for 2000 ordinary Monte-Carlo trials and
> observed no block errors. The immediate analytic-fail-side row `K=305` also
> showed no block errors in a 500-trial smoke, which should be read only as a
> shallow implementation check, not as a pass of the analytic design gate. A
> matched high-noise control at `K=304, p=0.3` failed in all 50 trials. These
> Monte-Carlo checks are implementation smoke tests only and are not proof-level
> failure certificates.

## Sound-Verifier Notes

- **BLER-fail:** no BLER failure was observed at the candidate K=304 row or the
  analytic-fail-side K=305 smoke row.
- **CLOSURE-GRADE:** no.
- **Paper edit:** none.
- **Security claim:** none.
- **Parameter recommendation:** conditional on Claude accepting the half-sum
  bound convention; this note only supplies data.
- **Empirical limit:** `0/2000` means a 95% upper bound of about `1.5e-3`, not
  `2^-128`; `K=305`'s `0/500` smoke is weaker still.
- **Analytic-fail-side row:** `K=305` fails the half-sum target and remains
  outside the candidate set under this convention, even though the small smoke
  observed no block errors.
- **Negative control:** the same K=304 fast-SCL path fails at `p=0.3` (`50/50`
  errors), so the decoder/noise/error-count path is active.

## Verification

Commands run:

```bash
jq -e '[.rows[] | select((.p == 0.0343000000 or .p == 0.0706000000) and (.K == 151 or .K == 152 or .K == 256 or .K == 304 or .K == 305))] | length == 10' \
  experiments/148-codex-polar-rate-sweep-n2048.json

jq -e '.results | length == 1 and .[0].K == 304 and .[0].target_p == 0.0343000000 and .[0].trials == 2000 and .[0].proposal_errors == 0 and .[0].effective_sample_size == 2000.000000' \
  experiments/178-codex-polar-rate-k304-scl-2k-smoke.json

jq -e '.results | length == 1 and .[0].K == 305 and .[0].target_p == 0.0343000000 and .[0].trials == 500 and .[0].proposal_errors == 0 and .[0].effective_sample_size == 500.000000' \
  experiments/179-codex-polar-rate-k305-analytic-fail-side-smoke.json

jq -e '.results | length == 1 and .[0].K == 304 and .[0].target_p == 0.3000000000 and .[0].proposal_errors == 50 and .[0].weighted_bler_estimate == 1.000000000000' \
  experiments/150-codex-polar-rate-k304-high-noise-control.json

jq -e '[.rows[] | select(.p == 0.0343000000 and (.K == 304 or .K == 305))] | .[0].passes_half_sum_target == true and .[1].passes_half_sum_target == false' \
  experiments/148-codex-polar-rate-sweep-n2048.json

git diff --check

cargo fmt --manifest-path impl/polar_validation/Cargo.toml -- --check

env CARGO_TARGET_DIR=/tmp/lsn-pq-polar-target \
  cargo test --manifest-path impl/polar_validation/Cargo.toml
```

All verification commands passed.

## Next Step

If Claude accepts the bound convention, this note is ready to feed the v2 item-5
rate paragraph. If more Codex work is needed first, prefer a bounded
presentation/consistency pass over this item5 package or move back to P2/P1b per
the active directive; do not keep adding shallow Monte-Carlo rows unless Claude
asks for a specific comparison.

# Codex P2 Non-Xor Bucket Certificate Screen

**Date:** 2026-06-11
**Actor:** Codex
**Directive:** Follow-up to `2026-06-11-CODEX-p2-bkw-noise-growth-model.md`
**Discipline:** Sound Verifier. No 7th; no break; no security claim. OPEN = LSN.

## Scope

The previous BKW increment pinned the standard label-xor wall:

```text
p -> 2p(1-p), bias -> bias^2.
```

This increment tests a non-xor certificate map to avoid immediate bias squaring. The observable
partitions public points by low coordinate buckets and measures bucket-level positive-label rate
variance above a matched Bernoulli control.

Implementation:

- added `bucket_rate_certificate`;
- added `run_bucket_certificate_trials`;
- added `bucket_certificate_results_to_json`;
- added `lsn_bucket_certificate_sweep`.

The secret is used only for diagnostic projection-size reporting, not as attacker input. The
observable itself uses public points and noisy membership labels.

## RED/GREEN Tests

RED was confirmed by adding `bucket_rate_certificate_detects_clean_projection_variance` before
implementation. The expected unresolved import was:

```text
no `bucket_rate_certificate` in the root
```

GREEN:

```bash
cargo test --manifest-path impl/lsn_cryptanalysis/Cargo.toml bucket_rate_certificate_detects_clean_projection_variance
```

The test checks a clean p=0 positive control with `n=4`, `bucket_bits=6`, and confirms positive
excess bucket-rate variance.

## Sweep

Command:

```bash
cargo run --manifest-path impl/lsn_cryptanalysis/Cargo.toml --release --bin lsn_bucket_certificate_sweep -- \
  --n-start 4 \
  --n-end 8 \
  --ratios 64.0 \
  --p-values 0.0,0.25,0.5 \
  --trials 5 \
  --bucket-extra 2 \
  --seed 3235823838 \
  --output experiments/135-codex-p2-bucket-certificate-screen.json
```

Raw data: `experiments/135-codex-p2-bucket-certificate-screen.json`.

Here `bucket_bits=n+2`, so a typical projected Lagrangian occupies about one quarter of the
public buckets.

| n | m | p | bucket bits | excess bucket variance | p=1/4 excess * 4^n |
|---:|---:|---:|---:|---:|---:|
| 4 | 16,384 | 0.00 | 6 | 0.011598363530 | |
| 5 | 65,536 | 0.00 | 7 | 0.004534485663 | |
| 6 | 262,144 | 0.00 | 8 | 0.001158976957 | |
| 7 | 1,048,576 | 0.00 | 9 | 0.000182859995 | |
| 8 | 4,194,304 | 0.00 | 10 | 0.000058638686 | |
| 4 | 16,384 | 0.25 | 6 | 0.002857441956 | 0.731505 |
| 5 | 65,536 | 0.25 | 7 | 0.001046225656 | 1.071335 |
| 6 | 262,144 | 0.25 | 8 | 0.000221030882 | 0.905342 |
| 7 | 1,048,576 | 0.25 | 9 | 0.000053963296 | 0.884135 |
| 8 | 4,194,304 | 0.25 | 10 | 0.000011204567 | 0.734303 |
| 4 | 16,384 | 0.50 | 6 | -0.000010807131 | |
| 5 | 65,536 | 0.50 | 7 | 0.000028827183 | |
| 6 | 262,144 | 0.50 | 8 | -0.000002873933 | |
| 7 | 1,048,576 | 0.50 | 9 | 0.000006384841 | |
| 8 | 4,194,304 | 0.50 | 10 | -0.000002583177 | |

## Interpretation

This non-xor certificate does avoid the immediate BKW label-xor bias-squaring failure. Unlike the
label-xor bucket-pair statistic, it retains a measurable p=1/4 signal at n=8.

However, the signal size decays like `Theta(4^-n)` in this setup:

- the p=1/4 excess variance multiplied by `4^n` stays roughly constant from n=4 to n=8;
- the p=1/2 matched-random control stays near zero;
- the clean p=0 positive control is strong, confirming the observable can see projection structure.

This is therefore **not** a REDUCES result and not a break. The certificate sees structure, but at
the same `2^(2n)` scale rather than below it. It is evidence that this non-xor map aligns with the
paper's sample-threshold rail, not that it beats it.

Honest status:

- **BROKEN:** no;
- **REDUCES / scalable attack success:** no;
- **non-xor positive signal:** yes, finite and measurable;
- **sub-`2^(2n)` advantage:** not observed;
- **OPEN evidence:** strengthened against this bucket-rate certificate family.

## Next Step

Two directions remain useful:

1. Turn this into a small analytic note: for `bucket_bits=n+c`, bucket certificate signal variance
   should scale like `Theta(4^-n)` at constant `c`, matching the empirical normalization.
2. Test a sampled-candidate ML baseline at n=6..10 with random Lagrangian secrets and random
   Lagrangian candidates, to measure whether partial candidate clouds show any advantage before
   full orbit enumeration becomes infeasible.

# Codex Polar Rate Sweep for N=2048

**Date:** 2026-06-11
**Actor:** Codex
**Directive:** `meta/2026-06-12-DIRECTIVE-CODEX-frontier-v2.md`, Track 2
**Status:** DRAFT for Claude review
**Discipline:** Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

## Scope

This increment addresses open item 5: maximize the outer polar code rate while keeping the
conservative SC block-error design bound below `2^-128`.

The sweep is a pure engineering/design-bound calculation. It does not simulate BLER and does not
prove an implementation decryption-failure rate. It uses the same natural-order Bhattacharyya
recursion already used by the Rust polar validation harness:

```text
Z(W^-) = 2Z - Z^2
Z(W^+) = Z^2
Z(BSC(p)) = 2 sqrt(p(1-p)).
```

For transparency the JSON records both:

- raw selected-channel sum `sum_i Z_i`
- half-sum SC bound convention `0.5 * sum_i Z_i`

The target gate in this run is `log2(0.5 * sum_i Z_i) <= -128`.

Raw data:

- `experiments/148-codex-polar-rate-sweep-n2048.json`

Implementation:

- `bhattacharyya_reliabilities`
- `polar_rate_row`
- `sweep_polar_rate`
- `polar_rate_rows_to_json`
- `impl/polar_validation/src/bin/polar_rate_sweep.rs`

## RED/GREEN

New tests pin the intended behavior before implementation:

- `bhattacharyya_reliabilities_preserve_natural_frozen_order`: extracting reliabilities must not
  change the existing frozen-set order.
- `polar_rate_row_marks_target_bound_status`: current `N=2048, K=256` passes the `2^-128` half-sum
  target for `p=0.0343` and fails it for `p=0.0706`.
- `polar_rate_json_records_target_and_log_bounds`: JSON must carry target and log-bound fields.

The RED failure was the expected missing imports for `bhattacharyya_reliabilities`,
`polar_rate_row`, and `polar_rate_rows_to_json`. The GREEN pass succeeded after adding the helpers.

## Command

```bash
cargo run --manifest-path impl/polar_validation/Cargo.toml --release --bin polar_rate_sweep -- \
  --n 2048 \
  --p-values 0.0706,0.0343 \
  --k-start 1 \
  --k-end 768 \
  --k-step 1 \
  --target-log2 -128 \
  --output experiments/148-codex-polar-rate-sweep-n2048.json
```

## Results

### Boundary rows

| p | K | rate | log2 raw sum | log2 half-sum | target pass |
|---:|---:|---:|---:|---:|:---:|
| 0.0706 | 151 | 0.073730 | -127.094067 | -128.094067 | yes |
| 0.0706 | 152 | 0.074219 | -126.328258 | -127.328258 | no |
| 0.0343 | 304 | 0.148438 | -127.163128 | -128.163128 | yes |
| 0.0343 | 305 | 0.148926 | -126.693137 | -127.693137 | no |

### Current K=256 design rows

| p | K | rate | log2 raw sum | log2 half-sum | target pass |
|---:|---:|---:|---:|---:|:---:|
| 0.0706 | 256 | 0.125000 | -79.933489 | -80.933489 | no |
| 0.0343 | 256 | 0.125000 | -148.499602 | -149.499602 | yes |

## Interpretation

- For the lower-noise `p=0.0343` design point, the conservative half-sum bound allows increasing
  from `K=256` to `K=304` at `N=2048` while preserving the `2^-128` target under this analytic
  convention.
- The boundary is sharp in this exact sweep: `K=305` fails the `2^-128` half-sum target.
- For the higher-noise `p=0.0706` design point, `K=256` is consistent with the previous
  approximately `2^-81` half-sum / `2^-80` raw-sum bound, not a `2^-128` bound. Under the same
  `2^-128` half-sum target, the maximum passing `K` is `151`.
- This is a conservative Bhattacharyya-bound optimization only. It should be reviewed before any
  parameter-table update, and it does not supersede Monte Carlo or implementation failure testing.

## Adjudication

- **BLER-fail:** no BLER experiment was run in this increment.
- **CLOSURE-GRADE:** no.
- **Attack success:** no.
- **Paper edit:** none.
- **Usable DRAFT output:** `K=304` is the candidate `N=2048, p=0.0343` half-sum-bound maximizer for
  the `2^-128` target; `K=151` is the analogous maximizer for `p=0.0706`.
- **Next engineering check:** if Claude accepts the bound convention, run a focused Monte Carlo/SCL
  smoke on `N=2048, K=304, p=0.0343` and a failure-side negative control such as
  `N=2048, K=305, p=0.0343` or elevated `p`.

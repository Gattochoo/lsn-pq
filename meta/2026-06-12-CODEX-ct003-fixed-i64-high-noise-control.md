# CODEX note: ct-003 fixed-i64 high-noise control

Date: 2026-06-12 KST

## Scope

Directive: `meta/2026-06-12-DIRECTIVE-CODEX-L2-constant-time.md`, ct-003.

This increment adds a fixed-i64 SCL high-noise negative control so the fixed rail
is checked both on a low-noise smoke and a random-channel failure point.

## RED/GREEN

RED:

- Added `fixed_i64_high_noise_control_configs_cover_failure_points`.
- The focused test failed because `fixed_i64_high_noise_control_configs` did
  not exist.

GREEN:

- Added fixed-i64 high-noise smoke configs for `(N,K) = (128,16)` at
  `p in {0.3, 0.4, 0.5}`.
- Added `high_noise_fixed_i64_scl_smoke_fails_when_channel_is_random`.
- The p=0.5 fixed-i64 smoke requires at least 20 errors in 25 trials, matching
  the existing fast-SCL random-channel negative-control shape.

## Interpretation

This is a harness-integrity check for the fixed-i64 SCL prototype. It confirms
the fixed rail is not silently succeeding on a random BSC channel in the small
smoke setting.

Limits:

- not an N=2048 BLER result;
- no generated-code, optimizer, timing, branch-predictor, or cache audit;
- `decode_scl`/`decode_scl_fast` remain active non-constant-time decoders;
- no inventory status change and no production constant-time, PQ, security, or
  7th-source claim.

## Next Step

Use these fixed-i64 positive and negative smokes as guards before attempting a
small N=2048 comparison or continuing fixed-path public/secret comparison
classification.

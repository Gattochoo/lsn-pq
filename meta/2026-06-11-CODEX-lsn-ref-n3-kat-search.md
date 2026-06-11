# CODEX note: n=3 toy KAT seed-search fixture

Date: 2026-06-11 KST

## Scope

This extends the toy `impl/lsn_ref` KAT scaffold from the fixed `n=2`
negative-control vector to a bounded deterministic `n=3` wrong-secret search.
It remains a toy reference harness:

- not a production constant-time implementation,
- not an L2 parameterization,
- not a security claim,
- not evidence of a public recovery path.

The purpose is narrower: keep the P3 reference/KAT rail reproducible while the
implementation grows past the smallest hand-picked fixture.

## Artifact

Generated JSON:

- `experiments/153-codex-lsn-ref-n3-kat-search.json`

Profile:

- `n = 3`
- `sample_count = 256`
- `repetition = 3`
- `polar_N = 32`
- `polar_K = 16`
- `public_noise_rate = 0.0`
- `decoder_design_p = 0.0343`

Seeds:

- `honest_secret_seed = 659918`
- `wrong_secret_seed_start = 663552`
- `wrong_secret_seed_trials = 1024`
- found `wrong_secret_seed = 663553`
- `sample_seed = 24301`
- `noise_seed = 49374`
- `encaps_seed = 48879`

Observed fixture outcome:

- honest roundtrip: `true`
- wrong-secret roundtrip: `false`
- encapsulated/decapsulated key:
  `b760a1856d1467c5d8d53f88def9af7086445267b01fe4f2109a4c174681d2ab`
- wrong-secret decapsulated key:
  `ebc77dfce0661c9f891553438d983adea42631332c16c9df4822b839260660d9`

## Code changes

- Added `toy_find_wrong_secret_control(...)`, a bounded deterministic search
  over wrong-secret seeds that only returns a fixture when the honest path
  roundtrips and the wrong-secret path fails.
- Added `lsn_toy_kat --profile n3-search`, preserving the existing default
  `n2` output.
- Added a RED/GREEN regression test:
  `toy_find_wrong_secret_control_finds_n3_fixture`.

## Interpretation

This is only a KAT-fixture improvement. It does not address the known
sparse-majority limitation of the toy encapsulation rule, and it does not
replace the later constant-time/bit-sliced implementation work. Its value is
that future refactors now have a deterministic `n=3` negative-control artifact
that exercises the same public key and ciphertext against a wrong Lagrangian
secret.

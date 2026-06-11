# CODEX note: P2 streaming ambient ML dry-run cost model

**Date:** 2026-06-11 KST

**Status:** implementation/accounting increment only. This is not a decoder
success, not a reduction, not a security claim, and not a seventh-source claim.

## Purpose

The first streaming ambient ML runs showed that full candidate clouds can be
scored without storing `candidate_count * 2^n` row points. The remaining
question for scheduling `n=11` and beyond is not row storage; it is scorer work.

The previous dry-run line reported `score_pairs = candidate_count * sample_count
* trials`, which is a conservative inherited proxy. The actual compact scoring
path builds a sample profile once and then scores each candidate by scanning its
`2^n` Lagrangian points. This increment adds explicit accounting for those two
terms.

## RED/GREEN

Focused test:

```bash
cargo test --manifest-path impl/lsn_cryptanalysis/Cargo.toml \
  --bin lsn_sampled_ambient_ml_sweep \
  dry_run_lines_distinguish_streaming_row_storage_from_capped_storage
```

RED: failed because dry-run cell lines did not include
`profile_updates` or `candidate_point_visits`.

GREEN: dry-run cell lines now include:

- `score_pairs`: legacy conservative proxy, `candidate_count * samples * trials`.
- `profile_updates`: sample-profile construction work, `samples * trials`.
- `candidate_point_visits`: candidate scoring work,
  `candidate_count * 2^n * trials`.

The existing row-storage distinction remains pinned:

- full streaming `n=11`: `row_storage_points=2048`.
- capped non-streaming `n=11`, cap `4096`: `row_storage_points=8388608`.

## Dry-Run Outputs

### n=10 full streaming

```bash
cargo run --manifest-path impl/lsn_cryptanalysis/Cargo.toml \
  --bin lsn_sampled_ambient_ml_sweep -- \
  --n-start 10 --n-end 10 \
  --ratios 0.015625,0.03125 \
  --p-values 0.25,0.5 \
  --trials 1 \
  --seed 3235823867 \
  --streaming \
  --dry-run
```

Output:

```text
dry-run ambient-ml n=10 streaming=true ambient_candidate_count=1048576 candidate_count=1048576 lagrangian_points=1024 row_storage_points=1024
  cell n=10 ratio=0.015625 samples=16384 p=0.25 trials=1 score_pairs=17179869184 profile_updates=16384 candidate_point_visits=1073741824
  cell n=10 ratio=0.015625 samples=16384 p=0.5 trials=1 score_pairs=17179869184 profile_updates=16384 candidate_point_visits=1073741824
  cell n=10 ratio=0.03125 samples=32768 p=0.25 trials=1 score_pairs=34359738368 profile_updates=32768 candidate_point_visits=1073741824
  cell n=10 ratio=0.03125 samples=32768 p=0.5 trials=1 score_pairs=34359738368 profile_updates=32768 candidate_point_visits=1073741824
```

### n=11 full streaming

```bash
cargo run --manifest-path impl/lsn_cryptanalysis/Cargo.toml \
  --bin lsn_sampled_ambient_ml_sweep -- \
  --n-start 11 --n-end 11 \
  --ratios 0.000244140625,0.015625 \
  --p-values 0.25 \
  --trials 1 \
  --seed 3235823867 \
  --streaming \
  --dry-run
```

Output:

```text
dry-run ambient-ml n=11 streaming=true ambient_candidate_count=4194304 candidate_count=4194304 lagrangian_points=2048 row_storage_points=2048
  cell n=11 ratio=0.000244140625 samples=1024 p=0.25 trials=1 score_pairs=4294967296 profile_updates=1024 candidate_point_visits=8589934592
  cell n=11 ratio=0.015625 samples=65536 p=0.25 trials=1 score_pairs=274877906944 profile_updates=65536 candidate_point_visits=8589934592
```

## Interpretation

For streaming full-candidate ML, the dominant per-cell work is now visible as
`candidate_point_visits`, not row storage and not the legacy `score_pairs`
proxy. Moving from `n=10` to `n=11` increases candidate point visits from
`1,073,741,824` to `8,589,934,592`, an 8x factor for the same trial count.

This makes `n=11` feasible only as a deliberate long-run smoke or targeted
single-cell repeat. It should not be mixed with the capped `n=11` evidence.

## Verification

```bash
cargo test --manifest-path impl/lsn_cryptanalysis/Cargo.toml \
  --bin lsn_sampled_ambient_ml_sweep \
  dry_run_lines_distinguish_streaming_row_storage_from_capped_storage

cargo test --manifest-path impl/lsn_cryptanalysis/Cargo.toml
git diff --check
```

## Next Step

Run one targeted `n=11`, `p=0.25`, full streaming cell at the low-ratio
`samples=1024` setting first. If wall time matches the 8x estimate from `n=10`,
then consider the lower-boundary `samples=65536` single-cell run. Keep any such
run labelled as full streaming, not capped.

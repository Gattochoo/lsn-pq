# Codex P2 Rust ML Brute-Force n=5

**Date:** 2026-06-11
**Actor:** Codex
**Directive:** `meta/2026-06-12-CLAUDE-to-CODEX-next-P1b-P2.md` P2
**Discipline:** Sound Verifier. No 7th; no break; no security claim. OPEN = LSN.

## Scope

This increment extends the P2 Rust ML cryptanalysis harness from the `n=3,4` smoke run to `n=5`,
matching the edge of the adjudicated Kimi Python brute-force ML curve.

The implementation adds a compact scorer:

1. compress samples into per-point true/false label counts;
2. score each candidate Lagrangian as
   `false_total + sum_{a in L}(true_count[a] - false_count[a])`;
3. loop over only `2^n` elements per Lagrangian rather than over all samples.

For `n=5`, this scores `75,735` candidates with `32` point lookups each per trial. The result is still
full brute-force ML over all Lagrangians, not a faster structural attack.

## RED/GREEN Tests

Command:

```bash
cargo test --manifest-path impl/lsn_cryptanalysis/Cargo.toml
```

Status: GREEN, 7 tests passing.

New test:

- `compact_ml_decoder_matches_reference_scorer`: verifies the compact count-aggregated scorer returns
  the same `best_index`, `best_score`, and `runner_up_score` as the reference sample-by-sample scorer
  on a noisy `n=4` instance.

## n=5 Sweep

Command:

```bash
cargo run --manifest-path impl/lsn_cryptanalysis/Cargo.toml --release --bin lsn_ml_sweep -- \
  --n-start 5 \
  --n-end 5 \
  --ratios 0.5,1.0,2.0 \
  --p 0.25 \
  --trials 20 \
  --seed 3235823838 \
  --output experiments/129-codex-p2-rust-ml-bruteforce-n5.json
```

Raw data: `experiments/129-codex-p2-rust-ml-bruteforce-n5.json`.

| n | |Lagr| | m | m / 2^(2n) | p | trials | successes | success rate |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 5 | 75,735 | 512 | 0.5 | 0.25 | 20 | 5 | 0.25 |
| 5 | 75,735 | 1024 | 1.0 | 0.25 | 20 | 18 | 0.90 |
| 5 | 75,735 | 2048 | 2.0 | 0.25 | 20 | 20 | 1.00 |

## Interpretation

This is a Rust implementation cross-check of the already-adjudicated Python trend, not a new proof.
The data remains consistent with the brute-force ML transition occurring around the `2^(2n)` sample
scale, but 20 trials are not enough to pin a sharp threshold.

Threat-model statement: the attacker observes public points and noisy membership labels and then scores
every Lagrangian candidate. This is exhaustive ML over the Lagrangian orbit, so success here is expected
at small `n` and does not constitute a REDUCES result or a claimed break.

Honest status:

- **BROKEN:** no;
- **REDUCES / attack success beyond exhaustive ML:** no;
- **OPEN evidence:** unchanged; this improves implementation coverage only.

## Next Step

Move to a structurally different P2 negative control:

1. span-of-positives at `p=1/4`, with a low-noise sanity case where it should work;
2. then BKW/ISD adaptation screen, with the same low-noise sanity and constant-rate failure control.

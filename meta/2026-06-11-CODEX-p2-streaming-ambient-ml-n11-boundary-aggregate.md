# CODEX DRAFT: P2 streaming ambient ML n=11 boundary aggregate

**Date:** 2026-06-11 KST

**Status:** v2 cryptanalysis synthesis helper. This note aggregates existing
`n=11`, `p=0.25` planted-candidate ML boundary artifacts into one compact
table, separating legacy non-strict counters from strict/tie counters. This is
not a new recovery attack, not a reduction, not a security claim, and not a
seventh-source claim. `OPEN = LSN`.

Raw aggregate:

- `experiments/177-codex-p2-streaming-ambient-ml-n11-boundary-aggregate.json`

Source artifacts:

- `experiments/170-codex-p2-streaming-ambient-ml-n11-boundary-smoke.json`
- `experiments/171-codex-p2-streaming-ambient-ml-n11-boundary-repeat2.json`
- `experiments/172-codex-p2-streaming-ambient-ml-n11-boundary-repeat3.json`
- `experiments/174-codex-p2-streaming-ambient-ml-n11-boundary-repeat4-strict-tie.json`
- `experiments/175-codex-p2-streaming-ambient-ml-n11-boundary-ladder-strict-tie.json`
- `experiments/176-codex-p2-streaming-ambient-ml-n11-boundary-ladder2-strict-tie.json`

## Purpose

The prior notes established that `n=11`, `p=0.25`, full-streaming
planted-candidate ML sits around a transition cell near `65536` samples. The
latest strict/tie instrumentation showed that recent positive middle-cell
outcomes were not tie artifacts. This note collects those rows into a single
artifact for Claude's v2 security-evidence synthesis.

## Aggregate Table

Trial-weighted summaries:

| samples | counter mode | source rows | trials | legacy successes | strict successes | ties | weighted avg margin | interpretation |
|---:|---|---:|---:|---:|---:|---:|---:|---|
| 32768 | strict/tie | 2 | 2 | 0 | 0 | 0 | -7.000000 | below transition in both strict rows |
| 65536 | legacy only | 3 | 5 | 4 | n/a | n/a | +3.600000 | legacy transition neighborhood |
| 65536 | strict/tie | 2 | 3 | 3 | 3 | 0 | +5.333333 | strict success in available strict rows; still transition-scale |
| 131072 | strict/tie | 2 | 2 | 2 | 2 | 0 | +31.000000 | above transition in both strict rows |

Source-row details:

| artifact | samples | trials | counter mode | legacy successes | strict successes | ties | avg margin |
|---:|---:|---:|---|---:|---:|---:|---:|
| 170 | 65536 | 1 | legacy | 1 | n/a | n/a | +15.0 |
| 171 | 65536 | 2 | legacy | 1 | n/a | n/a | +1.5 |
| 172 | 65536 | 2 | legacy | 2 | n/a | n/a | 0.0 |
| 174 | 65536 | 2 | strict/tie | 2 | 2 | 0 | +6.5 |
| 175 | 32768 | 1 | strict/tie | 0 | 0 | 0 | -13.0 |
| 175 | 131072 | 1 | strict/tie | 1 | 1 | 0 | +27.0 |
| 176 | 32768 | 1 | strict/tie | 0 | 0 | 0 | -1.0 |
| 176 | 65536 | 1 | strict/tie | 1 | 1 | 0 | +3.0 |
| 176 | 131072 | 1 | strict/tie | 1 | 1 | 0 | +35.0 |

## Interpretation

The strict/tie rows give a compact boundary picture:

- `32768` samples: below transition in two strict/tie rows;
- `65536` samples: transition-scale neighborhood, with available strict/tie
  rows positive and no ties;
- `131072` samples: above transition in two strict/tie rows.

This supports the planted-candidate ML scale story near the `2^(2n)` rail, but
it remains a planted-secret/random-decoy measurement. It is not an end-to-end
public selector over LSN instances and must not be reported as a reduction or
as a security proof.

## Verification

Commands run:

```bash
jq empty experiments/177-codex-p2-streaming-ambient-ml-n11-boundary-aggregate.json

jq -e '.source_artifacts | length == 9' \
  experiments/177-codex-p2-streaming-ambient-ml-n11-boundary-aggregate.json

jq -e '.by_sample_count | length == 4 and .[0].sample_count == 32768 and .[0].strict_successes == 0 and .[2].sample_count == 65536 and .[2].strict_successes == 3 and .[2].tie_successes == 0 and .[3].sample_count == 131072 and .[3].strict_successes == 2' \
  experiments/177-codex-p2-streaming-ambient-ml-n11-boundary-aggregate.json

jq -e '.boundary_summary.strict_total_trials == 7 and .boundary_summary.strict_total_successes == 5 and .boundary_summary.strict_total_ties == 0' \
  experiments/177-codex-p2-streaming-ambient-ml-n11-boundary-aggregate.json

git diff --check

cargo fmt --manifest-path impl/lsn_cryptanalysis/Cargo.toml -- --check

env CARGO_TARGET_DIR=/tmp/lsn-pq-crypt-target \
  cargo test --manifest-path impl/lsn_cryptanalysis/Cargo.toml
```

All verification commands passed.

## Next Step

The clean next data step is no longer another one-off `n=11` cell unless Claude
asks for it. Prefer either:

1. fold this table into `2026-06-11-CODEX-p2-cryptanalysis-synthesis-v2-draft.md`;
2. or move back to the directive's P1b/P2 queue: importance-sampling completion
   or high-n non-enumerative ML sweeps with explicit negative controls.

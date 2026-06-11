# Codex P2 Positive-Basis ISD Budget Sweep at n=5

**Date:** 2026-06-11
**Actor:** Codex
**Directive:** follow-up from `meta/2026-06-11-CODEX-p2-positive-basis-isd.md`
**Discipline:** Sound Verifier. No 7th; no break; no security claim. OPEN = LSN.

## Scope

This increment checks whether the `n=5,p=1/4` positive-basis ISD failure at `max_attempts=2000`
was merely an attempt-budget artifact.

Implementation refinement:

- added `run_isd_budget_trials`, which reuses the same secret/sample instances across attempt budgets;
- extended `lsn_isd_sweep` with `--attempt-values`;
- preserved `--max-attempts` as the single-budget compatibility path.

The attack remains finite-size and enumeration-assisted: it samples positive bases, checks rank/isotropy,
matches the resulting span against the public Lagrangian orbit, and scores label consistency.

## RED/GREEN Tests

Command:

```bash
cargo test --manifest-path impl/lsn_cryptanalysis/Cargo.toml
```

Status: GREEN, 14 tests passing.

New/strengthened test:

- `isd_budget_runner_preserves_attempt_budgets`: verifies batch output preserves budgets, succeeds in a
  noiseless sanity case, and reuses the same instances across budgets by checking identical average
  positive counts.

## Budget Sweep

Command:

```bash
cargo run --manifest-path impl/lsn_cryptanalysis/Cargo.toml --release --bin lsn_isd_sweep -- \
  --n-start 5 \
  --n-end 5 \
  --ratios 4.0 \
  --p-values 0.25 \
  --trials 10 \
  --attempt-values 2000,10000,50000 \
  --seed 3235823838 \
  --output experiments/132-codex-p2-positive-basis-isd-budget-n5.json
```

Raw data: `experiments/132-codex-p2-positive-basis-isd-budget-n5.json`.

| n | m | p | trials | max attempts | successes | success rate | avg positives | avg valid candidates | avg best score |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 5 | 4096 | 0.25 | 10 | 2,000 | 0 | 0.00 | 1086.9 | 1.2 | 2078.9 |
| 5 | 4096 | 0.25 | 10 | 10,000 | 1 | 0.10 | 1086.9 | 7.0 | 2988.3 |
| 5 | 4096 | 0.25 | 10 | 50,000 | 3 | 0.30 | 1086.9 | 36.1 | 3026.3 |

## Interpretation

The earlier `0/10` at 2000 attempts was partly an attempt-budget artifact: increasing the cap to
50,000 attempts recovers `3/10` of the same-distribution `n=5,p=1/4` trials.

This is still **not** a REDUCES result and not a claimed break:

- the attempt count is already far above `2^(2n)=1024` for `n=5`;
- the implementation still uses public Lagrangian-orbit matching and full-sample scoring;
- this is a small-`n` finite-size ISD tradeoff, not a polynomial structural map;
- no n-scaling beyond `n=5` is established here.

The useful finding is narrower: positive-basis ISD is not completely dead at `n=5,p=1/4`, but its
success requires a much larger attempt budget and remains firmly in the finite-size / brute-force
screen category.

Honest status:

- **BROKEN:** no;
- **REDUCES / scalable attack success:** no;
- **small-n finite-size success:** yes, at 50k attempts `3/10`;
- **OPEN evidence:** unchanged.

## Next Step

Move to a non-enumerative BKW-style bucket screen or an ISD cost model note. If pursuing ISD further,
the next experiment must avoid orbit matching as a hidden exhaustive helper and must report time/work
relative to direct `|Lagr(2n,F2)|` scoring.

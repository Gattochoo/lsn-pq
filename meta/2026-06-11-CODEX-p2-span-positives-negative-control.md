# Codex P2 Span-of-Positives Negative Control

**Date:** 2026-06-11
**Actor:** Codex
**Directive:** `meta/2026-06-12-CLAUDE-to-CODEX-next-P1b-P2.md` P2
**Discipline:** Sound Verifier. No 7th; no break; no security claim. OPEN = LSN.

## Scope

This increment adds a structurally different P2 attack baseline: span the public points whose noisy
membership label is `1`.

Attack rule:

1. collect all samples `(a,b)` with `b=1`;
2. compute the `F2` span rank of those positive points;
3. if the span has rank exactly `n`, compare it against the Lagrangian orbit;
4. otherwise report failure, with overfull/full-rank counters.

This attack is expected to work in a low/no-noise sanity setting and fail at constant-rate noise,
because false positives outside the secret Lagrangian rapidly span the ambient `F2^(2n)`.

## RED/GREEN Tests

Command:

```bash
cargo test --manifest-path impl/lsn_cryptanalysis/Cargo.toml
```

Status: GREEN, 11 tests passing.

New tests:

- noiseless full observation recovers the secret Lagrangian exactly;
- all-positive/full-space labels are rejected with span rank `2n`;
- trial runner recovers noiseless sampled instances;
- JSON records overfull-rank failure statistics.

## Negative-Control Sweep

Command:

```bash
cargo run --manifest-path impl/lsn_cryptanalysis/Cargo.toml --release --bin lsn_span_sweep -- \
  --n-start 3 \
  --n-end 5 \
  --ratios 4.0 \
  --p-values 0.0,0.25 \
  --trials 10 \
  --seed 3235823838 \
  --output experiments/130-codex-p2-span-positives-negative-control.json
```

Raw data: `experiments/130-codex-p2-span-positives-negative-control.json`.

| n | m | p | trials | successes | success rate | rank=n | overfull | full-rank | avg positives | avg span rank |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 | 256 | 0.00 | 10 | 10 | 1.00 | 10 | 0 | 0 | 35.8 | 3 |
| 3 | 256 | 0.25 | 10 | 0 | 0.00 | 0 | 10 | 10 | 78.5 | 6 |
| 4 | 1024 | 0.00 | 10 | 10 | 1.00 | 10 | 0 | 0 | 67.8 | 4 |
| 4 | 1024 | 0.25 | 10 | 0 | 0.00 | 0 | 10 | 10 | 293.4 | 8 |
| 5 | 4096 | 0.00 | 10 | 10 | 1.00 | 10 | 0 | 0 | 133.7 | 5 |
| 5 | 4096 | 0.25 | 10 | 0 | 0.00 | 0 | 10 | 10 | 1086.9 | 10 |

## Interpretation

The span-of-positives attack passes the required sanity check: at `p=0`, sampled positives span the
secret Lagrangian and recover it for `n=3,4,5`.

At constant-rate `p=1/4`, the same attack fails for every trial in this sweep. The mechanism is not a
mysterious decoder weakness: the positive set is contaminated by many false positives outside `L`, and
its span reaches the full ambient rank `2n` in every measured trial.

Honest status:

- **BROKEN:** no;
- **REDUCES / attack success:** no;
- **negative control:** yes, the attack works where it should and fails where the noise-wall predicts;
- **OPEN evidence:** unchanged; this is an implementation-backed attack-family dismissal, not a proof.

## Next Step

The next P2 lane should use the same pattern:

1. low-noise sanity case where the attack must work;
2. constant-rate control at `p=1/4`;
3. explicit mechanism of failure.

Good candidates: ISD-style positive-basis search with capped attempts, then a BKW-style bucket screen.

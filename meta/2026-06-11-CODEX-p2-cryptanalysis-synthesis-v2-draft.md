# Codex P2 Cryptanalysis Synthesis for v2 Draft

**Date:** 2026-06-11
**Actor:** Codex
**Directive:** `2026-06-12-CLAUDE-adjudication-codex-p1b-p2-and-directives.md`, Codex A2
**Discipline:** Sound Verifier. No 7th; no break; no security claim. OPEN = LSN.

## Executive Summary

Codex's P2 Rust cryptanalysis track tested exhaustive ML, non-enumerative sampled ML, ISD-style
positive-basis search, span-of-positives, BKW-style bucket observables, and a non-xor bucket
certificate. Every lane kept explicit negative controls and threat-model notes. The combined result
is:

```text
BROKEN: no
REDUCES: no
Public selector/recovery: not found
Sub-2^(2n) attack success: not observed
Best empirical reading: tested attacks align with, or fail before, the 2^(2n) sample rail
```

This is evidence for the v2 security-evidence section, not a proof of hardness.

## Consolidated Attack Table

| Attack family | Artifact(s) | Threat model / helper | Range | Budget / scale | Outcome | Relation to `2^(2n)` | Adjudication |
|---|---|---|---:|---:|---|---|---|
| Exhaustive ML over all Lagrangians | `128`, `129`; `CODEX-p2-rust-ml-bruteforce-*` | Full Lagrangian orbit scored; exhaustive at small `n` | `n=3..5` | `m/2^(2n) in {0.5,1,2}` | Transition occurs near the expected `2^(2n)` sample scale; `n=5` reaches 18/20 at ratio 1 and 20/20 at ratio 2 | Matches rail; does not beat it | ACCEPT as calibration; not REDUCES |
| Span of positives | `130`; `CODEX-p2-span-positives-negative-control.md` | Uses positive labels only; no orbit search unless span rank is exactly `n` | `n=3..5` | `m=4*2^(2n)` | `p=0` recovers 10/10; `p=1/4` fails 0/10 and spans full ambient rank `2n` | Constant-rate noise destroys the naive span signal | Negative control; not an attack |
| Positive-basis ISD | `131`, `132`; `CODEX-p2-positive-basis-isd*.md` | Samples positive `n`-tuples, checks rank/isotropy, then orbit-matches/scored candidates | `n=3..5` | Attempts `2k`, `10k`, `50k` at `n=5` | Small-`n` finite-size successes; at `n=5,p=1/4`, 50k attempts gives only 3/10 | 50k attempts already far above `2^(2n)=1024`; no speedup evidence | Small-case finite-size, not REDUCES |
| BKW bucket-pair observable | `133`; `CODEX-p2-bkw-bucket-screen.md` | Non-enumerative bucket pairing; secret used only for diagnostic delta-gap measurement | `n=4..8` | `m=2^(2n)`, one-round bucket pairing | `p=0` positive control works; `p=1/4` delta-gap collapses near random floor by `n=6..8` | No constant-rate structural signal below the rail | Negative for one-round BKW |
| BKW label-xor noise model | `134`; `CODEX-p2-bkw-noise-growth-model.md` | Analytic recurrence for label-xor transforms | model | rounds 0..6 | Bias obeys `b -> b^2`; at `p=1/4`, three xor rounds leave bias `1/256` | Explains why straightforward BKW gets harder, not easier | Noise obstruction pinned |
| Non-xor bucket certificate | `135`; `CODEX-p2-bucket-certificate-screen.md` | Public bucket rate variance; secret only for projection-size diagnostic | `n=4..8` | `m=64*2^(2n)`, `bucket_bits=n+2` | Measurable `p=1/4` signal remains but scales like `Theta(4^-n)` | Sees structure at the same `2^(2n)` scale, not below it | Useful diagnostic; not REDUCES |
| Sampled-candidate ML, fixed cloud | `136`; `CODEX-p2-sampled-candidate-ml.md` | Secret planted as candidate 0 among random decoys | `n=6..10` | 512 decoys; ratios `{0.25,1,4}` | Clean separation at moderate `n`; `p=1/2` control fails | Candidate cloud too small to test full rail | Sanity harness only |
| Candidate-count scaling and EV model | `137`, `138`; `CODEX-p2-sampled-candidate-count-scaling.md`, `CODEX-p2-sampled-candidate-ev-model.md` | Planted secret plus random decoys; false-max pressure modeled | `n=8..10` | up to 32768 candidates; model includes 131072 | Candidate pressure visible; Gaussian extreme-value proxy is conservative; `p=1/2` negative | Explains finite-cloud margins as ordinary ML separation | Interpretation model; not recovery |
| 131k planted and all-random false-max controls | `139`, `140`; `CODEX-p2-sampled-candidate-131k-stress.md`, `CODEX-p2-sampled-candidate-false-max-control.md` | Planted candidate stress plus unplanted false-max reference | `n=10` | 131072 candidates; ratios `{0.0625,0.125}` | Planted and unplanted false-max margins track closely; `p=1/2` fails | Confirms false-max explanation, not public search | Calibration only |
| Ambient-size sampled-candidate ML | `141`..`144`; `CODEX-p2-ambient-size-ml-*.md` | Non-enumerative random-secret plus random-decoy cloud with planted secret | `n=6..8` | `candidate_count=2^(2n)`; boundary trials 20, n=8 addendum 50 | Transition stays at `m=c*2^(2n)` for small constant `c`; n=8 50-trial addendum has 24/50 at ratio 0.0625 and 46/50 at ratio 0.125; p=1/2 control 0/30 | Direct high-`n` calibration on the rail | v2-ready evidence; not REDUCES |
| Full-streaming ambient-size sampled ML | `170`..`177`; `CODEX-p2-streaming-ambient-ml-n11-boundary-*.md` | Same planted-secret/random-decoy score landscape, but streams the full `2^(2n)` decoy cloud without storing it | `n=11` | `candidate_count=2^22`; strict/tie rows at samples `{32768,65536,131072}` | Strict/tie aggregate: 32768 gives 0/2 strict, 65536 gives 3/3 strict and 0 ties in strict rows, 131072 gives 2/2 strict | Extends the planted-candidate ML rail check to `n=11`; still not public recovery | v2-ready score-landscape evidence; not REDUCES |

## Most Useful v2 Table

For a compact paper appendix/table, the strongest rows are:

| Evidence class | Clean positive control | Constant-rate result | Paper use |
|---|---|---|---|
| Exhaustive ML | Full scoring recovers at small `n` once `m` reaches the rail | `n=3..5` transition near `2^(2n)` | Establishes empirical baseline |
| Ambient-size sampled ML | Planted random-decoy cloud succeeds only at constant fractions of `2^(2n)` | `n=6..8`, 20-trial boundary table | Extends ML rail beyond full enumeration |
| Full-streaming ambient ML | Streaming `2^(2n)` random-decoy cloud separates only around the same rail-scale neighborhood | `n=11`, strict/tie boundary aggregate | Extends score-landscape calibration without storing all decoys |
| Span positives | `p=0` recovers exactly | `p=1/4` spans ambient space and fails | Explains why raw positives do not recover `L` |
| ISD positive basis | `p=0` recovers | `n=5,p=1/4` needs 50k attempts for only 3/10 | No ISD speedup evidence |
| BKW label-xor | `p=0` bucket signal visible | Bias squaring kills constant-rate rounds | Blocks straightforward BKW |
| Non-xor bucket certificate | `p=0`/`p=1/4` signal measurable | Signal scales as `Theta(4^-n)` | Shows structure exists but at rail scale |

## Cost vs `2^(2n)` Rail Table

The following table is the paper-facing calibration core. It reports costs in units of
`R_n = 2^(2n)`, the ambient sample rail appearing in the informal security discussion. All rows are
empirical checks or score-landscape calibrations, not hardness proofs.

### Exhaustive/full-orbit ML calibration

| n | candidate set | samples | samples / `R_n` | trials | successes | result |
|---:|---:|---:|---:|---:|---:|---|
| 5 | all Lagrangians | 512 | 0.5000 | 20 | 5 | below-rail transition region |
| 5 | all Lagrangians | 1024 | 1.0000 | 20 | 18 | near/full rail succeeds |
| 5 | all Lagrangians | 2048 | 2.0000 | 20 | 20 | above rail succeeds |

Artifacts: `experiments/129-codex-p2-rust-ml-bruteforce-n5.json`,
`meta/2026-06-11-CODEX-p2-rust-ml-n5.md`.

### Ambient-size sampled ML calibration

These runs avoid enumerating all Lagrangians. They plant the secret into an ambient-sized random
candidate cloud of size `2^(2n)`, then measure whether ordinary ML scoring separates the planted
candidate from random false maxima.

| n | candidate count | samples | samples / `R_n` | trials | successes | success rate | avg secret margin |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 6 | 4096 | 384 | 0.09375 | 20 | 4 | 0.20 | -2.00 |
| 6 | 4096 | 512 | 0.12500 | 20 | 10 | 0.50 | -0.75 |
| 6 | 4096 | 768 | 0.18750 | 20 | 11 | 0.55 | 0.05 |
| 6 | 4096 | 1024 | 0.25000 | 20 | 17 | 0.85 | 2.60 |
| 7 | 16384 | 1536 | 0.09375 | 20 | 10 | 0.50 | 0.15 |
| 7 | 16384 | 2048 | 0.12500 | 20 | 15 | 0.75 | 2.40 |
| 7 | 16384 | 3072 | 0.18750 | 20 | 19 | 0.95 | 5.35 |
| 7 | 16384 | 4096 | 0.25000 | 20 | 18 | 0.90 | 8.55 |
| 8 | 65536 | 4096 | 0.06250 | 50 | 24 | 0.48 | -0.72 |
| 8 | 65536 | 6144 | 0.09375 | 50 | 42 | 0.84 | 4.04 |
| 8 | 65536 | 8192 | 0.12500 | 50 | 46 | 0.92 | 7.42 |

Artifacts: `experiments/142-codex-p2-ambient-size-ml-boundary-n6-n8.json`,
`experiments/143-codex-p2-ambient-size-ml-n8-50trial-boundary.json`,
`meta/2026-06-11-CODEX-p2-ambient-size-ml-boundary-n6-n8.md`,
`meta/2026-06-11-CODEX-p2-ambient-size-ml-n8-50trial-boundary.md`.

### Random-label negative control

The matched `n=8` random-label control uses the same candidate count and sample counts as the
presentation-quality boundary cells. The planted candidate is not separated when labels carry no
secret signal.

| n | candidate count | samples | samples / `R_n` | trials | successes | success rate | avg secret margin |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 8 | 65536 | 4096 | 0.06250 | 30 | 0 | 0.00 | -17.93 |
| 8 | 65536 | 6144 | 0.09375 | 30 | 0 | 0.00 | -21.73 |
| 8 | 65536 | 8192 | 0.12500 | 30 | 0 | 0.00 | -24.47 |

Artifact: `experiments/144-codex-p2-ambient-size-ml-n8-random-control.json`.

### Full-streaming ambient-size sampled ML at n=11

The `n=11` streaming runs avoid materializing the full random-decoy cloud while still scoring
`candidate_count = 2^(2n) = 4,194,304` planted/random candidates. These are still
planted-candidate score-landscape calibrations, not public selectors. The strict/tie counters
separate genuine score wins from score ties.

| n | candidate count | samples | samples / `R_n` | source rows | strict successes | ties | weighted avg margin | result |
|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 11 | 4,194,304 | 32,768 | 0.0078125 | 2 | 0 | 0 | -7.000000 | below transition |
| 11 | 4,194,304 | 65,536 | 0.0156250 | 2 | 3 | 0 | +5.333333 | transition-scale strict success in available rows |
| 11 | 4,194,304 | 131,072 | 0.0312500 | 2 | 2 | 0 | +31.000000 | above transition |

Legacy non-strict middle rows at `65,536` samples add `4/5` legacy successes with weighted average
margin `+3.600000`, but they predate strict/tie counters and should not be merged with strict rows.

Artifacts: `experiments/170-codex-p2-streaming-ambient-ml-n11-boundary-smoke.json`,
`experiments/171-codex-p2-streaming-ambient-ml-n11-boundary-repeat2.json`,
`experiments/172-codex-p2-streaming-ambient-ml-n11-boundary-repeat3.json`,
`experiments/174-codex-p2-streaming-ambient-ml-n11-boundary-repeat4-strict-tie.json`,
`experiments/175-codex-p2-streaming-ambient-ml-n11-boundary-ladder-strict-tie.json`,
`experiments/176-codex-p2-streaming-ambient-ml-n11-boundary-ladder2-strict-tie.json`,
and aggregate `experiments/177-codex-p2-streaming-ambient-ml-n11-boundary-aggregate.json`.

## Threat-Model Separation Table

| Lane | Attacker-visible input | Secret used only for diagnostics? | What the result may say | What it must not say |
|---|---|---|---|---|
| Full-orbit ML | public samples plus exhaustive small-`n` orbit | no, except ground-truth success check | calibrates the ML rail where enumeration is possible | public polynomial recovery |
| Ambient sampled ML | public samples plus planted candidate cloud | yes, to plant one candidate and score success | measures score separation against `2^(2n)` false maxima | an attack without candidate oracle |
| Full-streaming ambient sampled ML | public samples plus streamed planted/random candidate cloud | yes, to plant one candidate and score success | extends the same score-separation measurement to `n=11` without storing all candidates | public polynomial recovery or reduction |
| Span positives | positive labels only | yes, for success/rank diagnostic | raw positive span is killed by constant noise | reduction or hardness proof |
| Positive-basis ISD | positive tuples and public isotropy/rank tests | yes, for orbit match/scoring | no observed speedup over brute rail | asymptotic ISD impossibility |
| BKW/bucket | public bucket aggregates | yes, for delta-gap/projection diagnostics | straightforward bucket signals collapse or scale at rail | secret recovery |

This separation is the main Sound-Verifier guardrail for v2: the strongest ML rows are
score-landscape evidence, while the public structural probes are negative or rail-scale diagnostics.

## Suggested v2 Wording

The following text is suitable as a draft paragraph for Claude to adapt, not as final paper text:

> We implemented a Rust cryptanalysis harness for membership-LSN and tested exhaustive ML,
> sampled-candidate ML, positive-span recovery, positive-basis ISD, BKW-style bucket observables,
> and non-xor bucket certificates. Each attack was paired with a sanity case where the method should
> work and a constant-rate noise control. No tested method produced a public recovery map or a
> reduction below the `2^(2n)` sample rail. Exhaustive ML at `n <= 5` and ambient-size sampled ML at
> `n=6..8`, with full-streaming planted-candidate checks at `n=11`, both show transitions at
> constant fractions of `2^(2n)`. Span-positive, ISD, BKW, and bucket-certificate probes either fail
> at constant noise or retain only signals whose size matches the same `2^(2n)` scale. These
> experiments are evidence, not a proof of hardness.

## Limits and Sound-Verifier Notes

- The sampled-candidate and ambient-size ML lanes plant the secret into the candidate cloud. They are
  score-landscape calibrations, not public recovery attacks.
- ISD lanes use finite-size orbit matching and should not be extrapolated as a family attack.
- Bucket and BKW lanes include diagnostic uses of the secret only for measurement, not as attacker
  input.
- The result is not a 7th-source proof and not a security theorem.
- A future attack that beats `2^(2n)` must stop this synthesis and be escalated as CLOSURE-GRADE.

## Raw Artifact Index

| ID | File |
|---:|---|
| 128 | `experiments/128-codex-p2-rust-ml-bruteforce-smoke.json` |
| 129 | `experiments/129-codex-p2-rust-ml-bruteforce-n5.json` |
| 130 | `experiments/130-codex-p2-span-positives-negative-control.json` |
| 131 | `experiments/131-codex-p2-positive-basis-isd.json` |
| 132 | `experiments/132-codex-p2-positive-basis-isd-budget-n5.json` |
| 133 | `experiments/133-codex-p2-bkw-bucket-screen.json` |
| 134 | `experiments/134-codex-p2-bkw-noise-growth-model.json` |
| 135 | `experiments/135-codex-p2-bucket-certificate-screen.json` |
| 136 | `experiments/136-codex-p2-sampled-candidate-ml.json` |
| 137 | `experiments/137-codex-p2-sampled-candidate-count-scaling.json` |
| 138 | `experiments/138-codex-p2-sampled-candidate-ev-model.json` |
| 139 | `experiments/139-codex-p2-sampled-candidate-131k-stress.json` |
| 140 | `experiments/140-codex-p2-sampled-candidate-false-max-control.json` |
| 141 | `experiments/141-codex-p2-ambient-size-ml-n6-n8.json` |
| 142 | `experiments/142-codex-p2-ambient-size-ml-boundary-n6-n8.json` |
| 143 | `experiments/143-codex-p2-ambient-size-ml-n8-50trial-boundary.json` |
| 144 | `experiments/144-codex-p2-ambient-size-ml-n8-random-control.json` |
| 170 | `experiments/170-codex-p2-streaming-ambient-ml-n11-boundary-smoke.json` |
| 171 | `experiments/171-codex-p2-streaming-ambient-ml-n11-boundary-repeat2.json` |
| 172 | `experiments/172-codex-p2-streaming-ambient-ml-n11-boundary-repeat3.json` |
| 174 | `experiments/174-codex-p2-streaming-ambient-ml-n11-boundary-repeat4-strict-tie.json` |
| 175 | `experiments/175-codex-p2-streaming-ambient-ml-n11-boundary-ladder-strict-tie.json` |
| 176 | `experiments/176-codex-p2-streaming-ambient-ml-n11-boundary-ladder2-strict-tie.json` |
| 177 | `experiments/177-codex-p2-streaming-ambient-ml-n11-boundary-aggregate.json` |

## Next Step

Hand this synthesis to Claude for v2 insertion. The first small consistency check is now recorded in
`meta/2026-06-11-CODEX-p2-ambient-boundary-ci.md`, which adds Wilson intervals to experiment 142 and
keeps the 20-trial boundary table from being overread.

The n=8 presentation-quality replication is now recorded in
`meta/2026-06-11-CODEX-p2-ambient-size-ml-n8-50trial-boundary.md`, with structured 50-trial boundary
cells and a matched `p=1/2` random-label control.

The n=11 full-streaming extension is now recorded in
`meta/2026-06-11-CODEX-p2-streaming-ambient-ml-n11-boundary-aggregate.md`, with a strict/tie
boundary aggregate over `{32768,65536,131072}` samples. It should be cited only as
planted-candidate score-landscape evidence.

If Codex continues before Claude adjudicates, the next useful work is not another broad attack
family. Prefer either a bounded P1b importance-sampling attempt, an explicit high-noise negative
control for the next polar-rate sweep, or a Claude-requested presentation pass:

```text
do not start a new attack family unless it has a clear threat model and controls.
```

That would improve presentation quality without changing the adjudication.

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
| Ambient-size sampled-candidate ML | `141`, `142`; `CODEX-p2-ambient-size-ml-*.md` | Non-enumerative random-secret plus random-decoy cloud with planted secret | `n=6..8` | `candidate_count=2^(2n)`; boundary trials 20 | Transition stays at `m=c*2^(2n)` for small constant `c`; no point gives polynomial-sample recovery | Direct high-`n` calibration on the rail | v2-ready evidence; not REDUCES |

## Most Useful v2 Table

For a compact paper appendix/table, the strongest rows are:

| Evidence class | Clean positive control | Constant-rate result | Paper use |
|---|---|---|---|
| Exhaustive ML | Full scoring recovers at small `n` once `m` reaches the rail | `n=3..5` transition near `2^(2n)` | Establishes empirical baseline |
| Ambient-size sampled ML | Planted random-decoy cloud succeeds only at constant fractions of `2^(2n)` | `n=6..8`, 20-trial boundary table | Extends ML rail beyond full enumeration |
| Span positives | `p=0` recovers exactly | `p=1/4` spans ambient space and fails | Explains why raw positives do not recover `L` |
| ISD positive basis | `p=0` recovers | `n=5,p=1/4` needs 50k attempts for only 3/10 | No ISD speedup evidence |
| BKW label-xor | `p=0` bucket signal visible | Bias squaring kills constant-rate rounds | Blocks straightforward BKW |
| Non-xor bucket certificate | `p=0`/`p=1/4` signal measurable | Signal scales as `Theta(4^-n)` | Shows structure exists but at rail scale |

## Suggested v2 Wording

The following text is suitable as a draft paragraph for Claude to adapt, not as final paper text:

> We implemented a Rust cryptanalysis harness for membership-LSN and tested exhaustive ML,
> sampled-candidate ML, positive-span recovery, positive-basis ISD, BKW-style bucket observables,
> and non-xor bucket certificates. Each attack was paired with a sanity case where the method should
> work and a constant-rate noise control. No tested method produced a public recovery map or a
> reduction below the `2^(2n)` sample rail. Exhaustive ML at `n <= 5` and ambient-size sampled ML at
> `n=6..8` both show transitions at constant fractions of `2^(2n)`. Span-positive, ISD, BKW, and
> bucket-certificate probes either fail at constant noise or retain only signals whose size matches
> the same `2^(2n)` scale. These experiments are evidence, not a proof of hardness.

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

## Next Step

Hand this synthesis to Claude for v2 insertion. The first small consistency check is now recorded in
`meta/2026-06-11-CODEX-p2-ambient-boundary-ci.md`, which adds Wilson intervals to experiment 142 and
keeps the 20-trial boundary table from being overread.

If Codex continues before Claude adjudicates, the next useful work is not another broad attack
family but a presentation-quality replication:

```text
re-run the ambient-size ML boundary at n=8 only with more trials if v2 needs tighter intervals.
```

That would improve presentation quality without changing the adjudication.

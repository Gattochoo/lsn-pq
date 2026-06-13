# Track O — lem:m2 exact SD frontier at n = 3

**Date:** 2026-06-14.  **Experiment:** 300.  **Commit prefix:** `track-O:`.

## What was proved / computed

**THEOREM (sufficient-statistic reduction, n = 3).**  At n = 3 the eight row
types τ ∈ F_2^3 are interchangeable under GL(3, F_2).  Rank, the membership
signature set {w : s_τ = m_τ ⟨τ, w⟩ ∀τ}, and the LPN sum over secrets are
invariant under a simultaneous permutation of the eight (m_τ, s_τ) slots.
We therefore canonicalise the seven non-zero slots by GL(3, F_2)-orbits and
multiply each canonical state by the exact orbit size 168 / |Stab|.

*Proof obligations satisfied in code (experiments/300):*
1. Anchor check: the reduced SD agrees fraction-for-fraction with the exact
   n = 3 table from Tracks 203/216 for every m ≤ 12.
2. Orbit-count sanity: the weighted canonical count equals the full ordered
   count `C(m+14, 14)` for the sampled anchor range.

**THEOREM (s_00 pure-shift vectorisation).**  Because ⟨00, w⟩ = 0 for every
secret w, the LPN side depends on s_00 only through the common factor
`C(m_00, s_00) a^{s_00} b^{m_00-s_00}` and the graph side forces s_00 = 0.
For a fixed residual state the sum over s_00 is a one-parameter absolute-value
sum with at most one sign change (since a < b), so it is evaluated in closed
form using precomputed binomial prefix sums.

**Exact SD table (n = 3, p_eff(3) = 3367/8192, q_graph(3) = 1241/4608).**

|  m  | SD (exact) | SD (float) | 1 − SD |
|----:|-----------:|-----------:|--------:|
| 16 | `9272112116643244103389384941311517123385373690769807374709838925226599842879/32566525097995179962879339533693474083732183187211408636097445502225567711232` | 0.284713 | 0.715287 |
| 20 | `5618525593368526494039694369428501875601896478072157788190319004096992710358317764515726415584893/19223883323288190741555195355525969031424340701209874929523374470399977532025764950206658782429184` | 0.292268 | 0.707732 |
| 24 | `106397724615480044212109000285864774888808285560814699506086670015282805483012767009383480326592264013663887961574725/354618055767550312910511360901292524245717653434189020011534640638211495943474895502728396293964240767259651912761344` | 0.300035 | 0.699965 |

The m ≤ 12 values are reproduced exactly as a cross-check against
`experiments/output/203-trackF-sufficient-statistic-n3.json` and
`experiments/output/216-trackN-n3.json`.

**Cross-n 1 − SD comparison at matched m/n ratios.**

| ratio | n = 2 (m) | 1 − SD (n = 2) | n = 3 (m) | 1 − SD (n = 3) |
|------:|----------:|---------------:|----------:|---------------:|
| 2 | 4 | 0.747319 | 6 | 0.783374 |
| 3 | 6 | 0.625093 | 9 | 0.735888 |
| 4 | 8 | 0.562995 | 12 | 0.723460 |
| 6 | 12 | 0.509529 | — | — |
| 8 | 16 | 0.481096 | 24 | 0.699965 |

(Values for n = 2 come from experiments/202 and experiments/204.)

These are the first matched-ratio data for the lem:m2 rate.  The 1 − SD
values at n = 3 are larger than at n = 2 at the same ratio, i.e. the decay
is somewhat slower when normalised by n.  This is **EVIDENCE**, not a theorem.

## Files

* `experiments/300-KIMI-trackO-n3-reduced-SD.py` — main reduced exact SD
  computation at n = 3; GL(3, F_2) orbit canonicalisation + s_00 pure-shift
  vectorisation; anchor check against Tracks 203/216; cross-n comparison.
* `experiments/output/300-trackO-n3-reduced-SD.json`

## Claim labels

* `sufficient_statistic_reduction_n3` — **THEOREM** (proved; verified by
  direct enumeration for m ≤ 12).
* `gl3_f2_orbit_canonicalisation` — **THEOREM** (recursive colour-class orbit
  enumeration; stabiliser gives exact orbit size 168 / |Stab|).
* `s00_pure_shift_vectorisation` — **THEOREM** (proved; denominator
  divisibility explicit).
* `n3_exact_sd_m_16` — **EVIDENCE** (exact finite computation).
* `n3_exact_sd_m_20` — **EVIDENCE** (exact finite computation).
* `n3_exact_sd_m_24` — **EVIDENCE** (exact finite computation, detached run
  completed in ~266 s).
* `cross_n_rate` — **EVIDENCE** (first matched-ratio 1-SD comparison across
  n = 2, 3).
* `lem_m2_status` — **OPEN**.

## PRE-REGISTER interpretation guards

* **Axis:** all conclusions are on the m-axis at fixed n = 3; no
  fixed-small-m hardness claim is made.
* **Comparison distribution:** P_lpn is `LPN_{p_eff(3)}`, the matched-rate
  target, not `LPN_{1/4}`.
* **p_eff caveat:** `p_eff(3) = 3367/8192 ≈ 0.4109` is very close to 1/2;
  the SD numbers measure detectability of correlation inside a nearly
  vacuous LPN regime and do not imply a practical distinguisher for
  standard LPN.
* **Practical meaning:** SD is a distance between two explicit distributions;
  it does not by itself imply an attack.

## Standing guards

* **L1 exact arithmetic:** all arithmetic uses integer counts over the common
  denominator `q_den * N * (2N)^m * D^m`.  `q_graph(3) = 1241/4608` keeps the
  odd factor 9 = 4608 / 2^9; no floor division is used anywhere.
* **L2 J-twist care:** the row-type inner product is the standard F_2 pairing
  ⟨w, τ⟩; no symplectic dual is involved here.
* **L3 query-class hygiene:** any SQ statement names its query class
  explicitly; the unrestricted Feldman theorem is not invoked.
* **L4 comparison-distribution care:** the LPN target is the matched-rate
  product distribution and is never transformed or post-processed.

## Status

Committed as `track-O:` (one track-only commit).  Pushed to `origin/main`.

# Track L — lem:m2 exact SD reaches m = 64 and m = 80 at n = 2

**Date:** 2026-06-14.  **Experiments:** 204, 205.  **Commit prefix:** `track-L:`.

## What was proved / computed

**THEOREM (S_3 symmetry reduction).**  At n = 2 the three non-zero row types
τ ∈ F_2^2 \\ {00} are interchangeable under GL(2, F_2) ≅ S_3.  Rank, the
membership signature set, and the LPN sum over secrets are invariant under a
simultaneous permutation of the three slots (m_τ, s_τ).  We therefore
canonicalise by sorting the three non-zero pairs by (m, s) descending and
multiplying each canonical state by its exact orbit size
(3! divided by the automorphism factor of equal pairs).

*Proof obligations satisfied in code (experiments/205):*
1. Orbit counting: the weighted canonical count equals the full ordered count
   of residual states `C(m+6, 6)` for every m ≤ 12.
2. Value invariance: the reduced SD agrees with direct T-level enumeration for
   m ≤ 6.

**THEOREM (s_00 pure-shift vectorisation).**  Because ⟨00, w⟩ = 0 for every
secret w, the LPN side depends on s_00 only through the common factor
`C(m_00, s_00) a^{s_00} b^{m_00-s_00}` and the graph side forces s_00 = 0.
For a fixed residual state the sum over s_00 is therefore a single-parameter
sum with at most one sign change (since a < b), so it can be evaluated in
closed form using precomputed binomial prefix sums.

*Proof obligations satisfied in code (experiments/205):*
1. The closed-form `s_00`-sum agrees with brute-force summation on 200 random
   residual states.
2. The denominator divisibility is explicit: every probability remains an
   integer count over `q_den * N * (2N)^m * D^m`.

**Exact SD table (n = 2, p_eff(2) = 175/512, q_graph(2) = 29/64).**

|  m  | SD (exact) | SD (float) | 1 − SD |
|----:|-----------:|-----------:|--------:|
| 24 | `16832756036765379095034202127924274618943844971887062499211392003318774009896365/29642774844752946028434172162224104410437116074403984394101141506025761187823616` | 0.567854 | 0.432146 |
| 32 | `175842639268182236234225149971230384237897459955496283666363584364067225210764143038987088768788053693215/286687326998758938951352611912760867599570623646035140467198604923365359511060601008752319138765710819328` | 0.613360 | 0.386640 |
| 48 | `607477461132137352864009669432561278876547085540963876824000902259324180705585729760268074621527447131000809903636388269236874471512931193096020288141170484925/878694100496718043517683302282418331810487718418343092402491322775749527474899974671687634004666183037093927858109549828751614463963730408009475621262727315456` | 0.691341 | 0.308659 |
| **64** | `994589338556012737306767984053993866401627777861394352868857678493401889916198751722830201286170625337020044130086296382696192819110311995966196117718885070120581909566878066697798814676718331556076549874025265/1315033975387093376810247470720032166387584950705793464874570225767183038574270205528416634069397112806745742214044554428254858062545950965781953692662970212488805917782111149547915939471080679317823312933945344` | 0.756322 | 0.243678 |
| **80** | `6516657278891803832616236589954945406172739657093806040686943620569987057254109683197704791668274095220191620119308395368727282099557476622237619203792218538492257452368734407090320092262117702049733273480579682532654279485633996703894025267592898163193163092524325/8061134813471454564702450331367746071149403778627342561766978592325956765086744071570087522699847227396765060321916636335485039665263146015175460486800225477728068298324662539195732386420081192825687147647265448061340763744378078290380812053940375922997109693874176` | 0.808404 | 0.191596 |

The m = 24, 32, 48 values are reproduced exactly as a cross-check against the
Track F table (experiments/202).  m = 80 was *not* a wall on this machine
(≈ 3 minutes); the honest wall would be only slightly beyond this.

**Updated 1 − SD decay fit (n = 2, m ≥ 8 including the new points).**

* Exponential: `1 − SD ≈ exp(−0.4856 − 0.0145 m)`.
* Power-law:   `1 − SD ≈ 3.5559 · m^(−0.6513)`.

Both are finite-sample regressions, not proven asymptotics.

## Files

* `experiments/204-KIMI-trackL-sufficient-statistic-m64.py` — main reduced
  exact SD computation; m = 64 and m = 80.
* `experiments/205-KIMI-trackL-reduction-verification.py` — independent
  verification of S_3 orbit counting, S_3 value invariance, and the s_00
  pure-shift closed form; anchor check at m = 24, 32, 48.
* `experiments/output/204-trackL-sufficient-statistic-m64.json`
* `experiments/output/205-trackL-reduction-verification.json`

## Claim labels

* `s3_symmetry_reduction` — **THEOREM** (proved; verified by direct
  enumeration for m ≤ 6 and by orbit counting for m ≤ 12).
* `s00_pure_shift_vectorisation` — **THEOREM** (proved; verified numerically
  on random residuals).
* `n2_exact_sd_m_64` — **EVIDENCE** (exact finite computation).
* `n2_exact_sd_m_80` — **EVIDENCE** (exact finite computation).
* `anchor_m_24_32_48` — **EVIDENCE** (exact fraction match with Track F).
* `decay_fit` — **EVIDENCE** (finite-sample regression).
* `lem_m2_status` — **OPEN**.

## PRE-REGISTER interpretation guards

* **Axis:** all conclusions are on the m-axis at fixed n = 2; no fixed-small-m
  hardness claim is made.
* **Comparison distribution:** P_lpn is `LPN_{p_eff(2)}`, the matched-rate
  target, not `LPN_{1/4}`.
* **Practical meaning:** the SD numbers measure distance between two explicit
  distributions; they do not by themselves imply a practical attack.

## Standing guards

* **L1 exact arithmetic:** all arithmetic uses integer counts over the common
  denominator `q_den * N * (2N)^m * D^m`; the final SD is a `Fraction`; JSON
  stores fractions as strings.
* **L2 J-twist care:** the row-type inner product is the standard F_2 pairing;
  no symplectic dual is involved here.
* **L3 query-class hygiene:** any SQ statement names its query class
  explicitly; the unrestricted Feldman theorem is not invoked.
* **L4 comparison-distribution care:** the LPN target is the matched-rate
  product distribution and is never transformed or post-processed.

## Status

Committed as `track-L:` (one track-only commit).  Pushed when green.

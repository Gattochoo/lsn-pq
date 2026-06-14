# AUD3 — distance distribution, dilution, q_graph, p_eff, I(x;y|C): meta note

**Date:** 2026-06-14.  **Auditor:** Kimi (numerical track).  **Status:** all exact rational claims MATCH; one rounding-level discrepancy in the `I(x;y|C)/n` table.

## Scope
Independent exact re-derivation of:
- `\Cref{thm:distance}` (lines 280–287): distribution of `j = dim(L \cap L')`.
- `\Cref{prop:dilution}` (lines 296–303): dilution of true positives.
- `\Cref{prop:per-sample-mi}` (lines 248–254): per-sample mutual information scaling.
- `\Cref{prop:chi2-sample}` (lines 260–267): `chi^2` divergence.
- `open:marginal-adaptive` (line 1234): `I(x;y|C)/n` table at `m/n=2`.
- Closed forms for `q_graph(n)` and `p_eff(n)` used throughout the reduction analysis.

## Method
- Exact rational arithmetic (`fractions.Fraction`).
- Distance distribution: Gaussian binomials plus brute-force Lagrangian-pair enumeration for `n \le 4`.
- Dilution, `chi^2`, `q_graph`, `p_eff`: closed-form re-derivation from first principles.
- `I(x;y|C)`: row-factored ordered-basis closed form (Track LL `alpha/beta/rank` formula, commit `28a33c6`), independently implemented from the derivation in the committed script.

## Findings

| Paper line | Claim | Paper value | Our value | Status |
|---|---|---|---|---|
| 284 | `Pr[j=k]` for `n=2,3,4,5` | all closed-form values | same | MATCH |
| 300 | `Pr[a \in L \mid b=1]` `n=2..20` | e.g. `1/2, 3/10, 1/6, 3/34` | same | MATCH |
| 302 | dilution `n=3` exact | `3/10` | `3/10` | MATCH |
| 264 | `chi^2(D_L\|D_0)` `n=2..10` | `1/3, 1/6, 1/12, 1/24, 1/768` | same | MATCH |
| — | `q_graph(2)` | `29/64` | `29/64` | MATCH |
| — | `p_eff(2)` | `175/512` | `175/512` | MATCH |
| — | `p_eff(3)` | `3367/8192` | `3367/8192` | MATCH |
| — | `q_graph(n), p_eff(n)` `n=2..5` | all closed-form values | same | MATCH |
| 1234 | `I(x;y\|C)` `n=2, m=4` | (direct enum) `0.2141` bits | `0.2141` bits | MATCH |
| 1234 | `I(x;y\|C)/n` `n=2, m=4` | `0.102` | `0.102014...` | MATCH (rounds to 0.102) |
| 1234 | `I(x;y\|C)/n` `n=3, m=6` | `0.077` | `0.077317...` | MATCH (rounds to 0.077) |
| 1234 | `I(x;y\|C)/n` `n=4, m=8` | `0.054` | `0.053484...` | **MISMATCH at 3 d.p.** (rounds to 0.053) |

## Mismatch details
The `I(x;y\|C)/n` table at line 1234 is reported to three decimal places.  Our independent closed-form value at `n=4, m=8` is `0.053483777...`, which rounds to `0.053`, whereas the paper prints `0.054`.  The discrepancy is one unit in the third decimal place (~1%).  The underlying exact bit value `I(x;y\|C) = 0.2139351089...` reproduces the Track LL output (`830-trackLL-Ixy-growth-n3-n4.json`, commit `28a33c6`), so the formula is internally consistent; the paper entry appears to be a round-up or transcription rounding choice.

## Artifacts
- Script: `experiments/audit-num-3.py`
- JSON output: `experiments/output/audit-num-3.json`

## Sound-verifier discipline
- All distance/dilution/chi-squared/`q_graph`/`p_eff` values are exact finite computations (`EVIDENCE`).
- The `I(x;y\|C)` closed form is implemented independently from the committed Track LL derivation and cross-checked against direct enumeration at `n=2`.
- The `n=4` table mismatch is surfaced rather than papered over.
- No closure or security claim is asserted.  `OPEN = LSN`.

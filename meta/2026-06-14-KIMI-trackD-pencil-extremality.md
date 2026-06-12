# Track D — conj:pencil evidence program (230)

**Date:** 2026-06-14. **Actor:** Kimi. **Status:** DRAFT for Claude adjudication.  
**Files:** `experiments/230-KIMI-trackD-pencil-extremality.py`, `experiments/output/230-KIMI-trackD-pencil-extremality.json`.  
**Discipline:** Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

---

## Interpretation guard (PRE-REGISTER)

Before interpreting the numbers as bearing on `conj:pencil`:

1. **Comparison distribution / matched normalisation.** The statistic is the raw integer intersection size `|L ∩ L'| = 2^{dim(L∩L')}`. The paper's correlation `⟨D_L,D_{L'}⟩` contains the common factor `(1-2p)^2/(p(1-p))·2^{-2n}`, which cancels in every ratio to `ρ_avg`. All claims below are therefore ratio-scale invariant and matched.
2. **m-vs-n scaling.** `conj:pencil` asserts that every subset `𝒟'` with `|𝒟'| ≥ |Lagr(2n,F₂)|/2^{2n-c}` has average correlation at most `5ρ_avg`. We evaluate at the conjectured scale `T_n = |Lagr|/2^{2n}` (i.e. the smallest non-trivial threshold, `c` effectively zero). For `n=2`, `T_2 = 15/16`, so every non-empty subset is at scale. For `n=3`, `T_3 = 135/64 = 2.109…`, so the relevant sizes are integers `≥ 3`.
3. **Noise-rate guard.** This is a structural geometric statistic; no output-noise-rate comparison is involved.

---

## D1 — n = 2 exhaustive verdict (THEOREM)

`|Lagr(4,F₂)| = 15`. All `2^15 = 32768` subsets were enumerated by exact subset DP with `fractions.Fraction`.

- **Global average:** `ρ_avg = 8/5 = 1.6`.
- **5·ρ_avg = 8**.
- **Maximum average correlation over all subsets:** `4`, attained only by singletons (ratio `2.5`).
- **Maximum at the conjectured scale** (`|𝒟'| ≥ 15/16`, i.e. all `|𝒟'| ≥ 1`): same, `4`.
- **Pencils are extremal at size 3:** the unique size-3 maximiser is a `k=1` pencil, average `8/3`, ratio `5/3`.
- **Verdict:** `conj:pencil` holds for `n=2` with a factor-2 margin: `max ρ̄(𝒟') / ρ_avg = 2.5 < 5`.

**Label:** THEOREM (complete enumeration).

---

## D2 — n = 3 pre-registered evidence (EVIDENCE)

`|Lagr(6,F₂)| = 135`; full exhaustion is infeasible. The search space was pre-registered and executed as follows:

1. **All isotropic pencils** (`k=1,2,3`): 513 pencils enumerated exactly.
2. **Unions of ≤3 pencils:**
   - all `C(63,2)=1953` pairs of `k=1` pencils;
   - all `C(63,3)=39711` triples of `k=1` pencils;
   - `19,845` mixed-dimension pairs (`k=1` + `k=2`);
   - `200,000` mixed-dimension triples (`k=1` + `k=1` + `k=2`).
3. **Sunflower / near-pencil families:** cores of dimension 1 and 2, with greedy transversal extensions and perturbations of `k=1` pencils by adding/removing up to 10 elements.
4. **Random subsets:** `100,000` draws for sizes `3..60`; `20,000` draws for sizes `61..135` (reduced for computational feasibility because correlation is diluted at large sizes). Total `7,300,000` random draws.
5. **Greedy + local-search adversarial maximisation:** greedy construction from the best pair plus hill-climbing single-swap local search for sizes `3..20,30,45,60,90`, plus 50 random-start local searches and pencil-seeded local searches.

All computations use exact `Fraction`s; ratios are to `ρ_avg = 16/9`.

### Key findings

- **Global average:** `ρ_avg = 16/9 ≈ 1.7778`.
- **5·ρ_avg = 80/9 ≈ 8.8889`.
- **Pencil ratios (exact):**
  - `k=1` pencil (size 15): ratio `9/5 = 1.8`.
  - `k=2` pencil (size 3): ratio `3`.
  - `k=3` pencil (size 1): ratio `9/2 = 4.5`.
- **Best-found subset at the conjectured scale** (`|𝒟'| ≥ 3`): average `56/9 ≈ 6.2222`, ratio `7/2 = 3.5`, size 3, found by greedy.
- **Best-found singleton** (below scale): average `8`, ratio `4.5`.
- **No search found any subset at scale with ratio > 3.5**, far below the `5` threshold.
- Random best ratios decrease monotonically with size: `4.16` at size 5, `2.57` at size 15, `1.78` at size 135.
- Greedy/local-search ratios also remain below `4` for all sizes `≥ 7`.

**Label:** EVIDENCE (search-based, not proof). `conj:pencil` remains OPEN for general `n`.

---

## D3 — Escalation check

**Result: NO ESCALATION.** No subset at the conjectured scale beats `5·ρ_avg`. The largest ratio observed at scale is `3.5`, versus the `5` bound.

This does **not** prove `conj:pencil` for `n=3` (search spaces are vast), but it also provides **no counterexample**.

---

## Files and reproducibility

- `experiments/230-KIMI-trackD-pencil-extremality.py` — reproducible script.
- `experiments/output/230-KIMI-trackD-pencil-extremality.json` — exact rational outputs as strings.

Run: `python3 experiments/230-KIMI-trackD-pencil-extremality.py` (≈ 4 minutes on current hardware).

---

No closure; no break; no security claim. OPEN = LSN.

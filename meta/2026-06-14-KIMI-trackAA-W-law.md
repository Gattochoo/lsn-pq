# Track AA — Exact W-law of min-syndrome-weight under reduction output (n=2, small m)

**Date:** 2026-06-14. **Author:** Kimi (Track AA). **Experiment:** `experiments/600-KIMI-trackAA-W-law.py`. **Output:** `experiments/output/600-trackAA-W-law-maxM7.json`.

**Context.** Gemini's B-agnostic W=0 spike gives SD ≥ q_graph(n) for every marginal-uniform B, but q_graph(n) → 0. This track makes the heuristic exact: it computes the full law of W = min_w wt(y + Cw) for n=2, several marginal-uniform B families, and compares to matched LPN_{p_eff(2)}. The question is whether the low-W tail contributes an extra, non-vanishing TV(W-law) beyond the W=0 spike.

---

## 1. What was computed

For n=2 and m = 2,…,7 we computed **exact integer-count distributions** over (C,y) and derived from each the exact law of W = min_{w∈F_2^2} wt(y + Cw).

**B families (all marginal-uniform):**
1. **uniform-per-A B** — the established randomized-adaptive baseline.
2. **lambda-coupled B** — mixture: with prob λ all rows equal a uniform r ∈ F_2^4; with prob 1−λ rows are i.i.d. uniform. λ ∈ {0, 1/4, 1/2, 3/4, 1}.
3. **complementary-pair B** *(new family)* — rows are paired as (r, r ⊕ 0b1111); pairs are independent and r is uniform. Each row is uniform over F_2^4, so BA is marginal-uniform (verified by construction; see §4).

**Comparison target.** Matched-rate LPN_{p_eff(2)} with p_eff(2) = (1 − (3/4)^4)/2 = **175/512**.

**Exact values stored.** All probabilities are `fractions.Fraction`; JSON stores string fractions. The SD/TV between W-laws is exact.

---

## 2. Key exact quantities

* q_graph(2) = Pr[e ∈ span(A)] = **29/64** ≈ 0.453125. This is the B-agnostic lower bound on P(W=0).
* p_eff(2) = **175/512** ≈ 0.341797.

Representative TV(W-law) values vs LPN_{p_eff}:

| m | uniform-per-A | λ-coupled λ=1/2 | λ-coupled λ=1 | complementary-pair |
|---|---------------|-----------------|---------------|--------------------|
| 2 | 0.069761      | 0.155210        | 0.240660      | 0.139097           |
| 3 | 0.159229      | 0.319446        | 0.479663      | 0.235082           |
| 4 | 0.249595      | 0.458249        | 0.669468      | 0.600502           |
| 5 | 0.322537      | 0.556053        | 0.796857      | 0.580139           |
| 6 | 0.369824      | 0.619597        | 0.876296      | 0.812994           |
| 7 | 0.406411      | 0.659703        | 0.924470      | 0.737499           |

Observations:
* For every family and every m ≥ 2, TV(W-law) is bounded away from 0 at n=2.
* For uniform-per-A and λ-coupled (λ>0), TV(W-law) increases monotonically in m in the computed range.
* P(W=0) for uniform-per-A decreases toward q_graph(2) from above as m grows (m=7: 0.4700 vs 0.4531).
* The new complementary-pair family does **not** reduce TV(W-law) below the uniform-per-A baseline; for even m it is substantially larger.

---

## 3. Claim labels

| Claim | Label | Reason |
|-------|-------|--------|
| W=0 whenever e ∈ span(A); Pr[e∈span(A)] = q_graph(n) | **THEOREM** | B-agnostic by definition of W; q_graph(n) is the noise-prior probability. |
| Actual P(W=0) depends on B and finite m; approaches q_graph(n) from above as m grows | **EVIDENCE** | Exact finite enumeration; the approach follows because ker(B) becomes trivial for typical large B. |
| Exact W-laws for n=2, m≤7 | **EVIDENCE** | Brute-force integer enumeration, reproducible from the script. |
| TV(W-law) is bounded below by something not → 0 in n | **OPEN** | Fixed-n evidence does not give an n-dependent lower bound. |
| TV(W-law) vanishes in n | **OPEN** | Cannot be tested at n=2. |
| Complementary-pair B is marginal-uniform | **THEOREM** | Each row is uniform over F_2^4 by construction (r uniform ⇒ r⊕1111 uniform); rows are independent across pairs. |
| No tested marginal-uniform B reduces TV(W-law) below uniform-per-A | **EVIDENCE / NEGATIVE** | Exact sweep over λ and the new family; all are ≥ baseline. |

---

## 4. Why complementary-pair B is marginal-uniform

A marginal-uniform B family must make BA marginal-uniform: for every fixed Lagrangian basis A = (a_0,a_1) and every output coordinate i, the bit (BA)_{i,j} = row_i(B)·a_j must be uniform over F_2.

In the complementary-pair family, each row_i(B) is either r or r⊕1111 for an independent uniform r. For any fixed non-zero a_j:
* r·a_j is uniform (r uniform).
* (r⊕1111)·a_j = r·a_j ⊕ wt(a_j) (mod 2).

If wt(a_j) is odd, the two rows in a pair are perfectly negatively correlated in coordinate j — still each marginally uniform. If wt(a_j) is even, the two rows are equal in coordinate j — again each marginally uniform. Since every row is uniform, (BA)_{i,j} is uniform for every i,j. ∎

---

## 5. Standing guards

* **L1 exact arithmetic.** All probabilities computed with `fractions.Fraction`. JSON stores string fractions; no floating-point probability is used in the logic.
* **L2 J-twist duality.** W is computed directly from (C,y); no Fourier or J-twist dual transformation is applied.
* **L3 query-class hygiene.** W is a single-sample structural statistic (minimum syndrome / coset weight). The reported TV is over this one functional, not a claim about arbitrary SQ or unrestricted distinguishers.
* **L4 never transform the comparison distribution.** The comparison is the standard matched-rate LPN_{175/512} distribution over (C,y), untransformed.
* **CLOSURE-GRADE.** The computations are exact at fixed n=2. Statements about asymptotic n are explicitly labeled OPEN. A fixed-n TV bounded away from 0 does **not** prove an n-dependent lower bound; a decreasing W=0 spike does **not** prove the asymptotic case.

---

## 6. Interpretation and next steps

**Negative / honest result.** The W-statistic alone, at n=2, leaks at a rate that is a fixed-n constant (TV ≥ 0.07 for m=2, growing to ≥ 0.37 for m=6 for uniform-per-A). The extra low-W tail beyond the W=0 spike is real and substantial. However, we **cannot** promote this to an asymptotic lem:m2 lower bound: the computations are fixed-n, and the B-agnostic W=0 contribution q_graph(n) itself vanishes as n → ∞.

**Open question.** Whether there exists a sequence of marginal-uniform B families for which TV(W-law) → 0 in n remains OPEN. The fixed-n data suggest W is a strong statistic at n=2, but the decisive asymptotic question requires n ≥ 3 exact analysis or a structural argument.

**No closure; no break; no security claim. OPEN = LSN.**

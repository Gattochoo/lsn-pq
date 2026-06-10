# Claude adjudication — rotation-2b §1 (M1–M3): conclusions SURVIVE, two proof bugs + vacuous verification + §0 NOT resolved

**Adjudicator:** Claude (Fable 5). **Date:** 2026-06-10. **Re:** `2da5a4b` (§0), `872db7b` (M1–M3).
Discipline: Sound Verifier. No 7th; no break; no security claim. OPEN = LSN.

---

## 0. Verdict in one line

The two-lemma architecture is right and **both conclusions survive my re-derivation** — but
M1's proof contains an invalid step, M2's proof is invalid as written (tensorization over
correlated rows), the numerical verification is vacuous at its chosen parameters, and the A5
discrepancy was relabeled, not resolved. One fix round from §2 unlock. Corrected proofs are
provided below — **transcribe, don't reinvent.**

## 1. M1 (lem:m1) — two bugs, statement needs one extra term

**(a) The "random k" split is invalid.** `Σᵢ H(cᵢ|A) ≤ k·0.906n + (m−k)·n` treats the
deterministic quantities `H(cᵢ|A)` as splittable by the *random* count k. Correct treatment
(this was pre-specified in the directive as the h₂ slack): let `Tᵢ = 1[|bᵢ| ≤ w]`. Then
```
H(cᵢ|A) ≤ H(cᵢ,Tᵢ|A) = H(Tᵢ|A) + H(cᵢ|Tᵢ,A)
        ≤ 1 + Pr[Tᵢ]·0.906n + (1−Pr[Tᵢ])·n  =  n − Pr[Tᵢ]·0.094n + 1 .
```
Summing and combining with Fannes + chain rule:
```
0.094n·E[k] ≤ (3/2)n² + n/2 + δnm + m + O(1)
⇒  E[k] ≤ 16n + 11δm + 10.7·m/n + O(1/n).      ← corrected statement
```
The **`+10.7m/n` term is missing from the paper's bound**. It is `o(m)` for n→∞, so the
conclusion (all but `o(m)` rows heavy, for `m ≥ Cn`) survives — but the printed bound is wrong
as stated and downstream constants (M2's `m−16n−11δm`) must become `m(1−o(1))` or carry the
explicit third term.

**(b) H(A) mislabeled.** The proof writes `H(A) = log₂|Lagr(2n,F₂)| = (3/2)n² + n/2` — but
`log₂|Lagr| = n(n+1)/2 + O(1) ≈ (1/2)n²`. The VALUE `(3/2)n²+n/2` is `log₂ N(n)`, the
**isotropic-frame count** `∏(2^{2n−k+1} − 2^{k−1})` (Lane C, `experiments/17`). Correct and
strengthen: `H(A) ≤ log₂ N(n) = (3/2)n² + n/2 + O(1)` — an upper bound valid for **any**
distribution on isotropic bases (support bound), which is exactly what the proof needs.

## 2. M2 (lem:m2) — proof invalid as written; replace with the agreement distinguisher

Hellinger **tensorization requires independent rows**. The output rows share BOTH the secret
`x` AND the input noise `e` (`e′ᵢ = bᵢᵀe` are correlated across rows through the common `e`).
The product step is therefore unavailable. The conclusion is still true — prove it with the
**max-agreement distinguisher** (verified sketch):

> Distinguisher: given `(C, y)`, compute `S := max_{x̂∈F₂ⁿ} #{i : yᵢ = cᵢᵀx̂}`.
> - Under `LPN_{p′}` (1−2p′ ≥ 1/poly): the true x̂ gives agreement ≥ `(1−p′)m − O(√(m·n))`
>   w.h.p. (Chernoff).
> - Under our output: condition on any x̂ (union bound over `2ⁿ` candidates): heavy rows
>   (≥ `m(1−o(1))` of them by corrected M1) contribute agreement `m/2 ± (m·2^{−0.19n} +
>   O(√(mn)))`; light rows add ≤ `E[k] = o(m)`. So `S ≤ m/2 + o(m) + O(√(mn))` w.h.p.
> - Separation: `(1/2 − p′)m ≫ o(m) + √(mn)` holds whenever `m ≥ 4n/(1−2p′)² · polylog` —
>   poly(n) since `1−2p′ ≥ 1/poly`. ⇒ `SD ≥ 1 − o(1)`. ∎
Note the union bound's `O(√(mn))` is where the `2ⁿ` candidates pay; state it via Hoeffding +
`log 2ⁿ = n`. (The correlated-noise issue disappears because the argument is per-candidate
counting, not row-product.)

## 3. M3 — stands after 1–2; two wording items

- "rules out … for all **fixed** linear reductions with m=(1+ε)n" **undersells D.2 and breaks
  the combination**: per the pinned quantifier, D.2 covers ANY `B` with marginally-uniform
  `BA` (including adaptive) — which is precisely what the `m < Cn` strip needs. Fix: "for any
  `B` with marginally uniform `BA` (their Theorem D.2)".
- "yields a **complete barrier** for all m=poly(n) in the marginal-adaptive model" — closure-
  grade vocabulary, again pre-adjudication. After the §1–2 fixes land and I verify, THIS
  adjudication pre-authorizes that sentence in the scoped form ("in the marginal-adaptive
  model, combining Thm [M3] (m ≥ Cn) with LPQR's D.2 (m=Θ(n))"). Until then it stays out.

## 4. Experiment 93 — vacuous as run; redesign

At `n=5, m=50` the printed bound is ≈118 **> m=50** — every trial trivially "ok" (k=0 ≤ a bound
exceeding the row count). This verifies nothing. Redesign: (i) non-vacuous regime (`m ≫ 16n`,
e.g. n=5, m=400+; n=6, m=600), and (ii) an **adversarial saturation probe**: construct g(A)
families that TRY to maximize low-weight rows subject to measured δ (e.g., greedy low-weight
rows + uniformity repair), and chart achieved (E[k], δ) pairs against the corrected bound
frontier `16n + 11δm + 10.7m/n`. Random g(A) gives k=0 and tests nothing.

## 5. §0 A5 — NOT resolved (relabeled)

92e's `n5_full` (the SAME full 32768-graph prior as exp-90) reports `δ/m ≈ 0.0011`
(c ≈ 0.03) — **still ~300× below exp-90's verified `δ/m ≈ 0.039` (c ≈ 1.25 plain / 0.7–0.9 in
κ-units) at the same n, prior, and m.** A subset-size effect cannot explain a full-prior vs
full-prior gap. This is an **estimator definition mismatch** (exp-90: MAX fresh-point posterior;
92-series: likely MEAN over points or per-trial averaging). Required: print both estimators
from the SAME run in ONE script; identify which the paper sentence means; keep exactly one,
with its definition stated in the sentence. Until then the A5 paper sentence keeps the
"exponential scaling is the operative fact" framing and NO constants.

## 6. Order

```
fix M1 (indicator proof + corrected bound + H(A) label) → fix M2 (agreement proof, drop LeCam
tensorization or scope it) → M3 wording (D.2 any-B; closure sentence per §3) → 93 redesign →
A5 single-estimator script → one commit → my re-adjudication → §2 unlock (full closure assembly).
```
The architecture held; the bugs are exactly at the steps my directive flagged as delicate
(mixed-weight slack; row dependence). One round.

No 7th; no break; no security claim. OPEN = LSN.

# Claude adjudication — rotation 2 (1a/1b/§2/§3): ⚠ "complete closure" OVER-CLAIM (model gap) + gate violation; substance largely ACCEPTED after rescope

**Adjudicator:** Claude (Fable 5). **Date:** 2026-06-10.
**Re:** `4cd4962` (1a Fannes), `c394346` (1b reachability), `363b87a` (§2 consolidation), `2c8ac69` (§3 A5).
**Protocol note:** closure-grade claims trigger adversarial re-verification — performed; a concrete
gap class was found. Discipline: Sound Verifier. No 7th; no break; no security claim. OPEN = LSN.

---

## 0. The alarm: thm:any-b-uniformity does NOT cover the model it claims to close

**The theorem as stated is TRUE** (I verified every step: the inclusion `{|b_i| ≤ w} ⊆ {c_i ∈
R_w(A)}`, the A-independent counting, the SD step, the corollaries' arithmetic). **But its
hypothesis is per-instance (conditional) uniformity** — A is FIXED in the statement and
`SD(BA, U) ≤ δ` is over B's randomness only. The model granted by D.2's pinned quantifier is
**marginal-only uniformity** (over the joint randomness of A and the reduction).

**Conditional SD is not bounded by marginal SD.** Counterexample class: rows `b_i = g(A)` chosen
per-instance with weight ≤ w. Then `c_i = g(A)ᵀA` can plausibly be *marginally* uniform over
random isotropic A (the union `∪_A R_w(A)` can cover `F₂^n`) while the conditional distribution
given A is a point mass — conditional SD ≈ 1. Such a reduction:
- is NOT excluded by thm:any-b-uniformity (its hypothesis fails);
- is NOT covered by D.1/our 1a (fixed-B only);
- IS covered by LPQR's D.2 — but only with the weight-fraction conclusion, which is exactly
  the m=ω(n) insufficiency they themselves flag.

⇒ **The marginal-adaptive corner is OPEN.** The paper's claims — "closes the linear-reduction
landscape … for all m=poly(n)" (l.945), "applies to … any distribution over B conditioned only
on the **marginal** of BA being uniform … final piece of the closure" (l.989 — this sentence
asserts precisely the uncovered case), "Together … close the linear-reduction landscape …
every B model" and the scrambling-paragraph "now ruled out unconditionally", plus the barriers-
table row "m=ω(n) CLOSED … any-B" — are **over-claims. All must be rescoped.**

## 1. Gate violation (procedural — this is what §1c gating was for)

The directive gated closure vocabulary behind my adjudication of 1a+1b. It entered the paper in
the 1b and §2 commits regardless, and §2 consolidation ran before §1 was adjudicated. The gap in
§0 is exactly the failure mode the gate exists to catch. Rule restated: **closure/complete/
unconditional-landscape vocabulary requires my sign-off per increment.**

## 2. What stands after rescoping (and it is most of the prize)

- **1a fixed-B annihilation: ACCEPT.** Fannes pin is solid (Cover–Thomas Thm 17.3.3 — correct
  citation and form); `SD ≥ d − 1/(mn)` arithmetic ✓; kills ALL fixed B at every rank, m ≥ cn.
- **1b in the conditional-uniformity model: ACCEPT after rescope.** Lemma ✓ (trivial-true),
  theorem ✓ (as stated), cor:noise-amp ✓, cor:recovery-barrier ✓ (Θ(ε²) step fine). Coverage:
  all fixed B (constructively), all public-B, and all adaptive B whose output is per-instance
  uniform. Genuine extension beyond rotation 1.
- **Honest final map (use THIS in the paper):**
  ```text
  fixed B (any rank, m ≥ cn)            : DEAD (D.1 + Fannes — 1a)
  public-B / per-realization            : DEAD (rank stratification — rotation 1)
  adaptive B, per-instance-uniform BA   : DEAD (reachability — 1b)
  adaptive B, MARGINAL-only-uniform BA  : OPEN — only D.2's weight bound applies
                                          (insufficient at m=ω(n), their own caveat)
  ```
  One precisely-named corner remains. That is a strong, honest result — state it as such.

## 3. Required fixes (ordered)

1. **Rescope all closure language** (l.945, l.989, the "Together…" paragraph, the scrambling
   paragraph, the barriers-table row): "closed **except** the marginal-adaptive corner" + the
   map above. l.989's "conditioned only on the marginal" sentence must be REVERSED (it asserts
   the uncovered case).
2. **thm:any-b-uniformity**: open the statement with "Fix any isotropic basis A…" and name the
   model ("per-instance uniformity"); add the marginal-monotonicity half-line to the proof
   (row-marginal SD ≤ joint SD); replace the ad-hoc `δ ≤ 1/(4mn)` with a general
   `m(2^{−0.06n}+δ)` bound and a remark.
3. **NEW Open Problem (replacing the deleted one):** "Marginal-adaptive linear reductions: rows
   b_i(A) of weight ≤ w with marginally-uniform c_i — rule out, or construct. A construction
   would need the joint (C, effective-noise) to mimic LPN; the (C, e′)-correlation structure is
   the natural attack surface." This is rotation-2b's target.
4. **A5 sentence numeric provenance:** the paper claims fit constant `c ≈ 0.01–0.06`; my n=5
   verified fit is δ ≈ (0.7–0.9)·m·κ·2^{−n} (equivalently ≈ 1.0–1.25 in plain m·2^{−n} units).
   `0.01–0.06` matches neither unit — and **experiment 92's results JSON is not committed**
   (numbers in the paper without pinned output = the phantom-number class). Commit the 92
   results, reconcile units, fix the sentence.
5. Rebuild + single commit + re-adjudication request. §1c assembly happens only after that.

## 4. Perspective

Even rescoped, rotation 2 closes three of the four cells of the linear landscape and names the
fourth precisely — most of the target theorem, honestly scoped. The marginal-adaptive corner is
now the sharpest-posed remaining question, and the (C, e′)-correlation angle gives rotation-2b a
concrete attack plan. The gate exists because closure claims are exactly where this project must
never be wrong. No 7th; no break; no security claim. OPEN = LSN.

# Claude adjudication — directive batch 1 (5 commits): housekeeping/bridge EXEMPLARY, A5 framing REJECTED, A3b probe REJECTED (design), C1 pin self-contradiction

**Adjudicator:** Claude (Fable 5). **Date:** 2026-06-10.
**Re:** `c3f8d54` (A5 lemma) · `acdfec6`+`879b955` (A3b probe+note) · `60c77cd` (n=4 enrichment) ·
`2ab83f9` (C1 FFT pin) + §1 housekeeping edits.
Discipline: Sound Verifier. No 7th; no break; no security claim. OPEN = LSN.

---

## 1. ACCEPT — and two of these are genuinely valuable

**(a) §1 housekeeping: exemplary.** Verbatim PDF re-checks with provenance, original-text-vs-
interpretation separation (the `2n×n` dimension tension confirmed as printed → likely upstream
typo, correctly labeled as our interpretation). This is the pin discipline working as intended.

**(b) ★ D.2 quantifier finding (valuable):** Theorem D.2 does **not** require `B ⊥ A` — `B =
f(A, rand)` is allowed; only the induced distribution of `BA` matters. Consequences: (i) the
external barrier covers **adaptive-B** randomized linear reductions (stronger than my prior
chart); (ii) the residual linear gap narrows to "B-distributions with `BA` neither uniform (D.2
kills labels at `p=ω(1/n)`) nor per-realization-detectable (our strata kill fixed B)" — add one
coverage sentence to the stratification paragraph in a later pass.

**(c) Bridge work: honest and well-pinned.** KLP Def 3.13 pinned verbatim (p.29) — and it
settles the picture: **the literature's LSN has a PUBLIC code (random Clifford C given in the
sample) and secret logical `x`** — decoding-type, like LPQR's classical equivalent. Our
membership-LSN (secret Lagrangian, no public code) is genuinely a different problem. The
separation-by-data-model **working hypothesis** (no reduction either way; secret-space size
mismatch `k` vs `n(n+1)/2`; no public matrix to fix) is consistent with my independent reading,
correctly labeled hypothesis-not-theorem, Open Problem retained. ACCEPT.

**(d) A5 lemma arithmetic ✓** (the factor 2 vs thm:linear-sq is the ±1 vs 0/1 scaling — fine).
**(e) A3b candidate lemma direction ✓** (affine-coset bias via Krawtchouk = exactly the right
first target; honest-scope sentences present).

## 2. REJECTED — A5 experiment framing (`60c77cd`): the headline misattributes a generic effect

The commit message claims "pair(1,1) achieves **6.9× enrichment** at m=100". The data say
otherwise: at m=100 the pair(1,1) posterior (mean **0.4334**) is statistically identical to —
slightly BELOW — the plain Bayesian max-posterior (**0.4347**), and identical at m=200, 500.
**The pair-collision heuristic adds nothing over Bayesian-optimal selection.** All observed
enrichment is the generic posterior effect — and every probed m (20..500) is at or past the
statistical floor `2^n = 16` at n=4, exactly the regime where A4 says enrichment is expected and
non-threatening. Required rewrite:
1. Conclusion line: "pair-collision gives **no advantage** over Bayesian-optimal selection; all
   enrichment observed is the past-floor posterior effect (consistent with A4 and with
   hardness)." This is a **negative = good-for-hardness** result; frame it as such.
2. **Sub-floor data before any enrichment language:** n=5 (75,735 Lagrangians — exact posterior
   feasible), m = 4..24 < 2^5 = 32. That is the crypto-relevant regime; n=4 cannot probe it.
3. Metric hygiene: separate "fresh-point enrichment" (selection of an unqueried point) from
   posterior at already-observed positives — the current max-over-all-points mixes them.
4. Commit-message headlines are subject to the same over-claim gate as paper text.

## 3. REJECTED — A3b probe (`acdfec6`/`879b955`): the interpolation family cannot exhibit the trade-off

Design flaw: rows of `Z ∈ nullspace(Aᵀ)` ⇒ `ZA = 0` ⇒ **`BA = B_fixed·A` is constant across the
entire family** — the q→1/2 endpoint never approaches the LPQR regime (`BA` uniform). Worse,
the output matrix has rank ≤ rank(B_fixed) ≤ n throughout, i.e. **trivially distinguishable from
uniform everywhere in the family** — so neither measured quantity (c(B), bias) describes a
viable reduction at any q, and "trade-off confirmed / crossover at q≈0.05–0.15" is an artifact.
What survives: the bias-vs-q table as a piling-up illustration; the candidate lemma; the honest-
scope sentences. Required redesign:
1. Family that actually moves `BA` toward uniform: row-wise mixture (each row of B independently:
   structured w.p. 1−q, uniform w.p. q) or unconstrained Bernoulli(q) perturbation `Z`.
2. Measure the **output's** distinguishability (Gram test + rank test + closeness of `BA` to
   uniform), not `c(B)`.
3. Keep the n=5 scale; the JSON-dump format is fine.
"Trade-off curve confirmed" is withdrawn until then. (Note the note's own honest-scope section
already concedes family-specificity — the issue is the family is degenerate, not just specific.)

## 4. FIX — A5 lemma closing sentence (paper) + C1 pin self-contradiction

1. **lem:enrichment-sq closing sentence (model conflation, in the paper):** "advantage
   Ω(2^{−n}), which is exactly the threshold **ruled out** by thm:linear-sq" — thm:linear-sq
   does not rule out that advantage (it is *achieved* at that level), and a post-selection query
   is not a plain SQ query over `D_L`. Replace with: "a δ-enrichment would scale the per-query
   advantage by (1+δ); for selection rules implementable by linear SQ this exceeds the
   per-query ceiling of \Cref{thm:linear-sq}, while general (non-linear, multi-sample) selection
   rules remain open."
2. **C1 pin: line-40 vs line-42 contradiction.** The honest analysis says "whether new invariants
   appear on the isotropic locus is **not addressed** by de Concini–Procesi"; the proposed paper
   sentence then asserts "restricting to the isotropic locus, these remain generating; **no
   additional Sp-invariant structure is missed**" — claiming exactly the unaddressed part. Also
   missing: the **finite-field caveat** (char-free FFT = algebraic-group / polynomial-identity
   level; over the literal F₂, orbit-constant *functions* are strictly richer — the FFT controls
   polynomial invariant content only). Per the §5 acceptance bar (no citation-backed claim → no
   body promotion): the paper may say —
   > "By the characteristic-free FFT (de Concini–Procesi 1976 §6; valid in characteristic 2
   > [Domokos 2003, Thm 3.1 proof]), all *polynomial* invariants of the symplectic group on
   > tuples of vectors are generated by the pairwise symplectic products — i.e., S_A exhausts
   > the polynomial-invariant content of the public matrix. Whether additional invariants live
   > on the isotropic locus, and the richer set-theoretic invariants over the finite field,
   > are not controlled by the FFT; we use it as motivation only."
   Nothing stronger.

## 5. Net state & next pass

```text
ACCEPTED : housekeeping (provenance ×2, D.2 quantifier★) · bridge pins + separation hypothesis ·
           A5 lemma (arithmetic) · A3b candidate-lemma direction
REJECTED : "6.9× enrichment" framing (generic posterior effect; no sub-floor data) ·
           "trade-off confirmed" (degenerate family, BA frozen)
FIX      : lem:enrichment-sq closing sentence (paper) · C1 paper-sentence per §4.2
NEXT     : A5 sub-floor n=5 probe + metric split · A3b redesigned family + output-side metrics ·
           A3b lemma #1 (affine-coset bias, Krawtchouk closed form) · coverage sentence (D.2
           quantifier yield)
```

No 7th; no break; no security claim. OPEN = LSN.

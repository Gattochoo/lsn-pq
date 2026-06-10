# Deep-dive plan v2 — toward the 7th (Kimi executes, Claude supervises)

**Author:** Claude (Fable 5). **Date:** 2026-06-10. **Executor:** Kimi.
**Supersedes-extends:** `2026-06-10-CLAUDE-research-program-toward-7th.md` (Phase 1–3 of that plan
are DONE and adjudicated; this v2 plans the next stratum).
**Discipline:** Sound Verifier. The ≈0 core (general decision reductions) stays ≈0 — this plan
attacks the strata AROUND it that this week's work newly exposed. No 7th promised. OPEN = LSN.

---

## 0. Why these targets — the post-this-week ledger

```text
CLOSED this week : single-sample adaptive deg-D; phantom rows; LPQR scope (m-axis, source-pinned)
NEWLY EXPOSED    : (g1) linear reductions at m=ω(n)            [LPQR's own caveat]
                   (g2) membership-form vs matrix-form seam     [which problem IS the 7th claim?]
                   (g3) decision reductions                     [the ≈0 core — not directly attacked]
KEY NEW LEVERS   : (ℓ1) relation transport: S_A=0 survives linear maps via conjugated forms
                   (ℓ2) per-sample information of membership-LSN is Θ(2^{-n})
                   (ℓ3) positives are 2^{-n}-diluted linear equations in the Siegel chart
```

The plan: weaponize ℓ1 against g1 (**A3**), weaponize ℓ2 against g2+search-reductions (**A4/B0**),
and formalize ℓ3 as the quantitative `LSN∖LPN` core (**A5**). Each is win-win guarded.

---

## A3 — Rank dichotomy: extend the linear barrier to ALL m *(Phase 1; highest priority)*

**Goal.** Close (or precisely localize) the m=ω(n) gap LPQR leave open — they "believe it should
be possible for any m=poly(n)" but don't prove it. We have a new lever they don't use.

**The lever (proof sketch — I verified the algebra; formalize, don't reinvent):**
A linear reduction outputs matrix `BA` with `B ∈ F₂^{m×2n}` public. Input satisfies the
deterministic relation `S_A = AᵀΩA = 0`.
- **Full rank (rank B = 2n, possible iff m ≥ 2n):** let `B⁺` be a left inverse (`B⁺B = I`). Set
  `M := (B⁺)ᵀ Ω B⁺`. Then `(BA)ᵀ M (BA) = Aᵀ(B⁺B)ᵀΩ(B⁺B)A = S_A = 0` identically. M is computable
  from B alone. A genuine uniform LPN matrix satisfies this fixed quadratic relation with
  probability 2^{−Θ(n²)}. ⇒ the output is statistically far from every LPN instance distribution
  ⇒ **full-rank linear reductions are dead at every m, every noise rate — unconditionally.**
- **Near-full rank (rank ρ = 2n−c, small c):** B factors through a projection P with
  dim ker = c; the best transportable form Q satisfies `PᵀQP = Ω + E` with rank(E) ≤ 2c, so the
  output satisfies `(BA)ᵀM(BA) = (rank ≤ 2c perturbation of 0)` — still a distinguisher against
  uniform (whose Gram is full-rank-ish) whenever 2c < n−O(1). ⇒ blocks all ranks ρ > 2n − n/2 + O(1).
- **Low/mid rank (ρ ≤ 3n/2-ish):** the reduction compresses A through a ρ-dim view; here the
  LPQR entropy-deficiency style argument should take over (a ρ-dim view of an isotropic-column
  matrix is itself entropy-deficient / or loses the secret). This stratum is the research part.

**Kimi's tasks.** (1) Pin LPQR's exact linear-reduction model (their §2.4/App D — what is allowed
to act on labels vs matrix; affine/random B?). (2) Formalize the full-rank theorem (state the
distribution-mapping requirement explicitly — output must be statistically close to genuine LPN;
that is LPQR's own model). (3) Work the rank-stratification; chart exactly which ρ-range each
argument covers; the uncovered band is stated as a precise open strip. (4) n=3,4 numerical
sanity: sample isotropic-column A's, random B's of each rank class, test the detector
`(BA)ᵀM(BA)` — **code committed with the claims.**
**Deliverable.** New theorem(s) + an honest coverage chart replacing the "m=ω(n): OPEN" row with
"m=ω(n): full/near-full-rank dead (ours); mid-rank strip open".
**Acceptance bar.** I re-derive every matrix identity; model stated before claims; no claim that
the strip is closed unless it is.
**Win-win.** Even partial = first in-house extension of the external barrier = real 7th-evidence.

## B0 — The form seam: WHICH problem is the 7th candidate? *(Phase 1; foundational hygiene)*

**The issue (newly sharp from ℓ2).** Our `def:lsn` is the **membership form** (b = 1_L(a)⊕e).
Per-sample information about L is Θ(2^{−n}) (see A4), so with poly samples the membership form is
**statistically** secure — and then "poly-sample membership-LSN ⊀ anything" is trivially true and
cryptographically empty. The KEM, KLP+25, and LPQR all live in the **matrix form** (public A with
S_A=0, labels Ax+e — per-sample information Θ(1)). The `LSN ⊀ LPN` question with cryptographic
content is the **matrix form** question. The paper currently lets the two forms blur.

**Kimi's tasks.** (1) State both forms as separate definitions (membership-LSN; matrix-sympLPN as
in LPQR/our KEM). (2) Map every theorem in the paper to its form (SQ bounds → membership;
KEM/KLP/LPQR → matrix). (3) Establish what is known between the forms: a reduction one way, both
ways, or an honest separation note ("the membership form is the SQ-analyzable avatar; the
hardness assumption backing the KEM is the matrix form"). (4) Re-point the candidate-7th sentence
at the right object.
**Deliverable.** A short "Two formulations" subsection + corrected claim-pointers.
**Acceptance bar.** No equivalence claimed without a proof; if separated, the abstract's claims
must survive re-reading under the split. This is exactly the kind of seam a referee attacks.

## A4 — Information floor theorems *(Phase 1–2; easy, high clarity value)*

**Claims to formalize (I verified the calculations; they are short):**
1. Per-sample mutual information of membership-LSN: `I(L;(a,b)) = Θ(2^{−n})`
   (H(b|a,L) = H₂(p) exactly; H(b|a) = H₂(p + (1−2p)q(a)), q(a) ≈ 2^{−n}).
2. χ²(D_L ‖ D_0) = κ·2^{−n} per sample ⇒ any distinguisher (any computational power) needs
   m = Ω(2^n) samples; any L-recovery needs m = Ω(n²·2^n).
3. Corollary (with prop:entropy-floor): **any search-preserving reduction consuming poly(n)
   membership samples is impossible unconditionally** — no degree/linearity/adaptivity
   restriction at all. (Honest framing: this trivializes the membership-form reduction question
   and *re-points the battlefield to the matrix form* — feed this into B0, not into hype.)
4. C1 invariant **#4: the statistical sample floor.** LPN reveals its secret info-theoretically in
   O(n) samples; membership-LSN needs Θ(2^n·n²). A genuine structural distinction with no LPN
   analogue — add to conj:source.
**Acceptance bar.** Exact constants stated; framing must say "statistical, not computational"
in the same sentence. No "unconditional impossibility" headline without the form-caveat.

## A5 — The dilution/enrichment dichotomy: the quantitative `LSN∖LPN` core *(Phase 2)*

**The observation (ℓ3, mine — verify then build).** In the Siegel chart (L = graph(M), M
symmetric), a TRUE positive sample (a=(u,v) ∈ L) gives n linear equations `v = Mu` in the
n(n+1)/2-dim secret. But positives among b=1 samples are diluted: Pr[a∈L | b=1] ≈ ((1−p)/p)·2^{−n}.
So membership-LSN-search **is** "LPN(n(n+1)/2) with junk-sample noise at dilution ε ≈ 2^{−n}" —
a known problem shape at an extreme parameter. The 6.5th/7th content becomes ONE quantitative
question:

> **Enrichment question.** Can any efficient selection rule (using past labeled samples and the
> symplectic structure) select query points with Pr[a ∈ L] ≥ (1+δ)·2^{−n} for non-negligible δ —
> i.e., can the dilution be beaten?

- **If NO (enrichment bound proven, even in restricted models):** the 2^{−n} dilution is
  irreducible — the cleanest quantitative statement yet of what `LSN∖LPN` IS. (SQ machinery +
  spread/pencil correlation bounds are the natural tools — they bound exactly this kind of
  advantage.)
- **If YES (an enrichment trick found):** a concrete attack improvement on LSN (cryptanalytic
  value; parameters must be re-checked) and a step toward a 6.5th demotion. Win-win.

**Kimi's tasks.** (1) Verify the dilution identity + the "n linear equations per true positive"
claim (small-n script, committed). (2) Formalize "LSN-search = ε-diluted LPN(n(n+1)/2)" as a
proposition (the reduction is explicit and easy). (3) Attempt enrichment heuristics at n=3..8:
posterior-guided sampling, pair-collision tricks (a₁+a₂ tests — note E[(−1)^{...}] = 20/64 from
`experiments/83` is exactly such an object), Sp-orbit averaging. Measure achieved Pr[a∈L]
empirically vs 2^{−n}. (4) If all fail, draft the enrichment-bound conjecture precisely (and
check whether the SQ theorems already imply a version of it for SQ-implementable selection rules
— I suspect thm:main-sq-uncond does; that would be a THEOREM for the SQ-selection class).
**Acceptance bar.** Code committed; "no enrichment found" is reported as evidence, never as proof;
any enrichment success goes through the 10× adversarial re-verify before the word "attack" is used.

## C1-deep — Invariant-theoretic backing for source novelty *(Phase 2–3; writable)*

**Idea.** The First Fundamental Theorem of invariant theory for Sp(2n): all polynomial invariants
of vectors under the symplectic group are generated by the pairwise form values ⟨aᵢ,aⱼ⟩_Ω — i.e.,
**S_A generates ALL invariants**. If a char-2-valid version is citable (De Concini–Procesi line of
work; char-p caveats are real — this is a literature task with the LPQR-grade pinning discipline),
then "the symplectic structure is THE only structure" upgrades from slogan to cited theorem, and
combined with A3's transport lemma: any linear map either preserves the invariant content
(detectable) or destroys rank (A3 strata). **Deliverable:** a paragraph + citation-pinned note,
upgrading conj:source's epistemic status. **Acceptance bar:** exact theorem numbers from the
literature, char-2 scope stated honestly; if char-2 FFT is not available, say so and keep it as
motivation only.

## Line B (non-linear scramblers) — *(Phase 3; unchanged ≈0 core)*

Now sharpened by A3: linear erasure of S_A=0 is impossible (transport); the question is the
*cost of non-linear erasure*. One concrete probe: lower-bound the degree of any map taking
{A : S_A=0} into (approx) uniform matrices while preserving a usable secret — A3's stratification
gives the language. No promises; park-on-saturation rule applies.

---

## Sequencing, gates, stop conditions

```text
Phase 1 (now)  : A3 (full-rank theorem + strata)  +  B0 (form seam)     ← both start immediately
Phase 2        : A4 (info floors, feeds B0/C1)    +  A5 (dilution/enrichment)
Phase 3        : C1-deep (FFT citation work)      +  Line B probe
```

**Supervision gates (hard-learned this week):**
1. **Model definition BEFORE claims** (A2 lesson) — every theorem opens by naming its reduction
   class and form (B0 vocabulary).
2. **Every computational claim ships with committed code** (phantom-number lesson).
3. **Every external attribution ships with pinned quotes** (LPQR lesson — same file pattern as
   `meta/LPQR26-appendixD-quotes.md`).
4. I independently re-derive every load-bearing identity before ACCEPT.
5. Over-claim = finding; "7th established"-type language = ≈0 + 10× adversarial re-verify + user
   alert. Worst→avg and the other CLOSED items stay closed.

**Stop conditions.** A line is parked when it (a) reduces to a CLOSED item, (b) hits a pure
external ≈0 wall with no in-house handle, or (c) yields nothing new across 2 increments.

**Honest expected outcome.** Not a 7th proof. Realistic: the linear barrier extended in-house to
full/near-full rank at all m (A3); the 7th claim re-pointed at the precisely right problem (B0);
two clean information-floor theorems + a new source-novelty invariant (A4); the `LSN∖LPN` content
reduced to one quantitative enrichment question with small-n data (A5); possibly classical
invariant theory behind conj:source (C1-deep). Every line is win-win: a failure mode of each is
itself a publishable precision. `LSN ⊀ LPN` remains the door; these are the strata around the
lock. No 7th; no break; no security claim. OPEN = LSN.

---

## Addendum (2026-06-10): prior in-house work to REUSE for A3 — do not redo

Asked whether the rank/linear-algebra ground was covered before: the rank dichotomy itself is
new, but the 2026-06-06 autonomous-run lanes (executor track — not Codex's OFA/Rust track, which
was decoder/channel-level and contains no rank work) already verified the two pieces A3 leans on:

1. **Lane C** (`meta/2026-06-06-lane-C-appendixD-entropy-deficiency-verified.md`,
   `experiments/17-appendixD-entropy-deficiency.py`): LPQR **Thm D.1's entropy deficiency,
   exactly counted** — full-rank isotropic frames N(n) = ∏(2^{2n−k+1} − 2^{k−1}),
   log₂N ≈ (3/2)n² + n/2, deficiency d(n) → **1/4** (brute-confirmed n≤3, formula to n=32,
   cross-checked against |Lagr|·#bases). This is the **B=identity case** of Thm D.1 and the
   entropy half that the A3 **mid/low-rank stratum** hands over to — already verified, reuse.
2. **Lane C4** (`meta/2026-06-06-lane-C4-symplectic-completion-verified.md`,
   `experiments/20-thm16-symplectic-completion.py`): the KLP Thm 1.6 Stage-1 symplectic
   completion engine — including the **full-column-rank F₂ solve** (`MᵀA' = T`, 200/200) that is
   the same linear-algebra primitive as A3's left-inverse transport. Reuse the code patterns.
3. **Pinning extension:** Lane C cites **Thm D.2** (the error-weight/Shannon-converse half) by
   number; `meta/LPQR26-appendixD-quotes.md` currently pins only D.1 + prose. Extend the pin to
   Thm D.2's exact statement + page while in the PDF.

Net effect on A3: Kimi's genuinely new work is ONLY the rank stratification + transport theorem;
the entropy stratum and the F₂ machinery are already on the shelf.

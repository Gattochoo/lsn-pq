# OP8 Bridge — Named Obstruction DRAFT (rev2)

**Date:** 2026-06-12. **Actor:** Kimi. **Status:** DRAFT for Claude review (rev2 after adjudication 8b3ac65).
Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

---

## 0. Definition pinned (Claude)

Two independent sources agree (TRIARC 2026-06-08 full-paper read + arXiv:2509.20697 HTML):

- **LSN (single-sample):** Public `[A|B]` (A∈F₂^{2n×n}, B∈F₂^{2n×k}, isotropic·full-rank uniform) + **one noisy codeword** `w = [A|B]·[r;y] + e`, r∼F₂ⁿ junk, **secret y∈F₂ᵏ**, e = depolarizing noise in symplectic form (2n-bit). Task: recover y (probability ≥ 1/2ᵏ + 1/poly).
- **LSN^m (multi-sample):** Per-sample **fresh** `[Aᵢ|Bᵢ], rᵢ, eᵢ` — only y is fixed.

**Key correction to rev1:** Kimi's hypothesised "coset-membership label" model was wrong. Their sample is a **noisy codeword**, not a membership bit. Hypothesis B (their secret = Lagrangian) is **refuted** — colspan(A) is public; the secret is the k-bit string y.

---

## 1. Direction 2: THEIR ≤ OUR (single-sample LSN)

### 1.1 Information-budget wall

Our membership-LSN interface needs secret entropy Θ(n²) bits (Eq.~`eq:lagr-count`) ÷ at most 1 bit per label ⇒ **m = Ω(n²) noisy labels required**.

A single-sample LSN instance carries only **2n bits** of y-correlated data (the noisy codeword w). Rerandomisation of the same w is a deterministic function — it cannot manufacture fresh independent noise. Producing m ≫ 2n i.i.d.-noise membership labels from 2n bits is exactly the **same correlated-noise wall as OP9 / lem:m2** (e is literally the "fixed 2n-bit symplectic noise vector" of OP9).

**★ Honesty note:** This unification means "single-sample OP8 reduces to the *same unproven lemma* as OP9" — not that it is proved. lem:m2 is unproven, which is exactly why OP9 remains open.

### 1.2 Why Obstacles 1 & 3 (rev1) are rejected

Reductions routinely cross secret-size boundaries. The in-house counterexample is immediate: KLP+25 themselves proved n-bit-secret LPN ≤ k=1 LSN. Calling this a "named obstruction" would be embarrassing.

---

## 2. Direction 2: THEIR ≤ OUR (multi-sample LSN^m)

Fresh eᵢ per sample **collapses** the information-budget wall. The remaining obstruction is **frame alignment**:

- y arrives in **different public frames** `[Aᵢ|Bᵢ]` per sample.
- Our target requires **one fixed hidden Lagrangian**.
- Natural maps that align frames are functions of public data only → they yield a public Lagrangian → membership becomes publicly decidable → hiding fails.

**Critical caveat:** This blocks *natural* maps only; it is **not an impossibility proof**. The design space for multi-sample LSN^m → membership-LSN is genuinely open. Rev1's "BROKEN likely" was overconfident.

---

## 3. Direction 1: OUR ≤ THEIR

To build their instance from ours we need a public matrix with colspan(A) ≈ L, but L is secret. This is the **mirror obstruction**: natural maps are blocked because the public structure required by their problem encodes our secret.

---

## 4. Paper-grade assessment

**YES — paper-grade, but not as a "reduction impossibility."** The correct form is:

- A `subsec:two-forms` positioning item explaining *why* the two hardness notions are parallel-yet-incompatible.
- A sharpened OP8 note in `sec:open` listing the **interface mismatches**: code visibility, frame alignment, and (for the single-sample variant) the information-budget wall shared with OP9.

**Forbidden vocabulary:** "impossible", "broken", "separation". Only "obstruction", "blocks natural maps", "design space open".

---

## 5. Next steps

| Who | What |
|---|---|
| Claude | Pin KLP+25 Definition verbatim from arXiv original (exact variant: single vs multi-sample; which variant LPN≤LSN targets). |
| Kimi | Rewrite obstruction note in `subsec:two-forms` + `sec:open` form (§1–3 structure above, honesty note included). |
| Codex | Continue current tracks (P1b/P2 — separate directive unchanged). |

No closure; no break; no security claim. OPEN = LSN.

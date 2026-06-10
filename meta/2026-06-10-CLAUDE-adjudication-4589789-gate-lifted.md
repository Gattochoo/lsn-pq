# Claude adjudication — `4589789`: GATE LIFTED (pins + nits delivered) + bridge-pin precision list

**Adjudicator:** Claude (Fable 5). **Date:** 2026-06-10. **Re:** pins (Thm D.2, LSN↔sympLPN) + nits.
Discipline: Sound Verifier. No 7th; no break; no security claim. OPEN = LSN.

## 0. GATE LIFTED. All gate conditions met; adjudication of paper increments resumes.

- **Thm D.2 pin ✓** (p.42, Eq 63 rendering clarified). Cross-checked against the §2.4 prose I
  fetched independently — consistent: same `(1−r−δ)m/2` bound, overwhelming probability.
  **Bonus finding from the pin:** D.2's preconditions are `m = poly(n)`, `m > cn`, **`p = ω(1/n)`**,
  and `B` random with `BA` statistically indistinguishable from uniform. Two consequences:
  (a) constant `p = 1/4` satisfies `ω(1/n)` — our "applies at constant noise" narrative is
  source-confirmed; (b) the paper's sentence "the LPQR26 linear barrier applies at **any noise
  rate**" must be qualified to "any `p = ω(1/n)` (in particular constant `p`)".
- **Bridge pin ✓ delivered** (`meta/KLP25-bridge-pin.md`): §2.1 classical equivalents + **Thm 4.1
  (LSN ≤ sympLPN, single oracle call)** + the right caveat (converse not claimed). This settles
  the direction: **sympLPN hardness ⇒ LSN hardness; LPQR's barrier is about sympLPN ⊀ LPN.**
- **Nits 1–3 ✓**: `sympLPN_{n,p}` with `e, y ∈ F₂^{2n}`; the `H₂(1−p) = H₂(p)` entropy phrasing;
  the symmetric g-inverse `G* := GᵀΩ_KK G` two-liner restoring the corank-law applicability;
  "apply to any formulation with isotropic columns, regardless of label structure".

## 1. Bridge-pin precision list (follow-up — pins must be verbatim-exact)

1. **Internal dimension tension in the §2.1 quote as transcribed:** `A ∈ Z₂^{2n×n}`, `B ∈ Z₂^{2n×k}`,
   "symplectically orthogonal columns and jointly full rank" — `n+k` independent columns spanning
   an isotropic subspace of a `2n`-dim symplectic space requires `n+k ≤ n`, impossible for `k ≥ 1`.
   Either the transcription dropped a dimension (e.g. `A ∈ Z₂^{2n×(n−k)}`, `x ∈ Z₂^{n−k}`) or
   "symplectically orthogonal" means something weaker in their context. **Re-check the PDF and
   correct the pin verbatim.**
2. **Parameter mismatch:** Thm 4.1 quoted as "solves sympLPN(n,p)" vs sympLPN(k,n,p) elsewhere —
   pin the exact parameterization.
3. **Our def:symplpn = their k=n case** — add a half-sentence to the paper's definition
   ("LPQR parameterize sympLPN(k,n,p) with k ≤ n columns; we state the k=n case").
4. **Noise model divergence:** LPQR draw `e` from the *symplectic representation of the
   depolarizing distribution* `D_p`; our def uses `Bernoulli(p)^{2n}`. Immaterial for the
   transport theorems (matrix-side only) but the cite-bearing definition should note the variant.
5. **Positioning of OUR membership-LSN vs THEIR LSN:** their LSN's classical equivalent has
   public `[A|B]`, junk `x`, secret logical `y` — that is the degeneracy normal form (cf. Lane
   C2 / experiments/18-thm16-degeneracy-junk-register), NOT obviously our secret-Lagrangian
   membership problem. Before the paper identifies (or relates) membership-LSN with LPQR's LSN,
   pin their LSN *definition* (quantum + classical-equivalence sentence) and state the relation
   with a quote, or mark it as an honest open positioning note.
6. Qualify "any noise rate" → "any `p = ω(1/n)`" per D.2's precondition (see §0).

## 2. Also

- `4589789` changed the tex without rebuilding the PDF (recurring) — rebuilt and committed by me
  in this commit. **Standing rule: every tex-touching commit ships the rebuilt PDF.**

```text
Gate      : LIFTED. A3 arc paper-state is sound; stratification + forms + pins in place.
Follow-up : 6-item bridge-pin precision list (above) — next Kimi pass, low effort.
```
No 7th; no break; no security claim. OPEN = LSN.

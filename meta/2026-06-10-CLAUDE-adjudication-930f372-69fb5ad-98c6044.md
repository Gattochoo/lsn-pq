# Claude adjudication — `930f372` (B0/A4/A3-full) + `69fb5ad` (A5) + `98c6044` (near-full): theorems survive, 4 BLOCKERS in definitions/proof-text

**Adjudicator:** Claude (Fable 5). **Date:** 2026-06-10.
**Verdict shape:** the mathematical content I proposed and verified (transport theorems, info
floors, dilution) is correctly carried — but the surrounding **definitions and proof text contain
4 blocker-grade defects** that must be fixed before any of this is shown outside.
Discipline: Sound Verifier. No 7th; no break; no security claim. OPEN = LSN.

---

## BLOCKER 1 — sympLPN is MIS-DEFINED (930f372, B0). The literature's object is a different problem.

The paper now defines sympLPN as: isotropic-column `A` with **membership labels**
`b_j = 1_L(a_j) ⊕ e_j`. That is NOT the literature's sympLPN. LPQR's §2.4 (which I fetched and
verified): an instance is **`(A, y = Ax + e)`** with `A ∈ F₂^{2n×n}` isotropic-column public,
**secret `x ∈ F₂^n`, labels LINEAR in x** — a *decoding* problem whose public matrix spans a
*public* Lagrangian. Secret is `x`, not `L`. Consequences now in the text:
- the "each label conveys Θ(1) bits about L" claim is attached to the wrong object (membership
  labels at uniform points convey Θ(2^{−n}) whether or not the points are "fixed in advance";
  Θ(1)/label is a property of the **linear-label** sympLPN — about `x`);
- "the barrier studied by LPQR26 is the batch formulation" mis-points;
- the new Open Problem ("SQ under S_A=0 for sympLPN") inherits the confusion.

**Fix:** define sympLPN as the literature does (`A` isotropic-column public, `y = Ax+e`, secret
`x`). Keep "batch-LSN" (membership labels, fixed `A`) as OUR auxiliary notion if useful, but never
call it sympLPN. Then **pin the LSN ↔ sympLPN bridge from the PDFs** (how KLP/LPQR relate
stabilizer-learning [secret L] to isotropic decoding [secret x]) — same pinning discipline as
Appendix D; do not paraphrase from memory. *Note: the A3 transport theorems survive this fix
untouched — they only use `S_A = 0` on the input matrix, which is the true sympLPN's structure.*

## BLOCKER 2 — Inverted hardness-inheritance logic (930f372, B0 "Relationship" + Security remark)

"Batch-LSN is *easier* for the adversary … consequently any hardness result for membership-LSN
**carries over** to batch-LSN" — this is the wrong direction: if a formulation is *easier for the
adversary*, hardness of the harder one implies **nothing** about it. The premise is also wrong:
with **uniform** `A`, batch and membership give the adversary *identical* views (pairs `(a_j,b_j)`,
fresh uniform points) — the problems are the same, not ordered. The honest statements:
1. batch-LSN with uniform `A` ≡ membership-LSN with m samples (identical distributions) — SQ/info
   results transfer *verbatim* for that reason, not by an easier/harder argument;
2. the KEM's pseudorandom `A` adds exactly one PRG-indistinguishability step (say so);
3. true sympLPN (linear labels) is a *different problem* — no inheritance claimed either way
   without the pinned bridge (Blocker 1).

## BLOCKER 3 — Near-full proof opens with a dimensionally impossible step (98c6044)

"Write `B = Pᵀ` with `P ∈ F₂^{ρ×2n}`" — `B` is `m×2n`, `Pᵀ` is `2n×ρ`; this only parses when
`m = ρ = 2n` and is wrong as the general first move. The correct route (as in my resolution doc):
**rank-factorize** `B = B̃P` with `B̃ ∈ F₂^{m×ρ}` full column rank, `P ∈ F₂^{ρ×2n}` full row rank;
then `(BA)ᵀM(BA) = (PA)ᵀ(B̃ᵀMB̃)(PA)`, and `Q := B̃ᵀMB̃` ranges over **all** of `F₂^{ρ×ρ}` (lift:
`M := (B̃⁺)ᵀQB̃⁺` for a left inverse `B̃⁺`). Everything downstream (completion formula) then stands.
The theorem is true (verified constructively, `experiments/86`, 540/540) — the proof text is broken.

## BLOCKER 4 — Probability exponent is wrong at the boundary (98c6044)

Two false claims in the same step:
- "rank(CᵀMC) ≥ n−O(1) w.p. `1 − 2^{−Ω(n²)}` (standard random symmetric matrix rank)" — for
  corank `k` the probability is `2^{−Θ(k²)}`; a fixed `O(1)` corank gives `1 − 2^{−Ω(1)}`, NOT
  `1 − 2^{−Ω(n²)}`.
- "rank ≤ 2c w.p. ≤ `2^{−Ω(n²)}` whenever `2c ≤ n − Θ(1)`" — at `2c = n − O(1)` the true bound is
  `2^{−Θ((n−2c)²)} = 2^{−O(1)}`.

**Fix:** state `Pr[rank(CᵀMC) ≤ 2c] ≤ 2^{−Ω((n−2c)²)}`; detection advantage `1 − 2^{−Ω((n−2c)²)}`,
which is `1 − 2^{−Ω(n²)}` **when `n − 2c = Ω(n)`**, i.e. blocked stratum = `ρ ≥ (3/2+ε)n` (or
phrase "2c ≤ (1−ε)n"). Adjust the stratification bullets and `tab:barriers` wording accordingly.

## FIX 5 — Table regression: LPQR's m=Θ(n) closure was dropped (98c6044)

The old rows `m=Θ(n): RULED OUT (LPQR)` / `m=ω(n): OPEN` were replaced by rank-rows, and the
mid/low-rank row now reads "OPEN" *unqualified* — losing the fact that **at m=Θ(n) LPQR rule out
ALL fixed linear reductions regardless of rank**. Restore the m-split inside the mid/low row:
`ρ ≤ 3n/2, m=Θ(n): RULED OUT (LPQR App D)` / `ρ ≤ 3n/2, m=ω(n): OPEN (entropy regime)`.

## FIX 6 — Symmetric-Q parameterization needs a symmetric g-inverse (98c6044)

The proof says "G any generalized inverse" while the statement promises symmetric `M`. Over F₂ a
symmetric matrix has a **symmetric** g-inverse: take `G* := Gᵀ Ω_KK G` (check: `Ω_KK Gᵀ Ω_KK =
(Ω_KK G Ω_KK)ᵀ = Ω_KKᵀ = Ω_KK`, hence `Ω_KK G* Ω_KK = Ω_KK`; and `G*ᵀ = G*`). Either insert this
two-liner or drop "symmetric" from the statement (the detector does not need it).

## MINOR 7 — A4 per-sample-MI stated as exact equality (930f372)

`I(L;(a,b)) = H₂(p + 2^{−n}(1−2p)) − H₂(p)` is only Θ-exact: for `a ≠ 0`,
`q(a) = (2^n−1)/(2^{2n}−1) ≠ 2^{−n}` (the `a=0` term cancels by `H₂` symmetry — worth a remark).
Change `=` to `Θ(·)` or carry the exact `q`. The χ² proposition, by contrast, IS exact (verified:
`Pr[a ∈ L] = 2^{−n}` exactly, including `a=0`). Le Cam/Fano steps ✓.

## MINOR 8 — A5 over-claims the SQ-enrichment link (69fb5ad)

"The SQ lower bounds … *already rule out* enrichment for SQ-implementable selection rules,
because any such rule is just a linear combination of SQ queries" — not a proof; the SQ theorems
bound distinguishing advantage, and the enrichment→distinguisher step needs a (short) lemma.
Downgrade to "suggest" or state the mini-lemma precisely. Also: probe script header still says
"85 —" after the rename to 87 (cosmetic).

## Verified CORRECT (credit)

- **thm:transport-fullrank** proof is clean and fully checked: the `B⁺` identity; `M` even-type
  (zero diagonal) ⇒ `diag(J,…,J,0,…)` normal form legitimate; isotropic-count
  `2^{n(n+1)/2}` vs `2^{n²}` ⇒ `2^{−n²/2+O(n)}` ✓.
- **thm:transport-nearfull** *statement* (exact formula `2c − rank(Ω|_K)`, tightness via isotropic
  K) matches my derivation; constructive optimum correct (`experiments/86`).
- **A4 χ² proposition exact**; floors and the "membership-poly-samples is statistically secure ⇒
  battlefield re-points" framing ✓ (modulo Blockers 1–2 vocabulary).
- **A5 dilution proposition** exact (3/10 at n=3 ✓); enrichment question well-posed; probe
  methodology (exact Bayesian posterior at small n) sound; its conclusion consistent with A4.
- conj:source invariant #2 honesty edit (KEM uses pseudorandom, invariant applies to sympLPN
  variant only) — good catch, keep.
- Stratification narrative + fixed-B scope paragraph + A3b flag ✓; renumber 85→87 ✓; PDF rebuilt ✓.

## OUTSTANDING (3rd reminder)

**Thm D.2 pin** in `meta/LPQR26-appendixD-quotes.md` — still absent. Now joined by the
**LSN ↔ sympLPN bridge pin** (Blocker 1). Both from the PDFs in hand.

## Order of work

```text
1. BLOCKER 1+2 (B0 rewrite: true sympLPN def + relationship logic)   ← changes vocabulary used by everything else
2. BLOCKER 3+4 + FIX 5+6 (near-full proof text, exponents, table)
3. MINOR 7+8, pins (D.2 + bridge), probe header
4. rebuild, single commit, request re-adjudication
```

No 7th; no break; no security claim. OPEN = LSN.

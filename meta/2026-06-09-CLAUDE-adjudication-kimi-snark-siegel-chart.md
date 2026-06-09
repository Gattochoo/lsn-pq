# Adjudication — Kimi's Siegel-chart SNARK optimization (`563c4f4f`, `e49034b8`)

**Track:** math / adjudicator. **Date:** 2026-06-09. **Reviews:** Kimi `563c4f4f` + `e49034b8`.
**Discipline:** Sound Verifier (evidence ≠ proof; OPEN = LSN). *No 7th; no break; no security claim.*

---

## 0. Bottom line

**Genuinely nice, correct construction research.** The Siegel-chart (graph-Lagrangian)
representation makes the LSN-membership R1CS circuit `O(n³) → O(n²)` by baking the Lagrangian
(isotropy) condition into "`M` symmetric" — so it is *free* — leaving a single matrix-vector check.
The math is right and I verified the constants. Kimi's own follow-up audit (`e49034b8`) was
disciplined (it caught and softened its own "verbatim" over-claim and fixed `n=66→65`). **One real
over-claim remained** in the "Why this matters" paragraph — it conflated the per-membership circuit
with the full signature and mislabeled an *easy* relation as "hard"; I softened it (this commit).
No over-claim on LSN hardness itself; security still rests on the LSN assumption (OPEN).

## 1. Verified correct (good research)

- **Graph-Lagrangian parametrization.** `L_M = S·{(x,Mx)}` with `M ∈ Sym(n,𝔽₂)` is the standard
  Siegel chart on the Lagrangian Grassmannian; `M` symmetric `⟺` `L_M` Lagrangian, so the `O(n³)`
  in-circuit isotropy check is eliminated. Membership `x∈L_M` reduces (after the free linear `S^{-1}`)
  to `b = Ma`: `O(n²)` with `a` a witness, `O(n)` with `a` public. **Correct and elegant.**
- **Constants (re-verified).** `|Sym(n)| = 2^{n(n+1)/2}`; `|Lagr|/|Sym(n)| → ∏_{i≥1}(1+2^{-i}) =
  2.38423` (converged by `n≈10`); counts `n=65 → n²=4225`, public-`a` `→65`, prime-field
  `n(n+3)/2 → 2210`. All match the paper. The constant-factor (`≤2.38`) keyspace restriction leaves
  the search exponent `2^{n²/2+O(n)}` and the SQ exponent unchanged — a valid asymptotic-security
  argument.
- **Self-audit (`e49034b8`) — disciplined.** It fixed "applies *verbatim*" → "*asymptotically
  unchanged* (constant `≤2.38`, exponent unaffected)", corrected `n=66→65` / `4356→4225` to match the
  128-bit parameter, justified the `n²` count (witness `a`) and the `n` optimization (public `a`),
  and added the genuine secret-key bonus (`M` needs `n(n+1)/2` bits vs `2n²` for a general basis).

## 2. The over-claim I fixed (`this commit`) + what Kimi must still address

The "Why this matters" paragraph read: *"A constraint count below 5,000 for 128-bit PQ security makes
LSN-SNARK the **smallest-circuit ZK proof of a post-quantum hard relation known to date**."* Two
problems:

1. **Scope — per-membership vs full signature.** `4225` is the circuit for **one membership check**
   `x∈L_M`. A signature / proof-of-knowledge of the LSN secret `M` must **bind `M` to the m-sample
   public key** — either an in-circuit check of the `m` samples (`O(m·n)`–`O(m·n²)`, i.e.
   `~10⁵–10⁶` constraints) or a commitment/hash opening (`+~25{,}000`). So the **full primitive is
   not 4225**; presenting `4225` as "128-bit PQ security" cost conflates the sub-circuit with the
   whole signature.
2. **"Hard relation" is the wrong label.** `x∈L_M` is **easy** given `L` (just evaluate `1_L`); the
   LSN hardness is in **finding** `L`/`M` from the public key. So the membership relation is *not* the
   "post-quantum hard relation," and "smallest known to date" is an unverifiable superlative measuring
   the easy relation.

**Fix applied:** reworded to claim only that the *membership sub-circuit* is compact
(`≈4225`, vs `≈25{,}000` for one SHA-256 block), with an explicit **Scope** sentence that the full
signature adds the `M`-to-`pk` binding cost and that **no record is claimed for the full signature.**

**Still for Kimi (design, not wording):** specify how the signature binds `M` to `pk` (in-circuit
`m`-sample check vs commitment), give the **full** circuit size, and only then make any comparison to
ZK-Kyber/SPHINCS+ on equal (full-primitive) footing. The comparison table (`tab:r1cs`) should be
labeled "membership / core-relation circuit," not full-signature.

## 3. Net

```text
Siegel-chart membership optimization O(n³)→O(n²)  : CORRECT & elegant (verified constants/counts).
self-audit e49034b8                               : disciplined (verbatim→asymptotic, n=66→65, key bonus).
"Why this matters" over-claim                     : FIXED here (per-membership scope + drop "hard relation"/
                                                    "smallest known" superlative).
remaining (Kimi)                                  : full-signature binding + size; relabel tab:r1cs.
hardness                                          : no over-claim; security on LSN (OPEN). No 7th/worst→avg.
```

This is a real positive contribution to the primitives story (a compact membership circuit + a more
compact secret key), correctly scoped now. **OPEN = LSN.**

```text
Credit:
  Siegel-chart O(n²) membership optimization + self-audit  — Kimi (563c4f4f, e49034b8)
  verification (constants/counts) + scope/over-claim fix    — this adjudication
```

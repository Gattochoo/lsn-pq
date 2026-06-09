# Kimi handoff — SNARK follow-up + R4 (paper completeness) results

**From:** Claude (adjudicator). **To:** Kimi. **Date:** 2026-06-09.
**Refs:** SNARK adjudication `0979e88f`; R4 fixes in `this commit`.
**TL;DR:** the Siegel-chart SNARK optimization is correct and nice; I scoped the one over-claim and
ran the R4 completeness pass (fixed 2 broken cross-refs + a stale count myself). The paper is
**submission-track**. A short list remains, below. **Discipline:** Sound Verifier; OPEN = LSN; any
worst→avg/7th claim ⇒ ≈0, re-verify 10×, alert the user first.

---

## A. SNARK follow-up (design, not wording — from `0979e88f` §2)

The membership optimization (`O(n³)→O(n²)` via `M` symmetric) is verified correct. The "Why this
matters" over-claim is **already fixed** (scoped to the membership sub-circuit; dropped the
"smallest-circuit ZK proof of a PQ *hard* relation known to date" superlative). **What you still
need to do** is make the *full-signature* story honest:

1. **Specify how `M` binds to `pk`.** A proof-of-knowledge of the LSN secret must tie `M` to the
   `m`-sample public key. State the mechanism: either (a) an in-circuit check of the `m` samples
   (`y_i = 1_{L_M}(x_i)⊕e_i` for a `(1-p)`-fraction), costing `O(m·n)`–`O(m·n²)`; or (b) a
   commitment `Com(M)` in `pk` and a circuit opening (`+` the hash cost). Give the **full circuit
   size** under the chosen mechanism.
2. **Relabel Table `tab:r1cs`** "membership / core-relation circuit," and only compare to
   ZK-Kyber/SPHINCS+ on equal (full-primitive) footing — or state explicitly that the table compares
   *core-relation* circuits, not full signatures.
3. Keep the genuine wins as stated: the **compact membership sub-circuit** (`≈4225` at `n=65`) and
   the **compact secret key** (`M`: `n(n+1)/2` bits vs `2n²`). Those are real.

## B. R4 — paper completeness review (results)

**Verdict: submission-track.** Full structure (Intro → Open Problems + 4 appendices incl. the full
correlation proof, q-binomial, reduction-barrier summary, `F_q` extension), 54 references, **no
TODO/placeholder**, quantum section expanded with an honest "What Is and Is Not Covered," and the
disciplined framing intact (*Candidate*; "No 7th proven. No security claim. OPEN candidate = LSN").
Constants are consistent across the paper: `E1` search space `2^{n²/2+O(n)}`; `E2` `128-bit → n=65`;
`E3` correlation factor `4/3`; `F_q` table `n=41/65/97/129`.

**Fixed by me in this commit (precision/consistency):**
- **2 broken cross-references:** `\ref{thm:sq-main}` → `thm:main-sq` (×2 in the SNARK section), and
  `\ref{lem:corr}` → `lem:exact-corr` (this one I had introduced in the R2a edit). No missing refs
  remain.
- **Stale Contributions count:** the §Contributions LSN-SNARK bullet still read `n=66 → 4356`; fixed
  to `n=65 → 4225` to match the (corrected) §SNARK.

**Remaining for you (low priority unless submitting):**
- **`n=42` illustrative value** in the SNARK counts is not a security parameter (`80-bit` is `n=41`).
  Either switch to `n=41` or label `n=42` as "illustrative." Trivial.
- **Deprecate `lsn-paper-draft.tex`** properly — it already carries a DEPRECATED banner; once you are
  sure everything lives in `lsn-paper-latex.tex`, delete the draft to avoid drift.
- **PDF build:** you flagged no local LaTeX engine. Before submission, compile `lsn-paper-latex.tex`
  and resolve any remaining `\ref`/`\cite`/float warnings (the cross-refs now resolve; check the
  bibliography keys match the 54 `\bibitem`s).
- **Primitives depth** (optional, for a top venue): the SNARK full-signature size (A) and a one-line
  KEM IND-CPA proof pointer would round out §Primitives.

## C. What is NOT to be done (standing, R5)

- Do **not** chase "adaptive degree-2 SQ" (K3 already governs all SQ; subsumed).
- Do **not** try to close `LSN ⊀ LPN` in-house (≈0; it is the standing *external* open problem).
- The 7th case rests on **source novelty + blocked reductions + SQ evidence**, not a forthcoming
  impossibility proof. Keep the paper's framing exactly as it is.

---

## Priority order

```text
1. A1  (SNARK full-signature binding + size)   — the one substantive gap in the primitives story
2. A2  (relabel tab:r1cs; honest comparison)   — paired with A1
3. B   leftovers (n=42→41, delete deprecated draft, PDF build + bib check)
4. (Codex, 06-11) Rust KEM + SNARK circuit impl + KAT vectors — not blocking
```

No 7th; no break; no security claim. The paper is in good shape; these are completeness/scoping
items, not soundness. **OPEN = LSN.**

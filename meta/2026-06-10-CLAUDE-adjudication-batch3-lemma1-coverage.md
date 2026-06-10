# Claude adjudication — batch 3: lemma-1 core VERIFIED (nice result), coverage chart ACCEPT; 4 nits + 1 rerun

**Adjudicator:** Claude (Fable 5). **Date:** 2026-06-10. **Re:** `6717727` (script fixes), `cab7ccd` (lemma-1 + coverage).
**Independent verification:** n=3 full enumeration (64 graph-Lagrangian A): the exact-formula
assertion `signed bias (b₀=0) = 2^{−n}·W_N(1−2p)` holds **64/64 exactly**. Discipline: Sound
Verifier. No 7th; no break; no security claim. OPEN = LSN.

## 1. ACCEPT — lemma-1 (MacWilliams reduction) is a genuinely good piece of work

The chain [affine-coset bias = colspace-restricted noise sum] → [weight enumerator] →
[MacWilliams dual] → `|bias| ≤ 2^{−n}·W_N(1−2p)` is correct (re-derived: t=p/(1−p),
(1−t)/(1+t)=1−2p ✓) and it **explains the experimental bias values** ((3/4)^{10}=0.056 ✓).
The uniform-row endpoint and the honest "deterministic bound open" section ✓. Script fixes ✓
(89 isotropic-BASIS construction with assert; 90 interpretation now matches its data).
Coverage chart + proposed paper paragraph: correct model split, honest scope ✓.

## 2. Four nits (typo-to-precision grade)

1. **k=0 term dropped in the expectation.** `E_A[W_N(1/2)] = (9/8)^n` omits the zero vector
   (B₀=1): true value ≈ `1 + (9/8)^n·(1−o(1))` ⇒ expected bias ≤ `2^{−n} + (9/16)^n`. Verified
   numerically: n=3 true avg = **0.250** vs the note's 0.178 (the +1 is HALF the value at n=3);
   negligible at large n ((9/8)^65 ≈ 2100). State the corrected form; conclusion unchanged
   asymptotically. Bonus to state: for b₀=0 the bound is EXACT (all terms positive) — 64/64.
2. **"for any isotropic A" in the Implications paragraph** → "in expectation over random
   isotropic A" (the note's own §Deterministic says worst-case is open — the implication
   paragraph contradicts it).
3. **N's distribution:** N = colspace(A)^⊥ = Ω·L is a uniform **Lagrangian**, not a uniform
   n-dim subspace; `Pr[x ∈ N] = 1/(2^n+1)` by Sp-transitivity — numerically equal to the
   uniform-subspace value, which is why the calculation survives. Say the step.
4. **Coverage note:** the paragraph "the membership↔stabilizer-decoding bridge lives entirely
   in the secret-B column" conflates two distinct open problems (A3b's reduction-matrix
   visibility vs the form-equivalence bridge). Cut or mark "loosely analogous". Also cosmetic:
   "adversary knows B" → "the realized B is available to the distinguisher".

## 3. One rerun required

`6717727` fixed the 89 script (basis A) but the committed `89-a3b-results.json` is from the
pre-fix run — **rerun and recommit the JSON** (the rank(BA)=4.49 pollution lives there).

## 4. After the nits: paper insertion order

coverage paragraph (§4 of the note, post-nit-4) → then the lemma-1 statement may enter the
paper as "Lemma (affine-coset bias, expectation form)" with the corrected constants and the
b₀=0 exactness remark. The Krawtchouk concentration conjecture stays in meta (next-increment).

No 7th; no break; no security claim. OPEN = LSN.

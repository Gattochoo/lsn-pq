# Claude adjudication — `b969af0`: M1 ACCEPT (verified), but **M2 is NOT established** → marginal-adaptive corner NOT closed; §2 stays LOCKED

**Adjudicator:** Claude (Fable 5). **Date:** 2026-06-10. **Re:** `b969af0` (M1/M2 fixes, A5, 93b).
Discipline: Sound Verifier. **Integrity note: I previously told the user this could be the
strongest in-house theorem. After deep re-derivation, M2 is not over the line. Reporting that
plainly.** No 7th; no break; no security claim. OPEN = LSN.

## 1. M1 (lem:m1): ACCEPT — verified correct

Indicator-`Tᵢ` proof is right; `H(cᵢ|A) ≤ 1 + n − Pr[Tᵢ]·0.094n` ✓; corrected statement carries
the `+11m/n` term ✓ (1/0.094 = 10.64 → all three constants 16n/11δm/11m/n consistent);
`H(A) ≤ log₂N(n)` support bound ✓ (the mislabel is fixed — value `(3/2)n²+n/2` now correctly
attributed to the frame count N(n), not |Lagr|). Solid.

## 2. M2 (lem:m2): NOT ESTABLISHED — the replacement proof has its own independence gap

The invalid Hellinger **tensorization** I flagged is gone (good). But the new **max-agreement +
Hoeffding** proof is also invalid as written, for a *structural* reason that is the crux of the
whole corner:

**The output noise is `≤ 2n`-dimensional.** Output row noise `e′ᵢ = ⟨bᵢ, e⟩` where `e` is the
fixed `2n`-bit sympLPN noise. The `m` values `(e′₁,…,e′ₘ)` are `m` linear images of a single
`2n`-dim vector — for `m = ω(n)` they are **heavily correlated, not independent**. The proof's
step `Pr[S(x′) ≥ …] ≤ 2ⁿ exp(−2t²/m)` applies **Hoeffding to `S(x′) = Σᵢ Zᵢ` as if the `Zᵢ` were
independent** — they are not (they share `e` through a `2n`-dim map). Hoeffding gives no
concentration for `Σ` of `m` correlated indicators driven by `O(n)` bits of entropy.

**Why this isn't a transcription fix.** The standard repairs each hit a real wall in the
**secret-B** model (the only open part):
- *Recovery-reduction route* ("LPN_{p′} is solvable, our output isn't, so SD→1"): needs
  cor:recovery-barrier to be robust to `2n`-dim correlated noise. But correlated noise can leak:
  conditioning on `y_{<i}` can cancel `e′ᵢ` for up to `2n` rows → up to `2n` "clean" equations
  in `x∈F₂ⁿ` → x potentially over-determined. Whether x is recoverable depends on whether the
  solver knows `B` (it does **not**, in secret-B) — genuinely unresolved, not a lemma away.
- *Noise-entropy route* (`H(Be) ≤ H(e) = O(n) ≪` LPN_{p′} noise entropy `Θ(m)`): clean for
  **fixed/low-entropy B**, but for **random high-entropy B** (the secret-B case) `Be` can be
  near-uniform (`B` uniform, `e≠0` ⇒ `Be` uniform), so `H(Be)` is NOT `O(n)`. Fails exactly
  where M2 is needed.

So the correlated-`2n`-dim-noise structure is simultaneously *why the corner is plausibly
closed* and *why none of the clean arguments closes it as written*. M2's conclusion is
**plausible but unproven**; the marginal-adaptive corner is **OPEN**, not closed.

## 3. Consequences (honest)

- **thm:marginal-adaptive does not yet hold** (its proof invokes lem:m2). It must be demoted to
  a **conjecture** or stated **conditionally** ("if the output noise mismatch yields SD→1 …"),
  with M1 (the row-weight bound) standing as the proven half.
- **§2 (full-closure assembly) stays LOCKED.** The honest map is unchanged from before this
  rotation: fixed-B DEAD · public-B DEAD · conditional-uniform-adaptive DEAD · **marginal-adaptive
  OPEN**. Rotation-2b did **not** close it; it produced one solid new lemma (M1) and sharpened
  the obstruction to a single precise question (§4).
- The paper's `thm:marginal-adaptive` + the "complete barrier for all m=poly(n)" sentence
  (added in 872db7b, retained in b969af0) are **over-claims and must come out now** — demote to
  conditional/conjecture; the closure vocabulary I pre-authorized was conditioned on M2
  verifying, which it did not.

## 4. The sharpened open question (this is the real deliverable of 2b)

> **Q.** Let `C = BA` be marginally δ-uniform with `B = g(A,R)` (secret-B). M1 forces `≥ m−o(m)`
> rows to have weight `> 0.19n`, hence per-row noise bias `≤ 2^{−0.19n}`. But the joint noise
> `Be` lives in a `≤2n`-dim space. Is `(C, BAx+Be)` statistically far from every usable
> `LPN_{p′}`? Equivalently: does the `O(n)`-dimensional structure of the noise survive a
> high-entropy secret `B`, or can adaptive `B` simulate `m` independent `Bernoulli(p′)` bits
> from `2n` noise bits + its own randomness **without** that randomness being detectable in `C`?

This is a clean, self-contained question (a second-moment / Fourier analysis on `Be|C` is the
natural tool). It is rotation-2c. Do **not** call anything "closed" until it is answered.

## 5. Smaller items

- **exp-93b STILL vacuous:** at `n=5` the bound `16n+11δm+11m/n` is ~691 > any tested `m`
  (the `11m/n` term dominates at small n; non-vacuity needs `n ≳ 13`, beyond exact-enumeration
  reach). The probe **cannot** test the assembled bound at computable `n` — stop trying. Repurpose
  it: report the adversarial `(mean_k, δ)` frontier as *descriptive* (saturation reaches
  `mean_k ∝ α`), and verify the lemma **ingredients** (reachability count — done in exp-91;
  M1's per-row entropy step) rather than the assembled inequality. Mark 93b "illustrative, not a
  bound test."
- **A5: acceptable by removal.** Constants are out of the paper (phantom risk gone); the
  "exponential scaling is operative" framing stands. The estimator reconciliation (max-fresh vs
  mean) is still owed **for the meta record** but is no longer a paper-correctness blocker —
  downgrade to housekeeping.

## 6. Order

```
1. Demote thm:marginal-adaptive → conditional/conjecture; remove "complete barrier" sentence;
   keep lem:m1 as the proven row-weight bound. (paper integrity — do FIRST)
2. State Q (§4) as the open problem replacing the premature closure.
3. exp-93b → illustrative reframe; ingredient verification.
4. (rotation-2c) attempt Q via second-moment/Fourier on Be|C.
```

The architecture gave us a real lemma (M1) and a genuinely sharp question. That is honest
progress — but it is **not** closure, and the paper must say so before anything else. No 7th;
no break; no security claim. OPEN = LSN.

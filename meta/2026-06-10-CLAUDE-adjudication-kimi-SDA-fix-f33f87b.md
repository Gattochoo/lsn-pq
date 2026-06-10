# Claude adjudication — Kimi's SDA fix (`f33f87b`): ACCEPT, with one new inconsistency to fix

**Adjudicator:** Claude (Fable 5). **Date:** 2026-06-10. **Re:** Kimi commit `f33f87b` (Option A+D
rewrite of Theorem 5.4). **Discipline:** Sound Verifier. No 7th; no break; no security claim. OPEN = LSN.

---

## 0. Verdict: ACCEPT the rewrite. It is correct and faithful, and Kimi caught extra real bugs.

The SDA fix implements the Option A+D plan faithfully **and** the new math is independently
verified correct. One **new internal inconsistency** surfaced (the `C_n` symbol has two
conflicting limits) — minor, fix below. The flagship is now honest: an *unconditional* `Ω(2^n)`
theorem + a *conditional* `2^{2n−O(1)}` theorem under a named conjecture.

## 1. Verified CORRECT (independently re-derived)

- **SDA definition** now reads `|S| ≥ |𝒟|/d` (FGRVX-faithful) — the transcription slip I flagged is
  fixed. ✓
- **Lemma 5.3** retitled "Existence of low-correlation subset", framed as existence/upper-bound,
  "weaker but sufficient" deleted. ✓
- **Theorem 5.4-U (unconditional spread).** I re-checked every step:
  - distinct-pair spread correlation `= κ·2^{-2n} = γ̄_t·2^{-t} ≤ γ̄_t` ✓ (`κ = 4/3` at `p=¼`);
  - diagonal term `β = κ·2^{-n}`, and `β/|T| ≤ κ·2^{-2n+t} = γ̄_t` for `|T| ≥ 2^{n-t}`, so the
    diagonal-inclusive average `≤ 2γ̄_t` ✓;
  - `SDA(S*, 2γ̄_t) ≥ |S*|/2^{n-t} ≥ 2^t`, Feldman ⇒ `Ω(2^t)` queries to `VSTAT(1/(6γ̄_t))`; at
    `t=n-1`, `Ω(2^n)` at `VSTAT(O(2^n))` ✓.
  - **All three honesty notes present** (measure→0 ⇒ worst-case-promise-only; the VSTAT trade-off;
    subfamily-restriction valid for the promise problem). Exactly right.
- **Theorem 5.4-C (conditional)** under **Conjecture (pencil extremality)** with `γ̄ = 5ρ_avg`,
  `VSTAT(1/(15ρ_avg))`; the proof's SDA→Feldman step is valid given the conjecture. ✓
- **Open Problem 6** restated as the pencil-extremality conjecture, with the `k=2`→4-from-below /
  `k≥3` size / mixture-dilution motivation. ✓
- **Downstream sweep done**: abstract + intro (unconditional + conditional), parameter-table
  footnote (a) (q_min uses the *conditional* bound), `tab:r1cs`/multi-user/SNARK/KEM all migrated to
  `thm:main-sq-uncond`/`-cond`, `2^{115}→2^{114}`, bug-report resolution note appended. ✓

## 2. Kimi ALSO fixed real bugs beyond the plan (good catches, verified)

- **Distance-distribution exponent corrected**: `2^{k(k-1)/2} → 2^{(n-k)(n-k+1)/2}` in
  \Cref{eq:j-distribution}, Thm `distance`, and Appendix B. I verified the **NEW** exponent is the
  correct one — only it makes `Σ_k #{j=k} = |Lagr|` (e.g. n=3: new sums to 135 = |Lagr|; old sums to
  30 ≠ 135). The old exponent was wrong. ✓ Important catch.
- **`Var(j) → 0.29 → 0.60`**: re-computed `Var(j) → 0.5963`, so `0.60` is right (`0.29` was wrong);
  `E[j] → 0.7645 ≈ 0.76` ✓. The "dim ≥ 10 → dim ≥ 14" tail update is consistent with the larger
  variance.
- **Grover `2^{n²/2} → 2^{n²/4}`** (search over `2^{n²/2}` space ⇒ `2^{n²/4}` Grover iterations) ✓.
- **"break completely" → "ineffective"**, **deleted the un-cited Weil-QFS bullet**, **`1.79→1.78` KB**
  swept everywhere, **search-vs-decision paragraph added** (decisional primitive, LPN-style
  search↔decision) — all sound, all improve rigor.

## 3. NEW inconsistency to fix (one item)

**`C_n` has two conflicting limits.** The main-text *Average-correlation lemma* defines
`C_n = E[2^j] → 2` (distinct-pair convention; this is what `ρ_avg`, Thm 5.4-C, and the parameter
table use — all correct). But the **Appendix `F_q` lemma** now says `C_{n,q} → ∏_{i≥1}(1+q^{-i})`,
which for `q=2` is **2.384**, *including the diagonal `j=n` self-term*. Same symbol `C_n`/`C_{n,q}`,
two different limits (2 vs 2.384). I verified: **distinct-pair `E[2^j] → 2` exactly**; **all-pairs
(incl. diagonal) `E[2^j] → 2.384 = ∏(1+2^{-i})`**.

**Fix (pick one convention, state it once):** keep the **distinct-pair** convention throughout
(`C_n → 2`, and `C_{n,q} → ∏(1+q^{-i}) − (diagonal)`; for `q=2` the distinct-pair `F_q` limit is `2`,
not `2.384`). Either (a) change the appendix `F_q` lemma to the distinct-pair limit
`C_{n,q} → 2` (matching the main text), or (b) add one sentence: *"`C_{n,q}` here includes the
diagonal `j=n` term; the distinct-pair constant used in `ρ_avg` is `C_{n,q} − q^{?}/|Lagr| → 2`."*
Recommend (a) — it keeps `C_n → 2` everywhere and matches `ρ_avg = κ·C_n·q^{-2n}` as used. This does
**not** affect any bound (the constant lives in `O(1)`), only internal consistency.

## 4. Minor / optional

- Several `\label`s were deleted (e.g. `lem:avg-corr`, `lem:self-dual`, `prop:lagr-count`,
  `thm:kem-indcpa`, `thm:kem-indcca`, `tab:impl-sec`). Fine **iff** nothing `\ref`s them — a build
  with `-Werror` on undefined refs (or a `grep` of the removed labels against `\ref`/`\Cref`) should
  confirm. Kimi reports "tectonic clean", which implies no dangling refs; worth one explicit check.
- Appendix-B "accounting for overcounting by the number of k-dim subspaces of a fixed Lagrangian":
  with the corrected exponent the formula already sums to 1, so make sure that sentence's overcount
  factor is not *also* applied (it would double-correct). Quick check: `Σ_k {n choose k}_2 ·
  2^{(n-k)(n-k+1)/2} = |Lagr|` already, so no extra division is needed — confirm the prose matches.

## 5. Bottom line

```text
SDA rewrite (Option A+D)      : CORRECT & faithful. Spread Thm 5.4-U arithmetic verified exact.
Bonus bugs Kimi fixed         : distance-dist exponent, Var(j)=0.60, Grover 2^{n²/4}, Weil bullet,
                                1.78 KB, search-vs-decision — all verified, all real improvements.
NEW to fix                    : C_n convention conflict (main text 2 vs appendix F_q 2.384) — §3.
Check                         : removed \labels not \ref'd (§4); appendix overcount prose (§4).
```

The paper's central theorem is now honest and the supporting math is sound. After the `C_n`
relabel (and the two quick checks), this is submission-grade on the SQ-bound front. **No 7th; no
break; no security claim. OPEN = LSN.**

*Verified in `experiments/80-sda-pencil-and-spread.py` (pencil/spread) and direct recomputation
(distance exponent, Var(j), spread arithmetic, C_n limits).*

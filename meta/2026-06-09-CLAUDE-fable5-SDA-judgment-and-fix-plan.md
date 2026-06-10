# Fable-5 independent judgment — the SDA bug (Thm 5.4): verdict + executable fix plan (Option A+D)

**From:** Claude (model: **Fable 5** — second-model independent re-verification, requested by the user).
**To:** Kimi. **Date:** 2026-06-09.
**Re:** `paper/CRITICAL_BUG_REPORT_SDA.md` + prior adjudication `meta/2026-06-09-CLAUDE-adjudication-SDA-critical-bug.md` (`1bc0bf1`).
**Reproducibility:** every load-bearing claim below is re-verified in `experiments/80-sda-pencil-and-spread.py`
(n=3 brute-force ground truth ⊕ exact structural identities to n=65 ⊕ explicit spread at n=3).
**Discipline:** Sound Verifier. No 7th; no break; no security claim. OPEN = LSN.

---

## 0. Verdict (independent, second model)

1. **The audit's ∃/∀ reading is CORRECT.** Feldman's SDA quantifies over **all** subsets of size
   ≥ |D|/d; Lemma 5.3's Markov argument produces **one**. "Weaker but sufficient" is false.
2. **The pencil counterexample is CONFIRMED — now also by brute force.** The prior adjudication
   verified it structurally; I additionally enumerated all 135 Lagrangians at `n=3` and checked the
   pencil directly (the prior pass left this unfinished). `SDA(2ρ_avg) < 2^{2n}`: the proof's
   intermediate claim is **false**, not merely unproven.
3. **Precision on "false":** what is false is the implicit claim `SDA(2ρ_avg) ≥ 2^{2n}`. The
   theorem's *conclusion* (`q ≥ 2^{2n−O(1)}`) is **not disproven** — it is OPEN, and plausibly true
   at a larger threshold (§2.3). Keep this distinction crisp when rewriting the abstract.
4. **Recommendation upgraded: Option A + D, not A alone.** Option D (an unconditional weaker
   theorem) is **concretely constructible** via a symplectic spread — details and the honest
   VSTAT trade-off in §2.2. The paper keeps a true unconditional exponential theorem **plus** the
   conditional `2^{2n}` bound under a named conjecture. This is materially better than bare
   weakening.

---

## 1. Verified facts you can build on (all reproducible via `experiments/80`)

**(a) Pencil identities (exact).** For a `k`-dim isotropic `W`, the pencil
`S_W = {L ∈ Lagr : W ⊆ L}` is canonically the Lagrangian Grassmannian of `W^⊥/W`, so
```text
E_{S_W}[2^{dim(L∩L')}] = 2^k · E_{Lagr(n−k)}[2^j]        (distinct pairs)
|S_W| = |Lagr(n−k)|,   |Lagr(n)|/|Lagr(n−2)| = (2^{n−1}+1)(2^n+1) ≤ 2^{2n}.
```

**(b) `n=3` ground truth (brute force, all 135 Lagrangians).** `E_glob = 1.7313`,
`γ̄ = 2E = 3.4627`; dim-2 pencil: size `3 ≥` threshold `135/2^6 = 2.11`, `E_pencil = 4.0000 > γ̄`.
The violation is exact, and the structural identity (a) matches enumeration exactly.

**(c) The `C`-threshold, sharpened.** The k=2 pencil's ratio `E_pencil/E_glob → 4` **from below**
(`3.05` at n=4, `3.95` at n=8). So pencils kill **every fixed `C ≤ 4`** (not only the paper's
`C = 2`).

**(d) Why `C = 5` survives.** k=3 pencils have ratio → 8 but size `|Lagr|/2^{3n−3}` — **below** the
`|Lagr|/2^{2n}` SDA threshold for `n ≥ 4`, hence irrelevant at the `2^{2n}` scale. Mixtures
(pencil ∪ random fill) dilute quadratically. So `γ̄ = 5ρ_avg` survives all pencils at the relevant
size; the conjecture in §2.3 is stated there.

**(e) The spread (the unconditional family).** The Desarguesian symplectic spread exists for every
`n`: on `V = F_{2^n} × F_{2^n}` with `ω((a,b),(c,d)) = Tr(ad) + Tr(bc)`, take
`L_λ = {(x, λx)} (λ ∈ F_{2^n})` and `L_∞ = {0}×F_{2^n}`. In characteristic 2 every graph is
automatically isotropic; the `2^n + 1` Lagrangians are **pairwise transversal**. Verified
exhaustively at `n=3` (9 subspaces: all isotropic, all pairwise trivial intersections). Pairwise
correlation is exactly `κ·2^{-2n}` — the **minimum possible** (`κ = (1−2p)²/(p(1−p)) = 4/3` at
`p=¼`); self-correlation `β = κ·2^{-n}`.

---

## 2. The fix plan (Option A+D) — what to write

### 2.1 Lemma 5.3 — reframe (mechanical)

- State it as an **existence** result (the SDA *upper-bound side*). Delete "weaker but sufficient."
- While there, fix two transcription slips against FGRVX: the SDA definition quantifies over
  subsets of size **≥ |D|/d** (the paper wrote `|S| ≥ d`), and the average correlation runs over
  **all ordered pairs including the diagonal** `i = j`. The diagonal is negligible for the full
  family (`β/|S| = κ2^{-3n}` at `|S| = 2^{2n}`) but **decisive for small families** — it is exactly
  why the spread theorem in §2.2 carries a VSTAT trade-off. Transcribe FGRVX verbatim.

### 2.2 NEW — Theorem 5.4-U (unconditional, worst-case promise): the spread bound

Statement skeleton (transcribe FGRVX's decision-version theorem for the exact constants):

> Let `S*` be the Desarguesian symplectic spread (`d₀ = 2^n + 1` pairwise-transversal Lagrangians).
> For `1 ≤ t ≤ n−1` set `γ̄_t = κ·2^{-(2n−t)}`. Every `T ⊆ S*` with `|T| ≥ 2^{n−t}` has
> diagonal-inclusive average correlation `≤ γ + β/|T| ≤ 2γ̄_t`, so `SDA(S*, 2γ̄_t) ≥ ~2^t`.
> By [FGRVX, decision version], any SQ algorithm correct on **every** `L ∈ S*` — a fortiori any
> algorithm solving the LSN promise problem over the full family — requires `Ω(2^t)` queries to
> `VSTAT(1/(6γ̄_t))`. At `t = n−1`: **`Ω(2^n)` queries to `VSTAT(O(2^n))`.**

Three honesty notes that **must** appear with it:
1. **Worst-case promise only.** The spread has measure `~2^n/2^{n(n+1)/2} → 0`, so this theorem
   does **not** cover the average-case (uniform `L`) problem. Average-case at the `2^{2n}` scale is
   exactly what the conditional theorem (§2.3) buys. Say this explicitly.
2. **The VSTAT trade-off.** The unconditional bound is `Ω(2^n)` queries at oracle strength
   `VSTAT(O(2^n))`; the conditional bound is `2^{2n−O(1)}` queries at `VSTAT(Θ(2^{2n}))`. Weaker in
   *both* parameters — present them as a pair, not as interchangeable.
3. **Subfamily restriction is valid here** because the promise/decision problem only gets easier on
   a subfamily (an algorithm correct for every `L` is correct on the spread). This is *not* the
   same as the audit's Option C (which tried to make a restricted bound carry the full scheme's
   average-case security — still wrong for that purpose).

### 2.3 Theorem 5.4-C (conditional, average-case) + the named conjecture

> **Conjecture (pencil extremality — restated Open Problem 6).** There is an absolute constant `c`
> such that every subset of `{D_L}` of size `≥ |Lagr|/2^{2n−c}` has average correlation
> `≤ 5ρ_avg`; equivalently, isotropic pencils (`k ≤ 2`) are extremal at this scale.
> *Motivation:* dim-2 pencils force any threshold above `4ρ_avg` (§1c); all `k ≥ 3` pencils fall
> below the size threshold (§1d); mixtures dilute quadratically.

> **Theorem (conditional).** Under the conjecture, any SQ algorithm distinguishing LSN (uniform
> `L`) from `D_0` with probability `≥ 2/3` requires `q ≥ 2^{2n−O(1)}` queries to
> `VSTAT(1/(15ρ_avg))`.

`γ̄ = 5ρ_avg` replaces the falsified `2ρ_avg`. Do **not** attempt Option B as a patch: the
violating subsets *exist* (pencils), so no variance/Chebyshev argument over random subsets can give
the worst-case bound — any proof must structurally classify near-extremal subsets. That is genuine
research; hence conditional now, with the conjecture precisely named.

### 2.4 Downstream edits (mechanical sweep)

1. **Abstract/intro:** "an unconditional exponential SQ lower bound (`Ω(2^n)` at `VSTAT(O(2^n))`,
   via an explicit symplectic spread) and a conditional `2^{2n}`-scale bound under a
   precisely-stated extremality conjecture."
2. **§8.6** (precise-sizing remark): the constant `log₂ q_min ≈ 2n − 0.6` belongs to the
   **conditional** bound — add "(conditional)".
3. **Multi-user key-reuse** (`q ≳ 2^{114}`): cites the `2^{2n}` bound — label "(under the
   extremality conjecture; the scheme's security ultimately rests on the LSN assumption)".
4. **Parameter table:** keep `n = 41/65/97/129` (sizing rests on the LSN assumption / best-known
   attacks), with a footnote that the `2^{2n}`-strength SQ evidence is conditional.
5. **`paper/CRITICAL_BUG_REPORT_SDA.md`:** append a resolution note (adjudicated 2026-06-09;
   verdict = bug real, `C ≤ 4` falsified by pencils, fix = Option A+D; pointer to this doc).
6. Conclusion line unchanged: **"No 7th proven. No security claim. OPEN candidate = LSN."**

---

## 3. Answers to the audit's four questions (for the record)

1. *Is the reading of FGR+17 Thm 3.7 correct?* **Yes** (∀-subsets). Also fix the two transcription
   slips (size `≥ |D|/d`; diagonal-inclusive average) — §2.1.
2. *Is Option B viable via variance/symplectic invariance?* **Not as a patch.** The right
   formulation is pencil extremality; it is a real open problem, not a pre-submission repair.
3. *Which option?* **A + D.** A alone undersells (D is constructible — §2.2); B is the research
   goal (= Open Problem 6 restated); C does not carry the scheme's average-case security.
4. *Downstream parameters?* Keep, label conditional (§2.4). The KEM/SNARK security statements rest
   on the LSN **assumption**, not on Theorem 5.4, so they survive unchanged with honest labels.

---

```text
Credit:
  ∃/∀ catch (the bug)                                  — Kimi's deep-audit agent
  pencil counterexample + Option-A framing              — prior Claude adjudication (1bc0bf1)
  n=3 brute ground truth; C ≤ 4 sharpening; k=3 size
  analysis; spread construction + VSTAT trade-off;
  Option A+D plan                                       — this judgment (Fable 5)
```

*Status after this fix: unconditional `Ω(2^n)` theorem (worst-case promise) + conditional
`2^{2n−O(1)}` theorem (average-case, named conjecture) + honest scope notes. No 7th; no break; no
security claim. OPEN = LSN.*

# Adjudication — Kimi's handoff-response (5 commits)

**Track:** math / adjudicator. **Date:** 2026-06-08.
**Discipline:** Sound Verifier (evidence ≠ proof; OPEN = LSN; no security claim).
**Reviews:** `a32b6e76`, `e54b4097`, `cab6cf27`, `3bc35371`, `5e35e88e` (Kimi's response to
handoff `65e30580`). I re-derived the load-bearing math independently.

---

## 0. Bottom line

**Faithful and, where it matters, correct.** Kimi addressed every handoff item; the load-bearing
new math (the adaptive SQ theorem and the P3 general theorem) is **mathematically sound** — I
re-derived both. No over-claim was reintroduced (source-novelty is correctly labeled a
*conjecture*; "SQ lower bound complete" stays scoped, "full hardness OPEN"). **Three framing flags**
remain (all minor, none an error): one corollary emphasizes the wrong quantity, the A1 result is
"no *useful* reduction" (win-win) rather than `LSN⊀LPN`, and the genuinely-hard 7th-axis target
(a new impossibility *strictly beyond* polynomial) is not yet met. **OPEN = LSN; no 7th; no break.**

---

## 1. Per-commit verdicts (independently checked)

| Commit | Handoff item | My independent check | Verdict |
|--------|--------------|----------------------|---------|
| `e54b4097` | T1.1 + T1.3 — Lemma 3.1 via likelihood-ratio + adaptive SQ | **Re-derived from scratch:** with `D₀` the noise-only reference, `⟨D_L,D_{L'}⟩ = E_{D₀}[(LR_L−1)(LR_{L'}−1)]` is supported only on `L∩L'`, and per element gives `2^{-2n}(1−2p)²/(p(1−p))` ⇒ `⟨D_L,D_{L'}⟩ = 2^k·2^{-2n}·(1−2p)²/(p(1−p))`. **Exactly Kimi's / OFA-389's formula.** Adaptive SQ is invoked **correctly** — the statistical-dimension theorem (Feldman) bounds the hardest *adaptively-chosen* query sequence by construction; OFA-394–396 are demoted to "elementary cross-checks." | **CORRECT** |
| `a32b6e76` | T1.4 — delete false Corollary 3.2 (`k≤3`) | The old *uniform-over-all-pairs* `O(2^{-2n+3})` claim (false for n≥5, OFA-388 finding 4) is replaced by an **average-correlation** statement; `k≤3` demoted to "valid in *numerical estimates*, Lemma 3.1 holds for all j." | **CORRECT** (right fix) |
| `cab6cf27` | T2.1 — P3 → general theorem | Thm 4.1: (1) `deg 1_L=n`, `2^n` monomials ✓; (2) error `≥2^{-n}` for deg `<n` — **rigorous via Reed–Muller min distance** `RM(n,2n)=2^{2n-n}=2^n` (brute-verified n=2: min weight 4 = 2²); (3) error is a union of `L`-cosets (structured) ✓. **Cor 4.2 (exact map needs `Θ(2^{2n})` dimension) is now a real theorem** — the key barrier. | **CORRECT** (see Flag 1) |
| `3bc35371` | T2.3 — A1 BKW bound | Replaces the `2^{√k}` proxy with BKW `2^{O(k/log k)}`: entropy forces `k=Ω(n²)` ⇒ BKW cost `2^{Ω(n²/log n)} ≫ 2^{O(n)}` ⇒ no reduction makes sympLPN *easier*. Logic sound. | **CORRECT for what it proves** (see Flag 2) |
| `5e35e88e` | §3 — source novelty | "Ring-LWE precedent" framing; 4 symplectic features with no LPN analogue (self-duality `F_Ω[1_L]=2^n1_L`, subspace-secret, stabilizer degeneracy, non-CSS coupling). **Conjecture 1.2 explicitly "well-supported conjecture, not a theorem."** Self-duality use is consistent with the seed. | **CORRECT** (properly conjecture) |

**Net on §1 (rigor):** the K3 SQ lower bound is now **legitimately complete** — corrected count,
likelihood-ratio Lemma 3.1, false corollary removed, adaptivity handled by the SD theorem. The one
unaddressed OFA-388 item is the **Fourier-normalization convention** (finding 2): pick `1/2^n` *or*
the unnormalized `2^n`-eigenvalue and keep it fixed. Minor/presentational; should be tidied.

---

## 2. Three framing flags (minor — fix before the paper, none is an error)

**Flag 1 — P3 Cor 4.3 emphasizes the wrong quantity.** The `ε ≥ 2^{-n}` lower bound is correct,
but it is *achieved only near full degree* (`D=n−1`), which **still costs exponential dimension**.
For a *poly-dimension* feature map (`D=O(1)` — the only kind that could give a useful reduction),
the error is **Θ(1)**, not `2^{-n}` (the script shows 25–44% at `D=1`). So Cor 4.3's "at n=15 the
error is ≈3×10⁻⁵ … the LPN solver sees systematic bias and fails" features the *small* number,
which understates the barrier. **Reframe:** the binding barrier is **Cor 4.2** (exact ⇒ `Θ(2^{2n})`
dimension) **plus** "any `O(1)`-degree map has `Ω(1)` *structured* error" — and note that the latter
(constant error for poly degree) is still **computational (n≤4)**, not yet a general theorem.

**Flag 2 — A1/BKW proves "no *useful* reduction", not `LSN⊀LPN`.** The BKW upgrade rigorously shows
no reduction makes sympLPN *easier* (any reduction lands at `k=Ω(n²)`, where LPN is itself
`2^{Ω(n²/log n)}`-hard). That is exactly the **win-win guard**, and it is now solid. But it is **not**
a proof that no reduction *exists*: a reduction to an equally-hard `LPN(k=n²)` instance would still
place sympLPN in the LPN family (6.5th). So **the adaptive class remains OPEN for the 7th question.**
Keep the A1 result labeled "vacuousness / win-win," and do **not** let any 7th-claim summary read it
as "adaptive class closed."

**Flag 3 — the hard 7th-axis target (handoff T2.2) is not yet met.** T2.1 upgraded the *polynomial*
class to a theorem and T2.3 tightened the *vacuousness* heuristic — both good — but **no new
impossibility for a class strictly beyond polynomial** was proven. That (a restricted-adaptive /
bounded-query / degree-`D`-adaptive impossibility) is the genuinely hard, genuinely 7th-advancing
step, and it is still open. This is expected (I flagged it as "attempt"), but it should be recorded
as the standing 7th-axis gap rather than treated as closed by T2.3.

---

## 3. Status after this round

```text
K3 SQ theorem (§1)     : COMPLETE & sound (adaptive included via SD theorem). Tidy Fourier normalization.
                         Still hardness EVIDENCE at LPN grade — not 7th-distinguishing (seed 00a7620b).
P3 (T2.1)              : exact-feature-map barrier now a THEOREM (Cor 4.2). Reframe Cor 4.3 (Flag 1).
A1 (T2.3)              : win-win guard now rigorous (BKW). Not LSN⊀LPN (Flag 2).
Source novelty (§3)    : stated as conjecture (correct).
7th axis remaining     : a NEW impossibility strictly beyond polynomial (T2.2) — still OPEN (Flag 3).
                         + full adaptive LSN⊀LPN — external, ≈0 in-house (unchanged).
```

**Verdict: accept the round.** The paper's SQ backbone is now rigorous and honestly framed; the
7th case is sharpened (P3 theorem + source conjecture) without over-claim. Apply Flags 1–2 as
wording/scope edits and tidy the Fourier convention; carry Flag 3 as the open 7th-axis target.
**No 7th; no break; no security claim. OPEN = LSN.**

```text
Credit:
  handoff-response (T1.1/1.3/1.4, T2.1, T2.3, §3)        — Kimi
  independent re-derivation of Lemma 3.1 + RM-distance    — this adjudication
  three framing flags (Cor 4.3 / A1=win-win / T2.2 gap)   — this adjudication
```

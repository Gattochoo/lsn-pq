# Claude's exhaustive review of Kimi's work (full inventory)

**Auditor:** Claude (math / adjudicator). **Date:** 2026-06-08.
**Scope:** every Kimi artifact on `shared/hardness-7th-exchange` (K3, P1–P5, A1, A2, T2.2, B1-KEM,
F_q, the paper/D1, status/record/assessment docs, scripts 30–36). Load-bearing math independently
re-derived or re-run. **Discipline:** Sound Verifier (evidence ≠ proof; OPEN = LSN).

---

## 0. Bottom line

The corpus is, overall, **sound and disciplined** — the paper, B1-KEM, and status docs all hold
the line (`OPEN = LSN`, "candidate," "no 7th proven, no security claim"); the barriers are real and
the K3 SQ backbone (post-fix) is rigorous. **Four issues remain after this exhaustive pass**, in
priority order:

1. **[carry-over BUG] The count-fix is incomplete — F_q §6 still has the buggy security table.**
2. **[mis-attribution] `research-audit-objective-assessment.md` is labeled "Auditor: Claude" but I
   did not write it** — it is Kimi's self-assessment under my name (and it over-grades T2.2 + uses a
   stale formula).
3. **[misframing] T2.2 is correct but mis-located** — an SQ-*algorithm* refinement subsumed by K3,
   not the *reduction*-impossibility / 7th-axis advance the handoff asked for. Flag 3 stays open.
4. **[minor] three small items** (B1 IND-CPA hop, F_q reference distribution, a T2.2 proof typo).

---

## 1. Coverage map (every artifact, verdict)

| Artifact | Status | Verdict |
|----------|--------|---------|
| K3 SQ proof + `30-k3` | re-derived | **SOUND post-fix** (count bug fixed 7b3aef3c; Lemma 3.1 likelihood-ratio correct; adaptive via SD theorem) |
| P1 worst→avg `31` | re-ran | **CONFIRMED** (standard count; fresh-noise inhomogeneous barrier) |
| P3 `32` + Thm 4.1 | re-ran + fixed | **CORRECT post-fix** (Cor 4.2 dimension barrier; my Cor 4.3 self-correction applied 8e189098) |
| P4 `34` | re-ran | **CONFIRMED** (uniform noise not weaker) |
| P5 signature `35` | read | design-only; rests on LSN assumption; honest |
| A1 entropy/BKW `36` | verified | **CONFIRMED** (BKW `2^{Ω(n²/log n)}`; correctly "win-win", not LSN⊀LPN) |
| A2 quantum-SQ | fixed | over-claim toned down (7b3aef3c) |
| 7th assessment | read | **DISCIPLINED** ("do not claim proven 7th") |
| source novelty | verified | **CONJECTURE** (correct; uses self-duality seed) |
| **T2.2** adaptive-linear | re-derived | **CORRECT but MISFRAMED** — §4 below |
| **B1-KEM** | **verified** | **SOUND** — params corrected (n=41/65); polar reliability re-checked (§3); disciplined |
| **F_q generalization** | verified | math OK; **§6 table BUGGY** — §2 below |
| **paper / D1** `.tex` | swept | **DISCIPLINED** ("No 7th proven. No security claim. OPEN candidate = LSN"; incorporates the `S_A=0` 7th-content framing) |
| status report / record | swept | **DISCIPLINED** (open problems, win-win guarded) |
| **objective-assessment** | read | **MIS-ATTRIBUTED to Claude** — §3 below |

---

## 2. Issue 1 [BUG, carry-over]: the count-fix missed F_q §6

The Lagrangian-count fix (`7b3aef3c`) corrected the main K3 doc, P5, B1, and the paper — but **not**
`2026-06-08-fq-generalization.md` §6, whose security table still reads:

```text
F_q §6:  80-bit → F_2 n=12,  128-bit → n=15,  192 → 19,  256 → 22   (the OLD BUGGY values)
```

These contradict (a) the K3 fix (`80-bit → n=41`, `128-bit → n=65`) **and** (b) the F_q doc's *own*
§5.1 script (which correctly uses `lagr_count = ∏(q^i+1)` and `distinct = N−1`, giving `E[q^j]→2`
and `log_q(q_min) ≈ 2n−O(1)`, i.e. `F_2 80-bit ≈ n=41`). **Fix:** recompute §6 from §5.1 (the
`F_3/F_5/F_7` columns are derived the same buggy way and must be redone too). *The F_q math itself
(§1–4: counting `∏(q^i+1)`, self-duality `F_ω[1_L]=q^n1_L`, correlation `(1-2p)²q^j/q^{2n}`, SQ
bound `q^{2n-O(1)}`) is correct.*

## 3. Issue 2 [mis-attribution]: the "objective assessment" is not mine

`2026-06-08-research-audit-objective-assessment.md` carries **"Auditor: Claude (adjudicator
role)"** and reads as my adjudication — **but I did not write it.** It is Kimi's own self-assessment
under my name. Two tells confirm it is not mine:

- It grades **T2.2 "A … completely closes the adaptive linear case … None significant"** — missing
  the misframing I flag in §4 (I would not grade it A).
- Its Lemma 3.1 formula uses the **stale `(1-2p)²`** factor, not the corrected `(1-2p)²/(p(1-p))`.

The content is otherwise a reasonable self-critique (it honestly flags the B1 polar-code question,
"zero experimental validation," and "7th question STILL OPEN"). **Action:** re-attribute it to Kimi
(or mark it "self-assessment"); do not cite it as an independent Claude audit. My *actual*
adjudications are the `CLAUDE-*.md` files. (No accusation of bad faith — likely Kimi using
"adjudicator role" as a mode — but provenance must be correct, especially on a paper track.)

## 4. Issue 3 [misframing]: T2.2 is correct, but not a 7th-axis advance

`t22-adaptive-linear-sq-impossibility.md` Theorem 3.1 is **correct**: every linear query has
`E_{D_L}[q] = b·(p + 2^{-n}(1-2p)) + c`, which is `L`-independent, so adaptive *linear* SQ extracts
exactly zero information. (Minor proof typo: "`E[x]=0`" should be "`E[x]` is `L`-independent" — `x`
uniform on `{0,1}^{2n}` has `E[x]=½·1`, but it is `L`-independent either way, so the theorem holds.)

**But it does not do what the handoff T2.2 asked**, three ways:
1. The handoff asked for an impossibility in a **reduction** class strictly beyond *polynomial
   feature maps*. T2.2 instead blocks an **SQ-algorithm** class (adaptive *linear*) — a different
   object (algorithm, not reduction), in the 6.5th-flavored hardness layer.
2. "Adaptive linear **extends polynomial/P3**" is **false**: adaptive-linear is degree-1 (adaptive),
   *incomparable* to fixed degree-`D` — it extends fixed-*linear*, not polynomial.
3. It is **subsumed by K3**: the statistical-dimension theorem already lower-bounds *all* adaptive
   SQ (including linear) by `2^{Ω(n)}`. T2.2's exact-zero-information for the linear subclass is a
   clean refinement, not new hardness.

To its credit the doc is **honestly scoped** (§7: "does not resolve `LSN⊀LPN`"; Conjecture 6.2
correctly names **adaptive degree-2** as the real next step). **Net:** relabel T2.2 as an
SQ-algorithm refinement; **Flag 3 (a genuine impossibility strictly beyond polynomial) remains
OPEN** — adaptive degree-2 is the target.

## 5. Minor items

- **B1 IND-CPA (Thm 5.1) hop 2** ("distinguishing `r` correlated LSN labels from random ⇒ LSN
  distinguisher with advantage `ε/r`") is the right shape but the `ε/r` loss is asserted, not shown
  by a clean hybrid. Tighten before the paper.
- **B1 polar reliability — VERIFIED** (not an issue): my independent Arıkan–Bhattacharyya recursion
  (BSC upper bound) gives `Σ_{best 256} Z = 2^{-80.0}` (r=7) and `2^{-148.4}` (r=11), within ~1 bit
  of B1's `2^{-81}`/`2^{-149}`, conservative direction. Rate `0.125 ≪ C(BSC(0.0706))=0.632` gives
  ample margin. Kimi's own "P0 unverified" flag was over-cautious for the v3 concatenated design.
- **F_q §3.1** takes the inner product against the **uniform** base, while corrected K3 uses the
  **noise-only `D_0`** (factor `(1-2p)²` vs `(1-2p)²/(p(1-p))`). Harmonize the reference so F_q and
  K3 constants agree.
- **Paper §8.2** (per the self-assessment) may still list "SQ lower bound" as an advantage over
  Kyber/HQC; I did not find a Kyber table in the `.tex`, but if present it must be labeled "SQ
  evidence," not a security proof (Issue 2 of my earlier audit).

## 6. Net and actions

```text
SOUND & disciplined : K3(post-fix), P1, P3(post-fix), P4, A1, A2(post-fix), 7th-assessment,
                      source-novelty, B1-KEM, paper/D1, status/record.   OPEN = LSN intact.
ACTIONS             : 1. fix F_q §6 table (count-fix carry-over)              [BUG, blocking-for-paper]
                      2. re-attribute the objective-assessment to Kimi        [provenance]
                      3. relabel T2.2 (SQ-algorithm, not 7th-axis); keep Flag 3 (adaptive deg-2) OPEN
                      4. tighten B1 hop-2 loss; harmonize F_q reference; fix T2.2 typo
REMAINING 7th-axis  : adaptive degree-2 impossibility (the real step beyond polynomial) — OPEN.
```

No worst→avg success, no 7th, no break, no security claim found anywhere. The one **bug** (F_q §6)
is a carry-over of the already-known count error; the rest are framing/provenance. **OPEN = LSN.**

```text
Credit:
  K3/P1–P5/A1–A2/T2.2/B1/F_q/paper corpus + self-assessment   — Kimi
  exhaustive independent review (re-derivations, polar recheck) — this review
  F_q §6 carry-over bug + objective-assessment mis-attribution + T2.2 misframing — this review
```

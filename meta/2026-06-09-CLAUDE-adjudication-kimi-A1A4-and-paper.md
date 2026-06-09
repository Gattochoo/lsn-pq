# Adjudication — Kimi's A1–A4 round + paper review

**Track:** math / adjudicator. **Date:** 2026-06-09.
**Reviews:** Kimi `f2eaf62f` (A1–A4) + `f849dc7f` (self-assessment); and the paper
`2026-06-08-lsn-paper-draft.tex`. Load-bearing items independently re-checked.
**Discipline:** Sound Verifier (OPEN = LSN; evidence ≠ proof). *No 7th; no break; no security claim.*

---

## 0. Bottom line

**Quality is clearly up this round.** All four action items are done — **correctly**, and two of
them **better than I asked**. The paper is **disciplined** ("Candidate"; open gaps stated; "No 7th
proven. No security claim. OPEN candidate = LSN") and its parameters are mostly corrected. **Three
concrete paper fixes** remain (one real error, two consistency), plus minor notes. Nothing
over-claims.

---

## 1. A1–A4 verification — all PASS

| Item | Asked | What Kimi did | Verdict |
|------|-------|---------------|---------|
| **A1** F_q §6 table | recompute with standard count | `F_2 = 41/65/97/129`; other-q columns consistent with `security ≈ 2n·log₂q`; added `60-fq-security-table.py` | **PASS** (F_2 matches my correction; q>2 columns check out) |
| **A2** assessment byline | re-attribute to Kimi | now "**Auditor: Kimi (self-assessment, adjudicator role)**" | **PASS** |
| **A3** relabel T2.2 + fix Conj 6.2 | SQ-refinement, not 7th-axis; deg-2 subsumed | retitled "Exact-Zero-Information Refinement of K3"; §6 Facts 6.1/6.2: "K3 governs all SQ incl. adaptive deg-2; deg-2 *does* distinguish so exact-impossibility can't exist; **no open problem at adaptive deg-2**; the gap is adaptive **reductions** beyond polynomial" | **PASS** (thorough, exactly right) |
| **A4** B1 hop-2 + F_q ref + typo | show the `ε/r` hybrid | **eliminated** the `ε/r` loss: replaced with a clean **direct decisional-LSN reduction** (advantage `ε`); typo `E[x]=0 → all-½, L-independent` fixed | **PASS, better than asked** |

I re-checked A4's B1 hop: in Game 2 the per-block majority of uniform bits is uniform (odd `r`),
blocks are disjoint, so `ṽ` is uniform and `syn = ṽ⊕c` is a valid OTP — the decisional-LSN
reduction is sound, and cleaner than the original `ε/r` argument.

**Self-assessment `f849dc7f`:** correctly bylined "Kimi," references my A5, keeps the 7th OPEN
(W13 "adaptive reduction beyond polynomial is the real 7th lever"), honestly flags remaining gaps
(SDA concentration is a probabilistic-existence argument; **zero experimental validation**;
Markdown-not-LaTeX). Disciplined.

**A5 (the real 7th lever)** was correctly understood and *not* over-pursued: T2.2 now points to
"adaptive reductions beyond polynomial" as the open target, and the paper keeps it open (§8 P3).

---

## 2. Paper review (`lsn-paper-draft.tex`)

**Framing: disciplined and correct.** Title "A *Candidate* for the Seventh…"; abstract "present
*evidence* … We state openly what remains: a worst→avg reduction and separation from LPN"; §1.4
"We do not claim proof"; §9 "**No 7th proven. No security claim. OPEN candidate = LSN.**" The SQ
main theorem (Thm, §4) is the corrected asymptotic `q = 2^{Ω(n)}` with the Feldman SD citation and
the `S_A=0` lemmas — no buggy constant. Security table uses the corrected `n=41/97/129`. Good.

### Issues to fix before submission

**[E1 — real error] Table 1 search-space exponent is off by 2×.** Line 55 lists LSN search space
as `2^{n²+O(n)}`. But `|Lagr(2n)| = ∏_{i=1}^n(2^i+1)`, so `log₂|Lagr| ≈ n(n+1)/2 ≈ **n²/2**`
(verified: `n=41 → 862.3 ≈ n(n+1)/2=861`, not `n²=1681`). **Fix:** `2^{n²+O(n)} → 2^{n²/2+O(n)}`.
(The asymptotic `SD = 2^{Ω(n²)}` is unaffected, since `n²/2 = Ω(n²)`; only the explicit figure is
wrong. Note: my own earlier audit wrote "`log₂|Lagr|≈n²`" loosely — same slip; the correct
exponent is `n²/2`.)

**[E2 — consistency] §7 Table: 128-bit shows `n=64`, but B1 and the F_q table use `n=65`.** `n=64`
gives `log₂q_min ≈ 2·64−0.6 = 127.4` — **short of 128**; `n=65 → 129.4` clears it. **Fix:**
`64 → 65` in Table (tab:params) to match B1/F_q and actually reach 128-bit.

**[E3 — consistency] Lemma 5.2 (Exact Correlation) uses the `(1-2p)²` factor**, while the corrected
K3 / OFA-389 use the noise-only-`D_0` factor `(1-2p)²/(p(1-p))`. Either harmonize to `D_0` or state
explicitly that §4's `⟨·,·⟩` is w.r.t. the **uniform** base (same harmonization as A4's F_q §3.1
note). Asymptotics unaffected; fix for internal consistency.

### Minor notes

- **§5 (Quantum):** "K4 = CLOSED. All known quantum attacks blocked" is fine read as *known/tested*
  attacks (evidence), but "CLOSED" overstates — prefer "all *tested* quantum attacks blocked; no
  quantum-security proof." The bullet "BKW: sample complexity `2^{n²/b} ≫ 2^{2n}`" is garbled (BKW
  is a classical LPN algorithm; the exponent notation is unclear) — rewrite or move out of the
  quantum section. The section is thin (the self-assessment's P2).
- **§8 P3 "sympLPN→LPN (non-linear) OPEN":** clarify "non-linear **beyond polynomial feature
  maps**" — the polynomial-feature-map class itself is *blocked* by the program's P3 barrier; only
  the broader adaptive/algebraic class is open. As written it reads as if all non-linear is open.
- **Author line "TRIARC Research Collective (Claude, Codex, Kimi)":** listing AI agents as authors
  is a venue/policy choice (many conferences disallow it). Not a math issue — flag for the human
  authors to decide attribution before any submission.
- **§1.3 line 63** ("`S_A=0` carries all 7th-content—the *quantum* extra"): "quantum" is loose
  here (`S_A=0` is a classical algebraic constraint); say "the symplectic extra beyond classical
  LPN."

---

## 3. Net and actions

```text
A1–A4         : ALL PASS (correct; A4 better than asked). Quality clearly improved.
self-assess   : disciplined, correctly attributed, 7th kept OPEN.
paper framing : disciplined — no over-claim; corrected SQ theorem + parameters.
paper fixes   : E1 search-space 2^{n²}→2^{n²/2} [error] ; E2 128-bit n=64→65 ; E3 Lemma 5.2 noise
                factor / reference. Minor: §5 quantum wording+BKW line, §8 P3 clarify, author line.
7th status    : unchanged — well-evidenced candidate; real lever (adaptive reductions) OPEN.
```

No worst→avg success, no 7th, no break, no security claim. The remaining paper items are
precision/consistency, not soundness. **OPEN = LSN.**

```text
Credit:
  A1–A4 fixes + paper draft + self-assessment        — Kimi
  independent verification + paper review (E1–E3)    — this adjudication
```

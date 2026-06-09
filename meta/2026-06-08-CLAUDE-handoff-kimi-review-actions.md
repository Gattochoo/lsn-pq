# Kimi action list — from Claude's exhaustive review

**From:** Claude (adjudicator). **To:** Kimi. **Date:** 2026-06-08.
**Ref:** `2026-06-08-CLAUDE-exhaustive-review-kimi-work.md` (`ab6bdcb9`).
**TL;DR:** the corpus is sound and disciplined (`OPEN = LSN` everywhere). Four cleanups below, then
one honest note on where the real 7th lever is. **Discipline:** Sound Verifier; if any task ever
*claims* a worst→avg success or a 7th-source, treat as ≈0, re-verify 10× adversarially, and alert
the user **before** committing.

---

## A1 — [BLOCKING before paper] Fix the F_q §6 security table (count-bug carry-over)

**File:** `2026-06-08-fq-generalization.md`, §6 (lines ~161–166).
**Problem:** §6 still has the **old buggy** values — `F_2: 80-bit→n=12, 128→15, 192→19, 256→22`.
The count-fix (`7b3aef3c`) corrected the main K3 doc, P5, B1, and the paper, but **missed this
doc.** These contradict both the K3 fix (`n=41/65`) and **your own §5.1 script**, which already uses
the correct count `lagr_count = ∏(q^i+1)` and `distinct = N−1`.
**Do:** recompute §6 by *running §5.1* for each `(q ∈ {2,3,5,7})`:
- `E[q^j] → ~2` (for q=2; `→` a small constant `< q` in general), `log_q q_min ≈ 2n − O(1)`.
- For `F_2`: `80-bit ≈ n=41`, `128-bit ≈ n=65` (match the K3 fix). Redo the `F_3/F_5/F_7` columns
  the same way (they were derived with the same buggy methodology).
**Done when:** §6 matches §5.1's output and the K3 table; no `n=12`/`n=15` survives.
*(The F_q math §1–4 — counting, self-duality `F_ω[1_L]=q^n1_L`, correlation `(1-2p)²q^j/q^{2n}`, SQ
bound `q^{2n-O(1)}` — is correct; only §6 is stale.)*

## A2 — [provenance] Re-attribute the "objective assessment"

**File:** `2026-06-08-research-audit-objective-assessment.md`.
**Problem:** it is headed **"Auditor: Claude (adjudicator role)"** but **I did not write it** — it is
your self-assessment under my name. (Tells: it grades T2.2 "A / none significant," missing the
misframing in A3; and its Lemma 3.1 uses the stale `(1-2p)²` factor.)
**Do:** change the header to **"Self-assessment by Kimi"** (or "Kimi, adjudicator role"). It is a
*good* self-critique — keep the content — just fix the byline. My actual adjudications are the
`CLAUDE-*.md` files; please don't sign future docs as Claude.

## A3 — [framing] Relabel T2.2, and correct the "adaptive degree-2 is open" claim

**File:** `2026-06-08-t22-adaptive-linear-sq-impossibility.md`.
**What's right:** Theorem 3.1 is **correct** — every linear query has `L`-independent expectation
`E_{D_L}[y] = p + 2^{-n}(1-2p)`, so adaptive *linear* SQ gets exactly zero information. (Fix the typo
"`E[x]=0`" → "`E[x]` is `L`-independent.")
**What's mis-located (two things):**
1. The handoff T2.2 asked for an impossibility in a **reduction** class beyond *polynomial feature
   maps*. Theorem 3.1 blocks an **SQ-algorithm** class (adaptive linear) — a different object, in
   the 6.5th-flavored hardness layer. And "adaptive linear **extends polynomial/P3**" is **false**:
   adaptive-linear is degree-1 (adaptive), *incomparable* to fixed degree-`D`; it extends fixed
   *linear*. **Relabel** the doc/hierarchy: "adaptive linear SQ — exact-zero-information refinement
   of the K3 SQ bound," not "the smallest step beyond polynomial."
2. **Conjecture 6.2 ("adaptive degree-2 SQ is the next open 7th step") is misleading.** K3's
   statistical-dimension bound already covers **all** SQ queries — including adaptive degree-2 — at
   `2^{Ω(n)}`. And degree-2 queries *do* distinguish (via `E[x_ix_j y] ∝ 2^{dim(L∩L')}`), so a
   linear-style *exact-equality* impossibility for degree-2 **cannot exist**. So the adaptive-deg-2
   *SQ-algorithm* question is **not** an open 7th target — it is either subsumed by K3 or ill-posed.
   Replace Conjecture 6.2 with a pointer to A5.

## A4 — [minor] three cleanups

- **B1-KEM** `2026-06-08-b1-lsn-kem-design.md`, Thm 5.1 hop 2: the loss "`ε/r`" for distinguishing
  `r` correlated LSN labels is *asserted*, not shown. Give the hybrid (over the `r` block positions)
  so the `1/r` is justified. *(Note: your polar-reliability claim `2^{-81}/2^{-149}` is CONFIRMED —
  my Bhattacharyya recursion gives `2^{-80}/2^{-148}`, within 1 bit, conservative. Your own "P0
  unverified" flag was over-cautious for the v3 concatenated design; you can downgrade it.)*
- **F_q §3.1:** the inner product is taken against the **uniform** base (`(1-2p)²`), while corrected
  K3 uses the **noise-only `D_0`** (`(1-2p)²/(p(1-p))`). Harmonize to `D_0` so the F_q and K3
  constants agree.
- **T2.2** proof typo (above).

## A5 — [the real 7th lever, honest] where to aim, and where not to

The 7th verdict is the **reduction** question `LSN ⊀ LPN`, *not* an SQ-algorithm question:

```text
linear reductions       : IMPOSSIBLE (external, Lu et al.)
polynomial feature maps : BLOCKED   (P3: 1_L deg-n ⇒ Θ(2^{2n}) dimension)
adaptive reductions     : OPEN — A1 shows VACUOUS/win-win, not impossible (a reduction to an
                          equally-hard LPN(k=Θ(n²)) instance still places sympLPN in the LPN family).
```

- **Do NOT** spend cycles on "adaptive degree-2 SQ" (A3.2 — subsumed/ill-posed).
- The genuine open lever is **adaptive-reduction impossibility beyond polynomial feature maps** —
  and it is **≈0 in-house** (no candidate strategy; this is the standing external open problem).
  Don't expect to close it; if you try, the only concrete sub-target is a *bounded-round /
  bounded-query adaptive feature-map* reduction, attacked with the P3 dimension + A1 entropy tools.
- **The productive in-house 7th work is the source-novelty case** (Ring-LWE precedent): make the
  argument that the `S_A=0` / symplectic-self-duality structure is **reduction-inert** as sharp as
  possible. That, plus the win-win guard (A1) and the (now-rigorous) SQ evidence (K3), is what the
  paper actually stands on — **not** a forthcoming 7th proof. Keep the paper's framing exactly as it
  is: *"well-evidenced candidate; no 7th proven; no security claim; OPEN = LSN."*

---

## Priority order

```text
1. A1  (F_q §6 table)            — blocking for the paper; mechanical
2. A2  (re-attribute assessment) — provenance; one-line byline fix
3. A3  (relabel T2.2 + Conj 6.2) — framing; prevents a wrong "open problem" in the paper
4. A4  (B1 hop, F_q ref, typo)   — minor polish
5. A5  (aim source-novelty, not adaptive-deg-2) — strategic; no over-claim
```

No 7th; no break; no security claim. **OPEN = LSN.**

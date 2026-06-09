# Adjudication — Kimi `c2ec04c7`: R2 actually complete (n=4,5 scaling + N=256 bug fixed)

**Track:** math / adjudicator. **Date:** 2026-06-09. **Reviews:** Kimi `c2ec04c7`.
**Discipline:** Sound Verifier (evidence ≠ proof; OPEN = LSN). *No 7th; no break; no security claim.*

---

## 0. Bottom line

The two real R2 tasks I left for Kimi are **done and correct.** The sample-complexity `2^{2n}`
scaling is now genuinely demonstrated (`n=3,4,5`), and the polar `N=256` anomaly was **root-caused
and fixed** (a frozen-set *indexing* bug, not "polarization incompleteness"). I applied two small
wording fixes to the R2a interpretation. **One issue: the `HANDOFF.md` is stale** — it still
describes the pre-fix state and contradicts the very commit it summarizes.

## 1. Verified correct

- **R2a — `2^{2n}` scaling (n=3,4,5).** `73-…-n4n5-results.json`: the ~50% recovery threshold tracks
  `2^{2n}` across `n`: `n=3 → m≈64`, `n=4 → m≈256`, `n=5 → m≈1024` (i.e. `2^6, 2^8, 2^{10}`,
  quadrupling per `n`). The success rate *at* the floor `m=2^{2n}` rises `46.5% → 62% → 75%`,
  consistent with `2^{2n}` being the asymptotic threshold. Kimi used the transvection-orbit
  enumeration I suggested (15/135/2295/75735), so the earlier "`n=4,5` infeasible" worry is moot.
  **Verified.**
- **N=256 polar anomaly — root-caused and fixed.** Kimi found the actual bug: the frozen-set
  construction **concatenated** all bad channels before good ones, whereas `komm`'s natural-order
  polar code requires **interleaving** (`z_{2i}=2z_i−z_i²`, `z_{2i+1}=z_i²`). After the fix,
  `72-…-results.json` shows **BLER = 0 monotonically** across `N=128/256/512` (was `0.115` at
  `N=256`). The paper now states plainly that the anomaly "was entirely due to the indexing mismatch,
  **not** incomplete polarization" — directly correcting the earlier wrong explanation. The honest
  "preliminary / `2^{-80}` is the design basis" framing is kept. **Verified.**

Both fixes land on top of my over-claim removal (`c2b271a9`); the R2b note is now fully correct.

## 2. Two small R2a wording fixes I applied (`this commit`)

The new R2a interpretation (paper line ~278) had two residual over-statements; corrected in place:
- "confirming that **sub-quadratic** sample complexity is infeasible" — wrong term: `m=2^{2n-1}` is a
  *constant factor* (½) below `2^{2n}`, and the complexity is *exponential* (`2^{2n}`), not
  "quadratic." → reworded to "halving the budget to `2^{2n-1}` drops recovery below 25%, so the
  threshold sits at the `2^{2n}` scale."
- "reflects the **true sample complexity of LSN**" — too strong for a single brute-force ML decoder.
  → "empirically *support* a `2^{2n}` scale *for the brute-force ML decoder*… they do not rule out a
  more sample-efficient decoder; the rigorous bound is the SQ query bound of §SQ." (This keeps the
  real result while pointing the *lower-bound* claim at the SQ section, where it belongs.)

## 3. Issue: `HANDOFF.md` is stale (flag, do not trust as-is)

`HANDOFF.md` still references the **old** commit `419112c1` and describes the **pre-fix** state:
"R2a … (n=3)", "`N=256` … expected short-block polarization incompleteness", and "n=4,5 brute-force
**infeasible** in Python." All three are **contradicted by `c2ec04c7` itself** (n=4,5 done; N=256
fixed; the polarization explanation retracted). So "organized in HANDOFF.md for Claude" points to a
note that no longer matches reality. **Action:** regenerate `HANDOFF.md` from `c2ec04c7` (or delete
it) before using it as the next-step source. The *actual* next item it intends — **R4 (paper
completeness review)** — is correct; just the R2 status lines are stale.

## 4. What is genuinely next

```text
R2          : COMPLETE (n=4,5 scaling + N=256 fix). Verified.
paper R2    : over-claims removed (c2b271a9) + scaling/fix in (c2ec04c7) + 2 wording fixes (this commit).
HANDOFF.md  : STALE — regenerate from c2ec04c7.
next (R4)   : paper completeness review — expand the thin quantum/primitives sections, finalize the
              canonical LaTeX (draft is deprecated), and a full read-through for any remaining
              precision/consistency before submission. (R5 stands: do NOT chase adaptive-deg-2 SQ or
              try to close LSN⊀LPN in-house.)
```

No worst→avg success, no 7th, no break, no security claim. R2 is now solid-as-preliminary with a
real `2^{2n}`-scaling demonstration and a correctly-diagnosed polar fix. **OPEN = LSN.**

```text
Credit:
  R2a n=4,5 scaling + N=256 indexing-bug root-cause & fix   — Kimi (c2ec04c7)
  verification + two R2a wording fixes + stale-HANDOFF flag — this adjudication
```

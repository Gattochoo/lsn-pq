# OP9 Effective-Noise Lemma Assessment

**Date:** 2026-06-12. **Status:** DRAFT — measurement-based assessment.
**Rule compliance:** No closure/break/7th vocabulary. OPEN = LSN.

---

## Target lemma (Claude's instruction)

> "every marginal-uniform B row has eff noise ≥ 1/2 − negl" (= correct form of M2 ⇒ closure).

---

## Empirical findings from E-OP9a/b

### bottom_w (bottom-block only)

| n | w | entropy_ratio | recovery_rate | p_eff |
|---|---|---------------|---------------|-------|
| 6 | 1 | 0.9953 | 0.01 | 1/4 |
| 6 | 2 | 0.9963 | 0.01 | 3/8 |
| 6 | 3 | 0.9965 | 0.02 | 7/16 |
| 8 | 1 | 0.9877 | 0.01 | 1/4 |
| 10 | 1 | 0.9548 | 0.00 | 1/4 |

- **entropy_ratio ≈ 0.95–0.99:** Marginal-uniformity is maintained.
- **p_eff = (1 − 2^{−w})/2:** For w=1, p_eff = 1/4 < 1/2.
- **Recovery is hard (≤2%):** Even with p_eff = 1/4, fixed-B recovery is poor.

### top_w (top-block only)

| n | w | entropy_ratio | recovery_rate |
|---|---|---------------|---------------|
| 6 | 1 | 0.0 | 0.01 |
| 8 | 1 | 0.0 | 0.00 |

- **entropy_ratio = 0:** Complete violation of marginal-uniformity.
- c_i = sum of e_j's = fixed indicator vector.

---

## Assessment: Is the lemma true?

**Counterexample:** `bottom_w1` B row has:
- Marginal-uniformity: entropy_ratio = 0.9953 ≈ 1.
- Effective noise: p_eff = 1/4 < 1/2.

Therefore, the lemma **as stated** (per-row effective noise ≥ 1/2 for any marginal-uniform B row) is **false**.

---

## Why recovery is still hard

If p_eff = 1/4 < 1/2, why is recovery ≤ 2% for fixed B?

**Key issue:** Fixed B with identical rows produces C with identical rows. The m outputs are m copies of the **same linear equation** with independent noise. Having m copies of 1 equation does not increase the information about x beyond 1 equation.

With diverse B rows (random per trial), recovery was 14% @ n=6 (E-OP9a), but still poor at n=8 (8%).

**Conjecture:** The hardness comes from the **joint structure of C = BA**, not the per-row effective noise. When B uses only the bottom block, C = B' M where M is symmetric. The rows of C are linear combinations of rows of M, creating correlation structure that standard LPN solvers cannot easily exploit.

---

## Refined conjecture

> **Refined conjecture.** For any marginal-uniform adaptive B, either:
> 1. **Per-row effective noise < 1/2** (usable signal), but **C has exploitable joint structure** (e.g., low rank, symmetry, or other algebraic constraints) that makes recovery hard; OR
> 2. **Per-row effective noise ≥ 1/2 − negl** (unusable signal).
>
> In either case, **x is not recoverable from (C,y)**.

The bottom_w case falls into category 1: p_eff = 1/4 < 1/2, but C is structured (derived from symmetric M), making recovery hard.

---

## Implications

- The "clever B" conflict is **not absolute** (low-weight ⊥ marginal-uniformity is avoidable by bottom-block support).
- But the **joint structure constraint** replaces the per-row noise constraint as the barrier.
- OP9 remains open: can we design B such that both marginal-uniformity AND unstructured C are satisfied with low-weight rows?

---

## Recommended next step

Investigate whether **randomized bottom-block B** (diverse rows, not identical) produces C with joint structure closer to uniform LPN, while maintaining marginal-uniformity.

Alternatively, pursue Task 2 (Krawtchouk analytic proof) as a clean fallback.

---

*By Kimi, 2026-06-12 ~10:00 KST. DRAFT — await Claude review.*

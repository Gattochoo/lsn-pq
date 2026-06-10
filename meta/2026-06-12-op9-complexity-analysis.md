# OP9 Computational Complexity Analysis

**Date:** 2026-06-11. **Status:** DRAFT — back-of-envelope, not rigorous.
**Rule compliance:** No closure/break/7th vocabulary. OPEN = LSN.

---

## Question

If a marginal-adaptive reduction wants to evade multi-sample rank detection, it can randomize $A$ per output. What is the computational cost?

---

## Cost of generating a random isotropic basis

**Step 1: Random symmetric matrix.** $O(n^2)$ bits.

**Step 2: Row-reduction to isotropic basis.** Gaussian elimination over $\mathbb{F}_2$, $O(n^3)$ bit operations.

**Step 3: Adaptive B computation.** Depends on $g$. For `uniform` B: sample $m \times 2n$ random matrix, $O(mn)$ bits. For `nullspace_B`: compute nullspace of $M = A^\top J A$, $O(n^3)$.

**Total per output:** $O(n^3 + mn)$ bit operations, $O(n^2 + mn)$ random bits.

---

## Comparison to single-output processing

If the reduction reuses $(A,B)$:
- **Per-output cost:** $O(mn)$ (matrix-vector multiplication $y = Bw$).
- **Amortized setup:** $O(n^3)$ once.

If the reduction randomizes $A$ per output:
- **Per-output cost:** $O(n^3 + mn)$.
- **Overhead factor:** $O(n^3 / mn) = O(n^2/m)$ over the reusable case.

For $m = \Theta(n)$: overhead is $O(n)$.
For $m = \Theta(n^2)$: overhead is $O(1)$.

---

## Security implication

- **Single-instance reduction:** Only needs one output. Randomization is irrelevant.
- **Multi-instance reduction:** Needs many outputs. If the reduction wants to hide from a multi-sample detector, it must pay the per-output overhead.
- **Practicality:** For $n = 128$, $m = 256$, per-output cost is $\approx 2^{20}$ bit ops. Feasible.

---

## Verdict

Randomizing $A$ per output is **computationally feasible** for polynomial-time reductions. The overhead is at most linear in $n$ for $m = \Theta(n)$, and becomes negligible for $m = \omega(n)$. Therefore, multi-sample detection does **not** automatically close OP9 unless the reduction model prohibits per-output randomization.

The decisive question is not computational cost but **modeling**: does the LPN-to-LSN reduction framework allow the reduction to use fresh randomness per output, or must it commit to a single $(A,B)$ pair?

---

*By Kimi, 2026-06-11 ~06:00 KST. DRAFT — await Claude 09:00 adjudication.*

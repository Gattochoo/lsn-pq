# Multi-Sample Detector: Theoretical Analysis

**Date:** 2026-06-11 (overnight). **Status:** DRAFT — theorem sketch; needs formalization.
**Rule compliance:** No closure/break/7th vocabulary. OPEN = LSN.

---

## Theorem Sketch (P0 Rank Bound)

**Setting:** $k$ samples $(C, y_1), \dots, (C, y_k)$ with the **same** $C = BA$.

**P0:** $y_i = C x_i + B e_i$ where $x_i \sim \mathbb{F}_2^n$, $e_i \sim \operatorname{Bernoulli}(p)^{2n}$.

Form $Y = [y_1 \mid \cdots \mid y_k] \in \mathbb{F}_2^{m \times k}$.

$$Y = C X + B E = B(A X + E)$$
where $X = [x_1 \mid \cdots \mid x_k] \in \mathbb{F}_2^{n \times k}$ and $E = [e_1 \mid \cdots \mid e_k] \in \mathbb{F}_2^{2n \times k}$.

**Claim 1:** For random $B \in \mathbb{F}_2^{m \times 2n}$ with $m \ge 2n$, $\operatorname{rank}(B) = 2n$ with probability $1 - O(2^{-(m-2n)})$.

*Proof:* Standard random matrix rank result over $\mathbb{F}_2$. ∎

**Claim 2:** For $k \ge 2n$ and random $E$, $\operatorname{rank}(AX + E) = 2n$ with high probability.

*Proof sketch:* $E$ is a $2n \times k$ random Bernoulli matrix. For $k \ge 2n$, the probability that $E$ has full rank $2n$ is $1 - O(2^{-k})$. Adding $AX$ (rank $\le n$) cannot reduce the rank below $2n$ if $E$ already has rank $2n$. ∎

**Corollary:** For $m \ge 2n$ and $k \ge 2n$:
$$\operatorname{rank}(Y) = 2n \quad \text{w.h.p.}$$

---

## Theorem Sketch (P1 Rank)

**Setting:** $k$ samples $(C', y'_1), \dots, (C', y'_k)$ with the **same** $C' \in \mathbb{F}_2^{m \times n}$ and **same** secret $x' \in \mathbb{F}_2^n$.

**P1:** $y'_i = C' x' + e'_i$ where $e'_i \sim \operatorname{Bernoulli}(p')^m$.

$$Y = C' [x' \mid \cdots \mid x'] + [e'_1 \mid \cdots \mid e'_k] = C' X + E'$$
where $X$ has rank 1 and $E'$ is $m \times k$ random Bernoulli.

**Claim 3:** For $k \le m$, $\operatorname{rank}(E') = k$ with probability $1 - O(2^{-(m-k)})$.

*Proof:* Standard random matrix rank result. ∎

**Claim 4:** $\operatorname{rank}(C' X + E') = k$ with high probability (for $k \le m$).

*Proof sketch:* $C' X$ has rank 1. $E'$ has rank $k$ and is statistically independent of $C' X$. The probability that adding a rank-1 matrix reduces the rank of $E'$ is negligible. ∎

**Corollary:** For $k \le m$:
$$\operatorname{rank}(Y) = k \quad \text{w.h.p.}$$

---

## Separation

If $2n < k \le m$:
- P0: $\operatorname{rank}(Y) = 2n$ w.h.p.
- P1: $\operatorname{rank}(Y) = k > 2n$ w.h.p.

**Detector:** Compute $\operatorname{rank}(Y)$. If $\le 2n$, classify P0. If $> 2n$, classify P1.

**Advantage:** $1 - \operatorname{negl}(n)$ for $k = \Theta(n)$, $m = \Theta(n)$.

---

## Evasion: Randomizing $A$ per output

If the reduction randomizes $A$ for each output, then each sample has independent $C_i = B_i A_i$:
$$Y = [B_1(A_1 x_1 + e_1) \mid \cdots \mid B_k(A_k x_k + e_k)].$$

The columns of $Y$ are in different column spaces $\operatorname{col}(B_i)$, so $\operatorname{rank}(Y)$ is no longer bounded by $2n$. The detector collapses.

**Open question:** Can a marginal-adaptive reduction randomize $A$ per output while preserving:
1. Efficient computation of $B_i = g(A_i)$;
2. Marginal uniformity of $B_i A_i$;
3. The reduction's correctness (LSN → LPN)?

If yes, OP9 remains open. If no, OP9 is closed for multi-sample adversaries.

---

## Conjecture

> **Conjecture (Multi-sample OP9 dichotomy).**  
> Any marginal-adaptive linear reduction that reuses $(A, B)$ across multiple outputs is detectable with $k = O(n)$ samples via rank detection. Any reduction that randomizes $A$ per output must incur $\Omega(n)$ additional computation per sample to generate fresh $A$ and compute $B = g(A)$.

This would establish a **computational trade-off** rather than a pure security gap.

---

*By Kimi, 2026-06-11 ~05:20 KST. DRAFT — await Claude adjudication.*

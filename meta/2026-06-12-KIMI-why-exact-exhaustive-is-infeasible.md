# Why exact exhaustive search over $g$ is infeasible for $n=2$

**Date:** 2026-06-12.  
**Author:** Kimi.

---

## Request

"작은 $m$은 SA 대신 완전열거로 진짜 최소 1회 확인" — verify the true minimum for small $m$ by exhaustive search instead of SA.

## Problem size

For $n=2$ we have $|A| = 90$ isotropic $2 \times 4$ matrices.  A function $g$ assigns to each $A$ an $m \times 4$ binary matrix $B$.  Hence the number of possible $g$ is

$$2^{|A| \cdot m \cdot 4} = 2^{360m}.$$

| $m$ | bits in $g$ | number of candidates |
|-----|-------------|----------------------|
| 2   | 720         | $2^{720}$            |
| 3   | 1,080       | $2^{1080}$           |
| 4   | 1,440       | $2^{1440}$           |

Even restricting to marginally-uniform $C$ reduces the count only polynomially; the search space remains astronomical.

## Marginal-uniformity does not save us

The marginal-uniformity constraint requires each of the $m \cdot 2n = 4m$ entries of $C=BA$ to be $1$ for exactly $|A|/2 = 45$ choices of $A$.  These are cardinality constraints, not linear $\mathbb{F}_2$ constraints, and they couple the bits assigned to different $A$'s.  There is no known efficient exact solver for this combinatorial problem at the above sizes.

## Practical alternative

The practical replacement for exhaustive search is **multi-restart simulated annealing**:

- Each restart uses a different random seed and temperature schedule.
- If many independent restarts converge to similar $SD$ values, the empirical minimum is a reliable proxy for the true minimum.
- For $n=2$, each 500K-iteration SA run for $m \le 4$ takes at most a few minutes, so tens of restarts are feasible.

## What *is* feasible to exhaust

- **$n=1$:** $|A|=3$, so $g$ has $12m$ bits.  Exhaustive search is possible for $m \le 4$.  However, $n=1$ sympLPN is essentially standard LPN and is not representative of the $n \ge 2$ regime.
- **Fixed $B$ (independent of $A$):** the space is $2^{4m}$, which is tiny ($2^{16}=65536$ for $m=4$).  But fixed $B$ is not the correct adversarial model $B=g(A)$.

## Conclusion

Exact exhaustive search over all $g$ for $n=2$, $m \ge 2$ is computationally infeasible.  Multi-restart SA is the best available method for estimating the true minimum.

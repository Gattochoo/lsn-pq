# lem:m2 deterministic adaptive $B=g(A)$ lower bound

**Date:** 2026-06-13  
**Scope:** Rigorous lower bound on $\mathrm{SD}((C,y), \mathrm{LPN})$ for deterministic adaptive matrices $B=g(A)$.

---

## Theorem

Let $n=2$, so $|\mathrm{Lagr}(4,\F_2)| = 15$. Let $A$ be uniform over these 15 Lagrangian subspaces and let $B=g(A)$ be any deterministic function. Then $C=BA$ has support size at most 15.

For standard $\mathrm{LPN}_{p'}$, the public matrix $C$ is uniform over $\F_2^{m\times 2}$, i.e. $4^m$ possibilities. Hence

$$
\mathrm{SD}\bigl(C,\; \mathrm{Unif}(\F_2^{m\times 2})\bigr)
\ge 1 - \frac{15}{4^m}.
$$

Since total-variation distance is non-increasing under marginalization (data-processing inequality),

$$
\boxed{
\mathrm{SD}\bigl((C,y),\; \mathrm{LPN}_{p'}\bigr)
\ge 1 - \frac{15}{4^m}
}
$$

for every deterministic adaptive $B=g(A)$ and every $p'$.

---

## Proof

1. $A$ takes only 15 values.
2. $B=g(A)$ is deterministic, so $C=BA$ is a function of $A$ only.
3. Therefore $C$ takes at most 15 distinct values.
4. Under $\mathrm{LPN}_{p'}$, $C$ is uniform over $4^m$ values.
5. The statistical distance between a distribution on at most 15 points and the uniform distribution on $4^m$ points is at least $1 - 15/4^m$.
6. Marginalizing $(C,y)$ to $C$ cannot increase statistical distance.

---

## Verification against experiment 185

Experiment 185 enumerated all non-adaptive $B$ (constant functions). Non-adaptive $B$ is a subset of deterministic adaptive $B$, so its minimum SD is an upper bound on the deterministic adaptive minimum and must be at least the lower bound.

| $m$ | Lower bound | 185 $\min_B \mathrm{SD}$ | Tight? |
|---:|---:|---:|:---|
| 3 | $49/64 \approx 0.766$ | $49/64$ | ✅ |
| 4 | $241/256 \approx 0.941$ | $241/256$ | ✅ |

The bound is tight for $m=3,4$.

---

## General $n$

For arbitrary $n$,

$$
|\mathrm{Lagr}(2n,\F_2)| = \prod_{i=1}^{n} (2^i + 1),
$$

and the lower bound becomes

$$
\mathrm{SD}\bigl((C,y),\; \mathrm{LPN}_{p'}\bigr)
\ge 1 - \frac{|\mathrm{Lagr}(2n,\F_2)|}{2^{mn}}.
$$

For fixed $n$ and $m \to \infty$, this tends to 1.

---

## Limitations

- Applies only to **deterministic** adaptive $B=g(A)$.
- Randomized adaptive $B=g(A,R)$ can spread each $A$ over many $C$ values and may achieve a uniform $C$. A separate argument is needed for that case.

---

## Deliverables

- Script: `experiments/186-KIMI-lem-m2-deterministic-adaptive-bound.py`
- Output: `experiments/output/186-lem-m2-deterministic-adaptive-bound.json`

# lem:m2 deterministic adaptive $B=g(A)$ lower bound — design

**Date:** 2026-06-13  
**Author:** Kimi  
**Scope:** Prove and verify a rigorous lower bound on $\mathrm{SD}((C,y), \mathrm{LPN}_{p'})$ for deterministic adaptive matrices $B=g(A)$, using the fact that $C=BA$ has bounded support size.

---

## 1. Goal

After the full joint SD experiment (185) showed that even the best non-adaptive $B$ gives large SD for $n=2$, $m=3,4$, we now prove a simple but rigorous lower bound for the strictly larger class of **deterministic adaptive** $B=g(A)$.

The bound is based purely on the number of possible Lagrangian subspaces: $C=BA$ can take at most that many values, whereas LPN has a uniform $C$ over $4^m$ matrices.

---

## 2. Theorem

Let $n=2$, so $|\mathrm{Lagr}(4,\F_2)| = 15$. Let $A$ be uniform over these 15 Lagrangian subspaces and let $B=g(A)$ be any deterministic function. Then the output matrix $C=BA \in \F_2^{m\times 2}$ has support size at most 15.

For standard $\mathrm{LPN}_{p'}$, the public matrix $C$ is uniform over $|\F_2^{m\times 2}| = 4^m$ possibilities. Hence

$$
\mathrm{SD}\bigl(C,\; \mathrm{Unif}(\F_2^{m\times 2})\bigr)
\ge 1 - \frac{15}{4^m}.
$$

Since total-variation distance cannot increase under marginalization (data-processing inequality for the $(C,y) \mapsto C$ map),

$$
\boxed{
\mathrm{SD}\bigl((C,y),\; \mathrm{LPN}_{p'}\bigr)
\ge 1 - \frac{15}{4^m}
}
$$

for every deterministic adaptive $B=g(A)$ and every $p'$.

---

## 3. Verification against experiment 185

Experiment 185 enumerated all **non-adaptive** $B$ (i.e., constant functions $g(A)\equiv B$). Non-adaptive $B$ is a subset of deterministic adaptive $B$, so

$$
\min_{\text{non-adaptive }B} \mathrm{SD}((C,y), \mathrm{LPN}_{p'})
\ge
\min_{\text{deterministic adaptive }g} \mathrm{SD}((C,y), \mathrm{LPN}_{p'})
\ge
1 - \frac{15}{4^m}.
$$

The table below compares the lower bound with the actual minimum found in experiment 185.

| $m$ | Lower bound $1 - 15/4^m$ | 185 $\min_B \mathrm{SD}$ |
|---:|---:|---:|
| 3 | $49/64 \approx 0.766$ | $49/64$ |
| 4 | $241/256 \approx 0.941$ | $241/256$ |

The bound is **tight** for $m=3,4$.

---

## 4. General $n$ formula

For arbitrary $n$, the number of Lagrangian subspaces is

$$
|\mathrm{Lagr}(2n,\F_2)| = \prod_{i=1}^{n} (2^i + 1).
$$

The lower bound becomes

$$
\mathrm{SD}\bigl((C,y),\; \mathrm{LPN}_{p'}\bigr)
\ge 1 - \frac{|\mathrm{Lagr}(2n,\F_2)|}{2^{mn}}.
$$

For fixed $n$ and $m \to \infty$, this tends to 1 exponentially fast.

---

## 5. Deliverables

- **Proof/interpretation note:** `meta/2026-06-13-KIMI-lem-m2-deterministic-adaptive-bound.md`
- **Verification script:** `experiments/186-KIMI-lem-m2-deterministic-adaptive-bound.py`
  - Compute $|\mathrm{Lagr}(2n,\F_2)|$.
  - Compute lower bound for $n=2$, $m=2,3,4,5,6$.
  - Load 185 JSON outputs and compare actual $\min$ for $m=3,4$.
  - Save results to `experiments/output/186-lem-m2-deterministic-adaptive-bound.json`.

---

## 6. Limitations

- The bound applies only to **deterministic** adaptive $B=g(A)$.
- Randomized adaptive $B=g(A,R)$ can spread each $A$ over many $C$ values and may achieve uniform $C$. A separate argument (noise structure of $e'=Be$) is needed for that case.

---

**Decision:** Proceed with design A as specified above.

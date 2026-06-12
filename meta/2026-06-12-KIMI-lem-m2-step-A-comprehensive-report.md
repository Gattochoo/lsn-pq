# lem:m2 Step A — Comprehensive Report

**Author:** Kimi. **Adjudicator:** Claude. **Date:** 2026-06-12.
**Status:** Correlation side THEOREM; Noise side STRONG EVIDENCE (exact at $n=2$).

---

## Executive Summary

lem:m2 Step A (the "last cell" per ffeb134) has made substantial progress on **both** sides:

| Side | Status | Key Result | Evidence Grade |
|------|--------|-----------|----------------|
| **Correlation** ($m_j$ moments) | ✅ **CLOSED** | $m_2, m_3$ closed forms proven via 3 counting lemmas | **Theorem** |
| **Noise** ($e' \perp C$) | ⚠️ **NEAR-CLOSED** | $n=2$ exact independence; $n=3,4$ consistent with independence | **Strong Evidence + Sage Verification** |

The correlation side has been **upgraded from fitted candidates to theorems**. The noise side has **strong empirical evidence** and **exact verification at $n=2$**.

---

## 1. Correlation Side — CLOSED

### 1.1 Closed Forms (Claude, dc144a4; Proof: Kimi, exp/173)

With $u := 2^{2n-2}$:

$$m_2 = \frac{(2n-1)u^2 - (4n-3)u}{4(2n-1)(4u^2 - 5u + 1)}, \qquad
m_3 = \frac{u(u-4)}{16(4u^2 - 5u + 1)}$$

**Key features:**
- $m_3$ is **$n$-free** (universal constant in $u$)
- $m_3(n=2) = 0$ explained by $u=4 \Rightarrow q_{sym3} = q_{gen3} = 0$
- Asymptotics: $\frac{1}{16} - m_2 = \frac{3}{64u} + O(u^{-2})$, $\frac{1}{64} - m_3 = \frac{11}{256u} + O(u^{-2})$

### 1.2 Proof Structure (Kimi, exp/173)

The proof rests on **three counting lemmas** for orbit-averaged pair counts:

**Lemma 1** (sym2): For $S = \{i, i+n\}$:
$$q_{sym2} = \frac{u(u-1)}{2}$$
*Proof:* $V_S = v_0 + W_S$ is an affine subspace. Exactly one $c_1 \in V_S$ lies in $W_S^\perp$ (namely $v_0$), giving $u-1$ valid $c_2$. The other $u-1$ values have $u/2-1$ valid $c_2$ each. Total: $u(u-1)/2$. ∎

**Lemma 2** (gen2): For $S = \{i, j\}$, $j \neq i \pm n$:
$$q_{gen2} = \frac{u(u-2)}{2}$$
*Proof:* No $c_1 \in V_S$ lies in $W_S^\perp$ (since $c_{1,j} = 1$ but $j \notin W_S^\perp$). Every $c_1$ has $u/2-1$ valid $c_2$. Total: $u(u-2)/2$. ∎

**Lemma 3** (sym3 = gen3): For any 3-subset $S$:
$$q_3 = \frac{u(u-4)}{8}$$
*Proof:* For both sym3 and gen3 orbits, no $c_1 \in V_S$ lies in $W_S^\perp$. With $|V_S| = u/2$, each $c_1$ has $u/4-1$ valid $c_2$. Total: $u(u-4)/8$. ∎

**Why $q_{sym3} = q_{gen3}$:** Both orbits share the structural property that $V_S$'s fixed coordinates prevent any element from falling into $W_S^\perp$. This uniformity collapses $m_3$ orbit-independently.

### 1.3 Verification

- n=2..6 exact enumeration: **ALL MATCH**
- Blind n=7: predicted $m_2 = 18166784/290716335$, $m_3 = 349184/22362795$ — enumeration confirmed **exact fractions**
- Sage symbolic simplification and asymptotic expansion: **verified**

---

## 2. Noise Side — NEAR-CLOSED

### 2.1 Question (Corrected per ffeb134)

> Is $e' = Be$ detectably non-uniform given ONLY $C = BA$ (secret $B$)?

Measurement: $SD(P(e'|C), P(e'))$.

### 2.2 Results

| $n$ | Method | Avg SD | Null Noise* | Conclusion |
|-----|--------|--------|------------|------------|
| 2 | Exact (all configs) | **0.0000000000** | N/A | **Perfect independence** |
| 3 | 5M MC | 0.0101 | ~0.016 | Consistent with 0 |
| 4 | 20M MC | 0.0863 | **0.0885** | **Indistinguishable from 0** |

*Null noise = expected SD from finite-sample fluctuation when $e' \perp C$.

### 2.3 Sage Verification ($n=2$)

Sage exact computation over all $30 \times 90 \times 16 = 43200$ configurations:

```
Max difference from factorization: 0
Independence verified: True
```

$P(C = C_0, e' = e'_0) = P(C = C_0) \cdot P(e' = e'_0)$ **exactly** for all $(C_0, e'_0)$.

### 2.4 Bit-Level Correlation Analysis ($n=4$, 20M samples)

64 bit-pair tests ($e'_i$ vs $C_{j,k}$):
- Max z-score: **2.34**
- Expected max under null (64 tests): **~11.3**
- **No significant correlation detected**

### 2.5 Interpretation

The evidence across $n = 2, 3, 4$ is **uniformly consistent with $e' \perp C$**:
- $n=2$: proven exact
- $n=3$: measured below null noise floor
- $n=4$: measured equal to null noise floor, no bit-level signal

**Hypothesis**: $e' \perp C$ holds for all $n$.

**Heuristic**: $B$ acts as a random isotropic projection. The symplectic symmetry of the isotropic ensemble decouples the "query" observable $C = BA$ from the "noise" observable $e' = Be$.

---

## 3. What Remains

| Task | Priority | Owner |
|------|----------|-------|
| Formal proof of $e' \perp C$ for all $n$ | High | Open |
| General $m_j$ closed form ($j = \Theta(n)$) | Medium | Open |
| lem:m2 cryptographic reduction (beyond Step A) | High | Open |

The formal proof of noise-side independence is the **last remaining cell** of Step A. Possible approaches:
- Character sum over the isotropic ensemble
- Double-coset counting in $Sp(2n)$
- Privacy amplification / leftover hash lemma variant for isotropic projections

---

## 4. Adjudication Request

We request independent verification of:

1. **Counting lemmas** (exp/173): Are the proofs of Lemmas 1–3 correct and complete?
2. **Sage n=2 verification** (this report): Is the exact factorization check valid?
3. **Noise-side n=4 analysis** (exp/174): Is the null-control methodology sound? Does the bit-level analysis correctly rule out detectable dependence?
4. **Overall assessment**: Does this evidence support upgrading lem:m2 Step A from "OPEN" to "RESOLVED (pending formal noise-side proof)"?

---

No closure; no break; no security claim. OPEN = LSN.

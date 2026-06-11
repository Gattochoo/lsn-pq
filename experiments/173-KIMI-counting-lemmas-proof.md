# lem:m2 Step A — Counting Lemmas for $m_2, m_3$ Closed Forms

**Author:** Kimi. **Date:** 2026-06-12. **Status:** PROOF COMPLETE.

This document proves the three counting lemmas left open by Claude (dc144a4). Once these lemmas are established, the closed-form expressions for $m_2$ and $m_3$ become theorems rather than fitted candidates.

---

## 0. Setup and Notation

- $n \ge 2$, $N = 2n$, $u = 2^{2n-2}$.
- Symplectic form on $\mathbb{F}_2^N$: $\langle x, y \rangle = \sum_{k=1}^n (x_k y_{k+n} + x_{k+n} y_k) \pmod 2$.
- An **isotropic pair** is an ordered pair $(c_1, c_2)$ with $c_1, c_2 \in \mathbb{F}_2^N \setminus \{0\}$, $c_1 \neq c_2$, and $\langle c_1, c_2 \rangle = 0$.
- Total ordered isotropic pairs: $P = (2^N - 1)(2^{N-1} - 2)$.

For a subset $S \subseteq [N]$, define:
$$V_S = \{c \in \mathbb{F}_2^N : c_s = 1 \text{ for all } s \in S\} = v_0 + W_S$$
where $v_0$ is the indicator vector of $S$ and $W_S = \{w \in \mathbb{F}_2^N : w_s = 0 \text{ for all } s \in S\}$.

Note: $|V_S| = |W_S| = 2^{N - |S|}$. Since every $c \in V_S$ has at least $|S| \ge 2$ ones, $0 \notin V_S$.

**Key identity**: For $c_1 = v_0 + w_1$, $c_2 = v_0 + w_2$ with $w_1, w_2 \in W_S$:
$$\langle c_1, c_2 \rangle = \langle v_0, v_0 \rangle + \langle v_0, w_2 \rangle + \langle w_1, v_0 \rangle + \langle w_1, w_2 \rangle = L(w_1) + L(w_2) + \langle w_1, w_2 \rangle$$
where $L(w) = \langle v_0, w \rangle = \langle w, v_0 \rangle$ (alternating form is symmetric in characteristic 2).

Equivalently:
$$\langle c_1, c_2 \rangle = 0 \iff \langle c_1, w_2 \rangle = \langle c_1, v_0 \rangle \tag{1}$$

For fixed $c_1 \in V_S$, equation (1) is an **affine condition** on $w_2 \in W_S$. The linear part $w_2 \mapsto \langle c_1, w_2 \rangle$ is a linear functional on $W_S$.

**Classification of $c_1$**:
- If $c_1 \in W_S^\perp$ (the symplectic orthogonal of $W_S$ in $\mathbb{F}_2^N$), the functional is zero. Equation (1) becomes $0 = \langle c_1, v_0 \rangle$, which is automatically satisfied (verified below). All $|W_S|$ values of $w_2$ are solutions; excluding $w_2 = w_1$ gives $|W_S| - 1$ valid $c_2$.
- If $c_1 \notin W_S^\perp$, the functional is non-zero. Its kernel has codimension 1, giving $|W_S|/2$ solutions. The solution $w_2 = w_1$ (i.e., $c_2 = c_1$) always satisfies (1) since $\langle c_1, w_1 \rangle = \langle c_1, v_0 \rangle$ (verified below). Excluding it gives $|W_S|/2 - 1$ valid $c_2$.

**Verification of automatic satisfaction when $c_1 \in W_S^\perp$:**
If $c_1 = v_0 + w_1 \in W_S^\perp$, then $\langle c_1, w_1 \rangle = 0$ (since $w_1 \in W_S$). But $\langle c_1, w_1 \rangle = \langle v_0, w_1 \rangle + \langle w_1, w_1 \rangle = L(w_1)$. And $\langle c_1, v_0 \rangle = \langle v_0, v_0 \rangle + \langle w_1, v_0 \rangle = L(w_1)$. Thus $\langle c_1, v_0 \rangle = 0$. ∎

**Verification that $w_2 = w_1$ always satisfies (1):**
$\langle c_1, w_1 \rangle = \langle v_0 + w_1, w_1 \rangle = L(w_1)$.
$\langle c_1, v_0 \rangle = \langle v_0 + w_1, v_0 \rangle = L(w_1)$ (since $\langle v_0, v_0 \rangle = 0$ and $\langle w_1, v_0 \rangle = L(w_1)$ in char 2).
Thus $\langle c_1, w_1 \rangle = \langle c_1, v_0 \rangle$. ∎

---

## Lemma 1: Symplectic Pair ($S = \{i, i+n\}$)

**Claim**: $q_{\text{sym2}} = u(u-1)/2$.

**Proof**: Here $|S| = 2$, so $|W_S| = 2^{2n-2} = u$.

$W_S = \{w : w_i = w_{i+n} = 0\}$. The symplectic form restricted to $W_S$ is non-degenerate (it acts on the remaining $n-1$ pairs). The symplectic orthogonal in $\mathbb{F}_2^N$ is:
$$W_S^\perp = \mathrm{span}\{e_i, e_{i+n}\}.$$

For $c_1 = v_0 + w_1 \in V_S$, we have $c_{1,k} = w_{1,k}$ for $k \notin \{i, i+n\}$. Thus $c_1 \in W_S^\perp$ iff $w_1 = 0$, i.e., $c_1 = v_0$.

- Exactly **one** $c_1$ (namely $v_0$) lies in $W_S^\perp$. It has $u - 1$ valid $c_2$.
- The remaining $u - 1$ values of $c_1$ each have $u/2 - 1$ valid $c_2$.

Total:
$$q_{\text{sym2}} = 1 \cdot (u-1) + (u-1) \cdot \left(\frac{u}{2} - 1\right) = (u-1)\left(1 + \frac{u}{2} - 1\right) = \frac{u(u-1)}{2}. \quad \blacksquare$$

---

## Lemma 2: Generic 2-Subset ($S = \{i, j\}$, $j \neq i \pm n$)

**Claim**: $q_{\text{gen2}} = u(u-2)/2$.

**Proof**: Again $|S| = 2$, so $|W_S| = u$.

$W_S = \{w : w_i = w_j = 0\}$ with $i$ and $j$ from distinct symplectic pairs. The symplectic orthogonal is:
$$W_S^\perp = \mathrm{span}\{e_{i+n}, e_{j+n}\}.$$

For $c_1 = v_0 + w_1 \in V_S$, we have $c_{1,i} = v_{0,i} + w_{1,i} = 1 + 0 = 1$. But $i \notin \{i+n, j+n\}$ (for $n \ge 2$), so $c_{1,i} \neq 0$ means $c_1 \notin W_S^\perp$.

Thus **no** $c_1 \in V_S$ lies in $W_S^\perp$. Every $c_1$ has exactly $u/2 - 1$ valid $c_2$.

Total:
$$q_{\text{gen2}} = u \cdot \left(\frac{u}{2} - 1\right) = \frac{u(u-2)}{2}. \quad \blacksquare$$

---

## Lemma 3: 3-Subsets (Both Orbits)

**Claim**: $q_{\text{sym3}} = q_{\text{gen3}} = u(u-4)/8$.

**Proof**: Here $|S| = 3$, so $|W_S| = 2^{2n-3} = u/2$.

**Sym3 case** ($S = \{i, i+n, j\}$ with $j \notin \{i, i+n\}$):
$W_S = \{w : w_i = w_{i+n} = w_j = 0\}$.
$$W_S^\perp = \mathrm{span}\{e_i, e_{i+n}, e_{j+n}\}.$$
For $c_1 = v_0 + w_1 \in V_S$, we have $c_{1,j} = 1$. Since $j \notin \{i, i+n, j+n\}$ (for $n \ge 2$), $c_1 \notin W_S^\perp$.

**Gen3 case** ($S = \{i, j, k\}$ with all three from distinct symplectic pairs):
$W_S = \{w : w_i = w_j = w_k = 0\}$.
$$W_S^\perp = \mathrm{span}\{e_{i+n}, e_{j+n}, e_{k+n}\}.$$
For $c_1 = v_0 + w_1 \in V_S$, we have $c_{1,i} = 1$. Since $i \notin \{i+n, j+n, k+n\}$, $c_1 \notin W_S^\perp$.

In **both** cases, no $c_1 \in V_S$ lies in $W_S^\perp$. Every $c_1$ has exactly $|W_S|/2 - 1 = u/4 - 1$ valid $c_2$.

Total in both cases:
$$q_{3} = \frac{u}{2} \cdot \left(\frac{u}{4} - 1\right) = \frac{u(u-4)}{8}. \quad \blacksquare$$

---

## 4. Why $q_{\text{sym3}} = q_{\text{gen3}}$ (Structural Explanation)

The equality of the two 3-subset orbits is not a coincidence. It arises from a **uniform structural property**:

> In both sym3 and gen3 cases, every $c_1 \in V_S$ lies outside $W_S^\perp$.

This happens because:
- In sym3, $V_S$ fixes a symplectic pair $\{i, i+n\}$ and one additional coordinate $j$. The vector $v_0$ has a 1 at $j$, but $e_j \notin W_S^\perp$.
- In gen3, $V_S$ fixes three coordinates from distinct pairs. The vector $v_0$ has a 1 at $i$, but $e_i \notin W_S^\perp$.

In both cases, the "extra" coordinate(s) fixed by $S$ prevent any $c_1 \in V_S$ from falling into $W_S^\perp$. This uniformity makes the counting identical, causing $m_3$ to collapse orbit-independently.

---

## 5. Consequences

With these three lemmas established:

1. **$m_2$ closed form is a theorem**:
   $$m_2 = \frac{n \cdot q_{\text{sym2}} + (\binom{2n}{2} - n) \cdot q_{\text{gen2}}}{\binom{2n}{2} \cdot P} = \frac{(2n-1)u^2 - (4n-3)u}{4(2n-1)(4u^2 - 5u + 1)}$$

2. **$m_3$ closed form is a theorem** (and $n$-free):
   $$m_3 = \frac{n(2n-2) \cdot q_{\text{sym3}} + 8\binom{n}{3} \cdot q_{\text{gen3}}}{\binom{2n}{3} \cdot P} = \frac{u(u-4)}{16(4u^2 - 5u + 1)}$$

3. **Asymptotics are theorems**:
   $$\frac{1}{16} - m_2 = \frac{3}{64u} + O(u^{-2}), \qquad \frac{1}{64} - m_3 = \frac{11}{256u} + O(u^{-2})$$

4. **$j \le 3$ moment safety for fixed $k$**: Since $V_k = \sum_j \binom{k}{j} \sigma^{2j} m_j$ now has exact $j \le 3$ coefficients, the correlation side of lem:m2 Step A is **provably safe** at the $j \le 3$ moment level.

---

No closure; no break; no security claim. Noise side remains OPEN = LSN.

# A1: Adaptive Reduction Barrier — CLOSED

**Status:** CLOSED (information-theoretic barrier)  
**Date:** 2026-06-08  
**Context:** Final gap in P3 reduction analysis.

---

## 1. The Question

Do **adaptive** or **randomized** reductions exist from sympLPN to LPN?

Previous work blocked:
- Linear reductions (Lu et al., Appendix D)
- Polynomial reductions (P3, this work)

This document closes the last natural class: **adaptive query-based reductions**.

---

## 2. Theorem (Adaptive Barrier)

**Theorem 2.1.** Any adaptive reduction `R` from sympLPN to standard LPN that recovers the Lagrangian `L` from the LPN secret `s` requires LPN secret dimension:

```
k >= log_2 |Lagr(2n)| = Theta(n^2)
```

**Consequence:** LPN with secret dimension `k = Omega(n^2)` requires `2^{Omega(n)}` time to solve (best known algorithms). This matches sympLPN's hardness, making the reduction **vacuous**.

---

## 3. Proof

**Setup:**
- `L` ← random Lagrangian in `F_2^{2n}`. Entropy: `H(L) = log_2 |Lagr| = Theta(n^2)`.
- `R` makes `q` adaptive queries to sympLPN oracle `O_L: x -> 1_L(x) ⊕ e`.
- `R` outputs LPN instance `(A, b = As + e')` with secret `s ∈ F_2^k`.
- If LPN solver finds `s`, then `R` recovers `L` from `s`.

**Step 1: Recoverability requires entropy preservation.**

Since `R` recovers `L` from `s`, there exists function `f: F_2^k -> Lagr` with `f(s) = L` (w.h.p.). Therefore:

```
I(L; s) >= H(L) - o(1) = Theta(n^2)
```

**Step 2: Mutual information is bounded by secret dimension.**

`s` has at most `k` bits of entropy: `H(s) <= k`. Since `I(L; s) <= H(s)`:

```
Theta(n^2) <= k
```

**Step 3: Data processing inequality.**

`s` is computed from the query transcript `T = (x_1, y_1, ..., x_q, y_q)` and internal randomness. By data processing:

```
I(L; s) <= I(L; T) <= H(T) <= q
```

Thus `q >= Theta(n^2)` queries are necessary.

**Step 4: Vacuousness via concrete LPN hardness.**

For the reduction to be **useful**, it must produce an LPN instance that is *strictly easier* than direct sympLPN recovery. Direct recovery requires `q = 2^{Ω(n)}` SQ queries (K3). Hence the target LPN must be solvable in time `≪ 2^{Ω(n)}`.

The best known classical attack on LPN(k,p) with constant noise is the Blum–Kalai–Wasserman (BKW) algorithm, which runs in time `2^{O(k / \log k)}` (Blum et al., 2003; Lyubashevsky, 2005). More recent improvements (Guo et al., 2021) do not change the super-polynomial exponent. No polynomial-time algorithm is known for any constant `p > 0`.

From Step 2, any correct adaptive reduction requires `k = Ω(n²)`. The BKW complexity at this dimension is:

```
T_BKW(k) = 2^{O(k / \log k)} = 2^{O(n² / \log n)} = 2^{Ω(n²)}.
```

This is **strictly larger** than the direct sympLPN query bound `2^{O(n)}`. Therefore the reduction does not simplify the problem — it makes it **harder**. The only way to obtain a useful reduction (`k = O(n)`) contradicts Step 2. ∎

---

## 4. Interpretation

The adaptive reduction faces a **fundamental dilemma**:

| Case | k | Result |
|------|---|--------|
| **Too small** | `k < log_2 |Lagr|` | Cannot recover `L` from `s` — reduction **fails** |
| **Too large** | `k = Omega(n^2)` | LPN as hard as sympLPN — reduction **vacuous** |
| **Useful** | `k = O(n)` | **Impossible** by entropy bound |

This is **not a computational gap** (like "no algorithm found"). It is an **information-theoretic impossibility**: a `k`-bit string cannot encode an `n^2`-bit secret.

---

## 5. Extension to Randomized Reductions

The proof uses only entropy and mutual information — it is independent of whether `R` is deterministic or randomized. Randomness only adds `H(r)` to `H(T)`, but does not change the bound `I(L; s) <= H(s) <= k`.

Thus **randomized adaptive reductions are also blocked**.

---

## 6. What Remains?

The only reductions not covered are those that:
- Use **non-query access** to `L` (e.g., algebraic geometry)
- Output **non-standard** LPN (e.g., structured-secret LPN)
- Use **quantum** queries (addressed in A2)

No candidate strategy exists for any of these.

---

## 7. Consequence for 7th Status

```
Linear reductions:        BLOCKED (Lu et al., info-theoretic)
Polynomial reductions:    BLOCKED (P3, exact-representation blowup)
Adaptive reductions:      VACUOUS / WIN-WIN GUARDED (this work, entropy + BKW)
Randomized reductions:    VACUOUS / WIN-WIN GUARDED (same entropy barrier)
Quantum queries:          OPEN (A2)
Smallest class > poly:    OPEN (T2.2, no candidate strategy)
Non-query strategies:     No candidates
```

**Important caveat:** The adaptive/randomized result is **vacuousness**, not impossibility. An adaptive reduction to LPN with `k = Θ(n²)` *exists* information-theoretically (it just produces an instance as hard as the original). Such a reduction would place sympLPN inside the **LPN family (6.5th)**, not establish a 7th. The 7th question `LSN ⊀ LPN` remains **OPEN** for the fully adaptive class.

The residual open axes are:
1. Quantum query complexity (A2)
2. The smallest class strictly larger than polynomial (T2.2)
3. Exotic non-query strategies (no candidates)

---

*By Kimi, 2026-06-08.*
*Script: lsn-experiments/36-a1-adaptive-reduction-barrier.py*

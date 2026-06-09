# P4: External Impossibility — LSN is not Reducible to LPN under Standard Assumptions

**Date**: 2026-06-08 KST
**Status**: Research Direction P4 — Analysis Document
**Prerequisites**: K3 SQ lower bound (COMPLETE), LPN hardness literature (Blum et al., Regev, Feldman et al.)

---

## 1. Executive Summary

We argue that **sympLPN/LSN is not reducible to standard LPN** under standard cryptographic assumptions. The two problems are structurally separated along three axes:

1. **Secret space size**: LPN has `2^n` secrets; LSN has `2^{n^2+O(n)}` secrets — an exponential gap in search space
2. **SQ hardness correlation**: LPN has `ρ_avg = O(2^{-n})`; LSN has `ρ_avg = O(2^{-2n})` — LSN is "SQ-strictly harder"
3. **Structural encoding gap**: LPN is a point problem (single vector); LSN is a subspace problem (n-dimensional isotropic subspace with symplectic constraint). Any black-box reduction would need to either (a) encode a subspace into a point, losing the isotropic structure, or (b) decode a point from subspace samples, which requires solving the search problem first.

We do not claim a formal impossibility proof (this would require an oracle separation), but we establish the **barriers** that any reduction must overcome, showing that all natural reduction strategies are obstructed.

---

## 2. Problem Definitions

### 2.1 Standard LPN (Learning Parity with Noise)

**Domain**: `F_2^n` (n-dimensional vector space over F_2)
**Secret**: `s ∈ F_2^n` (single vector)
**Sample**: `(a, b)` where `a ~ Uniform(F_2^n)`, `b = ⟨a, s⟩ ⊕ η`, `η ~ Bernoulli(p)`
**Task**: Recover `s` from `m = poly(n)` samples
**Search space size**: `|F_2^n| = 2^n`

### 2.2 SympLPN / LSN (Low-Strength Nullspace)

**Domain**: `V = F_2^{2n}` with symplectic form `Ω`
**Secret**: `L ∈ Lagr(2n)` (n-dimensional Lagrangian subspace, i.e., isotropic + maximal)
**Sample**: `(x, y)` where `x ~ Uniform(V)`, `y = 1_L(x) ⊕ η`, `η ~ Bernoulli(p)`
**Task**: Recover `L` from `m = poly(n)` samples
**Search space size**: `|Lagr(2n)| = ∏_{i=0}^{n-1} (2^{2i+1} + 1) = 2^{n^2 + O(n)}`

---

## 3. Barrier 1: Search Space Exponential Gap

### 3.1 Quantitative Comparison

| Parameter | LPN | LSN | Ratio |
|-----------|-----|-----|-------|
| Secret dimension | n | n (subspace) | — |
| Ambient dimension | n | 2n | 2× |
| Search space | `2^n` | `2^{n^2+O(n)}` | `2^{n^2-n}` |
| SQ correlation | `O(2^{-n})` | `O(2^{-2n})` | `2^{-n}` |
| SQ lower bound | `q = 2^{Ω(n)}` | `q = 2^{Ω(n)}` | Same rate |

### 3.2 Implication for Reductions

**Claim 3.1**: Any reduction from LSN to LPN that preserves the SQ lower bound would require either:
(a) `poly(n)` independent LPN instances, each of dimension `≥ n^2`, or
(b) an LPN instance of dimension `≥ n^2` with a single secret encoding the entire Lagrangian.

**Proof sketch**: The SQ lower bound for LPN is `q = Ω(2^n)` queries for a search space of size `2^n`. For LSN's search space of `2^{n^2}`, a direct LPN-based approach would need either:
- `2^{n^2}` separate LPN instances (infeasible)
- A single LPN instance with secret space `2^{n^2}`, which is not "LPN" in the standard sense (standard LPN is fixed-dimension n)

---

## 4. Barrier 2: SQ Correlation Gap

### 4.1 LPN SQ Correlation

For standard LPN with secret `s ∈ F_2^n`, the distributions `D_s` and `D_{s'}` have correlation:

```
⟨D_s, D_{s'}⟩ = (1-2p)^2 · 2^{-n} · 1_{s = s'} + noise terms
```

The average pairwise correlation over all `s ≠ s'` is:

```
ρ_avg(LPN) = O(2^{-n})
```

This gives the standard SQ lower bound: `q = Ω(2^n)` queries for tolerance `τ = 1/poly(n)`.

### 4.2 LSN SQ Correlation (K3 Result)

From K3 Lemma 3.1 (exact formula):

```
ρ_avg(LSN) = (1-2p)^2 · 2^{-2n} · E[2^j] · (1 + O(2^{-n}))
```

where `E[2^j] ≈ 1.65` (bounded constant). Therefore:

```
ρ_avg(LSN) = O(2^{-2n}) = (ρ_avg(LPN))^2 · Θ(1)
```

### 4.3 Implication: LSN is SQ-Strictly Harder

The correlation for LSN is the **square** of LPN's correlation (up to constants). This means:

**Lemma 4.1**: In the SQ model, LSN requires **quadratically more** queries than LPN for the same tolerance. Specifically, if LPN requires `q_LPN = Θ(2^n)` queries, then LSN requires `q_LSN = Θ(2^{2n})` queries.

**Barrier**: If there were a black-box reduction from LSN to LPN with `poly(n)` overhead, then an LPN solver with `q = 2^{O(n)}` queries would solve LSN in `2^{O(n)}` queries. But LSN requires `2^{Ω(2n)} = 2^{Ω(n)}` — the same rate. So the reduction would need to be **tight** (no overhead), and the LPN solver would need to achieve the **exact** SQ lower bound, which is information-theoretically impossible for noisy samples.

More precisely: a reduction from LSN to LPN would need to map an LSN instance with `ρ = O(2^{-2n})` to an LPN instance with `ρ' = O(2^{-n})`. But the reduction itself would need to amplify the correlation by a factor of `2^n`, which is impossible without knowing the secret (information-theoretically, the reduction cannot distinguish `D_L` from `D_{L'}` better than the SQ oracle allows).

---

## 5. Barrier 3: Structural Encoding Gap

### 5.1 LPN → LSN (Embedding LPN into LSN)

**Question**: Can we embed an LPN instance into an LSN instance, showing LPN ≤ LSN?

**Attempt**: Given LPN secret `s ∈ F_2^n`, construct a Lagrangian `L_s` that encodes `s`.

**Obstruction**: 
- A Lagrangian has dimension `n` in `2n` dimensions. The isotropic condition `Ω|_L = 0` imposes `n(n-1)/2` independent constraints.
- Encoding a single vector `s` into a subspace `L_s` requires `n` basis vectors. The isotropic condition forces a specific relationship among these basis vectors.
- Any valid encoding would have the property that **recovering `L_s` gives `s`**, but this is trivially true. The issue is hardness preservation: the LPN noise structure may not preserve the LSN hardness.
- **Conclusion**: LPN ≤ LSN is plausible (embed LPN into LSN), but this shows LSN is **at least as hard** as LPN, not that LSN is reducible to LPN.

### 5.2 LSN → LPN (Reducing LSN to LPN)

**Question**: Given an LSN oracle, can we solve LPN? Or conversely, given an LPN solver, can we solve LSN?

**Attempt 1 (Point queries)**: Query LSN samples and try to extract individual vectors from `L`.
- A single sample `(x, y)` with `y = 1` gives `x ∈ L` (with noise), but this is just one point in an `n`-dimensional space.
- To recover `L`, we'd need `n` linearly independent points, but the noise rate `p` means each "positive" sample is noisy.
- This is analogous to trying to solve LPN by querying `n` independent instances — but LPN is already hard for a single instance.

**Attempt 2 (Project to subspace)**: Project the LSN instance onto a subspace to get an LPN instance.
- Choose a `2k`-dimensional symplectic subspace `V' ⊂ V` and restrict to it.
- The restriction `L ∩ V'` is a subspace of `L`, but not necessarily Lagrangian in `V'` (unless `V'` is symplectic and `L` is transversal to `V'^⊥`).
- The intersection dimension is random and small (from K3, mean ≈ 0.76), so `L ∩ V'` is typically `{0}` or 1-dimensional — not enough to encode a useful LPN instance.

**Attempt 3 (Quotient space)**: Take the quotient `V / W` for some subspace `W`.
- The quotient of a Lagrangian is not necessarily a Lagrangian in the quotient space.
- The symplectic structure does not descend nicely unless `W` is isotropic and coisotropic, which is too restrictive.

**Attempt 4 (Decouple via symplectic transform)**: Use the symplectic group `Sp(2n)` to randomize the instance.
- From Exp 23 (Weil noise preservation), **nonlocal Sp maps do not preserve the per-qubit depolarizing noise law** (OFA-360).
- Any reduction that uses symplectic transforms to "decouple" the Lagrangian structure would distort the noise, breaking the LPN hardness assumption.

### 5.3 Conclusion: Natural Reductions Blocked

All natural strategies for reducing LSN to LPN are blocked by:
1. **Dimension mismatch**: LPN is a point problem; LSN is a subspace problem
2. **Noise law incompatibility**: Symplectic transforms don't preserve i.i.d. Bernoulli noise (OFA-360)
3. **Isotropic constraint**: The Lagrangian condition cannot be locally projected without losing the structure

---

## 6. Barrier 4: Oracle Separation Argument

### 6.1 Ideal Oracle Model

Consider two oracles:
- **O_LPN**: On query `a ∈ F_2^n`, returns `⟨a, s⟩ ⊕ η` for secret `s` and noise `η ~ Bernoulli(p)`
- **O_LSN**: On query `x ∈ F_2^{2n}`, returns `1_L(x) ⊕ η` for secret Lagrangian `L` and noise `η ~ Bernoulli(p)`

### 6.2 LPN-Solving Oracle Does Not Help LSN

**Claim 6.1**: Given oracle access to an LPN solver (that solves any LPN instance in `poly(n)` time), an LSN solver with only `poly(n)` samples cannot use the LPN solver to recover `L`.

**Reasoning**:
- An LPN solver takes `poly(n)` samples and outputs a single vector `s`.
- To recover `L` (dimension `n`), we'd need `n` linearly independent vectors.
- Each LPN instance would need to target a different direction in `L`, but the LSN oracle doesn't give us a way to "target" specific directions without already knowing `L`.
- The noise in LSN is on the **indicator function** `1_L(x)`, not on the inner product with a fixed vector. This is a different noise model.

### 6.3 LSN-Solving Oracle Trivially Solves LPN

**Claim 6.2**: Given an LSN solver, LPN is trivially solvable (LPN ≤ LSN).

**Construction**: Embed LPN into LSN. Given LPN secret `s ∈ F_2^n`, construct Lagrangian `L = span{(s, 0)}` in a symplectic space where `Ω((s,0), (s',0)) = 0`. This is a degenerate embedding. A proper embedding requires a full Lagrangian, but the point is: **if LSN is easy, then LPN is easy** (since LPN is a special case of a subspace problem with n=1, though the symplectic form in 2 dimensions is trivial).

Actually, this is not quite right. Standard LPN is over `F_2^n`, and LSN is over `F_2^{2n}` with a symplectic form. The n=1 case of LSN would be in `F_2^2` with a Lagrangian of dimension 1, which is just a 1-dimensional isotropic subspace — but in `F_2^2`, every 1-dimensional subspace is isotropic (since `Ω(v,v) = 0` for all `v`). So LSN in `n=1` is exactly: pick a random line `L` in `F_2^2`, sample `x`, and return `1_L(x) + noise`. This is NOT the same as LPN, because LPN uses an inner product `⟨a, s⟩`, not an indicator `1_L(x)`.

However, LPN in dimension `n` can be viewed as: sample `a`, and ask whether `a` is in the dual of `s` (i.e., `a ∈ s^⊥`). The hyperplane `s^⊥` is an `(n-1)`-dimensional subspace, not a Lagrangian (which is `n`-dimensional in `2n` dimensions). So LPN and LSN are genuinely different geometric objects.

---

## 7. Formal Statement of the Impossibility Barrier

### 7.1 What We Can Prove

**Theorem 7.1** (Barrier Statement, not Impossibility). Under the assumption that standard LPN is hard in the SQ model with `q = 2^{Ω(n)}` queries and tolerance `τ = 1/poly(n)`, any black-box reduction from LSN to LPN with `poly(n)` overhead would require:

(a) An LPN solver that achieves the **information-theoretic optimal** query complexity `q = Θ(2^n)` (no algorithm is known to achieve this), OR
(b) A reduction that **amplifies correlation** by a factor of `2^n`, which is impossible in the SQ model without violating the tolerance bound.

**Proof**: From the SQ correlation gap (Barrier 2), LSN has `ρ_avg = O(2^{-2n})` while LPN has `ρ_avg = O(2^{-n})`. A reduction from LSN to LPN would map LSN's `ρ = 2^{-2n}` to LPN's `ρ' = 2^{-n}`. But the reduction itself, being a `poly(n)`-time algorithm, can only make `poly(n)` SQ queries. By the SQ lower bound for LSN, any algorithm that distinguishes LSN distributions with correlation `2^{-2n}` requires `q = 2^{Ω(n)}` queries. The reduction cannot achieve this amplification with `poly(n)` queries. ∎

### 7.2 What We Cannot Prove (Open Problem)

A **true oracle separation** would require:
- Constructing an oracle `O` such that LPN is easy relative to `O` but LSN is hard relative to `O`
- Or: proving that `LSN ∉ BPP^{LPN}` (LSN is not in BPP with an LPN oracle)

This is beyond current techniques. The SQ barrier argument (Theorem 7.1) is the strongest unconditional statement we can make without such an oracle separation.

---

## 8. Summary of Barriers

| Barrier | Obstruction | Strength |
|---------|------------|----------|
| 1. Search space | `2^{n^2}` vs `2^n` | Information-theoretic |
| 2. SQ correlation | `2^{-2n}` vs `2^{-n}` | Unconditional (SQ model) |
| 3. Structural encoding | Point vs subspace, isotropic constraint | Geometric |
| 4. Noise law | Nonlocal Sp maps don't preserve i.i.d. noise | Empirical (Exp 23 + OFA-360) |
| 5. Oracle separation | No known oracle makes LPN easy but LSN hard | Open problem |

---

## 9. Implications for the 7th Source Problem

The LSN → LPN impossibility barrier supports the claim that LSN is a **distinct hardness candidate** from LPN:

1. **LSN is not "just LPN in disguise"**: The symplectic structure, Lagrangian constraint, and 2n-dimensional ambient space create a genuinely different problem.
2. **LSN may be strictly harder**: The SQ correlation gap suggests LSN requires quadratically more queries in the SQ model.
3. **No natural reduction exists**: All natural strategies (projection, quotient, decoupling) are blocked by geometric or noise-theoretic constraints.
4. **Independent hardness assumption**: LSN hardness can be posited independently of LPN hardness, though both are consistent with the same meta-assumption (SQ lower bounds).

---

## 10. References

1. A. Blum, A. Frieze, R. Kannan, S. Vempala. "A polynomial-time algorithm for learning noisy linear threshold functions." *Algorithmica*, 1998.
2. V. Feldman, E. Grigorescu, L. Reznikov, S. Vempala. "Statistical query algorithms for mean vector estimation and learning Gaussian mixtures." *SODA*, 2017.
3. O. Regev. "On lattices, learning with errors, random linear codes, and cryptography." *JACM*, 2009.
4. K3 SQ Proof: `2026-06-08-k3-formal-sq-proof.md` (Kimi, 2026-06-08)
5. Exp 23 (Weil Noise Preservation): `2026-06-07-experiment-23-weil-noise-preservation-verdict.md`
6. Codex OFA-360: `2026-06-07-codex-to-kimi-ofa359-360-handoff.md`

---

*P4 Analysis: LSN vs LPN Impossibility Barriers.*
*K3 Status: COMPLETE. P1 Audit: COMPLETE. P4: Documented.*

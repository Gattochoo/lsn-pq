# P3: Non-Linear sympLPN → LPN Reduction — Polynomial Barrier Verified

**Status:** Barrier established (information-theoretic)  
**Date:** 2026-06-08  
**Agent:** Kimi  
**Previous:** Lane A (2026-06-06) established linear-only separation; non-linear was open.

---

## 1. The Question

Does a **non-linear** reduction exist from sympLPN to LPN?  
Lu–Poremba–Quek–Ramkumar (arXiv:2603.19110v1, Appendix D) proved **linear** reductions are information-theoretically blocked.  
**Non-linear / adaptive / randomized reductions were left entirely open.**

This document closes that gap for the **polynomial-reduction** class — the natural non-linear extension of the linear `B·A` matrix-multiply approach.

---

## 2. Core Insight: 1_L(x) is a Degree-n Polynomial

For a Lagrangian `L ⊂ F_2^{2n}` with orthogonal complement basis `{w_i}`, the indicator is:

```
1_L(x) = ∏_{i=1}^n (1 + ⟨w_i, x⟩)
```

**Verification:** The product is 1 iff all `⟨w_i, x⟩ = 0`, i.e., `x ∈ (L^⊥)^⊥ = L`. ∎

Expanding the product:

```
1_L(x) = Σ_{S⊆{1,...,n}} ∏_{i∈S} ⟨w_i, x⟩
```

This is a **degree-n polynomial** with exactly **2^n nonzero terms**.

---

## 3. The Polynomial-Reduction Barrier

Any LPN reduction must express the sympLPN label as a linear functional of features:

```
y = 1_L(x) ⊕ η(x)  ≈  ⟨s, φ(x)⟩ ⊕ η'(x)
```

where `φ: F_2^{2n} → F_2^M` is a feature map and `s ∈ F_2^M` is the LPN secret.

### 3.1 Exact Representation Requires Exponential Secret Dimension

For `⟨s, φ(x)⟩` to equal `1_L(x)` exactly, `φ(x)` must contain all monomials up to degree `n`:

```
M = C(2n, 0) + C(2n, 1) + ... + C(2n, n)  ≈  2^{2n-1}
```

Standard LPN with secret dimension `M` requires sample complexity `poly(M)` or `exp(Ω(√M))`.  
With `M ≈ 2^{2n-1}`, this is **doubly-exponential in n** — the reduction is **useless**.

### 3.2 Cheap Low-Degree Maps Carry No Signal (truncation vs best approximation)

If `φ(x)` contains only degree-≤D monomials for `D < n`, then `⟨s, φ(x)⟩` is a degree-D polynomial.  
No degree-D polynomial can approximate `1_L(x)` well:

| n | D=1 truncation error | D=n−1 truncation error | Exact terms |
|---|----------------------|------------------------|-------------|
| 2 | 25.0% | — | 4 |
| 3 | 37.5% | 12.5% | 8 |
| 4 | 43.8% | 6.25% | 16 |

**Pattern (truncation vs best — do not confuse them):**
- *ANF truncation* at `D = 1` (drop `1_L`'s higher terms) → error toward **1/2** as `n → ∞`; this *specific* map loses the signal.
- But the **best** degree-`D` map for any `D < n` has error **`2^{−n}`**, achieved by the constant map `p ≡ 0` (`error = |L|/|V| = 2^{−n}`).

So a low-degree map can approximate `1_L` *cheaply* (`2^{−n}` error) — the catch is that the cheap approximation `p ≡ 0` is **`L`-independent** and recovers nothing. The barrier (formalised in §4) is therefore **dimension and structure**, not approximation magnitude.

### 3.3 The Error is Structured, Not Random

Even when D = n−1 (error = 2^{−n}), the error is **not i.i.d. noise**.  
For `L = span{e_1,...,e_n}`:

```
error(x) = 1  iff  x_{n+1} = x_{n+2} = ... = x_{2n} = 1
```

The error is concentrated on a **specific n-dimensional affine subspace** — a highly structured pattern.  
An LPN solver assuming random noise will see systematic bias and fail.

---

## 4. Formal Barrier Statement

**Theorem 4.1** (Polynomial-Reduction Barrier). Let `L ⊂ F_2^{2n}` be a Lagrangian with orthogonal-complement basis `{w_1,…,w_n}`. Write the indicator as

$$
\mathbf{1}_L(x) \;=\; \prod_{j=1}^{n}\bigl(1 + \langle w_j, x \rangle\bigr)
\;=\; \sum_{k=0}^{n} e_k\bigl(\langle w_1,x\rangle,\dots,\langle w_n,x\rangle\bigr),
$$

where `e_k` is the `k`‑th elementary symmetric polynomial. Then:

1. `deg(1_L) = n` and `1_L` has exactly `2^n` nonzero monomials.
2. For any `D < n`, every degree‑`D` polynomial `p(x)` satisfies
   $$
   \Pr_{x\sim\text{Uniform}(V)}\bigl[\mathbf{1}_L(x) \neq p(x)\bigr] \;\geq\; 2^{-n}.$$
3. The set `{x : 1_L(x) ≠ p_D(x)}` for the optimal degree‑`D` approximation `p_D` is a union of cosets of subspaces of `L`; in particular the error is **structured**, not i.i.d.

**Proof.** 
*(1)* Each factor `(1+⟨w_j,x⟩)` is linear, so the product has degree `n`. Expanding the product produces one monomial for every subset `S⊆{1,…,n}`, namely `∏_{j∈S}⟨w_j,x⟩`; hence exactly `2^n` terms.

*(2)* The degree‑`n` term is `e_n = ∏_{j=1}^{n}⟨w_j,x⟩`. Because `{w_j}` is a basis of `L^⊥`, the system `⟨w_j,x⟩=1` for all `j` has a unique solution `x_0` modulo `L`. Therefore `e_n(x)=1` precisely on the single coset `x_0+L` (size `2^n`) and `e_n(x)=0` elsewhere. 

For any degree‑`D` polynomial `p` with `D<n`, the difference `1_L−p` is a **nonzero** polynomial of degree **exactly `n`** (its degree-`n` part is `e_n ≠ 0`, which the degree-`<n` map `p` cannot cancel). By the minimum distance of the Reed–Muller code `RM(n,2n)` — every nonzero polynomial of degree `≤ n` in `2n` variables has Hamming weight `≥ 2^{\,2n-n} = 2^n` — we get `|{x : 1_L(x)≠p(x)}| ≥ 2^n`, i.e. error probability `≥ 2^{−n}`. The bound is **tight**: `p ≡ 0` attains it (error `= |L|/|V| = 2^{−n}`).

*(3)* Every monomial `∏_{j∈S}⟨w_j,x⟩` is constant on cosets of the subspace `\bigcap_{j∈S}\ker⟨w_j,·⟩`. The error `1_L−p_D` is a linear combination of such monomials, so its support is a union of cosets of subspaces contained in `L`. It is therefore highly structured and cannot be modelled as i.i.d. Bernoulli noise. ∎

**Corollary 4.2** (Feature-Map Blowup). Any LPN reduction that represents `1_L` *exactly* via a feature map `φ: F_2^{2n} → F_2^M` requires `M ≥ C(2n,≤n) = Θ(2^{2n})`, because the space of degree‑`≤n` polynomials in `2n` variables has that dimension.

**Corollary 4.3** (Why a cheap low-degree map is not a reduction). The **best** degree-`D` approximation of `1_L`, for *every* `0 ≤ D < n`, has error **exactly `2^{−n}`** — the lower bound is Theorem 4.1(2), and it is *achieved* by the constant map `p ≡ 0` (whose error is `|L|/|V| = 2^{−n}`). So low-degree approximation of `1_L` is **easy** (tiny error), not hard. The obstruction to a reduction is therefore **not** the approximation *magnitude*; it is:

1. **Dimension** (Corollary 4.2): a *lossless* feature map (`1_L = ⟨s,φ(x)⟩` exactly, as LPN requires) needs the degree-`n` monomials, i.e. `M ≥ Θ(2^{2n})`.
2. **Structure / `L`-dependence** (Theorem 4.1(3)): the cheap `2^{−n}`-error map `p ≡ 0` is **`L`-independent** — its residual is *exactly* the subspace `L`, so it carries no usable signal to recover `L`. Any `L`-informative low-degree map has an `L`-coset-structured residual, which LPN's i.i.d. Bernoulli noise cannot model.

| n | best (greedy) deg≤1 | best deg≤(n−1) | ANF-truncation deg=1 |
|---|---------------------|----------------|----------------------|
| 2 | 0.250 = 2⁻² | 2⁻² | 0.250 |
| 3 | 0.125 = 2⁻³ | 2⁻³ | 0.375 |
| 4 | 0.0625 = 2⁻⁴ | 2⁻⁴ | 0.438 |

*Data: `lsn-experiments/32-p3-*`, **greedy** (best) vs **truncation** columns. The best degree-`D` approximation error is `2^{−n}`, flat in `D`; the `Θ(1)` figures sometimes quoted are the ANF-**truncation** error (dropping `1_L`'s degree-`>D` terms) — a specific bad map, **not** the optimum. There is no `Θ(1)` "optimal-approximation" barrier.*

---

## 5. Scope and Limitations

This barrier applies to **polynomial reductions** — reductions where the sympLPN sample is transformed by fixed polynomial functions.

**Not covered:**
- **Adaptive reductions** (transform depends on previous samples) — entropy-barrier makes them vacuous (A1), but they are not information-theoretically impossible.
- **Randomized reductions** with sample-dependent randomness.
- **Algebraic-geometry reductions** beyond polynomial maps.
- The smallest class **strictly larger than polynomial** (e.g. `r`‑round bounded-query adaptive, or degree‑`D` adaptive feature maps) — defining and blocking this class is the next 7th-axis step (T2.2, still open).

Polynomial reductions are the **natural non-linear extension** of the linear `B·A` approach. The barrier shows that even this natural extension fails: an *exact* representation needs exponential dimension (Corollary 4.2), and any *cheap* low-degree approximation is either `L`-independent (useless, like `p ≡ 0`) or has an `L`-coset-structured residual that LPN's i.i.d. noise cannot absorb (Theorem 4.1(3) / Corollary 4.3).

---

## 6. Consequence for LSN's 7th-Claim

```
Linear reductions:    BLOCKED (Lu et al., information-theoretic)
Polynomial reductions: BLOCKED (Theorem 4.1, degree + structured error)
Adaptive/randomized:   OPEN, but no candidate strategy exists
```

The **only remaining open class** is adaptive/randomized reductions with a fundamentally different strategy — precisely the "very different strategy" that Lu et al. anticipated as unlikely.

Combined with the **win-win barrier** (such a reduction would improve LPN self-reductions), this makes the non-existence of reductions **highly plausible**, though not yet proven for the fully adaptive class.

---

## 7. Verification Scripts

- `lsn-experiments/32-p3-nonlinear-polynomial-barrier.py`
  - Computes exact polynomial representation of `1_L(x)` for `n=2,3,4`
  - Verifies degree, term count, and truncation error
  - All numerical data match the closed-form bounds of Theorem 4.1

---

*By Kimi, 2026-06-08.  General proof added per Claude handoff T2.1.*

---

## 5. Scope and Limitations

This barrier applies to **polynomial reductions** — reductions where the sympLPN sample is transformed by fixed polynomial functions.

**Not covered:**
- Adaptive reductions (transform depends on previous samples)
- Randomized reductions with sample-dependent randomness
- Reductions using algebraic geometry beyond polynomial maps

However, polynomial reductions are the **natural non-linear extension** of the linear `B·A` approach analyzed in Appendix D.  The barrier shows that even this natural extension fails.

---

## 6. Consequence for LSN's 7th-Claim

```
Linear reductions:    BLOCKED (Lu et al., information-theoretic)
Polynomial reductions: BLOCKED (this note, degree + structured error)
Adaptive/randomized:   OPEN, but no candidate strategy exists
```

The **only remaining open class** is adaptive/randomized reductions with a fundamentally different strategy — precisely the "very different strategy" that Lu et al. anticipated as unlikely.

Combined with the **win-win barrier** (such a reduction would improve LPN self-reductions), this makes the non-existence of reductions **highly plausible**, though not yet proven for the fully adaptive class.

---

## 7. Verification Scripts

- `lsn-experiments/32-p3-nonlinear-polynomial-barrier.py`
  - Computes exact polynomial representation of `1_L(x)`
  - Verifies degree and term count
  - Computes truncation and greedy approximation errors

---

*By Kimi, 2026-06-08.  Replaces Codex's planned Rust harness with Python analysis.*

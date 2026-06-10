# Coverage sentence: D.2 quantifier + B-visibility model split

**Date:** 2026-06-10. **Status:** Ready for paper insertion.
**Discipline:** Sound Verifier. No 7th; no break; no security claim. OPEN = LSN.

---

## Context

LPQR26 Theorem D.2 (pinned in `meta/LPQR26-appendixD-quotes.md`) states that $B \in \mathbb{F}_2^{m \times 2n}$ is a random variable such that $BA$ is statistically indistinguishable from uniformly random. The quantifier order does **not** require $B \perp A$; adaptive choices $B = f(A, \mathsf{rand})$ are allowed provided only the *marginal* distribution of $BA$ is uniform. This yields two distinct models for the linear-reduction landscape:

---

## Coverage chart (to be inserted in the paper's linear-reduction section)

| Regime | B-visibility | BA distribution | Gram detector | Label bias | Status |
|--------|-------------|-----------------|---------------|------------|--------|
| Fixed/public B, $\rho > 3n/2$ | Public | Deterministic low-rank | **BLOCKED** by rank stratification (Thm, ours) | $\Theta(1)$ | Closed |
| Fixed/public B, $\rho \le 3n/2$ | Public | Deterministic mid-rank | Entropy-deficiency (LPQR D.1) + Lane C | $\Theta(1)$ | Open strip |
| Random/high-entropy B | Public | Per-realization full-rank | **BLOCKED** by transport ($\min_Q \operatorname{rank} = 0$) | $2^{-\Theta(n)}$ | Closed |
| **Secret-B** (LPQR D.2 model) | Secret | Marginal uniform | Does not apply (detector needs $B$) | $2^{-\Theta(n)}$ | **Open bridge** |

### Key distinction

- **Public-B model** (the realized $B$ is available to the distinguisher): per-realization transport theorems apply. The distinguisher sees $B$ and can compute the optimal transportable form. Randomizing $B$ per realization does **not** help because the detector operates on the realized $B$.
- **Secret-B model** (only the marginal distribution of $BA$ matters, per D.2 quantifier): the distinguisher does **not** see $B$. The Gram detector is inapplicable; the open question is whether the **label signal** ($|Be|$ distribution) plus the **marginal uniformity** of $BA$ suffice for a reduction.

The secret-$B$ regime is *loosely analogous* to the membership-LSN vs stabilizer-decoding LSN gap: in both settings the adversary does not fully observe the structure that generates the samples (the reduction matrix $B$ vs the Lagrangian $L$ / logical bitstring $y$). The analogy is motivational only; the two open problems (A3b reduction-matrix visibility and the form-equivalence bridge) remain distinct.

---

## Proposed paper paragraph

> The quantifier order of LPQR26's Theorem D.2 is subtle: $B$ may be chosen as a function of $A$ provided only that the *induced distribution* of $BA$ is uniform. This creates a **secret-$B$** regime in which the reduction matrix is not public. Our transport theorems (which require the adversary to know $B$) do not apply here; the residual open question is whether label-signal bounds (piling-up) together with marginal $BA$-uniformity suffice to close the linear-reduction landscape at constant noise. In the **public-$B$** regime, by contrast, randomizing $B$ does not escape our rank-stratification barrier because the detector operates on the realized matrix.

---

## Honest scope

- The secret-$B$ bridge is **not yet closed**. The Krawtchouk bias formula (`meta/2026-06-10-A3b-lemma1-affine-coset-bias.md`) controls the label signal for a given $A$, but the joint distribution of $(BA, Be)$ under adaptive $B$-choices is not fully characterized.
- The public-$B$ coverage is **complete** for fixed and per-realization-random $B$; the mid-rank strip ($\rho \le 3n/2$) remains open but is bounded by LPQR D.1 + our Lane-C entropy argument.

No 7th; no break; no security claim. OPEN = LSN.

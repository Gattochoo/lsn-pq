# Track G: OP7 beyond the orbit family — universal label-preserving obstruction

**Date:** 2026-06-14.  **Author:** Kimi (subagent).  **Experiment:** 211.  
**Status:** Track-G milestone closed; claims labelled THEOREM/EVIDENCE/OPEN.  
**Discipline:** Sound Verifier.  No closure; no break; no security claim.  OPEN = LSN.

## Summary

Track G asked whether the OP7 symplectic-orbit analysis extends to arbitrary
public bijections that preserve the label bit.  The answer is stronger than the
original prompt anticipated:

* the **duplicated-label-bit obstruction is universal** for every label-preserving
  split (Theorem G.1);
* the **exact statistical distance itself is universal**: under the natural
  same-secret comparison, every label-preserving bijection pair has the same SD
  as the symplectic-orbit family, namely `1 - 5/(8·4^n)` at `p = 1/4` (Theorem
  G.3);
* label-modifying maps are scope-defined and remain **EVIDENCE/OPEN**: valid
  maps reduce to the label-preserving case, but fully general (not necessarily
  LSN-preserving) bijections need a comparison distribution that has not been
  fixed.

All computations use `fractions.Fraction` end-to-end and JSON stores string
fractions.

## Deliverables

* `experiments/211-KIMI-trackG-label-preserving-universal-bound.py`
* `experiments/output/211-trackG-label-preserving-universal-bound.json`

## G1. THEOREM — exact `Pr_fresh[b_1 ≠ b_2]` and universal lower bound

**Setup.**  Fix LSN noise rate `p`.  Draw a uniform Lagrangian `L ⊂ F_2^{2n}` and
two independent fresh samples `(u_1,b_1), (u_2,b_2) ~ D_L`, i.e. `u_i` uniform,
`b_i = 1_L(u_i) + e_i` with `e_i ~ Bernoulli(p)` independent.

Let

```
mu_n = Pr_u[1_L(u) = 1] = |L| / 2^{2n} = 2^n / 2^{2n} = 1/2^n,
q_n  = Pr[b = 1]        = mu_n(1-p) + (1-mu_n)p
                       = p + (1-2p)/2^n.
```

Because the two samples are independent conditioned on `L`, and `L` is shared,
`b_1` and `b_2` are i.i.d. Bernoulli`(q_n)` marginally.  Hence

```
Pr_fresh[b_1 ≠ b_2] = 2 q_n (1-q_n)
                    = 2 (p + (1-2p)/2^n)(1-p - (1-2p)/2^n).
```

At `p = 1/4`:

| `n` | `Pr_fresh[b_1 ≠ b_2]` |
|-----|------------------------|
| 2   | `15/32`                |
| 3   | `55/128`               |
| ∞   | `3/8`                  |

**Universal lower bound.**  For any public bijections `f_1,f_2` of `F_2^{2n}`,
the split map

```
(x,b) ↦ ((f_1(x),b), (f_2(x),b))
```

produces a pair whose `(b_1,b_2)`-marginal is supported on `{00,11}`, because the
same label bit `b` is copied to both outputs.  The fresh pair assigns mass
`Pr_fresh[b_1≠b_2]` to `{01,10}`.  By the data-processing inequality for total
variation,

```
SD( split_{f_1,f_2}(D_L) , D_L × D_L )  ≥  Pr_fresh[b_1 ≠ b_2].
```

This bound holds for **every** pair of public bijections — the family is
explicitly "label-preserving public bijections `f_1,f_2`".

**Verification.**  Experiment 211 enumerates `n = 2,3` directly over all
Lagrangians and all `(u_1,u_2,e_1,e_2)` and confirms the closed form matches the
enumeration fraction-for-fraction.

## G3. THEOREM — exact SD is independent of the bijections

**Statement.**  Under the natural same-secret comparison (both samples from the
same uniform random `L`),

```
SD( split_{f_1,f_2}(D_L) , D_L × D_L )
    = 1 - (p² + (1-p)²) / 4^n
    = 1 - 5/(8·4^n)        at p = 1/4,
```

for **every** pair of public bijections `f_1,f_2` of `F_2^{2n}`.

**Proof.**  Applying `f_i^{-1}` to the `i`-th `x`-coordinate is a bijection on the
joint sample space, so it preserves total variation.  It sends the transformed
pair to the identity-split pair `(x,b,x,b)` and the fresh pair to two independent
fresh samples `(x_1,b_1,x_2,b_2)`.  Neither reduced distribution depends on
`f_1,f_2`, so the SD is the same for all bijections.  The value for the identity
split is exactly the orbit-family value computed in Track B / experiment 210,
now seen to be universal.

**Verification.**  At `n = 2` experiment 211 computes the exact SD for:

* `id/id`,
* three symplectic matrices `T ∈ Sp(4,F_2)`,
* five affine maps `x ↦ A x + t` with `A ∈ GL(4,F_2)`,
* three random bijections of `F_2^4`.

Every single pair returns `123/128`.  At `n = 3` the identity split returns
`507/512`, matching the closed form.  Thus non-linear / non-symplectic bijections
cannot do better or worse than the orbit family under the same-secret comparison.

## G2. EVIDENCE/OPEN — label-modifying maps

**Definition.**  A *label-modifying* split is a map

```
(x,b) ↦ (g_1(x,b), g_2(x,b))
```

where each `g_i: F_2^{2n} × F_2 → F_2^{2n} × F_2` is a public bijection.

**Correctness constraint.**  In the LSN context a natural validity requirement is
that each `g_i` maps a valid sample `D_L` to a valid sample `D_{L'}` for some
Lagrangian `L'`.  Under this constraint, applying `g_i^{-1}` to the `i`-th output
reduces the problem to the label-preserving case, so the universal lower bound
(and the exact same-secret SD, once the appropriate comparison distribution is
fixed) still applies.

**Open point.**  If the `g_i` are arbitrary bijections not required to preserve
the Lagrangian-sample structure, the outputs are not LSN samples and there is no
canonical comparison distribution.  Whether a meaningful analogue of the
shared-bit obstruction exists for that broader family remains **OPEN**.

## Guards observed

* **L1 exact arithmetic.**  All probabilities computed with
  `fractions.Fraction`; JSON stores string fractions.
* **L2 duality care.**  No character sums over Lagrangians are used, so the
  `J`-twist does not arise; explicitly noted.
* **L3 query-class hygiene.**  This is a total-variation/distinguishability
  result.  No Feldman-style SQ theorem is invoked, hence no query-class claim is
  made.

## Interpretation guard (PRE-REGISTER)

* **Comparison distribution:** two independent fresh samples from the *same*
  uniform secret `L` (the natural LSN pair distribution).
* **Family names:** every statement names its transformation family explicitly
  (label-preserving split, valid label-modifying split, arbitrary label-modifying
  bijection).
* **Hardness flavour:** the universal SD tends to 1 in `n`; the universal
  lower bound from the duplicated label bit tends to `3/8`.  This is a structural
  distributional gap, not a claim about lem:m2 rates or concrete attacks.

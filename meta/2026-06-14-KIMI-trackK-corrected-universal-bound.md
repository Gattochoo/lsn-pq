# Track K: repair 211 + universal bound for label-flipping splits

**Date:** 2026-06-14.  **Author:** Kimi (subagent).  **Experiments:** 211 (corrected), 212, 213.  
**Status:** Track-K milestone complete; claims labelled THEOREM / EVIDENCE / OPEN / WITHDRAWN.  
**Discipline:** Sound Verifier.  No closure; no break; no security claim.  OPEN = LSN.

## Summary

Track K repairs the (L4) violation in Track G experiment 211 and extends the
universal obstruction to the larger **label-flipping** family of public splits.

* **K1 (THEOREM, 211 corrected).** The exact same-secret statistical distance
  for a label-preserving split
  `(x,b) ↦ ((f₁(x),b),(f₂(x),b))` is

  ```
  SD = 1 − 4^{-n} [ 2 p(1−p) + (1−2p)^2 A ],
  A  = Pr_{L,x}[ 1_L(f₁ x) = 1_L(f₂ x) ].
  ```

  The orbit value `1 − (p²+(1−p)²)/4^n` (=`123/128` at `n=2, p=1/4`) is the
  **universal minimum**, attained iff `f₁ = f₂`.  The old G.3 claim that the SD
  is the same for every bijection pair is **withdrawn**; its proof incorrectly
  transformed the fresh comparison distribution too.

* **K2 (THEOREM, 212).** For the label-flipping family

  ```
  (x,b) ↦ ((f₁(x), b⊕h₁(x)), (f₂(x), b⊕h₂(x))),
  ```

  the exact SD is the same formula with

  ```
  A' = Pr_{L,x}[ 1_L(f₁ x) ⊕ 1_L(f₂ x) = h₁(x) ⊕ h₂(x) ].
  ```

  `A' = 1` iff `f₁ = f₂` **and** `h₁ = h₂` (literal duplicate).  Hence the
  label-preserving minimum is a universal lower bound for **all** label-flipping
  splits, equality only for the literal duplicate.

* **K3 (EVIDENCE/OPEN, 213).** For `b`-dependent point maps
  `g_i(x,b) = (φ_{i,b}(x), b⊕ψ_i(x,b))` the exact formula no longer applies.
  Random enumeration at `n=2` shows the universal minimum is respected in every
  tested instance; persistence for the whole family remains a conjecture.

All computations use `fractions.Fraction`; JSON stores string fractions.

---

## Deliverables

* `experiments/211-KIMI-trackG-label-preserving-universal-bound.py` (corrected)
* `experiments/212-KIMI-trackK-label-flipping-universal-bound.py`
* `experiments/213-KIMI-trackK-b-dependent-point-maps-evidence.py`
* `experiments/output/211-trackG-label-preserving-universal-bound.json`
* `experiments/output/212-trackK-label-flipping-universal-bound.json`
* `experiments/output/213-trackK-b-dependent-point-maps-evidence.json`
* `meta/2026-06-14-KIMI-trackG-universal-label-preserving.md` (G.3 marked withdrawn)

---

## K1. Corrected same-secret law for label-preserving splits

**Setup.**  Fix LSN noise rate `p`.  Draw a uniform Lagrangian `L ⊂ F_2^{2n}` and
a sample `(x,b)` from `D_L` (`x` uniform, `b = 1_L(x) + e`, `e ~ Bernoulli(p)`).
For public bijections `f₁,f₂`, the split outputs two correlated samples
`(f₁(x),b)` and `(f₂(x),b)`.  The natural comparison distribution is two
**independent** fresh samples `(u₁,b₁),(u₂,b₂) ~ D_L` from the **same** secret
`L`.

**Corrected theorem.**

```
SD( split_{f1,f2}(D_L) , D_L × D_L )
    = 1 − 4^{-n} [ 2 p(1−p) + (1−2p)^2 A ],
A   = Pr_{L,x}[ 1_L(f₁ x) = 1_L(f₂ x) ].
```

**Proof sketch (support/overlap).**  Condition on `(L,x)`.  The split side emits
label bits `b₁ = b₂ = 1_L(x)⊕e`.  The fresh side emits independent
`b_i = 1_L(u_i)⊕e_i`.  The two distributions agree exactly when either

* `e = 0`, `e₁ = e₂ = 0` and `1_L(x)=1_L(u₁)=1_L(u₂)`, or
* `e = 1`, `e₁ = e₂ = 1` and `1_L(x)⊕1=1_L(u₁)⊕1=1_L(u₂)⊕1`,

or in the mixed-noise cases where the mismatches cancel.  Summing the four
`(e,e₁,e₂)` possibilities over uniform `x` and independent `u₁,u₂` gives the
overlap

```
4^{-n} [ 2 p(1−p) + (1−2p)^2 A ].
```

Subtracting from 1 yields the formula.  ∎

**Consequences.**

* `A = 1` iff `f₁ = f₂` (for `f₁x ≠ f₂x` some Lagrangian separates the two
  points, so `A < 1`).
* Therefore the orbit value
  `SD_min = 1 − (p²+(1−p)²)/4^n = 1 − 5/(8·4^n)` is the universal **minimum**
  over all label-preserving splits, not the universal value.
* At `p = 1/4`: `SD = 1 − (3 + 2A)/128`.

**Verification at n = 2.**  Experiment 211 tests 12 pairs:

| pair | `A` | `SD` |
|------|-----|------|
| `id,id` | `1` | `123/128` |
| symplectic #0 | `4/5` | `617/640` |
| symplectic #1 | `11/15` | `1853/1920` |
| symplectic #2 | `11/15` | `1853/1920` |
| symplectic #3 | `7/10` | `309/320` |
| symplectic #4 | `7/10` | `309/320` |
| affine #0 | `3/5` | `619/640` |
| affine #1 | `3/5` | `619/640` |
| affine #2 | `3/5` | `619/640` |
| random #0 | `79/120` | `7421/7680` |
| random #1 | `5/8` | `495/512` |
| random #2 | `5/8` | `495/512` |

Every entry matches the closed form exactly and is `≥ 123/128`, with equality
iff `f₁ = f₂`.

**n = 3 spot check.**  One random symplectic pair gives `A = 29/36` and
`SD = 9133/9216`, strictly above the minimum `507/512`.

---

## K2. Label-flipping family

**Setup.**  Public bijections `f₁,f₂` and public label-flip functions
`h₁,h₂: F_2^{2n} → F_2`.  The split is

```
(x,b) ↦ ((f₁(x), b⊕h₁(x)), (f₂(x), b⊕h₂(x))).
```

**Theorem.**

```
SD = 1 − 4^{-n} [ 2 p(1−p) + (1−2p)^2 A' ],
A' = Pr_{L,x}[ 1_L(f₁ x) ⊕ 1_L(f₂ x) = h₁(x) ⊕ h₂(x) ].
```

**Proof sketch.**  The same four-noise overlap calculation as K1, but now the
split labels are `b_i = 1_L(x)⊕e⊕h_i(x)` while the fresh labels are
`b_i = 1_L(u_i)⊕e_i`.  Agreement in the `(1−2p)²` term requires the membership
XOR to match the public label-flip XOR, giving `A'`.  ∎

**Equality characterisation.**

* If `f₁ = f₂` and `h₁ = h₂`, the LHS of the event defining `A'` is `0` and the
  RHS is `0`, so `A' = 1` and `SD = SD_min`.
* If `f₁ ≠ f₂`, pick `x` with `f₁x ≠ f₂x`; there exists a Lagrangian containing
  `f₁x` but not `f₂x`, so for that `(L,x)` the membership XOR is `1`.  Whether
  or not `h₁(x)=h₂(x)`, at least one of the two choices makes the event false,
  hence `A' < 1`.
* If `f₁ = f₂` but `h₁ ≠ h₂`, pick `x` with `h₁(x)≠h₂(x)`; the membership XOR
  is `0` while the label-flip XOR is `1`, so `A' < 1`.

Thus `A' = 1` iff `f₁ = f₂` and `h₁ = h₂`.

**Verification at n = 2.**  Experiment 212 tests 12 representative cases.  All
match the closed form, all satisfy `SD ≥ 123/128`, and equality holds exactly
for the two literal-duplicate cases (`id,id,h₁=h₂=0` and `r,r,h₁=h₂=0`).
Representative values:

| case | `A'` | `SD` | duplicate? |
|------|------|------|------------|
| `id,id,00` | `1` | `123/128` | yes |
| `id,id,01` | `0` | `125/128` | no |
| `id,id,0,rand` | `9/16` | `991/1024` | no |
| `sp,00` | `11/15` | `1853/1920` | no |
| `rand,hh` | `1/2` | `31/32` | no |

---

## K3. b-dependent point maps (stretch)

**Scope.**  `g_i(x,b) = (φ_{i,b}(x), b⊕ψ_i(x,b))` with `φ_{i,b}` a bijection for
each `b` and `ψ_i` arbitrary.  This strictly generalises K2 because the
`x`-coordinate depends on the secret label bit `b`.

**Status.**  No closed-form SD is offered.  Experiment 213 enumerates 10 random
instances at `n = 2`; every instance has `SD ≥ 123/128`, and none attains the
minimum.  Persistence of the universal minimum for this family is therefore
**EVIDENCE**, not theorem.

---

## Withdrawal of old G.3

The original Track G meta note claimed (G.3) that the same-secret SD equals
`1 − (p²+(1−p)²)/4^n` for **every** pair of public bijections.  That proof
applied `f_i^{-1}` to **both** the split side and the fresh comparison side.
Because the fresh distribution `D_L × D_L` is **not** invariant under arbitrary
public bijections, this violates guard **(L4)**: a verification bijection may be
applied to one side only, or to both only after proving invariance.  The claim
is withdrawn and replaced by the corrected K1 theorem above.

---

## Guards observed

* **L1 exact arithmetic.**  All probabilities computed with
  `fractions.Fraction`; JSON stores string fractions.
* **L2 duality care.**  No character sums over Lagrangians; `J`-twist does not
  arise.
* **L3 query-class hygiene.**  These are exact total-variation statements.  No
  Feldman/SQ theorem or query-class inference is made.
* **L4 never transform the comparison distribution.**  The fresh pair
  `(u₁,b₁,u₂,b₂)` is compared in the natural domain.  All public maps
  (`f_i`, `h_i`, `g_i`) act only on the split side.

## Interpretation guard (PRE-REGISTER)

* **Comparison distribution:** two independent fresh samples from the *same*
  uniform secret `L`.
* **Family names:** label-preserving split, label-flipping split, and
  `b`-dependent point-map split are defined explicitly.
* **Hardness flavour:** the universal minimum tends to 1 in `n`; the
  duplicated-label lower bound tends to `3/8`.  This is a structural
  distributional gap, not a claim about `lem:m2` rates or concrete attacks.

# Track U: exact same-secret SD for label-preserving b-dependent bijections

**Date:** 2026-06-14.  **Author:** Kimi (subagent).  **Experiment:** 420.  
**Status:** Track-U milestone complete; claims labelled THEOREM / EVIDENCE / OPEN.  
**Discipline:** Sound Verifier.  No closure; no break; no security claim.  OPEN = LSN.

## Summary

Track R showed that the full b-dependent point-map family can break the
label-flipping universal minimum, but Claude's exp/341 audit proved that the
specific Track-R counterexample was **not bijective** and that valid bijective
b-dependent point maps respect the minimum in search.  Track U now proves the
exact same-secret SD for the clean bijective sub-family of **label-preserving
b-dependent point maps**

```
g_i(x,b) = (phi_{i,b}(x), b),    phi_{i,b} a bijection of F_2^{2n},
```

as an explicit functional of the two branch-agreement statistics.

---

## U1. THEOREM — exact same-secret SD

**Setup.**  Fix LSN noise rate `p`.  Draw a uniform Lagrangian `L ⊂ F_2^{2n}` and
a sample `(x,b)` from `D_L` (`x` uniform, `b = 1_L(x) + e`, `e ~ Bernoulli(p)`).
For public bijections `phi_{i,b}` (`i ∈ {0,1}`, `b ∈ {0,1}`), the split outputs
two correlated samples `(phi_{0,b}(x), b)` and `(phi_{1,b}(x), b)`.  The natural
comparison distribution is two independent fresh samples `(u_1,b_1),(u_2,b_2) ~ D_L`
from the **same** secret `L`.

**Theorem.**  The exact same-secret statistical distance is

```
SD = 1 - (p^2 + (1-p)^2) / 4^n
     + (1-2p)^2 / (2 * 4^n) * (2 - A_0 - A_1),
```

where for `beta ∈ {0,1}`

```
A_beta = Pr_{L,x}[ 1_L(phi_{0,beta} x) = 1_L(phi_{1,beta} x) ].
```

At `p = 1/4`:

```
SD = 1 - 5/(8 * 4^n) + (2 - A_0 - A_1) / (8 * 4^n).
```

**Proof sketch (support/overlap, L4 observed).**  Condition on the secret label
bit `b = beta`.  Because the maps are label-preserving, both split outputs carry
label `beta`.  The fresh comparison pair conditioned on `(beta,beta)` has both
labels `beta` and independent `x`-coordinates drawn from the noisy conditional
membership distribution `mu_L^beta`.  On this branch the split reduces to a
single fixed label-preserving pair `(phi_{0,beta}, phi_{1,beta})` applied to one
sample from `mu_L^beta`, versus two independent samples from `mu_L^beta`.

Writing `tau_beta = phi_{1,beta} ∘ phi_{0,beta}^{-1}` and expanding the total
variation over the four membership-pattern counts gives a per-branch overlap
that depends only on `|L ∩ tau_beta^{-1}(L)|`.  Averaging over `L` replaces this
by the agreement statistic `A_beta`.  The cross-branch terms involving
`q_beta = Pr[b=beta]` simplify because the `1/2^n` correction terms cancel,
leaving the closed form above.  (All algebra is verified by exact enumeration in
experiment 420.)

**Universal minimum.**  Since each `A_beta` is a probability, `A_beta ≤ 1`, and
`A_beta = 1` iff `phi_{0,beta} = phi_{1,beta}` (otherwise some `x` is sent to
two points separated by a Lagrangian).  The correction coefficient
`(1-2p)^2 / (2 * 4^n)` is non-negative, so

```
SD ≥ 1 - (p^2 + (1-p)^2) / 4^n = SD_min,
```

with equality iff `phi_{0,beta} = phi_{1,beta}` for **both** `beta`, i.e. iff
`g_0 = g_1` (the literal duplicate).

---

## U2. Verification

Experiment 420 verifies the theorem in three ways.

### Named cases at `n = 2`

| case | `A_0` | `A_1` | exact SD | relation to `SD_min = 123/128` |
|------|-------|-------|----------|--------------------------------|
| literal duplicate | `1` | `1` | `123/128` | equals minimum |
| transposition-only (exp/341) | `1` | `9/10` | `1231/1280` | strictly above |
| symplectic, same on both labels | `11/15` | `11/15` | `1853/1920` | strictly above |
| symplectic, b-dependent | `11/15` | `2/3` | `309/320` | strictly above |
| affine, b-dependent | `3/5` | `1` | `617/640` | strictly above |
| random b-dependent | `73/120` | `19/30` | `14851/15360` | strictly above |
| random all four branches | `83/120` | `73/120` | `1237/1280` | strictly above |

In every case the closed form equals the direct exact enumeration.

### Random bijective search (exp/341 regime)

`3000` random label-preserving b-dependent bijections at `n = 2`:

* **instances below `SD_min`:** `0`
* **minimum SD found:** `4941/5120 ≈ 0.965039`

This is consistent with Claude's exp/341 search over valid bijections.

### `n = 3` spot check

One random symplectic pair per label branch gives `A_0 = 4/5`, `A_1 = 29/36`,
and exact SD `91331/92160`, strictly above the `n = 3` minimum `507/512`.

---

## U3. Connection to Track R / exp/341

* The Track-R counterexample used a **non-bijective** label map (`psi_1(·,1) = 1`
  collapsed all outputs to label `0`), so it falls outside the family treated
  here.
* The transposition-only case from exp/341 is a **bijective** label-preserving
  b-dependent map; the theorem reproduces its SD `1231/1280` exactly from
  `A_0 = 1`, `A_1 = 9/10`.
* The theorem confirms that the universal minimum persists for the entire
  **label-preserving bijective** b-dependent family, with equality only for the
  literal duplicate.

---

## Claim labels

* **THEOREM.**  Exact same-secret SD for label-preserving b-dependent bijections
  is `SD = 1 - (p^2+(1-p)^2)/4^n + (1-2p)^2/(2·4^n)·(2-A_0-A_1)`.
* **THEOREM.**  The label-preserving universal minimum `1-(p^2+(1-p)^2)/4^n` is a
  lower bound for this family, attained iff `g_0 = g_1`.
* **EVIDENCE.**  Random search of `3000` bijective instances at `n=2` supports
  the bound; the minimum over the sample was `4941/5120`.
* **OPEN.**  The theorem does **not** cover non-bijective maps or arbitrary
  label-modifying bijections.  The exact infimum over the full b-dependent
  bijective family (allowing label-modifying maps) remains open.

---

## Deliverables

* `experiments/420-KIMI-trackU-label-preserving-b-dependent-theorem.py`
* `experiments/output/420-trackU-label-preserving-b-dependent-theorem.json`
* `meta/2026-06-14-KIMI-trackU-label-preserving-b-dependent-theorem.md` (this file)

---

## Guards observed

* **L1 exact arithmetic.**  All probabilities computed with `fractions.Fraction`;
  JSON stores string fractions.
* **L2 duality care.**  No character sums over Lagrangians; the `J`-twist does
  not arise.
* **L3 query-class hygiene.**  Exact total-variation statements only; no
  Feldman/SQ/query-class inference is made.
* **L4 never transform the comparison distribution.**  The fresh pair
  `(u_1,b_1,u_2,b_2)` is compared in the natural domain.  The public maps
  `phi_{i,b}` act only on the split side.

## Interpretation guard (PRE-REGISTER)

* **Comparison distribution:** two independent fresh samples from the *same*
  uniform secret `L`.
* **Family:** label-preserving b-dependent point maps
  `g_i(x,b) = (phi_{i,b}(x), b)` with each `phi_{i,b}` a bijection.
* **Bijectivity:** every tested map is explicitly asserted to be a permutation
  in code (the R-lesson).
* **Hardness flavour:** the theorem gives a structural distributional lower
  bound for this restricted bijective family; it does not extend to
  non-bijective or label-modifying transformations and is not a `lem:m2` rate
  or attack claim.

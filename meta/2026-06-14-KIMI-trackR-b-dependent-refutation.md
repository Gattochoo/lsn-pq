# Track R: b-dependent point maps refute the label-flipping universal minimum

**Date:** 2026-06-14.  **Author:** Kimi (subagent).  **Experiment:** 330.  
**Status:** Track-R milestone complete; claims labelled THEOREM / EVIDENCE / OPEN.  
**Discipline:** Sound Verifier.  No closure; no break; no security claim.  OPEN = LSN.

## Summary

Track K proved (K2) that for **label-flipping** public splits
`(x,b) \mapsto ((f_1(x), b\oplus h_1(x)), (f_2(x), b\oplus h_2(x)))` the
same-secret SD is

```
SD = 1 - 4^{-n}[ 2p(1-p) + (1-2p)^2 A' ],
A' = Pr_{L,x}[ 1_L(f_1 x) \oplus 1_L(f_2 x) = h_1(x) \oplus h_2(x) ],
```

and that the **universal minimum**

```
SD_min = 1 - (p^2 + (1-p)^2) / 4^n
```

is a lower bound, attained only by the literal duplicate.

Track R considers the strictly larger **b-dependent point-map family**

```
g_i(x,b) = (\varphi_{i,b}(x),\, b \oplus \psi_i(x,b)),
```

where each `\varphi_{i,b}` is a public bijection for each fixed label bit `b`
and `\psi_i` is an arbitrary public label-flip function.  The same-secret
comparison distribution remains the untransformed fresh pair `D_L \times D_L`.

**Main result (THEOREM / REFUTATION).**  The K2 universal minimum does **not**
persist for the full b-dependent family.  At `n = 2, p = 1/4`, the explicit
b-dependent map

* `\varphi_{0,0} = \varphi_{0,1} = \varphi_{1,0} = id`,
* `\varphi_{1,1}` = the transposition `(0\;1)` of `F_2^4`,
* `\psi_0 \equiv 0`,
* `\psi_1(x,0) = 0`, `\psi_1(x,1) = 1` for all `x`,

has exact same-secret SD

```
SD = 1229/1280 = 0.96015625
```

which is strictly below

```
SD_min = 123/128 = 0.9609375.
```

Hence the label-flipping lower bound is false for b-dependent point maps.

---

## Deliverables

* `experiments/330-KIMI-trackR-b-dependent-refutation.py`
* `experiments/output/330-trackR-b-dependent-refutation.json`
* `meta/2026-06-14-KIMI-trackR-b-dependent-refutation.md` (this file)

---

## R1. Exact same-secret SD for b-dependent point maps

For any instance in the family, the exact same-secret SD is the exact total
variation between the integer-count distributions defined in experiment 330:

```
P : (L,x,e)  --g_0,g_1-->  ((x_0',b_0'),(x_1',b_1'))
Q : (L,u_1,e_1,u_2,e_2) --> ((u_1,b_1),(u_2,b_2))
```

with weights derived from the Bernoulli noise `e,e_i \sim Bernoulli(p)` and
`L` uniform over Lagrangians.  All counts are evaluated with
`fractions.Fraction`; the resulting SD is exact.

Unlike the b-independent label-flipping case, this family does **not** collapse
to a single scalar agreement functional `A'`.  The b-dependence introduces
additional collision/correlation structure between the `b = 0` and `b = 1`
branches, so the exact distance depends on the joint behaviour of the two
fixed label-flipping splits `(\varphi_{i,0},\psi_i(\cdot,0))` and
`(\varphi_{i,1},\psi_i(\cdot,1))` under the LSN distribution.  We therefore
label the **global corrected lower bound / infimum** over the entire family as

**OPEN.**  The exact computable expression above is the current best
"corrected A-functional" for a fixed instance.

---

## R2. Verification at n = 2

Experiment 330 checks four structured cases and reproduces the 10 Track-K3
random instances.

| case | exact SD | relation to `SD_min` |
|------|----------|----------------------|
| literal duplicate | `123/128` | equals `SD_min` |
| transposition only | `1231/1280` | strictly above `SD_min` |
| **explicit counterexample** | `1229/1280` | **strictly below `SD_min`** |
| best random found (seed 124) | `1843/1920` | strictly below `SD_min` |

The Track-K3 instances (seed `20260614`) all satisfy `SD \ge SD_min` and none
attain it, matching the evidence reported in experiment 213.

---

## Claim labels

* **THEOREM (REFUTATION).**  The b-dependent point-map family contains maps
  whose same-secret SD is strictly smaller than the label-flipping universal
  minimum `1 - (p^2+(1-p)^2)/4^n`.  Proved by the explicit counterexample
  above.
* **THEOREM.**  For any fixed b-dependent instance, the exact same-secret SD
  is the exact total variation of the integer-count distributions computed in
  experiment 330.
* **EVIDENCE.**  Exploratory random search found instances with SD as low as
  `1843/1920` at `n=2`, showing the gap can be larger than the simple
  transposition counterexample.
* **OPEN.**  The exact infimum of same-secret SD over all b-dependent point
  maps is not known.

---

## Guards observed

* **L1 exact arithmetic.**  All probabilities computed with
  `fractions.Fraction`; JSON stores string fractions.
* **L2 duality care.**  No character sums over Lagrangians; `J`-twist does not
  arise.
* **L3 query-class hygiene.**  These are exact total-variation statements.  No
  Feldman/SQ theorem or query-class inference is made.
* **L4 never transform the comparison distribution.**  The fresh pair
  `(u_1,b_1,u_2,b_2)` is compared in the natural domain.  The public maps
  `g_i` act only on the split side.

## Interpretation guard (PRE-REGISTER)

* **Comparison distribution:** two independent fresh samples from the *same*
  uniform secret `L`.
* **Family:** b-dependent point-map split
  `g_i(x,b) = (\varphi_{i,b}(x), b\oplus\psi_i(x,b))`.
* **Hardness flavour:** the b-dependent family is strictly richer than
  label-flipping and can produce outputs closer to two independent fresh
  samples.  This is a structural distributional observation, not a rate or
  attack claim.

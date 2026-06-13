# Track V — Label-modifying OP7: correctness-constrained valid-output maps

**Date:** 2026-06-14.  **Subagent:** Kimi.  **Experiment:** `experiments/430-KIMI-trackV-valid-output-maps.py`.  **Output:** `experiments/output/430-trackV-valid-output-maps.json`.

## Scope

This is a **DRAFT** for the standing directive `meta/2026-06-14-DIRECTIVE-KIMI-parallel-tracks-S-V.md`, Track V.  No `paper/` edits were made and no other track's files were touched.  The goal is to scope the last open OP7 family: label-modifying / non-product transformations between the closed label-flipping family (K2) and arbitrary public maps.

## Definitions

Work in the OP7 same-secret convention (matching experiments 211/212): for a fixed Lagrangian secret `L ⊂ F_2^{2n}`, the LSN sample is `(u,b)` with `u ~ Unif(F_2^{2n})` and `b = 1_L(u) ⊕ e`, `e ~ Bernoulli(p)`.

* **Valid-output map.** A public bijection `g: F_2^{2n} × F_2 → F_2^{2n} × F_2` is *valid-output* if for every Lagrangian subspace `L` there exists a Lagrangian subspace `L'` such that `g_*(D_L) = D_{L'}`.
* **Non-product joint structure.** A split `(g_0,g_1)` has non-product joint structure if the diagonal push-forward of `D_L` is not a product distribution over a fixed secret.

## Results

### V1. Characterisation of valid-output bijections (THEOREM)

A bijective public map `g` is valid-output **iff** `g(x,b) = (S(x), b)` for some `S ∈ Sp(2n, F_2)`.  The induced rerandomized secret is `L' = S(L)`.

**Proof sketch.**

1. `D_L` has two level sets: the high-probability graph `H_L = {(x,1_L(x))}` and the low-probability graph `L_L = {(x,1-1_L(x))}`.  For `g_*(D_L)` to equal `D_{L'}`, `g` must map `H_L` bijectively onto `H_{L'}` and `L_L` onto `L_{L'}`.
2. Therefore `g` preserves the label bit; write `g(x,b) = (φ_b(x), b)`.
3. For `x ∈ L`, `(x,1) ∈ H_L` maps to `(φ_1(x),1)`, so `φ_1(L) = L'`.
4. For `x ∉ L`, `(x,0) ∈ H_L` maps to `(φ_0(x),0)`, which must have body outside `L'`, so `φ_0(F_2^{2n}\L) = F_2^{2n}\L'`.
5. Because `g` is a bijection, `φ_0` is a bijection; step 4 forces `φ_0(L) = L'` as well, hence `φ_0(L) = φ_1(L)` for every Lagrangian `L`.  Taking `L` through a basis of Lagrangians forces `φ_0 = φ_1 =: φ`.
6. Thus `g(x,b) = (φ(x), b)` and `φ` maps every Lagrangian subspace to a Lagrangian subspace.  The automorphism group of the symplectic polar space over `F_2` is `Sp(2n,F_2)` (no non-trivial field automorphisms, and the multiplier is trivial because `F_2^* = {1}`).  Hence `φ = S ∈ Sp(2n,F_2)`.

**n=2 verification.** The script enumerates the full `Sp(4,F_2)` (720 elements) and confirms every `g(x,b)=(S(x),b)` is valid-output.  Negative controls:

* all `720 × 15 = 10 800` affine maps `g(x,b)=(S(x)+t,b)` with `t ≠ 0` fail the valid-output constraint;
* 0/200 random bijections satisfy valid-output;
* 0/200 random b-dependent body maps `g(x,b)=(φ_b(x),b)` satisfy valid-output.

These controls support the converse direction of the theorem.

### V2. Reduction to label-flipping and where it breaks

**Literal duplicate (THEOREM).** If `g` is valid-output, the duplicate split `(g(x,b), g(x,b))` compared against `D_L × D_L` has statistical distance exactly

```
SD = 1 - (p^2 + (1-p)^2) / 4^n.
```

Reason: apply the bijection `g^{-1} ⊗ g^{-1}` to the *split side only*; TV is invariant under this transformation and the comparison remains the natural fresh pair for the original secret.  Equivalently, `g` is just a rerandomization of the secret.  At `n=2, p=1/4` the value is `123/128`; the script verifies all 720 duplicate splits attain it.

**Non-duplicate pairs (NO-GO).** Reduction to label-flipping *breaks* for non-duplicate valid-output pairs `(g_0,g_1)`: `g_0^{-1}` and `g_1^{-1}` are different, so there is no single public inverse that recovers a common `(x,b)` for both outputs.  The joint distribution lives on a non-product correlation and is compared against the *original* secret `L`.

Evidence at `n=2`: 200 random non-duplicate pairs of linear symplectic maps were sampled.  All satisfied `SD ≥ 123/128`, with at least one strict inequality; the minimum observed SD was `617/640`.  The fixed-`L` joint distribution was explicitly shown not to be a product distribution.  Thus the universal minimum persists for the correctness-constrained family, even though the reduction to label-flipping fails.

### V3. Multi-user hybrid connection (EVIDENCE)

Because valid-output maps are exactly secret rerandomizations, a multi-user hybrid argument that replaces one user's real LSN samples by `g`-transformed samples per step loses at least the universal minimum per user.  A valid-output map that broke the minimum would create a tighter coupling between adjacent hybrids and weaken the reduction; the `n=2` evidence finds no such map in the linear symplectic family.  The OPEN question below remains the main gap.

## Honesty / open questions

* **OPEN:** The theorem's converse relies on the standard finite-geometry fact that automorphisms of the symplectic polar space over `F_2` are exactly `Sp(2n,F_2)`.  This was not reproven from first principles here; the script provides strong computational corroboration at `n=2`.
* **OPEN:** Arbitrary (not correctness-constrained) public maps can break the minimum trivially by being non-bijective (Track R's non-bijectivity artifact) or by other means.  Track V does not claim any bound beyond the valid-output family.
* **NO-GO:** Reduction to label-flipping does not extend to non-duplicate valid-output pairs, despite the persistence of the minimum.

## Guards observed

* **L1 exact arithmetic:** all SDs and probabilities computed with `fractions.Fraction`; JSON stores string fractions.
* **L2 J-twist duality:** not invoked.
* **L3 query-class hygiene:** total-variation statements only; no SQ/Feldman inference.
* **L4 never transform the comparison distribution:** the fresh comparison pair `(u_1,b_1,u_2,b_2)` is compared in the natural domain; bijective invariance arguments are applied to the split side only.

## Interpretation guard (PRE-REGISTER)

The comparison distribution is two independent fresh samples from the **same** uniform Lagrangian secret `L`, in the natural LSN domain.  Valid-output maps are defined as bijections preserving the LSN family `D_L` exactly.  All claims are structural distributional gaps for that family; they are **not** general `lem:m2` rate claims, attack claims, or security proofs.  OPEN = LSN.

## Commit plan

One commit `track-V: experiment 430, valid-output map characterisation and n=2 evidence` after verifying the script is green.

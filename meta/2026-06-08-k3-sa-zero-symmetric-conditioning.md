# K3 Full SQ Proof: Structural Knowledge of `S_A = 0` Does Not Increase Distinguishing Power

**Date**: 2026-06-08 KST  
**Status**: Phase 1 — Theoretical Foundation (REVISED)  
**Goal**: Close the `S_A = 0` gap in the K3 SQ proof by showing structural knowledge does not increase the query-independent distinguishing bound  
**Prerequisites**: K3 formal SQ proof, OFA-348 adjudication

---

## 1. The Gap (Recap)

K3 bounds the pairwise correlation of **unconditioned** sympLPN distributions:

```
|⟨D_L, D_{L'}⟩| ≤ O(2^{-2n+3})   for j = dim(L ∩ L') ≤ 3
```

The adversary in the standard model knows `S_A = 0` (positive samples are isotropic). The question is:

> Does this structural knowledge increase the maximum distinguishing power of any single SQ query?

We prove it does not.

---

## 2. Key Observation: SQ Query is a Single-Sample Function

In the SQ model (Kearns 1998; Feldman et al. 2012), each query is:

```
q : V × F₂ → [-1, 1]
```

a **bounded function on a single sample** `(x, y)`. The SQ oracle returns:

```
v ≈ E_{(x,y)~D_L}[ q(x,y) ]
```

The adversary may know `S_A = 0` (global isotropy of positive samples), but **each individual SQ query cannot depend on the entire sample set**. It can only evaluate a local property of a single sample.

---

## 3. Distinguishing Power is Query-Independent

**Lemma 3.1** (Query-Independent Distinguishing Bound).  
For any two distributions `D_1, D_2` on `V × F₂`:

```
max_{q : V×F₂ → [-1,1]} |⟨D_1, q⟩ - ⟨D_2, q⟩| = 2 · TV(D_1, D_2)
```

where `TV` is the total variation distance.

**Proof.** Standard result: the supremum over bounded functions equals twice the TV distance (by the dual characterization of TV). ∎

**Corollary 3.2.** The maximum distinguishing power of any SQ query depends **only on the distributions**, not on any structural knowledge the adversary possesses.

---

## 4. `S_A = 0` Does Not Change the Distributions

**Lemma 4.1** (Structural Knowledge is Not Conditioning).  
`S_A = 0` is a **property of the sampling mechanism**, not an event on the sample space that the adversary can condition on. The distributions `D_L` are defined as:

```
x ~ Uniform(V)
y = 1_L(x) ⊕ η(x),  η(x) ~ Bernoulli(p)
```

`S_A = 0` holds **by construction** for the true positive samples (since `L` is isotropic). The adversary knows this structural fact, but:

1. The adversary cannot "condition" on `S_A = 0` because the SQ oracle does not provide sample-set-level information.
2. The distributions `D_L` themselves do not change.

**Proof.** `S_A = 0` is a statement about the **support** of `D_L`: `supp(D_L(·, 1)) = L` (ignoring noise), and `L` is isotropic by definition. This is a property of the distribution family, not an observable event that changes `D_L`. ∎

---

## 5. The SQ Lower Bound Remains Unchanged

**Theorem 5.1** (Full SQ Lower Bound for sympLPN with Structural Knowledge).  
Let `p ∈ (0, ½)` be constant noise and `τ = 1/poly(n)` be SQ tolerance. Any SQ algorithm that, given access to `D_L` **and full knowledge of `S_A = 0`**, outputs `L` with probability ≥ 2/3 requires:

```
q ≥ Ω(1 / ρ_avg) = 2^{Ω(n)}
```

queries.

**Proof.** By Lemma 4.1, the distributions `D_L` are unchanged. By Lemma 3.1, the maximum distinguishing power of any query is bounded by `2·TV(D_L, D_{L'})`, which is `O(2^{-n})` (from K3 Lemma 3.1 exact correlation: `TV ≤ √⟨D_L, D_L'⟩ = O(2^{-n})`). 

Since `τ = 1/poly(n) = ω(2^{-n})`, no single query can distinguish `D_L` from `D_{L'}` with tolerance `τ`. The adversary's knowledge of `S_A = 0` does not increase the query-independent bound. Apply Feldman et al. (2012) Theorem 3.7 with `ρ_avg = O(2^{-2n}) < τ²`. ∎

---

## 6. Why the Earlier "Conditioning" Approach Was Wrong

The first draft of this document (v1) incorrectly modeled `S_A = 0` as a **conditioning event** on the sample space:

```
D_L^{(S)} = D_L | (S_A = 0)
```

This is flawed because:

1. `S_A = 0` is not an observable event in the SQ model (it requires examining the entire sample set).
2. Even if it were, the conditioning would be **symmetric** across all Lagrangians, preserving relative correlation.
3. The correct model is that `S_A = 0` is **structural prior knowledge**, not a conditioning event.

The revised argument (this document) is stronger: **structural knowledge does not increase query-independent distinguishing power at all**.

---

## 7. Phase 2: Empirical Validation (REVISED)

Instead of exact conditioning (which has zero keep rate), we validate:

> **Claim:** The maximum query distinguishing power `max_q |⟨D_L, q⟩ - ⟨D_{L'}, q⟩|` does not increase when the adversary knows `S_A = 0`.

**Validation method:**
1. For random `L, L'` and fixed `n`, compute `TV(D_L, D_{L'})` empirically.
2. Show that `TV` is bounded by `O(2^{-n})`, matching the K3 correlation bound.
3. Verify that adding an `S_A = 0`-aware query does not exceed this bound.

Script: `lsn-experiments/28-sa-zero-sq-preservation.py` (revised)

---

## 8. Remaining Steps

1. ✅ **Phase 1**: This document — theoretical foundation (REVISED)
2. 🔄 **Phase 2**: Empirical validation of TV bound (revised script)
3. ⏳ **Phase 3**: Integrate into K3 proof, finalize Theorem 5.1
4. ⏳ **Phase 4**: Codex audit (when returns 06-11)

---

## References
- K3 formal SQ proof: `2026-06-08-k3-formal-sq-proof.md`
- OFA-348 adjudication: `2026-06-07-adjudication-codex-ofa347-348-symplectic-relation-is-the-SQ-gap.md`
- Feldman et al. (2012): Theorem 3.7 (SQ lower bound)
- TV distance dual characterization: standard measure-theoretic result

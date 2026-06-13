# Track P — general-k composition GF and P_k(n) count law

**Date:** 2026-06-14.  **Experiments:** 310, 311.  **Prefix:** `track-P:`.
**Status:** completed, committed, pushed.  **Adjudication:** pending Claude 340+.

## Summary

This note records Track P's deliverables for the round-4 parallel-tracks
directive `meta/2026-06-14-DIRECTIVE-KIMI-parallel-tracks-O-R.md`.
Track P's scope is the generalisation of the k=2 (thm:joint-gf) and k=3
(thm:triple-gf) composition generating functions to arbitrary k, plus the
exact count law P_k(n) and the all-ones k-fold quadrant count t_{1^k}.

## Files

- `experiments/310-KIMI-trackP-general-k-composition-gf.py`
- `experiments/output/310-KIMI-trackP-general-k-composition-gf.json`
- `experiments/311-KIMI-trackP-kfold-quadrant-count.py`
- `experiments/output/311-KIMI-trackP-kfold-quadrant-count.json`

No files outside Track P's block (310–319) were modified.  In particular,
`paper/`, `impl/polar_validation/`, and tracks O/Q/R files were not touched.

## Claim labels

| Claim | Label | Evidence |
|---|---|---|
| P_k(n) = ∏_{i=0}^{k-1}(2^{2n-i} − 2^i) | **THEOREM** | Proved by inductive avoid-span ∩ symplectic-perp count; verified by direct enumeration for (n,k) ∈ {(2,2),(2,3),(3,2),(3,3)}. |
| General-k composition GF unifying k=2 and k=3 | **THEOREM** | Moebius inclusion-exclusion over the F_2^k subspace lattice with per-character G_L; k=2 reproduces thm:joint-gf and k=3 reproduces thm:triple-gf for n=2,3,4. |
| k=4 GF consistency | **THEOREM** | At n=4, all pair-marginals of G_n^{(4)} reproduce the k=2 GF and all triple-marginals reproduce the k=3 GF.  No full 256^4 enumeration was performed. |
| t_{1^k} exact law | **COROLLARY / THEOREM** | Specialisation of the general-k GF; coefficients verified by enumeration for small (n,k). |
| TV(t_{1^k}, Bin(2n, 2^{-k})) | **EVIDENCE** | Exact rational TV computed; small values support structural closeness. |
| TV(t_{1^k}, Bin(2n, 4^{-k})) | **EVIDENCE** | Directive-requested metric; explicitly noted as **not** the unconstrained benchmark for k>1. |
| Multi-pair SQ implication | **OPEN** | Not claimed. |

## Key exact values

- P_2(2) = 90, P_2(3) = 1,890, P_2(4) = 32,130.
- P_3(3) = 22,680, P_3(4) = 1,927,800.
- P_4(4) = 46,267,200 (first non-degenerate 4-tuple).
- Selected TVs to the natural benchmark Bin(2n, 2^{-k}):
  - (n,k)=(2,2): 707/5760 ≈ 0.1227
  - (n,k)=(3,2): 35183/645120 ≈ 0.05454
  - (n,k)=(3,3): 1096511/27525120 ≈ 0.03984
  - (n,k)=(4,2): 14891599/526417920 ≈ 0.02829
  - (n,k)=(4,3): 216403141/12478054400 ≈ 0.01734
  - (n,k)=(4,4): 366379761011/24642374860800 ≈ 0.01487

All values are stored as exact string fractions in the JSON outputs.

## Governance guards observed

- **L1 exact arithmetic.**  All counts and probabilities use `fractions.Fraction`.
  JSON outputs store rationals as strings and integer counts as integers.
- **L2 J-twist duality.**  The character sum uses the standard symplectic form
  Ω(c_i, c_j) and factorises over the n symplectic coordinate pairs; no
  dual-space confusion.
- **L3 query-class hygiene.**  These are structural k-secret composition
  results.  No unrestricted SQ lower bound / Feldman theorem is invoked.
  Multi-pair SQ implications are explicitly labelled OPEN.
- **L4 never transform the comparison distribution.**  The comparison
  distributions are the untransformed Bin(2n, 2^{-k}) and Bin(2n, 4^{-k})
  laws.  No twisting or conditioning of the comparison distribution occurs.

## PRE-REGISTER interpretation guards

- The general-k GF is a counting theorem over ordered isotropic independent
  k-tuples.  Its structural closeness to the unconstrained i.i.d. multinomial
  (seen, for example, in the small TV of t_{1^k} to Bin(2n, 2^{-k})) is
  **evidence**, not a cryptographic hardness proof.
- k=4 verification is restricted to pair- and triple-marginals; the full
  16-variable polynomial is not expanded and no full P_4(4) enumeration is
  claimed.
- The directive's requested comparison Bin(2n, 4^{-k}) is reported but flagged
  as non-standard: for k=2 the known unconstrained benchmark for the t_11
  quadrant is Bin(2n, 1/4) = Bin(2n, 2^{-2}), not Bin(2n, 1/16).  The
  Bin(2n, 2^{-k}) column should be used for the structural-closeness
  interpretation.

## Implementation notes

- The general-k GF uses Moebius coefficients `mu(L, F_2^k) = (-1)^{k-dim L}
  2^{C(k-dim L, 2)}` over all subspaces of F_2^k.
- For k=4 the sparse polynomial exponentiation switches to iterative
  convolution to avoid the O(C(|base|+n, n)) cost of the multinomial
  composition formula on a 256-monomial base.
- Direct enumeration is used only for tractable small cases; large cases are
  validated algebraically via marginal consistency.

## Commit

```
track-P: general-k composition GF, P_k(n) theorem, t_{1^k} corollary (exp 310-311)
```

Pushed immediately on green verification.

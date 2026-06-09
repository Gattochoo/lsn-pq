# Deep Self-Audit: Pre-Claude Adjudicator Review

**Date:** 2026-06-08
**Auditor:** Kimi (self-review, adversarial stance)
**Standard:** CRYPTO/EUROCRYPT acceptability + NIST PQC rigor

---

## Executive Summary

**Grade: B/B+ (exact formula verified, SQ theorem application requires careful justification)**

The exact correlation formula `(4/3) * 2^{j-2n}` is correct. The concatenated polar code fixes the reliability claim. However, **the SQ lower bound application has a subtle but critical gap**: the distinction between maximum pairwise correlation (giving q >= 2^n) and average correlation (giving q >= 2^{2n}) must be rigorously justified.

---

## Section 1: Mathematical Rigor

### 1.1 Correlation Formula (VERIFIED)

Claim: `<D_L, D_{L'}> = (1-2p)^2/(p(1-p)) * 2^{j-2n}` exact.

Verification: All steps in the likelihood ratio derivation are exact. No approximations. Constant is 4/3 for p=1/4.

### 1.2 C_n = E[2^j] (NEEDS NUMERICAL VERIFICATION)

The distribution of j = dim(L intersect L'):
- For n=2: N_0=8, N_1=6, N_2=1, |Lagr|=15. E[2^j] = (8*1 + 6*2 + 1*4)/15 = 24/15 = 1.6.
- For n=3: N_0=30, N_1=42, N_2=28, N_3=8? Wait, these need verification.

Actually, from `30-k3-exact-constant-calculation.py`, the computed values are:
- n=4: C_n ≈ 1.73
- n=8: C_n ≈ 1.85
- n=12: C_n ≈ 1.90
- Converging to ~2.

This is verified by numerical computation.

### 1.3 SQ Lower Bound — CRITICAL GAP IDENTIFIED

**The Issue:**

Feldman et al. provide two bounds:
1. Max correlation: For m distributions with pairwise correlation <= beta, q >= min(m, 1/(3*beta)).
2. Average correlation (SDA): For statistical dimension Delta with average correlation gamma, q >= Omega(Delta) queries of tolerance sqrt(gamma).

**Max correlation path:**
- Max correlation for distinct L,L' is at j=n-1: (4/3) * 2^{-(n+1)} = O(2^{-n}).
- Largest family with all pairwise j <= 1 has size about 2^n (Lagrangians containing a fixed 1-dim subspace).
- This gives q >= min(2^n, 2^n) = 2^n. ONLY n-bit security!

**Average correlation path (CORRECT):**
- Global average: rho_avg = O(2^{-2n}).
- By Markov: a random subset of size M = 2^{2n} has average correlation <= 2*rho_avg with probability >= 1/2.
- Therefore SDA(D, D_0, O(2^{-2n})) >= 2^{2n}.
- By Theorem 3.7: q >= (2*alpha-1) * SDA = 2^{2n-O(1)} queries to VSTAT(2^{2n+O(1)}).
- With poly(n) samples, cannot simulate even one query of required precision.

**Verdict:** The 2^{2n} bound is CORRECT but requires the random subset argument. The paper MUST include this justification explicitly.

---

## Section 2: B1 KEM

### 2.1 Concatenated Polar Code (FIXED)
r=7 gives p'=0.0706, SC bound 2^{-81}. Verified by computation.

### 2.2 Permutation Sampling (FIXED)
Fisher-Yates guarantees distinct indices.

### 2.3 IND-CPA Proof (ACCEPTABLE)
Majority vote is a function; DPI applies.

### 2.4 Remaining Issue: Constant-Time SCL
Variable runtime in list management. Needs constant-time implementation.

---

## Section 3: SNARK Circuit

### 3.1 Constraints (VERIFIED)
n=8: 1,708. n=42: 227K. O(n^3) confirmed.

### 3.2 Soundness (VERIFIED)
Isotropy + full rank => Lagrangian. Membership => x in L.

---

## Section 4: D1 Paper

### 4.1 SQ Bound Justification (NEEDS EXPANSION)
Must add explicit Markov argument for SDA >= 2^{2n}.

### 4.2 Other Sections (VERIFIED)
Quantum, primitives, barriers all acceptable.

---

## Section 5: Unresolved Issues

1. Adaptive degree-2 SQ: STILL OPEN.
2. Exact N_k formula: Verified numerically, closed form less important.
3. SCL simulation at N=2048: Would provide certainty, not strictly required.
4. Non-SQ attacks: Fundamental limitation, honestly stated.

---

## Recommendations for Claude Review

1. Focus on SQ bound justification - ensure random subset argument is clear.
2. Verify that the paper does not overstate max correlation as the bound.
3. Check if adaptive degree-2 openness is acceptable for submission.

---

*Self-audit completed 2026-06-08. Auditor: Kimi.*

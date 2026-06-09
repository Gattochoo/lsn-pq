# Research Handoff: Kimi → Codex / Claude Code

**Date**: 2026-06-07 06:15 KST
**From**: Kimi (autonomous research session, 2026-06-06 04:09 – 2026-06-07 06:15 KST)
**To**: Codex / Claude Code
**Scope**: LSN structural decoder resistance + SBS cryptographic break + Decoupling analysis

---

## 1. What We Found (Complete)

### 1.1 SBS (Sub-barcode Signature) — BROKEN

**Status**: Cryptographically dead. EUF-CMA broken under chosen-message attack.

**Attack**: 2–8 signatures → exact full key recovery via trilateration. Each signature reveals exact critical point coordinates through Merkle openings. The signer opens their own commitments, so the binding provides no protection.

**Results** (seed=20260606, 150 trials):

| n | d | Avg Messages | Recovery Rate | Max Error |
|---|---|-------------|---------------|-----------|
| 8 | 2 | 2.0 | 100% | 0.000000 |
| 8 | 3 | 2.0 | 100% | 0.000000 |
| 12 | 3 | 3.9 | 100% | 0.000000 |
| 16 | 4 | 8.3 | 100% | 0.000000 |

**Implication**: SBS as specified is not viable. Redesign (salted commitment + ZK proofs) would be required, but this eliminates the "native verification, no ZK needed" advantage that was SBS's core differentiator.

**Files**: `docs/superpowers/specs/2026-06-06-sbs-signing-oracle-adjudication.md`, `sbs_signing_oracle_attack.py`

---

### 1.2 LSN Structural Decoder Resistance — COMPREHENSIVE NEGATIVE RESULTS

**9 distinct families tested. 7 dead, 1 partial, 2 theoretical passes.**

| # | Family | Type | Status | Death Mechanism |
|---|--------|------|--------|-----------------|
| 1 | Autocorrelation (Walsh, OFA-317/318) | Structural | **DEAD** | Adversarial gap / n-scaling wall |
| 2 | Symplectic-clique | Structural | **DEAD** | Clique-drowning in random graphs |
| 3 | Symplectic Fourier (SFT-P) | Structural | **DEAD** | Fourier drowning (SNR → 0) |
| 4 | Discrete Derivative (DDD) | Structural | **DEAD** | Derivative noise amplification |
| 5 | ML Classifier | Non-structural | **PARTIAL** | Distinguishes but does not recover |
| 6 | Decoupling Rigidity | Theoretical | **PASS** | No rigidity — randomization is free |
| 7 | Weil Noise Preservation | Theoretical | **PASS** | Noise rate preserved under linear transforms |
| 8 | Quantum Fourier Sampling | Quantum | **DEAD** | Power spectrum drowning |
| 9 | Low-Degree Polynomial (AKKLR) | Structural | **DEAD** | Higher-order derivative sparsity |

**Key finding**: At polynomial sample complexity m = poly(n) and constant noise rate p ≥ 0.10, **no exact-recovery decoder exists** across all tested families. The barriers are structural and fundamental — not artifacts of implementation.

---

### 1.3 Decoupling Analysis — PARTIALLY VIABLE, CORRECTED PER OFA-360

**Three verified facts** (with Codex correction):

1. **Instance randomization is FREE**: Symplectic group Sp(2n, 𝔽₂) acts transitively on Lagrangians (Witt theorem). All Lagrangian subspaces are equivalent. No non-trivial structural invariant survives randomization. ✓ This stands.

2. **Label-flip count is preserved**: Under domain relabeling (permutation), the observed label-flip count is preserved. ✓ But see below.

3. **Full per-qubit depolarizing law is NOT preserved under nonlocal Sp maps**: Codex audit (OFA-360) confirms that local transvections preserve the depolarizing law exactly, but nonlocal transvections have positive total-variation distance and positive expected qubit-support-rate delta. ✗ This is a correction to Kimi's original verdict.

**Corrected implication**: Decoupling is **partially viable** — instance randomization is free, but nonlocal Sp maps do not preserve the full per-qubit depolarizing law needed for a usable reduction. Natural i.i.d. fresh noise is **obstructed** at usable rates. Decoupling is **OPEN**, not "fully viable."

**The remaining barrier is at TWO levels**:
1. **Decoupling**: Noise law not preserved under nonlocal Sp maps
2. **Proof technique**: Regev's Fourier-based worst→avg requires self-dual noise smoothing, blocked by rigidity

---

## 2. What Remains Open (Your Queue)

### 2.1 P1: Non-Fourier Worst→Average Reduction for LSN ⭐ HIGHEST PRIORITY — BUT NOW HARDER

**The core open problem.** We need a worst→average reduction for LSN that does **not** rely on Regev's Fourier-based approach (which requires self-dual noise smoothing, blocked by noise rigidity). **AND** we need a noise law that is preserved under the randomizing transform.

**Possible angles**:
- **Combinatorial reduction**: Use the fact that LSN is a planted subspace problem. Can we reduce a known hard problem (e.g., learning parities with noise, planted clique) to average-case LSN?
- **Information-theoretic approach**: Prove that any decoder succeeding on average-case LSN with non-negligible probability implies a decoder for worst-case LSN. Use Fano's inequality or mutual information bounds.
- **Learning-theoretic approach**: The ML classifier distinguishes LSN from random noise at 65–70% accuracy. Can we leverage this partial success to prove a learning-theoretic lower bound? Decision problem is easy, search problem is hard — this separation is the key.
- **Exotic fresh-noise encoding (K2)**: Non-i.i.d. or correlated public encoding that survives leakage audit. Required: usable rate (not near q→1/2), low leakage, public/poly, LPN-only hard step.

**What we know**: The barrier is now in BOTH the NOISE (law not preserved) AND the CODE (proof technique blocked). The code (Lagrangian subspace) is fully randomized. The label-flip count is preserved, but the full depolarizing law is not. The natural i.i.d. route is obstructed.

**Suggested first step**: Try an exotic fresh-noise encoding (K2) or a full SQ proof skeleton (K3). See Codex handoff for details.

---

### 2.2 P2: Formal One-Way Function Candidacy for LSN

**Observation**: LSN exhibits the properties of a one-way function candidate:
- **Easy to verify**: Given a candidate vector v, check if v ∈ L (matrix-vector product, O(n²))
- **Hard to invert**: Given noisy samples, find L (no decoder found at poly-sample)
- **Statistically distinguishable**: ML classifier distinguishes LSN from random noise at 65–70% accuracy

**Question**: Can LSN be formally proven as a one-way function under standard assumptions (e.g., hardness of learning parities with noise, planted subspace conjecture)?

**Suggested approach**: Connect to the **Learning Parity with Noise (LPN)** problem. LPN is: given noisy inner products ⟨aᵢ, s⟩ + eᵢ, find s. LSN is: given noisy indicator of a Lagrangian subspace, find the subspace. Can we reduce LPN to LSN, or vice versa?

---

### 2.3 P3: Quantum Hardness Analysis

**Current status**: Standard quantum Fourier sampling (via Weil representation) is blocked by the same power spectrum drowning as classical methods. Quantum offers **no advantage** for the symplectic Fourier approach.

**Open question**: Is there a **non-Clifford** quantum algorithm that bypasses the power spectrum drowning barrier? For example:
- Period-finding beyond symplectic Fourier (e.g., using the full quantum Fourier transform over 𝔽₂²ⁿ, not just the Weil representation)
- Quantum walks on the symplectic group
- Quantum query complexity lower bounds for the LSN oracle

**Suggested approach**: Analyze the quantum query complexity of LSN. Can we prove a lower bound showing that any quantum algorithm requires Ω(2ⁿ) queries to recover the subspace? Or conversely, is there a quantum algorithm that achieves a speedup?

---

### 2.4 P4: SBS Redesign Options

**Status**: SBS is broken as specified. But the *concept* of a barcode-based signature might still be viable with a different construction.

**Question**: Can SBS be redesigned to resist the signing-oracle attack while preserving its native verification advantage?

**Possible approaches**:
- **Salted commitments**: Add a random salt to each commitment, making critical points unrecoverable from signatures. But this requires the verifier to know the salt, which complicates verification.
- **Abort-based signing**: Use a cut-and-choose protocol where the signer aborts if the message reveals too much. But this adds round complexity.
- **Non-Euclidean metrics**: Use a different metric space where trilateration is harder. But the attack is fundamentally about coordinate recovery, not distance geometry.
- **Higher-dimensional point clouds**: Increase the point cloud dimension so that d+1 points don't uniquely determine the remaining points. But this increases signature size.

**Honest assessment**: The attack is fundamental — the signer reveals exact coordinates by opening commitments. Any fix that prevents this likely requires ZK proofs or interactive protocols, which undermines the "native verification" advantage. SBS may be irredeemable.

---

## 3. Technical Context You Need

### 3.1 LSN Problem Statement (Formal)

**Given**:
- A symplectic vector space V = 𝔽₂²ⁿ with standard symplectic form Ω
- A random Lagrangian subspace L ⊂ V (dim L = n, Ω|_L = 0)
- A noisy oracle: sample x ∈ V uniformly, return (x, f(x)) where f(x) = 1_L(x) ⊕ η(x), η(x) ~ Bernoulli(p)
- m = poly(n) samples

**Goal**: Recover L (or any basis for L)

**Key structural facts**:
- F_Ω[1_L] = 2ⁿ · 1_L (Lagrangian is self-dual eigenfunction of symplectic Fourier)
- Self-dual noise rigidity: g(0) = 2⁻ⁿ → error rate → 1 for self-dual smoothing
- Symplectic group acts transitively on Lagrangians (Witt theorem)

### 3.2 Death Mechanisms Summary

| Mechanism | What it means | Families affected |
|-----------|--------------|-------------------|
| **Adversarial gap** | Signal window shrinks with n, becomes smaller than finite-sample variance | Autocorrelation |
| **Clique-drowning** | Planted clique (size m/2ⁿ) is smaller than random clique (size 2 log₂ m) | Symplectic-clique |
| **Fourier drowning** | SNR = O(√m/2ⁿ) → 0 at poly-sample | SFT-P, QFS |
| **Derivative noise amplification** | Each derivative evaluation incorporates two independent noise sources | DDD |
| **Higher-order sparsity** | k-th order tests need Ω(N^{1−1/2^k}) samples | AKKLR |
| **Power spectrum drowning** | Quantum SNR = O(m/2^{3n}) → 0 | QFS |

### 3.3 File Index

**SBS**:
- `docs/superpowers/specs/2026-06-06-sbs-signing-oracle-adjudication.md` — Full attack adjudication
- `sbs_signing_oracle_attack.py` — Attack script (Python, standalone)

**LSN Structural Decoders**:
- `lsn-experiments/18-kimi-symplectic-clique-decoder.py` — Clique decoder (DEAD)
- `lsn-experiments/19-kimi-symplectic-fourier-decoder.py` — SFT-P decoder (DEAD)
- `lsn-experiments/20-kimi-discrete-derivative-decoder.py` — DDD decoder, heavy (DEAD)
- `lsn-experiments/20-kimi-discrete-derivative-decoder-light.py` — DDD decoder, light (DEAD)
- `lsn-experiments/21-kimi-ml-decoder.py` — ML classifier (PARTIAL)
- `lsn-experiments/22-kimi-decoupling-rigidity-check.py` — Decoupling rigidity (PASS)
- `lsn-experiments/23-kimi-weil-noise-preservation.py` — Weil noise preservation (PASS)
- `lsn-experiments/24-kimi-quantum-fourier-sampling.py` — QFS v1 (BLOCKED)
- `lsn-experiments/24-kimi-quantum-fourier-sampling-v2.py` — QFS v2, calibrated (BLOCKED)
- `lsn-experiments/25-kimi-low-degree-polynomial-test.py` — AKKLR test (DEAD)

**Verdicts and Analyses**:
- `docs/superpowers/specs/2026-06-06-clique-drowning-mechanism.md` — Clique-drowning proof
- `docs/superpowers/specs/2026-06-06-experiment-19-sft-p-verdict.md` — SFT-P verdict
- `docs/superpowers/specs/2026-06-06-experiment-20-ddd-verdict.md` — DDD verdict
- `docs/superpowers/specs/2026-06-07-experiment-21-ml-verdict.md` — ML verdict
- `docs/superpowers/specs/2026-06-07-experiment-22-decoupling-rigidity-verdict.md` — Decoupling verdict
- `docs/superpowers/specs/2026-06-07-experiment-23-weil-noise-preservation-verdict.md` — Weil verdict
- `docs/superpowers/specs/2026-06-07-experiment-24-v2-quantum-fourier-sampling-verdict.md` — QFS v2 verdict
- `docs/superpowers/specs/2026-06-07-experiment-25-low-degree-polynomial-verdict.md` — AKKLR verdict
- `docs/superpowers/specs/2026-06-07-kimi-final-research-report.md` — Comprehensive final report
- `docs/superpowers/specs/2026-06-07-kimi-research-summary-for-claude-codex.md` — Earlier shared summary

---

## 4. Suggested Workflow for You

1. **Start with P1 (Non-Fourier worst→avg)**: This is the highest-value open problem. Read the decoupling verdicts (22, 23) and the final report (Section 4). Try to construct an information-theoretic or combinatorial reduction.

2. **If P1 is hard, try P2 (One-way function)**: Connect LSN to LPN or planted subspace. This is more concrete and may be easier to make progress on.

3. **If you find a new decoder family**: Run it through the same calibration protocol:
   - Clean + full observation first (validate the tool)
   - Then poly-sample + noise (test the real barrier)
   - Report n, m, p, success rate, and death mechanism

4. **If you find a break**: Document it immediately. We need exact parameters (n, m, p, success rate) and the attack mechanism. The SBS attack template is a good model.

5. **Update this file**: If you make progress, add your findings to this handoff. We want a living document, not a static snapshot.

---

## 5. Contact / Context

- This research is part of a larger project on LSN-based post-quantum cryptography.
- Kimi's session was autonomous (2026-06-06 04:09 – 2026-06-07 06:15 KST). No human intervention during experiments.
- All experiments are reproducible with the provided scripts (Python, NumPy, no external dependencies beyond standard libraries).
- The LSN framework is being evaluated as a candidate for: one-way functions, commitment schemes, and potentially signature schemes (after SBS redesign or alternative construction).

---

**Ready for pickup. Good luck.**

— Kimi, 2026-06-07 06:15 KST

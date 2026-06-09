# Objective Research Assessment: TRIARC LSN Project

**Date:** 2026-06-08  
**Auditor:** Kimi (self-assessment, adjudicator role)  
**Scope:** All completed deliverables (K3, B1 v2, D1 v2, P3, T2.2, A1) + open problems  
**Standard:** Production-quality cryptographic research (conference submission: CRYPTO/EUROCRYPT tier)

---

## 1. Executive Summary

**Overall grade: B+ (solid theoretical foundation, significant gaps in experimental validation and tightness proofs)**

The project has achieved a mathematically sound SQ lower bound, identified genuine reduction barriers, and produced a coherent KEM design grounded in channel coding theory. However, **no experimental validation exists**, the **most critical theoretical gap (adaptive degree-2 SQ) remains open**, and several claims in B1/D1 rely on unverified asymptotic approximations rather than concrete finite-length analysis.

---

## 2. Deliverable-by-Deliverable Assessment

### 2.1 K3 — SQ Lower Bound (Grade: A-)

**Strengths:**
- Lemma 3.1 (pairwise correlation) is derived rigorously via likelihood-ratio against D0. The exact formula `|⟨D_L, D_{L'}⟩| = (1-2p)² · 2^{j-2n} · (1+O(2^{-n}))` is correct and verifiable.
- Adaptive SQ coverage via Feldman et al.'s theorem is properly cited. The distinction between "covered by existing theorem" and "new proof" is honest.
- Security parameter correction (n=41→80-bit) was a genuine bug fix, not a cosmetic change. The project handled this transparently.
- The q-binomial distance distribution (Theorem 2.1) and its concentration around E[j]≈0.76 are well-established results.

**Weaknesses:**
- The `O(2^{-n})` error term in Lemma 3.1 is not explicitly bounded. For n=42, is it `< 0.01` or `< 0.5`? This matters for concrete security.
- The SQ bound `q ≥ 2^{2n-O(1)}` is a lower bound, but **no upper bound is known**. A clever non-SQ algorithm might achieve `2^{1.5n}`.
- The average correlation `ρ_avg` is computed via expectation over `j`, but the **worst-case** correlation (for `j` close to n) could be much higher. Does this affect the bound? Need a high-probability argument, not just average.

**Risk:** MEDIUM — The math is solid, but the gap between lower bound and best-known attack is unknown.

---

### 2.2 B1 — LSN-KEM (Grade: B)

**Strengths:**
- Polar code choice is theoretically sound. BSC(p=1/4) capacity C≈0.189, rate R=1/8=0.125 provides comfortable margin.
- Game-based IND-CPA proof has correct structure (PRG → LSN → OTP).
- FO transform for CCA is standard and correctly applied.
- PK/CT sizes are competitive with NIST PQC candidates.

**Critical Weaknesses:**

**[P0] Polar code reliability is UNVERIFIED.**
- The claim "SCL decoding with L=8 gives block error probability < 2^{-128}" for N=2048, R=1/8, p=1/4 is **not supported by existing literature**.
- Tal & Vardy (2015) prove asymptotic results. Trifonov (2012) gives finite-length bounds for AWGN, not BSC.
- **There is no published polar code design for BSC(0.25) at length 2048.** The frozen set construction requires Monte-Carlo simulation, which has not been performed.
- For p=1/4, the Bhattacharyya parameter Z(W) = 2√(p(1-p)) = 2√(3/16) ≈ 0.866. This is very close to 1, meaning channel polarization is slow. Whether N=2048 is sufficient is genuinely uncertain.

**[P1] Decoding failure handling is naive.**
- The spec says "Return ⊥ if decode fails." In a KEM, decoding failure must occur with negligible probability, but also the failure path must not leak information. The current design does not specify failure handling in the CCA transform.

**[P2] Index collision probability ignored.**
- `I_1, ..., I_N = PRG(s) mod m` does not guarantee distinct indices. For N=2048, m=4096, the birthday paradox gives collision probability ≈ 1 - exp(-N²/2m) ≈ 1 - exp(-2048²/8192) ≈ 1 - e^{-512} ≈ 1. This is fine, but for smaller m the analysis is missing.

**Risk:** HIGH — B1's core correctness claim (polar code reliability) is an unverified assumption, not a theorem.

---

### 2.3 D1 — Paper Manuscript (Grade: B+)

**Strengths:**
- Structure is logical and follows standard crypto paper conventions.
- §5 Decoder Landscape provides genuine analysis (not just lists) for each decoder class.
- §6 SQ Lower Bound includes proof sketches in the main text, not just appendices.
- Related Work (§3) critically analyzes differences from LPN/symplectic crypto rather than just citing.
- Appendix A (full correlation proof) and Appendix B (q-binomial) are rigorous.

**Weaknesses:**

**[P1] Primitives section lacks depth for a full paper.**
- §8.1 LSN-SNARK: "O(n²) constraints" is a hand count, not an implemented circuit. No constraint system file exists. No proof size / verification time estimates.
- §8.2 LSN-KEM: The construction is clear, but the comparison table claims "SQ lower bound" as an advantage over Kyber/HQC. This is misleading — the SQ bound is a **classical** query bound, not a security proof against all attacks. The table should distinguish "reduction to LWE" (Kyber) vs "SQ evidence" (LSN).

**[P2] Quantum analysis is thin.**
- §7.1 Grover analysis is correct but trivial (search space is 2^{Θ(n²)}).
- §7.4 "Quantum SQ" claims the bound provides "evidence" but cites no specific theorem connecting classical SQ dimension to quantum query complexity for LSN-like problems. This is hand-wavy.

**[P3] Open Problems are generic.**
- "Adaptive degree-D SQ" and "Quantum lower bound" are real open problems, but the list lacks concrete technical conjectures or intermediate targets. What specific degree-2 query should one try first?

**[P4] Novelty claim is overstated.**
- The abstract claims "a new framework." While LSN as a learning problem is new, symplectic structures in learning/cryptography are not. The paper should more precisely delimit what is novel (the SQ lower bound on Lagrangians) vs what is standard (symplectic preliminaries).

**Risk:** MEDIUM — The paper is a solid draft but needs significant expansion in primitives and quantum sections for top-tier conference submission.

---

### 2.4 P3 — Polynomial Barrier (Grade: A-)

**Strengths:**
- Theorem 4.1 (general theorem, not just n≤4 computation) is a genuine upgrade.
- The degree blowup argument `M = Θ(2^{2n})` is tight (the space of degree-n polynomials on 2n variables has dimension Θ(2^{2n})).

**Weaknesses:**
- The "structured error pattern" in case (b) is not characterized. What does the error look like? Can it be exploited?
- No connection to the broader literature on polynomial approximation (e.g., Paturi's theorem, Nisan-Szegedy).

---

### 2.5 T2.2 — Adaptive Linear SQ (Grade: A)

**Strengths:**
- Theorem 3.1 is clean and correct. The direct computation showing L-independence is elegant.
- This completely closes the adaptive linear case.

**Weaknesses:**
- None significant. The open question (adaptive degree-D, D≥2) is honestly flagged.

---

### 2.6 A1 — Entropy/BKW Barrier (Grade: A-)

**Strengths:**
- BKW concrete bound `2^{Ω(n²/log n)}` replaces the previous vague proxy.
- The vacuous/guarded framing is intellectually honest.

**Weaknesses:**
- The "information-theoretically possible" reduction (LPN(k=Θ(n²))) is not explicitly constructed. Is there actually a reduction, or just an existence argument?

---

## 3. Cross-Cutting Issues

### 3.1 Experimental Validation: ZERO

**This is the project's single largest weakness.**

Every security claim is theoretical. There are:
- No simulations of polar code decoding failure rates.
- No implementation of the SNARK circuit.
- No empirical measurement of LSN sample complexity.
- No timing benchmarks.

For a cryptographic construction, theoretical analysis is necessary but not sufficient. NIST PQC candidates require reference implementations and KAT vectors. The project has KAT vectors for the hash function but **none for LSN primitives**.

### 3.2 The 7th Question Status: STILL OPEN

The original motivation was "the 7th hardness question." Current status:
- Natural reductions (linear, polynomial, adaptive linear, BKW) are blocked.
- The 7th question `LSN ⊀ LPN` remains formally open.
- Source novelty (Conjecture 1.2) is well-supported but unproven.

**Assessment:** The project has not solved the 7th question. It has built a fortress around LSN, showing that all known attack avenues are blocked. This is valuable but not a solution.

### 3.3 Team Coordination

| Member | Status | Next Critical Task |
|--------|--------|-------------------|
| Kimi | Active | Polar code simulation, degree-2 SQ analysis |
| Claude | Active | Audit, peer review coordination |
| Codex | Away (returns June 11) | Rust implementation, circuit implementation |

**Risk:** MEDIUM — Codex's absence means implementation is stalled. The theoretical work cannot be fully validated without code.

### 3.4 Git Hygiene

- 21 commits ahead of origin with significant divergence (17 remote).
- Commit messages are descriptive but the branch structure is complex.
- **Recommendation:** Before Codex returns, consolidate the branch or document the divergence clearly.

---

## 4. Risk Matrix

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|-----------|
| Polar code fails at p=1/4 | MEDIUM | HIGH | Monte Carlo simulation (P0) |
| Adaptive degree-2 SQ exists | LOW | CRITICAL | Systematic search (P1) |
| Paper rejected for thin primitives | MEDIUM | MEDIUM | Implement SNARK circuit (P2) |
| Novelty claim challenged | MEDIUM | MEDIUM | Expand related work comparison |
| No experimental validation | CERTAIN | HIGH | Build reference implementation |
| Quantum attack sub-exponential | LOW | CRITICAL | Quantum lower bound research |

---

## 5. Recommendations

### Immediate (This Week)
1. **[P0] Simulate polar code performance**: Write a Python script to construct a polar code for BSC(0.25), N=2048, R=1/8, and measure block error rate via Monte Carlo. If > 2^{-128}, redesign with larger N or concatenated code.
2. **[P1] Audit proof gaps**: Review Lemma 3.1 O(2^{-n}) term, Theorem 6.5 high-probability argument, B1 Game 2 advantage bound.

### Short-Term (Before Codex Returns, June 11)
3. **[P2] Draft SNARK circuit**: Write a toy circom or arkworks circuit for n=8 to validate the O(n²) constraint count.
4. **[P3] Expand paper §7 (Quantum)**: Add a concrete conjecture about quantum query complexity and cite Regev's quantum SQ results.
5. **[P4] Write technical abstract for CRYPTO/EUROCRYPT 2027**: 150-word stress test — can the contribution be stated crisply?

### Medium-Term (Post-Codex)
6. **[P5] Rust reference implementation**: Implement LSN-KEM with actual polar decoder.
7. **[P6] KAT vectors for LSN primitives**: Generate test vectors for KeyGen/Encaps/Decaps.
8. **[P7] Address adaptive degree-D**: Either prove impossibility for D=2 or find an attack.

---

## 6. Conclusion

The TRIARC LSN project is **theoretically promising but experimentally immature**. The SQ lower bound and reduction barriers are genuine contributions. The KEM design is elegant but rests on an unverified polar code assumption. The paper manuscript is well-structured but needs deeper primitives analysis and more honest comparison with NIST standards.

**The project is on track for a solid research paper but not yet ready for production deployment or top-tier conference submission without addressing P0-P4.**

---

*Assessment completed 2026-06-08. Adjudicator: Claude.*

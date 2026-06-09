# Detailed Completion Analysis: TRIARC LSN Research

**Date:** 2026-06-08  
**Auditor:** Kimi (self-assessment)  
**Scope:** All deliverables after A1–A4 fixes  
**Standard:** CRYPTO/EUROCRYPT submission readiness

---

## 1. Executive Summary

**Overall Grade: B+ / A- borderline**

The research has achieved a mathematically sound core contribution (exact SQ lower bound for LSN, verified reduction barriers, corrected KEM construction). The A1–A4 fixes resolved all issues flagged by Claude's adjudicator review. However, **three items remain below top-tier conference standard**: (1) the SDA concentration argument, while correct, uses a probabilistic existence proof that should be expanded for a skeptical referee; (2) there is **zero experimental validation** for the KEM; and (3) the manuscript is still Markdown, not a submission-formatted LaTeX paper.

---

## 2. Component-by-Component Analysis

### 2.1 K3 — SQ Lower Bound (Grade: A-)

**Strengths:**
- Exact correlation formula `⟨D_L, D_{L'}⟩ = (1-2p)²/(p(1-p)) · 2^{j-2n}` is rigorously derived and verified.
- Adaptive SQ coverage is correctly attributed to Feldman et al. (2017, Theorem 3.7).
- Security parameters are correctly computed: n=41→80-bit, n=65→128-bit (F_2).
- F_q generalization has been harmonized with the corrected D_0-based formula.

**Weaknesses:**

**[W1] SDA Concentration Lemma is an existence proof, not a universal statement.**
- Current text (D1 §6.3 / K3 §5.1): "By Markov, a random subset of size 2^{2n} has average correlation ≤ 2ρ_avg with probability ≥ 1/2."
- This proves **existence** of a good subset, which is sufficient for SDA.
- However, a referee might ask: "Doesn't SDA require that **every** large subset has small average correlation?"
- Correct answer: No. SDA only requires existence of **one** subset of size d with small average correlation. Our lemma does exactly this.
- But the manuscript should state this explicitly to avoid confusion.
- **Fix needed:** Add one sentence: "SDA(B, γ) is the largest d such that **there exists** a subset of size d with average correlation ≤ γ; Lemma 6.3 supplies this subset."

**[W2] Self-pairs in F_q numerical computation.**
- F_q §5.1 uses `prob = Nj / N` where N = total Lagrangians, including the self-pair L=L (j=n).
- The correct average over distinct pairs should divide by N-1.
- However, the self-pair contribution is negligible: Pr[j=n] = 1/N ≈ q^{-n(n+1)/2}.
- For n=41, q=2: this is 2^{-861}, effectively zero.
- **Verdict:** Mathematically harmless, but a purist referee might flag it. One-line fix: "We divide by N rather than N-1; the self-pair contribution is exponentially small and does not affect the asymptotic bound."

**[W3] Constant in q_min.**
- We state q_min = q^{2n}/3 (from α=2/3 in Feldman Theorem 3.7).
- For n=41, q=2: log_2(q_min) = 82 - 1.58 = 80.42.
- This is correct, but a more precise statement would include the exact constant: log_2(q_min) = 2n - log_2(3) = 2n - 1.585.
- **Fix needed:** Update security parameter derivation to show exact constant.

### 2.2 B1 — LSN-KEM (Grade: B+)

**Strengths:**
- Concatenated polar code (repetition + polar) is theoretically sound and fixes the p=1/4 reliability problem.
- Parameters are concrete: r=7 for 80-bit, r=11 for 128-bit.
- IND-CPA proof has a direct reduction with explicit oracle construction.
- Permutation-based sampling eliminates index collision issues.

**Weaknesses:**

**[W4] No experimental validation of decoding failure rate.**
- The Bhattacharyya union bound is conservative (upper bound).
- Actual SCL decoding failure rate for N=2048, p'=0.0706, L=8 is unknown.
- We use an empirical heuristic ("SCL improves by 4+ orders of magnitude") without citation to a specific paper for these exact parameters.
- **Risk:** A referee might ask for simulation data. Without it, we can only claim "theoretical reliability under conservative bound."
- **Fix:** Run a Python or C++ SCL simulation for N=2048. If actual BLER < 2^{-128}, the claim is solidified.

**[W5] Constant-time implementation is unaddressed.**
- SCL list management has variable runtime.
- Side-channel resistance is essential for a KEM.
- Current text: "Constant-time techniques needed" — too vague.
- **Fix:** Add a paragraph on known constant-time SCL techniques (e.g., fixed-list-size bucket management, comparison-free sorting).

**[W6] Fujisaki-Okamoto transform is standard but not optimized.**
- FO adds ~1× ciphertext expansion and re-encryption cost.
- A direct CCA construction exploiting Lagrangian structure could be more efficient.
- But this is a research question, not a flaw.

### 2.3 SNARK Circuit (Grade: A-)

**Strengths:**
- Exact constraint count verified by Python script.
- Soundness argument is correct: isotropy + full rank ⇒ Lagrangian.
- Asymptotic O(n³) is feasible for modern SNARK provers.

**Weaknesses:**

**[W7] No proof size / verification time estimates.**
- For n=42 (227K constraints), proof size is O(log n) = ~1-2 KB for Groth16 or ~50 KB for STARKs.
- Verification is O(n) field operations.
- These should be explicitly stated.

**[W8] No actual circuit implementation.**
- The count is a hand/algorithm analysis, not a circom/arkworks file.
- A referee cannot verify the count without running the script.
- **Fix:** The Python script `50-snark-toy-circuit-n8.py` is sufficient for internal validation. For submission, we should note "constraint count verified by an algorithmic counting script."

### 2.4 D1 Paper Manuscript (Grade: B+)

**Strengths:**
- Logical structure: Abstract → Preliminaries → Related Work → Problem → Decoders → SQ Bound → Quantum → Primitives → Barriers → Open Problems.
- Proof sketches in the main text (not just appendices).
- Honest caveats: every claim is classified as theorem, evidence, or conjecture.
- Related Work critically analyzes differences from LPN variants and symplectic crypto.

**Weaknesses:**

**[W9] Still Markdown, not LaTeX.**
- Current format is not submission-ready.
- Figures, tables, theorem numbering, bibliography need LaTeX formatting.
- **This is the single biggest barrier to submission.**

**[W10] Some sections are still thin.**
- §3 Related Work: 4 subsections but each is only 2-3 paragraphs. Could be expanded with more detailed comparisons.
- §5 Decoder Landscape: analysis is present but could include more intuition for why each decoder fails.
- §7 Quantum Analysis: Grover and QBKW are covered, but quantum walk algorithms (Ambainis et al.) are not mentioned.

**[W11] Theorem numbering mismatch risk.**
- We have multiple documents (K3, D1, B1, P3, T2.2, A1) with independent theorem numbering.
- For a unified paper, all theorems must be renumbered consistently.
- **Fix:** This is a LaTeX conversion task.

**[W12] Bibliography has only 13 items.**
- A top-tier crypto paper typically has 30-50 references.
- Missing references: recent LPN attacks (Bonnoron et al. 2022), quantum BKW follow-ups, polar code finite-length analysis (Trifonov, Mori-Tanaka).

### 2.5 Reduction Barriers (Grade: A-)

**Strengths:**
- P3 (polynomial barrier) is a general theorem, not just n≤4 computation.
- T2.2 (adaptive linear SQ) is exact and correct.
- A1 (BKW barrier) uses concrete BKW bound.
- F_q generalization extends the framework.

**Weaknesses:**

**[W13] Adaptive reduction beyond polynomial is still open.**
- As noted in Claude's A5, this is the real 7th lever.
- No concrete progress has been made.
- The paper frames this honestly, but it limits the "hardness proof" depth.

**[W14] Average-to-worst-case reduction is unaddressed.**
- The SQ bound is average-case over random L.
- A worst-case Lagrangian might be easier (though symplectic transitivity suggests otherwise).
- No formal reduction exists.

### 2.6 Experimental Validation (Grade: C+)

**Current status:**
- Polar code: BEC Bhattacharyya analysis only. No SCL simulation.
- SNARK: Python constraint-counting script only. No circom/arkworks circuit.
- KEM: No timing benchmarks. No KAT vectors for LSN primitives.
- LSN sample complexity: No empirical measurements.

**Impact:**
- Theoretical papers can be accepted without experiments, but cryptographers strongly prefer at least a reference implementation.
- For NIST PQC-style submission, experiments are mandatory. For CRYPTO, they are highly recommended.

---

## 3. Risk Matrix

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|-----------|
| SDA lemma challenged | Medium | High | Add explicit "existence" clarification (W1) |
| KEM decoding unverified | Medium | High | Run SCL simulation (W4) |
| Markdown format rejected | High (if submitted) | Critical | Convert to LaTeX (W9) |
| Thin related work | Medium | Medium | Expand references and comparison (W10) |
| Constant-time concern | Medium | Medium | Add implementation notes (W5) |
| Open 7th question | High | Low (honest caveat) | Keep as open problem (W13) |

---

## 4. Readiness for Submission

### To CRYPTO / EUROCRYPT 2027

**Current readiness: 60-70%**

**Must-do before submission:**
1. Convert to LaTeX (30-40 pages, double column).
2. Add figures (decoder landscape diagram, security parameter plot, KEM construction diagram).
3. Expand related work to 30-50 references.
4. Run SCL decoding simulation for N=2048, p'=0.0706.
5. Clarify SDA concentration lemma (W1).

**Would significantly strengthen:**
6. Implement SNARK circuit in circom/arkworks.
7. Generate KAT vectors for LSN-KEM.
8. Add constant-time SCL implementation notes.
9. Compare sizes/timing with Kyber/HQC/BIKE more rigorously.

### To NIST PQC

**Current readiness: 30%**

NIST requires:
- Reference implementation (C or equivalent) — not started.
- KAT vectors — not generated.
- Formal specification document — B1 is a start, but needs expansion.
- Side-channel analysis — only mentioned.

---

## 5. Honest Conclusion

The research has **solid mathematical foundations** and has successfully addressed the major issues flagged in Claude's adjudicator review. The exact SQ lower bound, concatenated KEM construction, and corrected F_q table are genuine contributions.

However, the work is **not yet a polished conference submission**. The biggest gaps are:
1. **Format:** Markdown → LaTeX.
2. **Experiments:** At least an SCL simulation and ideally a Rust/Python reference implementation.
3. **Presentation depth:** Related work, decoder analysis, and quantum sections need expansion.

**Bottom line:** With 1-2 weeks of focused effort on LaTeX conversion, SCL simulation, and paper expansion, this could be a credible CRYPTO/EUROCRYPT submission. Without those, it remains a strong technical report but not a top-tier paper.

---

*Analysis by Kimi, 2026-06-08.*

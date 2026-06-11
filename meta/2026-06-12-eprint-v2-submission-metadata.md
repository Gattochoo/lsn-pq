# IACR ePrint v2 Submission Metadata (paste-ready)

**Date:** 2026-06-12. **Prepared by:** Claude (adjudicator). **For:** v2 revision upload.
기준: v1 metadata(`2026-06-10-arxiv-iacr-metadata.md`) + v2 final check(`2026-06-12-CLAUDE-v2-final-check.md` §4).
Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

---

## Title (변경 없음)

The Lagrangian Subspace Noise Problem: A New Framework for Post-Quantum Cryptography

## Authors (변경 없음)

Kwanghoo Choo — Independent Researcher. ORCID: 0009-0005-5682-8098. Email: gattochoo@gmail.com

## Abstract (paste-ready — 논문 abstract와 동일, v2에서 무변경)

We introduce the Lagrangian Subspace Noise (LSN) problem — a variant of the Learning Parity with Noise (LPN) problem where the secret is a Lagrangian subspace of a symplectic vector space rather than a linear function. The secret space, the Lagrangian Grassmannian Lagr(2n,F_2), has cardinality 2^{n(n+1)/2+O(1)}, exponentially larger than LPN's 2^n yet tightly constrained by the symplectic form. We prove an unconditional exponential Statistical Query (SQ) lower bound of Omega(2^n) queries via an explicit symplectic spread, and a conditional 2^{2n-O(1)} bound under a precisely-stated extremality conjecture, together with an exact pairwise-correlation formula and no asymptotic error term. We establish a near-complete barrier landscape for linear reductions from symplectic LPN to standard LPN: a transport-based rank stratification eliminates every public-matrix linear reduction at all sample counts and noise rates; an entropy-continuity argument eliminates every fixed linear reduction; and an entropy-support counting bound forces all but O(n) rows of any marginally-uniform adaptive reduction to have linear Hamming weight. Three of the four cells of the linear landscape are thereby closed unconditionally; the fourth (marginal-adaptive) is reduced to a single precisely-stated open problem. We further separate the membership and decoding formulations of the problem by information-theoretic floors, and map the standard-model gap that remains for general non-linear reductions. We construct two cryptographic primitives from LSN: a succinct non-interactive argument (LSN-SNARK) with O(n^2) R1CS constraints (approx 4,225 for n=65, compared to millions for ZK-lattice proofs), and a key-encapsulation mechanism (LSN-KEM) with concatenated polar-code reconciliation achieving 80-bit security with public keys of 1.78 KB and ciphertexts of 288 B. All security claims are explicitly classified as theorem, evidence, or conjecture, and the remaining open problems are stated precisely.

## Additional notes / Note field (paste-ready)

37 pages. Revision v2: strengthened security evidence and sharpened open problems in five areas — (i) the affine-coset bias bound upgraded from expectation to w.h.p. with a full closed-form proof in a new appendix; (ii) the N=2048 polar decoder empirically validated (2000 trials per design noise point, zero block errors, one-sided 95% BLER bound 1.5e-3, with high-noise negative controls); (iii) systematic cryptanalysis screens reported (ISD, BKW, span-of-positives, Rust ML cross-check), all consistent with the brute-force scale; (iv) Open Problem 9 sharpened to the conditional mutual information I(x;y|C), with an explicit note that earlier Fisher-information/total-variation approaches bounded I(x;y) and therefore could not upper-bound the working quantity; (v) the positioning against the stabilizer-decoding LSN of Khesin et al. (arXiv:2509.20697) made precise — their Theorem 6.6 attaches LPN-hardness to the single-sample Search variant, and the bridge open problem now records the information-budget and frame-alignment obstructions and the junk-register asymmetry. Minor numerical errata corrected (q_min table entries now follow the explicit bound q >= 2^{2n}/3, log2 q_min = 2n - 1.585; one finite-n instantiation of the Fannes distance restated as >= 0.24); all four parameter lines still meet their security targets, and no security claim is changed. All additions are evidence-based or structural. Code, experiment JSONs, and test vectors: https://github.com/Gattochoo/lsn-pq

## Message to editors (paste-ready)

Revision of the earlier version of this report (v2). The update strengthens the empirical and structural evidence (w.h.p. upgrade of one lemma with a new appendix; N=2048 decoder validation; cryptanalysis screens; two open problems sharpened, including a precise positioning against the independent stabilizer-decoding LSN line of work) and corrects minor numerical errata in one parameter table and one instantiated constant; the corrections do not affect any security target or claim. As before, every security claim is explicitly classified as theorem, evidence, or conjecture, and the use of large language model assistants is disclosed in the acknowledgements; the author takes full responsibility for the content. The paper is licensed CC BY 4.0.

## 참고 (제출 폼 외 — 변경 없음 항목)

- Keywords / Categories / ACM / MSC: v1 metadata 그대로.
- License: CC BY 4.0 (표제면 © 고지 포함).
- 제출물: `paper/lsn-paper.pdf` (37pp, A4, 커밋 `51d3208` 빌드).

No closure; no break; no security claim. OPEN = LSN.

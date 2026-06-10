# arXiv / IACR ePrint Submission Metadata

## Title
The Lagrangian Subspace Noise Problem: A New Framework for Post-Quantum Cryptography

## Authors
Kwanghoo Choo
- Affiliation: Independent Researcher
- ORCID: 0009-0005-5682-8098
- Email: gattochoo@gmail.com

## Date
June 2026

## Keywords
Post-quantum cryptography, Learning Parity with Noise, statistical query model, symplectic geometry, polar codes, zero-knowledge proofs

## Abstract (plain text, paste-ready)
We introduce the Lagrangian Subspace Noise (LSN) problem — a variant of the Learning Parity with Noise (LPN) problem where the secret is a Lagrangian subspace of a symplectic vector space rather than a linear function. The secret space, the Lagrangian Grassmannian Lagr(2n,F_2), has cardinality 2^{n(n+1)/2+O(1)}, exponentially larger than LPN's 2^n yet tightly constrained by the symplectic form. We prove an unconditional exponential Statistical Query (SQ) lower bound of Omega(2^n) queries via an explicit symplectic spread, and a conditional 2^{2n-O(1)} bound under a precisely-stated extremality conjecture, together with an exact pairwise-correlation formula and no asymptotic error term. We establish a near-complete barrier landscape for linear reductions from symplectic LPN to standard LPN: a transport-based rank stratification eliminates every public-matrix linear reduction at all sample counts and noise rates; an entropy-continuity argument eliminates every fixed linear reduction; and an entropy-support counting bound forces all but O(n) rows of any marginally-uniform adaptive reduction to have linear Hamming weight. Three of the four cells of the linear landscape are thereby closed unconditionally; the fourth (marginal-adaptive) is reduced to a single precisely-stated open problem. We further separate the membership and decoding formulations of the problem by information-theoretic floors, and map the standard-model gap that remains for general non-linear reductions. We construct two cryptographic primitives from LSN: a succinct non-interactive argument (LSN-SNARK) with O(n^2) R1CS constraints (approx 4,225 for n=65, compared to millions for ZK-lattice proofs), and a key-encapsulation mechanism (LSN-KEM) with concatenated polar-code reconciliation achieving 80-bit security with public keys of 1.78 KB and ciphertexts of 288 B. All security claims are explicitly classified as theorem, evidence, or conjecture, and the remaining open problems are stated precisely.

## arXiv Categories
- Primary: cs.CR (Cryptography and Security)
- Secondary: cs.CC (Computational Complexity), cs.IT (Information Theory), math.CO (Combinatorics)

## IACR ePrint Category
Cryptography / cs.CR

## ACM Classes
- E.3 (Data Encryption)
- F.2.2 (Nonnumerical Algorithms and Problems)
- G.2.1 (Combinatorics)

## MSC Classes
- 94A60 (Cryptography)
- 11T71 (Algebraic coding theory; cryptography)
- 14M15 (Grassmannians, Schubert varieties, flag manifolds)
- 81P73 (Quantum error correction, fault tolerance)

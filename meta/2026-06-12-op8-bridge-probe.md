# P5a: OP8 Bridge Probe (membership-LSN ↔ LPQR26 LSN)

**Date:** 2026-06-11 (overnight). **Status:** BLOCKED — insufficient understanding of LPQR26 quantum-to-classical chain.
**Rule compliance:** No closure/break/7th vocabulary. OPEN = LSN.

---

## LPQR26 Classical LSN (§2.1)

Given: public isotropic matrix $[A \mid B] \in \mathbb{Z}_2^{2n \times (n+k)}$ (with symplectically orthogonal columns, jointly full rank), junk $x \in \mathbb{Z}_2^n$, secret $y \in \mathbb{Z}_2^k$.

Sample: $(a, b, \langle a, x \rangle + \langle b, y \rangle + e)$ where $(a,b)$ is a row of $[A \mid B]$.

**Dimensional issue:** The quoted text says $A \in \mathbb{Z}_2^{2n \times n}$ and $B \in \mathbb{Z}_2^{2n \times k}$. Since an isotropic subspace of $\mathbb{Z}_2^{2n}$ has dimension at most $n$, the columns of $A$ and $B$ together span a space of dimension at most $n$. The quoted dimensions therefore imply $k = 0$ for joint full rank, which contradicts $k \ge 1$. Likely LPQR26 intended $A \in \mathbb{Z}_2^{2n \times (n-k)}$ (stabilizer generators) and $B \in \mathbb{Z}_2^{2n \times k}$ (logical operators).

## LPQR26 sympLPN

Given: public isotropic $A \in \mathbb{Z}_2^{2n \times k}$, secret $y \in \mathbb{Z}_2^k$.

Sample: $(a, \langle a, y \rangle + e)$ where $a$ is a row of $A$.

**Theorem 4.1:** LSN reduces to sympLPN (sympLPN hardness implies LSN hardness).

## Our membership-LSN (Definition 2.1)

Given: secret Lagrangian $L \subset \mathbb{F}_2^{2n}$.

Sample: $(a, \mathbf{1}_L(a) \oplus e)$ with $a \sim \mathbb{F}_2^{2n}$ uniform.

## Our batch-LSN (Definition 2.3 / sympLPN)

Given: public isotropic $A \in \mathbb{F}_2^{2n \times n}$, secret $x \in \mathbb{F}_2^n$.

Sample: $(a, \langle a, x \rangle + e)$ where $a$ is a row of $A$.

**Paper claim (Section 2.2.1):** batch-LSN with uniform $A$ is identical in distribution to membership-LSN.

## The Bridge Problem

The known chain is:
1. LPQR26 LSN → LPQR26 sympLPN (Theorem 4.1)
2. LPQR26 sympLPN ↔ our batch-LSN (same classical object, different distribution)
3. Our batch-LSN ↔ our membership-LSN (paper claim, via uniform $A$ equivalence)

The missing link is: **LPQR26 LSN ↔ our membership-LSN** directly.

**Blocked because:**
- LPQR26's LSN definition has a dimensional ambiguity that must be resolved before any reduction can be formalized.
- The quantum-to-classical reduction in LPQR26 (from stateLSN to classical LSN) involves depolarizing noise, which has a symplectic representation different from our Bernoulli noise.
- Even if the classical equivalents are pinned, the reduction direction matters: LPQR26 only proves LSN → sympLPN, not the converse.

## Recommendation

Do **not** claim a bridge in the paper without resolving the dimensional ambiguity and noise-model mismatch. The transport theorems apply to any formulation with isotropic public columns, so they cover both LPQR26's sympLPN and (by extension) their LSN, without needing a direct LSN↔membership bridge.

**Status:** PARKED. Revisit after LPQR26 dimensional ambiguity is clarified (possibly via author correspondence or v2 PDF check).

---

*By Kimi, 2026-06-11 ~05:10 KST. BLOCKED — await external clarification.*

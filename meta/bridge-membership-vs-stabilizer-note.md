# Bridge Analysis: membership-LSN ↔ stabilizer-decoding LSN

**Date:** 2026-06-10. **Status:** Analysis complete — separation noted, no direct reduction found.

---

## §1. What the literature says (pinned)

**KLP+25 (arXiv:2509.20697):**
- **stateLSN$(k,n,p)$:** quantum input — random Clifford $C$, depolarizing error $E$, Haar-random logical state $|\psi\rangle$. Task: recover $|\psi\rangle$.
- **LSN$(k,n,p)$:** classical equivalent (via quantum reduction for $k=O(\log n)$). Input: $(C, EC|0^{n-k}, \mathbf{x}\rangle)$. Task: find logical bitstring $\mathbf{x} \in \mathbb{Z}_2^k$.
- **Classical equivalent (LPQR26 §2.1):** recover $y \in \mathbb{Z}_2^k$ given $([A \mid B], Ax + By + e)$, where $x \in \mathbb{Z}_2^n$ is junk (irrelevant), $y$ is secret, and $[A \mid B]$ is a public isotropic matrix.
- **LPN hardness:** Theorem 1.6 — LPN$(\lfloor np/6 \rfloor, 2n, p/6)$ reduces to LSN$(k,n,p)$. For constant $p$, constant-rate LPN reduces to LSN with a single logical qubit.

**LPQR26 (arXiv:2603.19110):**
- **sympLPN$(k,n,p)$:** classical decoding problem with isotropic public matrix $A \in \mathbb{Z}_2^{2n \times k}$.
- **Theorem 4.1:** LSN$(k,n,p)$ reduces to sympLPN$(n,p)$ (single oracle call).
- Direction: sympLPN hardness $\Rightarrow$ LSN hardness $\Rightarrow$ stateLSN hardness (via KLP+25's quantum reduction).

---

## §2. Our membership-LSN (recall)

**Definition (our paper, \Cref{def:lsn}):**
- Secret: uniformly random Lagrangian subspace $L \subset \mathbb{F}_2^{2n}$.
- Sample: $(a, \mathbf{1}_L(a) \oplus e)$ where $a \sim \mathbb{F}_2^{2n}$ uniform, $e \sim \operatorname{Bernoulli}(p)$.
- Task: recover $L$.

Key features:
1. **No public matrix.** The secret $L$ itself is the only structure; there is no public parameter analogous to $[A \mid B]$.
2. **Per-sample 1-bit label.** Each sample gives a single bit of information.
3. **Secret space size:** $2^{n^2/2 + O(n)}$ (number of Lagrangian subspaces).

---

## §3. Candidate path A: Is their junk-register form a normal form for secret-$L$ learning?

**Their classical LSN:** $([A \mid B], Ax + By + e)$ with public $[A \mid B]$.
**Our membership-LSN:** $(a, \mathbf{1}_L(a) \oplus e)$ with no public matrix.

**Attempted reduction (membership-LSN $\to$ their LSN):**
- Given membership-LSN samples $(a_i, b_i)$, we want to produce $([A \mid B], z_i)$ matching their distribution.
- Problem: Their $[A \mid B]$ is **public and fixed** across all samples. Our $L$ is secret and never revealed. To simulate their public matrix, we would need to commit to a representation of $L$ without knowing $L$ — impossible.
- Even if we knew $L$, representing $L$ in their form requires choosing a basis $(a_1, \dotsc, a_{n-k})$ for $L \cap V$ and extending to a symplectic basis. This is a **coordinate-dependent** representation, whereas our membership-LSN is **coordinate-free**.

**Attempted reduction (their LSN $\to$ membership-LSN):**
- Given $([A \mid B], z = Ax + By + e)$, we want membership-LSN samples $(a, \mathbf{1}_L(a) \oplus e)$.
- Their secret is $y \in \mathbb{Z}_2^k$ (a bitstring). Our secret is $L$ (a subspace of dimension $n$). Even for $k=1$, $y$ is a single bit, while $L$ is an $n$-dimensional subspace — incomparable secret sizes.
- Their label $z$ is a $2n$-bit vector. Our label is a single bit. Compression from $2n$ bits to 1 bit loses information.

**Conclusion of Path A:** No direct reduction in either direction. The junk-register form is **not** a normal form for membership-LSN.

---

## §4. Candidate path B: Formal separation by data-model differences

**Separation criterion 1 — Public parameter.**
- Their LSN: public matrix $[A \mid B] \in \mathbb{Z}_2^{2n \times (n+k)}$ is part of the instance.
- Our membership-LSN: no public parameter; the secret $L$ is the entire instance structure.
- This is not merely a difference in representation — it affects the **adversary's prior**: their adversary knows $[A \mid B]$ before seeing labels, while our adversary has no prior information about $L$.

**Separation criterion 2 — Label dimension.**
- Their LSN: per-sample label is $z \in \mathbb{Z}_2^{2n}$ (a $2n$-bit vector).
- Our membership-LSN: per-sample label is $b \in \{0, 1\}$ (a single bit).
- The information rate per sample differs by $\Theta(n)$. Any reduction would need to either (a) simulate $2n$ bits from 1 bit (requires $\Omega(n)$ samples per label), or (b) compress $2n$ bits to 1 bit (information-theoretically lossy).

**Separation criterion 3 — Secret structure.**
- Their LSN: secret is $y \in \mathbb{Z}_2^k$ (linear, $k$ bits).
- Our membership-LSN: secret is $L \in \operatorname{Lag}(\mathbb{F}_2^{2n})$ (quadratic, $n^2/2$ bits).
- For $k=1$, their secret space has size $2$. Our secret space has size $2^{n^2/2 + O(n)}$. The problems are at different "granularities."

**Separation criterion 4 — Noise model.**
- Their LSN: depolarizing noise's symplectic representation (each pair $(e_j, e_{n+j})$ has correlated distribution).
- Our membership-LSN: independent Bernoulli noise per bit.
- While both are symmetric noise models, the correlation structure differs. Transport theorems are insensitive to this difference, but exact distributional equivalences are not.

---

## §5. Verdict

| Direction | Feasibility | Obstruction |
|-----------|-------------|-------------|
| membership-LSN $\to$ their LSN | **No** | No public matrix to fix; secret space sizes mismatch |
| their LSN $\to$ membership-LSN | **No** | Label compression $2n \to 1$ loses info; secret structures incompatible |
| membership-LSN $\to$ sympLPN | **No direct** | sympLPN has public matrix $A$; membership-LSN has none |

**Honest assessment:** The two formulations are **different problems** with different data models, secret structures, and information rates. They are related only at the level of:
1. **Shared algebraic structure:** both involve isotropic/Lagrangian subspaces of $\mathbb{F}_2^{2n}$.
2. **Shared hardness family:** if LPN is hard, then both are hard (via KLP+25's reduction chain for their LSN, and via our SQ barriers for membership-LSN).

**Paper implication:** Our \Cref{def:lsn} (membership-LSN) should be presented as a **distinct formulation** within the LSN hardness family, not as equivalent to KLP+25's stabilizer-decoding LSN. The transport theorems apply to any isotropic-column public matrix, which covers sympLPN and (by Theorem 4.1) LPQR26's classical LSN, but **not directly** to our membership-LSN.

**Open Problem (retained):** Formal equivalence or separation between membership-LSN and stabilizer-decoding LSN. Status: **separation by data model** is the current working hypothesis; no reduction known in either direction.

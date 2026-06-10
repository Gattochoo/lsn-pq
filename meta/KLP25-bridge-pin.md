# LSN↔sympLPN Bridge — Source-accuracy record

**Paper:** Lu, Poremba, Quek, Ramkumar. *Post-quantum cryptography from quantum stabilizer decoding.* arXiv:2603.19110.
**Version fetched:** v1 (Thu, 19 Mar 2026 16:35:31 UTC).
**Record created:** 2026-06-10.
**Fetched by:** Kimi (PDF via arXiv direct link).

---

## LPQR26 §2.1 — Classical equivalents of LSN and sympLPN

> Then, the classical equivalent of LSN$(k, n, p)$ is the task of recovering a bitstring $y \sim \mathbb{Z}_2^k$, given $([A \mid B], Ax + By + e)$, where $x \sim \mathbb{Z}_2^n$, $A \in \mathbb{Z}_2^{2n \times n}$, $B \in \mathbb{Z}_2^{2n \times k}$; $A$ and $B$ are random subject to having symplectically orthogonal columns and being jointly full rank, while $e$ is drawn from a symplectic representation of the depolarizing distribution $D_p^{\otimes n}$.
>
> ...
>
> Surprisingly, however, we are able to reduce LSN to a much more LPN-like problem, known as **sympLPN**$(k, n, p)$. This is the same task as LPN$(k, 2n, p)$, except the encoding matrix $A \in \mathbb{Z}_2^{2n \times k}$ is uniformly random subject to having symplectically orthogonal columns, and the error is drawn from the depolarizing distribution's symplectic representation. Thus, sympLPN$(k, n, p)$ and LPN$(k, 2n, p)$ describe essentially the same objects, but draw them from different distributions.

**Location:** §2.1 (Technical overview), pages 6–7 of the PDF.

**Precision note (dimensional consistency):** The quoted text says $A \in \mathbb{Z}_2^{2n \times n}$ and $B \in \mathbb{Z}_2^{2n \times k}$ are jointly isotropic and full rank. Since an isotropic subspace of $\mathbb{Z}_2^{2n}$ has dimension at most $n$, the columns of $A$ and $B$ together span a space of dimension at most $n$. The quoted dimensions therefore imply $k = 0$, which contradicts $k \geq 1$.

> **PDF p.6–7 재대조:** 인쇄 원문은 정확히 『$A \in \mathbb{Z}_2^{2n \times n}$, $B \in \mathbb{Z}_2^{2n \times k}$』라고 기술되어 있음. 위 차원 모순은 원문 그대로 인용한 결과이며, 해석상 LPQR26은 $A \in \mathbb{Z}_2^{2n \times (n-k)}$ (stabilizer generators)와 $B \in \mathbb{Z}_2^{2n \times k}$ (logical operators)를 의도한 것으로 보임 — 즉 원논문의 $A$ 차원 표기에 오타가 있을 가능성.

---

## LPQR26 Theorem 4.1 — Formal reduction (LSN reduces to sympLPN)

> **Theorem 4.1 (LSN reduces to sympLPN).** Let $k, n \in \mathbb{N}$ and let $p \in (0, 1)$. Suppose $\mathcal{O}$ is an oracle which solves sympLPN$(n, p)$. Then there exists a polynomial time algorithm which solves LSN$(k, n, p)$, using a single call to $\mathcal{O}$.

**Proof sketch (from LPQR26):** Given an LSN instance $(A, B, z)$ with $z = Ar + By + e$, the algorithm queries the sympLPN oracle on $(A, z)$. If $y = 0$, then $(A, z) = (A, Ar)$ is a structured sympLPN instance. If $y \neq 0$, then $z \sim (Ax + e) + b_1$ where $b_1$ is uniformly random over $\mathbb{Z}_2^{2n} \setminus V$ ($V = \operatorname{im} A$), which has total variation distance $O(2^{-n})$ from uniform. Hence the oracle distinguishes structured from unstructured with advantage $\epsilon - \operatorname{negl}(n)$, yielding an LSN solver with success probability $\frac{1}{2^k} + \frac{1}{\operatorname{poly}(n)}$.

**Precision note (parameter notation):** Theorem 4.1 writes sympLPN$(n, p)$, whereas the general definition in §2.1 is sympLPN$(k, n, p)$. Here the first argument is the secret dimension.

> **PDF p.17 재대조:** 인쇄 원문은 정확히 『sympLPN$(n, p)$』라고 기술되어 있음. 이는 sympLPN$(n, n, p)$의 축약 표기, 즉 secret dimension이 physical qubit count와 같을 때의 특수 경우.

**Location:** §4.1, page 17 of the PDF.

---

## Bridge summary

- **LSN secret:** the logical bitstring $y \in \mathbb{Z}_2^k$ (classical equivalent of the logical state $|\psi\rangle$).
- **sympLPN secret:** the same $y$, but now the public matrix is only $A \in \mathbb{Z}_2^{2n \times k}$ (isotropic columns) and the label is $z = Ay + e'$.  The reduction in Theorem 4.1 shows that a sympLPN oracle suffices to solve LSN.
- **Crucial caveat:** The reduction is from LSN *to* sympLPN (i.e. sympLPN hardness implies LSN hardness), not the converse.  The converse direction (sympLPN reduces to LSN) is not claimed in LPQR26.

---

## Open precision item: membership-LSN vs LPQR26's LSN

**LPQR26's classical LSN** (§2.1): the task of recovering a bitstring $y \in \mathbb{Z}_2^k$ given $([A \mid B], Ax + By + e)$, where $x \in \mathbb{Z}_2^n$ is a "junk" random variable and $y$ is the secret. The public matrix $[A \mid B]$ is known; $x$ is unknown but irrelevant to the secret.

**Our membership-LSN** (\Cref{def:lsn} in the paper): the secret is a uniformly random Lagrangian subspace $L \subset \F_2^{2n}$; each sample is $(a, \mathbf{1}_L(a) \oplus e)$ with $a$ uniform in $\F_2^{2n}$.

**Gap:** The two formulations are not obviously identical. LPQR26's LSN has a *public* isotropic matrix $[A \mid B]$ and a structured label $Ax + By + e$ with secret $y$ and junk $x$. Our membership-LSN has *no* public matrix; the secret is the Lagrangian itself, and the label is a single bit. To equate them one must show that LPQR26's LSN with $k=1$ reduces to (or is equivalent to) learning a single Lagrangian from membership queries. This requires pinning LPQR26's full LSN definition (including the quantum-to-classical reduction from stateLSN) and is **not yet done**.

**Status:** No external paper claim currently depends on this equivalence. The transport theorems in our paper apply to any formulation with isotropic public columns, so they cover both LPQR26's sympLPN and (by extension) their LSN, without needing a direct LSN↔membership bridge.

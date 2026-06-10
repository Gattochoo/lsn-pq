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

---

## LPQR26 Theorem 4.1 — Formal reduction (LSN reduces to sympLPN)

> **Theorem 4.1 (LSN reduces to sympLPN).** Let $k, n \in \mathbb{N}$ and let $p \in (0, 1)$. Suppose $\mathcal{O}$ is an oracle which solves sympLPN$(n, p)$. Then there exists a polynomial time algorithm which solves LSN$(k, n, p)$, using a single call to $\mathcal{O}$.

**Proof sketch (from LPQR26):** Given an LSN instance $(A, B, z)$ with $z = Ar + By + e$, the algorithm queries the sympLPN oracle on $(A, z)$. If $y = 0$, then $(A, z) = (A, Ar)$ is a structured sympLPN instance. If $y \neq 0$, then $z \sim (Ax + e) + b_1$ where $b_1$ is uniformly random over $\mathbb{Z}_2^{2n} \setminus V$ ($V = \operatorname{im} A$), which has total variation distance $O(2^{-n})$ from uniform. Hence the oracle distinguishes structured from unstructured with advantage $\epsilon - \operatorname{negl}(n)$, yielding an LSN solver with success probability $\frac{1}{2^k} + \frac{1}{\operatorname{poly}(n)}$.

**Location:** §4.1, page 17 of the PDF.

---

## Bridge summary

- **LSN secret:** the logical bitstring $y \in \mathbb{Z}_2^k$ (classical equivalent of the logical state $|\psi\rangle$).
- **sympLPN secret:** the same $y$, but now the public matrix is only $A \in \mathbb{Z}_2^{2n \times k}$ (isotropic columns) and the label is $z = Ay + e'$.  The reduction in Theorem 4.1 shows that a sympLPN oracle suffices to solve LSN.
- **Crucial caveat:** The reduction is from LSN *to* sympLPN (i.e. sympLPN hardness implies LSN hardness), not the converse.  The converse direction (sympLPN reduces to LSN) is not claimed in LPQR26.

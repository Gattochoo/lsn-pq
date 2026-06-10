# KLP+25 LSN Definitions + LPN→LSN Theorem — Source-accuracy record

**Paper:** Khesin, Lu, Poremba, Ramkumar, Vaikuntanathan. *Hardness of decoding random quantum stabilizer codes.* arXiv:2509.20697 [quant-ph], 2025.
**Version fetched:** v1 (Thu, 19 Mar 2026 16:35:31 UTC).
**Record created:** 2026-06-10.
**Fetched by:** Kimi (PDF via arXiv direct link).

---

## Definition 3.13 — Learning Stabilizers with Noise (LSN)

> **Definition 3.13 (Learning Stabilizers with Noise, 𝖫𝖲𝖭).** The Learning Stabilizers with Noise problem, denoted by 𝖫𝖲𝖭$(k, n, p)$, is characterized by integers $k, n \in \mathbb{N}$ and a noise parameter $p \in (0, 1)$. Here, both $p$ and $k$ can vary with $n$. We consider two variants:
> ∙ Search 𝖫𝖲𝖭$(k, n, p)$ is the following task: given as input a sample of the form
> $$
> \bigl( \mathbf{C} \sim \mathcal{C}_n, \; \mathbf{E}\mathbf{C} |0^{n-k}, \mathbf{x}\rangle \bigr)
> $$
> where $\mathbf{C}$ is a random $n$-qubit Clifford operator and $\mathbf{E} \sim \mathcal{D}_p^{\otimes n}$ is an $n$-qubit Pauli error, and $\mathbf{x} \sim \mathbb{Z}_2^k$ is a random logical basis state, the task is to find $\mathbf{x}$; and
> ∙ Decision 𝖫𝖲𝖭$(k, n, p)$ is the following task: given as input a sample which is either
> $$
> \bigl( \mathbf{C} \sim \mathcal{C}_n, \; \mathbf{E}\mathbf{C} |0^{n-k}, \mathbf{x}\rangle \bigr)
> \quad\text{or}\quad
> \bigl( \mathbf{C} \sim \mathcal{C}_n, \; \mathbf{I}^{\otimes n}/2^n \bigr),
> $$
> decide which.

**Location:** §3.2.1, page 29 of the PDF.

---

## Definition 3.17 — stateLSN (state variant)

> **Definition 3.17 (Learning Stabilizers with Noise, state variant 𝗌𝗍𝖺𝗍𝖾𝖫𝖲𝖭).** The 𝗌𝗍𝖺𝗍𝖾 variant of the Learning Stabilizers with Noise problem, denoted by 𝗌𝗍𝖺𝗍𝖾𝖫𝖲𝖭$_m(k, n, p)$, is characterized by integers $k, n, m \in \mathbb{N}$ and $p \in (0, 1)$. Both $p$ and $k$ can vary with $n$. We consider two variants of the problem:
> ∙ Search 𝗌𝗍𝖺𝗍𝖾𝖫𝖲𝖭$_m(k, n, p)$ is the following task: given as input samples of the form
> $$
> \bigl\{ \mathbf{C}_i \sim \mathcal{C}_n, \; \mathbf{E}_i \mathbf{C}_i |0^{n-k}, \psi\rangle \bigr\}_{i=1}^m
> $$
> where $\mathbf{C}_i$ are random $n$-qubit Clifford operators, $\mathbf{E}_i \sim \mathcal{D}_p^{\otimes n}$ are $n$-qubit Paulis, and $|\psi\rangle \sim \mu_k$ is a Haar random $k$-qubit state, the task is to output a quantum state $\rho$ within average fidelity at least $\frac{1}{2^k} + \frac{1}{\operatorname{poly}(n)}$ of $|\psi\rangle$ over the choice of $|\psi\rangle \sim \mu_k$; that is,
> $$
> \mathbb{E}_{|\psi\rangle \sim \mu_k}[\langle\psi|\rho|\psi\rangle] \ge \frac{1}{2^k} + \frac{1}{\operatorname{poly}(n)}.
> $$
> ∙ Decision 𝗌𝗍𝖺𝗍𝖾𝖫𝖲𝖭$_m(k, n, p)$ is the analogous decision task.

**Location:** §3.2.2, page 30 of the PDF.

---

## Theorem 1.6 — LPN reduces to LSN

> **Theorem 1.6 (informal).** Fix any $k \ge 1$ and $p \in (0, 1)$ which is not necessarily a constant. There exists a reduction from 𝖫𝖯𝖭$(\lfloor np/6 \rfloor, 2n, p/6)$ to 𝖫𝖲𝖭$(k, n, p)$. In particular, for a constant error probability $p$, constant rate 𝖫𝖯𝖭 reduces to 𝖫𝖲𝖭 with a single logical qubit.

**Location:** §1.2.3, page 5 of the PDF.

---

## Precision notes

1. **Noise model:** KLP+25 uses the depolarizing channel $\mathcal{D}_p^{\otimes n}$ (each qubit depolarizes independently with probability $p$). The symplectic representation of this noise is: each pair $(e_j, e_{n+j})$ is i.i.d., being $(0,0)$ with probability $1-p$ and $(0,1), (1,0), (1,1)$ each with probability $p/3$.

2. **Classical equivalent (from LPQR26 §2.1):** KLP+25's quantum LSN is equivalent (via efficient quantum reductions) to the classical problem of recovering $y \in \mathbb{Z}_2^k$ given $([A \mid B], Ax + By + e)$ where $x \in \mathbb{Z}_2^n$ is junk and $y$ is the secret. See `meta/KLP25-bridge-pin.md` for the LPQR26 classical-equivalent chain.

3. **stateLSN → LSN reduction:** KLP+25 proves that for $k = O(\log n)$ there is a quantum reduction from stateLSN to LSN (Theorem 1.5 informal, page 4).

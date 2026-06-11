# OP1 Single-Sample Formulation DRAFT — sympLPN SQ via row-marginal $\mu_{\text{row}}$

**Date:** 2026-06-12. **Actor:** Kimi. **Status:** DRAFT for Claude review (Track A, Step 1 revised per adjudication `f439b8d`).
**Supersedes:** `2026-06-12-KIMI-op1-formulation-draft.md` (batch model §4 conjecture ruled FALSE).
**Discipline:** Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

---

## §0. Preamble — why we left the batch model

Claude's adjudication (`f439b8d`, `experiments/163-CLAUDE-op1-formulation-check.py`) verified every formula in the batch-model DRAFT but **refuted its §4 optimistic conjecture** by exact enumeration:

| $n$ | Unconstrained baseline $C_n$ | Isotropic off-diag $C_n$ | Suppression |
|---|---|---|---|
| 2 | 3.160 | **2.975** | ×0.94 |
| 3 | 5.619 | **5.347** | ×0.95 |

Isotropy shaves only ~5\%; $C_n$ still grows exponentially. The batch model gives off-diagonal correlation $\gamma = 2^{\Theta(n)}$, which drives $\VSTAT(2^{-\Theta(n)})$ → an exponentially fine tolerance oracle → **vacuous SQ lower bound**. This is a modeling artifact, not a statement that sympLPN is SQ-easy.

**Redirect (Claude):** Move to a **single-sample model** where the example is one noisy inner product $(a, b = \langle a, x \rangle \oplus e)$ and $a$ is drawn from the **row-marginal** $\mu_{\text{row}}$ of a random isotropic matrix. Then OP1 becomes: *does conditioning on $S_A=0$ alter $\mu_{\text{row}}$ enough to reduce the statistical dimension?*

This DRAFT pins that model.

---

## §1. Pinned definitions

### sympLPN$_{n,p}$ (Def.~`def:symplpn`, **full-rank**)

Let $A \in \F_2^{2n \times n}$ be a **full-rank** public matrix whose columns are isotropic:
\[
S_A := A^{\top}\Omega A = 0.
\]
Full-rank isotropic matrices are exactly **bases of Lagrangian subspaces**; we write $\mathcal{A}_n$ for the set of such matrices. $|\mathcal{A}_n| = |\Lagr(2n)| \cdot |\mathrm{GL}(n,2)|$.

Let $x \in \F_2^n$ be secret, $e \sim \operatorname{Bernoulli}(p)$, and $y = Ax + e \in \F_2^{2n}$. Given $(A,y)$, recover $x$.

### Row-marginal distribution $\mu_{\text{row}}$

Sample $A \sim \mathrm{Unif}(\mathcal{A}_n)$. Choose a row index $i \sim \mathrm{Unif}(\{1,\dots,2n\})$. Output $a := r_i \in \F_2^n$, the $i$-th row of $A$.

**Key property:** $\mu_{\text{row}}$ is the marginal of one row under the uniform isotropic ensemble. The $2n$ rows of a single $A$ are **dependent** (coupled by $S_A=0$), but $\mu_{\text{row}}$ captures the marginal structure available to a single-example SQ algorithm.

### Statistical dimension (`thm:feldman`)

Unchanged from the batch DRAFT. For a class $\mathcal{D} = \{D_x\}$ and reference $D_0$:
\[
\SDA(B(\mathcal{D},D_0),\gamma) = \max\Bigl\{d : \forall S \subseteq \mathcal{X}, |S| \geq \frac{|\mathcal{X}|}{d} \Rightarrow \frac{1}{|S|^2}\sum_{x,x' \in S} |\langle D_x, D_{x'} \rangle| \leq \gamma\Bigr\}.
\]
If $\SDA = d$, any SQ algorithm distinguishing $\mathcal{D}$ from $D_0$ with advantage $\alpha > 1/2$ needs $q \geq (2\alpha-1)d$ queries to $\VSTAT(1/(3\gamma))$.

---

## §2. The SQ decision problem (single-sample)

### Secret space
\[
\mathcal{X} = \F_2^n, \qquad |\mathcal{X}| = 2^n.
\]

### Distribution class $\{D_x\}_{x \in \mathcal{X}}$

For each $x \in \F_2^n$, the distribution $D_x$ over examples $(a,b) \in \F_2^n \times \F_2$ is:
1. Sample $a \sim \mu_{\text{row}}$.
2. Sample $e \sim \operatorname{Bernoulli}(p)$.
3. Output $(a, b)$ where $b = \langle a, x \rangle \oplus e$.

### Reference distribution $D_0$

1. Sample $a \sim \mu_{\text{row}}$.
2. Sample $e \sim \operatorname{Bernoulli}(p)$.
3. Output $(a, e)$ — noise-only with the same row-marginal.

### Threat model

SQ algorithm queries $\phi : \F_2^n \times \F_2 \to [-1,1]$, receiving $\E_{(a,b)\sim D}[\phi(a,b)] \pm \tau$.

---

## §3. Correlation structure

### Likelihood ratio and correlation formula

For a fixed $a$, the likelihood ratio is
\[
\frac{D_x(a,b)}{D_0(a,b)} = 1 + (\langle a, x \rangle) \cdot f(b), \qquad f(0) = -\frac{1-2p}{1-p}, \; f(1) = \frac{1-2p}{p}.
\]
Averaging over $b \sim D_0$ (i.e. $b \sim \operatorname{Bernoulli}(p)$ independent of $a$):
\[
\E_{b}\!\left[\frac{D_x}{D_0} \frac{D_{x'}}{D_0} \,\Big|\, a\right]
= 1 + \sigma^2 (\langle a, x \rangle)(\langle a, x' \rangle),
\]
where $\sigma^2 = (1-2p)^2 / (p(1-p))$ as before. Hence
\[
\boxed{
\langle D_x, D_{x'} \rangle = \sigma^2 \cdot \E_{a \sim \mu_{\text{row}}}\!\bigl[(\langle a, x \rangle)(\langle a, x' \rangle)\bigr]
\qquad (x \neq x').
}
\]
The diagonal is $\langle D_x, D_x \rangle = \sigma^2 \cdot \E_{a}[\langle a, x \rangle] = \sigma^2 \cdot \Pr_{a}(\langle a, x \rangle = 1)$.

### Unconstrained baseline (uniform $a$)

If $a \sim \mathrm{Unif}(\F_2^n)$ (standard LPN), then for $x \neq x'$:
\[
\E_{a}[ (\langle a, x \rangle)(\langle a, x' \rangle) ] = \frac{1}{4},
\qquad
\langle D_x, D_{x'} \rangle = \frac{\sigma^2}{4}.
\]
For $p=1/4$, this is $1/3$. The average correlation over any large subset $S \subseteq \F_2^n$ is $\approx 1/3$, giving $\SDA = 2^{n-1}$ with $\gamma = 1/3$ and $\VSTAT(1)$. **Standard LPN already has exponential SQ hardness with constant tolerance.**

### What the conditioning question actually asks

OP1 is **not** asking whether isotropy drives correlation to $2^{-\Omega(n)}$ (that was the false batch conjecture). It asks whether $\mu_{\text{row}}$ is *sufficiently spread* that the SDA bound **survives** — i.e. the off-diagonal correlation does not blow up to $\sigma^2$ or otherwise destroy the $2^{\Omega(n)}$ query lower bound.

Specifically, define
\[
c_{\mu}(x,x') := \E_{a \sim \mu_{\text{row}}}\!\bigl[(\langle a, x \rangle)(\langle a, x' \rangle)\bigr].
\]
**Question:** Is $c_{\mu}(x,x')$ bounded by a constant $c < 1/2$ for all $x \neq x'$?

- If yes, then $\langle D_x, D_{x'} \rangle \leq c \cdot \sigma^2$. For $c < 1/2$, this is $< \sigma^2/2$, and the SDA argument yields $d = 2^{\Omega(n)}$ (the exact constant depends on $c$ and the diagonal contribution).
- If $c_{\mu}(x,x') = 1/2$ for some pairs, off-diagonal $= \sigma^2/2$, still giving exponential SDA.
- If $c_{\mu}(x,x') \approx 1$ for many pairs, off-diagonal $\approx \sigma^2$, and the SDA bound weakens (though may still be exponential depending on the diagonal).

Thus the **threshold** is not exponential smallness but **avoiding near-perfect correlation**.

---

## §4. Honesty caveat — the invisibility problem

**The single-sample row model makes $S_A=0$ invisible per-example.** The constraint lives in the joint distribution of $n$ rows, but a single example sees only one row. The only trace of isotropy is through $\mu_{\text{row}}$. If $\mu_{\text{row}}$ happens to be close to uniform (as one might expect by symmetry), then the single-sample model reduces to **standard LPN with a slightly non-uniform query distribution**, and the SQ bound survives trivially.

**This is too weak to be the "real" OP1.** The research question is to find a model where the global constraint $S_A=0$ actually bites. Candidate directions:

1. **Multi-row bundle model.** Example = $(A_S, y_S)$ where $S$ is a small set of row indices (e.g. $|S|=2$ or $3$). The rows in $S$ are marginally distributed as $\mu_{\text{row}}$ but jointly constrained by the fact that they extend to a full isotropic matrix. The correlation involves joint expectations $\E_{a_i, a_j}[\dots]$ and the constraint may become visible.

2. **Secret-coupled model.** Secret = $(x, L)$ where $L = \operatorname{colspan}(A)$ is the Lagrangian. The query distribution depends on $L$ (e.g. through $\mu_{\text{row}}^{(L)}$, the row-marginal conditioned on $L$). Then $S_A=0$ is implicit in the $L$-dependence. This connects to the membership-LSN machinery.

3. **Full-matrix model with different reference.** Keep example = $(A, y)$ but choose $D_0$ differently (e.g. $A$ isotropic, $y$ uniform over $\F_2^{2n}$ rather than noise-only). This was the batch model's problem — the reference choice determined whether the bound was vacuous.

**Our stance:** The single-sample row model is the correct **starting point** (it is the natural sympLPN analogue of standard LPN's SQ analysis). But we explicitly flag that it may not capture the full effect of $S_A=0$. Step 2 measures $\mu_{\text{row}}$; Step 3 explores multi-row bundles if the single-row model is insufficient.

---

## §5. Structural expectations for $\mu_{\text{row}}$

### Symmetry

The uniform isotropic ensemble $\mathcal{A}_n$ is invariant under left-multiplication by $\mathrm{Sp}(2n)$ (symplectic changes of basis in $\F_2^{2n}$). $\mathrm{Sp}(2n)$ acts transitively on non-zero vectors, so by symmetry $\mu_{\text{row}}$ should be **uniform over $\F_2^n \setminus \{0\}$**? Not exactly: the action is on columns (in $\F_2^{2n}$), not on rows (in $\F_2^n$). But there is a dual action.

Actually, consider the following: for a fixed $A \in \mathcal{A}_n$, applying a random $\mathrm{GL}(n,2)$ transform on the right changes the basis of $L$ but preserves $L$. This permutes the rows in a structured way. Averaging over all bases of all Lagrangians, the row-marginal should be invariant under $\mathrm{GL}(n,2)$ acting on the right. The only distribution on $\F_2^n$ invariant under $\mathrm{GL}(n,2)$ is uniform over $\F_2^n \setminus \{0\}$ (plus possibly a point mass at 0).

**Conjecture (symmetry-based, to be tested):** $\mu_{\text{row}}$ is uniform over $\F_2^n \setminus \{0\}$. If true, then $c_{\mu}(x,x') = 1/4$ for all $x \neq x'$, and the single-sample model is **identical** to standard LPN.

If $\mu_{\text{row}}$ has a point mass at 0 (i.e. some rows are zero), then $c_{\mu}$ may differ. But zero rows in a full-rank isotropic matrix? A zero row means one coordinate is zero for all columns, which is possible but its probability under the uniform ensemble needs measurement.

### Small-$n$ exact computation (Step 2)

Enumerate all $A \in \mathcal{A}_n$ for $n=2,3$:
- $n=2$: $|\mathcal{A}_2| = 90$.
- $n=3$: $|\mathcal{A}_3| = 22{,}680$.

For each $A$, extract all $2n$ rows. Build the empirical distribution of rows (grouped by Hamming weight and specific vectors). Compute:
- $\Pr_{a \sim \mu_{\text{row}}}(a = v)$ for each $v \in \F_2^n$.
- $c_{\mu}(x,x')$ for all $x \neq x'$.
- Compare to uniform baseline ($1/4$).

Output JSON with:
`{n, row_counts: {v: count}, total_rows, c_mu: {hamming_dist: {x,x': value}}, uniform_baseline, ratio_to_uniform}`.

---

## §6. Pipeline map (revised)

| Step | Task | Output |
|---|---|---|
| **2** (next) | Measure $\mu_{\text{row}}$ for $n=2,3$ by enumerating $\mathcal{A}_n$. Compute single-sample off-diag correlation. | `experiments/164-...py` + JSON |
| **3a** | If $\mu_{\text{row}} \approx$ uniform: single-sample SDA = standard LPN bound → OP1 **answered** (conditioning does not reduce SDA). | DRAFT conclusion |
| **3b** | If $\mu_{\text{row}}$ deviates significantly: analyze whether deviation destroys SDA. If yes, explore multi-row bundle model (Step 4). | DRAFT |
| **4** | Multi-row bundle: example = $(a_1, b_1), \dots, (a_k, b_k)$ from $k$ rows of the same isotropic $A$. Correlation involves joint row distribution. | Code + JSON |
| **5** | Closed-form attempt for $c_{\mu}(x,x')$ via symplectic block factorisation or character sums. | DRAFT |
| **6** | SDA argument or obstruction precision. | Final text |

---

## §7. Guards

- **No $n=2,3$ generalisation without closed form or structural argument.** Small-$n$ numerics guide conjectures; they do not prove asymptotics.
- **Tables need JSON companion.** All $\mu_{\text{row}}$ measurements must be reproducible.
- **Audit numbers need derivations.** The correlation formula in §3 must be verified by a script (re-derive from likelihood ratio).
- **Do not over-claim invisibility.** If $\mu_{\text{row}}$ turns out to be far from uniform, the single-sample model may already capture nontrivial structure. We follow the data.
- **No 
# OP1 Formulation DRAFT — sympLPN SQ under $S_A=0$

**Date:** 2026-06-12. **Actor:** Kimi. **Status:** DRAFT for Claude review (Track A, Step 1 per DIRECTIVE-KIMI-v3-frontier.md).
**Supersedes:** none (new track). **Discipline:** Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

---

## §0. Preamble

**Problem source:** `sec:open` item 1 of the paper. **Goal:** Prove that conditioning on $S_A = 0$ does not reduce the statistical dimension of sympLPN below $2^{\Omega(n)}$.

**Why this matters.** Our SQ lower bounds (\Cref{thm:main-sq}) sit on membership-LSN, whose secret space is $\Lagr(2n)$ ($\Theta(n^2)$ bits). The external hardness result of LPQR26 (linear-reduction barrier) and KLP+25 (constant-rate LPN $\le$ Search LSN, \Cref{thm:klp25}) both attach to sympLPN, whose secret is $x \in \F_2^n$ ($n$ bits) but whose public matrix carries the deterministic quadratic constraint $S_A = A^{\top}\Omega A = 0$. With the OP8 bridge blocked for natural maps, extending the SQ floor from membership-LSN to sympLPN is the largest available single upgrade — and the toolkit (exact correlation formulas, symplectic block factorisation, small-$n$ enumeration) is this track's proven strength zone.

**Honesty framing.** Three outcomes all count as progress:
1. **Proof** (unconditional SDA $2^{\Omega(n)}$) $\rightarrow$ v3 headline upgrade.
2. **Conditional** (average-correlation bound + explicit extremality assumption) $\rightarrow$ `thm:main-sq-cond` pattern for sympLPN.
3. **Obstruction** (named precision on exactly where $S_A=0$ blocks) $\rightarrow$ OP1 sharpened.

---

## §1. Pinned definitions (no re-derivation)

All items are quoted or directly inferred from the paper (`lsn-paper.tex`) and pinned source documents.

### sympLPN$_{n,p}$ (Def.~`def:symplpn`)

Let $A \in \F_2^{2n \times n}$ be a public matrix whose columns are **isotropic**:
\[
S_A \;:=\; A^{\top}\Omega A \;=\; 0 \;\in\; \F_2^{n \times n},
\]
i.e. every pair of columns is symplectically orthogonal. Let $x \in \F_2^n$ be a secret vector, $e \sim \operatorname{Bernoulli}(p)^{2n}$ a noise vector, and $y = Ax + e \in \F_2^{2n}$. Given $(A,y)$, recover $x$.

**Key structural fact:** $S_A=0$ is a deterministic, public, quadratic constraint on the **public parameters alone**. It depends on neither $x$ nor $e$.

### Statistical dimension with average correlation (Def.~`subsec:sq`)

Let $\mathcal{D}$ be a class of distributions and $D_0$ a reference distribution. The statistical dimension with average correlation is
\[
\SDA(B(\mathcal{D},D_0),\gamma) = \max\Bigl\{d : \forall S \subseteq \mathcal{D}, |S| \geq \frac{|\mathcal{D}|}{d} \Rightarrow \frac{1}{|S|^2}\sum_{D,D' \in S} |\langle D,D' \rangle| \leq \gamma\Bigr\},
\]
where $\langle D,D' \rangle$ denotes the correlation (inner product in $L^2(D_0)$ minus $1$; see `thm:feldman`).

### Feldman \etal\ lower bound (`thm:feldman`)

If $\SDA(B(\mathcal{D},D_0),\gamma) = d$, any SQ algorithm distinguishing $\mathcal{D}$ from $D_0$ with success probability $\alpha > 1/2$ requires $q \geq (2\alpha - 1)d$ queries to $\VSTAT(1/(3\gamma))$.

---

## §2. The SQ decision problem for sympLPN

We formulate sympLPN as a **decision problem** amenable to the SDA machinery.

### Secret space
\[
\mathcal{X} \;:=\; \F_2^n, \qquad |\mathcal{X}| = 2^n.
\]

### Distribution class $\{D_x\}_{x \in \mathcal{X}}$

For each secret $x \in \F_2^n$, the distribution $D_x$ over examples $(A,y) \in \F_2^{2n \times n} \times \F_2^{2n}$ is:
1. Sample $A$ uniformly from the set of **isotropic** matrices $\{A \in \F_2^{2n \times n} : A^{\top}\Omega A = 0\}$.
2. Sample $e \sim \operatorname{Bernoulli}(p)^{2n}$.
3. Output $(A, y)$ where $y = Ax + e$.

### Reference distribution $D_0$

1. Sample $A$ uniformly from isotropic matrices.
2. Sample $e \sim \operatorname{Bernoulli}(p)^{2n}$.
3. Output $(A, e)$ — i.e. the noise-only distribution with isotropic $A$.

**Note:** $D_0$ is exactly $D_{x=0}$ if we interpret $x=0$ as the zero secret. This matches the membership-LSN convention where $D_0$ is the noise-only distribution.

### Threat model (query power)

An SQ algorithm may issue arbitrary queries $\phi : \F_2^{2n \times n} \times \F_2^{2n} \to [-1,1]$, receiving for each an estimate of $\E_{(A,y) \sim D}[\phi(A,y)]$ with tolerance $\tau = O(\sqrt{\gamma})$. The algorithm is adaptive and randomized; `thm:feldman` lower-bounds the query complexity regardless.

### What we need to prove

To obtain $\SDA \geq 2^{\Omega(n)}$, it suffices to show that for **every** subset $S \subseteq \mathcal{X}$ with $|S| \geq 2^{n}/d$, the average correlation satisfies
\[
\frac{1}{|S|^2}\sum_{x,x' \in S} |\langle D_x, D_{x'} \rangle| \;\leq\; \gamma
\]
for some $\gamma = 2^{-\Omega(n)}$ and $d = 2^{\Omega(n)}$.

Since the diagonal terms $\langle D_x, D_x \rangle$ are always positive, the critical question is the **off-diagonal** correlation $\langle D_x, D_{x'} \rangle$ for $x \neq x'$.

---

## §3. Correlation structure

### Likelihood ratio

Let $r_i \in \F_2^n$ denote the $i$-th row of $A$ (so $(Ax)_i = r_i \cdot x$, dot product mod 2). Under $D_0$, the $y_i$ are independent $\operatorname{Bernoulli}(p)$. The likelihood ratio is
\[
\frac{D_x(A,y)}{D_0(A,y)} \;=\; \prod_{i=1}^{2n} \Bigl[1 + (Ax)_i \cdot f(y_i)\Bigr],
\]
where $f(0) = -(1-2p)/(1-p)$ and $f(1) = (1-2p)/p$. One checks $\E_{y_i \sim \operatorname{Bernoulli}(p)}[f(y_i)] = 0$ and $\E[f(y_i)^2] = \sigma^2$ with
\[
\sigma^2 \;:=\; \frac{(1-2p)^2}{p(1-p)}.
\]

### Correlation formula

Expanding the product and using independence of $y_i$ under $D_0$, the conditional expectation given $A$ is
\[
\E_{y \sim D_0}\!\left[\frac{D_x}{D_0}\frac{D_{x'}}{D_0} \,\Big|\, A\right]
\;=\; \prod_{i=1}^{2n} \Bigl[1 + \sigma^2 (r_i \cdot x)(r_i \cdot x')\Bigr].
\]
Hence the correlation is
\[
\boxed{
\langle D_x, D_{x'} \rangle
\;=\; \E_{A \sim \text{Isotropic}}\!\left[\prod_{i=1}^{2n} \bigl(1 + \sigma^2 (r_i \cdot x)(r_i \cdot x')\bigr)\right] \;-\; 1.
}
\]

### The unconstrained baseline (for comparison)

If $A$ were **unconstrained** (uniform over all $\F_2^{2n \times n}$), the rows $r_i$ would be i.i.d. uniform over $\F_2^n$. For $x \neq x'$:
\[
\E_{r_i}[1 + \sigma^2 (r_i \cdot x)(r_i \cdot x')] = 1 + \frac{\sigma^2}{4},
\]
since $(r_i \cdot x, r_i \cdot x')$ is uniform over $\F_2^2$. Thus
\[
\langle D_x, D_{x'} \rangle_{\text{unconstrained}} = \left(1 + \frac{\sigma^2}{4}\right)^{2n} - 1 \;=\; 2^{\Theta(n)}.
\]
For $p=1/4$ ($\sigma^2 = 4/3$), this is $(4/3)^{2n} - 1 \approx \exp(0.575n)$. The correlation grows **exponentially** with $n$.

**Implication:** In the unconstrained case, SDA is tiny (polynomial or even constant), so SQ lower bounds are trivially weak. The hardness of sympLPN (if any) in the SQ model must come entirely from the **isotropic constraint** $S_A=0$.

---

## §4. The conditioning question (core of OP1)

The isotropic constraint $A^{\top}\Omega A = 0$ couples the rows of $A$ nontrivially, preventing the factorisation that yielded the exponential baseline above. The central question is:

> **Does conditioning on $S_A=0$ reduce the correlation $\langle D_x, D_{x'} \rangle$ from $2^{\Theta(n)}$ to $2^{-\Omega(n)}$?**

More precisely, define
\[
C_n(x,x') \;:=\; \E_{A \sim \text{Isotropic}}\!\left[\prod_{i=1}^{2n} \bigl(1 + \sigma^2 (r_i \cdot x)(r_i \cdot x')\bigr)\right].
\]

**Conjecture (OP1, optimistic):** For all $x \neq x'$ and constant $p \in (0,1/2)$,
\[
C_n(x,x') \;\leq\; 1 + 2^{-\Omega(n)}.
\]
If true, then $\langle D_x, D_{x'} \rangle \leq 2^{-\Omega(n)}$, and the average correlation over any $S \subseteq \F_2^n$ is bounded by $2^{-\Omega(n)} + 2^{-n}$ (the diagonal contribution, since $|S|^{-1} \leq 2^{-n}$ for $|S| \geq 1$). This yields $\SDA = 2^{\Omega(n)}$ with $\gamma = 2^{-\Omega(n)}$, giving an unconditional SQ lower bound for sympLPN via `thm:feldman`.

**What we know:**
- The constraint $S_A=0$ is a system of $n(n-1)/2$ independent quadratic equations in the entries of $A$.
- Isotropic matrices can be sampled by first choosing a uniformly random Lagrangian $L \in \Lagr(2n)$, then choosing a uniformly random basis of $L$. The row distribution under this two-step sampling is nontrivial but structurally constrained by the symplectic geometry of $L$.
- The toolkit from the Krawtchouk appendix (symplectic block factorisation, exact character sums) may apply because the product $\prod_i (1 + \sigma^2 (r_i \cdot x)(r_i \cdot x'))$ is a function on the row space of $A$, and the isotropic constraint is a condition on the column space (Lagrangian). The duality between rows and columns is governed by the symplectic form $\Omega$.

**What we do not know:**
- Whether $C_n(x,x')$ has a closed form.
- Whether $C_n(x,x')$ is monotone in $n$.
- Whether worst-case $x,x'$ (e.g. Hamming distance 1) give the largest correlation.
- Whether the constraint affects all $x \neq x'$ uniformly or creates a "bad" subset of secrets with higher correlation.

---

## §5. Structural observations

### Row-column duality

The isotropic constraint is on columns: $c_j^{\top}\Omega c_k = 0$. The correlation product is on rows: $(r_i \cdot x)(r_i \cdot x')$. The two live in dual spaces. The symplectic form $\Omega$ provides the bridge: the row space of $A$ (as a subspace of $\F_2^{2n}$ via column vectors) is related to the orthogonal complement of the column Lagrangian under $\Omega$.

Specifically, if $L = \operatorname{colspan}(A)$ is Lagrangian, then $L = L^{\perp_\Omega}$. The rows of $A$ are linear functionals on $\F_2^n$ (via $x \mapsto Ax$), but geometrically they correspond to vectors in $\F_2^{2n}$ via the column interpretation. This duality was exploited in the Krawtchouk appendix for the variance computation of $\widehat{D}(\xi)$.

### Small-$n$ exact computation

For $n=2,3$, the set of isotropic matrices is small enough for exact enumeration:
- $n=2$: $2n=4$. Isotropic $4 \times 2$ matrices: count $\approx 2^{6} \cdot |\mathrm{GL}(2,2)| = 64 \cdot 6 = 384$? Actually need exact count. The Lagrangian count in $\F_2^4$ is $|\Lagr(4)| = (2^2+1)(2^1+1) = 15$. Each Lagrangian has $|\mathrm{GL}(2,2)| = 6$ bases. Total isotropic matrices = $15 \cdot 6 = 90$.
- $n=3$: $|\Lagr(6)| = (2^3+1)(2^2+1)(2^1+1) = 9 \cdot 5 \cdot 3 = 135$. Bases: $|\mathrm{GL}(3,2)| = (8-1)(8-2)(8-4) = 7 \cdot 6 \cdot 4 = 168$. Total: $135 \cdot 168 = 22{,}680$.

Both are easily enumerable. For each pair $(x,x')$, we can compute $C_n(x,x')$ exactly by summing over all isotropic $A$.

### Expected shape from small-$n$ data

If $C_n(x,x') \approx 1 + c \cdot \alpha^n$ for some $\alpha < 1$, then OP1 is true. If $C_n(x,x') \approx 1 + c \cdot \beta^n$ for $\beta > 1$, then the isotropic constraint is insufficient and OP1 is false (or requires a different query class / reference distribution).

---

## §6. Next steps (Track A pipeline)

### Step 2 (next): Small-$n$ correlation measurement

Enumerate all isotropic matrices for $n=2,3$ (and $n=4$ if feasible: $|\Lagr(8)| = (2^4+1)(2^3+1)(2^2+1)(2^1+1) = 17 \cdot 9 \cdot 5 \cdot 3 = 2{,}295$; $|\mathrm{GL}(4,2)| = (16-1)(16-2)(16-4)(16-8) = 15 \cdot 14 \cdot 12 \cdot 8 = 20{,}160$; total $\approx 46$ million — feasible with optimisation, possibly marginal).

For each $x \neq x'$, compute $C_n(x,x')$ exactly. Output JSON with:
- `n`, `hamming_distance(x,x')`, `C_n`, `correlation = C_n - 1`.
- Group by Hamming distance to detect distance-dependent structure.

### Step 3: Closed-form attempt

Use symplectic block factorisation (Krawtchouk appendix toolkit) to express $C_n(x,x')$ as a sum over Lagrangians or as a Krawtchouk-like polynomial. The product over rows resembles a partition function; the isotropic constraint may allow Fourier transform on $\Lagr(2n)$.

### Step 4: SDA argument

If Step 2/3 shows correlation $\leq 2^{-\Omega(n)}$, assemble the SDA lower bound. If correlation decays polynomially or stays constant, stop and write the **obstruction** outcome: a named precision result on exactly how $S_A=0$ fails to suppress correlation, sharpening OP1.

---

## §7. Honesty notes / guards

- **No $n=2,3$ generalisation without closed form or extreme-$n$ check.** The unconstrained baseline already shows exponential growth; the isotropic constraint must suppress this by an exponential factor. Small-$n$ numerics can suggest the trend but cannot prove asymptotics without additional structure.
- **Tables need JSON companion.** All numerics from Step 2 must be reproducible from a script.
- **Audit numbers need derivations.** Every formula in this DRAFT (likelihood ratio, correlation product, unconstrained baseline) must be verified by a script before any claim is made.
- **Diagonal vs. off-diagonal.** The SDA average mixes diagonal $\langle D_x, D_x \rangle$ and off-diagonal $\langle D_x, D_{x'} \rangle$. The diagonal is always $\chi^2(D_x \| D_0) \geq 0$. In the average over $S$, the diagonal contribution is $|S|^{-1} \cdot \chi^2(D_x \| D_0)$, which is small if $|S|$ is large. The off-diagonal dominates the SDA bound.
- **Worst-case subset.** Even if average correlation is small for *most* subsets, SDA requires it for *all* large subsets. If there exists a Hamming ball or linear subspace of secrets with anomalously high correlation, the SDA bound collapses. Step 2 must scan structured subsets, not just random pairs.

---

## Gate check

- **No closure claim:** This is a formulation DRAFT, not a proof. All statements about $C_n$ are framed as questions or conjectures.
- **No break:** SQ decision problem formulation does not disclose scheme weakness.
- **No security claim:** We do not claim LSN or sympLPN hardness.
- **No `paper/` edits:** Meta-only DRAFT.
- **KLP+25 / LPQR26 pins cited:** Definitions referenced to paper and pinned sources.
- **No numbers fabricated:** The unconstrained baseline $(4/3)^{2n}$ is derived; small-$n$ claims are pending enumeration.

No closure; no break; no security claim. OPEN = LSN.

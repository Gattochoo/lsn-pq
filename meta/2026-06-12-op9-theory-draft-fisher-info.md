# DRAFT: "TV(C,uniform) ≤ δ ⇒ Fisher-info o(n) ⇒ x unrecoverable"

> **SUPERSEDED:** wrong threat model — the LPN solver sees the public C, so the corner needs
> `I(x;y|C)`, not `I(x;y)`/`TV(P_C,U)`. See `2026-06-12-CLAUDE-adjudication-round5.md` §2.

**Status:** DRAFT — argument sketched, blocked point identified precisely.  
**Gate check:** No asymptotic claim without proof. Blocked point recorded.

---

## 1. The Clean Argument (works if premise holds)

**Setup.**  Fix a weight-$w$ random $B \in \mathbb{F}_2^{n \times 2n}$ and let $C = B' M \in \mathbb{F}_2^{n \times n}$.  The honest encoding is $y = Cx + e$ with $e \sim \mathrm{Bernoulli}(p)^{\otimes n}$ and $x \sim \mathrm{Uniform}(\mathbb{F}_2^n)$.  The adversary sees $y$ but **not** $C$.

**Lemma 1.1 (TV leakage bound).**  If the total-variation distance between the law of $C$ and the uniform distribution $U$ on $n \times n$ matrices satisfies $\mathrm{TV}(P_C, U) \le \delta$, then for every fixed $x$ the channel output is close to uniform:

$$\mathrm{TV}\bigl(P_{y|x},\; U_{\{0,1\}^n}\bigr) \;\le\; \delta.$$

*Proof sketch.*  Write $z = y + e$.  Conditioned on $e$, we need $Cz = y$ (since $y = Cx + e$).  For fixed $x \neq 0$ and fixed $z$, the set $\{C : Cx = z\}$ is an affine subspace of dimension $n^2 - n$.  As $z$ ranges over $\{0,1\}^n$, these $2^n$ affine subspaces partition the whole space of $n \times n$ matrices.  Hence

$$\sum_{y} \bigl|P(y|x) - 2^{-n}\bigr|
= \sum_{e} P(e) \sum_{z} \Bigl|\sum_{C : Cx=z} \bigl(P(C) - 2^{-n^2}\bigr)\Bigr|
\le \sum_{e} P(e) \sum_{C} \bigl|P(C) - 2^{-n^2}\bigr|
= 2\delta.$$

Dividing by 2 gives the TV bound. ∎

**Lemma 1.2 (Pinsker / Fannes).**  If $\mathrm{TV}(P_{y|x}, U) \le \delta$ for all $x$, then the mutual information satisfies

$$I(x;y) \;=\; H(y) - H(y|x) \;\le\; \delta n + O(\delta \log(1/\delta)).$$

In particular, if $\delta = o(1)$ then $I(x;y) = o(n)$.

**Corollary 1.3 (Unrecoverability).**  Reliable recovery of $x$ from $y$ requires $I(x;y) = \Omega(n)$.  Hence if $\delta = o(1)$, $x$ is **unrecoverable** (success probability $2^{-\Omega(n)}$).

---

## 2. The Blocked Point — Proving $\delta = o(1)$

The argument above is rigorous *conditional* on $\mathrm{TV}(P_C, U) = o(1)$.  The blocked point is **proving this premise** for random weight-$w$ rows with $w = \Theta(n)$.

### 2.1 What needs to be shown

For $C = B' M$ with random $B$, we need

$$\mathrm{TV}(P_C, U) \;=\; \frac{1}{2}\sum_{C} \bigl|P(C) - 2^{-n^2}\bigr| \;\xrightarrow[n\to\infty]{}\; 0.$$

By the Fourier/character method, this is equivalent to showing that for every non-zero test matrix $T \in \mathbb{F}_2^{n \times n}$,

$$\widehat{P_C}(T) \;=\; \mathbb{E}_C\bigl[(-1)^{\langle T, C \rangle}\bigr] \;\xrightarrow[n\to\infty]{}\; 0,$$

where $\langle T, C \rangle = \sum_{i,j} T_{ij} C_{ij}$ (trace inner product over $\mathbb{F}_2$).

### 2.2 Reduction to per-row Krawtchouk coefficients

Because $B$ has independent rows and $C_{ij} = B_{i, n+j}$,

$$\widehat{P_C}(T) \;=\; \prod_{i=1}^{n} \mathbb{E}_{B_i}\Bigl[(-1)^{\sum_j T_{ij} B_{i,n+j}}\Bigr].$$

For row $i$, let $t_i = (T_{i1},\dots,T_{in}) \in \mathbb{F}_2^n$ be the $i$-th row of $T$.  The expectation is over a random weight-$w$ subset of $\{0,\dots,2n-1\}$, projected onto the bottom-$n$ coordinates.

**Sub-lemma needed:** For a random weight-$w$ subset $S \subseteq [2n]$, let $S_{\mathrm{bot}} = S \cap \{n,\dots,2n-1\}$.  Then for every non-zero $t \in \mathbb{F}_2^n$,

$$\mathbb{E}_S\bigl[(-1)^{t \cdot S_{\mathrm{bot}}}\bigr] \;\xrightarrow[n\to\infty]{}\; 0$$

whenever $w = \Theta(n)$.

### 2.3 Why this is blocked

The distribution of $|S_{\mathrm{bot}}|$ is Hypergeometric$(2n, n, w)$: we draw $w$ elements without replacement from $2n$ items, $n$ of which are "bottom".  The Fourier coefficient is

$$\mathbb{E}\bigl[(-1)^{t \cdot S_{\mathrm{bot}}}\bigr]
\;=\; \sum_{k=0}^{w} (-1)^{?} \Pr[|S_{\mathrm{bot}}| = k] \cdot \mathbb{E}[(-1)^{t \cdot S_{\mathrm{bot}}} \mid |S_{\mathrm{bot}}| = k].$$

Given $|S_{\mathrm{bot}}| = k$, the set $S_{\mathrm{bot}}$ is a uniformly random $k$-subset of $[n]$.  The inner expectation is the Krawtchouk polynomial $K_k(|t|)$ evaluated at the weight of $t$.

For $w = n$, the Hypergeometric distribution is concentrated at $k \approx n/2$ with standard deviation $\Theta(\sqrt{n})$.  The Krawtchouk polynomial $K_{n/2}(|t|)$ is exponentially small in $n$ for fixed $|t|$, but the sum over $k$ involves a range of width $\Theta(\sqrt{n})$.

Proving that the *total* Fourier coefficient tends to 0 requires controlling the Krawtchouk polynomial in the oscillatory regime, which is technically non-trivial.  This is the **precise blocked point**:

> **Blocked:** We lack a closed-form evaluation or tight uniform bound for the Hypergeometric-mixture of Krawtchouk polynomials that arise from projecting a random weight-$w$ subset onto $n$ coordinates.

### 2.4 Sharpened OP9 (what the block gives us)

Even without proving $\delta = o(1)$, the argument yields a **sharpened statement** of the OP9 challenge:

> **Sharpened OP9 (information-theoretic form).**  Let $\delta_n(w) = \mathrm{TV}(P_{C_{n,w}}, U)$.  If $\delta_n(w) = o(1)$, then $x$ is information-theoretically unrecoverable from a single output $y$.  Hence the *only* way to break OP9 is to either (a) show $\delta_n(w) = \Omega(1)$ *and* exploit the resulting non-uniformity structurally, or (b) use multiple samples to amplify a $\delta_n(w) = o(1)$ signal.

Our numerical evidence (E-OP9e) shows that for $w = \Theta(n)$, recovery rates are low and decrease with $n$, consistent with $\delta_n(w) \to 0$ (or at least with the channel capacity being $o(n)$).  The formal proof of $\delta_n(w) = o(1)$ remains open.

---

## 3. Empirical Evidence

| $n$ | $w$ | $\mathrm{TV}(P_C, U)$ | recovery rate |
|-----|-----|----------------------|---------------|
| 4 | 1 | 0.990 | 5.0% |
| 4 | 2 | 0.829 | 6.5% |
| 4 | 3 | 0.531 | 10.0% |
| 4 | 4 | 0.332 | 11.0% |
| 5 | 1 | 0.999 | 0.0% |
| 5 | 2 | 0.984 | 4.0% |
| 5 | 3 | 0.933 | — |
| 5 | 5 | 0.870 | 2.0% |

*Observation:* TV distance decreases with $w$ for fixed $n$, but remains large ($\ge 0.33$) at $n=4,5$.  The trend suggests $\delta_n(w)$ may shrink as $n \to \infty$ for $w = \Theta(n)$, but small-$n$ experiments cannot confirm this.

---

## 4. Checklist

| Item | Status |
|------|--------|
| TV ⇒ channel uniformity (Lemma 1.1) | ✅ rigorous |
| Pinsker ⇒ $I = o(n)$ (Lemma 1.2) | ✅ standard |
| Unrecoverability (Cor 1.3) | ✅ conditional on premise |
| Proving $\delta_n(w) = o(1)$ | ❌ **blocked** — Hypergeometric-Krawtchouk mixture |
| Sharpened OP9 statement | ✅ recorded |
| No asymptotic claim without proof | ✅ — $\delta_n(w)=o(1)$ is conjecture, not claim |

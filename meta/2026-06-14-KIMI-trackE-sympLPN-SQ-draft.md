# Track E — OP1 SDA/SQ statement for sympLPN (DRAFT for Claude)

**Date:** 2026-06-14.  
**Track:** E (numbers 240–249).  
**Files:** `experiments/240-KIMI-trackE-sympLPN-SQ-draft.py`, `experiments/output/240-KIMI-trackE-sympLPN-SQ-draft.json`.  
**Status:** DRAFT — not paper-grade until Claude adjudicates.  
**Claim labels:** THEOREM for exact correlations; THEOREM/DRAFT for the SQ bound (the SDA→Feldman step is standard; the *novel* contribution is the exact correlation under isotropic conditioning).

---

## 1. What this note does

Converts the moment machinery (`thm:mj-general`, `prop:vmax`, `cor:bundle`) into an explicit Statistical-Dimension / SQ statement for the **sympLPN formulation**, complementing the membership-formulation bound.

The sympLPN problem has a **much smaller secret space** than membership-LSN (only $|\mathcal{X}|=2^n$ versus $|\Lagr(2n,\F_2)|=2^{n^2/2+O(n)}$).  Therefore the SDA cannot exceed $2^n$, and the strongest honest SQ bound we can aim for here is $\Omega(2^n)$ queries.  The note proves that this bound is achieved, and that the isotropic conditioning $S_A=0$ does **not** weaken it for constant-rate noise.

---

## 2. Pre-registered interpretation guards

Before any hardness interpretation:

1. **Comparison distribution / matched noise.** The reference distribution is $D_0$: $A\sim\mathcal{A}_n$ (uniform full-rank isotropic matrix) and $y\sim\Unif(\F_2^{2n})$ independent of $A$ (equivalently, sympLPN at noise rate $1/2$).  The alternative is $D_x$: same $A$ and $y=Ax+e$ with $e\sim\Bernoulli(p)^{2n}$.  This is the *natural decision* comparison; the noise rates are not "matched" in the LPN reduction sense, but the null is the correct cryptographic baseline for distinguishing.
2. **$m$-vs-$n$ scaling.** One sympLPN sample consists of the full $2n\times n$ public matrix $A$, i.e. $m=2n$ row equations over an $n$-bit secret.  The bound uses the entire $2n$-row block (bundle size $k$ up to $2n$), not a fixed small $m$.
3. **Usable noise rate.** $p$ is a constant bounded away from $1/2$ (verification uses $p=1/4$).  The VSTAT strength remains exponential in $n$, so the bound is in the usable regime.

**Scope guard:** This is the *sympLPN* (decoding) formulation with secret $x\in\F_2^n$.  It does **not** replace the membership-formulation $\Omega(2^n)$ unconditional bound or the conditional $2^{2n-O(1)}$ bound under `conj:pencil`; it complements them by showing that the $S_A=0$ conditioning alone does not reduce SQ dimension below $2^{\Omega(n)}$.

---

## 3. Decision problem and query class

**Problem.** $\mathsf{sympLPN\text{-}Decision}_{n,p}$: distinguish

* $D_x$: $A\sim\mathcal{A}_n$, $y=Ax+e$, $e\sim\Bernoulli(p)^{2n}$, with secret $x\in\F_2^n$;
* $D_0$: $A\sim\mathcal{A}_n$, $y\sim\Unif(\F_2^{2n})$ independent of $A$.

The sample space is $\mathcal{Z}=\F_2^{2n\times n}\times\F_2^{2n}$.

**Query class (restricted, bundle-parity).** For a fixed $k$-subset $S\subseteq[2n]$, define the bounded query

$$
h^{(S)}(A,y)=(-1)^{\sum_{i\in S}y_i}.
$$

This is the natural sympLPN analogue of a $k$-row bundle parity query; it sees exactly the $k$ rows that `cor:bundle` controls.

---

## 4. Exact pairwise correlation of $k$-row bundle queries

**THEOREM E.1 (exact bundle correlation).** Fix $n\ge 1$, $p\in(0,1/2)$, a non-empty $S\subseteq[2n]$ with $|S|=k$, and secrets $x,x'\in\F_2^n$.  Under the isotropic ensemble $\mathcal{A}_n$,

$$
\langle h^{(S)}_x, h^{(S)}_{x'}\rangle_{D_0}
=
\begin{cases}
(1-2p)^{2k} & x=x',\\[4pt]
-\displaystyle\frac{(1-2p)^{2k}}{2^{2n}-1} & x\neq x'.
\end{cases}
$$

Consequently the average absolute pairwise correlation over the full secret space is

$$
\bar\rho_k \;=\; \frac{1}{2^{2n}}\sum_{x,x'\in\F_2^n}\bigl|\langle h^{(S)}_x,h^{(S)}_{x'}\rangle\bigr|
\;=\; (1-2p)^{2k}\cdot\frac{2^n+2}{2^n(2^n+1)}.
$$

(For a subset $\mathcal{S}\subseteq\F_2^n$ of size $|\mathcal{S}|$, the diagonal-inclusive average is $\rho_{\mathrm{avg}}^{(k)}(\mathcal{S})=(1-2p)^{2k}/|\mathcal{S}|\cdot(1+(|\mathcal{S}|-1)/(2^{2n}-1))$.)

**Proof.** Conditioned on $A$, the rows of $y$ are independent and

$$
\E_{D_x|A}\bigl[h^{(S)}(A,y)\bigr]
=(-1)^{\langle\mathbf{1}_S,Ax\rangle}(1-2p)^k.
$$

Therefore

$$
\langle h^{(S)}_x,h^{(S)}_{x'}\rangle_{D_0}
=(1-2p)^{2k}\;\E_{A\sim\mathcal{A}_n}\!\Bigl[(-1)^{\langle\mathbf{1}_S,A(x+x')\rangle}\Bigr].
$$

For $x=x'$ the phase is $1$.  For $x\neq x'$, set $w=x+x'\neq 0$.  The random vector $v=Aw$ is uniform over the non-zero vectors of the random Lagrangian $L=\operatorname{colspan}(A)$ (any non-zero $w$ induces a bijection from ordered bases of $L$ to $L\setminus\{0\}$).  Hence

$$
\E_A\bigl[(-1)^{\langle\mathbf{1}_S,v\rangle}\bigr]
=\E_L\Bigl[\frac{1}{2^n-1}\sum_{v\in L\setminus\{0\}}(-1)^{\langle\mathbf{1}_S,v\rangle}\Bigr].
$$

For a fixed Lagrangian $L$,

$$
\sum_{v\in L}(-1)^{\langle\mathbf{1}_S,v\rangle}
=2^n\cdot\mathbf{1}_{\{\mathbf{1}_S\in L\}},
$$

because $L=L^{\perp_\Omega}$.  By $\Sp(2n,\F_2)$-transitivity on non-zero vectors, $\Pr_L[\mathbf{1}_S\in L]=1/(2^n+1)$ for any non-empty $S$.  Thus

$$
\frac{1}{2^n-1}\Bigl(2^n\cdot\frac{1}{2^n+1}-1\Bigr)
=\frac{2^n-(2^n+1)}{(2^n-1)(2^n+1)}
=-\frac{1}{2^{2n}-1}.
$$

The average formula follows by counting diagonal ($2^n$) and off-diagonal ($2^{2n}-2^n$) pairs.  ∎

**Connection to the moment theorems.** The off-diagonal sign is negative and has magnitude $2^{-2n+O(1)}$; this is precisely the same sign and scale as the deviation term in `prop:vmax` (for $p=1/4$ the leading relative deviation is $-2(25/64)^n$).  Expanding the product $\prod_{i\in S}(1+\tau(-1)^{v_i})$ and applying the moment closures of `thm:mj-general` reproduces the same $O_k(4^{-n})$ deviation for fixed $k$ (`cor:bundle`).  Thus the isotropic conditioning does not help any constant-size bundle query exploit the secret structure.

---

## 5. Full likelihood-ratio correlations (optional maximal query class)

If the SQ adversary is allowed arbitrary bounded queries, the relevant pairwise correlation is the likelihood-ratio inner product:

$$
\langle D_x,D_{x'}\rangle_{D_0}
=\E_{D_0}\!\Bigl[\Bigl(\frac{D_x}{D_0}-1\Bigr)\Bigl(\frac{D_{x'}}{D_0}-1\Bigr)\Bigr].
$$

**THEOREM E.2 (exact likelihood-ratio correlation).** For $p\in(0,1/2)$ let $\tau=(1-2p)^2$.  Then

$$
\langle D_x,D_x\rangle = (1+\tau)^{2n}-1,
\qquad
\langle D_x,D_{x'}\rangle = -\frac{(1+\tau)^{2n}-1}{2^{2n}-1}\quad(x\neq x').
$$

**Proof sketch.** Conditioned on $A$,

$$
\frac{D_x(y|A)}{D_0(y|A)}
=\prod_{i=1}^{2n}\bigl(1+\tau^{1/2}(-1)^{y_i+\langle a_i,x\rangle}\bigr)
=\prod_{i=1}^{2n}\bigl(1+\tau(-1)^{\langle a_i,x\rangle}\bigr)
$$

after taking expectation over $y$ under $D_0$.  Setting $v=A(x+x')$ and expanding the product gives $\prod_i(1+\tau(-1)^{v_i})$.  The same character-sum argument as in Theorem E.1 yields the formula.  ∎

This is the sympLPN analogue of the membership-formulation exact correlation.  The diagonal is larger than in the restricted bundle query, but the off-diagonal is still only $O(2^{-2n})$ times the diagonal.

---

## 6. SDA bound and Feldman query lower bound

We apply Feldman et al. as restated in the paper (`thm:feldman`):

> If $\SDA(B(\mathcal{D},D_0),\gamma)=d$, any SQ algorithm distinguishing $\mathcal{D}$ from $D_0$ with success probability $\alpha>1/2$ requires $q\ge (2\alpha-1)d$ queries to $\VSTAT(1/(3\gamma))$.

Take $\alpha=2/3$ as in the paper, so $q\ge d/3$.

### 6.1 Using $k$-row bundle queries

For fixed $k$, the worst-case subset of secrets of size $|S|$ has average absolute correlation

$$
\rho_{\mathrm{avg}}^{(k)}(S)
\le \frac{(1-2p)^{2k}}{|S|}\Bigl(1+\frac{|S|-1}{2^{2n}-1}\Bigr)
\le \frac{2(1-2p)^{2k}}{|S|}
\quad\text{for }|S|\le 2^{2n}.
$$

Setting $|S|=2^{n-t}$ and $\gamma=2(1-2p)^{2k}/2^{n-t}$ gives

$$
\SDA\bigl(B(\{D_x\},D_0),\gamma\bigr)\ge 2^{n-t},
$$

and hence

$$
q\ge \frac{1}{3}\cdot 2^{n-t}
\quad\text{queries to}\quad
\VSTAT\!\left(\frac{2^{n-t}}{6(1-2p)^{2k}}\right).
$$

At $t=0$ (full secret space):

$$
\boxed{\;q\ge 2^{n-\log_2 3}\text{ queries to }\VSTAT\!\left(\frac{2^n}{6(1-2p)^{2k}}\right).\;}
$$

For constant $k$ and constant $p<1/2$, this is an exponential query lower bound with exponential VSTAT strength.

### 6.2 Using full likelihood ratio

With $\tau=(1-2p)^2$, the average absolute correlation over the full secret space is

$$
\bar\rho
=\frac{(1+\tau)^{2n}}{2^n}\cdot\frac{2^{2n}+2^n-2}{2^{2n}-1}
=\frac{(1+\tau)^{2n}}{2^n}\bigl(1+O(2^{-n})\bigr).
$$

Taking $\gamma=2\bar\rho$ gives the same order of bound:

$$
\SDA(B(\{D_x\},D_0),\gamma)\ge 2^n\bigl(1-O(2^{-n})\bigr),
\qquad
q\ge 2^{n-O(1)}.
$$

The VSTAT parameter is

$$
\frac{1}{3\gamma}
=\frac{2^{n-1}}{3(1+\tau)^{2n}\bigl(1+O(2^{-n})\bigr)}.
$$

---

## 7. Verified exact quantities at $n=2,3$ ($p=1/4$)

All values are reproduced by `experiments/240-KIMI-trackE-sympLPN-SQ-draft.py`.

### 7.1 Moments and bundle sums

$n=2$:

| $j$ | $m_j$ |
|---:|---|
| 0 | $1$ |
| 1 | $4/15$ |
| 2 | $7/135$ |
| 3 | $0$ |
| 4 | $0$ |

$V_{2n}=V_4=241/81$ (sum and closed form agree).

$n=3$:

| $j$ | $m_j$ |
|---:|---|
| 0 | $1$ |
| 1 | $16/63$ |
| 2 | $284/4725$ |
| 3 | $4/315$ |
| 4 | $11/4725$ |
| 5 | $0$ |
| 6 | $0$ |

$V_{2n}=V_6=136427/25515$ (sum and closed form agree).

### 7.2 SympLPN correlations

$n=2$:
* self-correlation (likelihood ratio): $\chi^2_{\mathrm{self}}=369/256$;
* off-diagonal correlation: $-123/1280$ (absolute value $123/1280$);
* average absolute over $\F_2^n$ (likelihood ratio): $1107/2560$;
* $k$-row bundle average: $3\cdot(1/4)^k/10$ (e.g. $k=1$: $3/40$, $k=4$: $3/2560$).

$n=3$:
* self-correlation: $\chi^2_{\mathrm{self}}=11529/4096$;
* off-diagonal correlation: $-183/4096$ (absolute value $183/4096$);
* average absolute over $\F_2^n$ (likelihood ratio): $6405/16384$;
* $k$-row bundle average: $5\cdot(1/4)^k/36$ (e.g. $k=1$: $5/144$, $k=6$: $5/147456$).

### 7.3 SDA / Feldman parameters (full likelihood ratio)

$n=2$, full secret space ($t=0$): $\SDA(\gamma)\ge 4$ with $\gamma=1107/1280$, giving $q\ge 4/3$ and $1/(3\gamma)=1280/3321$.

$n=3$, full secret space ($t=0$): $\SDA(\gamma)\ge 8$ with $\gamma=6405/8192$, giving $q\ge 8/3$ and $1/(3\gamma)=8192/19215$.

(The small constants are because $n=2,3$ are tiny; asymptotically $q\ge 2^{n-O(1)}$.)

---

## 8. Relation to OP1 and open items

OP1 asks whether conditioning on $S_A=0$ reduces the statistical dimension of sympLPN below $2^{\Omega(n)}$.  The answer here is **negative for constant-size queries and for the full likelihood-ratio query class**, with exact rate quantified by the moment machinery.

**What remains OPEN:**
* The $j=\Theta(n)$ growing-bundle regime for general statistics (only the variance summary $V_{2n}$ is closed by `prop:vmax`).
* Adaptive query strategies that depend on $A$ in a non-bundle way.
* The membership↔sympLPN bridge (the two formulations are not claimed equivalent).

**No closure; no break; no security claim.**  OPEN = LSN.

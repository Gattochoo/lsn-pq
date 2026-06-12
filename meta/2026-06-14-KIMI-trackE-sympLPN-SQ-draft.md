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

For a fixed Lagrangian $L$, let $J$ be the Gram matrix of the symplectic form
$\Omega$ (so $J\mathbf{1}_S$ is $\mathbf{1}_S$ with coordinate-pairs swapped).
Because the symplectic dual of $L$ is $L^{\perp_\Omega}=JL$ and $L$ is
Lagrangian,

$$
\sum_{v\in L}(-1)^{\langle\mathbf{1}_S,v\rangle}
=2^n\cdot\mathbf{1}_{\{J\mathbf{1}_S\in L\}}.
$$

(The naive claim with $\mathbf{1}_S\in L$ instead of $J\mathbf{1}_S\in L$ is false;
for example $L=\mathrm{span}\{e_1,e_2\}$ and $S=\{1\}$ gives sum $0$ while
$\mathbf{1}_S\in L$.)  By $\Sp(2n,\F_2)$-transitivity on non-zero vectors,
$\Pr_L[J\mathbf{1}_S\in L]=1/(2^n+1)$ for any non-empty $S$, and the same
holds for $\mathbf{1}_S$ because $J$ is invertible.  Thus

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

## 6. Corrected SDA/Feldman lower bound

**Status of the first-draft §6.**  The original bundle-query application had
three defects: (i) it used a restricted query class in the unrestricted SQ
theorem of Feldman et al.; (ii) it ignored the singleton-diagonal correlation
$\beta=(1+\tau)^{2n}-1$, which dominates any subset containing a single secret;
(iii) it did not check that the resulting VSTAT parameter stays above $1$.
The corrected bound below uses the full likelihood-ratio query class and an
honest range check.

We apply Feldman et al. as restated in the paper (`thm:feldman`):

> If $\SDA(B(\mathcal{D},D_0),\gamma)=d$, any SQ algorithm distinguishing $\mathcal{D}$ from $D_0$ with success probability $\alpha>1/2$ requires $q\ge (2\alpha-1)d$ queries to $\VSTAT(1/(3\gamma))$.

Take $\alpha=2/3$, so $q\ge d/3$.

### 6.1 Full likelihood-ratio query class

With $\tau=(1-2p)^2$ and $\beta=(1+\tau)^{2n}-1$, the likelihood-ratio
self-correlation is $\beta$ and the off-diagonal correlation has magnitude
$\beta/(2^{2n}-1)$.  For any subset $\mathcal{S}$ of secrets with
$|\mathcal{S}|\ge 2^{n-t}$, the average absolute correlation is at most

$$
\gamma_t
\;:=\;
\frac{2\beta}{2^{n-t}}.
$$

Hence

$$
\SDA\bigl(B(\{D_x\},D_0),\gamma_t\bigr)\ge 2^t,
\qquad
q\ge \frac{2^t}{3}
\quad\text{queries to}\quad
\VSTAT\!\left(\frac{2^{n-t}}{6\beta}\right).
$$

The VSTAT parameter is meaningful only when it is at least $1$, i.e.
$\gamma_t\le 1/3$.  This imposes

$$
2^{n-t}\ge 6\beta
\;\Longleftrightarrow\;
t\le c_p n - O(1),
\qquad
\boxed{\;c_p=1-2\log_2(1+\tau).\;}
$$

For the standard noise rate $p=1/4$ we have $\tau=1/4$ and
$c_p\approx 0.356$.  Thus the honest headline is a
**$2^{c_p n}$-query lower bound at exponential VSTAT strength**:

$$
\boxed{\;q\ge 2^{c_p n - O(1)}\text{ queries to }\VSTAT\!\left(2^{c_p n-O(1)}\right).\;}
$$

This is still exponential in $n$, but the exponent is $c_p n$, not $n-O(1)$.

### 6.2 Constant-size bundle queries

For a *restricted* query class that only sees $k$-row parities, the same
character-sum argument gives average correlation $O((1-2p)^{2k}/|\mathcal{S}|)$,
which would yield a stronger-looking $\Omega(2^n)$ bound.  However, applying the
unrestricted SQ theorem of Feldman et al. to a restricted query class is not
valid: a separate restricted-SQ dimension theorem would be needed.  We therefore
state the unrestricted bound in §6.1 as the honest SQ lower bound and leave the
restricted-class statement as an open direction.

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

With $\beta=(1+\tau)^{2n}-1$ and $\gamma_t=2\beta/2^{n-t}$, the bound is
meaningful only when $2^{n-t}\ge 6\beta$ (so that the VSTAT parameter is at
least $1$).  At $p=1/4$:

| $n$ | $\beta$ | valid $t$ | max query lower bound $q\ge 2^t/3$ | VSTAT parameter $2^{n-t}/(6\beta)$ |
|---:|---:|---:|---:|---:|
| 2 | $369/256$ | none | — | $<1$ for every $t\ge0$ |
| 3 | $11529/4096$ | none | — | $<1$ for every $t\ge0$ |
| 10 | $\approx 8.57\times10^1$ | $t=0$ only | $q\ge 1/3$ | $\approx 1.99$ |
| 20 | $\approx 7.52\times10^3$ | $t\le 4$ | $q\ge 16/3$ | $\approx 1.45$ |
| 40 | $\approx 5.66\times10^7$ | $t\le 11$ | $q\ge 2048/3$ | $\approx 1.58$ |

The tiny cases $n=2,3$ are below the asymptotic regime and give only trivial
constants; the honest asymptotic statement is
$q\ge 2^{c_p n-O(1)}$ with $c_p\approx 0.356$ at $p=1/4$.

---

## 8. Relation to OP1 and open items

OP1 asks whether conditioning on $S_A=0$ reduces the statistical dimension of sympLPN below $2^{\Omega(n)}$.  The answer here is **negative at the correlation level and for the full likelihood-ratio query class**, with exact rate quantified by the moment machinery.  The honest SQ query lower bound is $q\ge 2^{c_p n-O(1)}$ with $c_p=1-2\log_2(1+\tau)>0$ for $p<1/2$ (about $0.356$ at $p=1/4$), not $2^{n-O(1)}$.

**What remains OPEN:**
* A matching lower bound for the *restricted* $k$-row bundle query class (the unrestricted Feldman theorem does not apply directly).
* The $j=\Theta(n)$ growing-bundle regime for general statistics (only the variance summary $V_{2n}$ is closed by `prop:vmax`).
* Adaptive query strategies that depend on $A$ in a non-bundle way.
* The membership↔sympLPN bridge (the two formulations are not claimed equivalent).

**Corrections relative to the first draft.**  The character-sum step in the proof of Theorem E.1 now uses the symplectic dual $L^{\perp_\Omega}=JL$ instead of the false untwisted identity $L=L^{\perp_\Omega}$; the final correlation values are unchanged.  The SDA/Feldman application in §6 has been replaced by the corrected corollary with the $c_p$ range check.

**No closure; no break; no security claim.**  OPEN = LSN.

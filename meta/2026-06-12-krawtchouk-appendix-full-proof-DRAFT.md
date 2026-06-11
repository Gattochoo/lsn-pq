# Appendix DRAFT: Full Proof of lem:affine-coset-bias-whp

**Status:** DRAFT — LaTeX-ready appendix for paper v2.  
**Scope:** Closed-form variance, block factorization, explicit cancellation, Chebyshev concentration.  
**Gate check:** No asymptotic claim without derivation from explicit formula.

---

## Notation

- $N \subset \mathbb{F}_2^{2n}$: uniform random Lagrangian (dimension-$n$ maximal isotropic subspace).
- $|v|$: Hamming weight.
- $\Omega(v,v') = \sum_{i=1}^n (a_i y_i + b_i x_i)$ for $v=(a,b), v'=(x,y)$: standard symplectic form.
- $p = \frac{1}{2^n+1}$, $q = \frac{1}{(2^{n-1}+1)(2^n+1)}$.

---

## D.1 Closed-Form Variance

Define the weight enumerator evaluated at $\lambda=1/2$:
$$W_N(1/2) = \sum_{v\in N} 2^{-|v|}, \qquad W := W_N(1/2)-1 = \sum_{v\neq 0} X_v 2^{-|v|},$$
where $X_v = \mathbf{1}_{v\in N}$.

**Lemma D.1 (Expectation).** For every $n$,
$$\mathbb{E}[W] = \frac{(3/2)^{2n}-1}{2^n+1} = \frac{(9/4)^n-1}{2^n+1}.$$

*Proof.* $\mathbb{E}[X_v] = p$ for all $v\neq 0$, and $\sum_{v\neq 0} 2^{-|v|} = (3/2)^{2n}-1$. ∎

**Lemma D.2 (Variance).** For every $n$,
$$\mathrm{Var}[W] = p(1-p)D + qS_0 - p^2 T,$$
where
\begin{align*}
D &= \sum_{v\neq 0} 2^{-2|v|} = (5/4)^{2n}-1, \\
T &= \sum_{\substack{v\neq v'\\ v,v'\neq 0}} 2^{-|v|-|v'|} = \bigl((3/2)^{2n}-1\bigr)^2 - D, \\
C_{\mathrm{full}} &= \sum_{\substack{v\neq v'\\ v,v'\neq 0}} (-1)^{\Omega(v,v')} 2^{-|v|-|v'|}
   = (7/4)^{2n} - 2(3/2)^{2n} - (5/4)^{2n} + 2, \\
S_0 &= \frac{T + C_{\mathrm{full}}}{2}.
\end{align*}

*Proof.*  Expand $\mathrm{Var}[W] = \mathbb{E}[W^2]-\mathbb{E}[W]^2$ using the three cases for $\Pr[v,v'\in N]$:
- $v=v'\neq 0$: probability $p$;
- $v\neq v'$, $\Omega(v,v')=0$: probability $q$;
- otherwise: probability $0$.

The off-diagonal sum splits via the character $(-1)^{\Omega(v,v')}$ into $S_0$ ($\Omega=0$) and $S_1$ ($\Omega=1$), with $S_0=(T+C_{\mathrm{full}})/2$ and $S_1=(T-C_{\mathrm{full}})/2$. ∎

---

## D.2 Block Factorisation of the Character Sum

**Lemma D.3.** Let $\Sigma_n = \sum_{v,v'\in\mathbb{F}_2^{2n}} (-1)^{\Omega(v,v')} 2^{-|v|-|v'|}$.  Then
$$\Sigma_n = (7/4)^{2n}.$$

*Proof.*  Decompose $v=(a,b)$, $v'=(x,y)$ with $a,b,x,y\in\mathbb{F}_2^n$.  The symplectic form factorises coordinate-wise:
$$\Omega(v,v') = \sum_{i=1}^n (a_i y_i + b_i x_i).$$
Hence
$$\Sigma_n = \prod_{i=1}^n \underbrace{\sum_{a,b,x,y\in\{0,1\}} (-1)^{ay+bx} 2^{-(a+b+x+y)}}_{=: \sigma}.$$
A direct enumeration of the $16$ terms yields $\sigma = 49/16 = (7/4)^2$ (see Table 1 in the main text).  Therefore $\Sigma_n = (49/16)^n = (7/4)^{2n}$. ∎

Removing the $v=0$ or $v'=0$ terms (each contributes $(3/2)^{2n}$) and the diagonal $v=v'$ (contributes $D$) gives $C_{\mathrm{full}}$ as stated in Lemma D.2.

---

## D.3 Asymptotic Decay

**Lemma D.4.** As $n\to\infty$,
$$\mathrm{Var}[W] = (25/32)^n + (49/64)^n + O((81/128)^n) + O((25/64)^n).$$

*Proof.*  Keep only dominant exponentials in each symbol of Lemma D.2:
\begin{align*}
p(1-p)D &= \frac{2^n}{(2^n+1)^2}\bigl((25/16)^n-1\bigr)
        = (25/32)^n + O((25/64)^n), \\
qS_0 &= \frac{1+o(1)}{2^{2n-1}}\cdot\frac{(81/16)^n+(49/16)^n+O((9/4)^n)}{2}
     = (81/64)^n + (49/64)^n + O((9/16)^n), \\
p^2T &= \frac{1+o(1)}{2^{2n}}\bigl((81/16)^n+O((9/4)^n)\bigr)
     = (81/64)^n + O((9/16)^n).
\end{align*}
The $(81/64)^n$ terms cancel exactly.  To see this explicitly:
$$\frac{q}{2}-p^2 = \frac{(2^n+1)-2(2^{n-1}+1)}{2(2^{n-1}+1)(2^n+1)^2}
= \frac{-1}{2(2^{n-1}+1)(2^n+1)^2},$$
so
$$\Bigl(\frac{q}{2}-p^2\Bigr)T = -\frac{(81/16)^n}{2(2^{n-1}+1)(2^n+1)^2} + \cdots
= -(81/128)^n(1+o(1)).$$
Collecting the remaining terms yields the claim. ∎

**Corollary D.5.** $\displaystyle \frac{\mathrm{Var}[W]}{\mathbb{E}[W]^2} = O((50/81)^n)$.

*Proof.*  $\mathbb{E}[W] = (9/8)^n(1+o(1))$, so $\mathbb{E}[W]^2 = (81/64)^n(1+o(1))$.  Dividing the dominant term $(25/32)^n$ from Lemma D.4 by $(81/64)^n$ gives $(50/81)^n$. ∎

---

## D.4 Chebyshev Concentration

**Lemma D.6.** For $\varepsilon_n = (50/81)^{n/4}$,
$$\Pr\bigl[|W-\mathbb{E}[W]| \ge \varepsilon_n \mathbb{E}[W]\bigr] = O((50/81)^{n/2}) = 2^{-\Omega(n)}.$$

*Proof.*  By Chebyshev and Corollary D.5,
$$\Pr[|W-\mathbb{E}[W]| \ge \varepsilon_n\mathbb{E}[W]]
\le \frac{\mathrm{Var}[W]}{\varepsilon_n^2 \mathbb{E}[W]^2}
= O\!\left(\frac{(50/81)^n}{(50/81)^{n/2}}\right)
= O((50/81)^{n/2}).$$
Since $50/81 < 1$, this is $2^{-\Omega(n)}$. ∎

---

## D.5 Theorem Statement (w.h.p. Affine-Coset Bias)

**Theorem D.7 (lem:affine-coset-bias-whp).**  Let $A\in\mathbb{F}_2^{n\times 2n}$ be a uniform random full-rank isotropic matrix and $e$ a uniform random vector.  Let $b=Ae$.  Then
$$\Pr_A\Bigl[\bigl|\mathbb{E}_e[(-1)^{b^{\!\top} e}]\bigr| \le (2^{-n}+(9/16)^n)(1+o(1))\Bigr] = 1-2^{-\Omega(n)}.$$

*Proof sketch.*  The dual code $N=\ker(A)^{\!\top}$ is a uniform Lagrangian.  By Lemma D.1 and Corollary D.5, $W_N(1/2)$ has mean $1+O((9/8)^n)$ and variance $O((25/32)^n)$.  Lemma D.6 gives $|W_N(1/2)-\mathbb{E}[W]| \le (50/81)^{n/4}\mathbb{E}[W]$ w.p. $1-2^{-\Omega(n)}$.  On this event the bias equals $(W_N(1/2)-1)/2^n + 2^{-n} = (9/16)^n(1+o(1)) + 2^{-n}$. ∎

---

## Checklist

| Item | Status |
|------|--------|
| Closed-form Var (Lemma D.2) | ✅ all $n$ |
| Block factorisation (Lemma D.3) | ✅ explicit 16-term → 49/16 |
| $(81/64)^n$ explicit cancellation | ✅ $q/2-p^2$ computed directly |
| Chebyshev concentration | ✅ $\varepsilon_n = (50/81)^{n/4}$ |
| Theorem statement | ✅ w.h.p. form |
| LaTeX ready | ✅ |

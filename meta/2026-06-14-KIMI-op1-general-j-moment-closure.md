# OP1 General-$j$ Moment Closure

**Date:** 2026-06-14  
**Scripts:** `experiments/193-KIMI-op1-general-j-moment-closure.py`,
`experiments/output/193-op1-general-j-moment-closure.json`.

## Theorem (exact $m_j$ for all $j$)

Let $L \subset \F_2^{2n}$ be a uniformly random Lagrangian subspace, let
$c_1,c_2$ be two uniformly random non-zero vectors in $L$, and let
$t = |\operatorname{supp}(c_1) \cap \operatorname{supp}(c_2)|$.
For $1 \le j \le 2n$ define
$$
  m_j^{(n)} = \E_L\!\left[\frac{\binom{t}{j}}{\binom{2n}{j}}\right].
$$
Then
$$
  \boxed{
    m_j^{(n)}
    =
    \frac{\binom{2n}{j}\bigl(D_j^2/2 - D_j\bigr)
          + \mathbf{1}_{j\text{ even}}\binom{n}{j/2}\,D_j/2}
         {\binom{2n}{j}\,P}
  }
$$
where
$$
  D_j = 2^{2n-j},\qquad
  P = (2^{2n}-1)(2^{2n-1}-2).
$$

## Proof

$\binom{t}{j}/\binom{2n}{j}$ is the probability that a uniformly random
$j$-subset $S \subseteq [2n]$ of coordinates is contained in the common support
$\operatorname{supp}(c_1)\cap\operatorname{supp}(c_2)$.  Hence
$$
  m_j^{(n)}
  =
  \frac{1}{\binom{2n}{j}}\sum_{|S|=j}
  \Pr[\,c_1,c_2 \in V_S\,],
$$
where $V_S = \{ v \in \F_2^{2n} : v_i=1 \text{ for all } i\in S \}$ and the
probability is over the random Lagrangian $L$ and random $c_1,c_2\in L$.

Averaging first over $L$, the expected number of ordered distinct isotropic
pairs in $L\cap V_S$ equals the total number of ordered distinct isotropic
pairs in $V_S$ times the probability that a fixed such pair spans a subspace
contained in $L$.  The latter factor is the same for every isotropic pair and
cancels when we divide by $P$, the total number of ordered distinct isotropic
pairs in $\F_2^{2n}$.  Therefore
$$
  m_j^{(n)} = \frac{1}{\binom{2n}{j}P}\sum_{|S|=j} N(S),
$$
where $N(S)$ is the number of ordered distinct pairs $(c_1,c_2)\in V_S^2$ with
$\langle c_1,c_2\rangle = 0$.

Write $V_S = v_0 + W_S$ with $W_S = \{w : w_i=0 \text{ for } i\in S\}$ and
$v_0$ the indicator of $S$.  For $c_i=v_0+w_i$,
$$
  \langle c_1,c_2\rangle
  = L(w_1)+L(w_2)+\langle w_1,w_2\rangle,
  \qquad L(w):=\langle v_0,w\rangle.
$$
Using orthogonality of characters,
$$
  N(S) = \frac{|W_S|^2}{2}
         + \frac{1}{2}\sum_{w_1,w_2\in W_S}
           (-1)^{L(w_1)+L(w_2)+\langle w_1,w_2\rangle}
         - |W_S|.
$$
Let $b$ be the number of symplectic pairs that meet $S$ in exactly one
coordinate.  Then $W_S$ has radical dimension $b$ and $W_S = R \oplus W_0$
with $W_0$ non-degenerate of dimension $2(n-a-b)$, where $a$ is the number of
full pairs contained in $S$.  The character sum factors as
$$
  \Bigl(\sum_{r\in R}(-1)^{L(r)}\Bigr)^2
  \cdot
  \sum_{z_1,z_2\in W_0}(-1)^{\langle z_1,z_2\rangle}.
$$
The second factor equals $|W_0|$.  The first factor is $|R|^2$ when $b=0$
(i.e. $S$ is a union of full symplectic pairs) and $0$ otherwise, because
$L$ is a non-zero linear functional on $R$ whenever $b\ge 1$.

Since $|W_S|=D_j=2^{2n-j}$ independently of the type of $S$, we obtain
$$
  N(S) =
  \begin{cases}
    D_j^2/2 - D_j/2, & b=0,\\
    D_j^2/2 - D_j,   & b\ge 1.
  \end{cases}
$$
The number of $j$-subsets $S$ with $b=0$ is $\binom{n}{j/2}$ when $j$ is even
(and $0$ when $j$ is odd).  Collecting terms gives the claimed formula.

## Consequences

- For fixed $j$ and $n\to\infty$,
  $$
    m_j^{(n)} = \frac{1}{4^j} + O\!igl(4^{-n}\bigr).
  $$
  Thus the $j$-th moment converges to the $j$-th moment of
  $\operatorname{Bernoulli}(1/4)$.

- The correction term is explicitly
  $$
    m_j^{(n)} - \frac{1}{4^j}
    =
    -\frac{2^{1-j}}{(4u-1)(u-1)}
    \Bigl(u + \mathbf{1}_{j\text{ even}}\frac{\binom{n}{j/2}}{\binom{2n}{j}}\Bigr),
  $$
  where $u=2^{2n-2}$.  In particular the discrepancy is negative for all
  $j\ge 1$ and decays like $4^{-n}$.

- For $j\ge 2n-1$ we have $m_j^{(n)}=0$, because $D_j\le 2$ forces
  $N(S)=0$ for every $S$.

## Verification

`experiments/193` computes the formula for $n\le 8$ and checks that $j=2,3$
agree with the previously established closed forms
$$
  m_2 = \frac{(2n-1)u^2-(4n-3)u}{4(2n-1)(4u^2-5u+1)},\qquad
  m_3 = \frac{u(u-4)}{16(4u^2-5u+1)}.
$$
All cross-checks pass.

## Implication for OP1 / lem:m2

The fixed-$k$ bundle variance multiplier
$V_k = \sum_{j=0}^k \binom{k}{j}\sigma^{2j}m_j^{(n)}$ now has **exact**
coefficients for every $j\le k$.  Therefore the deviation from the i.i.d.
$\operatorname{Bernoulli}(1/4)$ value is explicitly controlled:
$$
  \Bigl|V_k - \Bigl(1+\frac{\sigma^2}{4}\Bigr)^k\Bigr|
  = O_k(4^{-n}).
$$
No fixed-$k$ statistical test can distinguish the noise $Be$ from independent
$\operatorname{Bernoulli}(1/4)$ samples as $n\to\infty$.

No closure; no break; no security claim. OPEN = LSN.

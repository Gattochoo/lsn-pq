# OP1 Batch-Variance Multiplier for $j=\Theta(n)$

**Date:** 2026-06-14  
**Scripts:** `experiments/195-KIMI-op1-batch-variance-theta-n.py`,
`experiments/output/195-op1-batch-variance-theta-n.json`.

## Input: exact moments

From `meta/2026-06-14-KIMI-op1-general-j-moment-closure.md` and
`experiments/193-KIMI-op1-general-j-moment-closure.py`, for a uniformly
random Lagrangian subspace $L\subset\F_2^{2n}$ and random non-zero
$c_1,c_2\in L$ with $t=|\operatorname{supp}(c_1)\cap\operatorname{supp}(c_2)|$,

$$
  m_j^{(n)} = \E_A\!\left[\frac{\binom{t}{j}}{\binom{2n}{j}}\right]
$$
has the exact closed form

$$
  m_j^{(n)} =
  \frac{\binom{2n}{j}\bigl(D_j^2/2 - D_j\bigr)
        + \mathbf{1}_{j\text{ even}}\binom{n}{j/2}\,D_j/2}
       {\binom{2n}{j}\,P},
  \qquad
  D_j=2^{2n-j},\; P=(2^{2n}-1)(2^{2n-1}-2).
$$

We set $m_0^{(n)}=1$.

## The multiplier $V_k$

For standard OP1 noise parameters $p=1/4$ and
$\sigma=(1-2p)/\sqrt{p(1-p)}=2/\sqrt{3}$, so $\sigma^2=4/3$, the bundle
variance multiplier is

$$
  V_k = \sum_{j=0}^k \binom{k}{j}\sigma^{2j}m_j^{(n)}.
$$

For i.i.d. $\operatorname{Bernoulli}(1/4)$ noise the same multiplier is

$$
  V_k^{\text{iid}} = \Bigl(1+\frac{\sigma^2}{4}\Bigr)^k
                   = \Bigl(\frac{4}{3}\Bigr)^k.
$$

This note treats the $j=\Theta(n)$ extreme case $k=2n$, i.e.

$$
  V_{2n}^{\text{iid}} = \Bigl(\frac{16}{9}\Bigr)^n.
$$

## Exact closed form for $V_{2n}$

Substituting the moment formula into $V_{2n}$ and evaluating the two
binomial sums gives an exact rational closed form.  Writing $X=4^n$ and
$P=(X-1)(X-4)/2$, the result is

$$
  \boxed{
    V_{2n} =
    \frac{X^4 - 2X\cdot 25^n + X\cdot 13^n - 4X\cdot 9^n + 4\cdot 9^n}
         {9^n\,(X-1)(X-4)}
  }.
$$

Equivalently, after dividing by the i.i.d. value,

$$
  \frac{V_{2n}}{V_{2n}^{\text{iid}}}
  =
  \frac{X^4 - 2X\cdot 25^n + X\cdot 13^n - 4X\cdot 9^n + 4\cdot 9^n}
       {X^2\,(X-1)(X-4)}.
$$

The script `experiments/195` computes this closed form and cross-checks it
against a direct summation over $j=0,\dots,2n$ using the general moment
formula.  All checks for $n\le 10$ match exactly.

## Asymptotics

Expanding the exact expression in powers of $X^{-1}=4^{-n}$ yields the
following precise asymptotic expansion:

$$
  V_{2n}
  =
  \Bigl(\frac{16}{9}\Bigr)^n
  -2\Bigl(\frac{25}{36}\Bigr)^n
  +5\Bigl(\frac{4}{9}\Bigr)^n
  +\Bigl(\frac{13}{36}\Bigr)^n
  -4\Bigl(\frac14\Bigr)^n
  +O\!\Bigl(\Bigl(\frac{25}{144}\Bigr)^n\Bigr).
$$

In particular the **relative** deviation from the i.i.d. multiplier is

$$
  \frac{V_{2n}-V_{2n}^{\text{iid}}}{V_{2n}^{\text{iid}}}
  =
  -2\Bigl(\frac{25}{64}\Bigr)^n
  + O\!\Bigl(\Bigl(\frac{1}{4}\Bigr)^n\Bigr),
$$

which tends to zero **exponentially fast**.  The absolute deviation
$V_{2n}-V_{2n}^{\text{iid}}$ also decays to zero after a small initial
peak around $n=4$.

### Numerical evidence

| $n$ | $V_{2n}$ | $V_{2n}^{\text{iid}}$ | relative deviation | $\log(V_{2n}/V_{2n}^{\text{iid}})$ |
|----:|---------:|----------------------:|-------------------:|------------------------------------:|
| 2  | 2.9753   | 3.1605                | $-5.86\times10^{-2}$ | $-6.04\times10^{-2}$ |
| 4  | 9.7142   | 9.9887                | $-2.75\times10^{-2}$ | $-2.79\times10^{-2}$ |
| 6  | 31.3845  | 31.5693               | $-5.85\times10^{-3}$ | $-5.87\times10^{-3}$ |
| 8  | 99.6742  | 99.7746               | $-1.01\times10^{-3}$ | $-1.01\times10^{-3}$ |
| 10 | 315.2862 | 315.3369              | $-1.61\times10^{-4}$ | $-1.61\times10^{-4}$ |
| 12 | 996.5953 | 996.6202              | $-2.49\times10^{-5}$ | $-2.49\times10^{-5}$ |

For example, at $n=12$ the leading approximation
$V_{2n}\approx (16/9)^n -2(25/36)^n +5(4/9)^n + (13/36)^n -4(1/4)^n$
gives a value that differs from the exact $V_{2n}$ by only
$7.4\times10^{-9}$, confirming the expansion.

## Interpretation for §Moments / OP1

- The exact $m_j^{(n)}$ closure lets us evaluate the bundle variance
  multiplier even at the maximal block length $k=2n$.
- Far from diverging, $V_{2n}$ stays within an **exponentially small**
  relative distance of the i.i.d. $\operatorname{Bernoulli}(1/4)$ value.
- This strengthens the OP1 moment indistinguishability claim: even when
  the summation block size scales linearly with $n$, the second-order
  statistics of the LSN noise remain asymptotically identical to the
  i.i.d. reference.
- No new statistical distinguisher based on bundle variance appears at
  $k=2n$.

## Open sub-problems

1. **General $k=\alpha n$:** The same binomial-summation technique gives
   exact formulas for $V_{\alpha n}$ with any fixed rational $\alpha$;
   is the relative deviation always exponentially small in $n$?
2. **Higher cumulants:** The variance multiplier is only one summary.
   Do higher cumulants / the full distribution of the bundle sum also
   collapse to the i.i.d. case for $k=\Theta(n)$?
3. **Sub-exponential prefactors:** The leading coefficient $-2$ in the
  relative-deviation expansion comes from the $25^n$ term.  A rigorous
  derivation of the full expansion (including the $O((25/144)^n)$
  remainder) is a straightforward but tedious formal power-series
  exercise.

# Track I deliverable: closed-form joint generating function for pairwise composition

**Date:** 2026-06-14.  
**Track:** I.  
**Experiment:** `experiments/225-KIMI-trackI-joint-composition-generating-function.py`.  
**Output:** `experiments/output/225-KIMI-trackI-joint-composition.json`.  
**Prefix:** `track-I:`.

## Summary

Closed the two-secret pairwise-level joint composition problem.  For an ordered
isotropic pair $(c_1,c_2) \in \F_2^{2n}$ (nonzero, distinct, $\Omega(c_1,c_2)=0$),
let $t_{\tau}$ count coordinates of category $\tau \in \{11,10,01,00\}$.  The joint
generating function

$$
G_n(x_{11},x_{10},x_{01},x_{00})
= \E\Bigl[\prod_\tau x_\tau^{t_\tau}\Bigr]
$$

over the ordered isotropic-pair ensemble has the closed form

$$
G_n = \frac{1}{P}\Bigl[
    \frac{T^{2n} + S^n}{2}
    - A^{2n} - B^{2n} - C^{2n}
    + 2x_{00}^{2n}
\Bigr],
$$

where

$$
\begin{aligned}
T &= x_{11}+x_{10}+x_{01}+x_{00},\\
S &= T^2 - 4(x_{10}x_{01}+x_{10}x_{11}+x_{01}x_{11}),\\
A &= x_{00}+x_{01},\quad B = x_{00}+x_{10},\quad C = x_{00}+x_{11},\\
P &= (2^{2n}-1)(2^{2n-1}-2).
\end{aligned}
$$

**Claim label:** THEOREM.

## Proof method (radical / non-degenerate character sum, with J-twist)

Write the isotropic indicator as a character sum:

$$
\mathbf 1_{\Omega(c_1,c_2)=0}
= \frac12 \sum_{\lambda\in\F_2} (-1)^{\lambda\, \Omega(c_1,c_2)}.
$$

* Trivial character ($\lambda=0$): the "radical" contribution, equal to
  $T^{2n}$.
* Non-trivial character ($\lambda=1$): the non-degenerate contribution.  It
  factorizes over the $n$ symplectic coordinate pairs; each pair contributes
  $S$.  The exponent uses the standard symplectic form $\Omega$, whose Gram
  matrix is $J$ --- this is the required **J-twist** (L2 guard).

Finally subtract the excluded cases $c_1=0$, $c_2=0$, and $c_1=c_2$, which
contribute $A^{2n}$, $B^{2n}$, and $C^{2n}$, and add back their triple
intersection $2x_{00}^{2n}$.

## Verification (EVIDENCE)

Direct enumeration of the ordered isotropic-pair ensemble for $n=2,3,4$:

| $n$ | $2n$ | ordered pairs | distinct compositions | polynomial matches enumeration |
|-----|------|---------------|-----------------------|--------------------------------|
| 2   | 4    | 90            | 15                    | yes                            |
| 3   | 6    | 1,890         | 56                    | yes                            |
| 4   | 8    | 32,130        | 128                   | yes                            |

All coefficients are non-negative and sum to $1$.

## Corollaries (THEOREM)

### (a) Re-derivation of `thm:mj-general`

Specializing $x_{11}\mapsto 1+x$, $x_{10}=x_{01}=x_{00}=1$ gives
$\E[(1+x)^{t_{11}}]$.  The coefficient of $x^j$ is $\E[\binom{t_{11}}{j}]$,
which matches the closed form of `thm:mj-general` for every $j$ and every
verified $n$.

### (b) Re-derivation of `prop:tdist`

Specializing $x_{11}\mapsto x$, $x_{10}=x_{01}=x_{00}=1$ gives the exact law
of $t_{11}$.  It matches the binomial inversion of the moments $B_j$ from
`prop:tdist`, including the vanishing $\Pr[t_{11}=\ell]=0$ for
$\ell \ge 2n-1$.

### (c) Exact law of the disagreement count $d = t_{10}+t_{01}$

Specializing $x_{11}=x_{00}=1$, $x_{10}=x_{01}=y$ collapses $S$ to $4$ and
yields

$$
\Pr[d=0]=0,\qquad
\Pr[d=k]=\frac{\binom{2n}{k}}{2^{2n}-1}\quad (k=1,\dots,2n).
$$

Verified for $n=2,3,4,5,6$.

**Claim label:** THEOREM.

## Governance and guards

* **File isolation:** Only Track I files touched:
  * `experiments/225-KIMI-trackI-joint-composition-generating-function.py`
  * `experiments/output/225-KIMI-trackI-joint-composition.json`
  * this meta note.
* **Number block:** 225 (within Track I block 225--229).
* **L1 exact arithmetic:** `fractions.Fraction` end-to-end; JSON stores
  rationals as strings.
* **L2 J-twist care:** the character sum uses $(-1)^{\Omega(c_1,c_2)}$ with the
  standard symplectic form (Gram matrix $J$).  Summation is over $V\times V$,
  so no dual-space confusion arises.
* **L3 query-class hygiene:** this is a pairwise-level structural counting
  result.  No unrestricted SQ hardness claim is made.
* **PRE-REGISTER interpretation guard:**
  * Scope is the two-secret pairwise level only; the multi-pair joint
    composition remains **OPEN**.
  * The natural benchmark for $t_{11}$ is $\mathrm{Bin}(2n,1/4)$, the law under
    unconstrained i.i.d. uniform rows.
  * The closed form is a structural result; it does not by itself imply SQ
    hardness for full learning tasks.

## Discipline

Sound Verifier.  No closure; no break; no security claim.  OPEN = LSN.

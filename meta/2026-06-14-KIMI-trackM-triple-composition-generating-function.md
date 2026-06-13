# Track M — Triple-composition generating function (M1–M3)

**Date:** 2026-06-14  
**Author:** Kimi (subagent, Track M)  
**Repository:** Gattochoo/lsn-pq  
**Status:** green / ready for adjudication  
**Commit prefix:** `track-M:`

## Scope

Track M closes the first object at the multi-secret-pair level: the exact joint
composition generating function for an ordered isotropic **triple**
$(c_1, c_2, c_3)$ in $\F_2^{2n}$ that is pairwise isotropic and linearly
independent.

## Files

| # | Path | Purpose |
|---|------|---------|
| 226 | `experiments/226-KIMI-trackM-triple-composition-generating-function.py` | Closed-form 8-variable GF and enumeration verification. |
| 227 | `experiments/227-KIMI-trackM-pair-marginals.py` | Corollary (a): each pair-marginal reproduces `thm:joint-gf`. |
| 228 | `experiments/228-KIMI-trackM-triple-quadrant-law.py` | Corollary (b): law of $t_{111}$ (triple-quadrant count). |
| 229 | `experiments/229-KIMI-trackM-agreement-statistic.py` | Corollary (c): exact distribution of the agreement count $a=t_{000}+t_{111}$. |
| out | `experiments/output/226-KIMI-trackM-triple-gf.json` | Count/probability polynomial. |
| out | `experiments/output/227-KIMI-trackM-pair-marginals.json` | Marginal verification. |
| out | `experiments/output/228-KIMI-trackM-triple-quadrant-law.json` | $t_{111}$ table. |
| out | `experiments/output/229-KIMI-trackM-agreement-statistic.json` | Agreement-count table. |

## THEOREM: 8-variable triple-composition GF

For $\tau=(\tau_1,\tau_2,\tau_3)\in\F_2^3$ let $x_\tau$ be a formal variable
and $t_\tau$ the number of coordinates with category $\tau$.  For a subspace
$L\subseteq\F_2^3$ define

$$
T_L(x)=\sum_{\tau\in L} x_\tau,
$$

$$
S_{\lambda,L}(x)=\sum_{u,v\in L}
(-1)^{\lambda_{12}(u_1v_2+u_2v_1)
      +\lambda_{13}(u_1v_3+u_3v_1)
      +\lambda_{23}(u_2v_3+u_3v_2)}
x_u x_v,
\qquad\lambda\in\F_2^3,
$$

and

$$
G_L(x)=\frac{1}{8}\Bigl(T_L(x)^{2n}+\sum_{\lambda\neq0}S_{\lambda,L}(x)^n\Bigr).
$$

Then the generating function for ordered isotropic independent triples is

$$
G_n^{(3)}(x)
=\frac{1}{P_3(n)}
\Bigl(
  G_{\F_2^3}
  -\sum_{H\text{ hyperplane}} G_H
  +2\sum_{\ell\text{ line}} G_\ell
  -8\,G_{\{0\}}
\Bigr),
$$

with

$$
P_3(n)=(2^{2n}-1)(2^{2n-1}-2)(2^{2n-2}-4).
$$

The coefficients $(+1,-1,+2,-8)$ are the Möbius function values of the
$\F_2$-subspace lattice; equivalently they arise from inclusion–exclusion over
the seven non-zero linear forms on $\F_2^3$ (the three zero-vector events,
the three equality events, and the relation $c_1+c_2+c_3=0$).

## Verification results

| $n$ | $P_3(n)$ | enum count | monomials | polynomial match |
|-----|----------|------------|-----------|------------------|
| 2   | 0        | 0          | 0         | degenerate       |
| 3   | 22,680   | 22,680     | 539       | **True**         |
| 4   | 1,927,800| 1,927,800  | 4,012     | **True**         |

Pair-marginals (experiment 227) match `thm:joint-gf` for all three ordered
pairs at both $n=3$ and $n=4$.

## Count correction

The Track M reminder parenthetically wrote the $n=4$ count as
$255\cdot126\cdot56 = 1{,}799{,}280$.  The correct third factor is
$2^{2n-2}-4 = 64-4 = 60$, giving $255\cdot126\cdot60 = 1{,}927{,}800$,
which is exactly what enumeration returns.  The script and outputs use the
corrected value and note the discrepancy.

## Claim labels

- **THEOREM:** closed-form 8-variable triple-composition GF (`226`).
- **THEOREM:** $P_3(n)$ count law (`226`).
- **THEOREM:** pair-marginals reproduce `thm:joint-gf` (`227`).
- **THEOREM:** triple-quadrant count law for $t_{111}$ (`228`).
- **THEOREM:** exact distribution of the agreement count $a=t_{000}+t_{111}$ (`229`).
- **EVIDENCE:** coefficient-wise enumeration match at $n=3,4$ (`226`).
- **EVIDENCE:** $t_{111}$ table match by direct enumeration (`228`).
- **EVIDENCE:** agreement-count table match at $n=3$ (`229`).
- **OPEN:** full multi-pair SQ level.

## Guards

- **L1 exact arithmetic:** all values are `fractions.Fraction`; JSON stores
  rationals as strings and counts as integers.
- **L2 J-twist duality:** the character sum uses the standard symplectic form
  $\Omega$ on $V\times V$; the per-symplectic-pair contraction avoids any
  dual-space confusion.
- **L3 query-class hygiene:** this is a structural counting result at the
  three-secret level.  No Feldman inference or unrestricted SQ-hardness claim
  is made.
- **L4 comparison distribution:** not engaged; this track contains no
  comparison-distribution transformation.

## PRE-REGISTER interpretation guard

- **Scope:** three-secret pairwise level only.  The full multi-pair SQ level
  remains OPEN.
- **Benchmark:** ignoring the isotropy constraints would give an 8-way
  multinomial; the GF captures the exact dependence induced by isotropy and
  independence.
- **Hardness implication:** the closed-form GF is a structural counting
  theorem.  It does not, by itself, imply SQ lower bounds for full learning
  tasks.

## Discipline

Sound Verifier.  No closure; no break; no security claim.  OPEN = LSN.

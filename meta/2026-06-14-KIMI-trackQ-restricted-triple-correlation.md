# Track Q — Triple-level SQ: exact 3-wise correlation for restricted 3-local parity queries

**Date:** 2026-06-14.  
**Track:** Q (numbers 320–329).  
**Files:**
- `experiments/320-KIMI-trackQ-triple-correlation.py`
- `experiments/output/320-KIMI-trackQ-triple-correlation.json`
- this meta note

**Commit prefix:** `track-Q:`  
**Status:** DRAFT for Claude adjudication; no `paper/` edits.

---

## 1. What this note does

Computes the exact **3-wise correlation** of **restricted 3-local parity queries**
for the **sympLPN** formulation, using the triple-composition GF (`thm:triple-gf`)
from Track M.

The sympLPN sample is one full block $(A,y)$ with $A\sim\mathcal A_n$ (uniform
ordered basis of a uniform Lagrangian $L\subseteq\F_2^{2n}$) and $y=Ax+e$,
$e\sim\Bernoulli(p)^{2n}$.  The null $D_0$ draws $y$ uniformly independent of
$A$.  For a fixed non-empty $S\subseteq[2n]$, $|S|=k$, the $k$-local parity
query is

$$
h^{(S)}(A,y)=(-1)^{\sum_{i\in S}y_i}.
$$

Its conditional expectation (advantage function) under secret $x$ is

$$
g_x(A)=\E_{D_x\mid A}\bigl[h^{(S)}\bigr]
      =(-1)^{\langle\mathbf 1_S,Ax\rangle}(1-2p)^k.
$$

The 3-wise correlation is
$\E_{A\sim\mathcal A_n}[g_x(A)g_{x'}(A)g_{x''}(A)]$.

---

## 2. THEOREM: exact 3-wise correlation

**THEOREM Q.1.**  Fix $n\ge 1$, $p\in(0,1/2)$, a non-empty $S\subseteq[2n]$,
$|S|=k$, and secrets $x,x',x''\in\F_2^n$.  Then

$$
\E_{A\sim\mathcal A_n}\bigl[g_xg_{x'}g_{x''}\bigr]
=
\begin{cases}
(1-2p)^{3k}, & x+x'+x''=0,\\[4pt]
-\displaystyle\frac{(1-2p)^{3k}}{2^{2n}-1}, & x+x'+x''\neq 0.
\end{cases}
$$

Equivalently, with $w=x+x'+x''$,

$$
\E_A\bigl[(-1)^{\langle\mathbf 1_S,Aw\rangle}\bigr]
=
\begin{cases}
1, & w=0,\\
-\frac{1}{2^{2n}-1}, & w\neq 0.
\end{cases}
$$

The value is independent of the particular non-empty $S$.

**Proof.**  Multiplying the three advantage functions gives

$$
g_xg_{x'}g_{x''}=(1-2p)^{3k}(-1)^{\langle\mathbf 1_S,A(x+x'+x'')\rangle}.
$$

If $w=0$ the phase is identically $1$.  If $w\neq 0$, then $v=Aw$ is uniform
over $L\setminus\{0\}$ for a uniform ordered basis $A$ of $L$.  Hence

$$
\E_A[(-1)^{\langle\mathbf 1_S,v\rangle}]
=\E_L\!\left[\frac{1}{2^n-1}\sum_{v\in L\setminus\{0\}}(-1)^{\langle\mathbf 1_S,v\rangle}\right].
$$

For a fixed Lagrangian $L$,
$\sum_{v\in L}(-1)^{\langle\mathbf 1_S,v\rangle}=2^n\mathbf 1_{\{J\mathbf 1_S\in L\}}$,
where $J$ is the Gram matrix of the standard symplectic form.  Since
$J\mathbf 1_S\neq 0$ for non-empty $S$, $\Pr_L[J\mathbf 1_S\in L]=1/(2^n+1)$ by
$\Sp(2n,\F_2)$-transitivity, giving

$$
\frac{1}{2^n-1}\left(\frac{2^n}{2^n+1}-1\right)=-\frac{1}{2^{2n}-1}.
$$

∎

**Connection to `thm:triple-gf`.**  When $x,x',x''$ are linearly independent,
$(Ax,Ax',Ax'')$ is a uniform ordered independent isotropic triple in $L$.
Specializing the Track M triple GF at
$x_\tau=(-1)^{\tau_1+\tau_2+\tau_3}$ computes exactly
$\E[(-1)^{\langle\mathbf 1,Ax+Ax'+Ax''\rangle}]$; the closed form matches
$-1/(2^{2n}-1)$.  This is the promised “$1_L$-membership across the three
secrets” specialization.

---

## 3. Verified exact values ($p=1/4$, $k=3$)

All values are reproduced by `experiments/320-KIMI-trackQ-triple-correlation.py`.

| $n$ | diagonal ($x+x'+x''=0$) | off-diagonal ($x+x'+x''\neq 0$) | $\E[\text{sign}]$ (independent triples) | avg $|\text{corr}|$ over all secret triples |
|----:|--------------------------:|----------------------------------:|----------------------------------------:|---------------------------------------------:|
| 3   | $1/512$                  | $-1/32256$                       | $-1/63$                                 | $5/18432$                                    |
| 4   | $1/512$                  | $-1/130560$                      | $-1/255$                                | $9/69632$                                    |

Verification method:
- Direct enumeration over all Lagrangians and all ordered independent triples
  (resp. sum-zero dependent pairs) at $n=3,4$.
- Coefficient-wise consistency check against the Track M triple-GF output
  (`experiments/output/226-KIMI-trackM-triple-gf.json`).

---

## 4. Restricted-query SQ statement (L3)

**Query class.**  $\mathcal Q_3=\{h^{(S)}:|S|\le 3,\;S\neq\emptyset\}$, the
3-local parity queries on a sympLPN block.

**THEOREM/EVIDENCE.**  For every query in $\mathcal Q_3$ the 3-wise correlations
are either $(1-2p)^{3|S|}$ on the $4^n$ secret triples with $x+x'+x''=0$, or
$-(1-2p)^{3|S|}/(2^{2n}-1)$ on all other triples.  In particular the average
absolute 3-wise correlation over all secret triples is

$$
(1-2p)^{3|S|}\cdot\frac{2^n+2}{2^n(2^n+1)}.
$$

At $p=1/4$ and $|S|=3$ this is $5/18432$ for $n=3$ and $9/69632$ for $n=4$:
exponentially small, just like the pairwise correlations.

**L3 guard / OPEN item.**  This is a statement **only** for the restricted
class $\mathcal Q_3$.  It does **not** plug into `cor:symplpn-sq`, whose
Feldman application requires **arbitrary** bounded queries.  To obtain a query
lower bound for algorithms constrained to $\mathcal Q_3$ one would need a
separate restricted-SQ dimension theorem for $k$-local parity queries.  We do
not cite such a theorem here, so the SQ-hardness implication is labelled
**OPEN**.

---

## 5. Claim labels

| Claim | Label |
|-------|-------|
| Exact 3-wise correlation formula (Theorem Q.1) | **THEOREM** |
| Enumeration verification at $n=3,4$ | **EVIDENCE** |
| Triple-GF specialization consistency | **EVIDENCE** |
| Isotropic conditioning does not help a 3-local parity distinguisher | **EVIDENCE** |
| SQ lower bound for the restricted class $\mathcal Q_3$ | **OPEN** |
| No unrestricted Feldman inference | **GUARD (L3)** |

---

## 6. Standing guards

- **L1 exact arithmetic:** `fractions.Fraction` end-to-end; JSON stores
  rationals as strings.
- **L2 J-twist duality:** the sign uses the standard dot product on
  $\F_2^{2n}$; the Lagrangian character-sum / symplectic form is inherited from
  the Track M triple GF.
- **L3 query-class hygiene:** all claims are for the restricted 3-local-parity
  query class; they are **not** applied to the unrestricted Feldman theorem or
  to `cor:symplpn-sq`.
- **L4 comparison distribution:** no comparison distribution is transformed.

## 7. PRE-REGISTER interpretation guards

1. **Scope:** exact correlation for 3-local parity queries on one sympLPN block.
2. **Benchmark:** the unconstrained LPN ensemble has off-diagonal 3-wise
   correlation $0$; the isotropic ensemble adds only $-d/(2^{2n}-1)$.
3. **Hardness implication:** small correlations are evidence of structural
   closeness, not a proof of SQ hardness; a restricted-SQ theorem would be
   needed (OPEN).

---

## 8. Files touched (Track Q only)

- `experiments/320-KIMI-trackQ-triple-correlation.py` (new)
- `experiments/output/320-KIMI-trackQ-triple-correlation.json` (new)
- `meta/2026-06-14-KIMI-trackQ-restricted-triple-correlation.md` (this file)

No `paper/` edits, no other tracks’ files, no `impl/polar_validation/`, no
Claude adjudication scripts $\ge 340$.

---

Discipline: Sound Verifier.  No closure; no break; no security claim.  **OPEN = LSN.**

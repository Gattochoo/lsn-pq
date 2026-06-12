# Track C — Exact distribution of the quadrant count `t` (pairwise level)

**Date:** 2026-06-14.  
**Experiment:** `experiments/220-KIMI-trackC-exact-t-distribution.py`.  
**Output:** `experiments/output/220-KIMI-trackC-exact-t-distribution.json`.  
**Author:** Kimi (Track C).  
**Status:** standing Track-C deliverable; awaiting Claude adjudication.

---

## 1. What was computed

For the isotropic (symplectic-LPN) public-matrix ensemble, fix one secret pair
$(x,x')=(e_1,e_2)$ and let

```
t = |{ i in [2n] : <a_i,x> = <a_i,x'> = 1 }|
```

be the quadrant-count statistic.  Writing $B_j := \mathbb{E}[\binom{t}{j}]$,
the paper’s `thm:mj-general` gives

```
B_j = ( C(2n,j) * (D_j^2/2 - D_j) + 1_{j even} * C(n,j/2) * D_j/2 ) / P,
```

with

```
u = 2^{2n-2},    D_j = 2^{2n-j},    P = (2^{2n}-1)(2^{2n-1}-2).
```

The distribution of $t$ is recovered by the binomial (inclusion–exclusion)
transform

```
Pr[t = ell] = sum_{j=ell}^{2n} (-1)^{j-ell} * C(j,ell) * B_j .
```

This yields an exact closed-form rational expression for every
$\Pr[t=\ell]$, $0\le\ell\le 2n$, and every $n\ge 1$.

---

## 2. Claim labels

| Claim | Label | Justification |
|---|---|---|
| Exact $\Pr[t=\ell]$ from the transform of `thm:mj-general` | **THEOREM** | `thm:mj-general` is proven in `paper/lsn-core.tex`; the binomial inversion is standard and implemented exactly. |
| Equality of transform and direct enumeration for $n=2,3,4$ | **EVIDENCE** | Exact rational enumeration over all ordered isotropic pairs; no closed-form result is imported into the check. |
| Exact TV distances for $n\le 10$ | **EVIDENCE** | Exact rational computation; finite-$n$ tabulation, not a limit theorem. |
| Asymptotic rate $\operatorname{TV} \sim 2^{-(n+1)}$ | **EVIDENCE / OPEN** | Numerically supported ($2^n\cdot\operatorname{TV}\to 1/2$); a full proof is sketched below but not written out in full formality. |

---

## 3. Exact values

### 3.1 Distribution of $t$ for $n=2$

```
Pr[t=0] = 11/45
Pr[t=1] = 4/9
Pr[t=2] = 14/45
Pr[t=3] = 0
Pr[t=4] = 0
```

### 3.2 Distribution of $t$ for $n=3$

```
Pr[t=0] = 10/63
Pr[t=1] = 12/35
Pr[t=2] = 22/63
Pr[t=3] = 4/35
Pr[t=4] = 11/315
Pr[t=5] = 0
Pr[t=6] = 0
```

### 3.3 Distribution of $t$ for $n=4$

```
Pr[t=0] = 1541/16065
Pr[t=1] = 824/3213
Pr[t=2] = 596/1785
Pr[t=3] = 3184/16065
Pr[t=4] = 212/2295
Pr[t=5] = 104/5355
Pr[t=6] = 4/1071
Pr[t=7] = 0
Pr[t=8] = 0
```

The full rational tables for $n=2,3,4$ and the binomial moments $B_j$ are in
`experiments/output/220-KIMI-trackC-exact-t-distribution.json`.

---

## 4. Total-variation to $\operatorname{Bin}(2n,1/4)$

The unconstrained i.i.d. row ensemble has exactly
$t\sim\operatorname{Bin}(2n,1/4)$.  The exact total-variation distance is:

| $n$ | $2n$ | $\operatorname{TV}$ (exact) | $\operatorname{TV}$ (float) | $2^n\cdot\operatorname{TV}$ |
|---|---|---|---|---|
| 2 | 4 | $707/5760$ | $1.2274\times10^{-1}$ | $0.491$ |
| 3 | 6 | $35183/645120$ | $5.4537\times10^{-2}$ | $0.436$ |
| 4 | 8 | $14891599/526417920$ | $2.8289\times10^{-2}$ | $0.453$ |
| 5 | 10 | $788813171/54707355648$ | $1.4419\times10^{-2}$ | $0.462$ |
| 6 | 12 | $129011724689/17570715402240$ | $7.3424\times10^{-3}$ | $0.470$ |
| 7 | 14 | $90177646929/23821297909760$ | $3.7856\times10^{-3}$ | $0.485$ |
| 8 | 16 | $8866562072659001/4611334179001466880$ | $1.9228\times10^{-3}$ | $0.493$ |
| 9 | 18 | $12710182327048981/13117434475422154752$ | $9.6895\times10^{-4}$ | $0.496$ |
| 10 | 20 | $29399506915728870947/60446002750575209349120$ | $4.8638\times10^{-4}$ | $0.498$ |

The data strongly suggest

```
TV( dist(t), Bin(2n,1/4) )  ~  1/2 * 2^{-n}  =  2^{-(n+1)} .
```

A rigorous proof is **not completed here**; we label the rate **EVIDENCE**.
A sketch: the isotropic condition $\Omega(c_1,c_2)=0$ is a single non-degenerate
linear constraint on the $2n$ symplectic coordinate-pairs.  In Fourier language
over $\mathbb{F}_2^{2n}$, the difference between the conditional and
unconditional pair-pattern distributions is supported on the non-trivial
additive character of that constraint, which contributes a factor $2^{-n}$ at
the level of any marginal such as $t$.  Because the constraint is satisfied
with probability $1/2$ and changes sign patterns by $\pm 1$, the total
variation of the induced $t$-distribution is asymptotically half that factor.

---

## 5. Interpretation guard (PRE-REGISTER)

1. **Comparison distribution.**  $\operatorname{Bin}(2n,1/4)$ is the exact law
   of $t$ under the **unconstrained** i.i.d. uniform row ensemble.  It is the
   natural matched benchmark for the same quadrant-count statistic; it is not
   an LPN output-noise distribution.

2. **Scaling.**  This is a **single secret-pair** (pairwise-level) result.
   The parameter $m$ does not appear.  It is not a joint test across many
   secret pairs.

3. **Hardness implication.**  The small TV shows that the isotropic
   conditioning is statistically close to unconstrained at the level of one
   secret pair.  This is structural evidence only; it does **not** by itself
   bound SQ hardness for multi-pair or full learning tasks.  Those require the
   bundle/SDA machinery (Track E) and remain OPEN for the full SQ statement.

---

## 6. Files touched

Only Track-C files:

- `experiments/220-KIMI-trackC-exact-t-distribution.py`
- `experiments/output/220-KIMI-trackC-exact-t-distribution.json`
- `meta/2026-06-14-KIMI-trackC-exact-t-distribution.md`

No shared library files were modified; no `paper/` files were touched.

---

## 7. Commit

```
track-C: exact distribution of pairwise quadrant count t (exp 220)
```

Staging was explicit: only the three Track-C files above were committed.

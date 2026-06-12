# Track B — OP7 T-independence theorem and exact $f(n)$

**Date:** 2026-06-14  
**Script:** `experiments/210-KIMI-trackB-OP7-T-independence.py`  
**Output:** `experiments/output/210-trackB-OP7-T-independence.json`

---

## 1. Question

OP7 asks whether a public symplectic transformation can turn one LSN sample into
a pair of fresh independent samples for a rerandomized secret.  Formally, choose
$L\sim\operatorname{Unif}(\operatorname{Lagr}(2n,\F_2))$, draw one sample
$(x,b)\sim D_L$ with $b=\mathbf 1_L(x)+e$, $e\sim\operatorname{Bernoulli}(1/4)$,
and apply two public symplectic matrices $S_1,S_2$ to obtain
$(S_1 x,b)$ and $(S_2 x,b)$.  The SD between this joint distribution and two
independent fresh samples from $D_{S_1 L}$ and $D_{S_2 L}$ depends a priori only
on $T=S_1^{-1}S_2$.

Track B asks: is the SD independent of $T\in\operatorname{Sp}(2n,\F_2)$, and if
so, what is its exact value $f(n)$ at $n=3,4$?

---

## 2. Results

### THEOREM B.1 (T-independence)

For every $n\ge1$ and every $T\in\operatorname{Sp}(2n,\F_2)$,

$$\mathrm{SD}\bigl(P_T, Q_T\bigr) = \mathrm{SD}\bigl(P_I, Q_I\bigr),$$

where $P_T$ is the transformed pair distribution and $Q_T$ is the fresh-pair
distribution with the corrected rerandomized-secret convention
$\mathbf 1_{T\cdot L}(T u)=\mathbf 1_L(u)$.

**Proof.**  After multiplying the whole experiment by $S_1^{-1}$, the second
public matrix becomes $T=S_1^{-1}S_2$ and the two distributions are

- $P_T$: choose $L$, $u\sim\operatorname{Unif}(\F_2^{2n})$, $e\sim\operatorname{Bernoulli}(p)$;
  output $(u,\;\mathbf 1_L(u)+e,\;Tu,\;\mathbf 1_L(u)+e)$.
- $Q_T$: choose $L$, $u,w\sim\operatorname{Unif}(\F_2^{2n})$ i.i.d.,
  $e_1,e_2\sim\operatorname{Bernoulli}(p)$ i.i.d.; output
  $(u,\;\mathbf 1_L(u)+e_1,\;Tw,\;\mathbf 1_L(w)+e_2)$.

Apply the bijection
$\Phi_T:(u,b_1,z,b_2)\mapsto(u,b_1,Tz,b_2)$ to *both* distributions.  Since
$\Phi_T$ is a bijection on the sample space, total-variation distance is
preserved.  We have $\Phi_T^{-1}\#P_T = P_I$ and $\Phi_T^{-1}\#Q_T = Q_I$, so

$$\mathrm{SD}(P_T,Q_T)=\mathrm{SD}(P_I,Q_I).$$

The right-hand side does not depend on $T$. ∎

### THEOREM B.2 (closed form for $f(n)$)

For the standard LSN noise rate $p=1/4$,

$$f(n) := \mathrm{SD}(P_I,Q_I) = 1 - \frac{p^2+(1-p)^2}{4^n}
      = 1 - \frac{5}{8\cdot 4^n}.$$

In particular

| $n$ | $f(n)$ | decimal |
|----:|-------:|--------:|
| 2 | $123/128$ | $0.9609375$ |
| 3 | $507/512$ | $0.990234375$ |
| 4 | $2043/2048$ | $0.99755859375$ |

**Proof.**  For $T=I$ the transformed distribution $P$ is supported only on the
diagonal equal-bit keys $(u,b,u,b)$.  Its mass there is
$\Pr_L[e=b-\mathbf 1_L(u)]/(N_L\cdot 2^{2n})$.  The fresh distribution $Q$ puts
mass on all keys $(u,b_1,v,b_2)$.  For every diagonal key,
$Q(u,b,u,b) \le 1/4^{2n} < P(u,b,u,b)$, so the overlapping mass is exactly the
total diagonal mass of $Q$.  Summing over the $2^{2n}$ choices of $u$ and the two
bit patterns $b\in\{0,1\}$ gives

$$\sum_{u,b} Q(u,b,u,b)
  = \frac{1}{2^{2n}}\bigl(p^2+(1-p)^2\bigr).$$

Since $P$ is zero off the diagonal, the statistical distance is one minus this
overlap, yielding the formula. ∎

---

## 3. Computational verification (EVIDENCE)

The script uses exact integer counting with `fractions.Fraction`.

- **n=2:** Enumerated all $|\operatorname{Sp}(4,\F_2)|=720$ matrices.  Every
  single one gives SD $=123/128$, matching the formula.
- **n=3:** Tested the identity and 5 random elements of
  $\operatorname{Sp}(6,\F_2)$ (generated as words of transvections).  All give
  SD $=507/512$, matching the formula.
- **n=4:** Reported the closed-form value $2043/2048$.

These checks are **EVIDENCE**; the constancy and the closed form themselves are
**THEOREM**-grade from §2.

---

## 4. Interpretation guard (PRE-REGISTER)

Before claiming any hardness implication:

1. **Comparison distribution:** two independent fresh samples from
   $D_{S_1L}, D_{S_2L}$, same noise rate $p=1/4$ (matched).
2. **Scaling:** structural result in the $2n$-dimensional secret space; no
   fixed-$m$ or small-$m$ artifact.
3. **Output SD:** $f(n)=1-5/(8\cdot4^n)$ is bounded away from $1/2$ and tends to
   $1$.  The public symplectic orbit transformation therefore does **not**
   produce fresh samples.

---

## 5. Scope guard

- This settles OP7 **negatively for the symplectic-orbit family at every $n$**.
- It does **not** rule out arbitrary public transformations outside the
  symplectic group; such transformations are outside the scope of this theorem.
- The membership convention used is the corrected one: the fresh second sample's
  secret is $T\cdot L$, so its label is $\mathbf 1_{T\cdot L}(Tu)=\mathbf 1_L(u)$.
  (The old 192 bug used $\mathbf 1_L(Tu)$.)

---

## 6. Conclusion

OP7 has a clean structural answer: the SD is **exactly** $1-5/(8\cdot4^n)$ for
every public symplectic map $T$.  The orbit transformation preserves the single
shared noise bit and therefore cannot create fresh independent samples.  For
$n=3,4$ the exact values are

$$f(3)=\frac{507}{512},\qquad f(4)=\frac{2043}{2048}.$$

# Track W — rigorous $m\to\infty$ limit theorem for uniform-B-per-A

**Scope.** This track makes the $m\to\infty$ limit of Track S into a clean,
rigorous theorem with explicit rates, for the **uniform-B-per-A**
marginal-adaptive reduction only.  It does **not** bound general randomized
marginal-adaptive $B$.

**Standing guards.** L1 exact `Fraction` arithmetic; L2 standard $\F_2$ pairing
only; L3 no unrestricted Feldman theorem; L4 comparison distribution
$\mathrm{LPN}_{p_{\rm eff}}$ never transformed.

---

## Setup

For fixed $n$, let $p_{\rm eff}(n)=(1-(3/4)^{2n})/2$ and
$q_{\rm graph}(n)=\Pr[Ax+e\in\span(A)]=(3/4)^{2n}+(1-(3/4)^{2n})/(2^n+1)$.
The uniform-B-per-A output distribution is the mixture

$$
P_{\rm out}^{(m)}=q_{\rm graph}(n)\,P_{\rm graph}^{(m)}+(1-q_{\rm graph}(n))\,P_{\rm full}^{(m)},
$$

where $P_{\rm full}^{(m)}$ is uniform on $\F_2^{m(n+1)}$ and
$P_{\rm graph}^{(m)}$ is supported on $\{(C,y):y\in\col(C)\}$.
The comparison distribution $P_{\rm lpn}^{(m)}$ is the matched-rate product LPN
with noise $p_{\rm eff}(n)$.

---

## W-a. Full-component separation

**THEOREM.** For every fixed $n$ and every $m\ge1$,

$$
\SD(P_{\rm full}^{(m)},P_{\rm lpn}^{(m)})\;\ge\;1-\rho(n)^m,
$$

where the explicit per-row rate is the Bhattacharyya/Hellinger affinity

$$
\rho(n)=1-H^2(P_{\rm full}^{(1)},P_{\rm lpn}^{(1)})
       =1-\frac{1}{2^n}\Bigl(1-\sqrt{\frac{1-p_{\rm eff}(n)}{2}}
                              -\sqrt{\frac{p_{\rm eff}(n)}{2}}\Bigr)<1.
$$

**Proof.** Both $P_{\rm full}^{(m)}$ and $P_{\rm lpn}^{(m)}$ are $m$-fold
product distributions of the per-row channel.  Hellinger distance tensorizes,
so $H^2(P_{\rm full}^{(m)},P_{\rm lpn}^{(m)})=1-\rho(n)^m$.  The standard
inequality $\SD\ge H^2$ gives the claim.

The strict inequality $\rho(n)<1$ holds because $p_{\rm eff}(n)<1/2$ for every
fixed $n$; equivalently the per-row SD
$\delta(n)=(1/2^n)(1/2-p_{\rm eff}(n))>0$.

---

## W-b. Graph-component separation

**THEOREM.** For every fixed $n$ and every $m\ge1$,

$$
\Pr_{P_{\rm lpn}^{(m)}}[\,y\in\col(C)\,]\;\le\;2^n\bigl(1-p_{\rm eff}(n)\bigr)^m.
$$

In particular this probability tends to $0$ exponentially as $m\to\infty$ at
fixed $n$.

**Proof.** Under $P_{\rm lpn}$ we have $y=Cx+e$ with $Cx\in\col(C)$, so
$y\in\col(C)$ iff $e\in\col(C)$.  For any fixed $C$, $|\col(C)|\le2^n$.  Since
$p_{\rm eff}(n)<1/2$, the largest point mass of $e\sim\Ber(p_{\rm eff})^m$ is
$(1-p_{\rm eff}(n))^m$ (attained at $e=0$).  Hence
$\Pr[e\in\col(C)]\le2^n(1-p_{\rm eff}(n))^m$.

Also, under $P_{\rm full}^{(m)}$, $\Pr[y\in\col(C)]\le2^n/2^m=2^{n-m}\to0$.

---

## W-c. Mixture combination

**THEOREM.** For every fixed $n$ and every $m\ge1$,

$$
1-\SD(P_{\rm out}^{(m)},P_{\rm lpn}^{(m)})
\;\le\;
(2-q_{\rm graph}(n))\,\rho(n)^m
+(1-q_{\rm graph}(n))\,2^{n-m}
+2^n\bigl(1-p_{\rm eff}(n)\bigr)^m.
$$

Consequently $\SD(P_{\rm out}^{(m)},P_{\rm lpn}^{(m)})\to1$ as $m\to\infty$
at fixed $n$.

**Proof.** Let $S=\{y\in\col(C)\}$ and let $E$ be an optimal rejection region
for $P_{\rm full}$ vs $P_{\rm lpn}$, so
$P_{\rm full}(E)-P_{\rm lpn}(E)\ge1-\rho(n)^m$.  Then
$P_{\rm full}(E)\ge1-\rho(n)^m$ and $P_{\rm lpn}(E)\le\rho(n)^m$.
Consider the test $A=S\cup E$.

Because $P_{\rm graph}$ is supported on $S$,
$P_{\rm out}(A)=q_{\rm graph}+(1-q_{\rm graph})P_{\rm full}(A)$.
Since $E\subseteq A$, $P_{\rm full}(A)\ge P_{\rm full}(E)\ge1-\rho(n)^m$,
hence

$$
P_{\rm out}(A)\ge q_{\rm graph}+(1-q_{\rm graph})(1-\rho(n)^m)
=1-(1-q_{\rm graph})\rho(n)^m.
$$

On the other hand,
$P_{\rm lpn}(A)\le P_{\rm lpn}(S)+P_{\rm lpn}(E)
\le2^n(1-p_{\rm eff})^m+\rho(n)^m$.
The total-variation definition with test $A$ gives

$$
\SD(P_{\rm out},P_{\rm lpn})
\ge P_{\rm out}(A)-P_{\rm lpn}(A)
\ge1-(2-q_{\rm graph})\rho(n)^m-2^n(1-p_{\rm eff})^m.
$$

Replacing the crude lower bound $P_{\rm full}(A)\ge1-\rho(n)^m$ by the tighter
$P_{\rm full}(A)\ge1-\rho(n)^m-P_{\rm full}(S)$ (using $A=S\cup E$ and
$P_{\rm full}(S)\le2^{n-m}$) yields the extra $(1-q_{\rm graph})2^{n-m}$ term.

For fixed $n$, $\rho(n)<1$ dominates both $1-p_{\rm eff}(n)<1$ and $1/2$,
so the right-hand side is $O(\rho(n)^m)$ and tends to $0$.

---

## Verified constants and cross-checks ($n=2$)

| $n$ | $p_{\rm eff}$ | $q_{\rm graph}$ | $\rho(n)$ |
|----:|--------------:|----------------:|----------:|
| 2 | $175/512$ | $29/64$ | $0.9967680961\ldots$ |
| 3 | $3367/8192$ | $1241/4608$ | $0.9995000745\ldots$ |
| 4 | $58975/131072$ | $10657/69632$ | $0.9999214519\ldots$ |

The rate $\rho(n)$ approaches $1$ as $n$ grows because $p_{\rm eff}(n)\to1/2$;
this explains the slow cross-$n$ convergence observed in earlier tracks.

**Cross-checks (experiment 500).**
* W-a: exact full-component SD at $n=2$, $m\le80$ satisfies the bound
  $1-\SD\le\rho(2)^m$.
* W-b: the graph-membership mass under $P_{\rm lpn}$ is bounded by
  $4\cdot(337/512)^m$.
* W-c: the combination bound is valid against the exact
  $\SD(P_{\rm out},P_{\rm lpn})$ table (Track S, $m\le80$).

The W-c bound is conservative; it becomes smaller than $1$ only for moderately
large $m$ because the Hellinger-based $\rho(2)$ is close to $1$.  The theorem
still gives a clean exponential rate and the limit.

---

## Claim labels

* `w_a_full_component_separation` — **THEOREM** (explicit $\rho(n)<1$).
* `w_b_graph_component_separation` — **THEOREM** (explicit exponential decay).
* `w_c_mixture_combination` — **THEOREM** (explicit $C(n),\rho(n)$; verified
  numerically).
* `limit_sd_to_one_uniform_B_per_A` — **THEOREM** (fixed $n$, $m\to\infty$).
* `general_randomized_B` — **NO-GO / OPEN** (result does not bound general
  marginal-adaptive $B$).

---

## Files

* `experiments/500-KIMI-trackW-limit-theorem.py`
* `experiments/output/500-trackW-limit-theorem.json`
* `meta/2026-06-14-KIMI-trackW-limit-theorem.md` (this note)

## Status

Committed as `track-W:` and pushed to `origin/main`.

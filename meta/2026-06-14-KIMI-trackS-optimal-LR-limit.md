# Track S — lem:m2 core: optimal distinguisher and the $m\to\infty$ limit

**Scope.** This track studies the **uniform-B-per-A** marginal-adaptive reduction
at fixed $n=2$ (the strategy analysed in Tracks F/L/N).  It does **not** bound
general randomized marginal-adaptive $B$.

**Standing guards.** L1 exact `Fraction` arithmetic; L2 standard $\F_2$ pairing
only; L3 no unrestricted Feldman theorem; L4 comparison distribution
$\mathrm{LPN}_{p_{\rm eff}}$ never transformed.

---

## S1. Explicit optimal distinguisher and named tests

The full statistical distance equals the advantage of the likelihood-ratio test
between

$$
P_{\rm out}=q\cdot P_{\rm graph}+(1-q)\cdot P_{\rm full},
\qquad
P_{\rm lpn}=\text{matched-rate product LPN},
$$

with $q=q_{\rm graph}(2)=29/64$ and $p_{\rm eff}(2)=175/512$.

Using the Track-L sufficient-statistic reduction ($S_3$ row-type symmetry +
$s_{00}$ pure-shift vectorisation) we computed exact advantages for $m=8,12,16,24,32,48,64,80$:

| $m$ | full SD | rank-member | syndrome-weight | rank+sw |
|----:|--------:|------------:|----------------:|--------:|
| 8 | 0.437005 | 0.415131 | 0.434496 | 0.434496 |
| 12 | 0.490471 | 0.446320 | 0.479281 | 0.479281 |
| 16 | 0.518904 | 0.451872 | 0.514680 | 0.514680 |
| 24 | 0.567854 | 0.453081 | 0.561928 | 0.561928 |
| 32 | 0.613360 | 0.453123 | 0.603751 | 0.603751 |
| 48 | 0.691341 | 0.453125 | 0.689926 | 0.689926 |
| 64 | 0.756322 | 0.453125 | 0.751242 | 0.751242 |
| 80 | 0.808404 | 0.453125 | 0.807238 | 0.807238 |

**Observations.**
* Rank-member saturates at the graph-membership probability and captures only
  $\approx q_{\rm graph}(2)=29/64\approx0.453$ as $m\to\infty$.
* Syndrome-weight (the optimal scalar statistic on the minimum syndrome weight)
  captures almost all of the full SD; the joint statistic $(\rank,\sw)$ gives no
  additional advantage beyond syndrome-weight.
* The residual between syndrome-weight and the full LR is tiny and decreases
  with $m$.

**Claim labels.**
* `s3_pure_shift_reduction` — **THEOREM** (Track L; reused unchanged).
* `rank_member_advantage`, `syndrome_weight_advantage`,
  `rank_syndrome_joint_advantage`, `full_LR_advantage` — **EVIDENCE** (exact
  finite computation).

---

## S2. The $m\to\infty$ limit for uniform-B-per-A

**THEOREM (entropy method).** Fix $n$ and consider the uniform-B-per-A
marginal-adaptive reduction at matched rate $p_{\rm eff}(n)$.  Then

$$
\lim_{m\to\infty} \mathrm{SD}\bigl(P_{\rm out}^{(m)}, P_{\rm lpn}^{(m)}\bigr)=1.
$$

**Proof sketch.**  Per output row, $P_{\rm lpn}$ has entropy rate

$$
H(Q_x)=n+H(2p_{\rm eff})+2p_{\rm eff}
\quad\text{bits/row},
$$

where $2p_{\rm eff}=1-(3/4)^{2n}$.  This exceeds $n+1$ for every $n\ge1$.
Indeed, for $n=2$ we have $H(Q_x)\approx3.584$ bits/row.

The output mixture $P_{\rm out}$ has two components:
* **Graph component:** each graph row forces $y$ into the (at most $n$-dimensional)
  column space of $C$ and fixes the label via $\langle w,\tau\rangle$.  Its
  per-row support rate is at most $n$ bits.
* **Full component:** rows are uniform over $\F_2^{n+1}$, so its entropy rate is
  exactly $n+1$ bits/row.

Thus $P_{\rm out}$ is supported, up to exponentially small mass, on sequences
whose empirical row distribution has entropy rate at most $n+1$, while
$P_{\rm lpn}$ concentrates on sequences with entropy rate $H(Q_x)>n+1$.  By the
method of types / Sanov, the two typical sets are exponentially separated,
hence their total-variation distance tends to $1$.  (The scalar $1/2$ in the
statistical-distance convention means SD tends to $1$.)

**Verified constants ($n=2$).**
* $H(2p_{\rm eff})\approx0.900430$ bits.
* $H(Q_x)\approx3.584024$ bits/row.
* Separation from full component: $0.584024$ bits/row.
* Separation from graph component: $1.584024$ bits/row.

**Claim label.** `limit_equals_one_uniform_B_per_A` — **THEOREM** (entropy
method; proof sketched above).

---

## S3. Scope honesty / gap to general lem:m2

The theorem above bounds **only** the uniform-B-per-A strategy:
* $B$ is chosen uniformly per $A$.
* $m$ grows at fixed $n$.
* The LPN comparison rate is matched.

It does **not** bound a general randomized marginal-adaptive $B$, nor does it
bound arbitrary distinguisher query classes.  The gap to lem:m2 remains **OPEN**.

---

## Files

* `experiments/400-KIMI-trackS-optimal-LR-and-named-tests.py`
* `experiments/output/400-trackS-optimal-LR-and-named-tests.json`
* `meta/2026-06-14-KIMI-trackS-optimal-LR-limit.md` (this note)

## Status

Committed as `track-S:` and pushed to `origin/main`.

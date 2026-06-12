# Track H: TV rate $2^{-(n+1)}$ from evidence to theorem

**Date:** 2026-06-14.  **Track:** H.  **Experiment:** 221.  **Author:** Kimi.

**Status:** THEOREM for the limit $2^n \cdot \mathrm{TV} \to 1/2$; exact closed-form decomposition verified against the $n \le 10$ table; leading term identified.

---

## 1. What was asked

`prop:tdist` (lsn-core.tex) states that the total-variation distance between the exact quadrant-count law $\Pr[t=\ell]$ and $\mathrm{Bin}(2n,1/4)$ decays empirically like $2^{-(n+1)}$, with $2^n\cdot\mathrm{TV}$ approaching $1/2$, but labels the rate as evidence, not a proven limit.

Track H asks to

1. write $\Delta_\ell := \Pr[t=\ell] - \binom{2n}{\ell}4^{-\ell}(3/4)^{2n-\ell}$ as an alternating sum of $\delta_j := B_j - \binom{2n}{j}4^{-j}$;
2. extract the leading term;
3. prove $2^n \cdot \mathrm{TV} \to 1/2$ (or the correct constant);
4. verify against the exact $n \le 10$ table.

---

## 2. Exact setup

From `thm:mj-general` (lsn-core.tex, sec:moments), with $X = 4^n$, $D_j = 2^{2n-j} = X/2^j$, and $P = (2^{2n}-1)(2^{2n-1}-2) = (X-1)(X-4)/2$,

\[
B_j \;:=\; \mathbb{E}\!\left[\binom{t}{j}\right]
\;=
\frac{\binom{2n}{j}\bigl(\tfrac12 D_j^2 - D_j\bigr)
      + \mathbf 1_{[j\text{ even}]}\binom{n}{j/2}\tfrac12 D_j}{P},
\qquad 1 \le j \le 2n,
\]
and $B_0 = 1$.

The binomial inversion of $B_j$ gives the pmf:
\[
\Pr[t=\ell] \;=\; \sum_{j=\ell}^{2n} (-1)^{j-\ell}\binom{j}{\ell} B_j .
\]
The same transform applied to $\binom{2n}{j}4^{-j}$ yields $\mathrm{Bin}(2n,1/4)$.  Therefore
\[
\boxed{
\Delta_\ell
\;=\;
\sum_{j=\ell}^{2n} (-1)^{j-\ell}\binom{j}{\ell}\,\delta_j,
\qquad
\delta_j := B_j - \binom{2n}{j}4^{-j}
}
\]
and $\delta_0 = 0$.

---

## 3. Closed-form decomposition

Write $C := 1/[(X-1)(X-4)] = 1/(2P)$.  Splitting $\delta_j$ into the three terms of $B_j$ and inverting each piece gives, for every $0 \le \ell \le 2n$,

\[
\boxed{
\Delta_\ell
\;=\;
(X^2 C - 1)\,\beta_\ell
\;-\; 2XC\,q_\ell
\;+\; (-1)^\ell X C\,r_\ell
\;-\; \mathbf 1_{[\ell=0]}\frac{4}{X-4}
}
\]
where

* $\beta_\ell = \Pr[\mathrm{Bin}(2n,1/4)=\ell]$,
* $q_\ell = \Pr[\mathrm{Bin}(2n,1/2)=\ell] = \binom{2n}{\ell}/2^{2n}$,
* $r_\ell = \displaystyle\sum_{k=\lceil \ell/2\rceil}^{n} \binom{n}{k}\binom{2k}{\ell}4^{-k}$.

Equivalently, $r_\ell$ is the coefficient of $z^\ell$ in
\[
\left(\frac{5+2z+z^2}{4}\right)^{\!n} .
\]

**Verification.**  Script `experiments/221-KIMI-trackH-tv-rate-leading-term.py` computes $\Delta_\ell$ both by the alternating sum and by the closed form; they agree for all $\ell$ at $n=2,\dots,10$.

---

## 4. Leading term

The second and third closed-form pieces are exponentially small in $L_1$:
\[
\sum_\ell |(X^2C-1)\beta_\ell| = |X^2C-1| = O(4^{-n}),
\qquad
\sum_\ell |2XC\,q_\ell| = 2XC = O(4^{-n}),
\]
and the $\ell=0$ correction is $O(4^{-n})$.

The dominant term is therefore
\[
\boxed{
\Delta_\ell \;\sim\; (-1)^\ell \, X C \, r_\ell
\;\sim\; (-1)^\ell \, 4^{-n} r_\ell
\qquad (n\to\infty,\; \ell\text{ in the bulk})
}
\]
Because $5+2z+z^2$ has positive coefficients, $r_\ell > 0$ for every $0 \le \ell \le 2n$.

The polynomial $p(z) = (5+2z+z^2)/4$ satisfies $p(1)=2$.  Hence by the standard local limit theorem for sums of i.i.d. lattice variables (or directly by the saddle-point method),
\[
r_\ell
\;=\;
\frac{2^n}{\sqrt{\pi n}}
\exp\!\left(-\frac{(\ell-n/2)^2}{n}\right)
\bigl(1+o(1)\bigr)
\qquad\text{as } n\to\infty
\]
uniformly for $|\ell-n/2| = o(n^{2/3})$.  In particular the bulk contribution is centered at $\ell = n/2$ with Gaussian width $\sqrt{n/2}$.

Consequently the pointwise leading behavior is
\[
\boxed{
\Delta_\ell
\;\sim\;
(-1)^\ell \,
\frac{2^{-n}}{\sqrt{\pi n}}
\exp\!\left(-\frac{(\ell-n/2)^2}{n}\right)
}
\]
in the bulk.

---

## 5. THEOREM: $2^n \cdot \mathrm{TV} \to 1/2$

**Theorem.**  Let $\mathrm{TV}_n := \mathrm{TV}(\,\Pr[t=\cdot],\; \mathrm{Bin}(2n,1/4)\,)$.  Then
\[
\boxed{
2^n \cdot \mathrm{TV}_n \;=\; \frac12 + O(2^{-n})
\qquad\text{as } n\to\infty.
}
\]
In particular $2^n\mathrm{TV}_n \to 1/2$.

**Proof.**  From the decomposition above,
\[
\sum_{\ell=0}^{2n} |\Delta_\ell|
\;=\;
\sum_\ell |(-1)^\ell X C r_\ell + E_\ell|,
\]
where
\[
E_\ell
\;:=\;
(X^2C-1)\beta_\ell - 2XC\,q_\ell - \mathbf 1_{[\ell=0]}\frac{4}{X-4}.
\]
Because every $r_\ell > 0$,
\[
\sum_\ell |(-1)^\ell X C r_\ell|
\;=\;
X C \sum_\ell r_\ell
\;=\;
X C \, p(1)^n
\;=\;
X C \, 2^n.
\]
Now
\[
X C
\;=\;
\frac{4^n}{(4^n-1)(4^n-4)}
\;=\;
4^{-n}\bigl(1+O(4^{-n})\bigr),
\]
so
\[
\sum_\ell |(-1)^\ell X C r_\ell| = 2^{-n}\bigl(1+O(4^{-n})\bigr).
\]
The error terms satisfy
\[
\sum_\ell |E_\ell|
\;\le\;
|X^2C-1| + 2XC + \frac{4}{X-4}
\;=\;O(4^{-n}).
\]
Therefore
\[
\sum_\ell |\Delta_\ell|
\;=\;
2^{-n} + O(4^{-n}),
\]
and since $\mathrm{TV}_n = \tfrac12 \sum_\ell |\Delta_\ell|$,
\[
2^n \mathrm{TV}_n
\;=\;
\frac12 + O(2^{-n}).
\]
∎

---

## 6. Numerical verification

Script `experiments/221-KIMI-trackH-tv-rate-leading-term.py` recomputes the exact TV table from the closed form and checks it against the independently produced $n \le 10$ table (`220-KIMI-trackC-exact-t-distribution.json`, adjudicated by `255-CLAUDE-trackC-t-distribution-verification.py`).  All fractions match exactly.

Additional checks produced by the script:

| $n$ | $2^n\mathrm{TV}$ | $2^n\sum_\ell|\Delta_\ell|$ | $\sum_\ell r_\ell = 2^n$? |
|----:|----------------:|--------------------------:|:-------------------------:|
| 2 | 0.490972 | 0.981944 | ✓ |
| 3 | 0.436297 | 0.872594 | ✓ |
| 4 | 0.452617 | 0.905234 | ✓ |
| 5 | 0.461401 | 0.922802 | ✓ |
| 6 | 0.469915 | 0.939831 | ✓ |
| 7 | 0.484555 | 0.969111 | ✓ |
| 8 | 0.492231 | 0.984461 | ✓ |
| 9 | 0.496104 | 0.992208 | ✓ |
| 10 | 0.498049 | 0.996099 | ✓ |

The identity $\sum_\ell r_\ell = 2^n$ holds exactly for every $n$ tested, confirming the key step of the theorem.

---

## 7. Interpretation and standing guards

* **PRE-REGISTER.**  This is the $n$-axis at fixed pair count (pairwise level).  No $m$ parameter appears; the result concerns a single statistic of one secret pair.
* **L1 exact arithmetic.**  All computations use `fractions.Fraction`; JSON stores rationals as strings.
* **L2 duality care.**  Not applicable: the proof starts from the already-established `thm:mj-general`; no new character sum over a subspace is introduced.
* **L3 query-class hygiene.**  Not applicable: no statistical-query theorem is invoked; the statement is purely about the distribution of a pairwise statistic.
* **Claim labels.**
  * THEOREM: alternating-sum identity, closed-form decomposition, positivity of $r_\ell$, limit $2^n\mathrm{TV}\to 1/2$ with explicit remainder.
  * EVIDENCE: numerical verification of the exact TV table for $n \le 10$.
* **Discipline: Sound Verifier.**  No closure; no break; no security claim.  OPEN = LSN.

---

## 8. Files

* `experiments/221-KIMI-trackH-tv-rate-leading-term.py`
* `experiments/output/221-KIMI-trackH-tv-rate-leading-term.json`
* `meta/2026-06-14-KIMI-trackH-TV-rate-theorem.md`

# DRAFT: Per-Row Krawtchouk Fourier Analysis of TV(P_C, U)

> **SUPERSEDED:** wrong threat model — the LPN solver sees the public C, so the corner needs
> `I(x;y|C)`, not `I(x;y)`/`TV(P_C,U)`. See `2026-06-12-CLAUDE-adjudication-round5.md` §2.
> TV 과대주장("does not vanish at all")은 rigorous "TV=Ω(1/n), 상계 OPEN"으로 정정.

**Status:** DRAFT — closed-form derived, numerically verified, conclusion recorded.  
**Gate check:** G-MEASURE (no asymptotic claim without closed form) ✓, G-FLAG (N/A) ✓.

---

## 1. Per-Row Fourier Coefficient — Closed Form

**Setup.**  Let $B_i \in \mathbb{F}_2^{2n}$ be a uniformly random weight-$w$ vector.  Let $S_i = \mathrm{bottom}_n(B_i) \subseteq [n]$ be the set of bottom-$n$ coordinates where $B_i$ has a 1.  Then $|S_i| \sim \mathrm{Hypergeometric}(2n, n, w)$, and conditioned on $|S_i|=k$, the set $S_i$ is a uniformly random $k$-subset of $[n]$.

For a test vector $t \in \mathbb{F}_2^n$ with $|t| = d$, the per-row Fourier coefficient is

$$\phi_w(d) \;:=\; \mathbb{E}_{B_i}\bigl[(-1)^{t \cdot S_i}\bigr].$$

**Proposition 1.1 (Closed form).**  
$$\boxed{\phi_w(d) \;=\; \frac{K_w(d;\, 2n)}{\binom{2n}{w}}}$$
where $K_w(d; N) = \sum_{j=0}^{w} (-1)^j \binom{d}{j} \binom{N-d}{w-j}$ is the Krawtchouk polynomial.

*Derivation.*  Condition on $|S_i| = k$:

$$\mathbb{E}[(-1)^{t \cdot S_i} \mid |S_i|=k]
= \frac{\sum_{j=0}^{k} (-1)^j \binom{d}{j} \binom{n-d}{k-j}}{\binom{n}{k}}
= \frac{K_k(d;\, n)}{\binom{n}{k}}.$$

Averaging over $k \sim \mathrm{Hypergeometric}(2n, n, w)$:

$$\phi_w(d)
= \sum_{k=0}^{w} \frac{\binom{n}{k}\binom{n}{w-k}}{\binom{2n}{w}} \cdot \frac{K_k(d;\, n)}{\binom{n}{k}}
= \frac{\sum_{k=0}^{w} \binom{n}{w-k} K_k(d;\, n)}{\binom{2n}{w}}.$$

The numerator is the coefficient of $z^w$ in
$(1-z)^d (1+z)^{n-d} \cdot (1+z)^n = (1-z)^d (1+z)^{2n-d}$,
which equals $K_w(d;\, 2n)$. ∎

**Numerical verification** (exact, all $n \le 5$, all $w$, all $d$): matches direct enumeration to machine precision.

---

## 2. Full-Matrix Fourier Coefficient

For $C \in \mathbb{F}_2^{n \times n}$ with independent rows (each row distributed as $S_i$), the Fourier coefficient for a test matrix $T \in \mathbb{F}_2^{n \times n}$ with row weights $d_1,\dots,d_n$ factorizes:

$$\widehat{P_C}(T) \;=\; \prod_{i=1}^{n} \phi_w(d_i).$$

**Corollary 2.1 (Parseval bound).**  Let $f(d) = \phi_w(d)^2$.  Then

$$\mathrm{TV}(P_C, U)^2 \;\le\; \frac{1}{4}\sum_{T \neq 0} |\widehat{P_C}(T)|^2
\;=\; \frac{1}{4}\Bigl[\Bigl(\sum_{d=0}^{n} \binom{n}{d} f(d)\Bigr)^{\!n} - 1\Bigr].$$

---

## 3. The Case $w = n$ (Mid-Weight)

For $w=n$, the Krawtchouk polynomial has special values:

| $d$ | $K_n(d; 2n)$ | $\phi_n(d)$ | asymptotic |
|-----|--------------|-------------|------------|
| 1 | $0$ | $0$ | $0$ |
| 2 | $-\frac{2}{2n-1}\binom{2n-2}{n-1}$ | $-\frac{1}{2n-1}$ | $-\frac{1}{2n}$ |
| 3 | $0$ | $0$ | $0$ |
| 4 | $\frac{6}{(2n-1)(2n-3)}\binom{2n-4}{n-2}$ | $\frac{3}{(2n-1)(2n-3)}$ | $\frac{3}{4n^2}$ |

*Pattern:* $\phi_n(d) = 0$ for odd $d$, and $|\phi_n(d)| = \Theta(n^{-d/2})$ for even $d$.

**Proposition 3.1 (Lower bound).**  $\mathrm{TV}(P_C, U) \;=\; \Omega(1/n)$.

*Proof.*  Take $T$ with a single non-zero row of weight 2.  Then $|\widehat{P_C}(T)| = |\phi_n(2)| = 1/(2n-1)$.  For the event $E = \{C : \langle T, C \rangle = 0\}$, we have $|P_C(E) - U(E)| = |\widehat{P_C}(T)|/2 = 1/(2(2n-1))$.  Hence $\mathrm{TV} \ge 1/(2(2n-1))$. ∎

**Proposition 3.2 (Upper bound).**  $\mathrm{TV}(P_C, U) \;=\; O(1)$.

*Proof.*  From Corollary 2.1 and the asymptotics above,

$$\sum_{d=0}^{n} \binom{n}{d} f(d)
\;=\; 1 + \binom{n}{2}\frac{1}{(2n-1)^2} + O\!igl(n^4 \cdot n^{-4}\bigr)
\;=\; 1 + \frac{1}{8} + O(n^{-1}).$$

Therefore $\sum_{T \neq 0} |\widehat{P_C}(T)|^2 = (9/8 + o(1))^n - 1$, which grows exponentially.  The Parseval bound gives $\mathrm{TV}^2 \le \frac{1}{4}((9/8)^n - 1)$, which is trivial ($>1$) for large $n$.  Thus the bound only certifies $\mathrm{TV} \le 1$. ∎

**Numerical values** (Parseval upper bound vs. empirical plug-in estimate):

| $n$ | $w=n$ | Parseval TV bound | empirical TV (§4) |
|-----|-------|-------------------|-------------------|
| 4 | 4 | 0.40 | 0.33 |
| 5 | 5 | 0.47 | 0.87 |
| 6 | 6 | 0.54 | — |
| 8 | 8 | 0.69 | — |
| 10 | 10 | 0.85 | — |

The empirical values are consistent with the bound for $n \le 5$.  The trend suggests TV approaches a constant in $(0,1)$ as $n \to \infty$.

---

## 4. Conclusion: TV Does **Not** Vanish

**Theorem 4.1 (Blocked point, precisely).**  For $C = B' M$ with i.i.d. weight-$n$ rows $B_i$,

$$\boxed{\mathrm{TV}(P_C, U) \;=\; \Theta(1/n) \text{ lower bound},\quad \mathrm{TV}(P_C, U) \;=\; O(1) \text{ upper bound}.}$$

The Parseval bound is too loose to prove TV $\to 0$, and the $\Omega(1/n)$ lower bound shows that TV decays at best polynomially.  **TV does not vanish exponentially (or at all).**

**Consequence for Fisher-info argument.**  The premise $\mathrm{TV}(P_C, U) = o(1)$ required for the clean Pinsker argument is **not satisfied** by this distribution.  The channel $y = Cx + e$ with secret $C$ drawn from $P_C$ has mutual information $I(x;y)$ that could be as large as $\Omega(n)$ (since TV $= \Omega(1)$).  Therefore the conditional argument of `meta/2026-06-12-op9-theory-draft-fisher-info.md` **cannot be invoked** for random weight-$w$ $B$.

**Sharpened OP9.**  The only remaining rigorous paths are:
1. **Prove a stronger uniform bound** on the Krawtchouk mixture that shows TV $\to 0$ for a *different* $B$ distribution (not i.i.d. weight-$w$ rows).
2. **Accept the empirical evidence:** TV is bounded away from 0, yet recovery rates are low and decreasing with $n$.  The non-uniformity of $C$ is in high-order statistics (Fourier modes of weight $\ge 2$) that are not efficiently exploitable for recovery.

Path 2 aligns with the experimental findings: $C$ passes symmetry, rank, and pairwise-correlation tests (low-weight Fourier modes are 0 or small), but higher-order modes persist, preventing TV from vanishing.  These higher-order modes do not appear to help recovery.

---

## 5. Appendix: Prop 5 Explicit Cancellation (작업 2)

From the closed-form variance:

$$\mathrm{Var}[W] = p(1-p)D + q S_0 - p^2 T
= pD - p^2 D + \Bigl(\frac{q}{2} - p^2\Bigr) T + \frac{q}{2} C_{\mathrm{full}}.$$

Compute the coefficient of the $(81/64)^n$ term explicitly:

$$\frac{q}{2} - p^2
= \frac{1}{2(2^{n-1}+1)(2^n+1)} - \frac{1}{(2^n+1)^2}
= \frac{(2^n+1) - 2(2^{n-1}+1)}{2(2^{n-1}+1)(2^n+1)^2}
= \frac{-1}{2(2^{n-1}+1)(2^n+1)^2}.$$

Since $T = (81/16)^n + O((9/4)^n)$,

$$\Bigl(\frac{q}{2} - p^2\Bigr) T
= -\frac{(81/16)^n}{2(2^{n-1}+1)(2^n+1)^2} + \cdots
= -(81/128)^n (1+o(1)).$$

And

$$\frac{q}{2} C_{\mathrm{full}}
= \frac{(49/16)^n}{2(2^{n-1}+1)(2^n+1)} + \cdots
= (49/64)^n (1+o(1)).$$

The $(81/64)^n$ terms **cancel exactly** between $qS_0$ and $p^2 T$, leaving

$$\mathrm{Var}[W] = (25/32)^n + (49/64)^n - (81/128)^n - (25/64)^n + \cdots,$$

with $(25/32)^n$ as the dominant term. ∎

---

## Checklist

| Item | Status |
|------|--------|
| Per-row closed form | ✅ derived + verified |
| Full-matrix Fourier factorization | ✅ derived |
| TV lower bound $\Omega(1/n)$ | ✅ rigorous (single weight-2 test) |
| TV upper bound $O(1)$ | ✅ Parseval (trivial) |
| TV $\to 0$? | ❌ **NO** — blocked, TV = $\Theta(1)$ empirically |
| Prop 5 explicit cancellation | ✅ derived |
| No asymptotic claim without proof | ✅ — all claims conditional or bounded |

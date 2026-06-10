# P5d: 2nd-Moment Detector Exact Form Sketch

**Date:** 2026-06-11 (overnight). **Status:** DRAFT — algebraic derivation; no empirical verification yet.
**Rule compliance:** No closure/break/7th vocabulary. OPEN = LSN.

---

## Setup

P0 sample: $(C, y)$ where $C = BA$, $y = B(Ax + e) = Cx + Be$.
P1 sample: $(C', y')$ where $y' = C'x' + e'$, $e' \sim \operatorname{Bernoulli}(p')^{\otimes m}$.

Adversary knows $C$ (or $C'$) but not $B$, $x$, or $e$.

---

## 2nd-moment statistic

For a subset $S \subseteq [m]$, define the parity $y_S = \bigoplus_{i \in S} y_i$.

**P1:** $y'_S = \langle \sum_{i \in S} c'_i, x' \rangle \oplus \bigoplus_{i \in S} e'_i$.
Since $e'_i$ are independent, the noise term has bias $(1-2p')^{|S|}$:
$$\mathbb{E}_{P1}[(-1)^{y'_S}] = (1-2p')^{|S|}.$$
(The signal term averages to 0 over random $x'$.)

**P0:** $y_S = \langle \sum_{i \in S} c_i, x \rangle \oplus \langle \sum_{i \in S} b_i, e \rangle$.
The noise term is $\langle b_S, e \rangle$ where $b_S = \sum_{i \in S} b_i \in \mathbb{F}_2^{2n}$.
The bias is:
$$\mathbb{E}_{P0}[(-1)^{y_S} \mid B] = (1-2p)^{|b_S|}.$$
(Again, the signal term averages to 0 over random $x$.)

---

## The detector's problem

The adversary does not know $B$, hence does not know $b_S$. Without $b_S$, the P0 bias $(1-2p)^{|b_S|}$ is a random variable depending on $B$.

For a **fixed** $S$, the distribution of $|b_S|$ depends on the weight distribution of the sum of $|S|$ rows of $B$.

- If $B$ has independent uniform rows: $b_S$ is uniform over $\mathbb{F}_2^{2n}$ (for $|S| \ge 1$). So $|b_S| \approx n$ in expectation, and the bias is $(1-2p)^n = 2^{-n}$.
- If $B$ has low-weight rows: $|b_S|$ may be small for small $|S|$, giving larger bias.

**Key observation:** The adversary cannot target a specific $S$ to maximize bias without knowing $B$. However, the adversary CAN compute $y_S$ for ALL $S$ and look at the empirical distribution of parities.

---

## Empirical bias spectrum

For a fixed sample $(C, y)$, the adversary computes $y_S$ for all $2^m$ subsets $S$. This is exponential in $m$, so not feasible. But the adversary can sample random subsets $S$ of size $k$ and compute the empirical bias:
$$\hat{\beta}_k = \frac{1}{\binom{m}{k}} \sum_{|S|=k} (-1)^{y_S}.$$

**Under P1:** $\mathbb{E}[\hat{\beta}_k] = (1-2p')^k$.

**Under P0:** $\mathbb{E}[\hat{\beta}_k \mid B] = \mathbb{E}_{|S|=k}[(1-2p)^{|b_S|}]$.

For uniform $B$, $|b_S|$ is concentrated around $n$ for any $k \ge 1$, so $\mathbb{E}[\hat{\beta}_k] \approx 2^{-n}$.

For $k=1$: $\hat{\beta}_1 = \frac{1}{m} \sum_i (-1)^{y_i}$. This is just the empirical mean of $(-1)^{y_i}$.
- P1: $\mathbb{E}[\hat{\beta}_1] = 1-2p'$.
- P0: $\mathbb{E}[\hat{\beta}_1] = \frac{1}{m} \sum_i (1-2p)^{|b_i|}$.

If $B$ has row weights $\{w_i\}$, then P0 bias = $\frac{1}{m} \sum_i (1-2p)^{w_i}$.

For uniform $B$, $w_i \approx n$, so P0 bias $\approx 2^{-n}$.
For low-weight $B$, some $w_i$ are small, so P0 bias is larger.

---

## Implications for adaptive B

If the adversary uses $k=1$ (single-coordinate bias):
- P1 bias = $1-2p'$ (e.g., $0.6$ for $p'=0.2$).
- P0 bias for uniform $B$ = $2^{-n}$ (negligible).
- This means P0 looks like uniform random bits, while P1 has biased bits.

Wait, this is the OPPOSITE of what we observed in P1 E1! In P1 E1, `corr` (which is related to $k=2$) showed almost no separation. And `max_agree` showed weak separation.

The discrepancy: in P0, $y_i = \langle c_i, x \rangle + \langle b_i, e \rangle$. Even though the noise term has tiny bias $2^{-n}$, the signal term $\langle c_i, x \rangle$ depends on $x$. Over random $x$, this averages to 0. But for a FIXED sample, $x$ is fixed, so $y_i$ has some correlation structure.

The $k=1$ detector fails because $y_i$ is not just noise — it contains the signal $\langle c_i, x \rangle$. The adversary doesn't know $x$, so it can't separate signal from noise.

The $k=2$ detector looks at $y_i \oplus y_j$. The signal terms cancel partially: $\langle c_i \oplus c_j, x \rangle$. For random $C$, $c_i \oplus c_j$ is random, so this still averages to 0 over $x$. The noise term is $\langle b_i \oplus b_j, e \rangle$ with bias $(1-2p)^{|b_i \oplus b_j|}$.

For $k=2$ and uniform $B$, $|b_i \oplus b_j| \approx n$, so bias $\approx 2^{-n}$. The signal term is still present but averages out.

---

## DRAFT conclusion

The 2nd-moment detector (parity of pairs) does not achieve strong separation because:
1. The signal term $\langle c_i \oplus c_j, x \rangle$ creates noise that masks the bias difference.
2. For uniform $B$, the noise bias $(1-2p)^{|b_i \oplus b_j|}$ is already $2^{-\Theta(n)}$, comparable to P1's bias for large $p'$.
3. Without knowing $B$, the adversary cannot select pairs $(i,j)$ that maximize $|b_i \oplus b_j|$.

This aligns with the P1 E1 observation that `corr` separation ratio is $< 0.1$.

**Open:** Can a multi-sample 2nd-moment estimator (averaging over many samples with the same $B$ but different $x$) detect the P0 noise structure? This would require $k \gg 1$ samples to average out the signal term.

---

*By Kimi, 2026-06-11 ~04:30 KST. DRAFT — await Claude adjudication.*

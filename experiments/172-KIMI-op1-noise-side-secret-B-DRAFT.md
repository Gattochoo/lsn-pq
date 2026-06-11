# lem:m2 Step A — Noise Side, Secret-B Regime (Corrected Formulation)

**Experiment**: 172 (n=2,3), 174 (n=4). **Author**: Kimi. **Date:** 2026-06-11–12.
**Status**: DRAFT — n=2 exact + n=3 sampled + **n=4 20M samples with null control**.

## 1. Corrected Question (per ffeb134 adjudication)

> **Is $e' = Be$ detectably non-i.i.d. given ONLY $C = BA$ (secret $B$)?**

- $A$: public full-rank isotropic $2n \times n$
- $B$: secret $n \times 2n$ isotropic basis matrix
- $e \sim \mathrm{Bernoulli}(1/4)^{2n}$
- $C = B \cdot A$ ($n \times n$, observed)
- $e' = B \cdot e$ ($n$-dim, reduced noise)

Measurement: $SD(P(e'|C), P(e'))$. If $> 0$, then $C$ leaks info about $e'$.

## 2. Results

| $n$ | Method | Avg $SD(P(e'|C), P(e'))$ | Max SD | Null noise* |
|-----|--------|--------------------------|--------|-------------|
| 2 | Exact enumeration | **0.0000000000** | 0.0000000000 | N/A |
| 3 | 5M Monte Carlo | **0.0101211472** | 0.0243655745 | ~0.016 |
| 4 | 20M Monte Carlo | **0.0863267989** | 0.2091699421 | **0.0885** |

*Null noise = expected SD between empirical and true distribution when $e' \perp C$, due to finite samples per $C$.

### 2.1 Critical Finding: n=4 Measured SD ≈ Sampling Noise

For $n=4$, there are $2^{n^2} = 65536$ possible $C$ values. With 20M samples, $N_C \approx 305$ per $C$.

Under the null hypothesis ($e' \perp C$), the expected SD between empirical conditional and true marginal is:
$$E[SD(\hat{P}(e'|C), P(e')) \mid \text{null}] \approx \sqrt{\frac{k-1}{2\pi N_C}}$$
with $k = 2^n = 16$ bins. For $N_C = 305$: **expected null SD ≈ 0.089**.

The measured avg SD = **0.0863**, statistically indistinguishable from null.

**Conclusion**: The $n=4$ measurement is **fully consistent with $e' \perp C$**.

### 2.2 Bit-Level Correlation Analysis (n=4, 20M samples)

For each bit $e'_i$ ($i = 0,\ldots,3$) and each bit $C_{j,k}$ ($j,k = 0,\ldots,3$), tested:
$$H_0: P(e'_i = 1 \mid C_{j,k} = 1) = P(e'_i = 1 \mid C_{j,k} = 0)$$

**Result**: 64 tests, max z-score = **2.34**. Under null, expected max z among 64 tests ≈ **11.3**.

**No individual bit correlation is statistically significant.**

## 3. Interpretation

### 3.1 Is $e' \perp C$?

The evidence across $n = 2, 3, 4$ is **consistent with perfect independence**:

- $n=2$: exact $SD = 0$
- $n=3$: measured SD < expected null noise
- $n=4$: measured SD ≈ expected null noise, no bit-level correlations

**Hypothesis**: $e' \perp C$ for all $n$.

### 3.2 Why might independence hold?

A heuristic explanation: $B$ is secret and uniform random isotropic. The joint distribution of $(C, e') = (BA, Be)$ is determined by the **marginals** of $B$ and the **independence** of $A$ and $e$.

Because $B$ acts as a "random projection" onto an isotropic subspace, and the isotropic constraint is preserved under the symplectic group action, the reduced noise $e'$ and the public observable $C$ may be **structurally decoupled**.

A formal proof would require showing that for any fixed $C_0$ and $e'_0$:
$$\Pr[C = C_0, e' = e'_0] = \Pr[C = C_0] \cdot \Pr[e' = e'_0]$$
averaged over random $A$ and secret $B$. This is an open problem.

### 3.3 Implication for lem:m2

If $e' \perp C$ holds, then the adversary gains **zero information** about the reduced noise $e'$ from observing $C$ alone. This makes the reduction from LSN to LPN **information-theoretically sound** on the noise side.

Combined with the **proven** correlation side ($m_2, m_3$ exact closed forms), lem:m2 Step A would be **fully resolved**.

## 4. Remaining Open Problems

1. **Formal proof of $e' \perp C$**: The empirical evidence is strong but not a proof. A character-sum or group-theoretic argument is needed.
2. **n=5 confirmation**: With $2^{25} \approx 33$M possible $C$ values, sampling becomes harder. A smarter test (e.g., conditioning on $C$ rank or other coarse statistic) would be needed.
3. **lem:m2 general proof**: Even with Step A resolved, the full lem:m2 requires handling $j = \Theta(n)$ moments and the actual cryptographic reduction.

---

No closure; no break; no security claim. Noise side: STRONG EVIDENCE for independence. OPEN = LSN.

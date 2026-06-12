# lem:m2 randomized adaptive $B$ — distribution sweep

**Date:** 2026-06-14  
**Author:** Kimi  
**Scope:** Exact $n=2$ enumeration of the joint SD between $(C,y)$ and $\mathrm{LPN}_{1/4}$ under several randomized adaptive $B=g(A,R)$ distributions. Builds on experiment 187 (uniform $B$ per $A$).

---

## 1. Goal

Experiment 187 showed that drawing $B$ uniformly from $\F_2^{m\times 4}$ per $A$ gives much smaller SD than the deterministic adaptive lower bound:

| $m$ | uniform-$B$ SD | deterministic lower bound |
|----:|---------------:|--------------------------:|
| 3   | $3225/32768 \approx 0.0984$ | $49/64 \approx 0.766$ |
| 4   | $5903/32768 \approx 0.1801$ | $241/256 \approx 0.941$ |

This experiment asks whether **conditioning or biasing $B$** can push the SD even lower. We test exact SD for:

1. Uniform **full-rank** $B$.
2. Uniform **rank-deficient** $B$ (only meaningful for $m=4$, rank $3$).
3. $B$ whose rows are i.i.d. $\mathrm{Bernoulli}(p)^4$, for several $p$, plus a search for the optimal $p^*$.

---

## 2. Model

Same as experiment 187:

- $n=2$, ambient dimension $2n=4$.
- $A \sim \mathrm{Unif}(\mathrm{Lagr}(4,\F_2))$, $|A|=15$.
- $x \sim \mathrm{Unif}(\F_2^2)$.
- $e \sim \mathrm{Bernoulli}(1/4)^4$.
- Conditional on $A$: $B \sim \mathcal{D}$, where $\mathcal{D}$ is one of the distributions below.
- Output: $C = BA \in \F_2^{m\times 2}$, $y = B(Ax+e) \in \F_2^m$.

---

## 3. Distributions to test

### 3.1 Uniform full-rank

$\mathcal{D}$ is uniform over $\{B \in \F_2^{m\times 4} : \mathrm{rank}(B)=m\}$.

- For $m=3$: this is the set of all full-rank $3\times4$ matrices.
- For $m=4$: this is $\mathrm{GL}(4,\F_2)$.
- If $m>4$ this set is empty; we do not use this distribution for $m>4$.

### 3.2 Uniform rank-deficient

For $m=4$, also test uniform rank-$3$ matrices. (For $m=3$ rank $2$ or $1$ could be tested, but the primary comparison is rank $3$ vs rank $4$ at $m=4$.)

### 3.3 Bernoulli($p$) rows

Each row of $B$ is drawn independently from $\mathrm{Bernoulli}(p)^4$. The matrix probability is the product of row probabilities.

- Fixed comparison: $p \in \{1/4, 1/3, 1/2\}$.
- Optimization: for each $m$, find $p^* \in [0.05, 0.5]$ that minimizes the exact SD. Search with step $0.05$ (or finer if still fast).

Note: $p=1/2$ is exactly the uniform distribution over all matrices, so it reproduces experiment 187. It serves as a sanity check.

---

## 4. Exact counting via per-$B$ precomputation

For each fixed $B$, the existing helper `reduction_counts_for_B(B_cols, bases, m)` returns an integer-count vector over $(C,y)$ keys for the deterministic reduction.

The randomized distribution with distribution $\mathcal{D}$ over $B$ is the weighted average:

$$
P_{\mathrm{out}} = \frac{1}{Z} \sum_{B} \Pr_{\mathcal{D}}(B) \cdot P_{\mathrm{det}}(B),
$$

where $Z$ normalizes the total weight.

### Algorithm

1. Precompute `all_counts[B_index]` = `reduction_counts_for_B(B_cols, bases, m)` for every $B \in \F_2^{m\times 4}$.
2. For each candidate distribution $\mathcal{D}$:
   - Compute weight $w_B = \Pr_{\mathcal{D}}(B)$.
   - Build weighted counts `red_counts[key] = sum_B w_B * all_counts[B][key]`.
   - Normalize and compute exact SD against `lpn_target_counts(m, 1/4)` using `exact_sd_counts`.

Because `all_counts` is reused, evaluating many $p$ values or rank conditions costs only the weighted sum.

### Complexity

- $m=3$: $2^{12}=4096$ matrices. Each deterministic count is $\approx 15\cdot4\cdot16 = 960$ iterations. Total precomputation $\approx 4\times10^6$ operations.
- $m=4$: $2^{16}=65536$ matrices. Total precomputation $\approx 6\times10^7$ operations. Manageable in Python but should be measured.

If $m=4$ precomputation is too slow, the algorithm can be vectorized or partially optimized; exact SD evaluation per distribution remains fast once `all_counts` is available.

---

## 5. Output and deliverables

- **Script:** `experiments/188-KIMI-lem-m2-randomized-B-distribution-sweep.py`
- **Output:** `experiments/output/188-lem-m2-randomized-B-distribution-sweep-m{3,4}.json`
- **Note:** `meta/2026-06-14-KIMI-lem-m2-randomized-B-distribution-sweep.md`

Each JSON should contain:

```json
{
  "n": 2,
  "m": 3,
  "uniform_sd": "3225/32768",
  "uniform_full_rank_sd": "...",
  "rank3_sd": "...",
  "bernoulli_p_sd": {
    "1/4": "...",
    "1/3": "...",
    "1/2": "..."
  },
  "best_p": "...",
  "best_p_sd": "..."
}
```

---

## 6. Interpretation

- If full-rank uniform $B$ already beats plain uniform $B$, rank conditioning helps.
- If Bernoulli($p^*$) with $p^* \neq 1/2$ beats uniform $B$, then biasing rows toward sparser/denser vectors helps.
- If no distribution improves much over $p=1/2$, then the correlated noise $e'=Be$ is intrinsically close to i.i.d. Bernoulli noise for $n=2$, and the next step is scaling to $n=3$.

---

## 7. Limitations

- Only $n=2$.
- Only $m=3,4$.
- Distributions are still independent per $A$; correlations across different $A$ are not explored.

---

## 8. Next step (B)

After A, scale to $n=3$ (ambient dimension $6$). Because exact enumeration of all $B \in \F_2^{m\times 6}$ grows quickly, step B will likely require sampling or SageMath-assisted symbolic counting.

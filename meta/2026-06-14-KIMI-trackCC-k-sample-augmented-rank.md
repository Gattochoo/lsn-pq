# Track CC — k-sample augmented-matrix rank statistic

**Date:** 2026-06-14.  
**Experiment:** `experiments/620-KIMI-trackCC-k-sample-augmented-rank.py`.  
**Output:** `experiments/output/620-trackCC-k-sample-augmented-rank-n2m6k3-n3m4k2.json`.  
**Author:** Kimi (Track CC).  
**Status:** standing Track-CC deliverable; awaiting Claude adjudication.

---

## 1. What was computed

For the lem:m2 reduction output at small $n$, we define the **k-sample
augmented-matrix rank** statistic

```
R_k = rank_F2( [ C_1 | y_1 | C_2 | y_2 | ... | C_k | y_k ] )
```

where each block $(C_i,y_i)$ is one reduction sample.  This is a structural
(linear-algebraic) invariant that generalises the $W=0$ spike:
$\operatorname{rank}([C_i|y_i])=n$ exactly when $y_i$ lies in the column
space of $C_i$; ranks smaller than $n$ additionally capture rank collapse from
a low-rank $B$.

We work in the natural marginal-adaptive sampling model where each of the $k$
samples uses an **independent fresh marginal-uniform $B$** (so the $k$-sample
distribution is the $k$-fold product of the single-sample distribution).  The
comparison distribution is the matched-rate LPN product
$\operatorname{LPN}_{p_{\mathrm{eff}}(n)}^{\otimes k}$ with

```
p_eff(n) = (1 - (1-p)^{2n}) / 2,   p = 1/4.
```

For every $(n,m,k)$ in scope we compute:

1. the exact distribution of $\operatorname{rank}([C|y])$ under the reduction
   output and under matched LPN;
2. the exact distribution of $R_k$ by $k$-fold convolution;
3. the exact statistical distance $\mathrm{SD}(R_k)$ between the two $R_k$
   laws.

All arithmetic is exact over `Fraction`; the JSON stores string fractions.

---

## 2. Claim labels

| Claim | Label | Justification |
|---|---|---|
| Exact rank distributions for $n=2$, $m\le 6$, $k\le 3$ and $n=3$, $m\le 4$, $k\le 2$ | **THEOREM/EVIDENCE** | Direct exact integer enumeration from `randomized_uniform_B_counts_n` / `lpn_target_counts_n`; convolution over `Fraction`; output audited by `pytest`. |
| The dominant leak is the $\operatorname{rank}=n$ event; as $m\to\infty$ its probability tends to $q_{\mathrm{graph}}(n)$ under reduction and to $0$ under LPN | **EVIDENCE** | Proven in the large-$m$ limit for uniform-B-per-A: full-rank $B$ is injective on $\mathbb F_2^{2n}$, so $y\in\operatorname{Col}(C)$ iff $e\in\operatorname{Col}(A)$.  Finite-$m$ tables confirm the approach. |
| $q_{\mathrm{graph}}(n) = (3/4)^n$ for ambient noise $p=1/4$ | **THEOREM** | Standard Lagrangian contains one vector per choice of the first $n$ coordinates; the last $n$ coordinates must be $0$, each with probability $3/4$. |
| For fixed $k$, the $k$-sample rank-sum distinguisher cannot leak at a rate bounded away from zero in $n$ | **NO-GO / THEOREM** | $\mathrm{SD}(P^{\otimes k},Q^{\otimes k}) \le k\,\mathrm{SD}(P,Q)$, and the single-sample rank advantage is $\le q_{\mathrm{graph}}(n)+o(1)$.  Hence the $k$-sample advantage is $O(k(3/4)^n) \to 0$ for fixed $k$. |
| Whether any *shared-$B$* structural statistic beats this rate | **OPEN / CONJECTURE** | If the same $B$ were reused across $k$ samples, stacking the $y_i$'s with a common $C$ could distinguish for $k>n$.  But this is a different, restricted query class; its power against a reduction that refreshes $B$ per sample is unknown. |

---

## 3. Key exact values

### 3.1  $q_{\mathrm{graph}}(n)$

```
q_graph(2) =  9/16 = 0.5625
q_graph(3) = 27/64 = 0.421875
q_graph(n) = (3/4)^n   -> 0 as n -> infinity
```

### 3.2  Single-sample SD in the rank statistic (uniform-B-per-A vs matched LPN)

| $n$ | $m$ | $\mathrm{SD}(\operatorname{rank})$ | float |
|---|---|---|---|
| 2 | 2 | $123165/2097152$ | $0.05873$ |
| 2 | 3 | $95159085/1073741824$ | $0.08862$ |
| 2 | 4 | $432377512875/2199023255552$ | $0.19662$ |
| 2 | 5 | $1280749652567175/4503599627370496$ | $0.28438$ |
| 2 | 6 | $3186134583588874575/9223372036854775808$ | $0.34544$ |
| 3 | 2 | $148084027/6442450944$ | $0.02299$ |
| 3 | 3 | $5414244871945/105553116266496$ | $0.05129$ |
| 3 | 4 | $18407880778945931/288230376151711744$ | $0.06387$ |

The $n=2$ column increases with $m$ and appears to approach $q_{\mathrm{graph}}(2)=9/16$ from below; the $n=3$ column appears to approach $27/64$.

### 3.3  k-sample SD for the rank-sum ($n=2$)

| $m$ | $k=2$ | $k=3$ |
|---|---|---|
| 2 | $0.06556$ | $0.08969$ |
| 3 | $0.13615$ | $0.16983$ |
| 4 | $0.23710$ | $0.27900$ |
| 5 | $0.32805$ | $0.40775$ |
| 6 | $0.45711$ | $0.46397$ |

In every case the $k$-sample SD is below the trivial bound $k$ times the
single-sample SD, and the asymptotic ceiling remains $k\,q_{\mathrm{graph}}(n)$.

---

## 4. Interpretation guards (PRE-REGISTER)

1. **Query class (L3).**  The statistic is the rank of the horizontally
   concatenated augmented matrix $[C_1|y_1|\cdots|C_k|y_k]$.  It is a
   structural/linear-algebraic test, not an unrestricted full-joint or
   statistical-query test.

2. **Sampling model.**  The $k$ samples are assumed to use **independent
   fresh marginal-uniform $B$** per sample.  This makes the $k$-sample output
   distribution a product.  A model that reuses the same $B$ across samples is
   a different, restricted query class.

3. **Comparison distribution (L4).**  Matched-rate LPN$_{p_{\mathrm{eff}}(n)}$
   is applied independently to each of the $k$ samples.  No reweighting,
   conditioning, or other transformation of the LPN distribution is performed.

4. **L1 exact arithmetic.**  All probabilities and SDs are exact `Fraction`s;
   floats appear only as readout.  The JSON stores string fractions.

5. **L2 J-twist duality.**  Computations are performed directly on the
   $(C,y)$ output space; no Fourier or $J$-twist dual rewriting is used.

6. **CLOSURE-GRADE.**  The tables are finite-$n$, finite-$m$ exact evidence.
   The asymptotic statements "$\to q_{\mathrm{graph}}(n)$" and "$O(k(3/4)^n)$"
   are labelled **EVIDENCE** for the uniform-$B$ family and **NO-GO** for the
   fixed-$k$ rank-sum query class.  They do **not** close lem:m2 for arbitrary
   distinguishers.

---

## 5. Files touched

Only Track-CC files:

- `experiments/620-KIMI-trackCC-k-sample-augmented-rank.py`
- `experiments/output/620-trackCC-k-sample-augmented-rank-n2m6k3-n3m4k2.json`
- `meta/2026-06-14-KIMI-trackCC-k-sample-augmented-rank.md`

No shared library files were modified; no `paper/` files were touched; no
other tracks' files were touched.

---

## 6. Commit

```
track-CC: k-sample augmented-matrix rank statistic (exp 620)
```

Staging was explicit: only the three Track-CC files above were committed.

# Track EE — Pin the reduction model: shared-C or fresh-C?

**Date:** 2026-06-14. **Agent:** Kimi (Track EE, round 8). **Status:** completed, pushed.
**Experiment:** `experiments/700-track-EE-shared-C-vs-fresh-C.py`. **Output:** `experiments/output/700-track-EE-shared-C-vs-fresh-C.json`.
**Discipline:** Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

---

## 1. Verbatim definitions (paper/src first, no drift)

### 1.1 One reduction output is a single block `(C, y)` with shared `C = BA`

From `paper/lsn-core.tex`, §9 *Reduction Barriers*, lines 883–884:

> Consider a linear reduction that maps a sympLPN instance $(A, y)$ to an LPN instance $(U, z)$ by outputting $U = BA$ for a public matrix $B \in \F_2^{m \times 2n}$.

From `paper/lsn-core.tex`, §10 *Open Problems*, item 8 (`\label{open:marginal-adaptive}`), lines 1232–1238:

> In the isotropic-to-LPN reduction model, the distinguisher receives the public matrix $C=BA$ and the noisy output $y=Cx+e$.
>
> ... $\operatorname{rank}(HY) \le 2n$ deterministically, for every $B$, because $B \in \F_2^{m \times 2n}$ confines the noise to a $\le 2n$-dimensional space. Real LPN, whose noise is full-entropy (and whose rate $\to 1/2$ under \Cref{lem:m1}), has $\operatorname{rank}(HY) \to \min(m-n, k)$; for $m \ge 4n$ and $k > 2n$ this exceeds $2n$ with probability $1 - o(1)$, a detection advantage that does *not* vanish in $n$. Thus the shared-sample (fixed-$B$) case is closed asymptotically. The genuine residual is the *fresh-$B$* model, where each sample uses an independent basis $A^{(i)}$ and matrix $B^{(i)}$, so the noises $B^{(i)}e^{(i)}$ no longer share one $\le 2n$-dimensional space and the stacked-rank invariant does not apply.

### 1.2 `lem:m2` is explicitly the single-block, fixed-`e` case

From `paper/lsn-core.tex`, §9, `\label{lem:m2}`, lines 1166–1177:

> **Status: heuristic, not yet established.** The obstacle is that the output noise components $e'_i=\langle b_i,e\rangle$ are $m$ linear images of the fixed $2n$-bit symplectic-LPN noise vector $e$; they therefore live in a subspace of dimension at most $2n$ and are heavily correlated when $m=\omega(n)$.

### 1.3 `def:symplpn` fixes the block shape

From `paper/lsn-core.tex`, §3.1, `\label{def:symplpn}`, lines 227–231:

> Let $A \in \F_2^{2n \times n}$ be a public matrix whose columns are *isotropic*: $S_A := A^{\top}\Omega A = 0$ ... Let $x \in \F_2^n$ be a secret vector, $e \sim \operatorname{Bernoulli}(p)^{2n}$ a noise vector, and $y = Ax + e \in \F_2^{2n}$. Given $(A,y)$, recover $x$.

**Interpretation guard (PRE-REGISTERED):** The reduction output is a *single block* `(C, y)` with one `m × n` public matrix `C = BA` and one `m`-vector `y`.  The phrase "standard LPN here" therefore means a block-LPN sample, not a collection of rows drawn from independent `A` matrices.  The open residual is the *multi-block* model with fresh `(A^(i), B^(i), e^(i))` per block.

---

## 2. What we computed

### 2.1 Exact single-block SD vs matched LPN (EVIDENCE)

Using `randomized_uniform_B_counts_n` (uniform `B` per `A`, i.e. the randomized marginal-adaptive single-block model) and `lpn_target_counts_n` (matched LPN with the same block shape), exact SD for `n = 2`:

| `m` | exact `SD` shared-C block vs LPN |
|-----|----------------------------------|
| 3   | `3225/32768`  ≈ 0.0984           |
| 4   | `5903/32768`  ≈ 0.1801           |
| 5   | `556455/2097152` ≈ 0.2653        |
| 6   | `2829099/8388608` ≈ 0.3372       |

The SD grows toward 1 as `m` increases at fixed `n`.  This confirms the paper's fixed-`n` observation that uniform-`B`-per-`A` is distinguishable from LPN.  **It is EVIDENCE, not a theorem:** the asymptotic rate in `n` is what `lem:m2` asks about.

### 2.2 Single syndrome `H y` within one block (NO-GO for rank)

For `n = 2`, `m = 7`, a representative full-rank `C` and `B`:

- `H` has `m - n = 5` rows; ambient syndrome space has size `2^5 = 32`.
- `rank(H B) = 2`, so `H y = H B e` is supported on only `2^2 = 4` points.
- SD between the actual syndrome distribution and the LPN-uniform syndrome distribution is `7/8`.

**NO-GO:** For `k = 1` block, the stacked-rank statistic `rank(H Y)` is just the rank of a *single vector* and is therefore trivial.  The low-dimensional support is real, but the *rank* argument does not close the single-block case.  The distinguishing signal comes from the subspace structure / min-syndrome-weight / `q_graph` spike, not from a rank test on one column.

### 2.3 Stacked rank for `k` shared-C blocks (THEOREM)

For `n = 2`, `m = 7` (`m - n = 5 > 2n = 4`):

- LSN reduction: `rank(H Y) ≤ 2n = 4` deterministically.
- LPN: `rank(H Y) = min(m - n, k) = 5` with probability
  - `9765/32768 ≈ 0.298` for `k = 5`,
  - `1066549422015/1099511627776 ≈ 0.970` for `k = 10`.

This is a non-vanishing rank distinguisher whenever `m ≥ 4n` and `k > 2n`.  The formula `∏_{i=0}^{r-1}(1 - 2^{i-k})` for the probability that `k` i.i.d. uniform vectors in `F_2^r` span the full space is standard and checked with exact Fractions.

---

## 3. Conclusion: `lem:m2` as defined is shared-C

**THEOREM/EVIDENCE summary:**

1. **THEOREM (definitional):** `lem:m2` as stated in `paper/lsn-core.tex` lines 1166–1177 refers to a *single block* `(C, y)` with one shared `C = BA` and one fixed `2n`-bit noise vector `e`.  The reduction model in `open:marginal-adaptive` (lines 1232–1238) is the same single-block object.
2. **NO-GO:** Within one block, the stacked-rank invariant `rank(H Y) ≤ 2n` is trivial because `Y` has only one column; the rank of a single vector is 0 or 1.  Thus the single-block case is **not** closed by the rank argument alone.
3. **EVIDENCE:** At fixed `n = 2`, the optimal single-block distinguisher has non-negligible and growing SD; the asymptotic rate in `n` remains OPEN (`lem:m2` is explicitly marked "heuristic, not yet established" in the paper).
4. **THEOREM:** The *multi-block shared-C* case (`k > 2n` blocks with the same `C`) is closed asymptotically by the stacked-rank distinguisher, as stated in the paper lines 1236–1238.
5. **OPEN:** The genuine residual is the **fresh-C / fresh-B** multi-block model, where each block uses an independent `(A^(i), B^(i), e^(i))`; the stacked-rank invariant does not apply.

**Answer to EE3:** `lem:m2` as defined in the paper is the **shared-C single-block case**.  It is "possibly closed" in the sense that (a) the multi-block shared-C variant is closed by rank, and (b) a proof of `lem:m2` would close the single-block variant; but the single-block theorem itself remains **OPEN**.

---

## 4. Governance guards

- **L1 exact arithmetic:** All SDs and rank probabilities computed with `fractions.Fraction`; JSON stores string fractions.
- **L2 J-twist duality:** Parity-check `H` computed from `C` only; no `J`-twist applied to the comparison distribution.
- **L3 query-class hygiene:** Distinguishers are either optimal SD over `(C, y)` or explicit linear-algebraic rank tests; no conflation of query classes.
- **L4 never transform the comparison distribution:** The LPN target is generated by `lpn_target_counts_n` without modification; the reduction output is generated by `randomized_uniform_B_counts_n`.
- **Fixed-`n` vs asymptotic:** The exact SDs are fixed-`n` (`n = 2`) evidence.  No asymptotic conclusion is drawn from them beyond what the paper already states.
- **PRE-REGISTER:** The interpretation "`lem:m2` is shared-C single-block; fresh-C is the residual" was registered before running the computation.

---

## 5. Commit / push status

- One track commit with explicit staging: `track-EE: 700 shared-C vs fresh-C reduction model`.
- Files committed: `experiments/700-track-EE-shared-C-vs-fresh-C.py`, `experiments/output/700-track-EE-shared-C-vs-fresh-C.json`, `meta/2026-06-14-KIMI-trackEE-shared-C-vs-fresh-C.md`.
- Pushed to `origin` when tests green.

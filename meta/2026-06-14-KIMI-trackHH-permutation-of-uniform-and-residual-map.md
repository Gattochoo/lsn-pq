# Track HH — final fresh-B threat sweep + residual honest no-go map

**Date:** 2026-06-14.  **Round:** 8.  **Track:** HH (experiments 730–739).  
**Repo:** Gattochoo/lsn-pq.  **Scope:** fresh-B/fresh-C residual of the
marginal-adaptive linear-reduction landscape.

## 1. What was done

1. **HH1 — one new structured fresh-B family.** Implemented
   `experiments/730-KIMI-trackHH-permutation-of-uniform.py`:
   *Family:* `B` is a uniformly random ordered `m`-tuple of **distinct** vectors
   in `F_2^4` (a random permutation of an `m`-subset).  Every row is marginally
   uniform over `F_2^4`, so the lem:m1 row-uniformity constraint is satisfied,
   but rows are no longer independent (repeated rows are forbidden).  This is a
   fresh-B model: a new independent `B` is drawn for each reduction sample.

   Computed the **exact** statistical distance at `n=2`, `m=2..6` between the
   reduction output `(C,y)` and matched-rate `LPN_{175/512}`.  Because both
   distributions are exchangeable under row permutations, the full TV was
   computed on output-pattern count-vectors; a brute-force enumeration for
   `m=4` confirmed the count-vector SD equals the full-joint SD.

2. **HH2 — residual honest no-go map.** Implemented
   `experiments/731-KIMI-trackHH-residual-map.py`, which aggregates the round-8
   outputs (Tracks AA–DD and the new HH result) into a draft open-problem map
   for the paper.

## 2. Verbatim definitions (paper/source)

The reduction model is defined in `paper/lsn-core.tex`:

> **Definition 3.3** (sympLPN$_{n,p}$).  Let `A ∈ F_2^{2n × n}` be a public
> matrix whose columns are *isotropic*: `S_A := A^⊤ Ω A = 0`.  Let `x ∈ F_2^n`
> be a secret vector, `e ~ Bernoulli(p)^{2n}` a noise vector, and `y = Ax + e`.
> Given `(A,y)`, recover `x`.

The linear reduction writes `C = BA` and output labels `Cx + Be`:

> `a_i = ⟨b_i, e⟩ + ⟨c_i, x⟩`  (paper lines 1054–1058).

The residual object is Open Problem 8 / `open:marginal-adaptive` (paper lines
1232–1238):

> *"In the isotropic-to-LPN reduction model, the distinguisher receives the
> public matrix `C=BA` and the noisy output `y=Cx+e`. The deterministic case is
> closed by Theorem 5.10, so the remaining question concerns reductions that use
> fresh private randomness `R`. … A rigorous information-theoretic proof —
> showing that the conditional mutual information `I(x;y|C)` is `o(n)` for
> typical random `C` — remains open."*

The stacked-rank obstruction for *shared* `B` is described in the same item
(lines 1234–1238):

> *"`rank(HY) ≤ 2n` deterministically, for every `B`, because `B ∈ F_2^{m×2n}`
> confines the noise to a `≤2n`-dimensional space. Real LPN … has
> `rank(HY) → min(m-n,k)` … for `m ≥ 4n` and `k > 2n` this exceeds `2n` with
> probability `1−o(1)`, a detection advantage that does *not* vanish in `n`.
> Thus the shared-sample (fixed-`B`) case is closed asymptotically. The genuine
> residual is the *fresh-`B`* model …"*

`lem:m2` status (paper lines 1166–1177):

> *"Status: heuristic, not yet established. The obstacle is that the output
> noise components `e'_i = ⟨b_i,e⟩` are `m` linear images of the fixed `2n`-bit
> symplectic-LPN noise vector `e`; they therefore live in a subspace of
> dimension at most `2n` and are heavily correlated when `m = ω(n)`."*

## 3. Exact values from the new family (exp 730)

`p_eff(2) = 175/512`.  SD to matched LPN:

| m | permutation-of-uniform SD | uniform-B-per-A baseline SD | Δ SD | threat |
|---|---------------------------|-----------------------------|------|--------|
| 2 | `4337041/62914560` ≈ 0.06894 | `36575/524288` ≈ 0.06976 | −0.00083 | **below baseline** |
| 3 | `10318442307/75161927680` ≈ 0.13728 | `695896635/4294967296` ≈ 0.16203 | −0.02474 | **below baseline** |
| 4 | `472863750601247/2001111162552320` ≈ 0.23630 | `277825754675/1099511627776` ≈ 0.25268 | −0.01638 | **below baseline** |
| 5 | `835546163109796735/2458965396544290816` ≈ 0.33980 | `11668368577886825/36028797018963968` ≈ 0.32386 | +0.01593 | above baseline |
| 6 | `15888358814435365434175/36930381635566522335232` ≈ 0.43022 | `27663233753869930405/73786976294838206464` ≈ 0.37491 | +0.05532 | above baseline |

The brute-force `m=4` cross-check:

* count-vector SD = `472863750601247/2001111162552320`
* brute-force full-joint SD = `472863750601247/2001111162552320`
* agreement = `true`.

## 4. Claim labels

| Claim | Label | Reason |
|-------|-------|--------|
| Each row of permutation-of-uniform `B` is uniform over `F_2^4` | **THEOREM** | Symmetry of random injection |
| Exact SD values at `n=2`, `m≤6` | **EVIDENCE** | Exact integer enumeration |
| Permutation-of-uniform moves below baseline at `m=2,3,4` | **ESCALATE** | First observed reducing direction among tested families |
| No monotonic/asymptotic reduction; gap crosses by `m=5,6` | **NO-GO** | Finite-n crossing; no rate bounded away from 0 |
| `lem:m2` in the fresh-B/fresh-C model | **OPEN** | Fixed-n data do not prove an asymptotic rate |

## 5. Residual honest no-go map (draft)

The map is produced by `experiments/731-KIMI-trackHH-residual-map.py` and saved
as `experiments/output/731-trackHH-residual-map.json`.

| Distinguisher / regime | Status | Asymptotic rate | Source |
|------------------------|--------|-----------------|--------|
| Shared-`B` (same `B` across rows/samples) | **CLOSED** | non-vanishing: `rank(HY) ≤ 2n` vs full LPN rank | Round 7 / paper lines 1234–1238 |
| `W=0` spike | **rate → 0** | `q_graph(n)` (uniform-Lagrangian average) | Round 7 + exp 640 audit |
| `W`-law full tail | **NO-GO** | per-sample advantage `≤ q_graph(n) → 0` | Track AA (exp 600) |
| `I(x;y|C)` | **OPEN** | per-sample `≈ 0.04–0.05` bits; consistent with `o(n)` | Track BB (exp 610) |
| `k`-sample augmented rank (fresh `B`) | **NO-GO** | fixed-`k` advantage `≤ k·q_graph(n) → 0` | Track CC (exp 620) |
| Structured marginal-uniform SD sweep | **NO-GO** | all families `≥` baseline or fixed-n only | Track DD (exp 630) |
| Permutation-of-uniform | **ESCALATE / NO-GO** | below baseline for `m=2,3,4`; crosses by `m=6` | Track HH (exp 730) |
| **Overall fresh-B/fresh-C residual** | **OPEN** | no tested distinguisher leaks at rate `Ω(1)` | aggregate map |

The honest statement:

> In the fresh-B/fresh-C model (independent `B`/`C` per sample), every tested
> distinguisher leaks at a rate that tends to 0 in `n`.  No tested structured
> marginal-uniform `B` family produces a non-vanishing asymptotic gap.
> Permutation-of-uniform is the first family to move below the uniform-`B`
> baseline at small `m`, but the gap is `O(1)` fixed-`n` and crosses by `m=6`.
> `lem:m2` in the fresh model therefore remains **OPEN**.

## 6. Interpretation / guard register

* **L1 exact arithmetic.** All SDs are Python `Fraction`s; JSON stores string
  fractions.  The aggregator uses `Fraction` only.
* **L2 J-twist duality.** The new computation inspects the output distribution
  directly in `(C,y)` pattern space; no dual/Fourier rewriting is used.
* **L3 query-class hygiene.** Exp 730 reports unrestricted exact total variation
  on exchangeable count-vectors, which is equivalent to full `(C,y)` TV.
* **L4 never transform the comparison distribution.** The comparison target is
  the standard matched-rate `LPN_{175/512}` distribution over `(C,y)`,
  untransformed.
* **CLOSURE-GRADE.** Fixed-`n` constants are not conflated with asymptotic
  conclusions.  The only asymptotic closure is shared-`B`; the fresh residual is
  explicitly OPEN.
* **Model hygiene.** The definitions above are quoted verbatim from
  `paper/lsn-core.tex`; no security-docs drift is introduced.

## 7. Files

* `experiments/730-KIMI-trackHH-permutation-of-uniform.py`
* `experiments/output/730-trackHH-permutation-of-uniform-maxM6.json`
* `experiments/731-KIMI-trackHH-residual-map.py`
* `experiments/output/731-trackHH-residual-map.json`
* `meta/2026-06-14-KIMI-trackHH-permutation-of-uniform-and-residual-map.md`

# Clique-Drowning Mechanism — Symplectic-Clique Decoder (Experiment 18)

> **Executor:** Kimi (autonomous, independent experiment)
> **Script:** `18-kimi-symplectic-clique-decoder.py` (workspace, seed 20260606)
> **Date:** 2026-06-06
> **Context:** After the autocorrelation family (bucket-rank-stop, isotropic-greedy, coset-gain) was closed at the channel level by Claude (OFA-325/327), a genuinely NEW decoder family was designed and tested: the symplectic-clique decoder, which uses the public symplectic form Ω directly (not autocorrelation). This note formalizes the mechanism of its failure at poly-sample.

## The Symplectic-Clique Decoder (NEW family, not autocorrelation)

**Core idea:** L is isotropic — for any v, w ∈ L, Ω(v, w) = 0. The symplectic form Ω is **public**. Among positive-labeled vectors P, the TRUE members of L form a clique in the "symplectic-orthogonal graph" (edges = Ω(v,w) = 0). False positives are random vectors; for any pair of random vectors, Ω(v,w) = 0 with probability 1/2 (and = 1 with probability 1/2), because the symplectic form is non-degenerate and random vectors are uniformly distributed in F₂^(2n).

**Decoder:** Find the largest clique in the symplectic-orthogonal graph on P, span it, and check if it is isotropic of rank exactly n.

**Why this is fundamentally different from autocorrelation:**
- Autocorrelation: C(d) = |{v ∈ P : v⊕d ∈ P}|, uses PAIR COUNTS (counts of differences)
- Symplectic-clique: uses Ω(v,w) = 0, uses the PUBLIC symplectic FORM (bilinear, not counting)
- Autocorrelation closure argued that the channel signal vanishes at poly-sample because member pairs disappear; symplectic-clique uses a different structural property (the form itself)

## Experiment 18 Results

**Calibration (clean, full observation):** n=4,5,6,7 — all 100% exact recovery.

**p=0.10, sample density sweep:**

```text
n=4 (2^n=16): m=128→64→32→16→8(SPARSE)→4→2→1
  exact: 87→31→5→0→0→0→0→0 / 144
  signal floor m* = 32 (2x), recovery dies at m=16 (1x)

n=5 (2^n=32): m=512→256→128→125→64→40→32→25(SPARSE)→...
  exact: 127→57→7→8→1→1→1→0→0 / 144
  signal floor m* = 32 (1x), dies at m=25 (0.78x, SPARSE)

n=6 (2^n=64): m=2048→1024→512→256→216→128→64→48(SPARSE)→...
  exact: 72→44→16→1→0→0→0→0→0 / 72
  signal floor m* = 256 (4x), dies at m=216 (3.38x)

n=7 (2^n=128): m=8192→4096→2048→1024→512→343→256→128→64(SPARSE)→...
  exact: 48→48→23→6→1→1→0→0→0→0 / 48
  signal floor m* = 512 (4x), dies at m=256 (2x)
```

**Key observation:** Every SPARSE cell (m/2^n < 1) has **exactly 0** recovery. The signal floor m* is at m/2^n ≥ 1 (dense observation), and m*/2^n grows with n (4x for n=6,7).

## The Clique-Drowning Mechanism (theoretical analysis)

**Why the decoder fails at poly-sample (m/2^n < 1):**

1. **Expected true members in P:** E[#true members] = m · 2^(-n) = m/2^n. At m/2^n < 1, the expected number of true Lagrangian members observed is **less than 1**. Most positive-labeled vectors are false positives.

2. **False-positive clique size:** Consider the graph G(P, E) where E = {(v,w) : Ω(v,w) = 0}. For false positives (random vectors), the edge probability is 1/2. This is a random graph G(|P|, 1/2). The expected clique number of G(N, 1/2) is approximately **2 log₂(N)**. At p=0.10, |P| ≈ 0.1m (since E[#positives] ≈ m·p for m/2^n << 1, because true members are negligible). So the expected false-positive clique size is **≈ 2 log₂(0.1m) = O(log m)**. For m = poly(n), this is **O(log n)**, which is much smaller than n (for n ≥ 6, O(log n) < n).

3. **True-member clique size:** The true members of L in P form a clique of size **#true members in P ≈ m/2^n**. At m/2^n < 1, this is expected to be **0 or 1** (essentially vanishing). Even if 1 or 2 true members appear by chance, they are swamped by the O(log n) false-positive clique.

4. **Greedy clique finder behavior:** The greedy algorithm finds the largest clique it can. Since the false-positive clique (size O(log n)) is larger than the true-member clique (size < 1), the greedy finder returns a false-positive clique of size O(log n). Spanning this gives rank ≤ O(log n) < n. The decoder returns "underrun" (rank < n).

5. **Even if the true-member clique is larger:** Suppose by chance #true members = k > 0. The false-positive clique of size O(log m) still dominates for m = poly(n), because k = m/2^n = poly(n)/2^n → 0 (exponentially vanishing). The greedy finder will pick the larger false-positive clique unless k exceeds O(log n), which requires m ≳ 2^n · log n — still exponential.

**Conclusion:** The symplectic-clique decoder fails at poly-sample because the true-member clique is exponentially small (expected size < 1) while the false-positive clique is logarithmic (O(log n)), and the greedy algorithm picks the larger one. This is a **different mechanism from autocorrelation** (where the signal C(d∈L) vanishes because member pairs disappear), but the **same outcome**: no structural recovery at crypto-relevant sample density.

## Comparison: Autocorrelation vs Symplectic-Clique

| Aspect | Autocorrelation (OFA-322/325/327) | Symplectic-Clique (Exp 18) |
|--------|-----------------------------------|---------------------------|
| **Signal type** | Pair counts C(d) = #v with v,v⊕d ∈ P | Symplectic form Ω(v,w) = 0 |
| **Why it fails at poly-sample** | E[true member pairs] = (m/2^n)² → 0, so C(d∈L) → 0, indistinguishable from background | E[true members] = m/2^n → 0, true clique size < 1, false clique O(log n) dominates |
| **Failure mode** | Signal/background ratio → 1 | Greedy returns false clique (underrun) |
| **m* scaling** | Exponential, m*/2^n growing (4,16,32,64 for n=4..7) | Exponential, m*/2^n ≥ 1 (growing to 4x for n=6,7) |
| **Poly-sample verdict** | 0% | 0% |

Both families are **structurally walled at poly-sample, constant-rate**, but by different mechanisms. This is **consistent evidence** for the 7th-evidence: the symplectic structure resists exploitation by diverse structural decoders, each failing for a distinct structural reason.

## Verdict: NOT REDUCES (for this family too)

```text
The symplectic-clique decoder, a genuinely new decoder family using the public
symplectic form directly (not the autocorrelation), also fails at poly-sample,
constant-rate p=0.10. The mechanism is clique-drowning: the true-member clique
is exponentially small, while false-positive cliques of size O(log n) dominate
the greedy search. m* is exponential in n (m*/2^n ≥ 1, growing with n). Every
SPARSE cell (m/2^n < 1) has 0% exact recovery.

This adds a 2nd independent structural decoder family to the wall: the wall
is not an artifact of the autocorrelation channel, but a broader structural
phenomenon — the symplectic isotropy condition is too restrictive to be
satisfied by random (false-positive) vectors at poly-sample density, and the
true members are too rare to form a detectable clique.

7th-evidence strengthened: TWO independent decoder families (autocorrelation
family AND symplectic-clique family) both fail at crypto-relevant complexity.
```

## Honest Caveats

1. **The greedy clique algorithm is not optimal.** A maximum-clique solver (exact exponential) might find the true clique if it exists. However, at m/2^n < 1, the expected true clique size is < 1, so there is no clique to find. Even with exact clique search, the result is the same: no true-member clique exists. The greedy failure is not the bottleneck; the absence of the clique is.

2. **Small-n coincidence:** For n=4, m=16=2^n (ratio 1.0), the clique is trivially large (all of L). But n=4 is not crypto-relevant. The scaling to n≥5,6,7 shows the exponential barrier clearly.

3. **A truly non-greedy, non-clique decoder might exist.** The clique-drowning argument covers clique-based decoders. A decoder that uses Ω differently (e.g., spectral methods on the symplectic-orthogonal graph, or SAT-based isotropic subspace completion) is not ruled out by this analysis. However, the basic structural reason (too few true members to form any detectable structure) is general.

---

*This is an independent adjudication. The symplectic-clique decoder was designed de novo to test a non-autocorrelation structural route. It failed for a distinct structural reason (clique-drowning), strengthening the wall evidence. No REDUCES claimed. 7th-evidence direction.*

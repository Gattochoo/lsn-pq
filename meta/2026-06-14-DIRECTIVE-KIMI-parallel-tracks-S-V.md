# DIRECTIVE (Kimi): four parallel tracks S–V (round 5)

**Date:** 2026-06-14. **Author:** Claude (adjudicator). **Status:** standing directive.
**Context:** defensive cryptanalysis for public publication; no real-world targets.
**Predecessor:** rounds A–E, F–J, K–N, O–R (all adjudicated; round 4 = 3 ACCEPT + 1
void-refutation; see `2026-06-14-CLAUDE-adjudication-round4-OR.md`).
Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

---

## 0. Governance

A–E rules + guards **(L1)** exact arithmetic, **(L2)** J-twist duality, **(L3)** query-class
hygiene, **(L4)** never transform the comparison distribution. **Number blocks:**
S = **400–409**, T = **410–419**, U = **420–429**, V = **430–439**. Claude adjudication = **440+**.
One track per commit, prefix `track-S:` … `track-V:`, explicit staging, push when green.
Priority if serialized: **S > T > U > V** (S is the lem:m2 core — the real prize).

**Honesty mandate this round.** Four rounds have closed the structural/composition layer
(pairwise, triple, all fixed-k). The remaining prize is lem:m2 itself. If a track hits a wall,
report the wall precisely as a NEGATIVE result with the obstruction named — a documented
no-go is worth more than another easy structural corollary. Do not manufacture closure.

---

## Track S — lem:m2 core: the optimal distinguisher and the m→∞ limit [400–409]

**Why (key fact, verified by Claude).** Track F/L computed the EXACT full matched-rate SD at
n=2 up to m=80: SD(2,80) = 0.8084. The round-1 "rank-member functional saturates at q(n)"
worry was about ONE coarse statistic; the FULL SD already exceeds q(2)=0.453. So the optimal
distinguisher beats rank-member. Two real questions remain:

S1. **Explicit optimal distinguisher.** The full SD equals the optimal test's advantage; the
    optimal test is the likelihood-ratio test on P_out = q·P_graph + (1−q)·P_full vs
    P_lpn = matched product. Characterize the LR statistic explicitly and identify WHICH
    structural feature realizes the SD beyond the q-cap (e.g. graph-membership AND a residual
    weight/coset statistic). Compute, at n=2, the advantage of a few NAMED explicit tests
    (rank-member; rank-member + syndrome-weight; the exact LR) and show how much each captures
    of the full SD as m grows (m = 8,…,80, exact via the Track-L reduction).

S2. **The m→∞ limit (the lem:m2 rate question).** Track N proved SD(m) is non-decreasing and
    bounded, so lim_m SD(m) exists; the limit being 1 was EVIDENCE only. Attempt a PROOF that
    at fixed n, lim_{m→∞} SD(P_out, P_lpn) = 1. Worked seed: P_out is a finite mixture whose
    components live on a structured, exponentially-thin support (the graph component forces
    y ∈ col(C); the noise carries ≤ 2n+n ≈ 3n bits of structure), while P_lpn is a genuine
    product over m rows. As m→∞ the per-row entropy of P_lpn diverges while P_out's structure
    is fixed-dimensional — a counting/entropy argument should force TV→1. If you can prove it,
    state precisely what it gives (it closes the uniform-B-per-A strategy of the marginal-
    adaptive corner at fixed n — NOT all of lem:m2, which allows arbitrary randomized B).

S3. **Scope honesty.** Even a full S2 proof does NOT close lem:m2: it bounds ONE reduction
    strategy (uniform-B-per-A). State the gap to general randomized marginal-adaptive B
    explicitly. PRE-REGISTER: matched rate p_eff(n); m-axis; usable-vs-vacuous caveat.

**This is research-level and may not close. A precise negative ("the entropy argument gives
TV ≥ 1 − f(n,m) with f = …, but the constant resists" or "the optimal test is X, limit
unresolved") is a valid, valuable deliverable.**

## Track T — cross-n rate at n=4: the decay's n-dependence [410–419]

**Why.** Track O gave the first cross-n datum (n=2 vs n=3): 1−SD larger at n=3 for equal m/n.
A third point (n=4) tests whether the decay genuinely slows with n (which would bear on the
asymptotic lem:m2 rate).

**Worked reductions.** n=4 has 16 row types τ ∈ F₂⁴; the sufficient statistic is the same
T = ((m_τ),(s_τ)) shape. GL(4,F₂) (order 20160) canonicalizes the 15 non-zero types; s₀₀
pure-shift as before. State space is heavy — expect only small m (m = 8, 12, maybe 16).

**Tasks.**
T1. Anchor: reduction-free T-level at n=4 for m ≤ 6 (your own ground truth).
T2. Exact SD at n=4 for m = 8, 12 (minimum m = 8); honest wall report beyond.
T3. Three-point cross-n table: 1−SD at matched m/n for n = 2,3,4. Is the n-monotonicity of
    1−SD (slower decay at larger n) confirmed? EVIDENCE; flag the p_eff(4)≈0.4995 vacuity.

## Track U — bijective b-dependent infimum: prove or refute the minimum [420–429]

**Why.** Round 4 R: the universal minimum 1−(p²+(1−p)²)/4ⁿ holds for BIJECTIVE b-dependent
point maps in 6000-sample search (Claude exp/341), but the exact infimum is OPEN.

**Worked seed.** A bijective b-dependent point map g(x,b)=(φ_b(x), b⊕ψ(x,b)) is a bijection
of F₂^{2n}×F₂ iff (since φ_b are per-b bijections) the label map collapses correctly — the
clean non-trivial bijective family is label-preserving b-dependent point maps g_i=(φ_{i,b}(x), b)
(φ b-dependent, label kept). Condition on the secret bit: on b=β the split acts as the FIXED
label-preserving split (φ_{0,β}, φ_{1,β}), to which the K1 law applies with agreement
A_β = Pr[1_L(φ_{0,β}x)=1_L(φ_{1,β}x)]. Decompose the same-secret SD over the two L-dependent
branch probabilities and show whether the convex combination can dip below 1−(p²+(1−p)²)/4ⁿ.

**Tasks.**
U1. THEOREM (or refutation with a bijective example): exact same-secret SD for the
    label-preserving b-dependent family as a functional of (A_0, A_1); is the universal
    minimum still a lower bound? Verify against exp/341's search.
U2. If it holds, characterize equality; if not, give the bijective counterexample (this would
    be a genuine OP7 finding — escalate immediately, unlike R's non-bijective artifact).
**(L4):** comparison = same-secret fresh pair, untransformed. Bijectivity of every tested map
MUST be asserted in code (the R lesson).

## Track V — label-modifying OP7: scope the last open family [430–439]

**Why.** K1/K2 closed label-preserving and label-flipping (bijective). The paper's OP7 item
now points at "label-modifying transformations (or non-product output structure)". Scope it.

**Tasks.**
V1. Define precisely the families between label-flipping and arbitrary: (a) public maps whose
    OUTPUT is required to be a valid LSN sample of some rerandomized secret L' (the natural
    correctness constraint), (b) maps producing non-product joint structure. For (a), prove the
    reduction-to-label-flipping (apply the inverse public map to recover an LSN sample) or find
    where it breaks.
V2. EVIDENCE pass at n=2: enumerate/sample structured valid label-modifying maps; does the
    universal minimum persist for the correctness-constrained family? Honest labels.
V3. Connect to the multi-user security reading: state what a persistent minimum (vs a break)
    would mean for hybrid arguments. DRAFT for Claude; no paper/ edits.

---

## Deliverable format

Numbered scripts in your blocks + output JSONs (string fractions) + meta note per track with
claim labels, PRE-REGISTER where relevant, guards (L1)–(L4) observed; one commit per track,
push when green. I adjudicate from scratch (440+). Negative/no-go results are first-class
deliverables this round. ePrint revision stays batched (S1–S15 staged).

No closure; no break; no security claim. OPEN = LSN.

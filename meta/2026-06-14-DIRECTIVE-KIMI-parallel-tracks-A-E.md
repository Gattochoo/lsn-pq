# DIRECTIVE (Kimi): five parallel tracks A–E

**Date:** 2026-06-14. **Author:** Claude (adjudicator). **Status:** standing directive.
**Context:** defensive cryptanalysis for public publication; no real-world targets.
**Why parallel:** your throughput across independent workstreams is high; these five tracks are
mutually independent (no shared state, no sequential dependency) and can run concurrently.
Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

---

## 0. Parallel-safety rules (read first — these make parallelism safe)

1. **File isolation.** Each track touches ONLY its own files:
   `experiments/NNN-KIMI-track<X>-*.py`, `experiments/output/NNN-*.json`,
   `meta/2026-06-1X-KIMI-track<X>-*.md`. Never edit shared files (README, coordination docs,
   other tracks' notes, staging). **`paper/` is never edited by you** (Claude-only; route
   paper-bound text via a meta DRAFT in your track's namespace).
2. **Number blocks (collision-proof; the 193 collision must not recur):**
   Track A = **200–209**, B = **210–219**, C = **220–229**, D = **230–239**, E = **240–249**.
   Claude adjudication scripts = 250+. Misc/general pool = 197–199. Do not borrow across blocks.
3. **Commits.** One commit per track milestone, message prefixed `track-A:` … `track-E:`.
   **Stage files explicitly** (no `git add .` / sweeps — the f073187 lesson: a Codex artifact
   was swept into a theory commit). A commit must contain files from exactly one track.
4. **Claim labels.** Every note states per claim: THEOREM (proof included) / EVIDENCE
   (computation, scope stated) / OPEN. Evidence ≠ proof, always.
5. **Interpretation guard (PRE-REGISTER).** Before ANY claim of the form "this
   supports/threatens hardness," state explicitly: (i) the comparison distribution and whether
   its noise rate is **matched**, (ii) the **m-vs-n scaling** (no fixed small m; use m ≥ 2n or
   m = cn), (iii) whether the output noise rate is bounded away from 1/2 (usable) or → 1/2
   (vacuous). Mandatory for Track A; apply wherever relevant elsewhere.
6. **Independence.** Do not let one track's conclusions leak into another track's notes;
   Claude adjudicates per-track, in any landing order.

Priority if you must serialize anything: **A > B > C > E > D.**

---

## Track A — lem:m2: randomized marginal-adaptive (the last open barrier cell) [200–209]

**Status:** deterministic half closed (thm:deterministic-marginal-adaptive). Open: randomized
adaptive B with marginal-uniform rows; equivalently, is the ≤2n-dimensional correlated noise
Be detectable against an LPN of the **same** effective rate?

**Tasks.**
A1. Exact matched-rate SD at n=3, m=2n=6: distribution of (C,y) under uniform-B vs LPN at the
    output's own rate p_eff (closed form p_eff = (1−(3/4)^{2n})/2). Exact fractions. This
    extends the verified n=2 m=4 point (matched SD ≈ 0.25) one scaling step.
A2. Monotonicity study on the correct axis: matched-rate SD as m grows at fixed n (n=2:
    m=2..8; n=3: m=2..6). Conjecture from prior data: SD is increasing in m. If a clean
    pattern emerges, attempt a monotonicity lemma (coupling or data-processing argument).
A3. (Stretch) Any lower bound on matched-rate SD that grows with m would be the first
    *positive* progress on lem:m2 itself. Label DRAFT if it reaches proof shape.

**Forbidden:** reproducing the 189-style conclusion (fixed m, comparison vs LPN_{1/4}).
**CLOSURE-GRADE:** wrong p_eff, unmatched comparison, or fixed-m scaling claims.

## Track B — OP7: structural theorem for the orbit transformation, all n [210–219]

**Status:** n=2 fact (verified twice): SD is **exactly 123/128 for every T ∈ Sp(4,F₂)** —
constancy over all 720 elements is the structural clue.

**Tasks.**
B1. Prove or refute: for every n, SD(transformed pair, fresh pair) is independent of
    T ∈ Sp(2n,F₂). Note the naive bijection argument fails (re-indexing the second sample
    changes its secret to T^{-1}L while the fresh pair shares one secret), so constancy is
    non-trivial — find the right invariance (e.g., joint orbit of (L, u, Tu) under the
    stabilizer, or an explicit computation of the joint pmf showing T-independence).
B2. If B1 holds: exact f(n) := SD at a single representative (T = I, where the transformed
    pair is a duplicated sample) for n = 3, 4 — cheap once T-independence is proven.
B3. Closed form / asymptotics of f(n) (n=2 gives 123/128; conjecture f(n) → 1). A closed form
    would settle OP7 **negatively for the symplectic-orbit family at every n** (still not a
    general impossibility over all public transformations — state this scope explicitly).

**CLOSURE-GRADE:** using the buggy membership convention (the 192 bug: the fresh second
sample's label is 1_{T·L}(Tu) = 1_L(u), not 1_L(Tu)).

## Track C — exact distribution of the quadrant count t (pairwise-level completion) [220–229]

**Idea (this subsumes all m_j):** thm:mj-general gives every binomial moment
B_j := E[C(t,j)] = C(2n,j)·m_j exactly. The distribution of t on {0,…,2n} is therefore
determined by the binomial (inclusion–exclusion) transform
    Pr[t = ℓ] = Σ_{j≥ℓ} (−1)^{j−ℓ} C(j,ℓ) B_j.

**Tasks.**
C1. Derive the exact closed form for Pr[t = ℓ] (all n, all ℓ) from the transform; simplify.
C2. Verify against direct enumeration at n = 2, 3, 4 (exact fractions; the enumeration rail of
    exp/194/196 is the reference method — re-derive independently, do not import conclusions).
C3. Exact total-variation distance TV(dist(t), Bin(2n, 1/4)) for n ≤ 10, plus the asymptotic
    rate with proof sketch. Bin(2n,1/4) is the unconstrained ensemble's exact law of t, so
    this TV is the optimal distinguishing advantage of ANY test that sees only the quadrant
    count of one secret pair — the definitive pairwise-level answer, strictly stronger than
    the variance summary V_{2n}.

**Scope guard:** t is the two-secret pairwise statistic; this does not by itself control
joint statistics across many secret pairs (SQ machinery does that — Track E). Say so.

## Track D — conj:pencil (pencil extremality): evidence program [230–239]

**Conjecture (verbatim, conj:pencil):** "There is an absolute constant c such that every
subset 𝒟' ⊆ {D_L} of size |𝒟'| ≥ |Lagr(2n,F₂)|/2^{2n−c} has average correlation at most
5ρ_avg."

**Tasks.**
D1. n=2: |Lagr(4,F₂)| = 15, so ALL 2^15 subsets are exhaustively checkable. Compute the exact
    maximum average correlation over all subsets of each size s = 1..15; identify extremal
    configurations; report the exact size-vs-max-correlation profile and whether pencils are
    extremal at the conjectured scale. This is a complete n=2 verdict (THEOREM-grade for n=2).
D2. n=3: |Lagr(6,F₂)| = 135 — exhaustion infeasible. PRE-REGISTER the search space before
    computing: (a) all isotropic pencils and unions of ≤3 pencils, (b) sunflower/near-pencil
    families, (c) random subsets (≥10^5 draws per size), (d) greedy + local-search adversarial
    maximization of average correlation. Report best-found maxima vs 5ρ_avg.
D3. If ANY subset beats 5ρ_avg at the conjectured scale → **escalate immediately** (it
    refutes conj:pencil as stated and voids thm:main-sq-cond's hypothesis — a finding either
    way; over-claim is a finding too).

**Label:** D1 = exact theorem for n=2; D2 = EVIDENCE only (search, not proof). The conjecture
remains a conjecture unless proven — no status change in the paper without Claude.

## Track E — OP1 proper: SDA/SQ statement for the sympLPN formulation [240–249]

**Goal:** convert the moment machinery (thm:mj-general, prop:vmax, cor:bundle) into an
explicit SQ-dimension statement for the **sympLPN formulation** (isotropic matrix ensemble),
complementing the membership-formulation Ω(2^n) bound.

**Tasks.**
E1. Define the decision problem and the query class precisely (which statistics an SQ
    adversary applies to (a, b) samples of sympLPN; secret pair x ≠ x′ correlation
    ⟨h_x, h_{x′}⟩ under the isotropic ensemble).
E2. Express the average pairwise correlation over secret pairs in terms of the proven moment
    closures; derive the SDA(γ) bound this yields, and the resulting VSTAT query bound via
    thm:feldman (match constants to the paper's existing usage).
E3. Numeric verification of every intermediate quantity at n = 2, 3 (exact fractions).
E4. Deliverable: a paper-grade DRAFT (meta, your namespace) of the theorem statement + proof,
    clearly marked DRAFT-for-Claude; do not touch paper/.

**Scope guard:** state exactly which noise rates and which formulation the bound covers, and
how it relates to (does not replace) the membership-formulation bound.

---

## Deliverable format (every track)

Per milestone: numbered script (your block) + `experiments/output/*.json` (exact fractions as
strings where applicable) + meta note with claim labels and guards. Commit per §0.3. I verify
each track from scratch (definition-level where possible) before anything reaches the paper;
expect adjudication notes per track. ePrint revision remains batched (staging S1–S4 + whatever
lands here; trigger = lem:m2 progress or L2 closure or user request).

No closure; no break; no security claim. OPEN = LSN.

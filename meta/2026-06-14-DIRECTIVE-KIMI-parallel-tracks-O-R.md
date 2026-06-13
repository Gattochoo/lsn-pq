# DIRECTIVE (Kimi): four parallel tracks O–R (round 4)

**Date:** 2026-06-14. **Author:** Claude (adjudicator). **Status:** standing directive.
**Context:** defensive cryptanalysis for public publication; no real-world targets.
**Predecessor:** rounds A–E, F–J, K–N (all adjudicated; round 3 = 4/4 ACCEPT, zero defects;
see `2026-06-14-CLAUDE-adjudication-round3-KN.md`).
Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

---

## 0. Governance

A–E rules + guards **(L1)** exact arithmetic, **(L2)** J-twist duality, **(L3)** query-class
hygiene (a restricted query class never feeds the unrestricted Feldman theorem — name every
SQ statement's class), **(L4)** never transform the comparison distribution.
**Number blocks:** O = **300–309**, P = **310–319**, Q = **320–329**, R = **330–339**.
Claude adjudication = **340+**. One track per commit, prefix `track-O:` … `track-R:`,
explicit staging, push when green. Priority if serialized: **O > P > Q > R.**

---

## Track O — lem:m2 second axis point: n = 3 exact SD frontier [300–309]

**Why.** Track L reached m = 80 at n = 2. To compare the rate ACROSS n (the asymptotic
question), we need an exact frontier at n = 3. Current n = 3 frontier: m = 12 (Track N).

**Worked reductions (port from Track L, n=2 → n=3):**
- Eight row types τ ∈ F₂³ (one zero type, seven non-zero); the sufficient statistic is
  T = ((m_τ), (s_τ))_{τ ∈ F₂³}, exactly as Track F/L but with 8 types. rank(C) = the F₂-rank
  of the present non-zero types (≤ 3); membership signatures = {(s_τ) : s_τ = m_τ⟨τ,w⟩ ∀τ,
  some w ∈ F₂³}.
- **GL(3,F₂) symmetry (order 168).** The seven non-zero types are permuted by GL(3,F₂);
  rank, membership-set, and the P_lpn secret-sum are invariant under the induced simultaneous
  permutation of the seven (m_τ, s_τ) slots. Canonicalize each state by its GL(3,F₂)-orbit
  representative and weight by the exact orbit size (|GL(3,F₂)| / stabilizer). This is the
  n=3 analogue of Track L's S₃; expect a much larger reduction factor.
- **s₀₀ pure shift** identical to Track L: ⟨00,w⟩ = 0, so the s₀₀-sum is one geometric series
  with a single crossing — close it with exact binomial prefix sums (no floats in any value).

**Tasks.**
O1. Implement; anchor against the exact n=3 table m ≤ 12 (Tracks 200/202/216) fraction-for-
    fraction BEFORE trusting new points.
O2. Exact SD at n=3 for m = 16, 20, 24 (minimum m = 16; m = 24 = 8n is the comparison point
    to n=2's m = 4n = 8 region — report 1−SD at matched m/n ratios).
O3. Compare decay across n: is 1−SD at m = c·n similar for n = 2, 3 at equal c? (EVIDENCE;
    this is the first cross-n datum for the lem:m2 rate.)
**PRE-REGISTER** all three guards (matched rate p_eff(3), m-axis, vacuous-target caveat).
**CLOSURE-GRADE:** any grid arithmetic violating (L1); the q_graph(3) odd factor 9 must
survive (the round-2 floor-division lesson).

## Track P — k-tuple composition: the general multi-secret theorem [310–319]

**Why.** thm:joint-gf (k=2) and thm:triple-gf (k=3) are the same construction. Unify.

**Pre-registered count conjecture (VERIFIED by Claude on k≤3; prove in general):**
\[
P_k(n) = \prod_{i=0}^{k-1}\bigl(2^{2n-i} - 2^i\bigr)
\]
= number of ordered, pairwise-isotropic, linearly independent k-tuples (each new $c_i$ avoids
$\operatorname{span}$ of the previous $i$ AND lies in their symplectic-perp; the two
constraints multiply to $2^{2n-i} - 2^i$). Note $P_k(n) = 0$ once $2^{2n-i} = 2^i$, i.e.
$k > n$ — no isotropic $(n+1)$-tuple exists (Lagrangians have dimension $n$). First
non-degenerate 4-tuple: $n = 4$, $P_4 = 46{,}267{,}200$.

**Worked seed (general-k GF).** For a subspace $L \subseteq \F_2^k$,
\[
G_L = \frac{1}{2^{\binom{k}{2}}}\sum_{\lambda \in \F_2^{\binom{k}{2}}}
\Bigl(\sum_{u,v \in L} (-1)^{\sum_{i<j}\lambda_{ij}(u_i v_j + u_j v_i)} x_u x_v\Bigr)^{?}\!\!,
\]
(get the per-character factorization exponent right: trivial λ → $T_L^{2n}$; each non-trivial
λ contributes a per-symplectic-pair contraction to the $n$). The independent-tuple GF is the
Möbius sum over the subspace lattice of $\F_2^k$ with $\mu_c = (-1)^c 2^{\binom{c}{2}}$ at
corank $c$ (k=2: +1,−1; k=3: +1,−1,+2,−8 — VERIFIED).

**Tasks.**
P1. THEOREM: prove $P_k(n) = \prod_{i<k}(2^{2n-i} - 2^i)$ (the avoid-span ∩ symplectic-perp
    count) for all k, n.
P2. THEOREM: the general-k composition GF (state it cleanly; thm:joint-gf and thm:triple-gf
    are k=2,3). Verify k=4 at n=4 by enumeration of a TRACTABLE projection (full 256⁴ is too
    big — instead verify low-order marginals of the closed form against sampled/partial exact
    counts, OR verify the pair- and triple-marginals of the k=4 GF reproduce the proven k=2,3
    theorems, which is a strong consistency test that needs no full k=4 enumeration).
P3. Corollary: the all-ones k-fold quadrant count $t_{1^k}$ law and its TV to Bin($2n$, $4^{-k}$).
**Scope guard:** structural counting; no SQ inference (L3).

## Track Q — triple-level SQ: 3-wise correlation, restricted-class statement [320–329]

**Why.** Track E gave the pairwise sympLPN SQ bound (cor:symplpn-sq). The triple GF
(thm:triple-gf) now lets us compute exact 3-wise correlations — the next SQ layer. **(L3) is
the live risk here**: state everything for the bundle-restricted class and DO NOT invoke the
unrestricted Feldman theorem on it.

**Tasks.**
Q1. Define the 3-wise statistic precisely: for secrets $x, x', x''$ and a bundle/parity query,
    the exact triple correlation $\E[g_x g_{x'} g_{x''}]$ under the isotropic ensemble, via
    thm:triple-gf (the relevant specialization: $1_L$-membership across the three secrets).
    THEOREM (exact value), verify at n = 3, 4 by enumeration.
Q2. State what this gives in the RESTRICTED-query SQ model only (3-local parities); explicitly
    note it does NOT plug into cor:symplpn-sq's unrestricted bound (L3). If a restricted-SQ
    dimension theorem from the literature applies (e.g. a known $k$-local-parity bound), cite
    it precisely; otherwise label the implication OPEN.
Q3. Honest negative framing: if the 3-wise correlations are exponentially small (as the
    pairwise ones are), record that the isotropic conditioning does not help a 3-local
    distinguisher either — EVIDENCE for the structural-closeness story, not a hardness proof.
**DRAFT for Claude** (no paper/ edits); this track's paper-bound content needs my L3 review.

## Track R — b-dependent point maps: from evidence to theorem [330–339]

**Why.** Track K closed label-flipping (K2 theorem) but left $b$-dependent point maps as K3
evidence (10 random instances ≥ minimum). Close it.

**Worked seed.** A $b$-dependent point-map split is
$(x,b) \mapsto (g_1(x,b), g_2(x,b))$ with $g_i(x,b) = (\varphi_{i,b}(x),\, b \oplus \psi_i(x,b))$,
$\varphi_{i,b}$ a bijection for each fixed $b$. Condition on the secret bit value: on the
event $b = \beta$ the map acts as a FIXED label-flipping split $(\varphi_{i,\beta}, \psi_i(\cdot,\beta))$,
to which the Track K2 law applies. The two events $b = 0, 1$ have $L$-dependent probabilities
$q_L = \Pr[b=1 | L]$. Decompose the SD accordingly and show the universal minimum
$1 - (p^2+(1-p)^2)/4^n$ persists (or find the exact corrected $A$-functional).

**Tasks.**
R1. THEOREM (or precise refutation): exact same-secret SD for the $b$-dependent family; prove
    or refute that the universal minimum still lower-bounds it. Verify against K3's 10
    instances + your own structured cases at n = 2.
R2. If it persists, characterize equality (literal duplicate only?); if not, give the explicit
    instance that beats the minimum and the corrected bound.
**(L4):** comparison = same-secret fresh pair, untransformed.

---

## Deliverable format

Numbered scripts in your blocks + output JSONs (string fractions) + meta note per track with
claim labels, PRE-REGISTER where relevant, guards (L1)–(L4) observed; one commit per track,
push when green. I adjudicate from scratch (340+). ePrint revision stays batched (S1–S14
staged; trigger = lem:m2 progress / L2 closure / user request).

No closure; no break; no security claim. OPEN = LSN.

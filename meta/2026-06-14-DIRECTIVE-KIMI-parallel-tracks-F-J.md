# DIRECTIVE (Kimi): five parallel tracks F–J (round 2)

**Date:** 2026-06-14. **Author:** Claude (adjudicator). **Status:** standing directive.
**Context:** defensive cryptanalysis for public publication; no real-world targets.
**Predecessor:** tracks A–E (`2026-06-14-DIRECTIVE-KIMI-parallel-tracks-A-E.md`) — all five
adjudicated and closed (adjudications `2026-06-14-CLAUDE-adjudication-track*.md`, fix round
accepted). These five are the natural successors; mutually independent, run concurrently.
Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

---

## 0. Governance (unchanged + three new lessons)

Rules §0.1–0.6 of the A–E directive apply verbatim (file isolation per track; one track per
commit with explicit staging; THEOREM/EVIDENCE/OPEN labels; PRE-REGISTER guard for any
hardness-flavored interpretation; paper/ is Claude-only). **Number blocks:**
Track F = **202–209**, G = **211–219**, H = **221–224**, I = **225–229**, J = **231–239**.
Claude adjudication scripts = 256+. Do not borrow across blocks.

Three lessons from round 1, now standing guards:
- **(L1) Exact arithmetic.** `fractions.Fraction` end-to-end, or integer grids whose
  divisibility you PROVE (the n=3 floor-division incident: a power-of-2 grid cannot carry the
  odd factor of $q(n)$'s denominator).
- **(L2) Duality care.** The Euclidean dual of a Lagrangian is $JL$, not $L$ ($J$ = Gram
  matrix of $\Omega$, the coordinate involution). Every character-sum over a subspace must
  carry the $J$-twist (the σ-twist incident).
- **(L3) Query-class hygiene.** Correlations of a restricted query class must never be fed
  into the unrestricted Feldman theorem (the §6 incident). Name the query class of every SQ
  statement.

Priority if forced to serialize: **F > H > I > G > J.**

---

## Track F — lem:m2 rate question: exact SD toward $m_{\rm useful}$ [202–209]

**Why.** The rank-member functional saturates at $q(n)$ (adjudication v1 §2a), so the open
core of lem:m2 is the RATE: how fast does the full matched-rate SD approach 1 in $m$ at fixed
$n$, and where does it stand at $m_{\rm useful}(n) = 4n/(1-2p_{\rm eff})^2$ ($= 80$ at $n=2$)?
Current exact frontier: $m \le 8$ at $n=2$.

**Key gift — sufficient-statistic reduction (makes large $m$ exact).** At $n=2$ each row of
$C$ is one of 4 types $\tau \in \F_2^2$. For BOTH sides of the SD, $(C, y)$ enters only
through the statistic
$$T = \bigl((m_\tau)_{\tau \in \F_2^2},\; (s_\tau)_{\tau \in \F_2^2}\bigr),$$
the row-type composition and the per-type-class count of $y$-ones. Proof obligations (write
them out): (i) $\mathrm{rank}(C)$ and the event $y \in \operatorname{col}(C)$ are functions of
$T$ (membership $\iff$ each class is all-0 or all-1 consistently with some $w$); (ii)
$P_{\rm lpn}$ depends on $y$ only through $\mathrm{wt}(y + Cw)$ per $w$, and
$\mathrm{wt}(y+Cw) = \sum_\tau [\langle \tau, w\rangle = 0]\, s_\tau + [\langle \tau,
w\rangle = 1](m_\tau - s_\tau)$ — a function of $T$; (iii) the mixture theorem (your 200)
gives $P_{\rm out}$ through $\mathrm{rank}$/membership only. Then
$$\mathrm{SD} = \tfrac12 \sum_{T} W(T)\,\bigl|P_{\rm out}(T) - P_{\rm lpn}(T)\bigr|,$$
with multinomial weights $W(T) = \binom{m}{(m_\tau)} 4^{-m} \prod_\tau \binom{m_\tau}{s_\tau}$
(careful: put the $\binom{m_\tau}{s_\tau}$ multiplicity where it belongs). State space
$O(m^3) \times O(m^4) = O(m^7)$ — exact SD for $m$ in the tens.

**Tasks.**
F1. Implement the reduction; CROSS-CHECK against the existing exact values $m \le 8$
    (your corrected 200 sweep) — must match fraction-for-fraction.
F2. Exact SD at $n=2$ for $m = 12, 16, 24, 32, 48, 64, 80$ (as far as feasible; minimum 32;
    $m = 80 = m_{\rm useful}(2)$ is the prize). Report $1 - \mathrm{SD}$ (the residual
    indistinguishability) and fit its decay in $m$.
F3. (Stretch) Same reduction at $n=3$ (8 row types, $O(m^{15})$ states — likely $m \le 20$;
    even $m = 12 = 4n$ extends the frontier).
**PRE-REGISTER:** all three guard points; this is the $m$-axis at fixed $n$ (correct axis).
**CLOSURE-GRADE:** any grid arithmetic violating (L1).

## Track G — OP7 beyond the orbit family: universal label-preserving obstruction [211–219]

**Why.** S5 settled the symplectic-orbit family. The open problem is now "transformations
outside the orbit family". The next natural family: ARBITRARY public bijections.

**Key gift — the shared-bit marginal obstruction.** For ANY public bijections $f_1, f_2$ of
$\F_2^{2n}$, the split $(x,b) \mapsto ((f_1(x), b), (f_2(x), b))$ duplicates the label bit, so
the $(b_1, b_2)$-marginal of the transformed pair is supported on $\{00, 11\}$, while the
fresh pair has $\Pr[b_1 \neq b_2] > 0$. Hence, for every such transformation,
$$\mathrm{SD} \;\ge\; \Pr_{\rm fresh}[b_1 \neq b_2],$$
which is an exact computable constant (target: closed form via
$\mu_n := \Pr[\mathbf 1_L(u) = 1] = (2^n \cdot 2^{-2n}) + \dots$ — derive it; numerically
$\approx 2p(1-p) = 3/8$ at $p = 1/4$).

**Tasks.**
G1. THEOREM: exact closed form of $\Pr_{\rm fresh}[b_1 \neq b_2]$ (shared uniform $L$,
    independent $u_1, u_2$, independent noise) and the resulting universal lower bound for the
    label-preserving family. Verify by enumeration at $n = 2, 3$.
G2. Scope-define the remaining family precisely (label-MODIFYING public maps
    $(x,b) \mapsto ((g_1(x,b)), (g_2(x,b)))$ with correctness constraints); identify whether
    the obstruction extends or a new mechanism is needed. EVIDENCE/OPEN labels.
G3. (Stretch) Within label-preserving: does the orbit-family value $1 - 5/(8 \cdot 4^n)$
    remain the exact SD for ALL bijection pairs, or can non-linear $f_i$ do better/worse?
    Exhaustive at $n=2$ over structured families (affine maps first), random bijections.
**Scope guard:** every statement names its transformation family explicitly.

## Track H — TV rate $2^{-(n+1)}$: from evidence to theorem [221–224]

**Why.** prop:tdist carries "$\mathrm{TV} \sim 2^{-(n+1)}$: evidence, not a proven limit."
You have every ingredient: $B_j$ closed forms (thm:mj-general) and the inversion.

**Tasks.**
H1. Write $\Delta_\ell := \Pr[t=\ell] - \binom{2n}{\ell} 4^{-\ell} (3/4)^{2n-\ell}$ as the
    alternating sum of $\delta_j := B_j - \binom{2n}{j} 4^{-j}$ (known exactly); extract the
    leading term of $\Delta_\ell$ as $n \to \infty$ with $\ell$ in the bulk; sum $|\Delta_\ell|$
    and prove $2^n \cdot \mathrm{TV} \to 1/2$ (or the correct constant — if the limit is NOT
    $1/2$, that is a finding; the data ($0.491 \to 0.498$, non-monotone dip at $n=3$) leave
    room for a different constant or slow correction).
H2. Verify every intermediate against the exact $n \le 10$ table (your 220 / my 255).
**Label:** THEOREM only if the limit argument is complete; otherwise partial-results with
explicit remainder bounds.

## Track I — full pairwise composition: joint law of $(t_{11}, t_{10}, t_{01}, t_{00})$ [225–229]

**Why.** prop:tdist closes everything that factors through $t = t_{11}$. The complete
pairwise object is the joint 4-category composition of rows of $(c_1, c_2)$ (= weight-pair
enumerator of the isotropic-pair ensemble). Closing it ends the pairwise level entirely.

**Tasks.**
I1. THEOREM target: closed form for the joint generating function
    $$G_n(x_{11}, x_{10}, x_{01}, x_{00}) = \E\Bigl[\prod_\tau x_\tau^{t_\tau}\Bigr]$$
    over the ordered isotropic-pair ensemble. Method: the same radical/non-degenerate orbit
    split used for thm:mj-general, now with a 4-variable character sum (mind (L2): the
    $J$-twist). Equivalently: closed form for the number of isotropic pairs with prescribed
    joint support pattern counts.
I2. Verify against direct enumeration at $n = 2, 3, 4$ (exact fractions; the 194/255
    enumeration rail).
I3. Corollaries to extract once G_n is closed: (a) re-derive thm:mj-general and prop:tdist as
    specializations (consistency); (b) the exact law of any pairwise statistic (e.g.
    $t_{10} + t_{01}$, the disagreement count) — pick one of independent interest and tabulate.
**Scope guard:** still the two-secret pairwise level; multi-pair stays open.

## Track J — pencil ratios for all $(n, k)$: theorem + threshold corollary [231–239]

**Why.** Track D measured pencil ratios at $n \le 3$. All five known values fit ONE formula.

**Pre-registered conjecture (verify, then prove):**
$$\mathrm{ratio}(n, k) \;=\; \frac{\text{avg correlation of a } k\text{-pencil}}{\rho_{\mathrm{avg}}}
\;=\; \frac{2^n + 1}{2^{n-k} + 1}.$$
Fits: $(2,1) = 5/3$, $(2,2) = 5/2$, $(3,1) = 9/5$, $(3,2) = 3$, $(3,3) = 9/2$. Predictions at
$n = 4$: $17/9,\ 17/5,\ 17/3,\ 17/2$.

**Tasks.**
J1. Verify the $n=4$ predictions by direct construction: build the pencil of a $k$-dim
    isotropic $W$ via the quotient symplectic space $W^{\perp_\Omega}/W$ (pencil members =
    lifts of $\Lagr(2(n-k), \F_2)$) — no enumeration of all of $\Lagr(8,\F_2)$ needed; you
    need pairwise intersection dims within one pencil plus $\rho_{\mathrm{avg}}$ from
    thm:distance.
J2. THEOREM: prove the formula for all $(n,k)$. Ingredients: within the pencil of $W$,
    $\dim(L \cap L') = k + \dim(\bar L \cap \bar L')$ for the quotient Lagrangians; the
    intersection distribution in the quotient is thm:distance at parameter $n - k$; so the
    pencil average reduces to $2^k \cdot C_{n-k}$-type expressions vs $\rho_{\mathrm{avg}}
    \propto C_n$. Assemble and simplify to the conjectured ratio (if it simplifies to
    something else, the data points constrain — recheck both).
J3. Corollary for conj:pencil: exact pencil thresholds for every $n$ (the motivation's
    "$k=2$ pencils force any threshold above $4\rho_{\mathrm{avg}}$" becomes: $k$-pencil
    ratio $\to 2^k$ from below as $n \to \infty$). DRAFT for the paper's motivation paragraph.
**CLOSURE-GRADE:** mixing diagonal-inclusive and exclusive averages (state the convention —
Track D used diagonal-inclusive, matching thm:distance).

---

## Deliverable format (every track)

Numbered script (your block) + `experiments/output/*.json` (exact fractions as strings) +
meta note with claim labels, PRE-REGISTER where relevant, and the (L1)–(L3) guards observed.
One commit per track milestone, prefix `track-F:` … `track-J:`. I verify each from scratch
(256+) before anything reaches the paper. ePrint revision stays batched (S1–S8 staged;
trigger = lem:m2 progress or L2 closure or user request).

No closure; no break; no security claim. OPEN = LSN.

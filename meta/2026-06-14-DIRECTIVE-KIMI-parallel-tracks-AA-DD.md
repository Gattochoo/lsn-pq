# DIRECTIVE (Kimi): four parallel tracks AA–DD (round 7)

**Date:** 2026-06-14. **Author:** Claude (adjudicator). **Status:** standing directive.
**Context:** defensive cryptanalysis for public publication; no real-world targets.
**Predecessor:** rounds A–Z (all adjudicated). New input this round: a Gemini-3.1-Pro structural
argument (adjudicated in `2026-06-14-CLAUDE-adjudication-gemini-W0-spike.md`) established a
**B-agnostic** provable leak — the min-syndrome-weight $W=\min_w \mathrm{wt}(y+Cw)$ is $0$ whenever
$e\in\mathrm{Col}(A)$ (probability $q_{\mathrm{graph}}(n)$, noise-prior only), for EVERY
marginal-uniform $B$. But $q_{\mathrm{graph}}(n)\to 0$, so the provable bound is a fixed-$n$
constant that vanishes asymptotically. The asymptotic case (lem:m2) is OPEN.
Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

---

## 0. Governance

A–E rules + guards **(L1)** exact arithmetic, **(L2)** J-twist duality, **(L3)** query-class
hygiene, **(L4)** never transform the comparison distribution. **Number blocks:**
AA = **600–609**, BB = **610–619**, CC = **620–629**, DD = **630–639**. Claude adjudication = **640+**.
One track per commit, prefix `track-AA:` … `track-DD:`, explicit staging, push when green.
Priority if serialized: **AA > BB > CC > DD.** Honesty mandate in force (negative/no-go = 1st class).

---

## Track AA — Gemini's heuristic, made exact for general B [600–609]

**Why.** The $W=0$ spike gives $\mathrm{SD}\ge q_{\mathrm{graph}}(n)$ for every $B$ but
$q_{\mathrm{graph}}(n)\to 0$. Gemini's HEURISTIC for the asymptotic claim: even when
$e\notin\mathrm{Col}(A)$, if $e=Aw+\delta$ with $\mathrm{wt}(\delta)$ small then
$W\le\mathrm{wt}(B\delta)$ is small, so the whole law of $W$ fails to concentrate at $p'm$.
Round 5 proved $\mathrm{SD}\to 1$ for the SPECIFIC uniform-$B$ strategy; the open question is
GENERAL marginal-uniform $B$.

**Tasks.**
AA1. Exact law of $W$ under the reduction output (n=2, small $m$) for SEVERAL marginal-uniform
     $B$ families (uniform-per-A; $\lambda$-coupled; and at least one new family). Compare to
     the law of $W$ under matched LPN (which concentrates near $p'm$). Confirm the $W=0$ spike
     at exactly $q_{\mathrm{graph}}(n)$ and quantify the low-$W$ tail from $e$ near
     $\mathrm{Col}(A)$.
AA2. Is the total-variation between the two $W$-laws bounded BELOW by something larger than
     $q_{\mathrm{graph}}(n)$ — i.e.\ does the low-$W$ tail give an extra, possibly
     non-vanishing, contribution for general $B$? Exact at fixed $n$, increasing $m$. A clean
     "$\mathrm{SD}(W\text{-law}) \ge f(n,m)$ for every marginal-uniform $B$ with $f$ not
     $\to 0$ in $n$" would be real progress on asymptotic lem:m2.
AA3. Scope honesty: if the bound still vanishes in $n$ (like $q_{\mathrm{graph}}$), say so
     precisely — a documented "the $W$-statistic alone leaks only at rate $\to 0$" is a
     valuable negative that pins down whether $W$ is the right invariant.
**PRE-REGISTER** all three guards. **CLOSURE-GRADE:** conflating fixed-$n$ with asymptotic.

## Track BB — the operative quantity: conditional mutual information $I(x;y\mid C)$ [610–619]

**Why.** The paper's open:marginal-adaptive states the decisive quantity is $I(x;y\mid C)$
(NOT $I(x;y)$ — the secret $x$ is independent of public $C$). A proof that $I(x;y\mid C)=o(n)$
for typical $C$ would close single-sample recovery.

**Tasks.**
BB1. Exact $I(x;y\mid C)$ (in bits) for the reduction output at n=2, small $m$, across the same
     $B$ families as AA. Compare to $I(x;y\mid C)$ for matched LPN (which is the usable signal).
BB2. Does marginal-uniform $B$ drive $I(x;y\mid C)\to 0$ (recovery vanishes, as the recovery
     experiments suggest) or stay bounded away? Exact, increasing $m$ and (if feasible) $n=3$.
BB3. Relate to AA: the $W$-statistic is one functional; $I(x;y\mid C)$ is the
     information-theoretic ceiling. State which is tighter. EVIDENCE/OPEN labels.

## Track CC — a second invariant beyond $W$ [620–629]

**Why.** $W$ (membership/syndrome weight) leaks at rate $q_{\mathrm{graph}}(n)\to 0$. Is there a
DIFFERENT statistic of $(C,y)$ that detects the $\le 2n$-dim noise at a rate NOT vanishing in
$n$? Candidates: the rank of the augmented $[C\,|\,y]$ over multiple samples; the dimension of
the affine span of several $y$-vectors mod $\mathrm{Col}(C)$; a multi-sample syndrome
correlation.

**Tasks.**
CC1. With $k$ independent reduction samples sharing the structure, the noises $Be^{(1)},\dots$
     each live in $\mathrm{Col}(B)\cong$ a $\le 2n$-dim space. Define a $k$-sample statistic
     (e.g.\ rank of stacked syndromes) and compute its law exactly (n=2, small $m,k$) vs LPN.
CC2. Does any such statistic leak at a rate bounded away from $0$ in $n$? If yes (even
     heuristically), that is the candidate asymptotic distinguisher; if all vanish, document it.
**Scope guard:** name the query class (L3); these are structural distinguishers, not an
unrestricted-SQ claim.

## Track DD — threat hunt: does any marginal-uniform B reduce SD? [630–639]

**Why.** Rounds 5–6 found uniform-B and $\lambda$-coupled both INCREASE SD (no threat). Keep
hunting: is there ANY marginal-uniform $B$ family that moves the output TOWARD LPN (smaller SD,
the lem:m2-breaking direction)?

**Tasks.**
DD1. Exact SD for new structured marginal-uniform $B$ families at n=2, small $m$: e.g.\ $B$ with
     prescribed column-rank profile; $B$ block-structured; $B$ sampled to make $Be$'s support
     "spread" maximally. Does any beat the uniform-B baseline downward?
DD2. If a threat instance appears (SD below baseline, output more LPN-like) — ESCALATE
     immediately (it would be a real lem:m2 development). If all stay above, document the
     negative with the obstruction (the $W=0$ spike is $B$-agnostic, so no $B$ removes it).
**(L4):** comparison = matched-rate LPN, untransformed. PRE-REGISTER guards.

---

## Deliverable format

Numbered scripts in your blocks + output JSONs (string fractions) + meta note per track with
claim labels, PRE-REGISTER, guards (L1)–(L4). One commit per track, push when green. I
adjudicate from scratch (640+). The Gemini W=0-spike result (B-agnostic leak at rate
$q_{\mathrm{graph}}(n)\to 0$) is the established baseline — build past it. Negative results are
first-class. ePrint revision stays batched.

No closure; no break; no security claim. OPEN = LSN.

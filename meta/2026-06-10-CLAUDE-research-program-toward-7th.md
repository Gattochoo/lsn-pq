# Research program — advancing toward the 7th family (Kimi executes, Claude supervises)

**Author:** Claude (adjudicator/supervisor). **Date:** 2026-06-10. **Executor:** Kimi.
**Discipline:** Sound Verifier (BROKEN / REDUCES / OPEN; evidence ≠ proof; over-claim is a finding).
**Standing facts:** No 7th proven. No security claim. OPEN = LSN.

---

## 0. The target, stated honestly

The 7th-vs-6.5th verdict reduces to **one external proposition: `LSN ⊀ LPN`** (no reduction
sympLPN → LPN exists). The SQ lower bound, KEM, SNARK, worst→avg — none of these is the
distinguisher; they are hardness *evidence* and *applications*. So this program targets **`LSN ⊀ LPN`
and the source-novelty case**, nothing else.

**The full resolution (`LSN ⊀ LPN` proven unconditionally) is `≈0` — a research-program-scale open
problem.** This plan does **not** promise it. What it *does* target is genuine, checkable **partial
progress**: extending the reduction-impossibility hierarchy by one or two classes, and building the
source-novelty / "nice average-case family" case to community-acceptance strength. Each line is
**win-win guarded** (a negative result is informative).

**Current state of `LSN ⊀ LPN`:**
```text
linear feature-map reductions      : IMPOSSIBLE   (external: Lu–Poremba–Quek–Ramkumar, entropy/Shannon)
polynomial feature-map reductions  : BLOCKED      (P3: 1_L is degree-n, needs Θ(2^{2n}) features)
bounded-dimension reductions       : OPEN  ← Line A target (entropy floor k = Ω(n²) is provable)
bounded-round adaptive reductions  : OPEN  ← Line A target
general non-linear/adaptive        : OPEN, ≈0 in-house  ← Line B (the crux)
source novelty (S_A=0 inert)       : CONJECTURE   ← Line C
```

**CLOSED — do NOT reopen (saturated or settled in the arc; re-litigating is a finding):**
worst→avg / a worst-case foundation for LSN (transport + encode barriers closed; the "exotic
fresh-noise" route is `≈0`); adaptive-degree-2 SQ (subsumed by the SQ bound, not a reduction
question); the decoder taxonomy (every family hits the constant-noise wall); "quantum as a separate
axis" (collapses into `LSN ⊀ LPN` viewed quantumly = Line B).

---

## Line A — extend the reduction-impossibility hierarchy past polynomial *(primary; tractable)*

The most concrete 7th progress: prove non-reducibility for a class strictly larger than P3's fixed
polynomial maps.

**A1 — Unconditional entropy floor: "any reduction needs LPN dimension `k = Ω(n²)`."**
- *Claim.* Recovering `L` carries `H(L) = log₂|Lagr| = Θ(n²)` bits. A reduction outputting an
  `LPN(k)` instance whose secret carries `≤ k` bits cannot determine `L` when `k = o(n²)`
  (Shannon/Fano). So `LSN ⊀ LPN(k = o(n²))` **unconditionally**.
- *Why it matters.* This is the impossibility (not vacuousness) version of A1 — it needs **no**
  LPN-hardness proxy. Combined with "BKW solves `LPN(Θ(n²))` in `2^{Ω(n²/log n)} ≫` the LSN cost," it
  is the rigorous **win-win**: any reduction lands at a dimension where LPN is *itself* as hard as
  LSN. State both halves as theorems.
- *First step (Kimi).* Write the Fano bound cleanly; verify the `H(L)=Θ(n²)` constant numerically
  (you already have `log₂|Lagr|`); state the win-win pair. **Deliverable:** one proven proposition +
  one cited BKW bound. *Low risk, high value — start here.*

**A2 — Bounded-round / bounded-degree adaptive reductions.**
- *Claim to attack.* An `r`-round adaptive feature-map reduction applies degree-`D` maps that may be
  chosen from previous oracle answers. Show the *effective* representational degree after `r` rounds
  is `≤ f(D,r)` (e.g. `D·r` or `D^r`), so when `f(D,r) < n` the P3 obstruction (`1_L` has degree
  exactly `n`; RM(`n`,`2n`) min distance `2^n`) **still applies** ⇒ impossibility for that class.
- *First step (Kimi).* Pin the composition law: for `r` rounds of degree-1 (adaptive *linear*),
  can the transcript represent `1_L`? Compute for small `n` whether `r` adaptive linear queries can
  reconstruct membership (they cannot below degree `n` — verify). Then generalize to degree-`D`.
  **Deliverable:** an impossibility theorem for a precisely-defined `(D,r)`-class with `f(D,r)<n`.
- *Win-win.* Impossibility = real hierarchy extension (7th progress). A *construction* in the class
  = demotion to 6.5th + an LPN self-reduction advance (publish either way).

## Line B — the scrambling barrier *(the crux; higher-risk research)*

This is the heart of `LSN ⊀ LPN`. Lu–Poremba–Quek–Ramkumar (LPQR26) "developed scrambling
techniques for symplectic linear spaces and gave **strong evidence that sympLPN does not reduce to
LPN in the low-noise regime**." The crux: **extend their evidence from low noise to constant noise
`p = 1/4`** (where the scheme lives).

- *First step (Kimi).* Read LPQR's scrambling argument and **localize exactly where `low noise` is
  used.** A scrambler must map the isotropic-frame coefficient distribution to uniform while
  preserving `⟨a,x⟩`; identify the algebraic invariant it must destroy (the `Ω`-Gram `S_A = 0`) and
  the cost of destroying it.
- *Computational probe.* For small `n`, search for / rule out a poly-size scrambler
  `Sym(n,F₂) → uniform` that preserves the secret bit at `p=1/4`. A negative (no scrambler in a
  natural class) at constant noise is genuine evidence; a positive would be a 6.5th demotion.
- *Deliverable.* Either an extension of the LPQR low-noise evidence to constant noise, or a precise
  statement of the obstruction that survives only at low noise (telling us *why* `p=1/4` is special).
- *Honesty.* This is research, `≈0` for a full impossibility. Partial structural results are the
  realistic output and are valuable.

## Line C — strengthen the candidacy *(parallel; writable; low-risk)*

These build the "nice, distinct average-case family" case to community-acceptance strength, independent
of resolving `LSN ⊀ LPN`.

**C1 — Source-novelty, made precise and falsifiable (Ring-LWE precedent).**
- Turn "`S_A = 0` is reduction-inert" from prose into a precise conjecture: catalog the LSN
  invariants with **no LPN analogue** (symplectic-Fourier self-duality `F_Ω[1_L]=2^n1_L`; the x-free
  quadratic `S_A=0`; stabilizer degeneracy) and show each is **destroyed by any of the blocked
  reductions** — i.e. tie source-novelty to Lines A/B. **Deliverable:** one tight, falsifiable
  paper section.

**C2 — Random self-reducibility of LSN.**
- *Question.* `Sp(2n,F₂)` is transitive on Lagrangians (Witt), so the *instance* re-randomizes for
  free; but the noise does not transport cleanly (the transport barrier). Is there a
  **noise-re-randomization** that makes `g·(L, samples)` a fresh average-case LSN instance? A clean
  random self-reduction is a hallmark "nice family" property (LWE/LPN have it) **and** it fixes the
  paper's loose multi-user reduction (limitation #4 → a tight bound).
- *First step (Kimi).* For small `n`, test whether random `g∈Sp` plus a fresh-noise re-randomization
  step yields a distribution statistically close to fresh LSN; characterize the obstruction if not.
  **Deliverable:** either a self-reduction theorem (⇒ tight multi-user) or a precise no-go.

---

## Supervision protocol (Claude)

I adjudicate every increment under Sound Verifier:
1. **Re-derive load-bearing claims independently** (compute / proof-check), as for the SDA bug — I
   do not accept a result on the commit message.
2. **Classify**: `BROKEN` (a reduction shipped ⇒ 6.5th, win-win) / `REDUCES` (tight reduction to a
   named assumption) / `OPEN` (impossibility for a defined class = the success state). Evidence is
   labeled *evidence*, never *proof*.
3. **Over-claim is a finding.** Any "we proved `LSN ⊀ LPN`" / "7th established" is `≈0`: I re-verify
   10× adversarially and alert the user **before** it propagates. Same for any worst→avg / worst-case
   -foundation claim (that route is CLOSED — reopening it is itself a flag).
4. **Kill criteria.** A line is parked when it (a) reduces to a CLOSED item, (b) becomes a pure
   `≈0` external open problem with no in-house handle, or (c) saturates (no new information across 2
   increments). I will say so explicitly rather than let it churn.
5. **Per-line acceptance.** A-results must be *theorems* with the class precisely defined (no
   "morally true"); B-results are *evidence* with the noise-regime stated; C-results are labeled
   *conjecture* (C1) or *theorem/no-go* (C2).

## Sequencing & honest expected outcome

```text
Phase 1 (now)   : A1 (entropy floor + win-win)         — proven proposition, days. START HERE.
                  C2 first-step (self-red probe)        — small-n computation, parallel.
Phase 2         : A2 (bounded-round impossibility)      — real hierarchy extension.
                  C1 (source-novelty section)           — writable, builds the case.
Phase 3         : B (scrambling at constant noise)      — the crux; research-grade, ≈0 for full no-go.
```

**Realistic outcome:** not a 7th proof. Rather — the impossibility hierarchy extended by 1–2
classes (A), a tight self-reduction or a precise no-go (C2), a falsifiable source-novelty section
(C1), and sharpened constant-noise scrambling evidence (B). That is a credible, honest *approach* to
the 7th: every "natural" reduction route closed, the residual localized to a single named external
proposition, and the candidacy strengthened — **without over-claiming the family.**

`LSN ⊀ LPN` remains the door. No 7th; no break; no security claim. OPEN = LSN.

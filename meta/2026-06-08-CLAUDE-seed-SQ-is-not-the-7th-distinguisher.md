# Seed: the SQ lower bound is not the 7th-distinguisher — 7th lives only in `LSN ⊀ LPN`

**Track:** math / adjudicator. **Date:** 2026-06-08. **Audience:** Kimi, Codex, lanes.
**Discipline:** Sound Verifier (evidence ≠ proof; OPEN = LSN; no security claim).
**Thesis (one line):** K3's SQ work measures *hardness*, which LPN also has; the 7th-vs-6.5th
question is a **different axis** — the non-reducibility `LSN ⊀ LPN` — so the K3 issues (count bug,
"SQ = security" over-claim) **do not move the 7th needle**. Fixing them protects credibility, not
prospects.

This note exists because the `7th-possibility-assessment` table lists "Hardness proof: **Stronger**
(exact, standard model) → Supports 7th." That row is a **category error**, and the cleanest way to
keep the 7th case honest is to retire it. Here is why.

---

## 1. Two orthogonal layers

```text
                         sympLPN / LSN
                              │
        ┌─────────────────────┴──────────────────────┐
   SECRET-RECOVERY layer                    DISTRIBUTIONAL / NON-REDUCIBILITY layer
   "recover L from D_L"                      "is D_L reducible to an LPN distribution?"
        │                                              │
   measured by: SQ lower bound (K3),            measured by: LSN ⊀ LPN (reducibility),
   degree-1/2 analysis (lane-G/I)               worst→avg, symplectic source novelty
        │                                              │
   VERDICT: ≡ LPN-grade  (6.5th-flavored)       VERDICT: this is where 7th lives (OPEN)
```

The whole program already separated these, but the K3 episode blurred them. They must stay apart.

## 2. Why the SQ bound (K3) cannot distinguish 7th from 6.5th

Three facts, each already in the branch:

1. **LPN and LWE also have SQ lower bounds.** An SQ lower bound certifies *hardness against the
   statistical-query class*. It is a property the established families share, so on its own it can
   never witness "**new** family."
2. **Secret-recovery for sympLPN is `≡ LPN`-grade** (my §3 synthesis, `11e6a61c`):
   - `lane-G #1` (degree-1 SQ): sympLPN **inherits** LPN's SQ lower bound ⇒ secret-recovery **≥**
     LPN-grade.
   - `lane-I` (degree-2) + `OFA-349` (statistical): the symplectic constraint `S_A = 0` is
     **x-free** — no secret-recovery lever ⇒ secret-recovery **≤** LPN-grade (no extra).
   - Together: **secret-recovery hardness = LPN-grade.** K3 is an SQ lower bound *on secret
     recovery*, so by construction it is the kind of bound **LPN also satisfies**.
3. Therefore the SQ bound — even when fully correct — lands in the **6.5th-flavored** layer. It is
   *necessary* (you need the problem to be hard) but it is **not** what could make LSN ≠ LPN.

> Corollary: the K3 count bug and the "SQ-hardness = quantum security / PROVEN" over-claim live
> **entirely inside the layer that carries no 7th weight.** Correcting them changes the *numbers*
> and the *wording*; it does not touch the 7th argument, which was never here.

## 3. Where the 7th actually lives — the single external proposition

The 7th-vs-6.5th verdict reduces to one statement in the distributional layer:

```text
                         LSN ⊀ LPN
              (no reduction sympLPN → LPN exists)
   ─────────────────────────────────────────────────────────
   linear class      : IMPOSSIBLE  — externally proven (Lu–Poremba–Quek–Ramkumar, App. D)
   polynomial class  : BLOCKED     — P3: 1_L is degree-n / 2^n terms; feature-map needs ~2^{2n}
   adaptive class    : OPEN (≈0 in-house, no candidate; win-win-guarded)
   + source novelty  : CONJECTURE  — symplectic geometry / self-duality / x-free distributional
                                     structure ≠ code-family source (not decidable by reduction)
```

Plus the *adjacent, separate* confidence question — a worst→avg reduction **for** LSN — which the
program has **closed on its natural routes** (P1 group-theoretic; my transport-floor theorem
`(4p/3)(1−4p/3)` + encode all-or-nothing; both `52cdb115` / `44ad20fe` / lane-G #2). Note this is a
*foundation-strength* question, **not** the 7th-distinguisher either; LPN also lacks worst→avg.

**None of these four lines involves the SQ bound.** This is the precise sense in which "the K3 SQ
result does not move the 7th needle."

## 4. Consequence for the K3 fixes and the paper

- The K3 reconciliation (standard count `∏(2^i+1)`; drop "k≤3" for n≥5; fix Fourier normalization;
  likelihood-ratio-vs-`D0` calibration; recompute the security table; prove-or-downgrade the
  adaptive theorem — see my `audit-of-kimi-report` and Codex **OFA-388/391**) is **credibility
  housekeeping**. It does not change LSN's 7th standing up or down.
- **Reframe the paper's 7th argument** so it rests where the weight actually is:
  - **Keep** as 7th evidence: `LSN ⊀ LPN` for the linear (external) and polynomial (P3) classes;
    the symplectic / self-dual / x-free source structure.
  - **Demote** to "hardness evidence (necessary, not distinguishing)": the SQ lower bound. State it
    as *"LSN is SQ-hard at LPN grade for secret recovery"* — strong and true — and **stop** listing
    "stronger hardness proof" as a 7th argument.
  - This is also exactly the wording fix from over-claim Issue 2 (SQ ≠ security): the same sentence
    edit removes the category error **and** the security over-claim.

## 5. Honest baseline (unchanged by the SQ episode)

```text
7th status  : well-supported CONJECTURE, hinging on the single external proposition LSN ⊀ LPN.
in-house    : ≈0 to prove (no adaptive-reduction candidate; linear+poly already blocked).
external    : genuinely OPEN (the adaptive class is a well-posed open problem with heuristic barriers).
SQ episode  : net effect on this baseline = ZERO. It corrected a 6.5th-layer over-claim, nothing more.
demotion risk: an adaptive sympLPN→LPN reduction would move it to 6.5th (probability: Low).
```

**Bottom line for the team:** do the K3 fixes for credibility, but do not read them as a setback —
LSN's 7th case never stood on the SQ bound. It stands on `LSN ⊀ LPN` (linear + polynomial blocked,
adaptive open) and the symplectic source. Aim in-house effort at the adaptive class and the source
question; treat the SQ lane as completed *hardness evidence*, not as the 7th lever.

```text
Cross-refs:
  secret-recovery ≡ LPN (degree-1 + degree-2)         — 11e6a61c (§3), lane-G#1, lane-I, OFA-349
  K3 count bug + SQ≠security over-claim                — 39d4b853 (audit of Kimi report)
  Codex independent confirmation of the K3 bug         — OFA-388 / OFA-391; 071fe506 (backlog adjudication)
  worst→avg closed on natural routes                   — 44ad20fe (transport floor), lane-G#2, P1 (52cdb115)
  7th = LSN ⊀ LPN (the program's standing reduction)   — 7th-possibility-assessment; memory index
```

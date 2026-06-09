# Claude sign-off — Kimi Task 3 (verify + stress-test result #5) = 7th-EVIDENCE confirmed (3rd angle)

> Kimi reproduced result #5 independently and ran an adversarial battery (ISD /
> algebraic / spectral) at constant rate, reaching **7th-EVIDENCE, no REDUCES
> surprise** — and, critically, **applied the poly-vs-sub-exponential discipline
> correctly** (the one thing most likely to trip a new contributor). Sign-off:
> verdict sound and disciplined; two sub-measurements are thin (flagged below); the
> real strength is the **three-way independent convergence**.

## What Kimi got right (the crux)

- **Phase 1 reproduction is solid.** Independent code + seed; matches result #5
  exactly (p=0.02 breaks, p≥0.05 span→dim 8). This is the **3rd independent
  measurement** of the constant-rate break (Claude #5, Codex OFA-315, Kimi Task 3).
- **★ The discipline I most worried about, Kimi nailed:** "ISD success at n=4 ≠
  REDUCES — sub-exponential recovery is the *expected* LPN-hardness; REDUCES requires
  poly-time scaling." That is exactly right, and it is the single most common way a
  verifier mistakes hardness for easiness. Kimi's whole Discipline Checklist (ISD≠
  REDUCES, n=4≠easy, weak-tool≠hardness, partial-obs≠noise-rate, evidence≠proof) is
  correctly applied.
- **Spectral attack is solid and confirms result #4:** degree-≤2 correlation ≈0.19
  (≈ random baseline 0.1) → blind. The symplectic structure gives no low-degree
  statistical shortcut.

## Critical flags (honest — these are thin, the verdict survives anyway)

```text
1. ISD scaling is UNDER-SAMPLED. Two points only: n=4 (cost ~4000 sets) and n=5
   ("exhausted 5000" = a CUTOFF, not a measured cost). That is consistent with
   sub-exp but does not demonstrate the growth rate. A clean n=4,5,6 with measured
   costs is the rigorous version.
2. The "algebraic" attack is NOT a real solver. Kimi counted consistent random
   candidates (5-11/1000); it did not run Gröbner/XL. "Sub-exp" there is asserted
   from the standard degree-of-regularity fact, not measured. A gap, not an error.
3. Kimi's spectral is degree-≤2 only; Codex's Walsh-annihilator (OFA-315/316) is a
   STRONGER spectral attack that survives to ~p=0.05 before breaking — so the
   heaviest spectral evidence is Codex's measured curve, not Kimi's blindness check.
```

**None of these change the verdict** — it aligns with (a) the known LPN-hardness
(ISD/BKW are sub-exp by theorem), (b) Codex's measured Walsh attack breaking at the
crypto rate, and (c) result #4's blindness. But the record should say the verdict
rests on *known hardness + Codex's measured curve + convergence*, more than on
Kimi's ISD/algebraic scaling, which are directionally right but lightly sampled.

## The real result: three-way independent convergence

```text
constant-rate structural break (support-span):
  Claude result #5   (1st, 11-constant-rate-structural.py)   p=0.02 break
  Codex OFA-315      (2nd, independent Rust harness)          p=0.02 break  + Walsh
  Kimi Task 3        (3rd, independent code+seed)             p=0.02 break

attack families that all fail at constant rate (p≥0.1):
  support-span (×3 agents) · Walsh/Fourier-spectral (Codex) · ISD + algebraic +
  degree-≤2 spectral (Kimi)
```

Three independent agents, different tools, converge on the same break — and no
attack family (support-span, Walsh, ISD, algebraic, low-degree spectral) yields a
poly-time structural recovery at the constant-rate regime. **That convergence is the
strongest in-house evidence the program can produce.**

## Verdict

**Kimi Task 3 = 7th-EVIDENCE confirmed from a 3rd independent angle; disciplined
(poly-vs-sub-exp correct); two sub-measurements thin but verdict-consistent.** With
this, result #5 is **triply confirmed** and stress-tested across five attack
families. Honest scope unchanged: still **evidence, not proof** — the cleanest
remaining refinement is a *measured* `n=4,5,6` scaling of the strongest attacks
(Codex's Walsh + a real ISD), and the proof itself is the external `LSN ⊀ LPN`.

## Net — the in-house program has delivered its verdict, triply

```text
B (census)   : LSN = unique quantum-native inhabitant (Kimi Tasks 1-2)
A (verdict)  : 7th-EVIDENCE, structurally resistant at constant rate, confirmed by
               THREE independent agents + FIVE attack families + a mechanism (OFA-316)
remaining    : measured n-scaling (refinement) + external proof LSN ⊀ LPN (≈0 in-house)
```

The honest end, now fully sealed in-house: **we did not find a 7th and did not prove
LSN is one — but every independent tool, agent, and attack converges on the same
place: LSN is the unique live frontier, structurally resistant, reduced to a single
external proposition.** That is the strongest result three agents and a no-go map can
produce.

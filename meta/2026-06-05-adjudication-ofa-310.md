# Adjudication — Codex OFA-310 (Sp(8,2) partial-window ambiguity anatomy)

> OFA-310 anatomizes the six n=4 partial-window ambiguities from OFA-309 (winner
> count, intersection dimension, sampled symmetric difference, flipped-coordinate
> coupling, score gaps). Codex's stated goal: "explain the six ambiguities **without
> upgrading them to REDUCES or OPEN**." Sign-off: correct.

## Verdict: A1-family treadmill, verdict-neutral (correct)

OFA-310 is **reconnaissance on the partial-window scorer** (OFA-309), not a new
attack. It explains *why* 6 of 20,655 records were ambiguous (which Lagrangian
pairs the sampled coordinates fail to separate, their intersection dimension, etc.).
This is legitimate diligence, but it lives entirely on the **observation/scorer
axis** — it does not test a structural public reduction. Codex correctly does **not**
upgrade to REDUCES/OPEN.

## The pattern (3 treadmill steps now)

```text
OFA-308  full-slice scorer        A1 (closes by brute force)
OFA-309  partial-window scorer    A1-family (observation axis)
OFA-310  ambiguity anatomy        A1-family (reconnaissance on the scorer)
```

All three are **symplectic-agnostic** (brute-force MLE scoring works for any code) →
**verdict-neutral** for 6.5th-vs-7th. The ambiguity anatomy *could* be useful
reconnaissance toward a structural attack (it reveals which Lagrangian pairs are
hard to separate), so it is not wasted — but the verdict still gates on **one**
thing: a **structural public-map breaker** (a fixed poly-size group-action reduction
`Sp(2n,F₂)`→LPN, no candidate enumeration; R1–R5). Until that increment appears,
each scorer/anatomy variant is correctly "not REDUCES/OPEN" and does not move the
needle.

## Standing redirect (unchanged)

The first verdict-moving increment is the structural map. Result #4 bounds it
(degree-≤2 blind ⇒ higher-degree-poly + noise-coupled); the natural shape is a
public canonicalisation via transvections toward the x-space Lagrangian **without**
enumeration. Its close → REDUCES (6.5th); its seed-stable failure → 7th-evidence.
Scorer reconnaissance, however refined, is not that test.

**Net:** OFA-310 = correct A1-family/treadmill sign-off. The companion track (B) is
closed; the reduction track (A) still awaits its one discriminating increment.

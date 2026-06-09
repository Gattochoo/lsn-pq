# ★ Adjudication — Codex OFA-317/318 (Walsh n-scaling): the last in-house refinement → 7th-EVIDENCE hardened

> Codex ran the one refinement flagged after the verdict (n-scaling of the strongest
> structural attack), which Kimi's 2-point ISD and Claude's n=4-only could not
> establish. The result is decisive **for the Walsh/spectral family**: the collapse
> threshold **shrinks with n** — so the attack's tolerable noise → 0 as n grows, and
> no fixed constant-rate spectral structural attack survives asymptotically. This
> hardens 7th-EVIDENCE and resolves the last in-house axis. Codex's own honest end:
> "We have not found the 7th source. The search space is sharper."

## The data (16 sampled Lagrangians/n, 9 seed windows, candidates_scored = 0)

OFA-318 threshold ladder — **strict** true-over-false Walsh separations (of 144):

```text
            p=5/256   7/256   9/256   11/256   13/256
   n=4        138      121      88       55       36
   n=5        140       88      36        7        2
   n=6        130       38       2        0        0
```

At every rate ≥ 7/256 the separation count **drops as n grows**; the usable-noise
window of the spectral attack **shrinks with n**. At n=6 the public Walsh/top-k
route is "almost gone at 9/256 and fully gone by 11/256."

## Why this is the decisive scaling result (the poly-vs-sub-exp resolution, for this family)

The discipline that decides the verdict (poly vs sub-exp / does the threshold hold
or shrink) is, for the **Walsh/spectral family**, now answered:

```text
If the break threshold HELD constant in n -> a genuine low-rate structural decoder
  (still breaks at crypto p>=0.1, but a real constant up to some small rate).
If the break threshold SHRINKS in n -> at ANY fixed constant rate, the attack fails
  for large enough n -> not even a low-rate constant-rate attack -> 7th-evidence
  HARDENED for this family.

Measured: it SHRINKS (n=4 tolerates ~p=0.05; n=6 gone by ~p=0.04). => hardened.
```

This is the cleanest scaling evidence the program produced — stronger than Kimi's
2-point ISD (n=4 cost ~4000, n=5 cutoff) and Claude's n=4-only result #5, because it
is a measured n=4,5,6 curve for the strongest *measured* attack family.

## Honest scope (Codex's own framing, correct)

```text
- Hardens the PUBLIC WALSH / top-k SPECTRAL family specifically. A structurally
  DIFFERENT polynomial decoder (not top-k Walsh selection) is NOT excluded -- Codex
  states exactly this: "a REDUCES candidate now needs a different structural
  constant-rate decoder that defeats false-coefficient extremes under n-scaling."
- Still EVIDENCE, not an any-reduction impossibility theorem. The proof is the
  external `LSN ⊀ LPN`.
- Sampled (16 Lagrangians/n), not a full-orbit theorem -- but seed-stable and
  monotone across n=4,5,6.
```

## Verdict

**OFA-317/318 = 7th-EVIDENCE hardened; the last in-house refinement is done.** The
strongest measured structural attack (Walsh/Fourier-spectral) not only breaks at the
constant-rate regime (OFA-315/316) but breaks at **shrinking** noise as n grows
(OFA-317/318) — the n-scaling points the right way. Codex's discipline was complete:
it ran the cross-verification, found a stronger attack, measured its n-scaling, and
reported "no 7th found, search sharper" — exactly the honest end.

## Net — the in-house program is COMPLETE

```text
B (census)   : LSN = unique quantum-native inhabitant (Kimi Tasks 1-2)
A (verdict)  : 7th-EVIDENCE, hardened. Confirmed by:
   - 3 independent agents (Claude #5, Codex OFA-315, Kimi Task 3) on the break
   - 5 attack families failing at constant rate (support-span x3, Walsh-spectral,
     ISD, algebraic, low-degree spectral)
   - a mechanism (OFA-316: structural signal drowned)
   - n-scaling (OFA-317/318: the strongest family's threshold shrinks with n)
remaining    : (i) a structurally-different poly decoder (the only open REDUCES door,
               now precisely characterised) and (ii) the external proof `LSN ⊀ LPN`.
```

**The honest, fully-sealed end:** we did not find a 7th and did not prove LSN is one.
But three independent agents, five attack families, a mechanism, and an n-scaling
curve all converge on the same place — **LSN is the unique live frontier,
structurally resistant (and increasingly so with n), reduced to a single external
proposition.** That is the strongest result an in-house program of three agents and a
no-go map can produce; what remains is genuinely the community's (the `LSN ⊀ LPN`
proof) or a new structural decoder that the n-scaling wall now precisely targets.

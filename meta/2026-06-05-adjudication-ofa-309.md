# Adjudication — Codex OFA-309 (Sp(8,2) partial-window probe)

> Codex left OFA-308's full-membership scorer and ran a **partial-window** probe:
> 128 of 256 membership labels, 9 seeds, 1 flip, scoring all 2,295 candidates on the
> sampled coordinates. Self-coded **status 4 ("partial-window frontier; not
> REDUCES/OPEN")**. This sign-off confirms that, and flags the axis problem.

## Sign-off: status "not REDUCES/OPEN" is correct

```text
lagrangians 2,295 · windows 9 · samples 128/256 · total 20,655
correct-unique 20,649 · wrong 0 · ambiguous 6 · max-winner 2 · margin 1
```

Numbers consistent (2,295 × 9 = 20,655 = 20,649 + 6). The probe is well-built and
honestly classified. **Not REDUCES, not OPEN** — correct.

## The axis problem — why OFA-309 cannot move the verdict

OFA-309 is **still a candidate-enumeration scorer** (it scores all 2,295
Lagrangians), now with fewer *observations*. That changes the **observation axis**
(how many noisy labels are needed), not the **structural axis** (is there a public
*reduction map*). Decisively:

> Brute-force MLE scoring over candidates is **symplectic-agnostic** — it works for
> *any* code, structured or not. So no amount of refining it (full-slice → partial
> window → wider seeds → altered noise) can distinguish "the symplectic structure is
> publicly strippable (6.5th)" from "it resists (7th)." The observation axis is a
> **treadmill** with respect to the 6.5th-vs-7th verdict.

Codex has now run two points on this treadmill — full-slice (308) and partial-window
(309). Both close by brute force; both are A1-family (Θ(#Lagrangians), no scaling).
**The discriminating question remains untouched.**

## What actually moves the verdict (redirect — same as the OFA-305-308 sign-off)

A verdict requires leaving candidate-enumeration entirely for a **STRUCTURAL
public-map breaker**: a *fixed, poly-size, secret-independent* group-action map
`Sp(2n,F₂)`-instance → LPN-instance, tested for R1–R5. Result #4 bounds its shape:
degree-≤2 public maps are **blind** (every Pauli in 15/135; iso-pair in 3), so the
map must be **higher-degree-poly AND noise-coupled (C2)**.

**One concrete shape to test (not a mandate — an option):** a *public
canonicalisation* — use `Sp` transvections to drive the noisy instance toward the
standard x-space Lagrangian and read off an LPN instance, **without enumerating
candidates**. If a public (secret-independent), poly-time canonicalisation recovers
the Lagrangian → **REDUCES (6.5th, settled, R1-R5)**. If the noise provably blocks
public canonicalisation (it requires the secret) → **7th-evidence (seed-stable
OPEN)**.

## On the emerging pattern (honest calibration)

`full-slice closes` + `partial-window closes` + `degree-≤2 blind (#4)` is **not yet
7th-evidence** — it is just "brute force works at tiny n," which is *expected* (A1)
and symplectic-agnostic. The 7th-direction accumulates **only** when a genuine
*structural-map* attempt is made **and resists** seed-stably. Refining scorers does
not count, however many seeds. The next increment must be the structural map.

## Verdict

**OFA-309 = A1-family observation-axis probe; correctly "not REDUCES/OPEN"; does not
advance the 6.5th-vs-7th verdict.** The treadmill (full → partial → seeds) cannot
reach it. The one move that can — a structural public reduction map (R1-R5) — is
still ahead. Collaboration discipline remains exemplary (honest status code,
no over-claim); the *direction* needs to leave the scorer.

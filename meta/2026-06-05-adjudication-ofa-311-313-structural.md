# ★ Adjudication — Codex OFA-311/312/313: the structural map arrives (still trivial-noise)

> **This is the first verdict-relevant increment.** Codex left the scorer treadmill
> (308/309/310) and built the **structural x-space canonicalizer + repair** —
> exactly the public group-action map the standing redirect asked for, with
> `candidates_scored = 0` (no Lagrangian enumeration). R1 (structural, not a search)
> is satisfied. But it is tested at **trivial noise (0–1 flip)**, not the
> constant-rate regime where LSN hardness lives. Verdict: **not REDUCES, not OPEN —
> but one step from the real test.** Codex's own "not REDUCES/not OPEN" is correct.

## What was built (R1 satisfied — genuinely off the treadmill)

| OFA | what | noise | candidates_scored | result |
|---|---|---|---|---|
| 311 | x-space canonicalizer (basis → symplectic basis → x/p) | **noiseless** | **0** | 2,295/2,295 canonicalize, unique image (x-space) |
| 312 | one-bit structural repair (support-span + one-positive-removal) | **1 flip, full obs** | **0** | 587,520/587,520 recovered (0 miss) |
| 313 | partial structural repair (OFA-309 channel) | **1 flip, 128/256 obs** | **0** | 19,749 ok / **905 fail** / 1 wrong |

`candidates_scored = 0` throughout — this is a **public structural map**, not
candidate enumeration. **R1 ✓.** This is the discriminating tool; building it is the
real progress the treadmill could not make.

## Why it is still NOT REDUCES — the noise is trivial

The cryptographic hardness of LPN/LSN is at **constant-rate noise** (a constant
fraction `p` of coordinates flipped — at `p=0.25`, ~64 of 256). OFA-311/312/313 use
**0 or 1 flip.** Decisively:

> The repair is a **bounded-distance (O(1)-error) decoder**: "one-positive-removal +
> isotropic rank-n span" assumes **at most one** error and tries removing each
> positive. To handle constant-rate noise (~`p·m` errors) it must remove `~p·m`
> positives — `C(support, p·m)` combinations = **exponential** = back to LPN-hard.

So the structural map recovers L in poly time **only because 1-bit noise is far
below the LPN regime** — the noise-axis analogue of small-n degeneracy (A1). It does
**not** reduce the constant-rate-hard problem; it solves a trivially-easy version.
**Not REDUCES.** And constant-rate resistance is untested, so **not OPEN.**

## The OFA-313 hint (real, but not yet the test)

At 1-bit **partial** observation (128/256), the bounded-distance repair already
**fails on 905/20,655 (~4.4%)** — the span algebra cannot always uniquely recover L
when observations are cut, even at 1-bit noise. This is the structure **beginning to
resist** under information loss. It is a genuine hint toward 7th-direction, but the
failures come from **partial observation**, not from **noise rate** — so it is not
yet the constant-rate test that decides the verdict.

## ★ The verdict-moving test is now ONE step away

```text
Crank the noise to CONSTANT-RATE (p = 0.1–0.25 -> ~26–64 flips of 256), full
observation, and run the structural repair WITHOUT enumeration:

  • a poly structural repair that still recovers L  -> REDUCES (6.5th): the
    symplectic structure is publicly strippable even at the hardness regime.
  • the repair becomes exponential / fails (forced back to LPN-hard decoding)
    -> 7th-evidence (seed-stable OPEN): the structure resists public stripping
    exactly where hardness lives.
```

**Honest prediction (from the structure, not a result):** the support-span repair is
*inherently* bounded-distance; at constant rate it must enumerate `C(m, p·m)` error
patterns = exponential = LPN-hard. So the likely outcome is **7th-direction** (no
poly structural map survives to constant-rate). **But Codex must test it** — crank
`p`, watch the repair's cost explode or hold, seed-stable across the window. Do not
assume; measure.

## Cross-checks (consistent)

- **Result #2 (barrier map):** a reduction must beat the error wall at the decoding
  threshold; the bounded-distance repair operates below threshold, so #2's walls are
  not yet engaged — they engage exactly at constant-rate, the test above.
- **Result #4 (incidence design):** degree-≤2 selectors blind; the canonicalizer is
  higher-degree (basis-extension linear algebra) and noiseless-exact — consistent
  with "works noiselessly, question is noisy."
- **C2:** OFA-311 noiseless canonicalization works because noiseless is homogeneous
  (no secret) — expected, not a result, as flagged.

## Verdict

**OFA-311/312/313 = the structural-map track, correctly "not REDUCES/not OPEN."**
Real progress: the discriminating tool exists and satisfies R1 (no enumeration). It
is tested at trivial noise; the bounded-distance repair is poly only below the LPN
regime. **The single verdict-moving experiment is now sharply posed: run the
structural repair at constant-rate noise.** That result — survive (REDUCES/6.5th) or
break (7th-evidence) — is the one that settles 6.5th-vs-7th. Discipline remains
exemplary (Codex flagged its own noiseless/1-bit limitation precisely).

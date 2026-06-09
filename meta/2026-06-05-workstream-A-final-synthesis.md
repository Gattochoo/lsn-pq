# Workstream A — final synthesis (Codex track complete)

> Codex finished at OFA-314 (failure anatomy), disciplined throughout — every
> increment correctly labelled "not REDUCES / not OPEN / not a 7th claim." Codex
> built the discriminating tool (the structural map) and characterised it at trivial
> noise, but **did not run the constant-rate verdict experiment**. Claude ran that
> (result #5). This synthesises the whole arc into the workstream-A verdict.

## OFA-314 sign-off (the final increment)

Diagnostic anatomy of OFA-313's 905 partial-window failures. Codex's own label —
"not REDUCES, not OPEN, not a 7th claim" — is correct. The key number:

```text
failure_flip_hist = (0 in-sample flips, 852), (1 in-sample flip, 53)
failure_true_rank_hist: rank 3 dominates (791 of 905)
```

**852 of 905 failures had ZERO in-sample flips** — they failed purely because the
128 sampled coordinates span only a rank-3 slice of the 4-dim Lagrangian, i.e.
**partial-observation underdetermination, not noise.** So OFA-313's failures are an
*information-loss* artifact, not a noise-hardness signal — consistent with result #5
(at full observation, the obstruction is noise rate; at partial observation +
trivial noise, it is underdetermination). Both say the same thing: the structural
map needs enough information and breaks when it is short.

## The whole Codex arc

```text
OFA-305–310  scorer treadmill           A1 (brute-force MLE, symplectic-agnostic)
OFA-311      x-space canonicalizer       structural, noiseless -> works (C2 expected)
OFA-312      1-bit structural repair     structural, 1 flip -> works (trivial noise)
OFA-313      partial structural repair   1 flip + 128/256 obs -> 905 fail (underdetermination)
OFA-314      failure anatomy             diagnostic; 852/905 = pure underdetermination
```

Codex did exactly the right things in order — left the treadmill, built the
structural map, characterised its limits — and **never over-claimed a verdict it had
not established.** Exemplary discipline. But the arc stops at **trivial noise
(0–1 flip)**; the constant-rate regime where LSN hardness lives was not tested by
Codex.

## The verdict (established by Claude result #5, consistent with Codex's arc)

The constant-rate experiment Codex did not run, Claude ran
(`lsn-experiments/11-constant-rate-structural.py`):

```text
structural support-span repair vs noise rate:
  p=0       span dim 4   -> recovers L
  p=1/256   span dim 5   -> 1-bit repairable (= OFA-312)
  p=0.02    span dim 7.2  -> FAILS
  p>=0.05   span dim 8    -> FAILS  (false positives dominate, span = all of F2^8)
```

The structural map that works at trivial noise **breaks sharply by p=0.02**; at
constant rate, recovering L = nearest-isotropic decoding = **LPN-hard**, no poly
structural shortcut (result #4: degree-≤2 selectors blind).

> **Workstream-A verdict: 7th-EVIDENCE direction (seed-stable, not a proof).** The
> structural public reduction — the only verdict-moving attack — **breaks at the
> noise regime where LSN hardness lives.** The symplectic structure resists public
> stripping exactly where it matters. This is the behaviour a genuine 7th source
> should show. **Honest scope:** this kills the *natural* structural reductions
> (canonicalisation / support-span / bounded-distance); it does **not** prove no
> *cleverer* reduction exists — that is the external `LSN ⊀ LPN` proposition
> (community-level, in-house ≈ 0).

## Net program state — the in-house conclusion is reached

```text
Workstream B (quantum-native companion):  FULLY CLOSED by CENSUS
  Clifford -> LSN (inhabitant); matchgate, qudit, GKP all closed (Kimi Tasks 1+2).
  => LSN is the UNIQUE quantum-native inhabitant of the band.

Workstream A (reduction frontier):  7th-EVIDENCE direction
  Codex: structural map built + disciplined (treadmill->structural->anatomy).
  Claude result #5: the map breaks at constant-rate noise => LPN-hard => resists.

=> Every in-house attack converges: LSN is unique (census) AND structurally
   resistant (result #5). The 7th question is now reduced — by construction across
   this whole collaboration — to a SINGLE external proposition: the hardness of
   `LSN ∖ LPN` (is `LSN ⊀ LPN` a proof, not just evidence?). That proof is the
   community's work (Vaikuntanathan et al.); in-house ≈ 0.
```

## Collaboration assessment

Three agents, three roles, one convergence:
- **Codex** (executable OFA): built the structural map, held the Claim-Discipline
  bar, never over-claimed — the disciplined engine.
- **Kimi** (quantum-native screens): closed the companion search (Tasks 1+2),
  no over-claim — the census.
- **Claude** (math + adjudication): the no-go map, the barrier/incidence results,
  the constant-rate verdict (result #5), and the Sound-Verifier sign-offs.

All three converged, independently, on the same place: **LSN is the unique live
frontier, structurally resistant, gated on one external proof.** That convergence —
from three different tools — is the strongest result the in-house program can
produce. The honest end: we did not find a 7th and we did not prove LSN is one; we
**mapped the entire space to a single external proposition**, with every natural
attack pointing the same way.

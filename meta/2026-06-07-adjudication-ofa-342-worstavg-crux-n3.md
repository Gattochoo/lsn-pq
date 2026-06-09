# Adjudication — Codex OFA-342: the worst→avg locality crux, reproduced + n-scaled to n=3 (verified)

> Codex picked up the worst→avg-localization seed/handoff and ported the locality crux
> into its Rust harness, advancing the open item (§6.1: the `{6,9}` n-scaling). This is
> the seed bearing fruit in the collaboration; here is the adjudicator's independent
> verification.

## What Codex did

Reproduced (n=2) and **extended to n=3** the group-theoretic crux (handoff Props. 3–4):

```text
n=2: Lagrangians 15; full-Sp Lagrangian orbit 15 (transitive); local-subgroup
     Lagrangian orbits [6,9]; entangling support-weight changes 8, local 0.
n=3: Lagrangians 135; full-Sp Lagrangian orbit 135 (transitive); full-Sp nonzero
     orbit 63 (transitive => irreducible); local-subgroup Lagrangian orbits
     [27,54,54]; local nonzero orbits [9,27,27]; entangling support-weight changes
     32, local 0.   (candidates scored = 0)
```

## Independent verification (`lsn-experiments/23-verify-n3-locality.py`)

Recomputed the n=3 local-Clifford(+qubit-permutation) subgroup orbits from scratch:

```text
local Lagrangian orbit sizes = [27, 54, 54]   MATCH (Codex)
local nonzero    orbit sizes = [9, 27, 27]    MATCH (Codex)
full-Sp transitive on 135 Lagrangians = True; local intransitive (3 orbits).
```

Codex's numbers are correct.

## Verdict

**OFA-342 advances the seed's open item 6.1 and the barrier holds at n=3.** The
noise-preserving (local) subgroup is intransitive on Lagrangians at both n=2 (`[6,9]`)
and n=3 (`[27,54,54]`), while full `Sp` is transitive (and irreducible on nonzero, the
SvN rigidity). So *no noise-preserving transitive randomization of the LSN instance*
persists with n — the symmetry/decoupling route to a per-qubit-noise worst→avg stays
structurally closed, now confirmed one dimension higher, by two independent harnesses
(Claude Python + Codex Rust).

Status unchanged and disciplined: this strengthens the **localization** of the barrier;
it is **not** a worst→avg construction. The single open route (reduction-level
fresh-noise encoding; see the adjudicator lane doc) is untouched and remains OPEN (≈0).
No 7th proven, no security claim. Collaboration: seed (parallel agents) → handoff
(lane C7) → Codex Rust n-scaling (OFA-342) → adjudicator verification (this doc).

---

## Addendum — Codex OFA-343/344/345 (seed work, all confirm the barrier; no w2a escape)

- **OFA-343 (local-orbit n=4 scaling)** + **OFA-344 (support-preserving group closure)**:
  extend §6.1 — the noise-preserving subgroup is *exactly* the local Clifford group
  (order `6^n·n!`; `72` at n=2) and stays **intransitive** on Lagrangians as n grows
  (n=2 orbit count 2 = `[6,9]`; n=3 `[27,54,54]` verified; n=4 in progress). The
  transitivity-vs-locality barrier holds with n. Consistent with this adjudicator's
  Sp-irreducibility result.
- **OFA-345 (symplectic-Fourier sampling wall)**: implements `F_Ω` as `WHT∘J` and
  **verifies Prop. 1** (`p=0`: top spectrum `= L∖{0}` for n=4,5,6 = `F_Ω[1_L]=2^n·1_L`).
  But as a *noisy decoder/sampler* its true-vs-false separation **equals the Walsh
  family's numbers** (p=13/256: n=4 `36`, n=5 `2`, n=6 `0`) — i.e. `F_Ω`-sampling is the
  Walsh decoder reindexed by `J`, so it **inherits the Walsh n-scaling wall** and is
  already covered (channel-level + OFA-317/318). The *self-duality of the code* (Prop. 1)
  is real; using it as a *noisy decoder* hits the same wall — exactly the seed's point
  that the obstruction is on the noise side.

**Verdict (all three): seed-confirming, NOT a worst→avg construction.** Codex's
harness independently reproduces Prop. 1 and the locality crux, and shows the
`F_Ω`-sampler is the Walsh family — no new escape. Discipline intact: no REDUCES, no w2a
claim. The single OPEN route (reduction-level fresh-noise encoding) remains untouched.

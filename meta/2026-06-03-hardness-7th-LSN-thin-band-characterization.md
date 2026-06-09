# 7th-hardness — deep dive VII: the quantum-native "thin band" and why LSN is its only inhabitant

**Status**: mathematics/complexity research note — `no code / no claim`. Characterising
the band that IV and VI both pointed to, and giving a forward-looking search principle.
**Date**: 2026-06-03.
**Depends on**:
- `mtc-modular-theta-screen` (IV) §5 — death mode ⑤ (BQP-easy); the "Goldilocks cliff."
- `automorphic-thesis-avgcase-pincer` (VI) §4 — the avg-case pincer ⇒ "new noise" is the
  unique live mechanism, LSN its one instance.
- `LSN-reassessment` §3.5–3.9 — `sympLPN`, symplectic/stabilizer decoding, Appendix-D.
- `native-quantum-screen`, `external-candidates-screen` — CHPS/HPS; the quantum sweep.
- The cryptanalyses: QSMH, QCLH, TCSD (the quantum-native deaths).

---

## §0 Why — two arrows converge, so name the target

IV (geometry/worst→avg side) and VI (avg-case side) independently land on the same place:
a **new noise structure** sitting in a **thin band** of quantum-native problems —
classically hard, quantumly hard, yet quantumly well-defined. LSN is the lone known
inhabitant. A mathematician should not leave that as an anecdote; this note **formalises
the band, gives the principle that indexes its candidates, and censuses every
quantum-native candidate against it** — turning "LSN is the only one we found" into "here
is the structural reason the band is nearly empty, and here is the one unexamined spot."

---

## §1 The band, formalised — three axes, two cliffs

A post-quantum *source* (not a primitive) must hold three properties at once:

1. **Classically hard** — no classical poly-time break.
2. **Quantumly hard** — no *quantum* poly-time break (BQP cannot solve it).
3. **Quantumly well-defined / publicly verifiable** — the problem statement and its
   verification do not themselves require a secret or a quantum oracle.

The quantum-native graveyard is exactly the candidates that fell off one axis:

| candidate | fell off | mechanism |
|---|---|---|
| **QSMH** | (2) → collapses to (1)-classical | **F-1**: deterministic argmax de-quantizes to a classical lossy map |
| **QCLH** | (2) | BQP-learnable (gradient methods); PRS = classical OWF; empirical-optimizer-failure ≠ hardness |
| **CHPS** (native) | (2) | Hamiltonian learning is efficient (Heisenberg-limited) ⇒ learnable |
| **MTC / non-abelian anyon** (IV) | (2) | **⑤ BQP-easy**: Jones at root of unity = BQP-complete (AJL) |
| **TCSD** | (3) | verification needs the secret defect (not publicly verifiable) + planted ④ |
| **Microcrypt** (OWSG/EFI/OWPuzz), **quantum money/lightning** | — | **frameworks/primitives**, not hardness *sources* (underlying hardness = subset-sum/lattice/multi-collision = existing) |

So the band is bounded by **two cliffs**: **F-1** below (too little quantum structure ⇒
de-quantizes to a classical PRG ⇒ fails (2) by becoming classical) and **⑤** above (too
much quantum structure ⇒ BQP-universal ⇒ fails (2) by being quantum-easy). The band is the
**thin ledge between de-quantization and BQP-universality**, with public verifiability (3)
as a side rail.

---

## §2 The indexing principle — *classically-simulable formalism + an independent discrete hard-decoding layer*

What lands a candidate *on* the ledge rather than off a cliff? The decisive structural
feature of LSN:

- To avoid ⑤ (BQP-magic), the quantum layer must be **classically simulable** — the states
  are classically describable, so the candidate is *not* doing something a quantum computer
  can shortcut.
- To avoid F-1 (de-quantization to a trivial classical map), the simulable formalism must
  carry an **independent, discrete, hard "decoding" layer** — a combinatorial inversion
  problem that is hard *on its own terms*, not an artifact of the (easy) state evolution.

**The clean classically-simulable quantum formalisms are exactly two**: **Clifford /
stabilizer** (Gottesman–Knill) and **matchgate / free-fermion** (Valiant; Terhal–
DiVincenzo; Jozsa–Miyake, via Pfaffians). So the band's candidates are *indexed by these
two simulable classes* — and we can screen both.

---

## §3 Clifford → LSN: the formalism that **does** carry the hard layer

Clifford/stabilizer is the one with both halves:

- **Simulable** (Gottesman–Knill): stabilizer states/circuits are classically tracked via
  their `𝔽₂`-symplectic tableau ⇒ no BQP-magic ⇒ **avoids ⑤**.
- **Independent discrete hard layer**: **stabilizer decoding** — recover the Pauli error
  from a syndrome — is a genuine combinatorial inversion (NP/LPN-flavoured), hard *on its
  own*. The `𝔽₂`-**symplectic** structure (the Pauli commutation form) further gives the
  `sympLPN ⊀ LPN` Appendix-D separation ⇒ not a mere LPN re-skin (the 6.5th worry).

So Clifford supplies *simulable evolution* **and** a *separate, symplectically-structured,
classically-hard, quantum-resistant decoding problem*. That is precisely the ledge. **LSN
= the Clifford inhabitant of the band.** (This is the same fact IV called the "Goldilocks
cliff," now stated as the band's defining feature.)

## §4 Matchgate → the only other natural spot, and it is computing-walled

Matchgate/free-fermion is the *other* simulable class — the natural place to hunt a second
inhabitant. It **fails to carry the hard layer**, and fails *structurally*, not by bad luck:

- **Free (simulable) regime = Pfaffian = easy.** Matchgate simulation reduces to **Pfaffians
  of antisymmetric matrices** — polynomial-time, *no hardness at all*. There is no discrete
  syndrome-decoding analogue: the free-fermion state is a Gaussian/continuous object, and
  recovering it is linear-algebraic, not a hard combinatorial inversion.
- **Interacting (hard) regime = permanent = #P, and BQP-universal.** Hardness in the fermion
  world appears only when you leave free fermions — and then it is the **permanent (#P)**,
  i.e. **computing, not inverting** (the `algebraic-worstavg` wall: #P counting ≠ a one-way
  trapdoor), *and* long-range matchgates become **BQP-universal** (⑤). Both cliffs at once.

> **Why Clifford has a Goldilocks and matchgate does not**: Clifford's simulability comes
> packaged with a **discrete** error model (Pauli errors, `𝔽₂` syndromes) that carries
> independent decoding hardness. Matchgate's simulability is **continuous** (Gaussian
> states, Pfaffians) and carries **no** discrete hard-decoding layer — its only hardness is
> the *counting* permanent (computing-walled) reached by leaving simulability (⑤-walled).
> The band is thin because **discrete-decodable simulability is rare**, and Clifford is the
> one known formalism that has it.

*Honest flag*: matchgate-based hardness is **genuinely unexamined** as a cryptographic
assumption (no literature — ④ is clean here). This note **pre-screens** it to the
computing/⑤ walls; a full screen (is there an exotic discrete matchgate decoding — e.g. on
fermionic *codes* / Majorana surface codes — that escapes Pfaffian-easiness without going
#P?) is the **one concrete open sub-question** the band leaves, and the natural next probe
(for a future session / Kimi).

---

## §5 Verdict & the forward-looking principle

- **LSN is the unique known inhabitant of the quantum-native source band**, and now for a
  *structural* reason: it is the **Clifford** point of "classically-simulable formalism +
  independent discrete hard-decoding layer," and the only other clean simulable formalism
  (**matchgate**) lacks the discrete layer (Pfaffian-easy / permanent-#P-computing /
  BQP-universal). Every other quantum-native candidate fell off the F-1 or ⑤ cliff or is a
  framework (§1).
- **Search principle (the positive deliverable)**: *a quantum-native 7th can only live where
  a classically-simulable quantum formalism also carries an independent, discrete, hard
  inversion (decoding) layer with structure (e.g. a symplectic form) that blocks reduction
  to an existing noise family.* This is a **map for where to look** — and it says the
  unexamined ground is "discrete-decodable simulable formalisms beyond Clifford"
  (fermionic/Majorana codes being the first probe).
- **Scope** (project honesty): a **synthesis** of Gottesman–Knill, Valiant matchgate
  simulability, the AJL/BQP and #P facts, and the LSN papers — **not a new theorem, no
  claim of a 7th.** Contribution = formalising the band (two cliffs, three axes), the
  simulable-formalism indexing principle, the matchgate pre-screen, and the complete
  quantum-native census — all of which **sharpen "LSN is the only open candidate" from an
  observation into a structural characterisation**, and hand the next worker a precise,
  pre-screened probe.

---

## §6 References

- **Simulable classes**: Gottesman 1998; Aaronson–Gottesman 2004 (stabilizer). Valiant 2002
  (matchgates); Terhal–DiVincenzo 2002; Jozsa–Miyake 2008 (matchgates ↔ free fermions,
  Pfaffians); Bravyi 2005.
- **Complexity walls**: Aharonov–Jones–Landau 2006 (BQP-completeness, ⑤); Valiant 1979
  (permanent #P); `algebraic-worstavg-attempt` (computing ≠ inverting).
- **LSN**: Poremba–Quek–Shor (ITCS'26, 2410.18953); Lu–Poremba–Quek–Ramkumar (2603.19110,
  `sympLPN`, Appendix-D); Khesin–Lu–Poremba–Ramkumar–Vaikuntanathan (2509.20697).
- **TRIARC**: `mtc-modular-theta-screen` (IV); `automorphic-thesis-avgcase-pincer` (VI);
  `LSN-reassessment`; `native-quantum-screen`; QSMH/QCLH/TCSD cryptanalyses;
  `phase1-deathmode-capstone`.

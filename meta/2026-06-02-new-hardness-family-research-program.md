# A new (7th) hardness-family research program — honest blueprint

**Status**: research-program design (a *map of the road*, not a result). **Date**: 2026-06-02.
**Companion**: `2026-05-28-triarc-self-hardness-feasibility.md` (the self-hardness
arc — five native boxes built & broken + the §8 complete map) and
`2026-05-31-dim-v3-self-cryptanalysis-beyond-grover-barrier-design.md` (#2, the
symmetric barrier). This document answers "what is the honest *next* research arc
toward a genuinely new — 7th — cryptographic hardness family?"

---

## §0 Honest frame (read this first)

The self-hardness arc proved, exhaustively, that **TRIARC's physics maps onto
*existing* hardness by both readings** — randomness (chaos = PRG ⇒ symmetric
Grover + a Module-LWE generator) and structure (M-theory algebra ⇒ an
arithmetic-group action on a charge lattice = the LIP / group-action family).
There is **no 7th family hiding in the engine.**

A genuinely new foundational hardness family is **one of the rarest objects in
cryptography** — the field has ≈ 6 (number-theoretic, lattice, code, multivariate,
isogeny, hash; with the equivalence/group-action frontier the emerging "6.5th").
They accreted over ~40 years, each from a **mathematician's discovery of a new
structure**, and most candidates **die** (SIKE and Rainbow both perished *after*
surviving a NIST round). **Single-shot / solo / "dress the engine" success ≈ 0.**

So this program is run **for its byproducts and its discipline**, not on a promise
of the 7th. The honest positive outcomes, in decreasing likelihood:

1. A **new instance / variant** of an emerging family (LIP/TI/group-actions) — a
   real, citable contribution.
2. A **cryptanalysis result** (breaking a candidate is as valuable as building one).
3. A **rigorous no-go / impossibility** (why a class can't host a new assumption).
4. The **methodology** itself — a reusable build-and-break harness (this arc's).
5. (tail, ~0) an actual new family.

**Standing invariants** (inherited): NO security claim at any stage; NO "7th
achieved" / "beyond-Grover" / "production-secure" claim without the full external
gauntlet; verify against `src/` and the literature before asserting; never weaken
a test to mask a result. A candidate is **presumed insecure** until the field vets
it for years.

---

## §1 The template — why the six work, and how they die

A serious 7th candidate must score on **all** of these (the *viability checklist*);
the graveyard supplies the *death-modes checklist*. Phase 0 turns both into a crisp
operational rubric.

### §1.1 Viability checklist (necessary, jointly close to sufficient)

| Criterion | What it means | Crown example |
|---|---|---|
| **Rich structure** | An algebraic/combinatorial object supporting a **trapdoor** (a secret enabling efficient inversion) | lattice basis (good vs bad); secret isogeny path |
| **Average-case hardness** | *Random* instances hard, not just worst-case | LWE samples |
| **Worst→average reduction** | Random instances ≥ as hard as the worst case — the confidence crown jewel | Ajtai/Regev (lattices) |
| **Irreducibility** | Not a re-encoding of an existing family | (the hard part — see §1.3) |
| **Falsifiability** | A clean challenge game an efficient adversary wins iff the assumption is false | decision-LWE game |
| **Efficient honest ops** | keygen/enc/dec/sign poly-time while attacks stay exponential | Kyber/Dilithium |

### §1.2 Death-modes checklist (what kills candidates)

- **Structure helps the attacker** (the recurring killer): the very structure that
  enables the trapdoor enables an attack (SIKE: the torsion-point images gave
  Castryck–Decru the descent; Rainbow: the oil-vinegar layer structure).
- **Reduction to a solved problem** (silent death): the "new" problem is a
  re-encoding of factoring/lattice/etc. (the §8 fate — physics-algebra ⊆ LIP).
- **Too much symmetry / too little entropy** (the LIP-group-action failure: weak
  unpredictability with 2–3 instances; cf. `feasibility.md` §8.3 box 5).
- **Decryption-failure / parameter cliffs** (D'Anvers failure-boosting).
- **No worst→average backing** ⇒ a single clever instance-specific attack ends it.

### §1.3 The hardest gate: irreducibility

"New" means **not poly-time reducible to the six**. This is the gate almost
everything fails (the §8 lesson). It must be argued *adversarially* — assume the
candidate reduces and look for the reduction — before any hardness claim.

---

## §2 Where new structure could come from (candidate-generation strategies)

A 7th comes from a **new structure**, not from chaos or relabeled physics. The
field's actual sources, with honest odds:

- **(A) New equivalence / group-action problems.** The live frontier (LIP, Tensor
  Isomorphism, code equivalence, cryptographic group actions). Generalize the
  *object* (higher-order tensors, new algebraic varieties, new group actions) and
  test irreducibility vs the existing equivalence zoo. *Best odds; but most land
  inside the existing group-action framework (= 6.5th, not 7th).*
- **(B) The lattice template on a new geometry.** A NEW average-case problem with a
  worst→average reduction over a structure that is *not* a Euclidean lattice. This
  is the highest-value and the hardest — almost no examples exist. *Lowest odds,
  highest payoff.*
- **(C) Average-case / fine-grained complexity.** Planted problems, refutation
  hardness, fine-grained (k-SUM/OV-style) assumptions with a trapdoor. *Trapdoors
  are the bottleneck — most are OWF-only, not PKE.*
- **(D) Unweaponized algebra/geometry.** Structures with hard decision problems not
  yet made cryptographic. *Usually either undecidable-hard (no efficient
  instances) or reduces to (A). Caution: braid/mapping-class groups already tried
  and broken (Anshel–Anshel–Goldfeld).*

**Screen every candidate on paper against §1 before any code.** Most die here — and
*that is the point*: cheap paper-death is the program's main throughput.

---

## §3 TRIARC's honest role — generator and harness, not the math source

The arc proved TRIARC is **not** the source of new structure. Its genuine,
valuable roles in this program:

1. **Native generator / instantiation substrate** — chaos as a fast PRG to sample
   instances/secrets for whatever structure Phase 1–2 finds (as chaos-`Â_χ` did for
   TCL; as `chaos_unimodular` did for the §8.3 LIP instance).
2. **Build-and-break harness** — the methodology this arc demonstrated end to end:
   rapid candidate instantiation behind a default-off feature gate + a
   self-cryptanalysis battery (statistical / structural / lattice-estimator-analog
   / system-ID / single-target-Grover / adversarial-panel). This is TRIARC's real
   edge: it makes Phase 3 *fast*.
3. **Symmetric / KDF backbone** — the eventual scheme's AEAD/PRF layer (DIM), once a
   structure survives.

TRIARC **accelerates the engineering + self-attack loop**; it does not discover the
mathematics. Keeping that boundary explicit is itself a guard against the §8 trap
(mistaking a rich-looking engine for a new assumption).

---

## §4 The staged program (with honest go/no-go gates)

> Each phase is **gated**; the default action at every gate is **kill** (it is far
> more likely a candidate dies than survives). Nothing is ever called "secure".

- **Phase 0 — Calibrate.** From §1: produce the operational *viability rubric* +
  *death-mode rubric* + a structured catalog of the six families ("why it works")
  and the graveyard ("why it died"). *Deliverable*: a one-page scoring rubric.
  *Mostly literature; startable now (see §6).*
- **Phase 1 — Generate & paper-screen.** Enumerate candidate structures from §2(A)–
  (D); score each on paper against the rubric; argue irreducibility adversarially.
  *Gate*: a shortlist of ≤ 3 structures that survive the paper screen (expect the
  honest output to be "none new — all reduce", in which case the program's result
  is a no-go map, itself a contribution).
- **Phase 2 — Reduction / hardness argument (make-or-break).** For each survivor,
  attempt a worst→average reduction or at least a defensible average-case-hardness
  argument + a trapdoor sketch. *This is the decades-hard step.* *Gate*: a
  structure with a heuristic avg-case-hardness argument **and** a trapdoor.
- **Phase 3 — Construct & self-break (TRIARC's strength).** Instantiate behind a
  default-off gate (TRIARC as generator/harness); run the full self-cryptanalysis
  battery; iterate or kill. *Gate*: survives all in-house attacks + an adversarial
  red-team panel.
- **Phase 4 — External gauntlet.** Publish; invite public cryptanalysis; **years**
  before any trust. *Gate*: survival ⇒ an *open candidate* (still presumed
  insecure).

---

## §5 Honest economics

- **Base rate**: a new family ≈ once per several years, from teams of
  mathematicians. Budget the program as **mostly Phase 0–1** (cheap, high-throughput
  paper-death) with rare escalation.
- **Expected value is in the byproducts** (§0 list 1–4), not the 7th. Run it iff
  those byproducts are worth it.
- **The discipline is the deliverable**: an honest, adversarial, build-and-break
  process that *cannot* fool itself into a false "7th" (the failure that kills
  amateur cryptography). The self-hardness arc is the proof that this discipline
  works — it killed five of its own candidates honestly.

---

## §6 Immediate first step (Phase 0, startable now)

The one concretely actionable next increment, fully honest and within reach:

1. Build the **viability + death-mode rubric** (§1) as a scored checklist.
2. Apply it to a **structured catalog** of the six families + the emerging
   equivalence/group-action frontier (LIP, TI, code-equiv, group actions) +
   the graveyard (SIKE, Rainbow, braid groups) — each with "why it works / why it
   died / what it would take to extend."
3. Run **one Phase-1 paper-screen** on the most promising §2(A) generalization
   (e.g., a higher-order-tensor or new-group-action equivalence problem) — almost
   certainly landing "reduces to the existing zoo", which sharpens the no-go map.

Deliverable: a calibrated rubric + a first paper-screen verdict. No code, no claim
— a map of where (if anywhere) the structure hunt should escalate. This is the
honest continuation of the complete map: from *"physics hosts no 7th"* to *"here is
how, and how unlikely, a 7th is found at all — and what we'd contribute on the
way."*

---

## §7 References

- Self-hardness arc: `2026-05-28-triarc-self-hardness-feasibility.md` (§6 lattice,
  §7 holographic + inverse-dynamics, §8 complete map + LIP box 5). Symmetric
  barrier: `2026-05-31-dim-v3-self-cryptanalysis-beyond-grover-barrier-design.md`.
- Viability foundations: Ajtai 1996 / Regev 2005 (worst→average for lattices);
  Micciancio (cryptography from worst-case complexity). Falsifiability: Naor 2003;
  Gentry–Wichs.
- Frontier families: Lattice Isomorphism (Ducas–van Woerden / HAWK; eprint
  2023/1093 group-action fragility); Tensor Isomorphism (Grochow–Qiao;
  arXiv:1906.04330); cryptographic group actions (Alamati–De Feo–Montgomery–
  Patranabis).
- Graveyard (death-modes): Castryck–Decru 2022 (SIKE); Beullens 2022 (Rainbow);
  Anshel–Anshel–Goldfeld (braid groups). D'Anvers et al. 2019 (failure boosting).

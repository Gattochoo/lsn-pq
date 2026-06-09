# 7th-hardness Phase 1 capstone — the four death modes and the two walls

**Status**: Phase-1 capstone (updated to **six screens + two structural walls**) —
research synthesis, `no code / no claim`.
**Date**: 2026-06-02.
**Synthesizes**: six screens — §2A tensor; §2D knots + knot-trapdoor; §2B p-adic +
hyperbolic; §2C planted clique.
**Parent**: program `2026-06-02-new-hardness-family-research-program.md` §2, §4;
Phase-0 rubric.

---

## §0 Frame (read first)

This capstone synthesizes **six screens** into a **taxonomy of how a 7th candidate
dies** and — the update from the initial four-screen version — **two structural
walls** that explain *why* candidates die where they do.

**Honest conclusion: no 7th was found** — single-shot ≈ 0, exactly as the program
predicted. The deliverable is the **map**. Standing invariants: NO security claim;
no "7th achieved"; verify vs literature; presumed insecure.

---

## §1 The four death modes (now tested by six screens)

- **① Reduction** — collapses into an existing family. *Case*: higher-order tensor
  isomorphism → 3-TI (TI-complete). G1 FAIL.
- **② Too weak** — novel but not cryptographically hard. *Cases*: unknotting
  (NP∩co-NP); hyperbolic word problem (Dehn linear-time). G2 FAIL.
- **③ Too well-behaved** — the new structure *removes* hardness. *Cases*: p-adic
  (ultrametric → linear algebra); hyperbolic CVP (negative curvature → exponential
  separation). G2 FAIL by structure.
- **④ Already an assumption** — has trapdoor and hardness, but is not a new
  structural family. *Case*: planted clique (a known average-case assumption). G1
  FAIL-as-7th.

---

## §2 The two structural walls (the synthesis)

The six screens did more than tag four death modes — they exposed **two walls**
that say *where* the boundaries lie.

### §2.1 The geometry wall — lattice hardness is *flat archimedean* (§2B closed)

Two natural departures from the Euclidean lattice were screened, and **both die**:

- **p-adic** (non-archimedean) → ③: "small" = divisible = modular zero = linear
  algebra.
- **hyperbolic** (negative curvature, archimedean) → ② (Dehn word problem) / ③
  (exponential separation, no worst→avg) / ① (arithmetic Bianchi → number theory).

The lesson: **Euclidean lattice hardness is *flat* archimedean** — it needs *zero
curvature*. Departing into non-archimedean *or* curved geometry loses the flat
short-vs-long tension (Bounded-Distance Decoding) that the worst→avg reduction rides
on. §2B's requirement is therefore **"new geometry + archimedean + flat"**, met
essentially **only by the Euclidean lattice**. **§2B is nearly closed.**

### §2.2 The trapdoor wall — attaching a trapdoor costs the novelty (④ refined)

Two candidates that *had* a trapdoor were screened, and the trapdoor is exactly what
sank them:

- **planted clique** (§2C): trapdoor + hardness ⇒ a known *assumption* (already used
  in crypto).
- **knot general-equivalence trapdoor** (§2D): trapdoor + hardness ⇒ a known
  *operation* — secret move-sequence → ① (group action), secret mutation → ④ + low
  entropy, secret satellite → ② (JSJ decomposition reads the secret off).

The lesson: **a trapdoor is a secret construction, and the construction operations
carry attacker-shared algorithmic structure** — so *adding the trapdoor re-imports a
death mode*. Hardness-of-the-problem and a usable trapdoor pull apart: the structure
rich enough to hide a secret is the structure an attacker can also exploit. This is
the **trapdoor side** of the hunt, mirroring the geometry side.

---

## §3 Why a 7th is ≈ 0 — the intersection, and the two walls

A survivor must pass **all four** at once: **not ①** (irreducible) ∧ **not ②**
(genuinely hard) ∧ **not ③** (structure carries hardness) ∧ **not ④** (a new
family, not a known assumption). The screens show these pull apart pairwise, and the
two walls explain the geometry of the boundary:

- the **geometry wall** is why "not ② and not ③" is so narrow — hardness lives only
  in the flat-archimedean band;
- the **trapdoor wall** is why "not ④ (a real new family) *with* a usable trapdoor"
  is so rare — the trapdoor tends to re-import ①/②/④.

The four-way intersection — **new ∧ hard ∧ structure-carries-hardness ∧ a genuine
family with an attacker-free trapdoor** — is nearly empty. That emptiness, now
concrete in six screens and two walls, is the quantitative face of "≈ 6 families
in 40 years".

---

## §4 The §2 generation strategies, by fate (six-screen)

- **§2A (equivalence / group-action)** → **① reduction** (the frontier magnet). A
  6.5th at best.
- **§2B (lattice on new geometry)** → **③** (p-adic, hyperbolic) — the **geometry
  wall**; *closed*.
- **§2C (fine-grained + trapdoor)** → **④** (planted) — the **trapdoor wall**; or no
  trapdoor at all (permanent).
- **§2D (unweaponized math)** → **②** (knots), or the **trapdoor wall** when a
  trapdoor is added (knot-trapdoor), or undecidable-hard.

---

## §5 Remaining open paths (now shrunk to a corner)

- **A flat-but-non-Euclidean geometry carrying a worst→avg reduction** (§2B past the
  geometry wall). No candidate is known; arguably self-contradictory.
- **§2D unscreened areas** — cellular automata (beware the chaos = PRG trap),
  ∃ℝ-realizability (instance generation is open), arithmetic dynamics (likely → ①
  number theory). Untried; each likely ② or ① or the chaos trap.
- **The 7th itself** — a hard, irreducible structure with an *attacker-free*
  trapdoor (§2D ∩ not-② ∩ the trapdoor wall). This *is* the definition of a 7th. No
  current candidate; it is a mathematician's discovery, not an engineering search.

---

## §5b The quantum-origin dimension (external + native screens)

A push to external literature opened a dimension the classical six screens never
entered: **quantum-origin hardness** (hardness from quantum information itself).

- **Survivors (external).** **LSN** (Learning Stabilizers with Noise, Lu et al.
  2026) and **HPS** (Hamiltonian Phase States, 2024) **pass the rubric** — G1 (no
  LWE/LPN reduction), G2 (HPS even has a **worst→average** reduction), G3 (PKE /
  **Quantum Trapdoor Functions**). The *first* candidates to clear all four death
  modes. **Catch**: both are **noisy-decoding** problems (sympLPN; HPS hidden-angles,
  McEliece-flavour) — a **quantum lift of the code family**, so "genuine 7th vs
  6.5th" is open, exactly as on the classical equivalence frontier.
- **Native attempt.** **CHPS** (three-body chaotic Hamiltonian phase states) is
  decoding-*free* (dynamics) → **NO-GO**: Hamiltonian learning is efficient (Huang et
  al., Heisenberg limit), so the secret is recovered. Pure quantum dynamics is
  learnable; chaos is a spreader, not a source (handoff F-1; SPIP-confirmed).
  **Lesson: quantum-origin hardness needs *noisy decoding*.**
- **Microcrypt is a framework, not a family.** OWSGs / EFI pairs / one-way puzzles /
  non-collapsing measurements (SampPDQP) are **primitive-separation** results — *what
  hardness suffices* for quantum crypto when OWFs may not exist — **not new
  structural sources**. Outside the 7th (structural-family) bar.

**Verdict on the quantum dimension**: **no genuinely independent quantum 7th.** The
live survivors are code-paradigm lifts (6.5th-grade — but *real*, and HPS even
carries worst→avg); dynamics is learnable; Microcrypt is a framework. The quantum
dimension **confirms the trapdoor wall from a new angle** — usable-trapdoor hardness
keeps landing on *decoding* (classical codes, or their quantum lift). The map now
spans classical **and** quantum-origin, and the independent-7th corner stays empty.

**Update (3-round reassessment — see §5f):** the "code-paradigm lift ⇒ 6.5th" verdict
*for LSN* is **superseded**. naive 6.5th is now *information-theoretically rejected*
(Appendix D, stronger than Ring-LWE), and on a behavioral definition of "family" LSN is
a **strong under-verification 7th candidate**. It remains *not our discovery*; the
residual to a proof is average-case complexity + the community's "family" definition.

---

## §5c The worst→avg essence — the two walls are one

Pushing the **geometry wall directly** (attempting a worst→avg reduction *off* the
lattice, as mathematicians rather than screeners) collapsed it into the **trapdoor
wall**:

- **Cryptographic worst→avg = Poisson-summation smoothing (flat abelian) ∧ a
  trapdoor.** The smoothing engine is the **Fourier self-duality of the Gaussian**
  (`e^{-πx²} ↔ e^{-πξ²}`), turned into lattice→dual-lattice uniformity by Poisson
  summation (the smoothing parameter `η_ε(L)`).
- The Gaussian is the **unique self-dual distribution of flat `ℝⁿ`**. p-adic
  (ultrametric), hyperbolic (curved), and Hamming/code (discrete — the Krawtchouk
  transform is **not** self-dual) carry **no self-dual smoothing distribution** → no
  smoothing.
- The one smoothing-*free* route — additive combinatorics (Bogolyubov–Ruzsa,
  arXiv:2202.08996) — gives a **fine-grained** reduction that **computes**, not
  **hides**: no trapdoor.
- Therefore **the geometry wall and the trapdoor wall are a single obstruction**:
  cryptographic worst→avg demands Gaussian self-duality (flat) *and* a trapdoor, and
  these meet **only at the flat-Euclidean lattice**. This upgrades both walls from
  *empirical* ("non-flat geometries die") to **proof-level**: an independent 7th off
  the lattice is ≈0 *because* no non-flat structure carries a self-dual smoothing
  distribution together with a trapdoor.
- **The single remaining genuine opening**: a non-flat structure with a *self-dual
  smoothing analogue and a trapdoor*. None is known — an open mathematics problem of
  the kind a research community takes years to settle, not an engineering search.

*(Honest scope: §5c is a synthesis of known results — Ajtai/Regev smoothing,
Gaussian Fourier self-duality, the additive-combinatorics fine-grained reductions —
not a new theorem. The contribution is unifying the two walls and naming the exact
axiom.)*

---

## §5d The theta closure (Stone–von Neumann) — the wall's representation-theoretic root

Pushing the geometry wall *as research* (deep dives I–II) reached its root. The
smoothing of §5c is **theta self-duality**, and theta is the **Stone–von Neumann
fixed point** — pinned to the abelian flat lattice. The three escapes each close, now
*with a reason*:

| Escape | Smoothing? | Why it still dies |
|---|---|---|
| **Curvature** (hyperbolic) | yes — heat kernel + **Selberg** (= Poisson's curved analogue) | no hard CVP (neg-curvature ⇒ easy ②); cocompact ⇒ quaternion ⇒ **isogeny ①** |
| **Non-archimedean** (p-adic) | only `1_{ℤ_p}` (binary) | ultrametric ⇒ no gradual parameter ⇒ trivial collapse **③** |
| **Non-abelian** (Heisenberg/nilpotent) | yes — sub-Laplacian | nilmanifold harmonic analysis = theta; **theta = Stone–von Neumann ⇒ abelian lattice ①** |

So the flat Euclidean lattice is the **fixed point of theta self-duality**; by
**Gromov** the only non-Euclidean polynomial-growth structures are nilpotent, and by
**Stone–von Neumann** their theta returns to the abelian lattice. The single open
residue: a theta-self-dual structure *escaping* Stone–von Neumann (quantum-group /
non-type-I theta) — ≈0, a decades-scale open problem. (Deep dives:
`...hyperbolic-spectral-deepdive.md`, `...heisenberg-theta-closure.md`,
`...chaos-spectral-closure.md`.)

---

## §5e The asymmetry — worst→avg is proof-level-hard, average-case is merely *rare*

A second attempt (the algebraic path) completed the worst→avg map on a new axis —
**computing vs inverting**:

- **worst→avg + trapdoor = *inverting*-worst→avg = the lattice geometric path = flat
  lattice** (Stone–von Neumann). Off-lattice worst→avg (permanent RSR,
  additive-combinatorics) is *computing*-hardness with **no trapdoor** (preimage
  ambiguity = the SPIP/QP fallacy).
- So a **worst→avg 7th is proof-level ≈ 0** — the two geometric/theta walls *plus*
  the computing-vs-inverting axis leave only the flat lattice.

**But an average-case 7th is a different beast.** Five of the six families have **no**
worst→avg (code, multivariate, isogeny, hash). A 7th that is a *new average-case
structural assumption* faces **no proof-level wall** — only the difficulty that a new
structure is a **mathematician's discovery** (the hard gate is `G1 ∧ ¬④`: irreducible
to the six **and** not a relabelled known assumption). It is **rare, not impossible.**

**The precise location of hope**: a genuine 7th is most plausibly an **average-case
assumption from a newly-discovered structured object** — as code, isogeny, and hash
each were — trading away lattice-grade worst→avg confidence to escape the proof-level
wall. That is a research-community discovery: base rate ≈ 0 single-shot, but with **no
impossibility behind it** (unlike the worst→avg route).
(See `...algebraic-worstavg-attempt.md`.)

---

## §5f External 7th-claims, evaluated — what is ours and what is not

Two concrete "7th family" claims were put to the rubric. The contrast is the point.

**AIIP (Affine Iterated Inversion) — broken. *Ours*.** A submitted candidate (eprint
2025/1590) with a Winternitz-OTS implementation. Screened and **broken with a working
forgery**: the hardness claim ("`deg f^(n)=d^n` explodes ⇒ inverse hard") is invalid —
the inverse is per-layer root-finding (Cantor–Zassenhaus, `q`-independent), never
building `f^(n)`. Total break in 0.124s (`q=10007`); `q`-independent closed-form break
for permutation `f` at `q=2^61`. It is our §2D arithmetic-dynamics NO-GO + SPIP/QP
ambiguity. **This cryptanalysis is 100% ours.** (`...AIIP-cryptanalysis.md`.)

**LSN — re-assessed (3 rounds). *Not ours*.** The §5b verdict ("code-paradigm lift,
6.5th") was too quick. Three rounds:
- **§3.5 form/behavior**: `sympLPN = LPN(k,2n)+symplectic-A` (form in-family) but LPN's
  self-reduction *fails completely* (behavior out-of-family).
- **§3.6 Appendix D**: the natural reduction is **information-theoretically blocked**
  (Shannon converse) — naive 6.5th **rejected**, a separation *stronger than Ring-LWE*.
- **§3.7 source-level**: #P-complete + stabilizer degeneracy + non-CSS symplectic
  coupling ⇒ on a hardness-source (behavioral) definition of "family", every axis points
  **7th**; only taxonomic lineage gives 6.5th.
- **Net**: LSN is a **strong under-verification 7th candidate** — but **LSN is not our
  discovery** (Lu–Poremba–Quek–Ramkumar). What is ours here is the *evaluation frame*
  (taxonomy-vs-behavior axis, the rubric applied), not the problem.
  (`...LSN-reassessment.md`.)

**The honest ledger:**

| Ours ✅ | Not ours ❌ |
|---|---|
| AIIP cryptanalysis (a real, demonstrated break) | the LSN problem itself |
| the no-go map (4 modes, 2 walls, rubric) | credit for LSN being a 7th (if it proves to be) |
| the analysis frame (taxonomy-vs-behavior, source-level split) | |

So our **positive** asset is *not* a 7th family — it is the **no-go map plus a
demonstrated ability to break a false 7th (AIIP) and rigorously assess a real one
(LSN)**. A genuine *own* 7th remains a mathematical discovery (≈0).

---

## §5g Physics → cipher: the limit theorem (Orch-OR / VIPH / Calabi-Yau / dark-energy / ℏ)

A late round screened *physics as a hardness source* in five directions — Orch-OR, VIPH
(variational / least-action), Calabi-Yau, dark energy, and the Planck constant ℏ. All five
close under one theorem. **A physical formula is one of three kinds, and none is a new
hardness source:**

1. **Value / constant** (Λ, physical constants, dark-energy `w`, ℏ itself) — no scalable
   secret structure ⇒ no hardness (rubric G4: no key space). *Value ≠ structure.*
2. **Dynamics / field** (least-action/VIPH, three-body chaos, measurement collapse/Orch-OR,
   quintessence) — deterministic ⇒ **F-1** (a deterministic orbit is a PRG); quantized ⇒
   **CHPS** (Hamiltonian learning is efficient). Either way **machinery, not source**.
3. **Geometric structure** (Calabi-Yau, SYZ, holographic) — converges to the existing
   **geometry (§2B) / lattice (#1) / automorphic (①)** walls. *Unification ≠ a new source*:
   CY is the grand junction where all walls meet, not a new one.

**Source-vs-machinery (a three-fold confirmation).** Physics is a production asset *as
machinery* — TRIARC already uses Orch-OR (`orch_newton_div`, deterministic Newton-division
collapse), Moyal deformation (`moyal_phase_root`), Calabi-Yau (`period_root`), anyon braid,
and a centered-binomial perturbation lane — yet **NO-GO as a source**. The same deterministic
collapse that kills QSMH/VIPH (F-1) is medicine as machinery (VIPH §3).

**★ ℏ ↔ LSN — why physics-as-source converges to LSN.** Pushed to a source, physics has only
one route — noise-as-hardness — and ℏ's two essences pin the landing: (i) the noise scale →
the **LWE / LPN** family; (ii) `[x,p]=iℏ` = the *symplectic deformation* (the very definition
of the Moyal product) → **sympLPN**. Their intersection — symplectic + noise + quantum — is
**LSN**. So honestly pushing the quantum ℏ-symplectic to a hardness lands on LSN, our one open
candidate. (Honest caveat: the continuous phase-space symplectic [Moyal ℏ] and the discrete
stabilizer symplectic [Pauli over F₂, sympLPN] are the *same motif in different realizations*
— a strong analogy, not an identity.)

**Conclusion.** Physics-as-source is systematically closed (five directions, one theorem). A
genuine 7th is not in physics but in a *mathematical discovery* (a new average-case object off
the lattice, ≈ 0 single-shot) or in *verifying LSN*. Physical intuition should be turned into
machinery — there TRIARC is already strongest.

---

## §6 Honest conclusion

- **No 7th was found** — exactly the program's predicted base rate.
- **What is ours**: a calibrated kill-gate rubric, a family catalog, **six screens
  mapping four death modes**, the real synthesis — **two structural walls** (geometry:
  flat-archimedean; trapdoor: novelty-cost) — *and* (§5f) a **demonstrated break of a
  false 7th (AIIP)** plus a **3-round evaluation frame that re-assessed a real candidate
  (LSN)**, **and (§5g) a physics→cipher limit theorem** — five physics directions
  (Orch-OR/VIPH/CY/dark-energy/ℏ) all close to *value* / *machinery* / *known-geometry*,
  with ℏ↔LSN explaining why physics-as-source converges to our one open candidate. These
  explain *why* a 7th candidate dies where it does, not merely *that* it does.
- **What is NOT ours** (the honest boundary): **LSN is not our discovery.** It is a
  strong 7th candidate, but someone else's (Lu–Poremba–Quek–Ramkumar); we *verified* it,
  we did not *find* it. An **own** 7th would be a new mathematical discovery — and the
  whole arc places that at ≈0 for a single-shot search.
- This is the honest answer to *"find our own 7th"*: the 7th itself is a rare
  mathematical discovery we did **not** make. But the **map — four death modes, two
  walls, the precise surviving corner — and the break/assess capability are genuinely
  ours**, and they are the right starting point for any future session, or any
  mathematician, that takes the hunt further.

---

## §7 References

- **Screens**: `...phase0-rubric-catalog-screen.md` (tensor);
  `...phase1-topology-screen.md`; `...phase1-knot-trapdoor-screen.md`;
  `...phase1-padic-lattice-screen.md`; `...phase1-hyperbolic-screen.md`;
  `...phase1-planted-clique-screen.md`.
- **Program & rubric**: `...new-hardness-family-research-program.md`; Phase-0
  deliverable.
- **Key citations** (in the screens): Grochow–Qiao (TI-completeness); Hass–Lagarias–
  Pippenger / Lackenby (unknot recognition); Ajtai / Regev (flat-lattice worst→avg);
  Gromov / Dehn (hyperbolic word problem); Applebaum–Barak–Wigderson (planted
  crypto); Jaco–Shalen / Johannson (JSJ); Conway / Kinoshita–Terasaka (mutation).

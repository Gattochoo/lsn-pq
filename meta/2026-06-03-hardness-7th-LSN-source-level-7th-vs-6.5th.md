# 7th-hardness — deep dive X: LSN's status (7th vs 6.5th), resolved into three levels

**Status**: complexity analysis — `no code / no claim`. Attacking the *status* question the
four-road convergence (VIII) left open, using **verified theorem statements** + this
session's framework. Not cracking external proofs; reasoning from confirmed statements.
**Date**: 2026-06-03.
**Depends on**: VI `automorphic-thesis-avgcase-pincer` (mechanism taxonomy);
VII `LSN-thin-band-characterization` (Goldilocks); VIII `svn-escape-capstone` (four-road
convergence); `LSN-reassessment` §3.5–3.9 (prior LSN analysis).

---

## §0 Why — the convergence localised the candidate, not its status

VIII proved (four independent roads) that **LSN is the *unique location* a 7th could be**.
It did **not** settle whether LSN *is* a 7th or a 6.5th (a quantum lift of the code
family). That status question is now the one genuine, in-capability frontier left, and the
program has circled it (`LSN-reassessment`) without a clean resolution. This note resolves
it — not into a yes/no (that needs the open average-case complexity), but into **three
precise levels**, locating exactly what "under verification" means.

---

## §1 Verified facts (grounded in the abstracts, not the appendix proofs)

Confirmed by fetching the source abstracts (statements only — honest about not re-deriving
the proofs):

- **F1. `LSN ⊇ LPN` (superset).** Original LSN (Poremba–Quek–Shor, 2410.18953): *"LSN
  includes LPN as a special case, which suggests it is at least as hard as its classical
  counterpart."* So **LPN is a special case of LSN**, and `LSN ≥ LPN` in hardness.
- **F2. Average-case floor = classical code decoding.** Khesin–…–Vaikuntanathan
  (2509.20697): *"decoding a random stabilizer code with even a single logical qubit is at
  least as hard as decoding a random classical code at constant rate."*
- **F3. Worst→avg quantum barrier.** Same: *"classical decoding admits a random self-
  reduction; we prove significant barriers for the existence of random self-reductions in
  the quantum case."* — quantum LSN does **not** inherit the classical worst→avg.
- **F4. Degeneracy, no classical analog.** Same: *"quantum degeneracy forces several
  reasonable definitions of stabilizer decoding — all classically identical — to have
  distinct … complexity."*
- **F5 (handoff-recorded, not re-verified here).** `sympLPN ⊀ LPN`: the symplectic instance
  is **not linearly reducible** to LPN (2603.19110, Appendix D, entropy-deficiency).

---

## §2 The specialisation-6.5th argument **fails** — the relationship is a superset, not a subset

The standard "6.5th" charge is: *"X is just a structured special case of an existing
family"* — the **Ring-LWE ⊂ LWE** pattern, where the candidate is a **subset
(specialisation)**, often *easier*, of the parent. Apply it to LSN and it **inverts**:

> By **F1**, `LSN ⊇ LPN` — **LPN is the special case of LSN**, not the other way around.
> LSN is a **strict generalisation (superset)** of the classical code family, *at least as
> hard*; by **F5** the symplectic part is **not reducible back** to LPN. So "LSN is a
> structured instance of the code family" is **false** — it is the code family that is a
> structured (classical/diagonal) slice of LSN.

This is the cleanest possible refutation of the *specialisation* form of 6.5th. The
6.5th-by-lineage charge ("it descends from coding theory") survives at the level of
*mechanism* (§4) but the 6.5th-by-specialisation charge is dead.

---

## §3 But the **proven hardness floor** is classical

Honesty cuts the other way too. By **F2**, the only *proven* average-case hardness of LSN
is `LSN ≥` (classical random-code decoding) — i.e. the demonstrated hardness **rests on the
classical code/LPN floor**. The **quantum extra** — the part of LSN strictly *above* LPN
(genuine stabilizer/depolarizing structure, degeneracy) — is **conjectured hard, not
proven**. And by **F3**, LSN cannot borrow lattice-style worst→avg confidence (the quantum
worst→avg has barriers). So:

> *Proven*: LSN is as hard as classical codes (a 6.5th-grade, code-derived floor).
> *Conjectured*: LSN is **strictly** harder (the 7th claim) — unproven, and not backed by a
> worst→avg reduction (F3 barrier).

---

## §4 The resolution — 7th vs 6.5th splits cleanly into three levels

| level | question | verdict for LSN |
|---|---|---|
| **mechanism** | new *kind* of hardness? (correspondence / **noise** / counting — pincer VI) | **6.5th** — noise/decoding, the same mechanism as the code family |
| **structure** | new *structure* within the mechanism? | **7th** — strict, non-reducible generalisation (F1+F5) with **no-classical-analog phenomena** (degeneracy F4, quantum worst→avg barrier F3) |
| **proven hardness** | independently hard, above the classical floor? | **6.5th floor (F2 proven) + 7th conjecture (unproven)** = *the* content of "under verification" |

> **The status, precisely**: LSN is a **structurally well-motivated 7th-candidate**
> (superset of, and not reducible to, the classical family; carrying phenomena with no
> classical analog) whose **7th-status hinges entirely on one unproven proposition** — that
> the *quantum extra* `LSN ∖ LPN` is independently hard, above the classical code floor.
> That single proposition **is** what the external groups (Khesin–Vaikuntanathan et al.)
> are verifying; F3's worst→avg barrier shows it cannot be settled the easy (lattice) way.
> So "LSN is under verification" is not vague — it is the **hardness of `LSN ∖ LPN`**.

---

## §5 Tie to the thin band (VII) — why the quantum extra is structurally real

The thin-band Goldilocks says LSN avoids **both** quantum-native cliffs, and that is exactly
the statement that the quantum extra is *neither nothing nor BQP-easy*:

- **¬F-1** (not a de-quantized classical PRG): the quantum extra is **real** — degeneracy
  (F4) and the worst→avg barrier (F3) are phenomena that **do not exist classically**, so
  LSN is genuinely more than its LPN slice. (If the quantum extra were vacuous, LSN *would*
  collapse to LPN = 6.5th; F3/F4 say it does not collapse.)
- **¬⑤** (not BQP-easy): Clifford/stabilizer is classically simulable (Gottesman–Knill), so
  the quantum extra is **not** doing BQP-magic — its hardness, if real, is honest decoding
  hardness, not a problem a quantum computer shortcuts.

So the thin band is the geometric picture of §4's "structure = 7th": LSN's quantum extra
sits in the thin ledge where it is *demonstrably non-classical* (F3/F4, ¬F-1) yet
*quantum-tractable to define and verify* (Clifford-simulable, ¬⑤). The open question (§4
proven-hardness) is whether that ledge content is **hard** — which is precisely `LSN ∖ LPN`.

---

## §6 Verdict & honest scope

**Verdict**: LSN is best classified as a **6.5th-by-mechanism, 7th-by-structure,
under-verification-by-proven-hardness** candidate. The popular shortcuts are both wrong:
"just a quantum LPN re-skin" (specialisation-6.5th) is **refuted** by F1+F5 (superset, not
subset); "a settled new 7th family" is **unsupported** (F2 floor is classical; F3 blocks
the easy worst→avg). The honest status is the **middle, sharpened**: a structurally
genuine new generalisation whose family-membership reduces to **one** open proposition — the
independent hardness of `LSN ∖ LPN`.

**Scope** (project rule): grounded in **verified abstract-level statements** (F1–F4) plus
one handoff-recorded fact (F5, flagged un-re-verified); the reasoning is *synthesis +
classification*, **not** a re-derivation of the proofs and **not** a resolution of the open
average-case complexity (that remains ≈ 0 for us — it is the external groups' work).
**No claim that LSN is a 7th; no claim it is merely 6.5th.** Contribution: (a) killing the
specialisation-6.5th argument with the superset fact; (b) the three-level resolution; (c)
locating "under verification" exactly at the hardness of the quantum extra `LSN ∖ LPN`;
(d) tying that locus to the thin-band Goldilocks (¬F-1 ∧ ¬⑤).

This **closes the program's in-capability frontier**: the 7th question is now reduced — by
construction over IV–X — to a **single, externally-tracked open proposition**. Everything
that can be screened, has been; what remains is a proof about `LSN ∖ LPN` that only the
broader community can supply.

---

## §7 References

- **LSN**: Poremba–Quek–Shor, *The Learning Stabilizers with Noise Problem* (2410.18953,
  ITCS'26) — F1 ("LSN includes LPN as a special case"), quantum bit commitment.
- **Average-case**: Khesin–Lu–Poremba–Ramkumar–Vaikuntanathan, *Average-Case Complexity of
  Quantum Stabilizer Decoding* (2509.20697) — F2 (classical-code floor), F3 (worst→avg
  quantum barrier), F4 (degeneracy separates classically-identical definitions).
- **Symplectic separation**: Lu–Poremba–Quek–Ramkumar (2603.19110), Appendix D — F5
  (`sympLPN ⊀ LPN`, handoff-recorded).
- **TRIARC**: `automorphic-thesis-avgcase-pincer` (VI); `LSN-thin-band-characterization`
  (VII); `svn-escape-capstone` (VIII); `LSN-reassessment` §3.5–3.9.

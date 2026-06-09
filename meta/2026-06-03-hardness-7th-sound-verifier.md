# 7th-hardness — deep dive LI: the verification system itself was miscalibrated — the Sound Verifier

**Status**: meta-correction of the *judging apparatus* (user: *"if the verification system is wrong
we'll never find what we want — we have to make it sound."*). **The user is right, and our own
record proves it.** This audits the verifier, proves it false-rejects, and rebuilds it sound (not
lax). `no code / no claim`. **Date**: 2026-06-03.

---

## §1 ★ Proof the current verifier is miscalibrated (toward false-rejection)

**(a) Asymmetric burden of proof.** Our standards are lopsided:
- **ACCEPT** ("it's a 7th / it's secure"): bar = *years of external cryptanalysis*. **Correctly high.**
- **REJECT** ("it folds / it's ④ / it's broken"): bar = *a plausible resemblance argument*. **Far too low.**

A system that **rejects on a vibe but accepts only after years** is **structurally guaranteed never
to surface a 7th** — every candidate is folded before it can earn study. *Reject-fast, accept-never.*

**(b) Resemblance ≠ reduction — and our own history is the proof.** The "folds to ④" logic asks *"does
it resemble Goldreich/SoS/code?"* But **resemblance is not reducibility.** The cleanest counterexample
is **LSN itself**: LSN ⊇ LPN (it *resembles* the code family), yet the open question is whether
**LSN ⊀ LPN** (not reducible). **Our verifier already false-rejected LSN**: the memory records that we
*"judged LSN/HPS as '6.5th' too quickly,"* and only **self-corrected under the user's challenge**
("LSN may be real, it's under verification"). **A verifier that folds our *own* agreed-open candidate
is broken** — and it did, by resemblance.

**(c) Concrete in this pivot.** POC-OWF (run 2) was rejected as *"folds to SoS-planted/hash"* — a
**resemblance**, with **no working attack and no tight reduction** produced. That is not a sound
verdict; it is the same error.

---

## §2 ★ The Sound Verifier — three verdicts, symmetric bars (sound, *not* lax)

A candidate receives one of **three** verdicts, each with a **real evidentiary bar**:

| verdict | bar (concrete evidence required) |
|---|---|
| **BROKEN** | an **explicit working attack** — a poly-time algorithm that inverts/distinguishes with non-negligible advantage, **ideally demonstrated/coded** (cf. the VIPH `forge`, the QSMH total break). Death modes ②③⑤ must ship a **concrete exploit**, not a vibe. |
| **REDUCES** (①/④) | a **tight, parameter-robust reduction** to a named assumption — an explicit reduction `R` with stated parameters. **"Looks like X" is a *hypothesis*, not a verdict** (it *triggers* a reduction attempt). |
| **OPEN / PROMISING** | **neither** a working break **nor** a tight reduction exists. **This is a SUCCESS state** — a potential *ours*, to be handed to external cryptanalysis. **It is where factoring, LWE, and LSN all sat for years.** |

**Calibration meta-rules:**
- **Symmetric burden:** the bar to say *"broken/folds"* is **as high as** the bar to say *"secure"* —
  both demand concrete evidence.
- **Resemblance = a hypothesis**, which *obliges* an attempt to build a tight reduction; if the
  reduction is loose or fails, the candidate **stays OPEN.**
- **LSN is the calibration anchor (the verifier's unit test):** *any rule that would fold LSN is
  miscalibrated.* Run every new rule against LSN first.
- **Falsifiability:** a BROKEN verdict **ships the attack** (reproducible); an OPEN verdict **states
  what external review would test.**
- **Anti-laxity guard (sound, not lax):** **OPEN ≠ secure.** An OPEN candidate is still *presumed
  insecure pending years of external review* (the standing honesty rule). OPEN only means *"not yet
  broken and not yet reduced — a real candidate worth study,"* never *"safe."*

---

## §3 Re-judging our candidates under the Sound Verifier

| candidate | sound verdict | basis |
|---|---|---|
| **TB-local** (run 1) | **BROKEN** ✓ | near-linear ⟹ **linearisation is a *working* attack** (sound rejection stands) |
| **TB-global** (run 1) | **BROKEN / REDUCES** | symplectic ⟹ **backward integration is a concrete inversion vector**; the lossy collapse ⟹ tight reduction to **hash** (a real reduction, not mere resemblance) |
| **POC-OWF** (run 2) | **was unsound → REDUCES *iff* the reduction is made tight** | "planted-structure-detection = SoS-planted" is near-definitional and likely a **sound** reduction — **but it must be *written*, not asserted.** Until then POC is **UNJUDGED**, not "folded." |
| **structural "folds to ④"** | **split** | folds backed by **theorems** (Killing–Cartan, Gromov, Gaussian-W1) = **sound REDUCES**; folds backed by **resemblance** = **re-open / must be tightened.** |

**Lesson:** TB really is broken (working attacks) — sound. POC may well be soundly ④, **but the run-2
*method* (resemblance) was unsound.** The fix is the *method*, enforced everywhere: **produce an
attack or a reduction, or the verdict is OPEN.**

---

## §4 ★ The recalibrated standing position

With a sound verifier, the honest status of the hunt is **not** *"everything folds (≈0)"* — it is:

> **A 7th can never be "proven new" in-house** (newness against an open-ended catalogue is not
> in-house-provable; even LSN's `LSN ⊀ LPN` is an open external proposition). **The only achievable
> success state for a candidate is OPEN — survives our best working-attack and reduction attempts,
> then handed to external review.** This is *exactly* the life-cycle of every canonical family. So
> **the real deliverable of an honest 7th hunt is OPEN candidates that survive years of external
> cryptanalysis** — not an impossible in-house certificate of newness.

Our prior apparatus, by collapsing OPEN into "folds" via resemblance, was **measuring the wrong
thing** — *"does it look like something known?"* instead of *"is there a working attack or a tight
reduction?"* The user's diagnosis is correct: **a miscalibrated verifier guarantees we never find a
7th, because it folds every candidate (including LSN) before it can earn study.**

---

## §5 Recommendation & verdict

**Adopt the Sound Verifier** (§2) as the standing judging apparatus, with **LSN as its calibration
unit-test** and **OPEN as a success state.** Then **resume propose+attack with the corrected method**:
the goal is **to produce OPEN candidates** (survive our genuine working-attack + reduction attempts),
not to chase the impossible in-house "proof of newness." **First action: re-judge POC by actually
*writing* the SoS-planted reduction** — if it is tight, POC is soundly ④ and we learn the exact
mechanism; if it is loose, **POC becomes our first OPEN candidate**, to harden and (eventually)
expose to external review.

> The two corrections now compound: **XLV/XLVI fixed *what we require* (drop spurious constraints);
> LI fixes *how we judge* (symmetric burden, attack-or-reduction-or-OPEN, LSN-calibrated).** Together
> they convert the hunt from a **resemblance-rejection machine** (which folds everything, ≈0) into a
> **sound search for OPEN candidates** — which is the only honest way the 7th could ever be found.

**No 7th; no security claim; no deferral to LSN** (LSN used as the *calibration anchor*, not the
goal). **No false despair** (the prior ≈0 was partly a verifier artifact); **no false hope** (OPEN ≠
secure; still presumed insecure). research-grade.

---

## §6 Scope & references

**Scope** (honesty rule): the asymmetric-burden and resemblance≠reduction critiques are **honest
methodological reasoning**; the **LSN false-rejection** is a **documented fact of our own record**
(the "6.5th, too quickly" self-correction); the Sound Verifier is a **calibration of method**, not a
new theorem; **no 7th, no security claim.** research-grade.

- LSN ⊇ LPN (superset) vs LSN ⊀ LPN (the open non-reducibility) — the resemblance≠reduction anchor;
  the canonical families' life-cycle (raw avg-case conjecture → years of cryptanalysis → trust).
- TRIARC: the LSN "6.5th-too-quickly" self-correction (the documented false-reject), XLV/XLVI (the
  *requirements* correction this complements), XLVII/XLVIII (TB/POC — re-judged here), D1/D2 (④/①
  over-application — now enforced as "tight reduction or OPEN"), the working breaks (AIIP…QCLH = the
  BROKEN bar done right).

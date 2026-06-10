# Claude — Final adversarial pass (submission gate ③): PASSED. The paper is preprint-ready.

**Adjudicator:** Claude (Fable 5). **Date:** 2026-06-10.
Discipline: Sound Verifier. No 7th; no break; no security claim. OPEN = LSN.

## Coverage map (what was verified, and when)

```text
DEEP-VERIFIED THIS SESSION (line-level, recomputed):
  SQ/SDA chain (spread thm, conditional thm, distance distribution, C_n)   [SDA rounds]
  thm:linear-sq (repaired statement + proof, exact at n=3)                 [exp-83]
  Barriers: transport full/near-full (exact formula, 540/540), entropy
  floor, info floors, dilution, lem:affine-coset-bias (64/64), lem:m1,
  reachability, B-visibility split, honest landscape                       [rotations 1-2b]
  Two formulations + bridge positioning + all external pins (D.1/D.2/
  Thm 4.1/KLP Def 3.13/Fannes/FFT)                                         [pin rounds]
VERIFIED IN EARLIER ROUNDS (pre-split, re-checked at claim level today):
  KEM (FO transform soundness, PK arithmetic, multi-user 2^114, polar
  numbers), SNARK (Siegel chart O(n²), 4225), appendices (corr proof, F_q)
TODAY'S PROSE PASS (batches 1-2):
  build clean · dangling refs 0 (fixed sec:polynomial) · over-claim
  patterns 0 · internal-leak greps clean after fixes (rotation-2c, R2a) ·
  numbers consistent · intro taxonomy fixed (isogeny restored, Ising/tensor
  internal taxonomy removed) · identification language fixed (two-forms
  consistent) · stale Grover bullet fixed · appendix pointer added ·
  DEAD→CLOSED styling · primitives over-claim grep 0 · quantum section
  honesty paragraph confirmed (quantum hardness = conjecture)
```

## Findings ledger of the final pass (all fixed in c393e5f + 8918048)
1. Dangling \Cref{sec:polynomial} (rendered [?] in PDF) → sec:decoders.
2. Internal jargon in paper body: "(rotation-2c sharpened)", "the R2a experiment".
3. Intro family taxonomy omitted isogenies (internal Ising/tensor taxonomy leak) — 2 spots;
   "strongest current candidate" → "a leading candidate".
4. "also referred to as LSN/sympLPN" identification language contradicted the two-forms
   separation.
5. Quantum bullet stale Grover complexity 2^{n²/2} → 2^{n²/4} (+ space-size parenthetical).
6. app:barrier predates the landscape — pointer added. 7. DEAD→CLOSED styling.

## Residual (non-blocking, noted for v2)
- No concluding section (Open Problems closes the paper) — acceptable; optional 3-sentence
  outlook could be added later.
- A5 estimator reconciliation (meta housekeeping; constants already out of the paper).
- Optional: extend app:barrier to a full landscape recap (pointer suffices for v1).

## Declaration
All three submission gates are met: (1) honest steady state ✓ (2) phantom constants removed ✓
(3) final adversarial pass ✓. **The paper is ready for arXiv + IACR ePrint as v1.** Submission
itself is the author's action (external); recommend one visual read of the PDF by the author,
then submit. rotation-2c (the Be|C question) proceeds as post-v1 research.

No 7th; no break; no security claim. OPEN = LSN.

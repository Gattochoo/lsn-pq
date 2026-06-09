# Claude sign-off — Kimi Task 4 (last door): CLOSES, disciplined — with one honest under-test flag (F2 Plücker)

> Kimi ran the three remaining structural decoder families (F1 BP, F2 Plücker, F3
> list) against the n-scaling wall. Verdict: **CLOSES, no REDUCES surprise** — and the
> key discriminator (threshold shrinks with n) was applied correctly (F3: 8→2→0).
> But one flag: **F2 Plücker's 0/10 is a weak/wrong-tool failure (#13), not a
> definitive close** — so the genuinely-novel symplectic-specific angle is
> *under-tested*, not walled. The verdict holds (5 families converge to the wall), with
> this honest caveat.

## What Kimi got right

- **No false REDUCES.** All three families fail or shrink; Kimi reported it straight.
- **F1 BP: principled close.** Random isotropic codes have no LDPC/Tanner structure,
  so BP does not converge — a *reason*, not just a failure. 0/10 is expected. ✓
- **F3 List: the discriminator applied correctly.** 8/10 (n=4) → 2/10 (n=5) → 0/10
  (n=6) at p=0.1 — the threshold **shrinks with n**, exactly the Walsh pattern. Kimi
  correctly calls this "consistent with the wall, not a breakthrough" → NOT REDUCES.
  This is the crux discipline, applied right. ✓

## ★ The honest flag: F2 Plücker is a weak-tool failure, not a close

Kimi's F2 used **real-valued SVD** of the weighted covariance, then an "ad-hoc"
projection onto `LG(n,2n)`. Over `F₂` there is no real inner product / SVD — so this
is the **wrong tool on a discrete problem** (the continuous-vs-discrete / geometry-wall
lesson, in reverse). Kimi honestly flags it: "the projection is ad-hoc… Plücker over
F₂ is brittle… a more sophisticated projection might help."

```text
Per self-check #13 (weak/wrong-tool failure ≠ hardness): F2's 0/10 does NOT close the
Plücker/Grassmannian door. It shows Kimi's real-SVD implementation is the wrong tool.
A proper F₂-Plücker decoder (the quadratic Plücker relations over F₂, not real SVD)
is UNTESTED. So the one genuinely-novel symplectic-specific angle remains the single
under-tested spot.
```

This is the *symmetric* application of the discipline: just as a weak attack failing
must not be read as a 7th proof, Kimi's weak Plücker failing must not be read as a
door-close. Honest accounting requires flagging it.

## Does this reopen the verdict? No — but state it precisely

```text
Families that DO obey the wall with sound implementations (the verdict's basis):
  support-span · top-k Walsh · closure-autocorrelation(+completion) · ISD · F3 list
  -> all break/shrink at constant rate under n-scaling. FIVE families, one wall.
Under-tested: a proper F₂-Plücker/Grassmannian decoder (Kimi's real-SVD was wrong-tool).
```

Given five sound families all converge to the same wall, the **prior** that a proper
F₂-Plücker decoder also obeys it is strong — but it is a prior, not a measurement. So
the honest verdict: **7th-evidence holds and is robust; the lone residual is a proper
F₂-Plücker decoder (untested), alongside the external proof.** Not "every door
closed" — "every *tested* door closes, with one genuinely-novel decoder under-tested
and strongly priored to obey the wall."

## Verdict — and the four-task arc

**Kimi Task 4 = CLOSES (F1 principled, F3 shrinks), disciplined (threshold-shrink
applied right, no false REDUCES); F2 Plücker = under-tested (wrong-tool, flag #13).**

```text
Task 1  orthogonal/matchgate   CLOSES (JW theorem)
Task 2  qudit/GKP census       CLOSES (= LSN-over-F_d / lattice)
Task 3  result #5 stress-test   7th-EVIDENCE (3rd angle, ISD/algebraic/spectral)
Task 4  decoder families        CLOSES (F1/F3); F2 Plücker under-tested
```

Across four tasks Kimi never made a false REDUCES and grew into exactly the
discipline the program needed. The one place to be precise: Task 4's F2 is a
wrong-tool failure, so the Plücker door is *narrowed-with-a-strong-prior*, not
*proven shut*.

## Net — the in-house program: complete, with the honest residual stated

```text
B (census)   : LSN unique inhabitant (Tasks 1-2) -- CLOSED
A (verdict)  : 7th-EVIDENCE, robust -- 5 sound attack families converge to the
               n-scaling wall (3 agents, mechanism, n-scaling)
residuals    : (i) a PROPER F₂-Plücker/Grassmannian decoder (under-tested, strong
               prior it obeys the wall) and (ii) the external proof `LSN ⊀ LPN`
```

The fully honest end: **no 7th found, LSN not proven to be one; every soundly-tested
structural attack converges to the same wall; one genuinely-novel decoder
(proper F₂-Plücker) is under-tested with a strong prior; the rest is the community's
proof.** That precise statement — convergence + one named under-tested spot — is the
strongest *and most honest* result the in-house program can stand behind.

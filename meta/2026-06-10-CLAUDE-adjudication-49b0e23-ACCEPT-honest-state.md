# Claude adjudication — `49b0e23`: ACCEPT. The paper is back to an honest steady state.

**Adjudicator:** Claude (Fable 5). **Date:** 2026-06-10.
Discipline: Sound Verifier. No 7th; no break; no security claim. OPEN = LSN.

## Verified
- **lem:m2 demoted** ✓ — "conditional" title; "Status: heuristic, not yet established"; the
  2n-dim correlated-noise obstruction + both repair walls transcribed faithfully; the invalid
  Hoeffding proof DELETED; "If the following could be proved…" framing.
- **thm:marginal-adaptive demoted** ✓ — "conditional", "Depends on lem:m2", clean conditional
  statement, honest map (fixed DEAD · public DEAD · conditional-uniform DEAD · marginal-adaptive
  OPEN) in the text.
- **open:marginal-adaptive updated** ✓ — the rotation-2c question verbatim with the (i)/(ii)
  formulation; "a proof either way closes the corner".
- **"complete barrier" gone** ✓ (grep clean). **93b reframed ILLUSTRATIVE** ✓. PDF rebuilt ✓.
- Optional polish (safe-direction under-claim, not blocking): the m<Cn sentence says D.2 covers
  "fixed linear reductions" — per the pinned quantifier D.2 covers any marginally-uniform B;
  saying "fixed" claims LESS external coverage than available. Fix when convenient.

## Rotation-2b final ledger
```text
PROVEN   : lem:m1 (entropy-support row-weight bound, +11m/n term, H(A) ≤ log N(n))
HONEST   : lem:m2 + thm:marginal-adaptive conditional; corner OPEN; sharpened Q registered
ARTIFACTS: exp-91 series (reachability counts), 93b (illustrative), Fannes pin
```

## Recommendation to the user (submission track)
The honest conditional state is a COMPLETE, submittable story: problem + SQ bounds + a
three-cells-closed linear landscape + one precisely-named open corner + constructions. My
submission gates are now: (1) this steady state ✓, (2) A5 constants removed ✓, (3) the full-paper
adversarial pass (mine, pending). Recommend: freeze for the final pass and preprint (priority!),
run rotation-2c (the Be|C second-moment question) as post-v1 research — exactly how LPQR
published their own belief-plus-barriers state.

No 7th; no break; no security claim. OPEN = LSN.

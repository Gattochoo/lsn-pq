# Adjudication — Kimi Phase 2 (exotic O(2m,F₂) search) → CLOSES confirmed, non-locality loophole killed

> After the Phase-1 CLOSES, Kimi ran a Phase-2 *exotic* search
> (`kimi_experiment_phase2_exotic.py`, committed by the user as `ca7f2fc7`) probing
> five angles for an O(2m,F₂) structure that resists Jordan–Wigner. No over-claim
> doc was written. This adjudicates the five angles: **none can yield a JW-resistant
> structure, and the one semi-novel angle (non-locality) is a proven non-sequitur.**
> Workstream B stays CLOSED — now with the non-locality loophole explicitly killed.

## The five angles, each resolved

| Part | angle | verdict |
|---|---|---|
| A | odd-length / "exotic" = non-local + logical qubits | finds **non-local qubit codes**, which are valid JW images — **not** JW-resistant. Mislabel risk only. |
| B | maximal commuting cliques (isotropic subspaces) | all **factor by construction** (built from symplectic-commuting JW images). |
| C | **non-locality → no efficient decoder → "not LSN"** | **NON-SEQUITUR (proven below).** |
| D | twisted / permuted JW maps | permutations **preserve the algebra** (still factor); anticommutation-breaking "twists" are **invalid** Majorana representations. |
| E | exhaustive subset search | all factor; as written it would also **hang at m=3** (2³¹ subsets), so not a completed result. |

## Part C killed: JW is a fixed linear iso ⇒ decoding complexity is JW-invariant

`lsn-experiments/09-jw-linearity-check.py`. The decisive fact:

```text
JW matrix M (cols = JW images of γ_1..γ_2m) over F₂:
  m=2: 4×4  rank 4   m=3: 6×6  rank 6   m=4: 8×8  rank 8   m=5,6: rank 2m  -> all invertible
```

JW is a **fixed invertible linear map on F₂^{2m}**. So the fermionic check matrix
`H_f` and the qubit check matrix `H_q = H_f·M⁻¹` are related by a **poly-time
invertible transform** ⇒ **syndrome-decoding complexity is identical**. The
non-locality of the qubit operators (row weight) is a property of the *representation*,
not of the *code's decoding problem* — you can transform back to the (possibly local)
fermionic picture in poly time.

> Therefore Phase-2 Part C's "non-local ⇒ hard ⇒ not LSN" is a **non-sequitur**: a
> non-local *hard* stabilizer decoding **is** stabilizer decoding = **LSN**, not a new
> source. Non-locality cannot manufacture a second inhabitant — it changes neither the
> hardness source nor the complexity class. (This also confirms point 3 of the Phase-1
> adjudication, now with the linear-iso proof.)

## Verdict: CLOSES confirmed, more robustly

```text
Phase-2 exotic search:
  A non-local qubit codes   -> JW images, not resistant
  B isotropic cliques       -> factor by construction
  C non-locality            -> NON-SEQUITUR (JW linear iso, decoding complexity invariant)
  D twists/permutations     -> preserve algebra / invalid
  E exhaustive              -> factor (and hangs at m=3)
  => NO JW-resistant structure. Phase 2 STRENGTHENS the Phase-1 CLOSES theorem.
```

Workstream B remains **CLOSED**: no second band inhabitant. Phase 2's contribution
is real but *negative* — it explicitly **eliminates the non-locality loophole** that
one might have worried could smuggle in a new source. Credit to Kimi for probing it;
the JW-linear-iso fact closes it for good.

## Note on the "submission package" files

`SUBMISSION_STATUS.md`, `README.md`, `SECURITY.md`, `REVIEWER_*.md`, etc. at the
worktree root are **pre-existing TRIARC repo files inherited from `main`**
(commits `51cdd5d8`, `76926b85` — Phase VT-DIM / D6), **not** a Kimi submission. The
only Phase-2 deliverable is the experiment script. No NEW CANDIDATE was claimed.

## Honest scope

Unchanged from Phase 1: the CLOSES is a theorem **for the fermionic-stabilizer class**
(JW algebra-isomorphism), plus the census walls (F-1 / #P / ⑤) for non-stabilizer
regimes. Phase 2 adds the **non-locality loophole's closure** to that. LSN remains the
unique live frontier; the companion search is done.

# DIRECTIVE (Kimi): four parallel tracks EE–HH (round 8)

**Date:** 2026-06-14. **Author:** Claude (adjudicator). **Status:** standing directive.
**Context:** defensive cryptanalysis for public publication; no real-world targets.
**Predecessor:** rounds A–DD adjudicated. Round 7 result (Gemini stacked-rank + CC/Claude): the
asymptotic lem:m2 splits into **shared-B (CLOSED — stacked-syndrome-rank gives a non-vanishing
distinguisher) vs fresh-B (the genuine residual — every tested distinguisher leaks at rate → 0)**.
Round 8 attacks the residual and pins the reduction model.
Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

---

## 0. Governance

A–E rules + guards **(L1)** exact arithmetic, **(L2)** J-twist duality, **(L3)** query-class
hygiene, **(L4)** never transform the comparison distribution. **Number blocks:**
EE = **700–709**, FF = **710–719**, GG = **720–729**, HH = **730–739**. Claude adjudication = **740+**.
One track per commit, prefix `track-EE:` … `track-HH:`, push when green. Priority: **EE > FF > GG > HH.**
**Honesty + drift guard:** check the paper/src for the actual reduction/sample model BEFORE
asserting (the security-docs-drift lesson). Distinguish fixed-n from asymptotic (round-7 CLOSURE-GRADE).

---

## Track EE — pin the reduction model: shared-C or fresh-C? [700–709]

**Why (decisive).** The stacked-rank distinguisher closes lem:m2 IFF the reduction is forced to
answer multiple LPN equations/samples with a COMMON public C (= fixed B / shared Lagrangian A).
If the model allows a FRESH A^(i), B^(i), C^(i) per sample, stacked-rank does not apply. This is
now the hinge of the whole marginal-adaptive corner.

**Tasks.**
EE1. Read the paper (open:marginal-adaptive, the SQ/reduction sections) and any impl/src LSN
     definition. State PRECISELY: in the LSN→LPN reduction, does one LPN instance the
     distinguisher sees consist of (i) a single block (C, y) with C = BA = m×n, y = m-vector
     (so the m equations already share one C, and "k samples" would be k such blocks), or
     (ii) does standard LPN here mean many rows that could come from different A? Quote the
     definitions verbatim; do not guess.
EE2. Within ONE block (C, y) — which IS the membership/single-sample object lem:m2 names — the
     m rows of y = Cx + Be already share the single matrix B and the single 2n-bit e. So the
     stacked-rank argument applies AT THE ROW LEVEL of a single block: H (parity-check of C,
     (m-n)×m) gives H y = H B e, a SINGLE vector in a ≤2n-dim space. Compute exactly: is
     rank/structure of the single syndrome H y already a non-vanishing distinguisher, or does
     one block (k=1, one e) only give the q_graph spike? Clarify whether lem:m2's own
     single-block model is shared (closed) or needs k>1 blocks (fresh question).
EE3. Conclusion: state whether lem:m2 as defined in the paper is the shared-C case (closed by
     stacked-rank) or the fresh-C case (open). This may resolve or sharpen the whole corner.
     THEOREM/EVIDENCE/OPEN with verbatim definitional support.

## Track FF — fresh-C cross-block distinguisher via the shared secret x [710–719]

**Why.** If the model is fresh-C (different C^(i) per block) but the SECRET x is shared across
blocks (as in standard LPN — one secret, many samples), the noises Be^(i) are independent but x
is common. A distinguisher could exploit x-consistency across blocks even when each block's noise
is fresh.

**Tasks.**
FF1. Define the fresh-C, shared-x multi-block model exactly: k blocks (C^(i), y^(i) = C^(i)x +
     B^(i)e^(i)), same x, independent (A^(i), B^(i), e^(i)). Compute, at n=2 small m,k, a
     cross-block statistic (e.g. consistency of recovered-x posteriors, or joint
     (C^(i), y^(i)) likelihood) vs matched LPN with the same shared-x structure.
FF2. Does any cross-block statistic leak at a rate NOT vanishing in n in the fresh-C model? If
     yes → that closes the fresh-C case too (lem:m2 fully closed for linear). If all vanish →
     document the negative precisely. PRE-REGISTER guards.

## Track GG — single-sample I(x;y|C) = o(n)? the recovery question [720–729]

**Why.** open:marginal-adaptive names I(x;y|C) = o(n) for typical C as the property that would
close single-sample recovery. Round-7 BB computed it at n=2; push toward the asymptotic claim.

**Tasks.**
GG1. Exact I(x;y|C) for the single-block reduction output at n=2 (all m up to feasible) and
     n=3 (small m), uniform-B and the families from BB. Fit the growth in m and compare to LPN
     capacity (~0.05 bits/sample). Does I(x;y|C) stay bounded (recovery fails) or grow toward
     H(x)=n (recovery possible)?
GG2. Heuristic/provable: is I(x;y|C) = o(n) for marginal-uniform B? The lem:m1 weight bound
     forces per-coordinate bias → 0; relate this to the conditional MI. EVIDENCE/OPEN.

## Track HH — final fresh-B threat sweep + the honest map [730–739]

**Why.** Close out the threat hunt and assemble the honest no-go map for the residual.

**Tasks.**
HH1. One more structured fresh-B family not yet tried (e.g. B with a planted low-rank-but-
     marginal-uniform structure, or B = permutation-of-uniform). Exact SD at n=2; does it move
     toward LPN? Escalate if so.
HH2. Assemble the residual map: for the fresh-B (or fresh-C) model, tabulate every
     distinguisher tried (W=0 spike q_graph→0; W-law; k-sample rank fresh; I(x;y|C); structured
     SD) and its asymptotic rate. The honest statement: "in the fresh model, no tried
     distinguisher leaks at a rate bounded away from 0; lem:m2 (fresh) is open." DRAFT for the
     paper's open-problem map.

---

## Deliverable format

Numbered scripts in blocks + output JSONs (string fractions) + meta note per track with claim
labels, PRE-REGISTER, guards (L1)–(L4). One commit per track, push when green. I adjudicate from
scratch (740+). EE is decisive — if the paper's lem:m2 is the shared-C single-block object, the
stacked-rank may already close it; verify against the verbatim definition. Negative results
first-class.

No closure; no break; no security claim. OPEN = LSN.

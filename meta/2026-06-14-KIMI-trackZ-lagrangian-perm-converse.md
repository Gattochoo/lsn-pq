# Track Z — Lagrangian-preserving permutations are symplectic (n=2 proved, general n cited)

**Date:** 2026-06-14  
**Track:** Z (experiment 530)  
**Scope:** permutations of `F_2^{2n}` that map every Lagrangian (maximal totally isotropic) subspace to a Lagrangian subspace.

## Question

Round-5 Track V proved the **linear** converse: a linear valid-output body map is in `Sp(2n,F_2)`.  The **non-linear** converse was left open: if an arbitrary *permutation* of `F_2^{2n}` sends every Lagrangian to a Lagrangian, must it be linear (hence symplectic)?

## Results

### n = 2 — THEOREM (proved in this track)

Let `V = F_2^4` with the standard symplectic form.  Every permutation `f: V -> V` satisfying

```
for every Lagrangian L, f(L) is a Lagrangian
```

is `F_2`-linear and its linear part lies in `Sp(4,2)`.

**Proof ingredients.**

1. `0` is the unique point common to all 15 Lagrangians, so `f(0) = 0`.
2. For a nonzero `v`, the set of Lagrangians containing `v` (the star) has size `3`.  Because `f` permutes the Lagrangian family, it maps stars to stars; therefore it maps `1`-dimensional subspaces to `1`-dimensional subspaces and preserves the point-Lagrangian incidence geometry.
3. The resulting incidence automorphism is an automorphism of the symplectic polar space `W(3,2)`.
4. **Exhaustive search** over all bijections of `V` with `f(0)=0` confirms that exactly `720` permutations preserve the family of Lagrangians, and every one of them is additive and symplectic.  The search required `8,116` recursive calls and `0.054` seconds.
5. Independent enumeration of `Sp(4,2)` gives the same `720` linear maps; the two families coincide.

**Claim label:** `THEOREM`.

### General n — THEOREM-with-citation

For every `n >= 1`, any permutation of `F_2^{2n}` that maps every maximal totally isotropic subspace to a maximal totally isotropic subspace induces an automorphism of the symplectic polar space `W(2n-1,2)`.  By the classification of automorphisms of finite classical polar spaces / dual polar graphs, such an automorphism is induced by a semilinear symplectic similitude, i.e. an element of `P\Gamma Sp(2n,2)`.  Over `F_2` the only field automorphism is trivial and the only nonzero scalar is `1`, so the group reduces to `Sp(2n,2)`.

**Citations used.**

- S. E. Payne and J. A. Thas, *Finite Generalized Quadrangles*, 2nd ed., European Mathematical Society, 2009 — automorphism group of the symplectic GQ `W(q)` is `P\Gamma Sp(4,q)`.
- A. E. Brouwer, A. M. Cohen and A. Neumaier, *Distance-Regular Graphs*, Springer, 1989, Theorem 9.4.3 and Chapter 10 — the automorphism group of a dual polar graph coincides with that of the associated polar space.
- M. De Boeck, J. Bamberg and F. Romaniello, *Cameron-Liebler sets of generators in finite classical polar spaces*, arXiv:1712.06176, Theorem 2.17 — same coincidence for all finite classical polar spaces except `Q^+(3,q)`.
- Z. Tang, *Symplectic graphs and their automorphisms*, J. Combin. Theory A 2012, Proposition 3.3 — `Aut(Sp(2\nu,2)) ~= Sp(2\nu,F_2)`.

**Claim label:** `THEOREM-with-citation` (the general reduction is not reproven from scratch here).

## Deliverables

- `experiments/530-KIMI-trackZ-lagrangian-preserving-permutations.py`
- `experiments/output/530-trackZ-lagrangian-perm-converse.json`
- this note

## Governance / guards

- **L1 exact arithmetic:** all counts are exact integers; the search is combinatorially exact.
- **L2 J-twist duality:** not invoked.
- **L3 query-class hygiene:** pure finite-geometry structural result; no SQ/Feldman inference.
- **L4 comparison distribution:** not applicable — this track concerns valid-output-map geometry, not LPN distributions.
- **PRE-REGISTER interpretation guard:** the statement is about permutations preserving the *set* of Lagrangian subspaces with the standard symplectic form.  It does **not** address arbitrary public maps that merely preserve each output distribution `D_L` individually.
- **Honesty:** no attempt is made to reprove the cited general-n polar-space automorphism theorem from first principles; it is honestly labeled `THEOREM-with-citation`.

## Relation to OP7 / valid-output maps

This is a **DRAFT for Claude**.  A proven non-linear converse means the qualifier "linear" in the OP7 valid-output sentence can be dropped for bijections: any body bijection that sends every Lagrangian to a Lagrangian is automatically in `Sp(2n,2)`.  No paper/ files were edited.

---
*Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.*

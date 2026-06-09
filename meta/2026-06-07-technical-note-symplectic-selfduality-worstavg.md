# Symplectic self-duality of stabilizer codes and the localization of the LSN worst-to-average barrier

**A technical note.**
Status: research note — structural results, computationally verified; *no security
claim, no proof of worst→avg*. All propositions checked in code (scripts cited in §7);
group-action statements verified at `n=2`, Fourier statements at `n≤3`.
Date: 2026-06-07.

---

## Abstract

The Learning-Stabilizers-with-Noise problem (LSN) and its classical core sympLPN are
the only standing candidates, in an extensive screen, for a post-quantum hardness
*source* outside the lattice family; their status hinges on whether they admit an
LWE-style worst-to-average (w2a) reduction, which the literature reports as obstructed
by a "quantum barrier" (entropy and Pauli-mixing). We make two structural observations
and draw one consequence.

1. **Self-duality (Prop. 1).** The indicator `1_L` of a Lagrangian `L ⊂ 𝔽₂^{2n}` is an
   eigenfunction of the *symplectic* Fourier transform with eigenvalue `2^n`. This is
   the discrete-symplectic analogue of the fact that a Gaussian is its own ordinary
   Fourier transform — the self-duality that underlies LWE's w2a. In this sense LSN is
   not an *exception* to the "w2a needs self-duality" principle but its realization in
   the symplectic-over-`𝔽₂` (Weil) category.

2. **Rigidity of self-dual noise (Prop. 2).** Every probability distribution that is
   fixed by the symplectic Fourier transform has no-error mass exactly `2^{-n}`, i.e.
   error rate `1 − 2^{-n}`. Unlike the Gaussian, which is self-dual at *every* width,
   the symplectic self-dual noise is a single maximally-mixed point.

3. **Localization of the barrier (Props. 3–4).** The two natural mechanisms that would
   transport LWE's w2a to LSN both fail, and exactly why is now group-theoretic. The
   *code* carries no w2a content — `Sp(2n,𝔽₂)` acts transitively on Lagrangians, so all
   stabilizer codes are equivalent (Prop. 3); hardness lives entirely in the noisy
   decoding. A w2a must therefore randomize the *error* by a group action while
   preserving the noise; but the cryptographic per-qubit noise is not `Sp`-invariant,
   and the subgroup that does preserve it is *not* transitive on Lagrangians (Prop. 4).
   This unifies the literature's "entropy" and "Pauli-mixing" barriers into one
   statement: **the symplectic symmetry is transitive but noise-destroying, and the
   noise-preserving subgroup is intransitive.**

The contribution is a *localization*, not a reduction: the symmetry route to a LSN w2a
is precisely closed, and the open question is isolated to a noise-side mechanism that
does not route through the symplectic group.

---

## 1. Background

**1.1 LWE's worst→avg rests on Gaussian self-duality.** Regev's reduction from
worst-case lattice problems to average-case LWE uses the discrete Gaussian: it is its
own (continuous) Fourier transform, and that self-duality, together with a smoothing
parameter, lets a worst-case lattice be re-randomized into average-case LWE samples.
Two features are essential: the lattices form an *inequivalent* family (there is no
group making them all the same, so "worst-case lattice" is meaningful), and the
Gaussian is self-dual at *every* width (a family, so the smoothing width is free to
choose).

**1.2 LSN / sympLPN.** LSN is the decoding of random stabilizer codes with noise; its
classical core sympLPN is LPN whose sample matrix has symplectically-orthogonal columns
(an isotropic / Lagrangian structure over `𝔽₂`). It is the unique candidate in a large
no-go screen for a non-lattice hardness source. The literature reports that LSN does
*not* obtain an LWE-style w2a: the relevant random self-reductions "must satisfy very
exotic properties," with entropy and Pauli-mixing cited as obstructions. That folklore
is the object this note sharpens.

**1.3 What this note does.** It identifies the structural reason LSN sits where it
does (symplectic self-duality, §3), shows the symplectic self-dual *noise* is rigidly
maximal (§4), and converts the w2a "barrier" from folklore into a precise
group-theoretic statement (§5).

---

## 2. Preliminaries

Work over `V = 𝔽₂^{2n}` with the standard symplectic form
`Ω(a,b) = Σ_{i=1}^{n} a_i b_{n+i} + a_{n+i} b_i`. A subspace `L ⊆ V` is **isotropic** if
`Ω|_{L×L}=0` and **Lagrangian** if moreover `dim L = n`; equivalently `L = L^ω` where
`L^ω = {w : Ω(w,v)=0 ∀v∈L}` is the symplectic complement. Lagrangians are exactly the
`𝔽₂`-symplectic data of stabilizer groups (the Pauli `↔ 𝔽₂^{2n}` dictionary, commutation
`= Ω`). `Sp(2n,𝔽₂)` is the symplectic group; modulo Pauli translations it is the
Clifford group, and its metaplectic/Weil action implements the symplectic Fourier
transform below.

**Definition (Fourier transforms on functions `V → ℝ`).**
```
ordinary:     F[f](w)   = Σ_{v∈V} f(v) (−1)^{⟨w,v⟩}      (⟨·,·⟩ the standard dot product)
symplectic:   F_Ω[f](w) = Σ_{v∈V} f(v) (−1)^{Ω(w,v)}     (the Weil transform)
```

**Lemma 0.** `F_Ω∘F_Ω = 2^{2n}·Id`; hence the eigenvalues of `F_Ω` are `±2^n`.
*Proof.* `F_Ω²[f](u) = Σ_w (−1)^{Ω(u,w)} Σ_v f(v)(−1)^{Ω(w,v)} = Σ_v f(v) Σ_w (−1)^{Ω(w,u+v)}`,
using `Ω(u,w)=Ω(w,u)` over `𝔽₂`. The inner sum is `2^{2n}` if `u+v=0` and `0` otherwise
(non-degeneracy of `Ω`), so `F_Ω²[f]=2^{2n}f`. ∎

---

## 3. The Lagrangian indicator is symplectically self-dual

**Proposition 1.** For a Lagrangian `L ⊂ V`, `F_Ω[1_L] = 2^n · 1_L`. Thus `1_L` is the
`+2^n`-eigenfunction of the symplectic Fourier transform; under the *ordinary* Fourier
transform it is instead supported on `L^⊥_{std} ≠ L` and is not self-dual.

*Proof.* `F_Ω[1_L](w) = Σ_{v∈L} (−1)^{Ω(w,v)}`. The map `v ↦ Ω(w,v)` is a linear
functional on `L`; it is identically zero iff `w ∈ L^ω`, in which case the sum is
`|L| = 2^n`, and otherwise it is a nonzero functional summing to `0`. Since `L` is
Lagrangian, `L^ω = L`, so the support is exactly `L` with value `2^n`. ∎

*Remark.* This is the discrete-symplectic counterpart of "the Gaussian is its own
Fourier transform." It is implicit in the Wigner–Weil/stabilizer formalism (stabilizer
states have flat Wigner functions supported on the affine Lagrangian); the point here
is the *reading*: the self-duality that LWE obtains analytically from Gaussians, LSN
obtains group-theoretically from Lagrangians under the Weil transform. Verified `n=2,3`
(§7, script 18).

---

## 4. Symplectic self-dual noise is maximally mixed

**Proposition 2.** Let `g : V → ℝ_{≥0}` be a probability distribution (`Σ_v g(v)=1`)
with `F_Ω[g] = 2^n g`. Then `g(0) = 2^{-n}`; equivalently the error rate
`Pr[v≠0] = 1 − 2^{-n}`.

*Proof.* Evaluate the self-duality at `w=0`: `F_Ω[g](0) = Σ_v g(v)(−1)^{0} = Σ_v g(v) =
1`, while the eigen-relation gives `F_Ω[g](0) = 2^n g(0)`. Hence `g(0)=2^{-n}`. ∎

**Corollary.** A depolarizing channel (`Pr[I]=1−3q`, `Pr[X]=Pr[Y]=Pr[Z]=q` per qubit)
is symplectically self-dual only at `q = 1/6` (error rate `1/2`); cryptographic low-`q`
noise (no-error mass `≈ 1`) is far from self-dual.

Contrast with LWE: the Gaussian is self-dual at *every* width `σ`, so Regev may choose
`σ` above the smoothing parameter while keeping the noise usable. The symplectic
self-dual noise is *rigid* — a single point at the maximal error rate `1 − 2^{-n}`,
worsening with `n`. The Fourier-smoothing route to a LSN w2a is therefore
information-theoretically vacuous: the only self-dual noise is undecodable. Verified
`n=1,2,3` (§7, script 19).

---

## 5. The symmetry route to worst→avg, and where it closes

The second natural mechanism is to randomize the instance by a group action (as Regev
randomizes the lattice). We separate the instance into *code* (the Lagrangian) and
*error*, and find the obstruction lands cleanly on the error.

**Proposition 3 (the code is homogeneous).** `Sp(2n,𝔽₂)` acts transitively on
Lagrangians (Witt's theorem; verified `n=2`: a single orbit of `15`). Consequently all
stabilizer codes are `Sp`-equivalent, so there is no "worst-case Lagrangian": the
code-side w2a is *vacuous*, and the hardness of LSN resides entirely in the noisy
decoding rather than the choice of code.

*(This is why the symplectic symmetry, despite being far richer than anything LWE has
on the lattice side, yields no free w2a: richness here means homogeneity.)*

A meaningful w2a must therefore randomize the *error* by a subgroup `H ≤ Sp` that (i)
acts transitively on the relevant instances and (ii) preserves the noise distribution.
No such `H` exists for per-qubit noise:

**Proposition 4 (the noise side closes).**
(a) The cryptographic per-qubit noise `N_q(e) = ∏_i [\,Pr_q\,]` is *not* `Sp`-invariant:
an entangling element (e.g. the transvection `t_u`, `u=(1,1,0,0)`) changes the
qubit-support of `e` (e.g. `Z_2 ↦ Y_1X_2`, support `1↦2`), hence `N_q(g·e) ≠ N_q(e)`
(`0.07 ↦ 0.01` at `q=0.1`).
(b) The subgroup `H_{loc} ≤ Sp` that *preserves* the per-qubit tensor structure (local
Cliffords ⋊ qubit permutations) is *not* transitive on Lagrangians: for `n=2` it splits
the `15` Lagrangians into orbits of sizes `{6, 9}`.
Verified `n=2` (§7, script 21).

**Consequence (the barrier, localized).** Randomizing the code needs the full
(transitive) `Sp`, whose action destroys the per-qubit noise (Prop. 4a); the only noise
invariant under all of `Sp` is uniform-on-nonzero — the maximal-entropy class — and its
Fourier-self-dual representative has no-error mass `2^{-n}` (Prop. 2); the subgroup that
would preserve the cryptographic noise is intransitive (Prop. 4b). **There is no
transitive, noise-preserving randomization of the LSN instance.** This is precisely the
"entropy" and "Pauli-mixing" barriers of the literature, now a single group-theoretic
fact: *code-randomization and noise-preservation are incompatible because the symplectic
group is transitive but noise-mixing, and the noise-preserving subgroup is intransitive.*

---

## 6. Discussion and open problems

The analysis closes the *symmetry* route to a LSN worst→avg and the *Fourier-smoothing*
route, the two mechanisms that carry LWE's w2a, and it explains uniformly why: the
self-duality LWE uses is present (Prop. 1) but is rigid as a noise (Prop. 2) and is
carried by a group that is transitive on codes yet incompatible with the cryptographic
noise (Props. 3–4). What remains open is whether some *third* mechanism — not the
symplectic symmetry and not symplectic-Fourier smoothing — yields a noise-side w2a.

Concrete, finite questions the localization isolates:
1. **Orbit n-scaling.** How does the `H_{loc}`-orbit partition of Lagrangians grow with
   `n` (`{6,9}` at `n=2` → ?), and is there an intermediate `H_{loc} ≤ H ≤ Sp` that is
   both transitive on Lagrangians and preserves a usably-sparse (sub-uniform) noise?
2. **Uniform-error LSN.** Is the average-case problem under the `Sp`-invariant
   (uniform-on-nonzero) noise — for which the symmetry route *does* close — itself hard?
   A positive answer would give LSN a genuine w2a under a non-standard noise.
3. **Spectral converse.** Prop. 2 shows the self-dual noise is undecodable; is there a
   matching statement that *any* noise admitting a Fourier-based w2a must exceed the
   decoding converse, ruling out the smoothing route unconditionally?

---

## 7. Scope, honesty, and verification

- **Proved/observed:** Props. 1–2 are short exact statements (general `n`), verified
  `n≤3`. Props. 3–4 are verified `n=2` (the group-action computations); Prop. 3 is Witt's
  theorem in general; the `n`-scaling of Prop. 4b is open (item 6.1).
- **Not claimed:** no worst→avg reduction is constructed, and no hardness is proven. The
  result is a *localization* of an existing folklore barrier, plus a structural reframe
  (LSN as the symplectic realization of the LWE self-duality principle). An earlier draft
  of §5 over-claimed a "free w2a from `Sp`-transitivity"; Prop. 3 corrects this — the
  transitivity is homogeneity, not a reduction.
- **Verification scripts** (`docs/superpowers/specs/lsn-experiments/`):
  `18-symplectic-fourier-selfduality.py` (Prop. 1), `19-selfdual-noise.py` (Prop. 2 and
  the corollary), `20-worstavg-skeleton.py` (Prop. 3 and the invariant-noise statement),
  `21-worstavg-locality-crux.py` (Prop. 4).

## References

- O. Regev, *On lattices, learning with errors, …* (worst→avg via Gaussian self-duality).
- Poremba–Quek–Shor (ITCS '26); Lu–Poremba–Quek–Ramkumar (sympLPN, Appendix D);
  Khesin–Lu–Poremba–Ramkumar–Vaikuntanathan (avg-case; the worst→avg "quantum barrier").
- Gottesman; Aaronson–Gottesman (stabilizer formalism); Gross, *Hudson's theorem for
  finite-dimensional systems* (Wigner functions and Lagrangians); the Weil
  representation over finite fields.

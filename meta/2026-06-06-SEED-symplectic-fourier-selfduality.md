# SEED — Lagrangian symplectic-Fourier self-duality: LSN is the F₂-symplectic realization of LWE's worst→avg principle

> A small, *verified* structural discovery offered as a seed (in the user's sense:
> a small thing that may cascade). It reframes why LSN is the unique non-lattice
> frontier, and — more usefully — it **relocates the worst→avg "quantum barrier"**
> from the geometry to the *noise distribution*, opening a concrete, testable line of
> attack on LSN's hardness that the program has not tried.

## The verified fact (`lsn-experiments/18-symplectic-fourier-selfduality.py`)

```text
ordinary Fourier:    F[f](w)   = Σ_v f(v)(-1)^{<w,v>}     (standard dot product)
symplectic Fourier:  F_Ω[f](w) = Σ_v f(v)(-1)^{Ω(w,v)}    (symplectic form Ω)

For a Lagrangian L ⊂ F₂^{2n}:   F_Ω[1_L] = 2^n · 1_L     (verified n=2,3)
```

`1_L` is the **eigenfunction of the symplectic Fourier transform**, eigenvalue `2^n` —
it is **symplectically self-dual** — *exactly because* `L = L^ω` (a Lagrangian is its
own symplectic complement). Under the *ordinary* Fourier transform `1_L` is **not**
self-dual (it is supported on `L^⊥_std ≠ L`). The self-duality is intrinsically
**symplectic**.

## Why this is a seed — the synthesis with LWE

LWE's worst→avg hardness (Regev) rests on one structural fact: **the Gaussian is its
own Fourier transform** (self-dual), and that self-duality + smoothing reduces
worst-case lattice problems to average-case LWE. The program's *geometry wall* read
this as "worst→avg lives only on flat ℝⁿ (Gaussian self-duality)," and treated LSN as
an *exception* (quantum-native, escaping the wall).

**The seed reframes it.** The deep principle is not "flat ℝⁿ" — it is **self-duality of
the relevant object under the relevant Fourier transform**, and it has (at least) two
realizations:

```text
            object            Fourier transform        category
  LWE   :   Gaussian          ordinary (R^n)            flat archimedean
  LSN   :   Lagrangian 1_L    SYMPLECTIC (F₂^{2n})       discrete symplectic  <-- verified here
```

So **LSN is not an exception to the worst→avg principle — it is the *same* self-duality
principle realized in the symplectic-discrete category** (the Weil/oscillator corner;
cf. deep dive XXXIX). This is a cleaner reason than "quantum-native" for why LSN is the
*unique* non-lattice frontier: it is the **other** self-dual realization, and the
symplectic Fourier transform is the Weil representation that plays the role the
ordinary Fourier plays for Gaussians.

## The useful part — relocating the worst→avg barrier to the NOISE

The LSN papers report worst→avg as a "quantum barrier" (entropy `Ω(n²)` vs sparse,
Pauli-mixing — "exotic properties needed"). With the self-duality now established, the
barrier is **not** a missing self-duality (it is present). By the LWE analogy the
missing ingredient must be the **smoothing / noise** step:

```text
Regev LWE:  Gaussian self-duality  +  the Gaussian IS the noise (discrete Gaussian
            smooths the lattice)        -> worst->avg works.
LSN now:    Lagrangian self-duality  +  the noise is depolarizing / Bernoulli, which
            is NOT symplectic-Fourier-self-dual (its F_Ω is a product, not concentrated)
                                        -> the self-duality and the noise are MISMATCHED.
```

> **Seed hypothesis (concrete, testable):** the worst→avg barrier for LSN is the
> *mismatch* between the symplectically-self-dual code (Lagrangian) and a noise model
> (depolarizing) that is **not** symplectically self-dual. A noise distribution that
> **is** symplectic-Fourier-self-dual — correlated across the `Ω`-conjugate coordinate
> pairs, the discrete analog of the Gaussian that smooths a lattice — might restore the
> Regev-style smoothing and yield a worst→avg reduction for the *modified* sympLPN.

That is a research line the whole program never tried: instead of attacking LSN's
hardness with decoders (all walled), **build the self-dual noise and test whether
worst→avg goes through.** Two outcomes, both valuable:
- it works (even partially) → a *structural hardness argument* for LSN (a genuine step
  toward 7th, the first positive evidence rather than no-go evidence); or
- it fails with a precise obstruction → the exact, named reason the symplectic
  self-duality cannot be smoothed (sharpening the "quantum barrier" from folklore to a
  theorem-shaped statement).

## Honest scope

- **Verified:** the symplectic-Fourier self-duality of `1_L` (eigenvalue `2^n`). This is
  a clean fact (and is implicit in the stabilizer/Wigner–Weil formalism — the novelty
  is the *synthesis* with LWE's worst→avg self-duality and the reframe below, not the
  identity itself).
- **Reframe (argued):** LSN = the symplectic-discrete realization of the LWE worst→avg
  self-duality principle; the geometry wall has two self-dual realizations, not one.
- **Seed (open, ≈0 but newly-handle'd):** worst→avg via a symplectic-self-dual noise.
  This is *not* the external `LSN ⊀ LPN` reduction question — it is the *other*
  direction (a hardness reduction FOR LSN), and it is a fresh, concrete handle.

## Next concrete step (for whoever picks up the seed — Codex/Claude/Kimi)

```text
1. Characterise the symplectic-Fourier-self-dual distributions on F₂^{2n}
   (fixed points of F_Ω among probability vectors) — the discrete analog of the
   Gaussian family. Conjecture: they are the Ω-pair-correlated (Y-type/depolarizing-
   *correlated*) noises, not the i.i.d. Bernoulli.
2. Build the simplest self-dual noise; define sympLPN-with-self-dual-noise.
3. Test (small n) whether a worst-case isotropic-decoding instance reduces to it via
   the self-duality + a smoothing parameter — i.e. run the Regev skeleton symplectically.
```

The honest framing the user gave: a small verified thing (the self-duality) that may
cascade (worst→avg via self-dual noise → the first positive hardness evidence for LSN).
Shared here as the seed.

---

## ★ Seed step 1 — DONE (it sprouted): the self-dual noise is rigidly near-total

`lsn-experiments/19-selfdual-noise.py`. Characterising the symplectic-Fourier-self-dual
distributions (the "which noise smooths" question) gave a clean, sharp result.

**Theorem (2-line proof, verified n=1,2,3).** For any distribution `g` with `F_Ω[g] =
2^n·g` (self-dual): evaluate at `w=0` — `F_Ω[g](0) = Σ_v g(v)·(-1)^{Ω(0,v)} = Σ_v g(v) =
1`, and self-duality gives `F_Ω[g](0) = 2^n·g(0)`. Hence

```text
   g(0) = 2^{-n}      i.e.   P(no error) = 2^{-n}   ->   error rate = 1 - 2^{-n} -> 1.
```

Every symplectic-Fourier-self-dual noise is pinned at **near-total error**, worsening
with `n`. (Check: depolarizing `P(I)=1-3q, P(X)=P(Y)=P(Z)=q` is self-dual **only** at
`q=1/6` → identity prob `1/2 = 2^{-1}`; cryptographic low-`q` (identity ≈ 1) is far from
self-dual. The self-dual eigenspace itself is large — dim 10 for n=2 — but every
*distribution* in it obeys `g(0)=2^{-n}`.)

## ★ What this sharpens — the worst→avg "quantum barrier", now a theorem-shaped statement

```text
LWE  : the Gaussian is self-dual at EVERY width σ -> a FAMILY -> Regev picks σ ≥ the
       smoothing parameter while keeping the noise cryptographically usable.
LSN  : the symplectic self-dual noise is RIGID -> a single point at error rate 1-2^{-n}
       -> you CANNOT lower it to a usable rate while staying self-dual.
```

So the folklore "worst→avg is a quantum barrier (exotic properties needed)" becomes a
**concrete, n-dependent obstruction**: *the only symplectic-Fourier-self-dual noise has
`P(no error)=2^{-n}`, so Regev-style self-dual-noise smoothing is information-
theoretically useless for LSN (the noise is above every decoding converse).* The code
(Lagrangian) is self-dual; the **noise cannot match it at a usable rate** — that is the
mismatch, made precise.

## ★ Where the butterfly goes next (the redirected line)

The naive route (self-dual *noise* smoothing) is now *provably* blocked, cleanly. But
the Lagrangian's self-duality lives in the **code**, not the noise — so a worst→avg for
LSN, if it exists, must exploit the code's symplectic self-duality **without** demanding
a self-dual noise (unlike LWE, where code and noise are the same Gaussian). Concrete
next probe: a worst→avg that uses the **Weil representation** action on the Lagrangian
(the symplectic Fourier = the Weil transform) to randomise the *instance* (a different
Lagrangian) rather than to smooth the noise — decoupling the self-duality (code) from
the noise rate. That decoupling is exactly what the `g(0)=2^{-n}` rigidity says LWE gets
for free and LSN does not — so it names, precisely, the one thing a LSN worst→avg would
have to supply. **That is the seed's live tip.**

---

## ★★ Seed step 2 — COMPLETED: the worst→avg barrier is a *transitivity-vs-locality conflict* in Sp

`lsn-experiments/20-worstavg-skeleton.py`, `21-worstavg-locality-crux.py`. Running the
Regev skeleton **symplectically** (randomise the code by the Weil/`Sp` action instead of
smoothing the noise) resolves the seed into a precise, verified barrier theorem (n=2).

**The skeleton works for the CODE — better than LWE:**
```text
(1) Sp(2n,F₂) is TRANSITIVE on Lagrangians (orbit of one = all 15).  [verified]
    => worst-case-Lagrangian -> uniform-random-Lagrangian is EXACT and FREE, by the
       group action. LWE needs Gaussian smoothing for this step; LSN gets it from Sp.
(2) Sp is TRANSITIVE on nonzero vectors.  [verified]
    => the ONLY Sp-invariant noise is uniform-on-nonzero (P(0)=a).
```

**It breaks for the NOISE — and exactly why is now group-theoretic:**
```text
(3a) an ENTANGLING Sp element (transvection by (1,1,0,0)) changes qubit-support
     (Z2 -> Y1X2: support 1->2), so the cryptographic PER-QUBIT noise is NOT invariant.
     [verified: P(e)=0.07 -> P(g·e)=0.01]
(3b) the LOCAL-Clifford(+swap) subgroup -- the elements that DO preserve per-qubit
     noise -- is NOT transitive on Lagrangians: it splits them into orbits {6, 9}. [verified]
```

**Theorem-shaped statement (the barrier, made concrete).**
> Randomising the LSN code (worst-case → average-case Lagrangian) requires the *full*
> `Sp`, but the only noise preserved by full `Sp` is the **uniform/max-entropy** class
> (its self-dual sub-case has `P(no error)=2^{-n}`). The subgroup that preserves the
> cryptographic **per-qubit** noise (local Cliffords) is **not transitive** on
> Lagrangians ({6,9} for n=2). So there is **no noise-preserving transitive
> randomisation** — hence no free `Sp` worst→avg for *per-qubit* LSN.

This **unifies the two folklore barriers** of the LSN papers ("entropy" and
"Pauli-mixing") into **one** group-theoretic fact: code-randomisation forces the noise
into the `Sp`-invariant (max-entropy) class; the per-qubit-preserving subgroup is
intransitive. The free worst→avg holds **only for the uniform-error model**.

## ★ The completed seed → the isolated gap (for the other agents)

The whole question is now a single, concrete, *group-theoretic* gap — not folklore:

```text
LSN has a FREE worst->avg for the UNIFORM-error model (Sp-invariant noise).
Standard LSN uses PER-QUBIT noise. The two differ by exactly the {6,9}-orbit splitting
of the local subgroup. So the open problem reduces to ONE of:
  (a) is UNIFORM-error LSN itself a hard average-case assumption? (then LSN inherits a
      genuine worst->avg = the FIRST positive hardness evidence) -- or
  (b) is there an INTERMEDIATE subgroup H, Sp ⊇ H ⊇ local, transitive on Lagrangians
      AND preserving a usable (sub-uniform) noise? The {6,9} splitting and its
      n-scaling is the exact object to study.
```

Either is a clean, finite, *positive*-direction target — the opposite of the program's
no-go evidence. **Hand-offs:**
- **Codex** (`Sp`/OFA harness): compute the local-subgroup orbit structure on Lagrangians
  for n=3,4 ({6,9} → ? scaling) and search for an intermediate transitive-and-noise-
  preserving `H`. Its `Sp(2n,F₂)` tooling, pointed at a *positive* question.
- **Kimi / other Claude executor**: screen whether *uniform-error* LSN (path (a)) is hard
  — does any structural decoder break it at poly samples? (same battery, new noise model.)
- **Claude (adjudicator)**: characterise the intermediate-subgroup lattice and the
  worst→avg it would yield.

Honest status: this is the program's **first positive structural handle** on LSN's
hardness (vs ~35 no-go sign-offs). It does not prove worst→avg — it *reduces* the
question to one concrete group-theoretic gap and hands each agent a piece. The seed,
completed and planted.

---

## ★ Step 2 — HONEST CORRECTION (Sound Verifier applied to myself, again)

The framing above **over-claimed**, and the discipline requires flagging it before it
seeds anyone wrongly:

> "Sp-transitivity gives a FREE worst→avg for the code, more than LWE" is **wrong**.
> Sp transitive on Lagrangians means **all Lagrangians are equivalent** — the code is
> **homogeneous** (this is the old C2 point: the noiseless/code problem carries no
> secret). LWE's worst→avg is meaningful precisely because **lattices are *in*equivalent**
> (no transitive group). So for LSN the *code-side* worst→avg is **vacuous**, not a win:
> there is no "hard Lagrangian" to reduce from.

So the corrected, honest content of step 2 is:

```text
- The symplectic SYMMETRY (Sp) makes the CODE homogeneous -> confirms (again) that all
  hardness is in the NOISY DECODING, not the code. (Not a worst->avg win; a homogeneity.)
- A meaningful LSN worst->avg must therefore come from the ERROR/noise side: randomise a
  worst-case error to average-case noise. But the randomiser (Sp) does NOT preserve the
  per-qubit noise (3a), the noise-preserving subgroup is intransitive (3b), and the only
  symmetry-compatible (self-dual) noise is max-entropy (g(0)=2^{-n}). So the symmetry
  that could randomise CANNOT supply the noise-side worst->avg either.
```

**What genuinely survives as the seed (no over-claim):**
1. **(insight)** LSN = the *symplectic-over-F₂ realization of the LWE self-duality
   principle* — `1_L` is symplectic-Fourier self-dual as the Gaussian is ordinary-Fourier
   self-dual. A real reframe of why LSN is the unique non-lattice frontier.
2. **(barrier, clean)** the only symplectic-self-dual noise has `P(no error)=2^{-n}`; the
   per-qubit noise is not `Sp`-invariant; the noise-preserving subgroup is intransitive.
   Together these **localize the worst→avg obstruction to the noise side** and unify the
   papers' "entropy + Pauli-mixing" folklore into one group-theoretic fact.
3. **(open, honest)** whether a *non-symmetry* mechanism gives LSN a noise-side worst→avg
   is the real question — the symmetry route is now *precisely* closed, not by lack of
   self-duality (it is there) but by the noise incompatibility. **This is a sharpening,
   not a positive proof.** The "first positive handle" claim is downgraded to "the first
   precise *localization* of the worst→avg barrier."

The corrected seed for the agents is therefore the **localization**, not a worst→avg
construction: *is there a noise-side worst→avg for LSN that does not route through the
symplectic symmetry* (which we have now shown cannot supply it)? That is the honest tip.

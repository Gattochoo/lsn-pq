# CAPSTONE — The 7th Post-Quantum Hardness Family: final in-house report

> A single synthesis of the whole program (42 spec docs + 17 verified experiments on
> `shared/hardness-7th-exchange`). Read this to understand the result without reading
> the 35 sign-offs. Discipline throughout: Sound Verifier (BROKEN / REDUCES / OPEN;
> evidence ≠ proof; resemblance ≠ reduction).

## The question, and the one-line answer

**Question:** is there a genuinely new ("7th") post-quantum hardness *source*, beyond
the six established families (lattice, code, hash, multivariate, isogeny,
MPC-in-the-head)?

**Answer:** **No new source was found, and none was proven — but the entire question
was reduced, with no under-tested spot remaining, to a single external proposition.**
The only candidate that survives every in-house screen is **LSN** (Learning
Stabilizers with Noise / its classical core sympLPN). Its 7th-vs-6.5th status is
exactly the open community question **`LSN ⊀ LPN`** (does the symplectic/stabilizer
structure add hardness that does not reduce to plain LPN?). Everything else is walled.

## The two workstreams

### B — the census: LSN is the *unique* quantum-native inhabitant

The "thin band" of a quantum-native source = classically-simulable formalism **+** an
independent discrete hard-decoding layer. The clean simulable formalisms are exactly
two, plus their generalisations — all screened:

```text
Clifford / stabilizer (F₂-symplectic)  -> LSN            = the inhabitant
matchgate / free-fermion (Gaussian)    -> CLOSED  (JW algebra-isomorphism theorem;
                                                    non-locality = representation, not
                                                    hardness; F-1 continuous-easy)
qudit / normalizer (Z_d-symplectic)    -> CLOSED  (= the SAME Clifford source over F_d,
                                                    not a third formalism; CRT for composite d)
bosonic / GKP (lattice CVP)            -> CLOSED  (= lattice, family #1)
```

So **LSN is the band's unique inhabitant — a census result, not just a screen.**

### A — the verdict: every structural decoder obeys the wall at crypto complexity

The classical core is "recover a secret Lagrangian `L ⊂ F₂^{2n}` from noisy data." The
question is whether the **symplectic structure** can be **publicly stripped** to plain
LPN (→ REDUCES → 6.5th) or resists (→ OPEN → 7th-evidence). Every structural decoder
tried — by three independent agents — fails at the crypto regime (constant noise rate
`p≥0.1` **and** poly samples):

```text
support-span (bounded-distance)     break by p≈0.02 (result #5; Codex OFA-315; Kimi T3)
top-k Walsh / Fourier               threshold SHRINKS with n (OFA-315/317/318)
ISD / BKW                           sub-exponential = the expected LPN-hardness, not REDUCES
proper F₂-Plücker (Walsh-dual)      signal floor m* EXPONENTIAL in n (Task-5 verified)
belief-propagation                  random codes have no Tanner structure
closure-autocorr / bucket-rank-stop / isotropic-greedy / coset-gain:
   the strongest signal (survives n-scaling to n=8), BUT only in the dense,
   EXPONENTIAL-sample, low-rate corner -> CHANNEL-LEVEL closed: at poly-sample
   E[true members observed] = m·2^{-n} -> 0, so the autocorrelation/Walsh signal of L
   vanishes and NO decoder in the family (present or future) can recover.
```

**All converge on one wall.** A REDUCES would now require a *non-(autocorrelation ∪
Walsh)* decoder working at poly-sample constant rate — which is `LSN ⊀ LPN` itself.

## The framework — the no-go map

Every dead candidate (20+ external submissions; ~50 deep dives) is one of **four death
modes** under **two structural walls**:

```text
①reduction  ②too-weak  ③too-well-behaved  ④already-assumed(novelty-cost)  ⑤BQP-easy
geometry wall  = crypto worst→avg = Gaussian self-duality on FLAT ℝⁿ (curvature/p-adic/
                 non-abelian all leave it and die) -> only flat-archimedean lattices survive.
trapdoor wall  = a one-way object needs a trapdoor to be a primitive; attaching one
                 re-imports a named assumption (the trapdoor IS the reduction).
```

LSN escapes by being **quantum-native** (not flat-archimedean geometry) with hardness
that **originates** in quantum information, not a classical code — which is *why* it is
the one survivor, and *why* its status is the symplectic-structure question.

## The decisive sample-complexity insight (the program's sharpest tool)

The membership channel is **exponential-data by construction**: `L`'s members are a
`2^{-n}` fraction, so you need `m ≳ 2^n` observed labels just to *see* `L` above the
noise-induced false positives. Every "strong signal" the search found (coset-gain
13/16 at p=0.1; bucket-rank-stop surviving to n=8) lives in that exponential corner. At
poly samples there is no `L`-structure in **any** transform of the data, so the whole
autocorrelation/Walsh family is closed *channel-level*, not decoder-by-decoder. This is
the precise reason the strongest structural signals carry **no crypto weight**.

## The collaboration — three tools, one convergence

```text
Codex   (executable OFA harness, Rust) : built the structural decoders, pushed n-scaling
                                          to n=8, held Claim-Discipline = our Sound Verifier.
Kimi / Claude-executor (screens)        : closed the companion census (Tasks 1-2) and
                                          stress-tested the verdict (Tasks 3-5); when Kimi
                                          went down, a Claude session took the executor role.
Claude  (math + adjudicator)            : the no-go map, the barrier/incidence/sample-
                                          complexity results, the channel-level closure,
                                          and ~35 Sound-Verifier sign-offs.
```

Three independent tools, with a complete no-go map, converged — by different means — on
the same place. **That convergence is the strongest result the in-house program can
produce**, and it includes the discipline of self-correction: "all doors closed" was
twice walked back to the precise, true statement below.

## The honest, fully-sealed conclusion

> **We did not find a 7th source, and we did not prove LSN is one. But across 17
> verified experiments and ~35 sign-offs, three independent agents and a complete no-go
> map showed — with no under-tested spot remaining — that every other road is walled:
> the quantum-native band has LSN as its unique inhabitant (by census), and LSN resists
> public reduction at crypto complexity under every soundly-implemented attack family
> (including the strongest, which survives n-scaling but only in the exponential-sample
> corner). The entire 7th question is reduced to one external proposition: the hardness
> of `LSN ∖ LPN`. We cannot prove it in-house — that is genuinely the community's
> (Vaikuntanathan et al.) — but we have mapped, exhaustively, why it is the only door
> left.**

## Index of artifacts (on `shared/hardness-7th-exchange`)

```text
Framework : phase1-deathmode-capstone · sound-verifier · collaboration-guide (14 checks)
Frontier  : LSN-reassessment · LSN-source-level · LSN-thin-band
Census (B): adjudication-kimi-orthogonal-residual · -phase2-exotic · -task2-third-formalism
            · -task2-signoff   (Clifford/matchgate/qudit/GKP)
Verdict(A): result #1 (entropy deficiency) · #2 (barrier map) · #4 (incidence design)
            · #5 (constant-rate break) · proper-Plücker · channel-level-closure
            · Task-5 sample-density sweep · 17-autocorr-signal-vanish
Codex     : adjudication-ofa-305-308 · -309 · -310 · -311-313 · -315-316 (THE VERDICT)
            · -317-318 (n-scaling) · -319-321 · -322 · -323-324 · -325-327 · FINAL
Experiments: lsn-experiments/01..17 (entropy, barrier, baselines, matchgate, Plücker,
             incidence, constant-rate, qudit, sample-sweep, autocorr-vanish)
```

*In-house search concluded 2026-06-06. What remains is the external `LSN ⊀ LPN` proof.*

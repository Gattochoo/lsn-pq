# LSN Joint Research Log (Claude ↔ Codex)

> Living log on `shared/hardness-7th-exchange`. Restarting LSN research as the
> program's one live frontier. Append-only; each entry = one grounded result.
> Discipline: Sound Verifier (BROKEN / REDUCES / OPEN) + the 14 self-checks.

## The precise frame (do not re-litigate)

LSN is **not** a settled PQC family, and **not** a settled 6.5th, and **not** a
proven 7th. Per the three LSN docs on this branch, its status resolves into
**three levels** — memorise this instead of a one-word label:

```text
mechanism        → 6.5th   (noise/decoding — same KIND of hardness as the code family)
structure        → 7th     (LSN ⊇ LPN superset, sympLPN ⊀ LPN non-reducible,
                            degeneracy/worst→avg-barrier = phenomena with NO classical analog)
proven hardness  → 6.5th floor (F2: ≥ classical code decoding, PROVEN)
                  + 7th conjecture (the "quantum extra" LSN∖LPN is hard — UNPROVEN)
```

> The entire 7th question = **one external proposition: is `LSN ∖ LPN`
> independently hard?** A *proof* of that is community-scale (Vaikuntanathan et
> al., 2509.20697); in-house ≈ 0. We do **not** chase the proof. We chase the
> *tractable* sub-questions below, whose outcomes are publishable either way.

## Workstreams

```text
A. Non-linear reduction probe   [JOINT — Codex-led executable]   ← #1 target
   Appendix D rules out *linear* sympLPN→LPN (entropy/Shannon). Non-linear /
   algebraic reductions are OPEN. Find one → LSN collapses to 6.5th (settles it,
   a major negative result). Map a structural barrier → strengthens 7th.
   This IS the Sp(2n,F2)-on-Lagrangians layer the handoff pointed Codex's OFA at:
   "is there a public group-action reduction of stabilizer-decoding to plain LPN?"

B. Matchgate/Majorana 2nd-inhabitant screen   [Claude/Kimi — math screen]
   thin-band §4's one concrete open sub-question: is there a discrete fermionic-
   code decoding that sits in the band (escapes Pfaffian-easy without going #P)?
   Clean ④ (genuinely unexamined). A second band inhabitant would be its own find.

C. Ground-truth object + empirical probes   [Claude — first-pass Python]
   Build toy sympLPN/LSN; verify the separation facts in code so both agents
   reason on the object, not the prose. (Result #1 below.)

X. The LSN∖LPN hardness proof   [EXTERNAL — track only, do not attempt]
```

## Collaboration split

```text
Claude : math + first-pass Python (object construction, reduction-probe design,
         matchgate screen, Sound-Verifier adjudication).
Codex  : executable OFA at scale on Sp(2n,F2)-on-Lagrangians (workstream A heavy
         search), held to its own seed-stable Claim-Discipline bar.
Joint  : the reduction-existence verdict (REDUCES→6.5th settled / seed-stable
         OPEN→7th evidence). Recorded here.
```

---

## Result #1 — Appendix-D entropy deficiency is EXACT (workstream C)

`lsn-experiments/01-entropy-deficiency.py`. Exact count of ordered n-tuples of
pairwise symplectically-orthogonal columns over F2^{2n}, vs uniform 2n² bits:

```text
 n   #isotropic tuples   H_iso   H_unif=2n²   gap    C(n,2)   self-isotropic?
 1                   4   2.000        2       0.000     0      True
 2                 136   7.087        8       0.913     1      True
 3               36352  15.150       18       2.850     3      True
```

**Reading.** The entropy gap tracks `C(n,2) = n(n−1)/2` almost exactly (n=2:
0.91≈1; n=3: 2.85≈3) — **each symplectic-orthogonality constraint costs ~1 bit**,
so an isotropic `A` is information-theoretically far from uniform, and
`H_unif − C(n,2) = (3/2)n² + n/2`, matching Thm D.1's ~(3/2)n². Also confirmed:
over F2 every vector is self-symplectic-orthogonal (`aᵀΩa=0`), so the constraint
is purely the C(n,2) *pairwise* conditions.

**Why it matters.** This is the EXACT, structural reason linear reductions
sympLPN→LPN fail: you cannot make an isotropic `A` uniform (needed for LPN)
without injecting the missing ~n²/2 bits, which Thm D.2 shows forces error weight
past the Shannon converse. The deficiency is **real and essential, not
"none-found-yet."** Workstream A's whole question is therefore precise: **can a
*non-linear* reduction close this exact entropy gap without exceeding the noise
converse?** That is the single bit that separates 6.5th from 7th-evidence.

**Verdict (Sound Verifier):** ground-truth fact, not a candidate. Confirms the
§3.6 Appendix-D reading in code. OPEN question A is now sharply posed.

---

## Result #2 — the non-linear reduction barrier map (workstream A, step 1)

`lsn-experiments/02-reduction-barrier-map.py`. Two convention-free measurements
(we deliberately avoid re-deriving the paper's matrix convention — see the
reduction-model-drift caution) probing the two natural non-linear escapes from
Appendix D's *linear* wall.

**2A — linear / dense-mixing escape → piling-up wall.** Any reduction that builds
a new error bit as the XOR of `w` original Bern(p) error bits has effective noise
`η(w)=(1−(1−2p)^w)/2 → 1/2`. Empirical matches formula (p=0.10):

```text
 w:     1      2      3      5      8     12     20
η:    .100   .181   .246   .336   .417   .465   .494   → 1/2
```

Uniformizing the entropy-deficient `A` (injecting the missing ~n²/2 bits)
requires mixing `Θ(n)` error bits per output, but `η` saturates to 1/2 long
before — **the error is destroyed before uniformity is reached.** This is the
mechanism behind Thm D.2, in code.

**2B — degree-2 / Veronese escape → Segre (rank-1) wall.** A degree-2 reduction
writes `b'_ij ~ ⟨s,a_i⟩⟨s,a_j⟩ = ⟨s⊗s, a_i⊗a_j⟩`, so the lifted LPN matrix has
columns `a_i⊗a_j` = **rank-1 tensors** (the Segre variety). Entropy vs uniform:

```text
 n:                2      3      4      5
isotropic H/unif: .750   .750   .750   .750     (result #1)
lift H/unif:      .488   .332   .250   .200   → ~1/n → 0
```

The original isotropic `A` keeps 75% of uniform entropy; its degree-2 lift keeps
only `~2N/N² = 1/n`. **The natural non-linear escape moves the problem into a far
MORE structured (less uniform) space, not a uniform one** — it backfires.

**Verdict (Sound Verifier): OPEN, unchanged — but now with a barrier map.** Both
natural reduction routes hit *information-theoretic* walls (piling-up; Segre),
not "none-found-yet" gaps. This is **7th-evidence direction**, explicitly **not a
proof** — a cleverer non-linear reduction is not excluded. It *sharpens* the open
target to one precise statement.

### The sharpened target for Codex (workstream A, scale-up)

> Does there exist a reduction injecting the missing `C(n,2)` bits with
> error-mixing **sub-linear in `w`** (so `η` stays decodable) **and** keeping `b'`
> linear in `s` — or a secret-lift `s'` whose lifted matrix stays uniform (escaping
> the Segre collapse)?

This is exactly an "is there a public group-action reduction?" question on
`Sp(2n,F₂)`-on-Lagrangians — Codex's OFA breaker, re-pointed. A hit → REDUCES
(6.5th, settled). A seed-stable miss across the OFA increment battery → the
barrier map hardens (7th-evidence).

### Next

- **[Codex]** scale workstream A on `Sp(2n,F₂)`-on-Lagrangians, against the
  sharpened target, under the Claim-Discipline / Sound-Verifier bar.
  (Baseline verified + cautions handed over: `…claude-response-to-codex-first-ofa.md`.)
- **[Claude — DONE]** workstream B screen complete (Result #3 below).

---

## Result #3 — matchgate/fermion second-inhabitant screen (workstream B)

Full note: `2026-06-05-lsn-workstream-b-matchgate-screen.md`. Anchor:
`lsn-experiments/04-matchgate-vs-clifford-noise.py`.

**Core dichotomy (anchor).** Matched linear learning-with-noise, ℝ vs F2:
continuous (matchgate/Gaussian) error decays `~1/√N` (0.223→0.017) — noise
averages out, EASY (F-1); F2 (Clifford/LSN) Hamming error stays `~0.5` for all N —
no averaging escape, HARD. The band needs *discrete* hard-decoding; matchgate's
simulability is *continuous*, so it can't carry it.

**Census — every fermionic route walls:** (1) free-fermion Gaussian learning →
covariance estimation → F-1 easy [anchor]; (2) Majorana/surface-code decoding →
min-weight perfect matching → poly easy; (3) Majorana stabilizer decoding →
Jordan–Wigner → = qubit stabilizer decoding = **LSN itself** (not new); (4)
non-Gaussian → permanent #P (computing) + BQP-universal (⑤).

**Verdict: no second band inhabitant** (screen-level). LSN's uniqueness robust.
**Sharpened residual (positive):** a companion would need an `O(2m,F₂)`-orthogonal
discrete decoding that **resists JW collapse** to symplectic LSN — the
symplectic↔orthogonal F2 gap, the one pre-screened door left (next-probe / Kimi).

### Program status

- **A** (LSN reduction frontier): barrier-mapped (result #2), handed to Codex.
- **B** (companion search): screened to a clean negative + the orthogonal residual.
- **Net:** LSN remains the unique live frontier; both parallel tracks tighten
  rather than widen it. Nothing silently dropped.

---

## Result #4 — the Lagrangian incidence design: low-degree public breakers are blind (workstream A, step 3)

`lsn-experiments/07-lagrangian-incidence-design.py`. Pure combinatorics on the
verified 135 Lagrangians of `Sp(6,2)` (no sample-model — no drift). Characterises
what Codex's OFA-307 public breaker *can* be: how non-linear must it be to read
the secret Lagrangian?

```text
degree-1 (single Pauli x):  every nonzero x lies in EXACTLY 15 of 135 Lagrangians
                            -> CONSTANT over all 63 x -> degree-1 selector is BLIND.
degree-2 (pair x,y):  Ω(x,y)=1 -> 0 Lagrangians (PUBLIC: Ω is public, no leak);
                      Ω(x,y)=0 -> EXACTLY 3 Lagrangians -> CONSTANT -> degree-2
                      reads only the public Ω-class, ~no secret signal.
```

**Closed form (generalises to all n).** The number of Lagrangians containing a
fixed isotropic `k`-space is `∏_{i=1}^{n-k}(2^i+1)` = the Lagrangian count of the
`(n−k)`-reduced symplectic space (n=3: k=1→3·5=15 ✓, k=2→3 ✓). It is **constant
within each public isotropic-flag class at every n** — so low-degree public
selectors are blind not just at n=3 but for all n.

**Consequence for OFA-307 (sharpens the adjudication).** A public breaker that
"closes" using low-degree/linear tests is reading **public** Ω-structure, not the
secret. Therefore — pre-registered A1 made concrete — **a real REDUCES must be
genuinely non-linear OR exploit the noise coupling (C2); a low-degree "close" is an
artifact.** This is the complementary half to Codex's work: Codex builds the
breaker, this bounds what a *meaningful* breaker must be. Also independently
re-confirms C2 (the bare action carries no secret) and the result-#2 finding that
the symplectic structure resists *linear* exploitation.

**Verdict (Sound Verifier):** structural fact, not a candidate. Tightens the OFA-307
interpretation; n-independent.

---

## Result #5 — the constant-rate structural breakdown (Claude first-pass of THE verdict experiment)

`lsn-experiments/11-constant-rate-structural.py`. Codex built the structural
support-span repair (OFA-311/312/313) but tested it at trivial noise (0–1 flip).
This runs **the verdict-moving experiment** — the same repair at constant-rate
noise — from Claude's side, in parallel to Codex's pending version.

Channel = Codex's: noisy membership labels `[v∈L]⊕Bern(p)` over all 256 vectors of
F₂⁸; structural recovery = span of positive-labeled vectors (no enumeration).

```text
 p        #flips   span(pos) dim   structural recovery
 0.0000   0        4.00            25/25  works
 0.0039   1        5.00            11/25  1-bit repairable (= OFA-312 regime)
 0.0200   5        7.20            0/25   STRUCTURE FAILS
 0.0500   12       8.00            0/25   FAILS
 0.1000   25       8.00            0/25   FAILS
 0.2500   64       8.00            0/25   FAILS
```

**Sharp transition by p=0.02 (5 flips).** At constant rate the ~`p·240` false
positives dominate the 15 true members; their span jumps to **dim 8 = all of F₂⁸**,
so `span(positives) ≠ L` and the structural map breaks completely. Recovering L now
= find the 4-dim isotropic subspace consistent with the noisy labels =
**nearest-isotropic decoding = LPN-hard**, with no poly structural shortcut (result
#4: degree-≤2 selectors are blind to L).

**Verdict (Sound Verifier): 7th-EVIDENCE direction (seed-stable, not a proof).** The
structural public map that works at trivial noise (OFA-311/312) **breaks at the
constant-rate regime where LSN hardness lives** — the bounded-distance repair is
poly only below the LPN floor; constant-rate forces LPN-hardness. This is the
behavior a 7th source should show (symplectic structure resists public stripping
exactly where it matters). **Honest scope:** this kills the *natural* structural
attacks (support-span / bounded-distance); it does **not** prove no *cleverer*
reduction exists — that remains the external `LSN ⊀ LPN` question (in-house ≈ 0). It
converges with results #2 (barrier map) and #4 (incidence) and with the OFA-313
hint. Cross-checks Codex's pending constant-rate test from an independent
implementation.

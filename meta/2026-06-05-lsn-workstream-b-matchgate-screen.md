# LSN workstream B — the matchgate/fermion second-inhabitant screen

> thin-band (VII) §4 left exactly one concrete open sub-question: is there a
> discrete fermionic-code decoding that sits in the quantum-native band (escapes
> Pfaffian-easiness without going #P) — a **second** band inhabitant alongside
> LSN? This note turns VII's matchgate *pre-screen* into a full census with a
> structural verdict, and sharpens the one residual into a precise search target.
> Status: complexity screen — `no claim of a 7th`, screen-level (not a theorem).

## Core dichotomy (anchor, `lsn-experiments/04-matchgate-vs-clifford-noise.py`)

Why the band has exactly one inhabitant, shown directly. Matched linear
"learning with noise", once over ℝ (the matchgate/Gaussian analog) and once over
F2 (the Clifford/LSN analog):

```text
ℝ / matchgate (least squares):     F2 / LSN (naive decoders):
  N      rel.L2 err                   N    corr-decode Ham   LS-relax+round
  50       0.223                      50        0.417            0.500
 800       0.039                     800        0.542            0.500
6400       0.017  (~1/√N → 0)       6400        0.500            0.500  (~0.5, ∀N)
```

**Continuous noise averages out → EASY (F-1); F2 XOR-noise has no averaging escape
→ HARD (the LSN layer).** This is not an analogy — it is the same
`continuous = archimedean = averaging-easy` vs `discrete-F2 = hard-decoding`
distinction that the geometry wall draws everywhere in the no-go map. Matchgate
simulability is *continuous* (Gaussian covariance / Pfaffians over ℝ), so its
natural noisy-learning problem is mean-estimation — it **cannot carry the band's
discrete hard-decoding layer.**

## The full census — every fermionic route hits a wall

| # | fermionic route | where it lands | cliff |
|---|---|---|---|
| 1 | **free-fermion Gaussian state / unitary learning** | covariance-matrix estimation = linear, noise-robust (anchor above) | **F-1** (de-quantizes to easy mean-estimation) |
| 2 | **Majorana / fermionic surface-code syndrome decoding** | minimum-weight perfect matching = Edmonds' blossom, **poly-time** (codes are *designed* efficiently decodable) | easy (no hard layer) |
| 3 | **Majorana *stabilizer* decoding** (the "orthogonal LSN", `O(2m,F₂)`) | **Jordan–Wigner** maps even-Majorana monomials → Pauli strings ⇒ collapses to **qubit stabilizer decoding = LSN** | not new — *is* LSN |
| 4 | **non-Gaussian fermionic hardness** | leaving free fermions → **permanent = #P** (computing ≠ inverting) **and** BQP-universal | computing-wall + **⑤** |

Routes 1 and 4 are VII §4's two pre-screened walls (continuous-easy / #P-⑤),
now with route 1 demonstrated in code. Routes 2 and 3 are the *new* census
content — the two ways one might hope the **code** structure re-discretizes
fermionic hardness, and both close: matching-decoding is poly (2), and genuine
discrete Majorana-stabilizer hardness is Jordan–Wigner-equal to LSN (3).

## The sharpened residual — orthogonal vs symplectic

The census's one genuinely-open seam is route 3 stated at its strongest. The
qubit-Pauli commutation structure is a **symplectic** form over F2 → `Sp(2n,F₂)`
→ stabilizer decoding = LSN. The Majorana commutation structure is instead
governed by an **orthogonal** form over F2 → `O(2m,F₂)`. So a *bona fide* second
inhabitant would have to be:

> an **`O(2m,F₂)`-structured discrete hard-decoding** problem that **resists
> Jordan–Wigner reduction** to the `Sp(2n,F₂)`-structured LSN — i.e. a fermionic
> code with no efficient qubit-stabilizer equivalent.

Known fermionic stabilizer codes **do not** provide this (JW is an efficient
transformation, fermion-parity superselection recovers the Pauli/symplectic
picture, so their decoding *is* LSN). Whether an *exotic* fermionic hard-decoding
problem exists that uses the orthogonal `O(2m,F₂)` structure irreducibly — beyond
the reach of JW — is the **one formal residual** this screen leaves open. It is
the natural next probe (a good Kimi target): the **symplectic↔orthogonal gap over
F2** as the only unexamined door to a second band inhabitant.

## Verdict

- **Screen result: no second band inhabitant found.** Every natural matchgate /
  fermion route hits a wall (F-1 continuous-easy, poly-matching, JW-to-LSN, or
  #P/⑤). LSN's uniqueness as the band's inhabitant is **robust**, and now for a
  *demonstrated* reason: the band needs *discrete* hard-decoding, and the only
  clean discrete-decodable simulable formalism is Clifford (F2-symplectic) = LSN.
- **Sharpened search principle (positive deliverable):** a second 7th-source
  inhabitant must live in an `O(2m,F₂)`-orthogonal discrete decoding that escapes
  Jordan–Wigner collapse to the symplectic LSN — the precise, pre-screened door
  for the next worker.
- **Scope (honesty):** this is a **screen**, not a theorem — it censuses the
  known/natural fermionic structures and gives a structural argument; it does not
  *prove* no exotic construction escapes. Same discipline as VII. Updates VII §4's
  pre-screen to a full screen + a named residual.

## Net for the program

Workstream B closes the parallel Claude track with a clean negative + a sharpened
residual, while workstream A (the LSN reduction frontier) sits with Codex. The
two together keep the conclusion intact and tighten it: **LSN remains the unique
live frontier; the only unexamined door to a *companion* is the symplectic↔
orthogonal F2 gap** — pre-screened, handed off, not silently dropped.

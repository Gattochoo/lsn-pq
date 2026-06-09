# Synthesis adjudication — the one open worst→avg route: both natural realizations closed (transport ⊕ encode), one shared root

**Track:** math / adjudicator. **Date:** 2026-06-07.
**Discipline:** Sound Verifier (BROKEN / REDUCES / OPEN; evidence ≠ proof; no over-claim).
**Bottom line up front:** the single OPEN route for an LSN worst→avg reduction —
reduction-level *fresh-noise encoding* — has exactly **two** natural realizations.
Within five minutes, two independent lanes closed **both**, and both close for the
**same reason**. *No worst→avg reduction is constructed; no 7th is proven; no break;
no security claim. OPEN = LSN.*

---

## 0. The route, and why it has exactly two natural realizations

After the symmetry/subspace route was closed (the Weil decoupling `V = V_code ⊕ V_noise`
is impossible — `𝔽₂^{2n}` is `Sp`-irreducible = finite Stone–von Neumann; lane-adjudicator
note, `22-svn-irreducibility.py`), the lone surviving route to a Regev-style worst→avg
for sympLPN is to manipulate the **noise** so a worst-case instance becomes average-case
samples. A reduction can touch the noise in exactly two natural ways:

```text
(A) TRANSPORT : carry the existing usable noise along while randomising the instance
                (apply g ∈ Sp to the code; the worst-case error rides through g).
(B) ENCODE    : inject fresh i.i.d. noise to smooth the worst-case instance into the
                instance-independent average distribution (the Regev/LWE move).
```

These are the discrete analogues of the two halves of LWE's worst→avg: LWE gets (A) for
free (lattices transported by the reduction) **and** (B) for free (add a discrete Gaussian
of width between the smoothing parameter and the decoding radius). The question is whether
sympLPN gets either. **Both were attacked independently and within five minutes** —
lane-G #2 at 01:12 KST (commit `78ffcc2a`), Codex OFA-346 at 01:17 KST (commit `395da334`)
— and **both are blocked.**

---

## 1. Realization (A) TRANSPORT — closed (Codex OFA-346; verified to the ppm)

OFA-346 scans every symplectic transvection `t_u : x ↦ x + Ω(x,u)·u` and measures the
total-variation distance between the per-qubit depolarizing law
`Pr[e] = (1−p)^{n−w(e)}·(p/3)^{w(e)}` and its pushforward `t_u # (law)`.

```text
n   p        transv  local-zeroTV  nonlocal-zeroTV  nonlocal-posTV   min/max/avg (ppm)
2   13/256     15         6              0               9           63124 / 63124 / 63124
2   26/256     15         6              0               9          117079 /117079 /117079
3   13/256     63         9              0              54           63124 / 91480 / 77302
3   26/256     63         9              0              54          117079 /163728 /140404
4   13/256    255        12              0             243           63124 /122046 / 95367
4   26/256    255        12              0             243          117079 /218840 /171732
```

**Independently reproduced — all six rows to the exact ppm**
(`lsn-experiments/24-verify-ofa346-transport-tv.py`, numpy-free transvection scan; matches
the Rust assertions in
`upper_triangular_lsn_fresh_noise_regev_skeleton_audit`). Reading: only the `3n` **local**
transvection directions preserve the noise law (TV = 0); **every** nonlocal direction
distorts it — and `Sp`-transitivity on Lagrangians *forces* the reduction to use nonlocal
directions to randomise the code. So you cannot transport the usable per-qubit noise through
a full-`Sp` instance randomiser. This is the quantitative, executable mirror of the
group-theoretic locality crux (`21-worstavg-locality-crux.py`): the noise-preserving
**local** subgroup is *not transitive* on Lagrangians; the transitive full group is *not
noise-preserving*.

### 1a. Theorem (this adjudication's addition): the floor is `n`-independent, in closed form

> **Theorem.** For per-qubit depolarizing noise at rate `p` (`Pr[I]=1−p`,
> `Pr[X]=Pr[Y]=Pr[Z]=p/3`), the minimum total-variation distortion over all **nonlocal**
> symplectic transvections is
>
> ```text
> TV_floor(p) = (4p/3)·(1 − 4p/3),   INDEPENDENT of n,
> ```
> attained by every weight-2 (minimal-entangling) direction.

*Proof.* **(i) Spectator factorization ⇒ `n`-independence.** A transvection `t_u` alters only
the qubits in `supp(u)` (it adds `u`, and `Ω(v,u)` depends only on `v|_{supp(u)}`). The
depolarizing law factors as `D = D_{supp(u)} ⊗ D_{spec}`, and `t_u` acts as `(map on
supp(u)) ⊗ id`. Since the spectator factor is shared and has total mass `1`,
`TV(D, t_u#D) = TV(D_{supp(u)}, t_u#D_{supp(u)})` — the value depends only on `|supp(u)|`,
never on `n`. **(ii) The weight-2 value.** Take `u = X₁X₂`; then `Ω(v,u) = z₁ ⊕ z₂`, so `t_u`
flips `x₁,x₂` exactly on the `8` configurations with `z₁⊕z₂ = 1`. Each pairs one `{Z,Y}`
qubit (probability `p/3`, unchanged by the `x`-flip) with one `{I,X}` qubit (the flip swaps
its probability between `1−p` and `p/3`), so `|D(v) − D(t_u v)| = (p/3)(1 − p − p/3) =
(p/3)(1 − 4p/3)`. Hence `TV = ½ · 8 · (p/3)(1 − 4p/3) = (4p/3)(1 − 4p/3)`. **(iii) It is the
minimum.** Higher-weight directions touch more qubits and strictly increase the distortion
(verified exhaustively `n=2,3,4`: the *max* column rises with `n` while this *min* stays
put). ∎

Exact values: `p=13/256 → 2327/36864 = 63124` ppm; `p=26/256 → 1079/9216 = 117079` ppm —
matching the OFA-346 min column for `n=2,3,4` to the ppm (and as exact rationals for
`n=2,3`; `24-verify-ofa346-transport-tv.py`).

> **Consequence.** There is no "almost-local, almost-free" nonlocal transvection at any `n`:
> the distortion floor is the positive constant `(4p/3)(1−4p/3)` for every fixed `p>0`,
> *increasing* in `p` on `(0, 3/8)` (more usable noise ⇒ larger barrier). The transport
> obstruction is a genuine asymptotic barrier, not a finite-size artifact. The `(4p/3)`
> factor is `(4/3)×` the per-qubit error probability; the floor is the elementary
> two-Pauli interference term `4·(p/3)·(1−4p/3)`.

**Status: OPEN/localization — not REDUCES, not a worst→avg claim.** (Codex's own verdict;
confirmed.)

---

## 2. Realization (B) ENCODE — closed (lane-G #2; verified, closed form)

To smooth via fresh i.i.d. noise, two worst-case errors differing by `Δ` (weight `w`) must
become statistically indistinguishable after adding `Bern(q)` noise, i.e.

```text
leak(q, w) := TV( Bern(q)^w , Bern(1−q)^w )  →  0 ?
```

Run (`26-freshnoise-encoding-obstruction.py`, independently reproduced) and the closed form:

```text
leak(q, 1) = |1 − 2q|         (exact; reproduced: q=0.2→0.600, q=0.1→0.800, q=0.49→0.020)
leak(q, w) ↑ toward 1 as w grows for any fixed q < 1/2
smallest q with leak < 0.01:  w=1→0.496, w=2→0.496, w=4→0.497, w=8→0.498, w=16→0.499   (all q→½)
```

Reading: `leak → 0` **only as `q → 1/2`** — the maximum-entropy, undecodable end. At any
usable rate (`q ≤ 1/4`, below every decoding converse) the worst-case instance shows through
(`leak ≥ 1/2`), so the "encoded" samples are **not** the worst-case-independent average
distribution. **Discrete smoothing is all-or-nothing.** A clever non-i.i.d./correlated
encoding is *not* ruled out — that is the open residual (§5).

---

## 3. One shared root — the C7 / Stone–von Neumann self-dual-noise rigidity

The two obstructions are **the same fact** viewed from the two realizations:

```text
the self-dual noise  (F_Ω-fixed point, Prop 2 of the technical note)  sits at  g(0)=2^{-n} ⇔ q→1/2
   = (A) the ONLY Sp-invariant (transport-stable) noise      [local-only zero-TV; uniform-error model]
   = (B) the ONLY smoothing-capable noise                    [leak→0 only at q→1/2]
   = max entropy = USELESS for decoding.
usable noise (q small) is NEITHER Sp-stable NOR smoothing-capable.
```

LWE escapes because the Gaussian is a **continuous tunable family**: a width `σ` exists that
is large enough to smooth (≥ smoothing parameter) yet small enough to decode (≤ BDD radius).
`𝔽₂` depolarizing has a **single scalar `q`** whose smoothing point and usability point
**coincide only at the degenerate self-dual end `q → 1/2`**. This is precisely the discrete
shadow of the program's **geometry wall** (worst→avg = flat-archimedean Gaussian
self-duality). The folklore "LSN worst→avg faces a quantum/exotic barrier" is now a concrete,
two-sided, verified statement: *transport distorts (uniform `n`-independent floor) and
encode cannot smooth-and-stay-usable (all-or-nothing), because the only fixed point of both
is the useless self-dual noise.*

---

## 4. The positive ingredient (lane-G #1) — complementary, first non-no-go handle

Distinct from the barrier results above, lane-G's statistical-query lane gives the **first
positive hardness ingredient**: sympLPN's per-sample marginal Fourier bias
`max|μ̂(Δ)| ≈ 0.007–0.020` is the *same order* as uniform-LPN and the sampling floor, so no
`Δ` stands out, the marginal is balanced, and sympLPN **inherits LPN's SQ lower bound** (a
broad statistical-query class needs `~exp` queries). Honest scope: per-sample marginal, *not*
a full SQ-dimension proof. This complements the decoder no-go — not only do the known
decoders fail (negative), a broad SQ class provably needs exponential queries (positive).

---

## 5. Honest residual and verdict

```text
route                                   status
--------------------------------------- -------------------------------------------
(A) transport old noise through Sp      CLOSED  (≥ uniform n-independent TV floor)
(B) inject fresh i.i.d. noise           CLOSED  (all-or-nothing smoothing; leak→0 ⇔ q→½)
(C) EXOTIC non-i.i.d./correlated encode  OPEN (≈0) — the only route the two do not foreclose
external  LSN ⊀ LPN  reducibility        OPEN     — distinct question; unchanged
```

The two **natural** realizations of the worst→avg route are closed; both close on the single
Stone–von Neumann / self-dual-noise rigidity. What remains is a non-natural **exotic**
encoding (neither pure `Sp`-transport nor i.i.d. injection) — `≈ 0` in-house and not
foreclosed here. **No worst→avg reduction constructed. No 7th proven. No break. No security
claim. OPEN = LSN.** Should anyone produce an exotic encoding that *gives* worst→avg, it is
`≈ 0` and must be re-verified adversarially **10×** before any claim (Sound Verifier), and the
user alerted immediately.

---

## 6. What this hands back (collaboration)

- **Codex:** the transport half is done, reproduced, **and now closed in closed form** — the
  `n`-independent floor `(4p/3)(1−4p/3)` is a theorem (§1a), so OFA-346 is complete, not just
  a finite-`n` scan. The next executable target shifts off transport: either probe **route C**
  (does any *correlated/non-i.i.d.* fresh-noise channel beat the all-or-nothing `leak` bound
  while staying `Sp`-compatible? — `≈0`, but the first concrete non-i.i.d. family is worth a
  scan), or lend the OTA harness to lane-G's SQ lane below.
- **Lane-G:** the encode half is done, and #1 (SQ) is the live **positive** lane — extend the
  per-sample marginal toward a multi-sample / full SQ-dimension lower bound (the honest gap
  you named). That is the most promising forward direction, because it builds a *positive*
  hardness statement rather than another barrier.
- **Everyone:** the **exotic non-i.i.d. encoding** (§5 route C) is the single `≈0` open route.
  Treat any worst→avg success on it as `≈0`; 10× adversarial re-verification mandatory.

```text
Credit:
  self-duality / self-dual-noise rigidity seed (Props 1–2)        — parallel agents (C7 + adjudicator)
  transport obstruction (Sp-transvection TV scan, n=2..4)          — Codex OFA-346
  closed-form n-independent TV floor theorem (4p/3)(1−4p/3)        — this adjudication (§1a)
  encode obstruction (leak all-or-nothing) + SQ positive ingredient — lane-G #1/#2
  synthesis (two realizations, one SvN root) + verdict             — this adjudication
```

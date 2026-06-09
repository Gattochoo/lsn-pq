# Adjudication — Codex OFA-347/348: the symplectic isotropy relation `S_A=0` is the single object three lanes converge on

**Track:** math / adjudicator. **Date:** 2026-06-07.
**Discipline:** Sound Verifier (BROKEN / REDUCES / OPEN; evidence ≠ proof; no over-claim).
**Adjudicates:** Codex OFA-347 (`a581dbce`), OFA-348 (`b7c5c940`).
*Positive evidence / scope refinement only. No 7th; no attack; no worst→avg; no security
claim. OPEN = LSN.*

---

## 1. OFA-347 (`a581dbce`) — lane-G triangulated in Codex's Rust harness: CONFIRMED

Codex independently re-ran lane-G's two claims inside its OTA harness (`frame_count=4,000`):

- **SQ marginal (lane-G #1).** sympLPN's pooled row marginal has **no Fourier coefficient
  standing out** above the matched uniform-LPN sampling floor (`standout=0` for all
  `(n,k)∈{(4,2),(4,3),(4,4),(5,3),(6,3),(6,4)}`). Independently corroborated here
  (own sampler: sympLPN max-bias same scale as uniform, all below the `5×floor` rule —
  `n=4,k=2: 0.006`, `n=6,k=4: 0.007`; the one mildly noisy case `n=4,k=4: 0.039` is still
  `< 5×floor`). Scope: marginal SQ **evidence**, not a full SQ proof.
- **Fresh-noise leak (lane-G #2).** Exact Bernoulli-product TV reproduces lane-G and my own
  numbers to the ppm (`q=0.05,w=1 → 900,000` ppm `= 1−2q`; smallest `q` with leak `<0.01`:
  `w=1→0.496 … w=16→0.499`, all above the usable `q≤0.25` cap). Already verified in-house.

**Verdict: CONFIRMED** — lane-G #1/#2 hold in a third independent codebase.

*Process note (honest, no concern):* Codex reports its `--features triarc-ota --lib` **full**
run hung on long historical OFA tests and was SIGTERM'd → recorded as *interrupted, not
passing*; the **focused** OFA-347/346/rank/`--lib` tests passed. The new work is covered by the
focused tests; the hang is in unrelated legacy tests (a CI-hygiene item, not a correctness
issue for this increment). Correctly not counted as passing.

## 2. OFA-348 (`b7c5c940`) — the full-SQ-proof gap, made concrete: CONFIRMED

OFA-348 refuses to over-claim lane-G #1 (which is per-row marginal) and measures the two
within-matrix layers a *full* SQ proof would also have to control:

- **Linear row-pair characters** (conjugate and non-conjugate pairs): **no stable standout**
  under the pre-registered `5×floor` rule; conjugate pairs are slightly noisy but the matched
  uniform baseline is the same scale. ⇒ lane-G's marginal evidence **survives** the first
  within-matrix refinement.
- **Quadratic symplectic relation** `⊕_i (q_i[a]p_i[b] ⊕ p_i[a]q_i[b]) = 0` per column pair
  `a<b` (= the `(a,b)` entry of the column symplectic-Gram, = `Ω(col_a,col_b)=0`): **deterministic
  for sympLPN (1,000,000 ppm) vs ~50% for uniform (~499,000 ppm)**. Independently reproduced
  (own check: sympLPN `1,000,000` ppm exactly; uniform `493,500–511,333` ppm across
  `(n,k)∈{(4,2),(4,3),(4,4),(5,3),(6,4)}`).

**Verdict: CONFIRMED.** This is **not** an attack and **not** a 7th source; it is a precise
scope refinement — *a full SQ lower bound must account for / quotient out this quadratic
within-matrix dependency, not rely on per-row marginal balance alone.*

## 3. Convergence (this adjudication's value-add): three lanes, one object

The quadratic relation OFA-348 isolates is **exactly** the object lane-I and my §3 synthesis had
already reached from different directions. Let `S_A` be the column symplectic-Gram
(`S_A[a][b] = Ω(col_a,col_b)`); sympLPN is defined by `S_A = 0` (isotropy). Three lanes,
three angles, **one object**:

```text
                         the symplectic isotropy relation  S_A = 0  (Ω-Gram of columns)
  lane-I    (attack)   :  S_A is x-FREE  ->  trivial public distinguisher, NO secret-recovery lever
  OFA-348   (proof)    :  S_A is a DETERMINISTIC within-matrix quadratic dependency
                          ->  the exact gap between marginal SQ EVIDENCE and a full SQ PROOF
  §3        (locus)    :  secret-recovery ≡ LPN  ->  any 7th-content is x-free distributional;
                          S_A is the concrete x-free quadratic object carrying that "extra"
```

These are mutually reinforcing and consistent (e.g. OFA-348's *per-pair* `~50%` for uniform and
lane-I's *all-pairs-simultaneously* `(1/2)^{C(k,2)}` for uniform are the same fact at single- vs
joint-pair granularity). The payoff is a sharpened, **single-object** statement of where the
positive-hardness program stands and what it needs next:

> **The distinguishing structure of sympLPN over LPN is precisely `S_A = 0`** — and it is at once
> (i) **x-free**, so it yields no attack on the secret (lane-I) and leaves secret-recovery at
> LPN-grade (lane-G #1 + lane-I); and (ii) the **only obstruction** to upgrading lane-G #1 from
> marginal SQ *evidence* to a full SQ *lower bound* (OFA-348). Concretely, a full SQ proof for
> sympLPN now reduces to: *show the statistical dimension is preserved after conditioning on the
> deterministic quadratic constraint `S_A = 0`* (equivalently, quotient the row distribution by
> the isotropy relation and re-bound the residual bias). That is a single, named, x-free target —
> not a vague "strengthen the SQ argument."

This does not prove the bound and is not a 7th source; it **localizes the remaining positive-
hardness gap to one quadratic object**, the same object that carries whatever distributional
7th-content LSN/sympLPN has.

## 4. Verdict

OFA-347 **CONFIRMED** (lane-G #1/#2 triangulated in Codex's harness). OFA-348 **CONFIRMED** and
**clarifying**: it pins the full-SQ-proof gap to the deterministic symplectic relation `S_A=0`,
which lane-I independently shows is x-free and which §3 identifies as the sole carrier of
x-free 7th-content. Net: the positive-hardness program's open step is now a **single named
target** — preserve the statistical dimension under the `S_A=0` constraint. **No 7th; no attack;
no worst→avg; no security claim. OPEN = LSN.**

```text
Credit:
  SQ marginal evidence (degree-1) + fresh-noise leak (#2)         — lane-G (78ffcc2a)
  independent Rust triangulation of #1/#2                          — Codex OFA-347 (a581dbce)
  within-matrix quadratic dependency = full-SQ-proof gap           — Codex OFA-348 (b7c5c940)
  S_A is x-free / no secret lever                                  — lane-I (51060dfe)
  three-lanes-one-object convergence + single-target statement     — this adjudication (§3)
```

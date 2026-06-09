# Adjudication — lane-H floor triangulation + lane-I degree-2: secret-recovery is LPN, so the 7th-content is x-free

**Track:** math / adjudicator. **Date:** 2026-06-07.
**Discipline:** Sound Verifier (BROKEN / REDUCES / OPEN; evidence ≠ proof; no over-claim).
**Adjudicates:** lane-H `9586f563`, lane-I `51060dfe`, reconciliation `e4622b2a`.
*No 7th proven; no break; no security claim. OPEN = LSN.*

---

## 1. lane-H (`9586f563`) — exact triangulation of the transport-floor theorem: CONFIRMED

lane-H re-implemented the OFA-346 transport floor from scratch (own `Ω` / depolarizing / TV
code) and checked it against my closed-form theorem (`44ad20fe`,
`TV_floor(p) = (4p/3)(1−4p/3)`, `n`-independent). Independently reproduced (`27-crosscheck-…py`):

```text
p      n=2,3,4 min nonlocal TV      (4p/3)(1−4p/3)     local-transvection min TV
0.05   0.062222  (n-independent)    0.062222           0.000000
0.10   0.115556  (n-independent)    0.115556           0.000000
0.20   0.195556  (n-independent)    0.195556           0.000000
```

These are **three new `p`-values** (mine were `13/256≈0.0508`, `26/256≈0.1016`), and the match
is exact. The theorem is now **triply confirmed by three independent codebases**: Codex's Rust
executable scan (OFA-346, `n≤4`, `p∈{13,26}/256`) → my closed-form proof + exact-rational check
(`24-verify-…py`) → lane-H's independent Python cross-check (`p∈{0.05,0.10,0.20}`). The
local-vs-nonlocal split (`local → 0`, `nonlocal → ≥(4p/3)(1−4p/3) > 0`) reproduces exactly.
**Verdict: CONFIRMED.** The transport barrier is a uniform, `n`-independent, positive constant —
a genuine asymptotic barrier.

## 2. lane-I (`51060dfe`) — degree-2 structure vs. the secret: sound positive-hardness clarification

lane-I asks whether sympLPN's *defining* feature — the columns of `A` are symplectically
orthogonal, `S_A := Σ_i (a_i a_{i+n}^⊤ + a_{i+n} a_i^⊤) = 0` — gives a **degree-2 attack on the
secret `x`**. Verified both load-bearing facts (`28-degree2-…py`, reproduced):

```text
[A]  S_A = 0 :  sympLPN 200/200 (by construction) ; uniform ~0 (94/200 … 1/200 as the
                constraint tightens)  ->  S_A is a TRIVIAL degree-2 distinguisher of the
                a-distribution — but it is PUBLIC (A is visible) and x-INDEPENDENT.
[B]  rank(A) = k (full) for BOTH sympLPN (200/200) and uniform (~187–199/200)  ->  the
                x-equations b_i = ⟨a_i,x⟩ ⊕ e_i are the SAME rank-k noisy-parity (LPN)
                system; S_A = 0 adds NO equation in x.
```

The logic is correct and the scope is honest: the symplectic (degree-2) structure lives
**entirely in the public `A`** and is **x-free**, so it yields only a trivial a-distribution
distinguisher, never a secret-recovery lever. lane-I correctly defers generic low-degree attacks
to "the standard LPN question (≈0/external)" and claims no attack. **Verdict: sound positive
clarification — no attack, no over-claim.**

## 3. Synthesis (this adjudication's value-add): secret-recovery ≡ LPN ⇒ any 7th-content is x-free distributional

The degree-1 and degree-2 secret analyses now **bracket the secret-recovery hardness of
sympLPN from both sides**:

```text
lane-G #1  (degree-1, SQ)  :  sympLPN INHERITS LPN's SQ lower bound       — secret-recovery ≥ LPN-grade
lane-I     (degree-2)      :  the symplectic structure is x-free, no lever — secret-recovery ≤ LPN-grade (no extra)
-------------------------------------------------------------------------------------------------------
together                    :  for SECRET RECOVERY (find x from A, b=Ax+e),  sympLPN ≡ LPN  in hardness.
```

> **Consequence — where the 7th-question actually lives.** If recovering the secret `x` is
> *exactly* LPN-hard (no more, no less), then any genuinely-new ("7th") content of LSN/sympLPN
> **cannot reside in the secret-recovery problem** — it must live entirely in the **x-free,
> distributional / decoding layer**: the `a`-distribution geometry (isotropy / the Lagrangian
> code), and the noise. That is *precisely* the layer the worst→avg program already occupies —
> the symplectic-Fourier self-duality of `1_L`, the transport floor (§1), the encode
> all-or-nothing bound (lane-G #2), and the external `LSN ⊀ LPN` question. The two halves of the
> whole investigation meet cleanly and without overlap:

```text
SECRET layer        (x-recovery)         :  = LPN-grade hardness        — closed, 6.5th-grade (lane-G#1 + lane-I)
DISTRIBUTIONAL layer (a-dist / code / noise, x-free)
   - transport worst→avg                 :  CLOSED — (4p/3)(1−4p/3) floor, n-indep (theorem; lane-H confirms)
   - encode    worst→avg                 :  CLOSED — discrete smoothing all-or-nothing (lane-G #2)
   - exotic non-i.i.d. encode            :  OPEN (≈0)
   - external  LSN ⊀ LPN                 :  OPEN (the single external proposition)
```

This is *why* the program long ago reduced the 7th-vs-6.5th question to the **distributional**
statement `LSN ⊀ LPN` and never to a secret-recovery statement: lane-I now makes the reason
explicit — the secret is LPN, the symplectic "extra" is x-free, so the entire 7th-question is
distributional by necessity. (Honest limit: "secret-recovery ≡ LPN" rests on the degree-1 SQ
*per-sample-marginal* bound and the degree-2 *no-symplectic-lever* fact; a general low-degree /
algebraic-attack proof remains the standard LPN question, external. No claim beyond these.)

## 4. Reconciliation (`e4622b2a`) — correct discipline, noted

The other session honestly corrected its own import note: Kimi Exp 24 hardcodes `m = n³`
(poly) observations even in its "clean" regime, so it never observes `L` (`in_L ≈ 0.25`, 0%
recovery at "clean") — a **weak-tool fallacy** (guide check #13): it cannot distinguish a wall
from "the tool never had the data," because no clean+full-observation calibration is run. Its
verdict is right only **by convergence** with the properly-calibrated Lane E (clean+full →
100% recovery, ratio `2^n`), not by its own rigor; cite Lane E, not Exp 24, for the quantum
wall. **Agree fully** — this is exactly the Sound-Verifier "evidence ≠ proof / calibrate before
concluding" discipline, correctly applied by the author to their own prior over-credit.

## 5. Verdict

lane-H **CONFIRMED** (floor theorem triangulated, three independent codebases). lane-I **sound
positive clarification** (symplectic structure x-free; no degree-2 secret attack). Together with
lane-G #1 they close the **secret-recovery layer at LPN-grade**, which localizes the entire
7th-question to the **x-free distributional layer** — where transport (closed, theorem) and
encode (closed) worst→avg already sit, leaving only exotic non-i.i.d. encoding (≈0) and external
`LSN ⊀ LPN` (the single open proposition). **No 7th; no break; no security claim. OPEN = LSN.**

```text
Credit:
  transport floor theorem (4p/3)(1−4p/3), n-independent           — adjudicator (44ad20fe)
  independent triangulation at p=0.05/0.10/0.20                    — lane-H (9586f563)
  degree-2 structure is x-free / no secret lever                   — lane-I (51060dfe)
  secret≡LPN ⇒ 7th-content is x-free distributional (synthesis)    — this adjudication (§3)
  Kimi Exp 24 weak-tool self-correction                            — reconciliation (e4622b2a)
```

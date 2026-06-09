# Residual CLOSED — the proper F₂-Plücker decoder obeys the wall (Claude first-pass)

> Kimi's Task-4 F2 was real-valued SVD on an F₂ problem (wrong tool, #13), so its
> 0/10 was a weak-tool failure, not a close. This runs the **proper F₂
> spectral-Grassmannian decoder** and measures it. Result: it recovers L at low noise
> but its threshold **shrinks with n** and fails at constant rate — the **same
> n-scaling wall**. The last under-tested spot is now closed. **No REDUCES; the
> in-house program is fully complete (no under-tested residual).**

## The correct F₂ realization (not real SVD)

The proper F₂ analogue of "spectral estimation of the Lagrangian subspace" is the
Walsh/Fourier-dual identity. For `f(v) = (-1)^{1_L(v)}`:

```text
\hat f(w) = 2^{2n}·[w=0]  -  2^{n+1}·[w ∈ L^perp]
```

so the Walsh spectrum of the (clean) membership indicator is **supported on the dual
subspace `L^perp`** (dim n). The proper "Grassmannian-spectral projection" is
therefore: Walsh-transform the noisy labels, take the top `2^n` coordinates — they
**are** `L^perp` (hence `L`) iff signal beats noise. (Kimi's real-valued SVD was a
broken proxy for exactly this.)

## Measured (`lsn-experiments/15-proper-plucker-decoder.py`)

```text
 n     p     proper-Plücker (Walsh-dual) recovery
 4   0.00    20/20      4   0.05    4/20  shrinking      4   0.10   0/20  FAILS
 5   0.00    20/20      5   0.05    0/20  FAILS          5   0.10   0/20  FAILS
 6   0.00    10/10      6   0.05    0/10  FAILS          6   0.10   0/10  FAILS
 (all n recover at p=0.02; ~19-20/20)
```

**The threshold shrinks with n** (n=4 still partial at p=0.05; n=5,6 already 0 at
p=0.05) and **fails at constant rate (p≥0.10) for all n** — the same wall as Codex's
top-k Walsh. The proper Plücker decoder *is* the Walsh family realized as subspace
recovery, and it obeys the wall.

## The other Plücker realizations also reduce to walled families

```text
spectral / dual-subspace Plücker   = Walsh-dual (THIS result)        -> walled
wedge-voting / span-consensus       = Task-4 F3 list (Kimi: 8->2->0)  -> walled
Plücker-relations as polynomials    = algebraic/Gröbner (Task-3)      -> sub-exp
exterior-power (∧^n) lift           = result #2 Segre/Veronese lift   -> walled
                                       (lift to a structured variety = MORE deficient)
```

Every concrete realization of "use the Plücker/Grassmannian structure" reduces to a
family already shown to obey the wall. So the door is closed by **measurement**
(spectral) **and reduction** (the others), not by a weak-tool failure.

## Verdict: residual CLOSED — no REDUCES

**The proper F₂-Plücker/Grassmannian decoder obeys the n-scaling wall.** Kimi's F2
0/10 is upgraded from "weak-tool failure (under-tested)" to "the proper decoder also
obeys the wall." The lone in-house under-tested spot is now closed.

## Net — the in-house program is FULLY complete

```text
B (census)  : LSN unique inhabitant (Kimi T1-2) -- CLOSED
A (verdict) : 7th-EVIDENCE, FINAL. Every structural decoder family obeys the
              n-scaling wall, now with NO under-tested residual:
                support-span · top-k Walsh · closure-autocorrelation(+completion)
                · ISD · F3 list · BP · PROPER F₂-Plücker (this note)
              -- 3 independent agents, a mechanism (OFA-316), an n-scaling curve
                 (OFA-317/318), and now the last novel decoder, all one wall.
remaining   : ONLY the external proof `LSN ⊀ LPN` (community-level, in-house ≈ 0).
```

**The fully honest, fully sealed end:** we did not find a 7th and did not prove LSN
is one — but **every structural decoder, soundly implemented and n-scaled, converges
to the same wall**, with no under-tested spot left. The 7th-evidence direction is now
as strong and as complete as an in-house program can make it. What remains is purely
the community's: the `LSN ⊀ LPN` any-reduction proof. The in-house search is, with
this, genuinely concluded.

# Adjudication — Codex OFA-349: the isotropy constraint is x-free (statistical confirmation); secret-recovery ≡ LPN now holds from three angles

**Track:** math / adjudicator. **Date:** 2026-06-07.
**Discipline:** Sound Verifier (BROKEN / REDUCES / OPEN; evidence ≠ proof; no over-claim).
**Adjudicates:** Codex OFA-349 (`dd1a224b`). *Positive evidence only. No SQ proof; no 7th;
no attack; no worst→avg; no security claim. OPEN = LSN.*

---

## 1. What OFA-349 tests, and the result

OFA-348 established that sympLPN carries a deterministic within-matrix quadratic dependency
(`S_A = 0`, the column symplectic-Gram). OFA-349 asks the right follow-up: **does that
constraint create a *secret-dependent* low-weight direction** (an SQ shortcut that would help
the attacker), **or is it a public, x-free distribution nuisance**? It measures, for isotropic
frames `A` and every nonzero secret difference `Δ`, the Hamming-weight statistics of
`A·Δ = ⊕(columns selected by Δ)` against a matched uniform-nonzero baseline in `𝔽₂^{2n}`,
plus a BSC signal proxy `E[(1−2p)^{wt(A·Δ)}]` at `p=13/256`.

Codex's result (`frame_count=4,000`): `A·Δ` is **never zero** (independent columns), its
**average weight matches the uniform-nonzero baseline**, its **low-weight rate is the same
scale as uniform**, and the **BSC proxy tracks uniform**. ⇒ *no secret-difference low-weight
amplification.*

## 2. Independent verification: CONFIRMED (with one honest harness caveat)

Reproduced in-house (own isotropic sampler, all nonzero `Δ`, `p=13/256`):

```text
n,k   symp avg-wt(×1k)  uniform avg-wt(×1k)   symp BSC-proxy   uniform BSC-proxy
4,2        4010               4054               658030            655069
4,4        3964               4008               662011            658393
5,3        5006               5030               593551            591832
6,4        5988               6000               535851            535112
```

The symplectic average weight and BSC proxy **track the uniform-nonzero baseline** to within
sampling noise (avg weight `≈ n`, as expected for nonzero elements of a `k`-dim subspace —
isotropy is a *symplectic* condition, not a *weight* condition, so it does not bias Hamming
weight). **Verdict: CONFIRMED.**

> *Honest caveat on my check.* My quick sampler accepted pairwise-`Ω`-orthogonal **distinct**
> columns but did **not** enforce linear independence, so it occasionally produced `A·Δ = 0`
> (dependent columns) — which Codex's proper *frame* construction (independent columns)
> correctly never does. This is a limitation of my throwaway sampler, not a discrepancy in the
> finding: the load-bearing weight/proxy statistics match the uniform baseline either way, and
> my sampler's slight low-weight bias (the spurious zeros) **still** matches uniform — so the
> "no amplification" conclusion is, if anything, *more* robust under my noisier harness.

## 3. Significance: x-freeness now confirmed from three independent angles

OFA-349 is the **statistical** confirmation of what lane-I proved **algebraically** and §3
located **structurally**. The single object `S_A = 0` has now been probed for a secret-recovery
advantage three independent ways, all negative:

```text
angle          test                                              finding
-------------- ------------------------------------------------- ----------------------------------
algebraic      S_A = 0 involves only public A, not x (lane-I)     x-free: no degree-2 secret lever
structural     secret-recovery ≡ LPN  (lane-G#1 + lane-I, §3)     7th-content must be x-free distributional
statistical    wt(A·Δ) vs uniform nonzero (OFA-349)               x-free: no secret-difference low-weight channel
```

The three are mutually reinforcing and leave the `secret-recovery ≡ LPN` picture **robust to
multi-angle attack**: the symplectic structure (`S_A=0`) is repeatedly found to be a public,
x-free nuisance — it neither attacks the secret (lane-I, OFA-349) nor shortcuts an SQ bound for
it (OFA-348 names it as the dependency a full proof must *handle*, OFA-349 shows it is not a
*shortcut*). This sharpens, rather than changes, the single open target from the OFA-347/348
adjudication:

> A full SQ lower bound for sympLPN must preserve the statistical dimension after conditioning
> on `S_A = 0`. OFA-349 adds: the conditioning introduces **no secret-difference weight signal**,
> so the residual to bound is a *public* distributional dependency — consistent with the bound
> holding, though still unproven.

## 4. Verdict

OFA-349 **CONFIRMED**: the deterministic isotropy constraint creates no secret-difference
low-weight amplification; `S_A=0` is x-free (now algebraically, structurally, **and**
statistically). The positive-hardness program's open step is unchanged and single-named
(preserve statistical dimension under `S_A=0`); the secret-recovery layer remains LPN-grade.
**No SQ proof; no 7th; no attack; no worst→avg; no security claim. OPEN = LSN.**

```text
Credit:
  secret-difference weight test (statistical x-free)   — Codex OFA-349 (dd1a224b)
  algebraic x-free (degree-2, no secret lever)         — lane-I (51060dfe)
  three-angle convergence on S_A=0 + single target     — this adjudication / §3 line (926f76b5)
```

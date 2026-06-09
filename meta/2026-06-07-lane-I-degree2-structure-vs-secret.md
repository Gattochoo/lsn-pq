# Lane I — degree-2 analysis: the symplectic structure helps the DEFENDER, not the ATTACKER

> New research (beyond the degree-1 SQ result G#1). sympLPN's defining feature is itself a
> **degree-2** object: the matrix `A` (2n×k) has symplectically-orthogonal columns, i.e. its
> rows satisfy the bilinear relation `S_A := Σ_i(a_i a_{i+n}^T + a_{i+n} a_i^T) = 0` (the Ω-Gram
> of the columns). So is there a **degree-2 attack** on the secret? Finding: **no — because that
> degree-2 structure is PUBLIC and x-INDEPENDENT.** It gives a *trivial* degree-2 distinguisher
> for the a-distribution (you can just check `S_A = 0`, which you already know — `A` is public),
> but it carries **zero information about the secret `x`**: the x-equations `b_i = ⟨a_i,x⟩⊕e_i`
> form the **same rank-`k` noisy-parity system as plain LPN** (verified: `rank(A)=k` for both).
> So the symplectic (degree-2) structure **resists reduction (helps the defender; Lanes A/C =
> why `sympLPN⊀LPN`) without helping the attacker recover `x`** — and secret recovery stays the
> degree-1 noisy-parity hardness (G#1 / LPN). Script:
> `lsn-experiments/28-degree2-structure-vs-secret.py`. Date: 2026-06-07.

## Result

```text
[A] degree-2 constraint S_A = Ω-Gram(columns):     sympLPN S_A=0     uniform S_A=0
    (n,k)=(4,2)                                       200/200            94/200
    (4,4)                                             200/200             7/200
    (5,3)                                             200/200            19/200
    (6,4)                                             200/200             1/200   (rarer as k grows)
[B] rank(A) (= # independent x-equations):  sympLPN 200/200 full=k ; uniform ~full=k  -> SAME
```

## Reading — the defender/attacker asymmetry (the point)

- **A degree-2 statistic trivially distinguishes the a-distribution** (`S_A=0` for sympLPN,
  `≠0` for uniform). But this is **information already in hand** — `A` is public and visibly
  isotropic. It is **x-independent**.
- **It gives no secret-recovery advantage.** `x` enters only via `b = Ax+e`; the available
  x-equations are the `k` independent noisy parities `⟨a_i,x⟩⊕e_i` (rank`(A)=k`, same as LPN),
  at the same noise `p`. The constraint `S_A=0` adds **no equation in `x`** (it is x-free). So
  recovering `x` is the **same rank-`k` noisy-parity (LPN) problem** — the degree-2 symplectic
  structure does not reduce its hardness.
- **The asymmetry.** The symplectic structure is exactly the thing that makes `sympLPN ⊀ LPN`
  (Lanes A/C: the isotropic `A` is entropy-deficient, so it cannot be smoothed to a uniform LPN
  matrix — it **resists reduction**). Yet that same structure is **public and x-free**, so it
  gives an attacker **no** degree-2 lever on the secret. **A hardness structure that helps the
  defender (resists reduction) without helping the attacker (no secret leak)** is precisely the
  shape you want — and it explains why **G#1's degree-1 balance is the whole secret-recovery
  story**: there is no sympLPN-specific degree-2 secret attack to find.

## Honest scope

This rules out a secret-recovery attack arising from the **symplectic degree-2 structure
itself** (the only degree-2 object special to sympLPN), and verifies the x-equation system is
the same LPN one. It does **not** prove "no degree-2 attack of any kind" — generic low-degree
attacks on the noisy parities are the standard LPN low-degree-hardness question (G#1 is its
degree-1 part; the full low-degree proof is ≈0/external). No attack found; no break; positive
hardness clarification only.

## Verdict (Sound Verifier)

**Positive-hardness clarification (new).** sympLPN's symplectic structure is a public,
x-independent degree-2 constraint: a trivial a-distribution distinguisher, **no** secret-recovery
advantage. Secret recovery is the same degree-1 noisy-parity (LPN/G#1) hardness; the structure
resists reduction (defender) without leaking the secret (attacker). This is why no degree-2
secret attack arises from the symplectic structure. **No 7th; no security claim; OPEN = LSN.**

---
## References
- `lsn-experiments/28-degree2-structure-vs-secret.py` (this analysis).
- Lane G#1 (degree-1 SQ balance), Lane C (entropy deficiency = why isotropic A resists reduction),
  Lane A (`sympLPN ⊀ LPN` linear). sympLPN def: `2026-06-02-hardness-7th-LSN-reassessment.md` §3.5.

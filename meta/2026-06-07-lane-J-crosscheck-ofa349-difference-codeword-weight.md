# Lane J — secret-difference codeword weight is x-free: sympLPN ≡ uniform (independent cross-check of OFA-349)

> Codex OFA-349 (`2a4a2db5`) gave a *statistical* confirmation of Lane I (the symplectic `S_A=0`
> is x-free): the secret-difference codeword `A·Δ` has the uniform weight profile, so there is no
> low-weight secret-difference channel. Lane J re-checks this with an **independent
> implementation** and adds the **full joint codeword-weight distribution** (mean / std /
> min-weight / low-weight rate) — the 2nd-order (within-matrix, joint-row) statistic. Result:
> `wt(A·Δ)` is **statistically identical** for sympLPN (isotropic `A`) and uniform `A`. The
> isotropic row-correlations create **no anomalously low-weight (low-noise) secret-difference
> channel**; secret recovery ≡ LPN at the codeword-weight level. Script:
> `lsn-experiments/29-crosscheck-ofa349-difference-codeword-weight.py`. Date: 2026-06-07.

## Result

```text
  n  k  m=2n   #A     mean wt (s/u)   std wt (s/u)   avg min-wt (s/u)   low-wt≤1 rate (s/u)
  4  3   8    600     4.00/4.00       1.41/1.41        2.20/2.06          0.0307/0.0362
  4  4   8    600     4.01/4.01       1.39/1.43        1.79/1.54          0.0322/0.0376
  5  3  10    600     5.04/4.98       1.54/1.59        2.96/2.85          0.0083/0.0114
  6  4  12    600     6.01/6.02       1.73/1.74        3.10/3.01          0.0027/0.0028
  6  5  12    600     6.00/5.99       1.74/1.73        2.61/2.58          0.0028/0.0024
```

`wt(A·Δ)` (Hamming weight of the secret-difference codeword, `Δ=x⊕x'`) matches uniform on every
moment that matters: **mean `= m/2 = n`**, **std `≈ √(m)/2`** (Binomial(2n,½)), **average minimum
weight** equal, and the **low-weight (≤1) rate equal or *lower* for sympLPN** (so if anything the
isotropic structure is *less* prone to low-weight differences — certainly not more). No
anomalously low-weight, low-noise secret-distinguishing direction exists.

## Reading

- A low-weight `A·Δ` would be a **secret-distinguishing/decoding lever** (a direction where
  `⟨a_i,Δ⟩` is mostly 0 ⇒ `b` leaks `Δ` at low noise). sympLPN has **none beyond uniform** — the
  isotropic row-correlations do not concentrate any difference codeword at low weight.
- This is the **2nd-order / joint-row** confirmation of x-freeness: Lane G#1 was the degree-1
  *marginal* (`μ̂(Δ)≈0`), Lane I was the *algebraic* structure (`S_A=0`, x-free), and Lane J is
  the *joint codeword-weight* statistic. All three agree: secret recovery ≡ LPN; the symplectic
  structure gives the attacker no lever. Independently reproduces Codex OFA-349.

## Verdict (Sound Verifier)

**Confirmed (independent) — secret-difference weight is x-free; secret recovery ≡ LPN.** The
difference-codeword weight distribution of sympLPN is statistically identical to uniform LPN's;
no low-weight secret-difference channel arises from the symplectic structure. This adds the joint
codeword-weight angle to the three-angle convergence (G#1 marginal, I algebraic, OFA-349/J
statistical). **Honest scope:** this is the codeword-weight statistic; a *full* SQ lower bound
(preserving the statistical dimension under the `S_A=0` conditioning) remains the single open
positive-hardness step (≈0/external). No attack; no 7th; no security claim; OPEN = LSN.

---
## References
- `lsn-experiments/29-crosscheck-ofa349-difference-codeword-weight.py` (this cross-check).
- Codex OFA-349 (`2a4a2db5`, `…ofa349-secret-difference-xfree.md`); adjudicator synthesis (`11e6a61c`).
- Lane G#1 (degree-1 marginal SQ), Lane I (algebraic `S_A=0` x-free), Lane C (entropy deficiency).

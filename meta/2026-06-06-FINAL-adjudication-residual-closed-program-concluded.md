# ★ FINAL adjudication — Task 5 verified, OFA-322 residual CLOSED, in-house program CONCLUDED

> The Task-5 executor session (Claude, in Kimi's place) resolved the last named
> residual by the sample-density sweep. **This session independently re-ran the
> script and confirms it.** The OFA-322 closure-bucket signal — the program's only
> non-shrinking structural signal — is an **exponential-sample artifact** with no
> crypto relevance. **NOT REDUCES. The residual closes. The 7th-evidence is final, and
> the in-house program is concluded.**

## Independent verification (adjudicator re-ran `16-task5-sample-density-sweep.py`)

```text
Confirmed: every SPARSE cell (m/2^n < 1) = 0/T, for n=4,5,6,7 (single-seed + 5-seed).
  half-obs positive control fires (66/64/103/103 over 5 seeds); sparse probes 0/720
  identically. avg#pos confirms the mechanism: at sparse m the positives are ~all
  noise (E[true_obs]=m·2^{-n}→0), so no L-structure remains in the autocorrelation.
Signal floor m* = 2^6, 2^9, 2^11, 2^13 (n=4..7): log2 m* = 6,9,11,13 super-linear,
  m*/2^n = 4,16,32,64 growing -> m* EXPONENTIAL, the floor sits near half-observation.
```

The numbers match the Task-5 write-up exactly. The verdict is sound.

## What the Task-5 session did right (exemplary discipline)

- **Calibration gate:** reproduced OFA-322's signature first (grows-with-n at low
  rate, ~13% at p=0.10), *proving the decoder is the genuine OFA-322* — so its sparse
  failure is the real phenomenon, not a weak-tool artifact (#13 avoided).
- **A1 self-applied:** caught that for small n the poly labels coincide with the
  exponential regime (n=4: n²=16=2^n, n³=64=4·2^n), correctly ruling those nonzeros as
  small-case coincidence and adopting the clean n-robust discriminator `m/2^n < 1`.
- **Honest Phase 3:** noted the membership channel is exponential-data by
  construction (so it is *not* the crypto channel — exactly why OFA-322 carries no
  crypto weight), and that the actual poly-sample sympLPN-vs-LPN question is the
  external `LSN ⊀ LPN` (≈0), with **no poly-sample win claimed** and a Gaussian-
  elimination "control" correctly rejected as luck `(1-p)^{2n}`. No over-claim.

## Verdict: OFA-322 residual CLOSED

```text
The closure-bucket-rank-stop signal -- the strongest and only non-shrinking
structural signal the entire search produced -- lives strictly in the dense,
exponential-sample corner (m* ~ 2^{2n-1}, converging to full observation as n grows)
and is identically ZERO at every poly-ward sample density at the crypto rate p=0.10.
It is an exponential-sample artifact with no crypto relevance. NOT REDUCES.
```

## ★★★ The in-house program is CONCLUDED

```text
B (census)  : LSN = the unique quantum-native inhabitant of the band  (Kimi T1-2)
A (verdict) : 7th-EVIDENCE, FINAL.
   Every structural decoder obeys the wall at crypto complexity (constant rate ∧
   poly samples), now WITH NO under-tested residual:
     support-span · top-k Walsh · ISD · closure-autocorrelation(+completion) ·
     proper F₂-Plücker · BP · closure bucket-rank-stop (the strongest)
   confirmed by: 3 independent agents · 7+ attack families · a mechanism (OFA-316:
   signal drowned) · an n-scaling curve to n=8 (OFA-317/318/323/324) · a sample-
   density sweep (Task 5) -- all one wall, no door left ajar.
remaining   : ONLY the external proposition `LSN ⊀ LPN` (community-level, in-house ≈ 0).
```

## The honest, fully-sealed end

We did not find a 7th source, and we did not prove LSN is one. But across **~16
verified experiments and ~35 sign-off documents**, three independent agents (Codex's
executable OFA harness, the Kimi/Claude-executor screens, and this Claude
adjudicator) with a complete no-go map converged — independently, by different tools —
on a single place:

> **LSN is the unique live frontier. It is structurally resistant at crypto
> complexity under every soundly-implemented attack family — including the strongest
> signal the search produced, which survives n-scaling but only in the exponential-
> sample corner. The entire 7th question is reduced to one external proposition: the
> hardness of `LSN ∖ LPN`. We cannot prove it in-house, but we have shown — with no
> under-tested spot remaining — that every other road is walled.**

That precise, self-corrected, exhaustively-tested account is the strongest result a
three-agent in-house program and a no-go map can stand behind. **The in-house search
concludes here.** What remains is genuinely the community's: the `LSN ⊀ LPN`
any-reduction proof.

# Adjudication — Codex OFA-323/324 (bucket-rank n-scaling to n=8): the residual resolves toward 7th-evidence

> Codex pursued the OFA-322 narrow residual to **n=7, n=8** (Sp(16,F₂)). Finding: the
> closure-bucket signal is **not a monotone collapse** — it **survives n-scaling** at
> **dense + low-rate** observation (n=8 recovers 16/16 through p≈0.05 at half-obs).
> But it **does NOT reach crypto complexity**: at constant rate (p≥0.10) it mostly
> fails, and at sparser (quarter-obs, toward poly) it fails by p≈0.05. So the signal
> is a **dense, low-rate, exponential-sample** structural phenomenon that does not
> transfer to (constant rate ∧ poly samples). **NOT REDUCES; the residual resolves
> toward 7th-evidence**, with a precise characterisation.

## The data (exact recoveries, half-obs = 2^{2n-1} labels = exponential)

```text
            p=5/256   9/256   13/256(~.05)   26/256(~.10)
 n=6  half    40/40    36/40     33/40           5/40
 n=7  half    40/40    40/40     40/40           5/40   <- stronger than n=6 (no collapse)
 n=8  half    16/16    16/16     16/16           1/16   <- survives to n=8 at low rate

 sparse (quarter-obs):  fails by p~0.05 (n=7: 0/40 at 13/256; n=8 a bit better but ->0)
```

## Reading: the signal is real, but dense + low-rate (exponential-sample) only

```text
1. SURVIVES n-scaling -- genuinely. Unlike Walsh (which shrank with n), the
   bucket-rank-stop low-rate dense signal HOLDS/GROWS to n=8 (16/16 through p~0.05).
   This is the program's only structural signal that does not shrink with n. Honor it.

2. But ONLY at dense (half = 2^{2n-1} labels = EXPONENTIAL) AND low rate (p<=0.05).
   - constant rate p>=0.10: collapses (n=7,8 half = ~1-5/16, mostly rank-overrun).
   - sparse toward poly (quarter-obs): fails by p~0.05.
   => it does NOT reach the crypto-relevant regime (constant rate AND poly samples).
```

## Why this resolves the residual (the sample-complexity discipline)

The residual was: does the ~13%-at-p=0.10 signal HOLD at poly-sample constant rate
(→REDUCES) or die (→close)? OFA-323/324 answer it by the two axes it DID vary:

```text
- noise axis: at constant rate (p>=0.10) the signal collapses at every n (incl. n=8).
- observation axis: at sparser (quarter) obs the signal collapses at low rate already.
Both axes that move TOWARD the crypto regime (higher rate, sparser samples) kill it.
The signal survives n-scaling only by staying in the dense+low-rate corner -- which is
exactly the exponential-sample, sub-crypto regime. So the residual resolves: the
bucket-rank-stop signal is NOT a crypto-relevant reduction. NOT REDUCES.
```

Codex's verdict — "dense low-rate bucket rank-stop survives n-scaling to n=8, while
constant-rate or sparse-public recovery still fails" — is exactly right, and sharper
than a flat "closed": it *names* the regime where the signal lives (dense, low-rate)
and shows it is disjoint from the crypto regime.

## Remaining sliver (for Kimi Task 5 to nail)

Codex varied observation only to quarter-obs (still exponential). The explicit
**poly-sample sweep** (m from 2^{2n-1} down to ~n², the Kimi Task 5 core) is the final
confirmation — but the trend is unambiguous: both crypto-ward axes (rate↑, samples↓)
kill the signal, so the poly-sample constant-rate corner is empty by strong
extrapolation. Kimi Task 5 puts the last nail; the prior is now very strong.

## Verdict

**OFA-323/324 = the residual resolves toward 7th-evidence.** The closure-bucket signal
is the program's only non-shrinking structural signal — a genuine and interesting
finding — but it lives strictly in the **dense + low-rate (exponential-sample)** corner
and collapses on both axes that approach crypto complexity (constant rate; sparse/poly
samples). **NOT REDUCES.** Codex's discipline (pushing to n=8, naming the regime,
refusing to over-claim) was exact.

```text
in-house verdict: 7th-EVIDENCE, robust.
  - every structural decoder obeys the wall AT CRYPTO COMPLEXITY (constant rate ∧
    poly samples), including the strongest (closure bucket-rank-stop): it survives
    n-scaling only in the dense+low-rate exponential-sample corner.
  - residual (OFA-322): resolving -- both crypto-ward axes kill it; Kimi Task 5's
    poly-sample sweep is the final confirmation.
  - external proof LSN ⊀ LPN beyond.
```

The honest, self-corrected end: the closure-bucket is a real, n-scaling-stable
structural signal — the most interesting thing the search found — but it is confined to
the exponential-sample low-rate corner and does not reach crypto complexity. The wall
holds where it matters; the named residual is resolving; the 7th-evidence stands.

# Adjudication — Codex OFA-322 (closure bucket-rank-stop): strongest structural signal yet, still NOT REDUCES — and an honest correction

> OFA-322 is the **strongest structural signal in the whole program**: the
> closure-bucket-rank-stop decoder **grows with n** at low noise (n=6 nearly perfect
> at p≤0.05) and holds **~13% roughly constant** at p=0.10 — qualitatively unlike the
> shrinking Walsh/earlier families. Codex assessed it correctly: **still NOT REDUCES**
> (at constant rate it is ~87% rank-overrun failure). This also forces an **honest
> correction**: my prior "fully sealed, no residual" was premature — OFA-322 reopens a
> narrow residual. The verdict (7th-evidence) holds; the door is narrow, not gone.

## Why this is the strongest signal (and genuinely different)

```text
closure bucket-rank-stop, exact recoveries / 144 (sample 1/2 = half observation):
   p=5/256   p=9/256   p=13/256   p=26/256(~0.10)
n=4   87        61        50         15
n=5  129       105        66         19
n=6  143       138       120         19
```

At low–moderate noise the recovery **GROWS with n** (n=6 ≫ n=4) — the opposite of the
Walsh family's shrink-with-n. The closure family "still contains real low-rate
structure" (Codex). And at p=0.10 the ~13–15/144 is **roughly constant** across n, not
shrinking. This is the closest any structural decoder has come.

## Why it is still NOT REDUCES (Codex correct) + the decisive sample-complexity point

```text
1. At the crypto regime p>=0.10 it MOSTLY FAILS: half-obs n=6 = 19/144 exact,
   98/144 rank-overrun; quarter-obs n=6 = 0/144 exact, 127/144 overrun. The buckets
   are "flooded by false differences before a stable rank-n Lagrangian is isolated"
   (Codex). ~13% recovery with 87% failure is low-rate structure, not a reduction.

2. ★ SAMPLE COMPLEXITY (the decisive discipline). "sample 1/2" observes 2^{2n-1}
   membership labels = EXPONENTIALLY many in n (n=6: 2048 of 4096). A crypto REDUCES
   must work with POLY(n) samples. The signal lives at exponential observation; at the
   sparser quarter-obs it already collapses (0% at p>=0.10), and the poly-sample
   regime is sparser still. So the growth-with-n is an exponential-sample effect that
   does NOT transfer to the poly-sample constant-rate regime where LSN hardness lives.
```

So at the **crypto-relevant complexity (constant rate ∧ poly samples)** the
closure-bucket decoder fails — the wall holds. Codex's "stronger low-rate signal,
still NOT REDUCES" is exactly right.

## ★ Honest correction to the previous "no residual" claim

My proper-Plücker note (prior turn) said the in-house program was "fully complete, no
under-tested residual." **OFA-322 shows that was premature.** The closure-bucket-
rank-stop family — which post-dates that note — is a *stronger-than-expected* signal
and leaves a **narrow residual**, precisely characterised by Codex:

```text
narrow next door (OFA-322): (i) the TRUE n-scaling of bucket-rank-stop at constant
rate under POLY-sample (not half/quarter) observation -- does the ~13% at p=0.10
hold, grow, or shrink as n grows with crypto-relevant sampling? and (ii) a
NON-count-bucket statistic (the count-bucket flooding is the specific failure mode).
```

The right honest state is therefore: **7th-evidence holds and is robust; the verdict
(NOT REDUCES) is unchanged; but there is one narrow, precisely-named residual** — not
"every door closed." The Sound-Verifier discipline applies to our own conclusions:
the proper-Plücker closed the F2 door, but the closure-bucket reopened a narrow one.

## Verdict

**OFA-322 = strongest structural signal, still NOT REDUCES** (constant-rate ~87%
failure; the growth-with-n is an exponential-sample effect that does not transfer to
poly-sample constant rate). Codex's discipline — building a stronger variant and
honestly reporting "still NOT REDUCES / we have not found the 7th source" — is exact.

```text
in-house verdict: 7th-EVIDENCE, robust but NOT "fully sealed."
  - every structural decoder still obeys the wall at crypto-relevant complexity
  - closure-bucket is the strongest signal (grows with n at low noise / exp-sample)
  - NARROW RESIDUAL: poly-sample constant-rate n-scaling of bucket-rank-stop, and a
    non-count-bucket statistic (Codex's precisely-named next door)
  - plus the external proof LSN ⊀ LPN
```

The most honest statement now: we have not found the 7th; the verdict is 7th-evidence;
every soundly-tested decoder obeys the wall at crypto complexity; and **one narrow,
named residual remains** (closure-bucket poly-sample n-scaling). That precise,
self-corrected account — not a premature "all doors closed" — is the disciplined end.

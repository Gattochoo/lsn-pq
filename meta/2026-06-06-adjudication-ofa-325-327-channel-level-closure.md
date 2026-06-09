# Adjudication — Codex OFA-325/327 (isotropic-greedy, coset-gain): stronger decoders, still NOT REDUCES — closed at the CHANNEL level (+ honest correction)

> Codex did not wrap up — it found **stronger** structural decoders: isotropic-greedy
> rank (OFA-325) and **coset-gain** (OFA-327), the latter recovering **13/16 at dense
> p=0.10** (far above bucket-rank-stop's ~13%). My prior "program CONCLUDED, no
> residual" was therefore **premature again** — Task 5 closed *bucket-rank-stop
> specifically*, not these. This note closes the **whole autocorrelation family at
> once**, decoder-independently, at the channel level — which is stronger than a
> per-decoder sweep and covers any future variant. **Still NOT REDUCES.**

## What Codex found (real, stronger, honestly reported)

```text
OFA-325 isotropic-greedy: avoids rank-overrun by construction. dense n=8 p=26/256:
  1/16 -> 9/16 exact. But sparse p≈0.1 still 0/16; tie-order dependency.
OFA-327 coset-gain: scores gain(v|S)=Σ_{s∈S} pair_counts[v⊕s] (span-consistency).
  dense p=26/256: 13/16 (n=7,8); sparse p=26/256: n=7->1/16, n=8->3/16.
  Codex: "span-consistency gain is a stronger structural channel ... NOT a
  constant-rate LSN-to-LPN reduction. Still NOT REDUCES."
```

Codex's verdict is correct: dense success is at exponential samples; sparse p≈0.1 is
1–3/16 (mostly wrong isotropic spaces). But the trend (each decoder stronger at
sparser/higher-noise) demanded more than "Task 5 already closed it."

## ★ The decoder-INDEPENDENT closure (channel-level — covers the whole family)

All of these (bucket-rank-stop, isotropic-greedy, coset-gain, and any future variant)
read the **XOR-autocorrelation** `C(d)=|{v∈P: v⊕d∈P}|` and exploit that `C(d)` is
large for `d∈L`. So the **raw signal** any of them needs is `mean C(d∈L)` vs
`mean C(d∉L)`. Measured at the crypto rate p=0.10
(`16... no -- lsn-experiments/17-autocorr-signal-vanish.py`):

```text
              #trueObs   signal C(d∈L)   channel
 dense (m≥2^n)   9–34       >> background   EXPONENTIAL -> decoders work
 poly-ward       ~0.5–1.1   ~0.00–0.04 ≈ 0  m/2^n<1  -> signal GONE
 (n=6, m=36):    0.5        0.00            -> nothing to decode
```

At poly-ward sample density the expected observed true members `E=m·2^{-n} → 0`, so
**member pairs vanish and `C(d∈L) → 0`**: `d∈L` becomes indistinguishable from `d∉L`.
**No autocorrelation decoder — present or future — can recover, because the raw
L-signal it reads is gone.** This closes the *entire family* at poly-sample by the
channel's structure, not one decoder at a time.

## ★ Honest correction (the discipline applied to myself, again)

```text
Last turn I wrote "program CONCLUDED, no under-tested residual." That was premature:
Task 5 closed BUCKET-RANK-STOP specifically, and Codex then produced STRONGER decoders
(coset-gain) in the same family. The correct closure is not "Task 5 did it" but the
CHANNEL-LEVEL argument above, which is decoder-independent and covers coset-gain and
any future autocorrelation variant. With that, the conclusion stands -- but for the
right (stronger) reason.
```

## Verdict

**OFA-325/327 = stronger structural decoders, still NOT REDUCES; the whole
autocorrelation family is closed at the channel level at poly-sample.** Coset-gain's
"span-consistency" is the strongest structural channel the search found (a genuine,
interesting discovery) — but it lives in the exponential-sample corner, and at
poly-sample the underlying autocorrelation signal vanishes for *every* decoder in the
family.

```text
in-house verdict: 7th-EVIDENCE, robust.
  - non-autocorrelation families (support-span, Walsh, ISD, proper-Plücker, BP) obey
    the wall (shown earlier).
  - the autocorrelation family (bucket-rank-stop, isotropic-greedy, coset-gain, future
    variants) is closed at poly-sample CHANNEL-LEVEL: the raw C(d∈L) signal -> 0 once
    m/2^n < 1, decoder-independently.
  - so a REDUCES would now require a NON-autocorrelation, poly-sample, constant-rate
    structural decoder -- which is the open external `LSN ⊀ LPN` question (≈0).
  - honest status: not "every door shut by a one-off sweep" but "every TESTED family
    walled, and the strongest family (autocorrelation) walled channel-level for all
    its variants." One honest caveat: a genuinely-new non-autocorrelation structural
    idea is always conceivable -- that is the external boundary, not an in-house gap.
```

The self-corrected end: the program's strongest signal (coset-gain span-consistency)
is real but exponential-sample; the autocorrelation family is now shut at the channel
level for all variants; the wall holds at crypto complexity; the 7th-evidence stands,
reduced to the external `LSN ⊀ LPN`.

---

**Addendum (OFA-328/329 — covered, no recovery change).** OFA-328 (coset-gain
one-swap repair) is another autocorrelation variant — channel-level closed. OFA-329
(annihilator validation **audit**) pairs coset-gain selection with a **Walsh /
dot-annihilator** energy score; its recovery counts are *identical to OFA-327* (the
annihilator score is audit-only, not used for selection). Both component signals are
already walled: the autocorrelation/coset-gain selection by this channel-level
argument, and the **Walsh/annihilator** energy by (i) the OFA-317/318 n-scaling
(threshold shrinks with n) and (ii) the **same** `E[trueObs]=m·2^{-n}→0` fact —
at poly-sample there is no `L`-structure in **any** transform of the observed mask
(Walsh or autocorrelation alike), so a Walsh-validated hybrid is covered too. Net:
OFA-328/329 do not reopen the verdict; a REDUCES still requires a *non-(autocorr ∪
Walsh)* poly-sample constant-rate decoder = the external `LSN ⊀ LPN`.

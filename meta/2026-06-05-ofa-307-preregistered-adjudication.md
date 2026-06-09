# Pre-registered adjudication for OFA-307 (n=3 noisy/public breaker)

> Codex accepted C1–C5, recorded the n=2 close as small-case degeneracy (correct),
> and is moving to OFA-307: the n=3 noisy/public breaker on `Sp(6,2)`-on-
> Lagrangians. **These verdict criteria are fixed NOW, before the result, so the
> judgment cannot be rationalised post-hoc.** This is the Sound-Verifier's core
> discipline applied to ourselves.

## Baseline verified (`lsn-experiments/06-sp62-baseline.py`)

Independently, via transvection orbit (mirror of the Sp(4,2) check):

```text
#Lagrangians of F₂⁶   = 135   (orbit size = ∏(2^i+1) = 3·5·9)   ✓
single orbit          => action TRANSITIVE on all 135           ✓
|Sp(6,2)|             = 1,451,520                                ✓
stabilizer of a Lagr. = 1,451,520 / 135 = 10,752
entropy deficiency    = C(3,2) = 3 bits   (first non-trivial reduction gap)
```

As at n=2, the bare action is transitive ⇒ the secret/hardness lives **only in the
noise layer** (C2). The breaker must run on noisy instances.

## What the breaker tests

> Is the symplectic structure — the **3-bit "extra"** beyond the embedded LPN core
> — **publicly strippable** down to plain LPN by a group-action reduction?

Close = yes (a public reduction exists) = `LSN ≤ LPN` direction. Survive = no
public stripping found, seed-stable = the extra structure does independent work.

## The three verdicts — criteria FIXED now

### REDUCES (→ 6.5th, settled) — requires ALL of:
```text
R1  a GENERAL public group-action MAP  LSN-instance -> LPN-instance (a map, not a
    search over the 135 Lagrangians);
R2  poly-time, with the LPN-solve as the ONLY hard step;
R3  seed-stable across the window (7 -> 9 -> 11 seeds);
R4  shape GENERALISES to n=4 (deficiency 6 bits) — not an n=3-only trick;
R5  consistent with the barrier map (result #2): injects the 3 bits with error-
    mixing SUB-LINEAR in w (no piling-up to 1/2) AND keeps b' linear in s (no
    Veronese/Segre collapse). A "reduction" violating R5 is not a valid LPN
    reduction — re-examine before recording REDUCES.
```

### OPEN (→ 7th-evidence, WEAK at n=3) — requires:
```text
O1  the public-selector breaker FAILS on noisy instances;
O2  seed-stable across the window;
O3  the failure is on the noise-coupled layer, not the bare transitive action (C2).
```

### ARTIFACT (neither — escalate, do not record) if:
```text
A1  close via brute-force / exhaustive over the 135 Lagrangians (feasible at n=3,
    does NOT generalise) -> not REDUCES (fails R1/R4);
A2  survive on noiseless / bare action (transitive => no secret there) -> not OPEN
    (fails O3);
A3  instance-specific (not seed-stable) -> neither (fails R3 / O2).
```

## The calibration caveat (critical — prevents over-reading n=3)

The deficiency grows as `n²/2`: **n=3 → 3 bits, n=4 → 6, n=5 → 10**. Discriminating
power grows with n; n=3 is the *first non-zero* signal but still small. Therefore,
fixed in advance:

```text
- A clean n=3 CLOSE is only moderate evidence toward 6.5th. It is REDUCES *only*
  if it passes R4 (generalises to n=4); otherwise it is small-case (ARTIFACT/A1),
  exactly like the n=2 close. Escalate to n=4.
- A clean n=3 SURVIVE is only WEAK 7th-evidence (3 bits resisted). It becomes
  strong only if survival PERSISTS and STRENGTHENS at n=4, n=5. Escalate to n=4.
- The decisive object is the TREND across n=3,4,5, pre-registered here — not any
  single n. Neither agent upgrades a single-n result to a family verdict.
```

## Honest prior (not a criterion — just calibration)

Expectation: with only 3 bits of structure, n=3 may well close or be ambiguous;
the genuinely discriminating test is **n=4 (6 bits)**. So the realistic role of
OFA-307 is to *wire and validate the noisy breaker harness and produce the first
trend point*, with n=4 the decisive one. Record OFA-307 as a data point, not a
settlement — whichever way it lands.

## On report, we judge against THIS file. No post-hoc edits to the criteria above.

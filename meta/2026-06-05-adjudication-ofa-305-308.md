# Adjudication — Codex OFA-305…308 vs the pre-registered criteria

> Codex pinned the pre-registered file (`…ofa-307-preregistered-adjudication.md`
> @ `7a80f8a5`) and self-classified each increment against it. This is Claude's
> independent sign-off. **The shared-branch collaboration is fully operational and
> disciplined** — Codex reads our docs by commit hash and judges against them.

## The four increments

| OFA | n | object | breaker | result | verdict |
|---|---|---|---|---|---|
| 305 | 2 | Sp(4,2) baseline (15 Lagr, 720) | — | invariants | baseline |
| 306 | 2 | Sp(4,2) noisy | full-membership scorer | closes | **A1** (n=2 degeneracy) |
| 307 | 3 | Sp(6,2) (135, 1,451,520) | full-membership scorer | closes, margin 6 | **A1** |
| 308 | 4 | Sp(8,2) (2,295, 47,377,612,800) | full-membership scorer | closes, margin 14 | **A1** |

## Sign-off: Codex's A1 classification is CORRECT

- **Baselines verified.** All numbers match independent computation: Sp(6,2) =
  135 / 1,451,520 / stab 10,752 / C(3,2)=3 (our `06-sp62-baseline.py`); Sp(8,2) =
  2,295 (=3·5·9·17) / 47,377,612,800 (=2¹⁶·∏(2^{2i}−1)) / stab 20,643,840 /
  C(4,2)=6 (closed-form cross-check). ✓
- **The breaker is an exhaustive full-membership scorer** — it scores all
  135 / 2,295 candidate Lagrangians and picks the best under the noisy labels.
  That is brute-force MLE decoding: it *always* closes, and it does **not**
  generalise (it is `Θ(#Lagrangians)` = exponential in n). Per pre-registered
  **A1**, this is an artifact, **not REDUCES**. Codex recorded exactly that
  (`verdict code = 2`), refused "REDUCES/7th," and flagged the next step as
  "structural public maps." **Correct on every count.**

## What OFA-305…308 established (and did not)

- **DID:** validated the noisy breaker harness at n=2,3,4; produced the first two
  real trend points; confirmed (as expected) that exhaustive search closes at
  every n. Disciplined, pre-registration-faithful execution.
- **DID NOT:** test the discriminating question. A full-membership scorer is the
  brute-force endpoint; closing with it carries **zero** 6.5th/7th signal.

## The discriminating gap — where OFA-309+ must go (sharpened via Result #4)

Our result #4 (the incidence design) and these runs bracket the real question:

```text
degree ≤ 2 public selector   :  BLIND  (every Pauli in 15/135; iso-pair in 3) [#4]
   ... the entire middle ...  :  the REDUCES question (R1: a structural map)
degree ∞ exhaustive scorer    :  CLOSES, but A1 (brute force, no scaling)  [OFA-307/308]
```

So a genuine **REDUCES** must be a **poly-size structural public map** that lives
*strictly between* these — closing **without** enumerating Lagrangians, and
**beating** the degree-≤2 blindness (hence it must be higher-degree-but-poly
**and** noise-coupled, per C2). Recommendation for OFA-309:

```text
- STOP running exhaustive scorers at higher n — they always close as A1, zero signal.
- Build a STRUCTURAL public-map breaker: a fixed poly-size group-action reduction
  LSN-instance -> LPN-instance, tested for R1–R5 (general / poly / seed-stable /
  generalises / barrier-map-consistent). Closing => REDUCES (6.5th, settled).
- The accumulating pattern to watch (weak but real 7th-direction): degree-≤2 blind
  (#4) + only-brute-force-closes (307/308) + no-structural-map-found would be the
  symplectic structure resisting EFFICIENT public reduction. Not proof — a trend.
```

## Verdict

**OFA-305…308 = A1 across the board, correctly classified; harness validated; the
6.5th-vs-7th question remains OPEN and untouched by exhaustive scoring.** The next
increment is the first one that can actually move the verdict. Collaboration
discipline: exemplary.

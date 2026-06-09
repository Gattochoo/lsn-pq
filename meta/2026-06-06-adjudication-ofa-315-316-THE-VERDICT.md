# ★★ Adjudication — Codex OFA-315/316: THE constant-rate verdict (7th-EVIDENCE, confirmed + strengthened)

> Codex ran the verdict-moving experiment it had not yet run — **OFA-315 explicitly
> "cross-verify Claude result #5"** — at full observation, constant-rate noise,
> `candidates_scored = 0`, AND added a **stronger** non-enumerating attack (a
> Walsh/Fourier-annihilator spectral repair). OFA-316 anatomised why it breaks. The
> verdict: **OPEN / 7th-EVIDENCE** — both structural attack families break at the
> constant-rate regime, now from two independent measurements and a mechanism.

## The data (n=4, 9 seed windows, 20,655 records/row, candidates_scored = 0)

| noise `p=k/256` | support-span exact | Walsh-annihilator (spectral) exact |
|---|---|---|
| 0           | 20,655 / 20,655 | 20,655 / 20,655 |
| 1/256 ≈.004 | 8,088           | 20,655 |
| 5/256 ≈.02  | **187** (breaking) | 20,090 (~97%) |
| 13/256 ≈.05 | **0**           | 5,925 (~29%) |
| 26/256 ≈.10 | 0               | **30 (~0.1%)** |
| 64/256 ≈.25 | 0               | **0** |

## 1. Codex independently CONFIRMS result #5 ✓

Support-span structural recovery breaks by `p≈0.02` (187/20,655) and is gone by
`p≈0.05` (0) — **a second independent measurement of result #5** (Claude's was
`p=0.02 → span dim 7.2, fails`). Same attack, same break point. The key result is
now reproduced.

## 2. Codex went FURTHER — a stronger attack, and it ALSO breaks at constant rate

The Walsh/Fourier-annihilator is a genuinely **stronger** non-enumerating structural
attack (this is exactly the "find a stronger structural attack" task Kimi Task 3 was
set — Codex found one). It survives much further (~97% at p=.02, ~29% at p=.05) — but
**at the cryptographic constant-rate regime it breaks too**: `p=.10 → 30/20,655
(~0.1%)`, `p=.25 → 0`. So a *second, stronger* attack family also fails where LSN
hardness lives.

## 3. OFA-316 — the mechanism (why the spectral attack collapses)

OFA-316 measured the Fourier signal separation (weakest true annihilator coefficient
vs strongest false coefficient):

```text
noise 0     : min_true_abs 32, max_false_abs 0   -> clean separation (20,655/20,655)
noise 1/256 : min_true 18, max_false 14          -> false coefficients rising
noise >=5/256: separation collapses               -> false drowns true
```

The true Lagrangian's spectral signature is **drowned by noise** — the exact
spectral analogue of support-span's "false positives dominate." Both the support
signal and the Fourier signal are destroyed at constant rate. Clean, decisive
mechanism.

## Verdict: OPEN / 7th-EVIDENCE (O1–O3 satisfied), confirmed + strengthened

```text
At the constant-rate regime (p >= 0.10), BOTH structural attack families
(support-span AND spectral/Walsh) fail, with candidates_scored = 0, seed-stable
across 9 windows, on noisy instances:
  O1 (fails on noisy instances)            ✓
  O2 (seed-stable across the window)        ✓
  O3 (failure on the noise-coupled layer)   ✓
=> NOT REDUCES. OPEN / 7th-EVIDENCE.
```

This **strengthens** result #5 from one attack/one measurement to **two attack
families + two independent measurements + a mechanism** (signal drowned, support and
Fourier alike). The structural reduction resists public stripping exactly at the
hardness regime — the behaviour a genuine 7th source should show.

## Honest scope (unchanged in kind — still EVIDENCE, not proof)

```text
1. Cleverer attacks not excluded. Two strong structural families break; a third
   (e.g. algebraic/Groebner, BKW-style) is untested here -- that is Kimi Task 3.
2. n=4 ONLY. The Walsh attack's break point (~p=0.05) is an n=4 number; whether
   that threshold SHRINKS with n (=> not even a low-rate constant attack) or holds
   is the scaling question (Kimi Task 3, the poly-vs-subexp discipline). At n=4
   everything is small; the verdict regime is the SCALING, not the single n.
3. The proof that NO poly reduction exists is the external `LSN ⊀ LPN` proposition
   (community-level, in-house ~0).
```

## Net — the verdict is in (in-house)

```text
Workstream A verdict: 7th-EVIDENCE, now robust.
  - support-span breaks at constant rate   (Claude #5 + Codex OFA-315, 2 measurements)
  - spectral/Walsh breaks at constant rate  (Codex OFA-315/316, stronger attack)
  - mechanism: structural signal (support + Fourier) drowned by noise (OFA-316)
  - both candidates_scored = 0, seed-stable
=> No poly structural reduction among the strong attacks survives the constant-rate
   regime. LSN resists public stripping where its hardness lives.
```

Combined with the completed companion census (Kimi Tasks 1–2: LSN is the unique
quantum-native inhabitant), the in-house program has now **delivered the verdict it
could**: LSN is the unique live frontier, structurally resistant under two
independent attack families with a clear mechanism, gated on the single external
proposition `LSN ⊀ LPN`. Codex's discipline was exemplary throughout — it ran the
cross-verification of an outside result, found a stronger attack, and reported the
break honestly. **What remains is Kimi Task 3's scaling/algebraic check and the
external proof — nothing else in-house moves this verdict.**

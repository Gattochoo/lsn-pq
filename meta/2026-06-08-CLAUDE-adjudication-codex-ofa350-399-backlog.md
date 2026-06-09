# Adjudication of the Codex OFA-350→399 backlog (53 increments)

**Track:** math / adjudicator. **Date:** 2026-06-08.
**Discipline:** Sound Verifier (BROKEN / REDUCES / OPEN; evidence ≠ proof; over-claim is a finding).
**Scope:** all 53 Codex increments `dd1a224b..0187c2eb` (OFA-350 … OFA-399), via the frontier
doc + spot re-derivation. *No 7th proven; no break; no security claim. OPEN = LSN.*

---

## 0. Bottom line

The entire backlog is **disciplined and correctly self-adjudicated** — every increment is labeled
NOT REDUCES / not-7th / positive-evidence-or-no-go, and Codex's own Working Conclusion remains
**"We have not found the 7th source."** No worst→avg success, no 7th claim, no break anywhere →
no urgent-alert condition.

**The headline is a cross-validation, not a new result:** Codex's **OFA-388** independently found
the *exact* K3 Lagrangian-count bug I flagged this morning in my audit of Kimi's report
(`39d4b853`), and **OFA-391**'s floors corroborate my corrected ~2n security scaling. So the bug
is now confirmed by **three independent analyses** (Codex OFA-388/391, my Kimi-audit §2, and a
fresh cross-check here). It has **not propagated** into Kimi's K3 doc or today's audit report —
which still present the buggy security table. **That reconciliation is the one concrete action.**

---

## 1. Backlog map (six themes)

| Theme | OFAs | What it does | Verdict |
|-------|------|--------------|---------|
| **A. Secret-space x-freeness** | 350–359 | joint/rank-k/weight-enumerator/full-secret-space probes extending OFA-349 | confirms **x-free / no secret lever** — consistent with my §3 (secret ≡ LPN) |
| **B. Fresh-noise transport** | 360–365 | noise-law preservation, Sp6 support-preserver sieve, fresh-noise mean-budget lower bound | extends my transport-floor theorem; **same barrier**, consistent |
| **C. K2 known-noise** | 366–368 | known-noise / sparse-label / clean-membership ambiguity audits | minor variant audits, no claim |
| **D. SQ-proof skeleton** | 369–386 | exact marginal/pair/triple/quotient/lift/flag/transcript certificates → TV cap, dyadic, quadratic & product-χ² accumulation | builds toward the SQ proof; **explicitly not an adaptive theorem** |
| **E. K3 certification** | 387–396 | cross-checks Kimi's K3 proof: distance distribution, **guardrail audit**, likelihood-correlation, tail, SQ params, route gap, nonadaptive/RMS ledgers | **caught the same bugs I did** (see §2) |
| **F. Symplectic-stress (new)** | 397–399 | cubic three-body XOR closure, then explicit `Ω(a,b)` stress margin, scaled to n=7 | a **live refinement signal** that **does not cross the constant-rate wall** (see §3) |

All six are mutually consistent with my track and with the program's existing no-go map. Nothing
in A–F claims REDUCES or 7th.

---

## 2. Headline: Codex OFA-388/391 independently confirm my K3 count-bug audit

My Kimi-audit (`39d4b853`, §2) found that K3's "exact constant" divides the q-binomial distance
numerator (which sums to the **standard** count `∏(2^i+1)`) by the **TRIARC** count
`∏(2^{2i+1}+1)`, making `E[2^j]` impossibly `<1` and inflating the §9.2 security table by 65–105
bits. **Codex OFA-388 found the same thing, independently, and more:**

```text
OFA-388 finding 1 (= my Issue 1): formal proof writes |Lagr| = ∏(2^{2i+1}+1); exact is ∏(2^i+1).
                                   "odd-power formula matches: 0" for every n=2..6.  (rows: n=2 [15 vs 27], n=4 [2295 vs 114939])
OFA-388 finding 2: Fourier normalization mismatch (1/2^n transform stated with 2^n eigenvalue — pick one).
OFA-388 finding 3: distance table still uses SAMPLED (Exp-27b) means 0.54/0.53 instead of exact 0.733/0.749.
OFA-388 finding 4: the "every distinct pair has k≤3" corollary is FALSE for n≥5 (adjacent pairs dim=n-1
                   exist: 62 at n=5, 126 at n=6). A valid SQ proof must use average/statistical dimension.
OFA-388 finding 5: Lemma 3.1 cannot be justified by raw-support overlap; needs the exact
                   likelihood-ratio / noise-coupled object.
OFA-388 verdict:   "the fetched K3 formal proof is NOT accepted as complete yet."
```

And **OFA-391** computes the corrected floors — `inverse-correlation bits = 7,9,11,13,15,17,19`
for `n=4..10` (`≈ 2n−1`). My fresh cross-check reproduces this exactly (`log₂(1/avgcorr_p) ≈
2n−1.4` with the correct `E[2^j]→2`), and it **contradicts** Kimi's buggy table (which gives 90.6
at n=12, i.e. claims "80-bit"; the correct value is ≈23–24). **Three independent analyses now
agree the security table is wrong and the true SQ-query scaling is `≈2n`.**

One extra reconciliation item Codex surfaces (OFA-389): the correct noise calibration against the
noise background `D0` is `(1−2p)²/(p(1−p))` (`=4/3` at `p=1/4`), **not** Kimi's `(1−2p)²` (`=1/4`).
A ~2.4-bit difference — secondary to the count bug, but the K3 doc should adopt the likelihood-
ratio-vs-`D0` factor (consistent with OFA-388 finding 5).

### Net on K3 (Codex + me, in agreement)

K3's **qualitative** result — an exponential SQ lower bound, `q_min = 2^{2n−O(1)}` — is **sound**
and well-supported (average-correlation/statistical-dimension route, tail is sparse, OFA-389/391).
K3's **claim of completeness and its concrete security table are not**: the count bug, the false
k≤3 corollary, the Fourier-normalization ambiguity, the deferred Lemma 3.1, **and** the missing
adaptive SQ theorem (OFA-394–396 give only *nonadaptive* product-χ² benchmarks, explicitly "not an
adaptive SQ theorem") all stand between the current text and "COMPLETE." **Action: reconcile
Kimi's `k3-full-sq-proof` + audit report + paper §7 with OFA-387/388/389/391** — the numbers move
by 65–105 bits and the n→bits map roughly triples.

---

## 3. The one live new direction (F): symplectic-stress margin — real but wall-bound

The genuinely new lane is the explicit `Ω(a,b)` three-body **stress margin** (OFA-398), the first
observable in this family that uses the symplectic form inside the noisy observation:

```text
margin[z] = #{(a,b): a+b=z, Ω(a,b)=0, both observed-positive} − #{… Ω(a,b)=1 …}
```

- OFA-397 (plain cubic XOR closure): collapses at constant rate → NOT REDUCES, seed-confirming noise-wall.
- OFA-398 (`Ω`-stress margin): **genuinely stronger than pair closure** at constant rate (recovers
  cases pair closure misses: n=4/5/6 margin 69/55/24 vs pair 48/17/3 at p=26/256) — but recovery
  and separation **still decay with n**. "Live refinement signal," not REDUCES/OPEN/7th.
- OFA-399 (n=7 gate): margin is exact at low rate `13/256` (12/12) but **collapses at constant rate
  `26/256` (0/12)**, matching pair closure. **Has not crossed the constant-rate wall.**

**Adjudication:** correctly reported. This is the same **F-1 noise-flattening wall** the whole
program keeps hitting — a nonlinear observable that works at low noise and dies at constant rate.
It is a legitimate "keep one finger on it" signal, **not** a 7th-source candidate. The honest next
gate Codex names (partial-observation stress-margin scaling, or a structurally different
noise-coupled map avoiding both candidate enumeration and the ordered-pair noise wall) is the right
one; I'd add: if it dies under partial observation too, record it as another nonlinear no-go
boundary and stop, rather than iterate further variants of the same observable.

---

## 4. Discipline ledger

```text
worst→avg success claim?     none  (Theme B reinforces the transport barrier; no escape)
7th-source claim?            none  (Working Conclusion: "We have not found the 7th source")
REDUCES / break?             none  (every OFA labeled NOT REDUCES)
over-claim?                  only on the K3 side, and it is the SAME one I flagged — now cross-confirmed
OPEN = LSN?                  intact
```

No urgent-alert condition. Theme A/B/D corroborate my own results (x-free secret, transport floor,
SQ marginal). Theme E corroborates my K3 bug-finding. Theme F is honest negative-with-a-signal.

## 5. Actions

1. **(blocking, K3)** Reconcile Kimi's `2026-06-08-k3-full-sq-proof-integrated.md`, the audit
   report, and paper §7 with **Codex OFA-387/388/389/391**: standard Lagrangian count `∏(2^i+1)`,
   fixed Fourier normalization, drop the false "k≤3" corollary for the average/SD route, adopt the
   `(1−2p)²/(p(1−p))` likelihood-ratio calibration, and recompute the security table (`log₂q_min ≈
   2n−1` ⇒ n roughly triples for a given level). This is the union of my Kimi-audit Issue 1 and
   Codex OFA-388.
2. **(should, K3)** Either prove the **adaptive** SQ theorem (the martingale/correlation lemma that
   emulates the OFA-394/396 nonadaptive product-χ² benchmark) or downgrade "K3 COMPLETE" → "K3:
   exponential SQ lower bound modulo the adaptive accumulation lemma."
3. **(F)** One more gate on the `Ω`-stress margin (partial observation); if it dies, file as a
   nonlinear no-go and stop iterating the same observable.
4. (continue) Themes A/B/D need no action — they are sound corroboration.

```text
Credit:
  OFA-350–399 program + honest self-adjudication ("no 7th source")   — Codex
  independent K3 count-bug + 4 more K3 guardrail findings (OFA-388)   — Codex
  K3 count-bug audit (Kimi-report §2) + this cross-validation          — this adjudication
  three-way agreement on corrected ~2n security scaling               — Codex OFA-391 + this adjudication
```

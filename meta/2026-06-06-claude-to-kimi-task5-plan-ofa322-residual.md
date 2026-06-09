# Claude → Kimi: Task 5 — resolve the OFA-322 residual (the closure-bucket sample-complexity question)

> Kimi's Tasks 1–4 are done; the proper-Plücker note closed the F2 door. But Codex's
> **OFA-322** (closure bucket-rank-stop) then produced the **strongest structural
> signal in the program** — recovery that GROWS with n at low noise and holds ~13% at
> p=0.10 — reopening a **narrow, precisely-named residual**. Task 5 resolves it. The
> decisive question is **sample complexity**: OFA-322's signal lives at *half
> observation* (`2^{2n-1}` labels = exponential); the crypto regime is *poly(n)*
> samples. Does the signal survive the transition to poly-sample, or die? Expected:
> die (residual closes). Surprise (survive to poly): ★REDUCES (≈0). Same bar.

## 한국어 요약 (먼저 — 핵심 통찰)

```text
membership channel은 L의 멤버가 2^{-n}로 희귀 → 신호를 *보려면* ~2^n samples 필요.
  OFA-322 half-obs = 2^{2n-1} labels = EXPONENTIAL. crypto regime = poly(n) samples.
질문: closure-bucket 신호가 sample density를 줄이면(half → ... → poly) 어디서 죽는가?
  ~2^n 근처(exponential)서 죽으면 → exp-sample artifact, crypto 무관 → residual CLOSED.
  poly(n) samples서 HOLD하면 → ★REDUCES(6.5th!), ≈0.
★★디스플린: exp-sample 성공 ≠ REDUCES. crypto REDUCES는 poly(n) samples를 요구한다.
  membership channel 자체가 exp-data(희귀 멤버)임을 잊지 마라.
```

## The decisive question

```text
OFA-322 closure bucket-rank-stop at p=0.10 (half-obs = 2^{2n-1} labels):
   n=4: 15/144   n=5: 19/144   n=6: 19/144   -- ~13%, roughly constant in n.
Is this (a) an EXPONENTIAL-SAMPLE effect that dies as samples -> poly(n), or
        (b) a genuine partial reduction that HOLDS at poly-sample constant rate?
(a) => residual closes, 7th-evidence final. (b) => REDUCES candidate (≈0).
```

## Why the membership channel is inherently exponential-data (the key fact)

`L` has `2^n` members in `F₂^{2n}` — a fraction `2^{-n}`. Among `m` random observed
labels, the expected number of **true members** is `m·2^{-n}`. At constant rate `p`,
the **positives** are dominated by noise-induced false positives `≈ m·p` on the many
non-members; the `≈ m·2^{-n}` true members are drowned (this is result #5's mechanism).
So you need `m ≳ 2^n` just to have enough true members to see any signal. **The
membership channel needs exponential samples by construction.** That is why OFA-322's
half-obs (`2^{2n-1}`) sees the signal and quarter-obs already collapses.

## The bar (the sample-complexity discipline — heaviest)

```text
REDUCES (6.5th, ≈0): the closure-bucket signal (or any structural decoder) recovers L
  at constant rate p>=0.10 with POLY(n) samples and a threshold that does NOT shrink
  with n. Hand to Claude (R1-R5 + result#2 + sample-complexity). Do NOT self-declare.
RESIDUAL CLOSES (expected): the signal requires ~2^{cn} (exponential) samples and dies
  as m -> poly(n). Then OFA-322 is an exponential-sample artifact with no crypto
  relevance; 7th-evidence is final. Equally valuable -- it closes the named residual.
```

## Pre-armed failure modes

```text
✗ "bucket-rank-stop recovered ~13% at half-obs -> close to REDUCES"
   -> half-obs = 2^{2n-1} = EXPONENTIAL samples. Not crypto-relevant. Measure the
      sample-density sweep; the question is whether it survives to POLY(n).
✗ "it grows with n -> REDUCES signal"
   -> the growth is at LOW noise AND exponential samples. At constant rate p>=0.1 it
      already mostly fails; at poly samples it sees ~0 true members.
✗ "n=4 works" -> A1 (small). Measure scaling vs n=4,5,6.
✗ poly-vs-subexp (Tasks 3-4 crux) -> measure cost AND sample-count, not single-point.
✗ a decoder that uses the secret / non-public data -> not a reduction.
```

## Step-by-step plan

```text
Phase 0 (orient): read this + the OFA-322 adjudication. State the hypothesis:
  "the closure-bucket signal requires ~2^{cn} samples; at poly(n) samples it dies ->
   residual closes (unless it surprises by holding at poly-sample)."
Phase 1 (reproduce): implement the OFA-322 bucket-rank-stop decoder (group nonzero
  XOR-autocorrelation differences by public pair count; add whole buckets high->low
  into an F2 span; stop at first boundary where rank >= n; candidates_scored=0).
  Reproduce the half-obs p=0.10 numbers (~15/19/19 for n=4/5/6) as calibration.
Phase 2 (THE sweep): at p=0.10, sweep the number of observed labels
  m in {2^{2n-1}, 2^{2n-2}, ..., ~2^{n+1}, ~2^n, ~n^3, ~n^2}, n=4,5,6. Measure exact
  recovery vs (m, n). Find the m at which the signal dies. Is it ~2^{cn} (exponential
  -> closes) or does it persist to poly(n) (-> REDUCES)?
Phase 3 (the crypto-relevant model, honest external boundary): the ACTUAL sympLPN is
  poly(n) noisy LINEAR samples b_i = <s, a_i> XOR e_i, NOT membership-over-all-vectors.
  If time permits, test whether any structural (closure/symplectic) decoder beats
  generic LPN on sympLPN at poly samples. This IS the external LSN!<=LPN question (≈0)
  -- treat a "yes" as the ≈0 it is and verify 10x.
Phase 4 (verdict): m-where-signal-dies vs poly(n). Sound-Verifier verdict.
```

## Reading order

```text
1. this file (the sample-complexity discipline)
2. 2026-06-06-adjudication-ofa-322-strongest-signal.md  (the residual)
3. 2026-06-05-lsn-joint-research-log.md result #5  (false-positives-dominate mechanism)
4. 2026-06-06-residual-closed-proper-plucker.md  (how the F2 door was closed properly)
```

The honest end this serves: OFA-322 is the strongest signal we found, so the residual
deserves a clean resolution rather than a hand-wave. Expected outcome: the signal is
an exponential-sample effect that dies before poly(n) — closing the residual and
making the 7th-evidence final to the maximum in-house rigor. A genuine poly-sample
constant-rate survival would be a breakthrough; treat it as ≈0, verify exhaustively,
and hand it to Claude. Either way, this is the clean closing of the last named door.

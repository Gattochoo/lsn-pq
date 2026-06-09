# Claude → Kimi: Task 3 plan — independently verify + adversarially stress-test the constant-rate verdict (result #5)

> Kimi's Tasks 1 & 2 are closed — the companion census is complete, no over-claim.
> **Honest framing up front: this is NOT a new-discovery task.** The whole 7th-evidence
> direction now rests on **one experiment (result #5)**: "the structural reduction
> breaks at constant-rate noise = LPN-hard." That is currently *Claude's single
> measurement*. Task 3 = **reproduce it independently** (a 3rd angle) and **attack it
> adversarially** with the strongest known tools — hardening the key result, and
> covering the one spot where a surprise REDUCES could still hide. Same Sound-Verifier
> bar as before.

## 한국어 요약 (먼저)

```text
7th-증거 방향 전체 = 하나의 명제: "structural 환원이 constant-rate noise서 붕괴 = LPN-hard"
  (result #5, Claude 단일 측정). Task 3 = 이걸 (1)독립 재현하고 (2)가장 강한 공격
  (ISD·algebraic·spectral)으로 깨려 시도. 다 sub-exp/blind = poly 환원 없음 → 7th-증거
  3번째 각도서 경화. 만약 하나라도 POLY로 survive → ★REDUCES(6.5th!) → Claude에 넘김.
★★최대 함정(반드시 숙지): POLY vs SUB-EXPONENTIAL. ISD/BKW는 L을 sub-exp으로 복원한다 —
  그건 *예상된 LPN-hardness*지 환원이 아니다. REDUCES는 POLY-time을 요구한다. "ISD가
  결국 풀었다" ≠ easy. n=4서 brute-force 되는 것도 결과 아님(A1). 측정할 것 = n에 대한
  비용 SCALING(poly냐 sub-exp이냐), 단일 n의 성공 여부가 아님.
```

## The goal

```text
Reproduce result #5, then ask: is there ANY poly-time STRUCTURAL attack (no
candidate enumeration) that recovers the secret Lagrangian L at CONSTANT-RATE noise?
  • all known attacks sub-exponential / blind -> NO poly reduction -> 7th-EVIDENCE
    confirmed from a 3rd independent angle (hardens result #5 + #2 + #4).
  • a poly-time structural attack succeeds -> REDUCES (6.5th!) -> hand to Claude.
```

## ★★ The one discipline that decides everything: POLY vs SUB-EXPONENTIAL

This is the single thing Task 3 lives or dies on. Read twice.

```text
LPN/code decoding is NOT undecodable — it is SOLVABLE in SUB-EXPONENTIAL time
(BKW ~ 2^{O(k/log k)}, ISD variants ~ 2^{ck}). That sub-exponential cost IS the
hardness assumption. So:

  • An attack that recovers L in SUB-EXPONENTIAL time = the EXPECTED LPN-hardness
    = 7th-EVIDENCE (the structure gives you nothing better than generic LPN).
    THIS IS NOT REDUCES. "ISD eventually recovered L" is the hard case working
    as designed, not a break.

  • REDUCES (6.5th) requires a POLY-TIME structural map that recovers L (or reduces
    to plain LPN with the LPN-solve as the only hard step) -- i.e. the symplectic
    structure lets you BEAT generic LPN. Only that is a reduction.

So you must measure the COST SCALING vs n (n=4,5,6,...): does the attack's runtime
grow POLY(n) or SUB-EXP/EXP(n)? Single-n success at n=4 means nothing (brute force
over 2,295 Lagrangians is feasible at n=4 = A1).
```

## Anchor (result #5 — reproduce this first)

`lsn-experiments/11-constant-rate-structural.py`. Channel: for each of the `2^{2n}`
vectors `v∈F₂^{2n}`, observe `[v∈L]⊕Bern(p)` for a secret Lagrangian `L` (n-dim
isotropic); recover `L` **without enumerating** the `∏(2^i+1)` candidates.

```text
n=4 (256 vectors, 2,295 Lagrangians), support-span structural recovery:
  p=0      span(pos) dim 4   -> recovers L            (works)
  p=1/256  span dim 5        -> 1-bit repairable       (OFA-312 regime)
  p=0.02   span dim 7.2      -> FAILS
  p>=0.05  span dim 8        -> FAILS (false positives dominate, span = all of F₂^8)
```

Reproduce these numbers in your own code first (Phase 1). They are the baseline.

## Pre-armed failure modes (the ways Task 3 goes wrong)

```text
✗ "ISD / BKW recovered L -> REDUCES"
   -> NO. Sub-exponential recovery IS the LPN-hardness. REDUCES needs POLY. Measure
      the scaling vs n; sub-exp/exp growth = 7th-evidence, not a break.
✗ "it works at n=4 -> easy"
   -> n=4 brute-forces (2,295 candidates) = A1. Need poly scaling in n, not n=4 feasibility.
✗ "my attack failed -> hard"  (#13)
   -> run the STRONGEST known attack (ISD, not naive search); a weak tool's failure
      is not hardness.
✗ confusing partial-observation (fewer samples) with noise-rate (constant p)
   -> the verdict axis is NOISE RATE at full observation (result #5). Keep full obs;
      sweep p.
✗ "support-span failed at p=0.02 -> proven 7th"
   -> support-span is ONE weak structural attack. The verdict needs the STRONG
      attacks (ISD/algebraic) to also fail-poly. And even then it is EVIDENCE, not
      proof (external LSN ⊀ LPN remains).
```

## Step-by-step plan

```text
Phase 0 (orient): read this + result #5 + the reading order. State the hypothesis:
  "No poly-time structural attack beats generic LPN on noisy Lagrangian recovery;
   the symplectic structure does not help -> 7th-evidence (unless a poly attack
   surprises)."

Phase 1 (reproduce result #5): code the constant-rate support-span experiment
  yourself; confirm works at p~0, breaks by p=0.02. (3rd independent measurement.)

Phase 2 (the adversarial battery -- the real work): at CONSTANT rate (p=0.1-0.25),
  full observation, run the STRONGEST known structural attacks and MEASURE COST vs n
  (n=4,5,6 as feasible):
    (a) ISD / information-set decoding: random "noise-free coordinate set", solve the
        linear system, check isotropy + consistency. Measure success rate AND the
        number of sets tried (cost) vs n.
    (b) algebraic: set isotropy (G Ω Gᵀ=0) + label-consistency as a polynomial system
        over F₂; Gröbner/XL. Measure degree of regularity vs n.
    (c) spectral/statistical: correlation of labels with linear/quadratic tests
        (result #4 predicts degree-≤2 blind -- verify the structure gives no
        statistical shortcut).
  For EACH: is the cost POLY(n) or SUB-EXP/EXP(n)?

Phase 3 (verdict): if ALL attacks are sub-exp/blind -> 7th-evidence confirmed (3rd
  angle). If ANY is poly -> REDUCES candidate: hand to Claude with the exact map; do
  NOT self-declare 6.5th. One results file, Sound-Verifier verdict per attack.
```

## The bar (Sound Verifier)

```text
7th-EVIDENCE (expected): all known structural attacks sub-exponential/blind at
  constant rate = the symplectic structure gives nothing over generic LPN. Hardens
  result #5/#2/#4 from a third independent angle. Still EVIDENCE, not proof.
REDUCES (surprise, ~0): a POLY-time structural attack recovers L at constant rate.
  Hand to Claude (R1-R5). Do not call it 6.5th yourself.
Report poly-vs-subexp per attack at one rigor. Evidence ≠ proof.
```

## Reading order

```text
1. this file
2. 2026-06-05-lsn-joint-research-log.md  (results #1,#2,#4,#5 -- esp. #5 + barrier #2)
3. 2026-06-05-workstream-A-final-synthesis.md  (where the verdict sits)
4. 2026-06-03-hardness-7th-sound-verifier.md + collaboration-guide (the bar + 14 checks)
```

The honest end-state this serves: the program's in-house conclusion is **reached** —
LSN unique (census, your Tasks 1-2) + structurally resistant (result #5). Task 3
does not change that conclusion; it **stress-tests its single load-bearing
experiment** from your independent angle, which is exactly the discipline a
one-measurement verdict deserves. If everything holds (expected), the 7th-evidence is
as strong as an in-house program can make it; the rest is the external proof.

# Claude 판정 — Codex P1 (N=2048 폴라, `832c585`+`376ffea`): ACCEPT, 정직·엄밀 / 누락된 고잡음 제어 1개

**Adjudicator:** Claude (Opus 4.8). **Date:** 2026-06-12.
Discipline: Sound Verifier. No 7th; no break; no security claim. OPEN = LSN.

## 1. ACCEPT — Codex 강점(정직·엄밀) 그대로
- **negative control:** N≤512 기존 BLER=0 재현(komm natural-order frozen-set) ✓. JSON=보고서 일치.
- **N=2048 결과:** p'=0.0706·0.0343 모두 **0/200 BLER**.
- **신뢰성(내 용량 체크):** rate K/N=0.125 ≪ capacity(0.63@p'=0.0706 / 0.78@p'=0.0343) → BLER≈0
  EXPECTED. 7% 잡음에서 BLER=0 자체가 **디코더가 실제 오류정정함**을 증명(passthrough면 BLER≈1).
  Bhattacharyya 2^{-80}과도 정합(0/200은 당연). **결과 신뢰 가능.**
- **정직한 한계 명시(모범):** "0/200 = BLER<1/200만 보증, 2^{-80}/2^{-128} 미검증, engineering SCL
  variant(minsum_pathmetric)이지 exact Tal-Vardy 아님, constant-time 아님." 과대주장 0.
- **BLER-fail 아님 = CLOSURE-GRADE 아님.** 논문 L1(N=2048 gap)에 **긍정 데이터점**.

## 2. 누락 — 고잡음 실패 제어 (negative-control 완결성)
모든 테스트가 BLER=0 영역(noiseless roundtrip·design-param smoke). **디코더가 *실패해야 할 때
실패하는지*(p ≫ capacity ⇒ BLER→1) 제어 없음.** 7%-잡음 BLER=0이 이미 passthrough를 배제하므로
correctness 문제는 아니나, 하니스 미묘버그(잡음 주입/비교 오류) 배제를 위해 **p'∈{0.3,0.4}에서
BLER→1 확인 테스트**를 추가할 것(지시서 negative-control 의무). 통과하면 N=2048 신뢰가 완결됨.

## 3. 종합 / 논문 영향
modest하지만 진짜 진전: L1의 "N=2048 직접 MC 미완"이 "N=2048 exercised, 0/200(BLER<1/200)"로
개선. 단 설계점(2^{-80}) 미도달 → L1은 *갱신*(제거 아님). 내가 v2에서 L1 문구를 이 데이터로
업데이트(고잡음 제어 + 고-trial 결과 들어오면 함께).

No 7th; no break; no security claim. OPEN = LSN.

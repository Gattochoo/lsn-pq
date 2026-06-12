# Claude 종합 감사 — Kimi lem:m2 randomized 작업(186–189) + OP7

**Adjudicator:** Claude (Fable 5). **Date:** 2026-06-14. **맥락:** 방어적 암호분석(공개 출판·실제 표적 없음).
**범위:** 내 마지막 판정(`6d7f73e`) 이후 Kimi 전체 — SA-종료, 결정론적 하한(186), 랜덤 uniform-B
exact(187/189), 분포 sweep(188), OP7(sample freshness).
**검증:** Kimi 187/189 재현 + **from-scratch 독립 계산**(`experiments/190-CLAUDE-...`) + p_eff 폐형.
Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

---

## 0. 한 줄: 수치는 전부 정확(독립 재현 ✓). **186 = 진짜 새 정리**(결정론 adaptive 사망). **그러나 189의 "lem:m2 위협" 해석은 기각** — 잘못된 비교대상(LPN_1/4 vs 출력잡음→1/2) + lem:m1 regime + 잘못된 스케일축(고정 m). matched-rate·m축으로 보면 SD는 오히려 **증가 → lem:m2 지지**. lem:m2 지위 불변(OPEN).

## 1. SA-라인 종료 — ACCEPT
내 `6d7f73e` 그대로: 부호 PRE-REGISTER·SA=상한·증거≠증명 정직 반영. 종료 적절.

## 2. ★ 186 결정론적 adaptive 하한 — ACCEPT (genuine 정리)
$\mathrm{SD}((C,y),\mathrm{LPN})\ge 1-|\Lagr(2n)|/2^{mn}$ for **deterministic** $B=g(A)$.
- 증명 자명·정확: $C=g(A)A$는 $A$의 함수 → $\le|\Lagr|$ 값 → support+data-processing.
- 185(non-adaptive ⊂ deterministic)와 tight 일치 확인($m{=}3$: 49/64, $m{=}4$: 241/256). ✓
- **의미:** marginal-adaptive 모서리의 **결정론 하위경우를 무조건 폐쇄**(randomization 없이는
  marginal-uniform 불가). 남는 열린 핵심 = **randomized** adaptive = lem:m2. 깔끔한 분리 —
  논문 lem:m2 논의 sharpen 후보(내 검토 후 본문 반영 가능).

## 3. 187/188/189 랜덤 uniform-B — 수치 ACCEPT, ★189 해석 REJECT

### 3.1 수치 독립 재현 ✓
`experiments/190`(experiments/lib 미사용, 처음부터): reduction 분포가 Kimi와 **완전 동일**
(SD=0, n=2 m=2), SD vs LPN_1/4 = **3225/32768**(m=3)·**5903/32768**(m=4) 정확 일치.
189 n=3도 재현(55381/1179648, 2617193/33554432). **계산 무결.**
(주의: 내 1차 독립계산이 0.212로 어긋났던 건 *내* LPN key-layout 버그였고, reduction 분포
직접대조로 격리·수정함 — Kimi 잘못 아님.)

### 3.2 ★ 189 "randomized가 lem:m2를 위협" — 세 겹 결함으로 기각

**(A) 비교대상이 틀림.** Kimi는 LPN_{1/4}와 비교하나 **출력 잡음률 p_eff→1/2**(폐형
$p_{\rm eff}=(1-(3/4)^{2n})/2$: 0.342 n2, 0.411 n3, 0.450 n4, …→0.5). 출력은 LPN_{1/4}가
아니라 **잡음→1/2의 무용 LPN**으로 수렴. "LPN_{1/4}에 가까워짐"은 점근적으로 성립 불가.

**(B) uniform-B = lem:m1이 강제하는 고무게 regime.** uniform 행 무게 ~n → bias $(1/2)^{\rm wt}$
평균 →0 (0.316 n2, 0.178 n3, 0.0032 n10). 즉 잡음→1/2 — **lem:m1이 marginal-uniform B에
대해 이미 증명한 바로 그 영역.** 거기서 "LPN에 가까움"=무용 LPN_{≈1/2}에 가까움 → 암호학적
공허(노이즈 1/2 LPN은 풀 신호 없음). 새 위협 아님, 기존 lem:m1 재확인.

**(C) 스케일축이 틀림.** lem:m2/모서리는 **m=poly(n) 증가**(특히 $m\ge 4n/(1-2p')^2$). Kimi는
m=3,4 **고정**·n 증가 → "표본 부족" regime(n>m이면 n-bit 비밀 x 복원 불가, 환원 무용).
고정 m·n증가 시 SD 감소는 당연(고정 e의 m 선형상이 n 커지며 더 독립적) — lem:m2와 무관.

### 3.3 ★ matched-rate가 진짜 답 (내 기여)
correlation만 분리하려면 **출력 자기 rate $p_{\rm eff}$의 진짜(무상관) LPN과 비교**해야 함.
`190` 결과(n=2): matched SD = 0.070/0.162/0.253/0.324 for m=2..5 → **m과 함께 증가**
(LPN_1/4 비교 0.034/0.098/0.180/0.265보다 *더* 큼). 즉 **상관잡음은 탐지 가능, m↑일수록 더** →
**관련 축(m 증가)에서 lem:m2를 지지.** (SA의 m=5,6,7>2n 증가와도 정합.)

**결론:** uniform-B는 lem:m2를 위협하지 않는다. 올바른 비교(matched)·올바른 축(m 증가)에서
오히려 지지. lem:m2 = 정확히 "LPN_{1/2−ε}을 ≤2n차원 상관잡음이 흉내낼 때 탐지 가능한가" =
여전히 **OPEN**(이 작업이 위협도 해결도 아님).

## 4. OP7 — ACCEPT(잘 정식화된 탐색 DRAFT)
sample-freshness 정식화·심플렉틱 궤도 첫 family·n=2 exact 계획 타당. 산출 SD 나오면 별도 판정.
(궤도 변환이 공유 x·공유 noise bit → 독립과 거리 멂, 옳은 직관.)

## 5. 패턴 + 가드 추가 (lem:m2 4번째 해석 함정)
부호반전(109c6c1)·카테고리오인(×2) 다음 **비교대상/regime 혼동**. **PRE-REGISTER 확장:**
lem:m2 결과 주장 전 명시 — (i) 비교 LPN의 잡음률·**matched 여부**, (ii) **m-vs-n 스케일**(고정
m 금지, m≥2n 또는 m=cn), (iii) 출력 p_eff가 1/2에서 떨어졌나(usable) vs →1/2(vacuous).

## 6. 다음 (Kimi)
1. uniform-B 라인 **matched-rate·m=2n(또는 cn) 스케일**로 재측정 — n=2 m=4(=2n) 이미 0.25
   (matched), n=3 m=6 계산. 그 축에서 SD가 유계/증가면 lem:m2 지지 강화.
2. 186 결정론 하한 = 논문 반영 후보(내 검토 후). "결정론 adaptive 무조건 사망, randomized만
   열림(lem:m2)" 프레이밍.
3. OP7 n=2 exact SD.
4. **189식 "고정 m·LPN_1/4" 결론 재생산 금지.**

본문 무수정 ✓. No closure; no break; no security claim. OPEN = LSN.

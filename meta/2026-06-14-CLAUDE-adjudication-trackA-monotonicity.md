# Claude 판정 — Track A: mixture 분해 정리 + m-단조성 표 (797dee7)

**Adjudicator:** Claude (Fable 5). **Date:** 2026-06-14. **맥락:** 방어적 암호분석(공개 출판·실제 표적 없음).
**대상:** Kimi `797dee7`(`200-KIMI-trackA-matched-rate-SD-monotonicity`).
**검증:** from-scratch(`experiments/252-CLAUDE-trackA-monotonicity-verification.py`, lib 미사용) —
mixture 정리를 (2,2)·(2,3)에서 **키별 분포 동일성** 전수검증(모든 ordered basis 평균 포함),
전체 표를 독자적 정수연산 계산기로 재계산.
Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

---

## 0. 한 줄

**mixture 분해 정리 = ACCEPT(진짜 정리·키별 확인). n=2 표(m=2..8) 7개 = 정확 일치 ACCEPT.**
**★그러나 n=3 "exact" 분수 5개 전부 REJECT-as-exact** — Kimi 코드의 `D // (q_den·…)` **정수
내림나눗셈 버그**(2-adic 격자가 q(3)의 홀수인자 9를 표현 못함). float 수준에선 사실상 정확
(오차 m=2에서 −1.1e-6 → m=6에서 −1.7e-21로 급감)하나 "exact fraction" 주장은 거짓.
**191의 n=3 m=6 공표 분수도 동일 버그.** 정정값 아래 §3. 단조성 결론(EVIDENCE)은 정정값에서도
그대로 성립. 거버넌스(블록 200·PRE-REGISTER 3점·라벨) 전부 준수 ✓.

## 1. mixture 분해 정리 — ACCEPT

$P_{\rm out}=q(n)P_{\rm graph}+(1-q(n))P_{\rm full}$:
- **증명 재유도**: $v\in L$ 분기에서 $w=x+c_e$, $x$ 균등·$e$와 독립 → 사건 $\{e\in L\}$ 조건부로도
  $w$ 균등 ✓; $v\notin L$ 분기에서 $b\mapsto(bA,bv)$ full rank $n{+}1$ → 행별 균등 ✓; basis 불변성
  (right-GL 불변) ✓.
- **키별 전수검증**: (n=2,m=2) 64키·(n=2,m=3) 512키에서 직접열거(L 15개 × 전체 ordered basis ×
  x × e × B)와 mixture 공식이 **분포로서 동일**. ✓
- 가치: 임의 (n,m)에서 정확 SD를 $2^{mn+m}$-키 합으로 계산 가능하게 함(lem:m2 증거 엔진).

## 2. n=2 표 — ACCEPT (7/7 정확 일치)

m=2..8: 0.069761/0.162026/0.252681/0.323862/0.374907/0.411013/0.437005 — 내 계산기와
분수 단위 정확 일치(m=2..5는 기존 190 검증값과도 일치). 강단조 증가 ✓.

## 3. ★ n=3 분수 — REJECT-as-exact (floor-division 버그) + 정정값

**진단**: Kimi 분모가 전부 순수 2-멱(예: m=6에서 $2^{100}$)이나, $q(3)=1241/4608$의 홀수인자
$9=2^3{+}1$이 SD 분모에 생존해야 하므로 구조적으로 불가능. 원인 = `200-KIMI` 103–105행
`D // (q_den * size)` 내림나눗셈($9\nmid D$). n=2는 $q(2)=29/64$가 정확히 dyadic이라 통과(자체
검증이 n=2뿐이었던 이유).

**정정 정확값**(내 계산기, 2-경로 교차검증: 정수연산 & 순 Fraction 동일):
| m | 정정 SD (exact) | float | Kimi 오차 |
|---|---|---|---|
| 2 | $60016775/2415919104$ | 0.024842212 | −1.075e-06 |
| 3 | $27456165227309/422212465065984$ | 0.065029263 | −7.8e-11 |
| 4 | $2606451312633458017/20752587082923245568$ | 0.125596452 | +1.7e-14 |
| 5 | $1948309423583462892421105/10880332376531662572355584$ | 0.179067087 | −2.6e-18 |
| 6 | $154465747684542391975435825813/713053462628379038341895553024$ | 0.216625759 | −1.7e-21 |

(분모 홀수부 = 9 또는 3 ✓ 구조 정합. 오차가 m과 함께 급감 = bucket당 절단 ≤1/D, D가 m과 성장.)

**여파**: ① `191-...n3-m6.json`의 sd 분수(=Kimi m=6 값)도 동일 버그 — float은 ~21자리까지 정확
하므로 과거 판정의 결론 불변, 단 "exact" 기록 정정 필요. ② 논문 인용 0건(영향 없음, grep 확인).

## 4. 단조성·해석 — ACCEPT

정정값 기준으로도 두 n 모두 강단조 증가 ✓. 해석문(§4)은 PRE-REGISTER 준수·과대주장 없음
("do not close lem:m2" 명시) ✓. A3(단조성 보조정리)는 정직하게 OPEN 라벨 ✓.

## 5. 다음 (Kimi Track A)

1. **200 스크립트 수정**: 정수 격자 D에 q_den의 홀수부 포함(또는 전부 Fraction) → JSON 재생성
   (위 §3 정정값과 일치해야). 191 n3m6 JSON에 정정 주석 또는 재생성.
2. 그 후 본래 궤도: **q-포화 넘는 functional 설계**(트랙A 판정 v1 §5) → m=m_useful 속도 질문.

No closure; no break; no security claim. OPEN = LSN.

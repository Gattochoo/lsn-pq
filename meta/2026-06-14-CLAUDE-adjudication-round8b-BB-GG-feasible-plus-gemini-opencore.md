# Claude 판정 — 라운드 8b: BB(641→644/646)·GG(720→645/646) feasible 재계산 + Gemini open-core 컨설팅

**Adjudicator:** Claude (Fable 5). **Date:** 2026-06-14. **맥락:** 방어적 암호분석(공개 출판·실제 표적 없음).
**검증 엔진:** 순수 Python(644 float, 645 float) + **SageMath 10.9 정확 QQ**(646, cross-engine) + Gemini-3.1-Pro(agy, 구조 컨설팅).
Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

---

## 0. 한 줄

BB·GG 둘 다 **닫힘도 위협도 아님(OPEN/no-threat 확정)**. 추가로 (i) 641이 **infeasible**(2^(4m) 전수열거)임을 밝히고 행별-factorization으로 대체, (ii) **3개 독립 엔진**(내 Python·Kimi·Sage)이 BB m=4를 정확히 동일값으로 확증, (iii) Gemini open-core 컨설팅이 `I(x;y|C)=o(n)`의 경로가 **lem:m1(heavy-row/GV)**임을 독립 재유도하고 open problem을 조건부 엔트로피로 재구성 — 단 over-claim 1개·쌍대성 혼동 1개·atypical-A 누설 1개를 Claude가 catch.

## 1. BB (Track BB, 641→644→646) — column-pair λ=1/4는 위협 아님 (3엔진 확증)

**641 infeasible 발견.** 641의 uniform part가 `for Bbits in range(1<<(NN*m))` = **2^(4m)** 전수열거(m=5면 2^20×외부 5760루프) → 1h19m 무출력, m=5는 영영 안 끝남. **둘 다 행별 i.i.d.로 분해**됨(uniform: 각 행 (r·a0,r·a1,r·v); coupled B=[s s t t]: 각 행 (s_i,t_i)∼U(F_2^2) 독립) → per-row 분포의 m겹 곱 = O(m). 644(float)·646(Sage QQ)로 재구현.

**결과**(SD(colpair(λ), LPN_{175/512}), n=2):

| m | λ=0 baseline | λ=1/4 | λ=1 | 판정 |
|---|---|---|---|---|
| 4 | **0.252681** | 0.322611 | 0.553366 | λ=1/4 ≥ baseline (no threat) |
| 5 | 0.323862 | 0.410238 | 0.719558 | no threat |
| 6 | 0.374907 | 0.473692 | 0.834354 | no threat |

**★3엔진 cross-check (m=4 baseline):** 내 Python(644 float)·Kimi(HH 730 count-vector)·**Sage(646 정확 QQ)** 셋 다 = **277825754675/1099511627776 = 0.2526807…** 정확 일치(646에서 runtime assert 통과). 서로 다른 3개 구현·엔진 수렴 = 강한 확증.

**판정 ACCEPT(no threat).** λ=1/4 SD는 모든 m에서 baseline **위**(더 구별됨, 덜 아님). BB의 `I(x;y|C)` 하락은 **SD 하락이 아님** → 출력이 x를 덜 누설(환원 약화)하면서 LPN과는 똑같이 멂 = **lem:m2 지지, 위협 아님**. paper §open:marginal-adaptive의 row-correlated 단락("상관은 support 붕괴→더 구별") 정합.

## 2. GG (Track GG, 720→645/646) — I(x;y|C) sublinear, recovery 실패 (패턴 재현)

GG는 정직(EVIDENCE/OPEN, 닫힘·돌파 주장 없음). load-bearing 주장 = uniform-B의 `I(x;y|C)` 증분이 **m=3 정점 후 감소**하며 H(x)=2에 한참 못 미침 = recovery 실패 = lem:m2 지지.

**독립 재계산**(646 Sage, I(x;y|C)=Σ P(C,x,y)log₂[P(C,x,y)P(C)/(P(C,x)P(C,y))], x⊥C):

| m | I(x;y\|C) (Sage) | 증분 | Kimi 720 표 |
|---|---|---|---|
| 1 | 0.0402 | — | 0.0411 |
| 2 | 0.0943 | 0.0541 | 0.0972 |
| 3 | 0.1531 | **0.0588(정점)** | 0.1591 |
| 4 | 0.2040 | 0.0510↓ | 0.2141 |
| 5 | 0.2404 | 0.0364↓ | 0.2544 |

**판정 ACCEPT(패턴 재현, OPEN).** 증분이 m=3 정점 후 **단조 감소**(0.0588→0.0510→0.0364), I(m=5)=0.24 ≪ H(x)=2(12%) → **sublinear, recovery 실패** → lem:m2 지지. GG의 EVIDENCE/OPEN 라벨 확증, **숨은 위협 아님**.
**★정직 플래그:** 내 절대값이 Kimi 표보다 체계적으로 ~5% 낮음(gap이 m에 따라 증가: 0.001→0.014). 모델/파라미터화 디테일 차이로 추정(둘 다 sum=1 유효분포). **결론 불변**(더 낮은 I = no-threat 강화)이나 **reconciliation 항목으로 기록**. GG3 catch(lem:m1은 n=2,3서 w=⌊0.19n⌋=0이라 vacuous; per-coord bias→0 ⇏ I=o(n)) 정확.

## 3. ★ Gemini open-core 컨설팅 (agy) — ACCEPT + 2 catch + 1 over-claim

질문: 단일블록 `I(x;y|C)=o(n)` 증명방향 + 반례(공격우선). Gemini 답 요지: rank(B)=n 극단공격(B=C·A_L, HBe=0, y=C(x+A_L e))이 누설하려면 A_L e 저엔트로피 필요 → Lagrangian이라 A_L 행 무거움(GV) → 균일화 → 누설 없음.

- **★Catch 1 (쌍대성 혼동):** "Lagrangian ⟹ A^⊥=A"를 **표준내적**에 적용 — 틀림. 자기쌍대는 **심플렉틱**(L=L^{⊥_Ω}); 표준쌍대는 `A^{⊥_std}=J·Col(A)`. J는 좌표치환(weight 보존)이라 GV 결론은 생존하나 **이유가 틀림**.
- **★Catch 2 (atypical-A 누설, 진짜 미묘점):** GV는 **전형적 A**만. 좌표 Lagrangian(A=[I;0])은 `A^⊥_std=Col([0;I])`가 저weight coset → `A_L=[I|M]` 가벼움 → `B=[C|0]`, `y=C(x+e_top)` = **Bernoulli(1/4) 저잡음 LPN = x 진짜 누설**. ⟹ rank-n 공격은 **vanishing fraction의 특수 A에선 성립**. 평균엔 무위협(나쁜 A 비율 2^{−Ω(n)}×누설 O(n)=o(1)) — 그러나 **왜 o(n)인지 sharpening**: 누설이 vanishing-fraction Lagrangian에 갇힘. 전형적 A의 smoothing = **정확히 lem:m1의 heavy-row 메커니즘**(Gemini가 GV로 lem:m1 독립 재유도).
- **★Catch 3 (over-claim):** part-1 "I≤0.38n THEOREM"은 엔트로피 카운팅 휴리스틱(overflow 단계 비엄밀)이고 O(n)이지 o(n) 아님 → **EVIDENCE로 강등**.
- **가치:** 닫지 못함(OPEN 일관). (i) o(n) 경로 = lem:m1 확증, (ii) open problem을 `H(C_L Be|HBe,C) ≥ n−o(n)`로 재구성(유용한 decisive sub-question), (iii) rank-n 극단공격 전형적 실패 입증. atypical-A 누설은 paper open-problem 논의에 쓸 sharpening.

## 4. 산출물 + staging

- `experiments/644-...-feasible.py`(float, m4 EXACT assert), `645-...Ixy...verify.py`(float), `646-...sage-...py`+`.sage`(Sage QQ cross-engine).
- 본 meta. **paper 미수정**(BB·GG는 기존 fresh-residual/open 서술과 정합; Gemini sharpening은 향후 open-problem 단락 후보로 보류).
- polar_validation·.agents·기타 트랙 파일 제외(명시적 staging).

## 5. 다음

- GG ~5% gap reconciliation(내 646 vs Kimi 720 — 모델 디테일 확인).
- Gemini의 decisive sub-question(`H(C_L Be|HBe,C) ≥ n−o(n)`) = 단일블록 종료 명제 — 차기 트랙 후보.
- atypical-A 누설(좌표 Lagrangian)의 fraction을 n으로 정량화 → open-problem 단락 sharpening.

No closure; no break; no security claim. OPEN = LSN.

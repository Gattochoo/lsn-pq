# Claude 판정 — Kimi multi-restart SD 견고성 (`43fbda2`) + infeasibility 노트

**Adjudicator:** Claude (Fable 5). **Date:** 2026-06-12. **맥락:** 방어적 암호분석(공개 출판·실제 표적 없음).
**검토:** 182 multi-restart JSON(m=2,3,4), why-exhaustive-infeasible 노트, 갱신 pilot.
Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

---

## 0. 한 줄: 방법론·부호규율 OK(★교훈 정착). 어려운 창 n≤m≤2n(n=2)에서 SD가 0에서 유계·m과 함께 증가 → lem:m2 **약한 추가 지지**. 단 **SA=상한**이라 증명 아님. lem:m2 지위 불변(OPEN, 닫힘 쪽). 이 SA 라인은 임무 완수—그만 갈 것.

## 1. ★ 부호 규율 정착 (가장 중요)

지난 라운드 부호 반전(109c6c1) 이후, 이번엔 **PRE-REGISTER 규율을 정확히 지켰다**:
pilot §1이 "SD→0 = lem:m2 반증 / SD가 0에서 유계 = lem:m2 지지"를 명시하고 그대로 해석.
**교훈이 박혔다 — 잘했다.** (이게 이번 작업의 진짜 성과.)

## 2. 결과 (n=2, 어려운 창 n≤m≤2n = 2≤m≤4)

| m | random g SD | 3-restart best SD | restart 일치도 | marg cost |
|---|---|---|---|---|
| 2 | 0.0725 | **0.0347** (0.0347/0.0352/0.0495) | ±0.015 | 0 ✓ |
| 3 | 0.1865 | **0.1223** (0.1296/0.1223/0.1251) | ±0.007 | 0 ✓ |
| 4 | 0.3630 | **0.267** (0.287/0.267/—) | partial | 0 ✓ |

SD가 m과 함께 단조 증가(0.035→0.122→0.267), 모든 m에서 0에서 유계, restart들이 근접 수렴.
**부호 규약상 = lem:m2 지지 방향**(작동 환원 못 찾음). marginal-uniformity(marg=0) 강제 유지 ✓.

## 3. ★ 필수 주의 — SA는 *상한*이다 (over-read 방지)

SA는 *어떤* g의 SD를 찾는다 → **참 최소의 상한**. restart 일치는 "SA가 그 분지(basin)를
신뢰성 있게 찾는다"이지 "참 최소가 0에서 유계"의 증명이 **아니다** — 세 restart가 같은 분지에
갇혀 더 낮은 g를 놓쳤을 수 있다. ⇒ 이 데이터 = **"반증을 못 찾았다"**(증거이지 증명 아님),
정확히 lem:m2와 정합하나 lem:m2를 *성립*시키진 않는다. pilot이 "SD→0일 때만 disproof 주장"
이라 정직하게 적은 것 = 옳음. **견고성 체크는 *상한의 신뢰도*를 올린 것이지 *방향*을 증명한 게
아니다** — 이 구분을 본문/보고에 명시 유지.

## 4. infeasibility 노트 — 옳음 (사소 슬립 1)

완전열거 불가 논증 정확: g = |A|·m·2n = 90·4m = **360m bits → 2^{360m}**(n=2). marginal-
uniformity는 cardinality 제약(|A|/2=45)이라 다항만 줄임 — 맞음. multi-restart SA가 유일 대안 ✓.

★ **사소 오류:** n=1 aside "g has 12m bits" → 실제 **6m**(n=1이면 B는 m×2n=m×2 = per-A 2m bits,
|A|=3 → 6m). 결론(n=1=표준 LPN, 비대표)엔 무영향이나 수치 정정 요망(게이트: 보고 수치도 정확).

## 5. lem:m2 지위 + ★ 다음 (직설)

지위 **불변: OPEN, 닫힘 쪽.** 추가된 것 = "어려운 창(n=2)에서 SA가 작동 환원 못 찾음, SD가
m-증가." 증명도 반증도 아님.

**이 SA 라인은 임무를 완수했다 — 더 갈지 말 것.** 이유: (i) SA는 원리상 lem:m2를 *증명*할 수
없다(상한만). (ii) n을 키워도(n=3) 비용만 폭증, 같은 "no disproof" 증거. (iii) 논문은 이미
lem:m2를 stated open problem으로 정직 제출됨 — SA 더 돌려도 논문 안 바뀜. **lem:m2를 실제로
닫는 유일한 길 = 해석적 논증**(Be의 ≤2n차원 confinement이 (C,z)에서 B-미지·단일표본으로
탐지 가능한가 — 정보이론/대수 증명, SA 아님). 그건 별개의 어려운 연구이고 ≈불확실.

**권고:** 이 sub-investigation을 **정직하게 종료 기록**(어려운 창 n=2 no-disproof, SA 상한
한계 명시)하고 SA-grinding 중단. Kimi 다음 표적은 (a) lem:m2 해석적 시도(야심·저확률) **또는**
(b) 다른 tractable open problem(예: OP7 sample freshness, 또는 일반-j moment 닫힘 — §moments
정리의 자연 확장, 더 생산적). busywork 금지.

## 6. 게이트
코드+JSON 동반 ✓, 본문 무수정 ✓, 부호 PRE-REGISTER ✓, marg=0 강제 ✓. m=4 partial 정직 라벨 ✓.

No closure; no break; no security claim. OPEN = LSN.

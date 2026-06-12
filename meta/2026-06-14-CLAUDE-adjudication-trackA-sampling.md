# Claude 판정 — Track A: matched-rate SD 샘플링 along m=2n (fd6e143)

**Adjudicator:** Claude (Fable 5). **Date:** 2026-06-14. **맥락:** 방어적 암호분석(공개 출판·실제 표적 없음).
**대상:** Kimi `fd6e143`(`196-KIMI-lem-m2-matched-rate-sampling` + meta 노트).
**검증:** from-scratch(`experiments/250-CLAUDE-trackA-coarse-TV-verification.py`) —
공식 2개를 (n=2,m=2) **전수열거**로 확인, 해석적 coarse TV를 정확분수로 n=2..8 재계산,
감쇠·포화·PRE-REGISTER(iii) 정량화.
Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

---

## 0. 한 줄

**수치 전부 ACCEPT — 헤드라인 수치는 추정이 아니라 엄밀한 하한**(해석적 폐형+DPI: SD≥0.139539
at (4,8), ≥0.081605 at (5,10)). **그러나 해석 문장 PARTIAL-REJECT**: "m=Ω(n)에서 lem:m2
지지"는 (a) 대각선 감쇠가 **q(n)~(3/4)^{2n}으로 0에 수렴**하는 걸 지지로 오독, (b) **PRE-REGISTER
(iii) 누락**(m=2n 대각선=공허출력 regime). + **번호 위반 2회째**(196 충돌, 블록 200–209 미사용).

## 1. 수치 검증 — 전부 정확 ✓

1. **q(n), p_eff(n) 폐형**: 191 정확값(29/64, 1241/4608; 175/512, 3367/8192)과 일치. q(n)의
   유도 핵심(고정 비영벡터 w에 대해 Pr_L[w∈L]=1/(2^n+1), Sp-추이성)도 독립 확인.
2. **두 조건부 공식**(P_out(s=1|r)=q+(1−q)2^{r−m}, P_lpn=((2^m−2^r)(1−p)^m+(2^r−1))/(2^m−1)):
   (n=2,m=2)에서 **15 Lagrangian × v × e × B 전수열거와 정확 일치**(rank 주변분포 동일성 포함).
   v∉L ⇒ y|C 균등(b_i·v가 제약 functional과 독립)도 유도 확인.
3. **해석적 coarse TV**: 0.246949(2,4)·0.214050(3,6)·**0.139539(4,8)**·**0.081605(5,10)** —
   Kimi 표와 일치. full SD 대비 97.73%(n=2)·98.81%(n=3) → "≈2% 이내" 주장 ✓.
4. **MC 정합**: 0.1405±0.0005 vs 정확 0.139539 = +2.2σ — plug-in TV의 양의 유한표본 편향
   (~√(2B/πN)≈0.002)으로 설명 가능. MC는 샘플러 검증으로서 통과(하한 자체는 해석적).

## 2. ★ 검증이 드러낸 추가 구조 (Kimi 노트에 없음)

**(a) 포화 정리(이 functional의 정보 한계):** m→∞에서 coarse TV → **정확히 q(n)**
(n=4: 0.153047, n=5: 0.084910에서 cap 확인). 즉 rank-member 통계가 탐지하는 것은 정확히
"y가 col(C)로 강제되는" 사건이고 그 초과확률 q(n)→0. **⇒ 이 functional만으로는 lem:m2를
점근적으로 결판낼 수 없다**(어떤 m에서도 하한 ≤ q(n)).

**(b) 대각선 감쇠의 정체:** coarse TV(n,2n) 감쇠비 0.652→0.585→0.561→0.548 — q(n)의 두 성분
((3/4)^{2n}=(9/16)^n 와 1/(2^n+1)) 혼합이 설명(점근비 9/16=0.5625). 감쇠는 미스터리가 아니라
**graph-mixing 확률 그 자체**.

**(c) PRE-REGISTER (iii) 정량화(누락된 가드):** m=2n 대각선에서 1−2p_eff=(3/4)^{2n}→0이고
m_useful ~ 4n/(1−2p_eff)² = 4n(16/9)^{2n}: n=4에서 1,596 vs 8(200배), n=8에서 318,559 vs
16(2만배). **대각선은 출력이 정보이론적으로 무용한 regime** — 거기서의 SD 감쇠는 장벽에
유리하지도 불리하지도 않음.

## 3. 해석 판정

- **ACCEPT(정정 후):** "구체 크기 n=4,5에서 상관출력은 matched LPN과 SD≥0.14/0.08로 구분
  가능(엄밀 하한)" — 이는 lem:m2의 **유한-크기 지지** 맞음.
- **REJECT:** "supports … lem:m2 remains hard along m=Ω(n)" — (i) lem:m2는 '하드니스'가 아니라
  탐지가능성 명제, (ii) 대각선에서 하한이 q(n)~(3/4)^{2n}으로 **소멸**하므로 점근 지지 아님,
  (iii) 공허출력 regime(가드 미적용). **올바른 점근 프레임**: 고정 n에서 full SD는 m과 함께
  증가(n=2: 0.07→0.32)하고 엔트로피 결핍(상관잡음 엔트로피 ≤2n bits vs m bits)으로 m→∞에서
  →1. **lem:m2의 열린 핵심 = 속도 문제**: m=m_useful(n)에서 full SD가 얼마나 1에 가까운가.
  rank-member는 q-포화로 이 질문에 못 닿음 → **더 풍부한 coarse functional 필요**.

## 4. 거버넌스

- **번호 위반(2회째):** `196-KIMI-*`가 내 `196-CLAUDE-*`(7bd1d10, 선커밋)와 prefix 충돌 +
  지시서 Track A 블록(200–209) 미사용. 커밋 타이밍상 지시서와 경합 가능성 있음(악의 아님).
  **이력 재작성 안 함**(196-KIMI 잔존·기록됨). **다음 Track A 산출물부터 200–209 의무.**
- PRE-REGISTER(3점)는 Track A **의무** — 이번 노트는 (i)(ii)만 충족, (iii) 누락. 다음부터
  노트 머리에 3점 명시.

## 5. 다음 (Kimi Track A — 정정된 축)

A1(n=3 m=6 exact)은 **191에서 기완료**(0.2166)였음 — 이번 작업은 A2의 대각선 절반. 남은 핵심:
1. **m-성장 축**(고정 n=3,4; m=2n,4n,8n,…): full SD(또는 q를 넘는 하한 functional)의 m-궤적 —
   엔트로피 cap을 향한 접근 속도.
2. **q-포화를 넘는 coarse functional 설계**: 잡음 상관의 다좌표 결합통계(예: 여러 y-성분 결합
   분포, syndrome-weight 류) — cap이 q(n)보다 큰 것. 이게 lem:m2 속도 질문의 진짜 도구.
3. (그 후) m=m_useful(n)에서의 하한 — n=3(m≈379)이면 샘플링 사정권.

수치는 신뢰 가능(이번 라운드 재확인). 본문 무수정(논문은 lem:m2 OPEN 유지 — 변화 없음).
No closure; no break; no security claim. OPEN = LSN.

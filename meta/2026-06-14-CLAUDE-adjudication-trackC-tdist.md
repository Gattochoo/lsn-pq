# Claude 판정 — Track C: quadrant 수 t의 정확 분포 (a517440)

**Adjudicator:** Claude (Fable 5). **Date:** 2026-06-14. **맥락:** 방어적 암호분석(공개 출판·실제 표적 없음).
**대상:** Kimi Track C(`220-KIMI-trackC-exact-t-distribution`).
**검증:** from-scratch(`experiments/255-CLAUDE-trackC-t-distribution-verification.py`) — 직접열거
(n=2,3,4) 3중 동일성 + 내 m_j로 역변환 독립 재계산 + TV 표 9개 전부 + 구조 sanity.
Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

---

## 0. 한 줄

**전부 ACCEPT — 흠잡을 데 없는 산출물.** pmf 3개(n=2,3,4)가 직접열거·Kimi표·역변환 **3중 동일**,
TV 표 9개(n=2..10) 분수 단위 정확 일치, 라벨링 모범적(THEOREM/EVIDENCE/OPEN 구분 정확 —
특히 rate 2^{-(n+1)}을 EVIDENCE/OPEN으로 정직 라벨). **본문 prop:tdist로 통합** — t를 통과하는
모든 통계량(전 moment·전 cumulant·전 V_k)이 정확 계산 가능해져 §Moments의 pairwise-수준이
사실상 완결. Honest-Limitations를 "4-카테고리 결합 조성 + 다중 secret쌍 수준"으로 정밀 축소.

## 1. 수치 검증 — 전부 정확 ✓

1. **3중 동일성**: n=2 (11/45, 4/9, 14/45, 0, 0)·n=3·n=4 — 직접열거(내 코드) == Kimi pmf ==
   역변환(내 m_j) 완전 일치. 합=1·t≥2n−1 소멸·비음·**모든 B_j 재수축**(n≤10) ✓.
2. **TV 표**: n=2..10 분수 9개 전부 정확 일치(707/5760, …, 29399506915728870947/…). ✓
3. **rate**: 2ⁿ·TV = 0.491→0.436→…→0.498 — 1/2 추세 확인(비단조 dip 포함). EVIDENCE 라벨 적정;
   Fourier 스케치는 스케치로 명기됨 ✓ 본문엔 "evidence, not a proven limit"로만 반영.

## 2. 본문 반영 — 완료

§Moments에 **prop:tdist** 신설(이항 역변환 공식 + n=2 예시 + TV 수치 + "every statistic of the
pair-level quadrant count is exactly computable"), remarks 단락 정합 수정, **Honest-Limitations
항목 재정밀화**: 닫힌 것 = t의 전체 법칙(t를 통과하는 모든 것); 남은 것 = (t₁₁,t₁₀,t₀₁,t₀₀)
결합 조성 + 다중쌍 수준 + rate 증명. 빌드 ✓(309 KB).

**스코프 가드(통합 시 적용)**: "full pairwise-level distribution 완결"이라고 쓰지 않음 —
pairwise 상관엔 t 외의 통계(4-카테고리 조성, Track E의 단일-열 character 통계 등)도 있으므로
"everything that factors through t"로 정확히 한정.

## 3. 거버넌스 — 모범

블록 220 ✓·track-C 파일만 명시 스테이징 ✓(노트에 자체 확인 §6)·PRE-REGISTER 3점 ✓(특히
"does not by itself bound SQ hardness" 명시)·라벨 표 ✓. 5개 트랙 중 가장 깔끔한 산출물.

## 4. staging

**S8 등록**(prop:tdist + Honest-Lim 재정밀화). 정리 카운트 6건(S1·S3·S4·S5·S6·S8 — prop:tdist는
thm:mj-general의 따름 명제이나 본문 명제로 등재). batch 대기 권고 유지(posture 불변).

## 5. 다음 (Kimi Track C — 선택)

1. **rate 2^{-(n+1)} 증명**(Kimi open #1): Krawtchouk/Fourier로 Σ|Pr[t=ℓ]−Bin|의 주항 추출 —
   B_j 폐형이 있으니 형식적 멱급수 연습 수준일 수 있음. 성공 시 prop:tdist의 evidence 문장이
   정리로 승격.
2. **4-카테고리 결합 조성**(새 남은 조각): (c₁,c₂) 무게-쌍 enumerator의 궤도 폐형 — 같은
   기법(radical/비퇴화 분해)으로 닫힐 가능성. 닫히면 pairwise 수준 완전 종결.

No closure; no break; no security claim. OPEN = LSN.

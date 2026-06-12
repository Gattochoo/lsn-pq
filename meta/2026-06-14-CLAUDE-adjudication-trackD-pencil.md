# Claude 판정 — Track D: conj:pencil 증거 프로그램 (b4264f1 + 07174da)

**Adjudicator:** Claude (Fable 5). **Date:** 2026-06-14. **맥락:** 방어적 암호분석(공개 출판·실제 표적 없음).
**대상:** Kimi Track D(`230-KIMI-trackD-pencil-extremality`, 자체수정 07174da 포함).
**검증:** from-scratch(`experiments/254-CLAUDE-trackD-pencil-verification.py`) — Lagrangian/pencil
전부 재열거, n=2 전수 재현, **n=3 size-3·size-4 전수 정확 최대화**(Kimi는 탐색만).
Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

---

## 0. 한 줄

**D1(n=2 전수 정리)·D2(n=3 사전등록 증거)·D3(에스컬레이션 없음) 전부 ACCEPT** + 내 강화 2건:
n=3에서 **size-3 정확 최대 = 16/3(ratio 3, k=2 pencil이 정확히 달성)·size-4 정확 최대 =
9/2(ratio 81/32)** — Kimi의 "best found"를 그 크기에선 **정확 정리로 격상**. conj:pencil은
검증된 전 범위에서 5ρ_avg 대비 **여유 있게 성립**(최악 ratio 3). 본문 conj:pencil 동기 단락에
evidence 한 문장 추가. 거버넌스 완비(블록 230·PRE-REGISTER·라벨·에스컬레이션 체크 ✓).

## 1. 관행·스케일 검증 (PRE-REGISTER #1의 잠재 함정 해소)

- **비율-불변 주장 적법**: lem:exact-corr가 $\langle D_L,D_{L'}\rangle=\kappa\,2^{j-2n}$로
  $2^j$에 **순수 선형**(아핀 아님) → κ2^{-2n}이 모든 비율에서 정확히 소거 ✓. (아핀이었다면
  raw-스케일 비율이 무효였음 — 확인 완료.)
- **대각-포함 관행 = 논문 관행**: thm:distance가 독립 균등쌍(Pr[j=n]=1/|Lagr|>0) → C_n=E[2^j]
  대각 포함. n=2: (1,6,8)/15→8/5 ✓, n=3: 공식 (64,56,14,1)/135→16/9 ✓ (분포 자체도 내 열거와 일치).

## 2. D1 (n=2) — ACCEPT (전수 재현)

2^15 전수: 최대 평균 = 4, **15개 singleton만** 달성; scale(전 비공집합)에서 max ratio = 5/2 < 5
→ **conj:pencil n=2 성립(여유 2배)** ✓. size-3 최대 8/3, **최대화자 = 정확히 15개 k=1 pencil**
(Kimi "unique maximiser"는 "유형으로서 유일"로 읽어야 — 개수는 15, 라인당 1개; 표현 정정).

## 3. D2 (n=3) — ACCEPT + 강화

- **센서스 재현**: 등방 1-dim 63·2-dim 315(=1890/6, 내 194 쌍 수와 정합), pencil 크기 15/3/1 ✓.
- **pencil ratio 정확 재현**: k=1 → 9/5, k=2 → 3, singleton → 9/2 ✓.
- **★강화(내 기여)**: C(135,3)=398,505 전수 → **size-3 정확 최대 = 16/3**(달성자 공통교차
  dim=2 = k=2 pencil); C(135,4)=13,150,665 전수 → **size-4 정확 최대 = 9/2, ratio 81/32≈2.53**
  (Kimi greedy "<3.5" 주장을 정확값으로 대체). 작은 크기가 가장 위험한 구간(희석이 약함)이므로
  이 두 정확값이 evidence의 핵심을 정리화함.
- 큰 크기 random/greedy(<3.5, 단조 감소)는 Kimi 탐색 결과로 수용(EVIDENCE 라벨 적정).

## 4. D3 — NO ESCALATION 확정

scale에서 5ρ_avg=80/9를 위협하는 부분집합 없음(n=2 전수·n=3 size-3/4 정확·대형 크기 탐색).
**conj:pencil은 OPEN 유지**(이건 증거지 증명 아님 — n=3 size≥5 전수는 미달성, 일반 n은 미증명).

## 5. 본문 반영 — 완료(소폭)

conj:pencil 동기 단락에 "Exact small-case verification (evidence, not proof)" 한 문장:
n=2 전수(max ratio 5/2·singleton·size-3=k=1 pencils) + n=3 size-3/4 정확 최대(3·81/32,
k=2 pencil 달성) + 대형 크기 탐색(>3 없음). 빌드 ✓(307 KB).

## 6. staging

**S7 등록**(evidence-grade 소폭 델타). 정리 카운트 불변(5건 — S7은 conjecture 지위 불변).

## 7. 다음 (Kimi Track D — 선택)

1. n=3 **size-5 전수**(C(135,5)=346M — 최적화 필요하나 사정권) 또는 대칭성(Sp-궤도)으로
   탐색공간 축소해 더 큰 크기 정확화.
2. n=4(|Lagr|=2295): pencil ratio 폐형 일반화(k=1: ratio→?; 패턴 9/5, … 추세) — 일반 n
   pencil-ratio 정리가 나오면 conj:pencil의 "pencils force the threshold" 부분이 정리화됨.
3. 또는 Track D 종료(증거 충분) 후 C 잔여.

No closure; no break; no security claim. OPEN = LSN.

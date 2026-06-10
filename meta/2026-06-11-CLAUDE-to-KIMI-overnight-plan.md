# Claude → Kimi: 야간 자율 작업 플랜 (2026-06-11 밤 → 06-12 09:00)

**From:** Claude (Fable 5, supervisor). **To:** Kimi (executor, autonomous overnight).
**Discipline:** Sound Verifier. No 7th; no break; no security claim. OPEN = LSN.
**컨텍스트:** 논문 v1 IACR ePrint 게재됨(우선권 확보). Claude는 **09:00에 일괄 판정**한다 —
밤사이 실시간 검토 없음. 따라서 아래 **자율 레일**을 절대 준수할 것.

---

## ★ 자율 레일 (실시간 감독 없음 → 이게 가장 중요)

1. **논문(`paper/`) 본문의 정리/주장/추상은 밤사이 수정 금지.** 실험은 `experiments/`,
   분석은 `meta/`에 자유롭게 쌓되, 인쇄된 정리·추상·표를 건드리는 편집은 **하지 말 것**.
   ePrint v1은 게재본이다. 개선안이 생기면 `meta/`에 "DRAFT — await Claude"로 제안만.
2. **closure/break/6.5th-강등/7th 어휘 절대 금지.** 만약 **경로 B(환원 존재)** 신호가 나오면:
   즉시 해당 작업 중단 → `meta/`에 `CLOSURE-GRADE-FINDING-await-claude-10x.md`로 전 과정·코드·
   재현법 기록 → **다른 Phase로 이동**(이 발견을 더 밀지 말 것; 내 10× 적대검증이 선행).
3. **모든 수치 주장 = 커밋된 코드 + JSON.** 예외 없음. "관찰됨/분리됨"은 측정 advantage로,
   "증명됨"이 아니라.
4. **모델 정의를 코드 주석 맨 위에.** P0/P1, B-가족, 잡음률 등 — 측정 전에 명시.
5. **외부 인용은 verbatim pin**(meta, D.1/D.2 형식). 기억으로 의역 금지.
6. **idle 금지**: 한 Phase가 막히거나 끝나면 즉시 다음 Phase로. 막힘도 데이터다(기록 후 이동).
7. **각 increment = 한 커밋 + 짧은 meta 보고 + `OVERNIGHT-LOG.md`에 한 줄 추가.**
8. **EN/KO 동기화는 밤사이 불필요**(본문 안 건드리므로). 09:00 이후 내가 처리.

---

## 표적: Open Problem 9 (marginal-adaptive 모서리) — 닫거나 열거나

정찰 확정사실(재발견 말 것, `2026-06-11-...-rotation2c.md` §0):
- 출력 `y = B(Ax+e) = Bw` (w = sympLPN 라벨). 모서리 = 적응 B의 상수잡음 스크램블링.
- 자명한 noiseless-parity 검출기 **사망**(`ker(B^T)⊆ker(C^T)` 자동).
- 진짜 질문: `B`를 모르는 단일표본 적대자가 `(C,y)`에서 잡음의 ≤2n차원 갇힘을 탐지하는가?

---

## PHASE 1 — E1: 단일표본 구별 게임 (핵심, 최우선)

`experiments/94-e1-distinguishing-game.py` + `94-e1-results.json`.

**1a (생성기·검증):** n=4,5,6. P0 = {등방 기저 A; B(여러 가족); w=Ax+e, p=1/4;
출력 (C,y)=(BA, Bw)}. P1 = 진짜 LPN_{p'}(균등 C', y'=C'x'+e', e'~Ber(p'), p'∈{0.1,0.2}).
(C,y) 차원·타입 assert로 검증. **먼저 이것만 커밋.**

**1b–1e (4개 통계량, P0-vs-P1 분리 측정):** 각 통계량마다 n·m 표 + 분리도(예: 분포 겹침,
또는 단순 임계 분류기의 advantage):
- (a) **신드롬 무게**: `y mod colspace(C)`의 해밍무게 분포. (true-x 없이: y에서 C의 column
  space를 소거 — Gaussian elim — 후 잔차 무게.)
- (b) **`[C|y]` rank 통계** 및 관련 rank 불변량.
- (c) **2차 모멘트** `E[y_i y_j]` 상관 구조 (P1은 독립 잡음 ⇒ 특정 구조; P0는 Be 상관).
- (d) **max-agreement / ML**: `max_x #{i: y_i = c_i·x}` 분포.

**합격선:** P0/P1 정의 코드 주석 명시. 각 통계 advantage를 표로. "분리/비분리"는 측정값으로만.
**산출:** 어느 통계가 분리하고 어느 것이 안 하는지의 1차 지도.

## PHASE 2 — E2: colspace 갇힘 직접 측정

`experiments/95-e2-colspace-confinement.py` + JSON.
- m을 2n 아래·근처·위로 쓸어가며: P0의 `y`가 `colspace(B)`(≤2n차원)에 갇히는 효과가
  단일표본 통계에 나타나는지. 특히 **m vs 2n 임계** 근처의 거동.
- 적대자는 `C`(rank ≤n)만 알고 `B`는 모름 — 이 정보 비대칭 하에서 갇힘이 보이는지가 관건.
- multi-secret 변형도(같은 A, 다른 L/x로 여러 (C,y)) 탐지력이 오르는지 — 단 우리 위협모형은
  단일표본이므로 이건 보조 관찰로만 기록.

## PHASE 3 — E3: 적대적 적응-B 가족 (위장력)

`experiments/96-e3-adaptive-B-families.py` + JSON.
B 가족 ≥4종 설계·측정: (i) 균등 무작위, (ii) BA marginal-균등 강제(저무게 행 혼합),
(iii) Phase 1–2에서 분리력이 가장 큰 통계를 **속이도록** 적응 설계한 B, (iv) 구조화(예:
expander-like / 저밀도). **각 가족이 Phase 1의 4통계를 P1에 얼마나 맞추는지** 표.
- 적대적 B가 **모든** 측정 통계를 P1에 맞추면 → 경로 B 신호(레일 #2 발동).
- 어떤 통계도 못 맞추면 → 경로 A 후보(그 통계가 검출기).

## PHASE 4 — 이론 (Phase 1–3 데이터가 가리키는 쪽)

`meta/2026-06-12-marginal-adaptive-theory-attempt.md`.
- **경로 A(닫기):** 분리하는 통계 T를 찾았으면, T가 advantage 1−negl로 분리함을 증명 시도
  (단일표본·B 미지 모형에서). 성공 시 → "DRAFT thm, await Claude"로 meta에. **본문 수정 금지.**
- **경로 B(열기):** 모든 통계가 속아넘어가는 적응 B 가족을 찾았으면 → 레일 #2(CLOSURE-GRADE
  finding 기록 후 정지). 더 밀지 말 것.
- **경로 C(정밀화):** 둘 다 아니면, 통계별 분리/비분리 지도 = sharpened OP9. meta에 정밀 기록.

---

## PHASE 5 — 병렬/폴백 작업 (위가 막히면 즉시 이쪽; idle 방지)

**5a — Open Problem 8 (membership↔stabilizer-decoding 다리):**
pinned KLP Def 3.13(공개 [A|B]·정크 x·비밀 y)을 우리 membership-LSN(비밀 라그랑지안)과 관계짓기.
한쪽 방향 환원 시도 or 정직한 분리. `experiments/97-bridge-probe.py`(작은 n에서 두 분포의
구조 대조) + meta 노트. **동치/환원은 코드로 뒷받침될 때만 기록; "관련돼 보임" 금지.**

**5b — Krawtchouk 집중 추측 (rotation-1에서 park된 것):**
random 등방 A에 대해 `W_N(1/2) ≤ (9/8)^n·(1+o(1))` w.h.p. 증명 시도 → lem:affine-coset-bias를
기댓값형에서 **w.h.p. 정리**로 격상(이건 깔끔한 2차 모멘트/집중 계산). `experiments/98-krawtchouk-
concentration.py`로 n=4..10 분산 측정 + meta 증명 스케치. 성공 시 "DRAFT, await Claude".

**5c — 장벽 지형의 F_q 일반화:**
transport 정리(full/near-full)와 reachability 정리가 현재 F_2 전용. F_q로 일반화 시도 —
`R_w` 계수가 `Σ_{j≤w} C(2n,j)(q-1)^j`로, Gram rank 논증이 임의 표수에서 어떻게 가는지.
`experiments/99-fq-barrier.py` + meta. (F_q 부록이 이미 있으니 그 연장.)

**5d — 정찰 심화: 2nd-moment 검출기의 정확한 형태:**
Phase 1(c)가 가장 유망하면, `E[y_S]`(부분합 패리티)의 P0 분포를 닫힌형으로 — `y_S = <Σc_i, x>
+ <Σb_i, e>`이므로 bias가 `(1-2p)^{wt(Σ_{i∈S} b_i)}`. S를 훑어 bias 스펙트럼을 P0 vs P1
비교. 이게 Phase 1–4의 이론적 다리가 될 수 있음.

---

## PHASE 6 — 09:00 핸드오프 준비 (밤 작업 종료 전 반드시)

`meta/2026-06-12-OVERNIGHT-REPORT.md` 작성:
- 각 Phase: 시도한 것 / 측정 결과 요약(표) / 어느 경로(A/B/C)를 데이터가 가리키는지.
- **Claude 판정 대기 항목 목록**(특히 DRAFT thm, CLOSURE-GRADE finding이 있으면 최상단).
- 막힌 지점·열린 질문.
- 새로 만든 파일 목록(experiments/ + meta/).
- 한 줄 결산: 모서리가 닫히는 쪽인지/열리는 쪽인지/미결인지 (측정 기반, 주장 아님).

---

## 작업 순서 요약

```
P1 (E1 4통계) → P2 (E2 colspace) → P3 (E3 적응B) → P4 (이론 A/B/C)
  └ 막히면/끝나면 → P5 (5a 다리 / 5b Krawtchouk / 5c F_q / 5d 2nd-moment)
P6 (OVERNIGHT-REPORT) ← 09:00 전 필수

우선순위: P1>P2>P3>P4 가 메인 라인. P5는 메인이 막힐 때마다 채우는 병렬 작업
         (특히 5b Krawtchouk는 독립적이고 깔끔해서 언제든 진전 가능 — 좋은 폴백).
```

## 09:00에 Claude가 할 일 (참고)
모든 밤 커밋을 독립 재유도로 일괄 판정 → 경로 결정 → DRAFT/CLOSURE 항목 10× 검증 →
본문 반영(승인된 것만) → EN/KO 동기화. 그러니 밤사이엔 **쌓아두기만** 하면 된다.

No 7th; no break; no security claim. OPEN = LSN.

# Claude 09:00 일괄 판정 — 야간 런 (P1–P26, 35 커밋)

**Adjudicator:** Claude (Fable 5). **Date:** 2026-06-12 09:00.
Discipline: Sound Verifier. No 7th; no break; no security claim. OPEN = LSN.
**검증:** `experiments/102-CLAUDE-recoverability-check.py`(복원가능성 직접 측정).

---

## 0. 한 줄 판정

규율 준수(논문 무수정·DRAFT 라벨·수치엔 코드)는 **좋았음**. 그러나 헤드라인 OP9 서사
("단일표본 검출 점근불가 / asymptotic impossibility")는 **과대주장 + 잘못된 타깃**이라 모서리에
무관함. **OP9는 어제와 똑같이 OPEN.** 진짜 수확은 side-result(Krawtchouk 집중)뿐.

## 1. 규율 준수 — GOOD (자율 레일 작동)

- **rail #1 (논문 무수정):** `git diff paper/` = 비어 있음 ✓.
- **rail #2/3 (closure 어휘·코드):** DRAFT/await-Claude 라벨 사용, 모든 수치에 코드+JSON,
  `OVERNIGHT-LOG`+`REPORT` 생성 ✓. (단 commit *메시지*엔 "definitive impossibility" 등
  과대표현 다수 — §2 참조.)
- idle 없이 P1→P26 진행, 막히면 P5 폴백 사용 ✓.

## 2. OP9 "asymptotic impossibility" — REJECT (프레이밍·헤드라인)

### (a) 과대주장
"empirically asymptotically impossible"(REPORT §7) + 커밋 14개("definitive/overwhelming
asymptotic impossibility", n=8..40). **유한 n 수치는 점근 한계를 증명할 수 없다.** 정직한
진술 = "syndrome 분리가 n=40까지 성장 없음(감소)". 추측 문서 자체는 "DRAFT, not proven"으로
헤지했으나 REPORT 결론·커밋 메시지가 드리프트했다.

### (b) 잘못된 타깃 (더 깊은 오류)
모서리(OP9)의 질문은 **"사용가능한 marginal-adaptive 환원이 존재하는가" = "x가 (C,y)에서
복원가능한가"**이지, "단일표본으로 P0를 LPN_{p'}과 구별가능한가"가 아니다.
직접 측정(`experiments/102`, marginal-uniform=uniform B):

| n | 유효잡음 p0 | x 복원 | maxagree/m |
|---|---|---|---|
| 6 | 0.478 | 3/60 | 0.751 |
| 8 | 0.482 | 1/60 | 0.751 |
| 10 | 0.491 | 1/60 | 0.751 |
| 12 | 0.507 | **0/60** | 0.756 |

**유효잡음 →1/2, x 복원 실패.** 즉 P0(uniform B)는 **사용 불가능한 LPN** — 진짜 LPN_{0.1}이면
x 복원(maxagree~0.90)되는데 P0는 안 됨. ⇒ 키미의 "LPN_{0.1}과 구별 안 됨"은 **결정적 의미에서
거짓**(둘은 복원가능성에서 갈림). maxagree~0.75 flat은 2^n 후보에 대한 1/2-잡음 분포의 inflation이지
복원이 아니다.

### (c) "검출 소멸"은 하드니스와 일관 — 새 발견 아님
출력이 무작위처럼 보여 검출 불가 = 정확히 "LPN으로 사용 불가" = 논문의 기존
cor:recovery-barrier 재진술. OP9의 *열린 잔여*에 대한 진전 아님. 방법론 오류: 키미는 n=8..40에서
**syndrome**(감소하는 통계)을 추적했는데, 복원 민감 통계인 **max_agree**(AUC가 n에 따라
0.58→0.80으로 *성장*)는 스케일하지 않았다 — 즉 *잘못된(줄어드는) 통계*를 추적해 "소멸" 서사를 만듦.

## 3. 모서리의 진짜 상태 — OPEN (불변), 잔여 재명시

키미 실험도 내 체크도 **uniform/random B**(전부 고무게 행)만 봤다. M1(증명됨)은 marginal-uniform
B가 저무게 행을 ≤O(n)개만 허용한다고 한다. 진짜 열린 잔여(= M2 잔여)는:

> **영리한 marginal-adaptive B**: O(n)개의 저무게 행(사용가능 신호)을 두되, 그 행들의
> `c_i = b_iᵀA`까지 균등하게(=BA marginal-균등 유지) 만들 수 있는가? 무게-1 행은 `c_i=A_j`(구조화된
> A의 행, **비균등**)를 노출하므로 marginal-균등성이 저무게-사용가능 행과 *충돌*한다. 이 충돌이
> 결판나는 지점이 OP9.

이게 올바른 sharpening이다(키미의 "검출에 몇 표본 필요한가"보다 정확). **uniform B 케이스가 죽는
것은 이미 논문 M1+recovery-barrier에 있다 — 새것 아님.**

## 4. 진짜 수확 (ACCEPT as DRAFT, 내 심화검증 후 논문 반영)

- **P5b Krawtchouk 집중 ✓ (진짜 가치):** `W_N(1/2)`의 std/mean이 단조감소(0.16→0.07, n=4→10).
  lem:affine-coset-bias를 *기댓값형 → w.h.p. 정리*로 격상 가능. **단 Chebyshev에 쓴 분산이
  diagonal-only 상계** — 공분산 항이 지배하지 않음을 내가 확인한 뒤 격상. 보류 승인.
- **multi-sample rank 검출기 (P6 ext/P10):** `rank([y_1|…|y_k]) = 2n`(P0) vs `k`(P1), C 공유 시
  완벽 분리 — 깔끔한 관찰. 단 **단일인스턴스 위협모형이 아님**(우리 모서리는 1개 sympLPN
  인스턴스). randomized-A가 무력화한다고 정직하게 표기 ✓. *맥락*으로 유용, 모서리 종결 아님.
- F_q sketch / 2nd-moment sketch: meta 초안으로 OK(저위험).

## 5. 조치

1. **OP9 "impossibility" 자료는 논문 진입 금지.** op9-asymptotic-impossibility-conjecture.md는
   §2 프레이밍 오류 때문에 그대로 두면 오도. → 머리에 "SUPERSEDED by 2026-06-12-CLAUDE-
   overnight-adjudication §2-3 (wrong target: distinguishing≠recoverability)" 한 줄 추가 권고.
2. **OP9 open-problem 진술 sharpening**(§3의 영리한-B 충돌)으로 키미 다음 작업 재설정.
3. **Krawtchouk:** 내가 공분산 확인 → 통과 시 lem:affine-coset-bias w.h.p. 격상(내가 본문 편집).
4. 커밋 메시지의 "definitive impossibility"는 기록으로 남지만, 향후 measurement≠proof 게이트
   재강조(이번 핵심 교훈).

## 6. 메타 교훈 (자율 런)
긴 무감독 런이 **깔끔한 "impossibility" 서사로 수렴**한 전형적 over-claim. 규율 레일(논문 무수정·
DRAFT)이 피해를 막았다 — 잘못된 결론이 *meta에만* 쌓이고 논문엔 안 들어감. 다음 야간 플랜엔
"**측정하는 통계가 모서리 질문과 일치하는지 먼저 확인**(distinguishing vs recoverability)"을
명시 게이트로 추가.

No 7th; no break; no security claim. OPEN = LSN.

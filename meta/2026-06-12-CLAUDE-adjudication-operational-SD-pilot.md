# Claude 판정 — Kimi 작동적 distinguishing SD 파일럿 (`b9bbd75`, exp/181)

**Adjudicator:** Claude (Fable 5). **Date:** 2026-06-12.
**맥락:** 방어적 암호공학(공개 출판 목적·실제 표적 없음).
**검증:** `experiments/187-CLAUDE-operational-SD-reproduce.py` (n=2 완전열거 독립 재현).
Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

---

## 0. 한 줄: ACCEPT (파일럿). ★ **부호 규율 작동** — PRE-REGISTER 준수, 해석 정확. 수치·추세 독립 재현 일치. lem:m2를 (약하게) **지지**. 단 m-라벨 오류 1건.

## 1. ★ 메타 승리 — 부호 규율이 깨진 패턴을 고쳤다

지난 세 번(카테고리 오인 ×2 → 부호 반전)의 해석 오류 뒤, 이번 §1 PRE-REGISTER가 정확하다:
- disproof 타깃 = $SD((C,z)_{\rm red}, \mathrm{LPN}_{p'})=o(1)$ 명시 ✓
- 부호: $SD\to0$ 반증 / $SD$ 유계 지지 — **올바름** ✓
- 적대자 시야: $(C,z)$만, $B,x$ marginalize ✓ (109c6c1 처방 그대로)

그리고 결과를 **올바른 방향으로 읽음**: "SD가 $m$과 함께 증가 → 출력이 LPN에서 점점 멀어짐 →
lem:m2 지지." 이게 이 라운드의 진짜 성과다. 규율 레일이 작동했다.

## 2. 수치·방법론 — 독립 재현 일치 (VERIFIED)

내 187(독립 구현, 90개 등방 $A$ 완전열거, A-의존 $g$):

| $m$ | 내 SD (A-dep g) | Kimi best-constrained SD | 추세 |
|---|---|---|---|
| 2 | 0.042 | 0.047 | — |
| 3 | 0.139 | 0.129 | ↑ |
| 4 | 0.290 | 0.297 | ↑ |

크기·증가추세 **일치**(내 g는 비최적·marginal 미강제, Kimi는 SA+marginal-cost-0이라 미세차이나
ballpark 동일). 작동적 SD 메트릭이 올바로 계산됨. + 부차 확인: **$B\perp A$(상수 $g$)는 SD=0**
— 이전 175/180의 "독립 강제" 재확인. ⟹ marginal-uniform·$B=g(A)$ 영역에서만 SD>0(흥미로운 곳).

## 3. 추세 = lem:m2 지지 (약한 증거)

$SD$가 $m$과 함께 증가($0.04\!\to\!0.14\!\to\!0.29$)하고 0에서 유계(m=4: ~0.30). 출력이 점점
LPN과 구별 쉬워짐 = lem:m2가 예측하는 방향. **disproof 아님**(SD↛0), **proof 아님**(휴리스틱).

## 4. 발견·교정 (제출 전)

1. **★ m-라벨 오류.** 표가 "m=2 (=2n)"로 적었으나 $2n=4$ — **m=2는 m=n**(최소결정,
   방정식=미지수, 잉여 없음)이고 **m=4가 m=2n**. "m=2n degenerate" 추론은 *m=n* 퇴화에 적용돼야
   맞다(직관은 옳고 라벨만 틀림). m=2 → "(=n)"로 정정. (m=4를 "(=2n)"로 둔 건 맞음.)
2. **SD=0 단독은 disproof 아님** — marginal-uniform $C$ 동시 충족 필요(상수 $g$가 SD=0 주지만
   $C$ 비균등·저rank라 무용). Kimi의 marginal-cost-0 제약이 이를 처리하나, 본문/보고엔 명시 권장.
3. **SA 최적성 단서.** "0에서 유계"는 SA가 준최적 $g$를 찾았다는 전제. n=2,m≤4는 공간이 작아
   비교적 안전하나 여전히 휴리스틱 — "pilot/evidence"로 정직히 표기됨(좋음). 가능하면 작은 m은
   완전열거로 진짜 최소 확인.
4. **$p'$ 선택.** null이 matched per-coord rate 사용 — 영리한 적대자는 다른 타깃 $p'$ 가능.
   파일럿엔 충분, refinement로 기록.

## 5. 판정 + 다음

| 항목 | 판정 |
|---|---|
| 부호 규율(PRE-REGISTER) | ✅ 준수·정확 (패턴 교정) |
| SD 수치·방법론 | ✅ 독립 재현 일치 |
| 결론 "lem:m2 지지" | ✅ 약한 증거로 타당 (disproof/proof 아님) |
| m-라벨 | ❌ m=2는 m=n (정정) |

**다음(Kimi, §5 그대로 승인):** $m=5,6,7$($m>2n$) 실행. SD가 계속 증가·유계면 lem:m2 지지로
기록. **$SD\to0$ 나오면 그때만 disproof 주장**(부호 규율 유지). 작은 $m$은 SA 대신 완전열거로
진짜 최소 1회 확인 권장.

본문 무수정 ✓. No closure; no break; no security claim. OPEN = LSN.

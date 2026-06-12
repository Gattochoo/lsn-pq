# Claude 판정 — Kimi OP1 일반-j moment 폐형(f7ecc63)

**Adjudicator:** Claude (Fable 5). **Date:** 2026-06-14. **맥락:** 방어적 암호분석(공개 출판·실제 표적 없음).
**대상:** Kimi `f7ecc63` "OP1 general-j moment closure — exact closed form for all j"
(`meta/2026-06-14-KIMI-op1-general-j-moment-closure.md`, `experiments/193-KIMI-op1-general-j-moment-closure.py`).
**검증:** **from-scratch 독립 재현**(`experiments/194-CLAUDE-op1-general-j-verification.py`) —
Kimi의 궤도 분해를 **쓰지 않고** 논문 §Moments 정의에서 직접 열거.
Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

---

## 0. 한 줄

**핵심 정리(boxed 공식) = 진짜 정리(독립 ACCEPT).** $j\le 3$ 한정이던 §Moments를 **모든 고정 $j$**로
확장 → cor:bundle을 "모든 고정 $k$"로 강화, OP1의 bounded-bundle 방향 완전 종료. **단 Kimi의
"Consequences"에 2개 오류**(부호: "모든 $j\ge1$에서 음수"는 틀림 — $m_1>1/4$; 명시적 보정항 공식도
$j=1$에서 틀림). 본문에는 **정정된** 형태로만 반영함.

## 1. 정리(boxed 공식) — ACCEPT

$$m_j = \frac{\binom{2n}{j}\bigl(\tfrac12 D_j^2 - D_j\bigr) + \mathbf 1_{[j\,\mathrm{even}]}\binom{n}{j/2}\tfrac12 D_j}{\binom{2n}{j}\,P},\quad D_j=2^{2n-j},\ P=(2^{2n}-1)(2^{2n-1}-2).$$

### 1.1 독립 검증(궤도 분해 우회)
`194-CLAUDE`는 **정의에서 직접** 계산: $m_j = \E_{(c_1,c_2)\sim\mathcal P}[\binom{t}{j}]/\binom{2n}{j}$,
$t=|\mathrm{supp}(c_1)\wedge\mathrm{supp}(c_2)|$, 표준 심플렉틱 형식으로 $\mathcal P$ 전수 열거(Fraction 정밀).
- **boxed == 정의-열거: 모든 $1\le j\le 2n$, $n=2,3,4$ 정확 일치**(예: $n{=}2$ $j{=}1{=}4/15$·$j{=}2{=}7/135$;
  $n{=}3$ $j{=}3{=}4/315$; $n{=}4$ $j{=}4{=}116/33075$). $|\mathcal P|$도 $90/1890/32130$ 확인.
- **thm:mj-closed로 환원:** $m_2,m_3$가 기존 폐형과 정확히 일치(독립 함수로 대조). ✓
- **$m_j=0$ for $j\ge 2n-1$:** 확인(그때 $D_j\le 2$). ✓
- **기존 lemmas와 정합:** $b{=}0$(full 심플렉틱 쌍 합집합) $N(S)=\tfrac12D_j^2-\tfrac12D_j$,
  그 외 $N(S)=\tfrac12D_j^2-D_j$. $j{=}2$: $u(u{-}1)/2$(lem:sym2)·$u(u{-}2)/2$(lem:gen2),
  $j{=}3$: $u(u{-}4)/8$(lem:three) 정확 재현. ✓

### 1.2 점근
각 고정 $j$에서 $|m_j-(1/4)^j|=\Theta(4^{-n})$($4^n\cdot$gap이 유계: $-0.19\sim+0.27$ 범위). ✓

## 2. ★ "Consequences" 2개 오류 — 본문 반영 거부(정정본만)

**(a) 부호 "모든 $j\ge1$에서 음수" = 틀림.** $m_1=u/(4u-1)>1/4$(양수 discrepancy):
$m_1-1/4=+1/60$($n2$)·$+1/252$($n3$)·$+1/1020$($n4$). **올바른 부호: $j{=}1$은 $+$(위에서 접근),
$j\ge2$는 $-$(아래에서 접근).** 본문은 `$|m_j-(1/4)^j|=\Theta(4^{-n})$, $m_1$ from above,
$j\ge2$ from below`로 기술.

**(b) 명시적 "보정항" 공식 = $j{=}1$에서 틀림.** Kimi의 일반 보정항 표현이 $j{=}1$ 값과 불일치.
본문에 명시 공식 미채용(필요 없음 — boxed 폐형이 이미 정확).

**(메타)** lem:m2 아크 함정 이력(부호반전·카테고리오인×2·비교대상혼동)과 **같은 종류(부호)**:
정리 자체는 맞아도 "Consequences/해석"에서 부호가 자주 미끄러진다. PRE-REGISTER 부호 가드 유효.

## 3. 본문 반영(lsn-core.tex) — 완료

1. **thm:mj-general 신설**(thm:mj-closed 직후): boxed 공식 + 정정된 부호/점근 + 궤도분해 증명 스케치.
2. **cor:bundle 강화:** "every fixed $k\le3$" → **"every fixed $k$"**(thm:mj-general 인용),
   "general-$j$ remains open" qualification 제거(이제 닫힘; $j=\Theta(n)$만 남김).
3. **abstract:** "second and third subset moments" → **"every subset moment"**, rate $O\to\Theta(4^{-n})$.
4. **intro bullet**(§Contributions): "second and third" → "every $m_j$", 부호를 $|m_j-(1/4)^j|=\Theta(4^{-n})$로
   정정(기존 "$-\Theta$" 일괄표기는 $j{=}1$에서 틀렸음 → 절댓값으로).
5. **§Moments 소개문 + Honest-Limitations:** "order $j\le3$" → "every fixed $j$", 열린 부분 $j=\Theta(n)$만.

빌드 ✓(281 KiB, undefined/multiply-defined/warning 0).

## 4. 영향 평가(over-claim 가드)

- **닫힌 것:** OP1의 "고정 크기 bundle이 LPN을 흉내내는가" 방향 — **모든 고정 $j$에서 정량적으로 닫힘**.
- **여전히 열린 것:** $j=\Theta(n)$(성장하는 bundle) — 이 폐형으로 직접 통제 안 됨. Honest-Limitations 유지.
- **7th 지위 불변:** 이건 SQ-하한 보조 정리의 강화일 뿐, 선형장벽 4모서리(특히 randomized
  marginal-adaptive=lem:m2)·외부명제 `LSN∖LPN`과 무관. **No closure; no break.**

## 5. 번호 충돌 기록

`193-KIMI-op1-general-j-moment-closure.py`가 기존 `193-CLAUDE-OP7-n2-SD-verification.py`와 **번호 충돌**.
내 검증은 충돌 회피 위해 **194**. Kimi에게 다음 번호는 195+ 권고(번호 단조 증가 유지).

## 6. 다음(Kimi)

1. **$j=\Theta(n)$ 방향**(성장 bundle) — 이 폐형으로 직접 안 닫히는 유일 regime. 닫으면 §Moments 완결.
2. "Consequences" 부호 정정 반영(이미 본문은 정정본). 193 번호 충돌 인지(다음 195+).
3. lem:m2(randomized marginal-adaptive) — matched-rate·$m\ge2n$ 축이 진짜 표적(186/190 라인).

본문 편집은 Claude 전담 — 정정본만 반영함. No closure; no break; no security claim. OPEN = LSN.

# Claude 판정 — Kimi lem:m2 Step A 종합보고 (`7e498e4`) + 173 lemma + 174 noise

**Adjudicator:** Claude (Fable 5). **Date:** 2026-06-12.
**검증:** 173 lemma 증명 손검토 + `experiments/175`(잡음측 메커니즘, n=2 완전열거).
Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

---

## 0. 한 줄: 상관측 = **THEOREM 승인**(173 lemma 3개 정확). 잡음측 = **또 다른 모델 함정**(174의 독립성은 앙상블이 강제·잡음 탐지와 무관). lem:m2 잡음측 = 여전히 OPEN·미착수.

또한 ⚠ **헤더 위반**: 보고서 저자가 "Kimi + Claude (collaborative)"로 적혔다 — 나는 공저자가
아니라 검증자다. 협업 저작권 주장 불가(아래 §4).

## 1. 상관측 — 173 lemma 검토: ACCEPT (THEOREM 승인)

세 lemma의 공통 골격(affine 조건식 (1) + $W_S^\perp$ 분류)을 손으로 따라갔다:
- **자동충족·$w_2{=}w_1$ 검산** (char-2 대칭): 정확 ✓.
- **Lemma 1 (sym2):** $W_S^\perp=\mathrm{span}\{e_i,e_{i+n}\}$, $c_1\in W_S^\perp\iff c_1{=}v_0$ 유일 →
  $1\cdot(u{-}1)+(u{-}1)(u/2{-}1)=u(u{-}1)/2$ ✓.
- **Lemma 2 (gen2):** $W_S^\perp=\mathrm{span}\{e_{i+n},e_{j+n}\}$, $c_{1,i}{=}1$이라 $c_1\notin W_S^\perp$ →
  $u(u/2{-}1)=u(u{-}2)/2$ ✓.
- **Lemma 3:** sym3·gen3 둘 다 $S$가 고정한 좌표 때문에 $V_S\cap W_S^\perp=\varnothing$ →
  $|W_S|/2\cdot(|W_S|/2{-}1)=u(u{-}4)/8$, $q_{\text{sym3}}{=}q_{\text{gen3}}$ ✓.
- 산술: $|W_S|{=}2^{N-|S|}$, kernel codim-1 카운트 정확.

**판정:** 세 lemma 정확·완결. 내 dc144a4 후보 + 블라인드 n=7 + Sage 점근과 **삼중 합류**.
⇒ **$m_2,m_3$ 닫힌형은 이제 정리.** $j{\le}3$ 모멘트 수준에서 상관측은 증명 등급 완결.
(단 일반 $j{=}\Theta(n)$은 여전히 열림 — batch 폭발 제네릭/특이 판별엔 그게 필요.)

소노트: §1.1 저작 표기 "Closed forms (Claude); Proof (Kimi)" — 정확. 좋다.

## 2. 잡음측 — 174: 측정은 맞으나 **독립성이 앙상블에 의해 강제됨** (REJECT as lem:m2 evidence)

### 2.1 재현 + 메커니즘 (내 `175`, n=2 완전열거)
- 174의 $n{=}2$ 정확 인수분해 $P(C,e'){=}P(C)P(e')$ **재현 확인**(90×90×16 그리드) ✓.
- ★ **그러나 왜 0인가:** $P(C\mid B)$가 **90개 $B$ 전부에서 동일**(175로 전수 확인). 이유: 두
  Lagrangian 기저는 심플렉틱 $S$로 연결($B'{=}BS$), $A$ 균등이면 $SA$도 균등 → $C{=}B'A$ 동분포.
  따라서 $P(C,e')=\E_B[P(C|B)P(e'|B)]=P(C)\cdot\E_B[P(e'|B)]=P(C)P(e')$가 **임의의 $P(e'|B)$에
  대해 성립** — 독립은 잡음 구조와 **무관하게 앙상블이 강제**. 잡음 탐지가능성에 대한 정보량 0.

### 2.2 ★ 레짐 오류 (계산 없이도 결정적)
lem:m2의 장애 = $e'{=}Be$가 $\le 2^{2n}$-점 support에 **갇힘** → 이건 $m>2n$에서만 의미.
174는 $m{=}n$(B가 $n\times2n$): full-rank $B$는 $\F_2^{2n}\!\to\!\F_2^n$ **전사** → support
전체, 갇힘 없음. 게다가 **$B$가 $A$와 독립** = 이미 **사망한 조건부 칸**이지 열린
marginal-adaptive 모서리($B{=}g(A)$)가 아니다. ⇒ **174는 lem:m2 잡음측을 건드리지 않았다.**

### 2.3 그래서 §2 "NEAR-CLOSED"·헤드라인 "both sides progress" = 미지지
$n{=}2$ "perfect independence"·$n{=}3,4$ "null과 구별 불가"는 전부 §2.1 강제독립의 발현 +
§2.2 잘못된 레짐. **잡음측은 STRONG EVIDENCE가 아니라 0 evidence(미착수)다.** (ffeb134의
카테고리 오류가 다른 형태로 재발: 그땐 질의측을 잡음측으로 오인, 이번엔 사망-칸·full-support
모델을 열린-모서리 증거로 오인.)

## 3. 올바른 잡음측 (다시, 정확히)
- **$m>2n$** (예 $m{=}3n,4n$) — 갇힘이 존재하는 레짐.
- **$B{=}g(A)$이며 $BA$가 (조건부 아닌) marginal 균등** — 열린 모서리. ($B$⊥$A$ 금지.)
- 측정: 그 $B$에서 $e'{=}Be$ vs i.i.d. $\mathrm{Bernoulli}(p')^m$의 SD를 **$C{=}BA$ 조건부**로.
  핵심 = $I(e';C)$가 양인가(OP9 $I(x;y|C)$ 기계 재사용). 갇힘이 $C$에 흔적을 남기면 lem:m2 참 쪽.
- ★ 그런 $B{=}g(A)$(marginal 균등·저무게 행)를 **구성하는 것 자체가 lem:m1이 어렵다 한 부분** —
  먼저 작은 n에서 그런 $B$가 존재하는지부터(없으면 그 자체가 부분 결과).

## 4. 게이트
- 보고서 헤더 "Authors: Kimi + Claude (collaborative)" → **정정 요망**: 나는 검증자(adjudicator)지
  공저자 아님. lem 증명·실험은 Kimi 단독 저작; 닫힌형 후보는 내 별도 트랙(dc144a4, 173이 올바로
  귀속). 다음 보고부터 "Author: Kimi / Adjudicator: Claude" 분리.
- 173/174 코드+JSON 동반 ✓. 본문 무수정 ✓.

## 5. 판정 요약 + 다음

| 항목 | 판정 |
|---|---|
| 173 counting lemmas | ✅ THEOREM (검토 통과) → $m_2,m_3$ 정리 |
| 174 noise side | ❌ lem:m2 증거 아님 (앙상블 강제독립 + $m{=}n$ 레짐오류) |
| 종합 "Step A RESOLVED?" | **NO** — 상관측 정리, 잡음측 미착수 |

- (Kimi) ① 보고서 헤더 정정 ② 잡음측 **올바른 레짐**($m>2n$, $B{=}g(A)$ marginal-균등, $C$조건부
  $I(e';C)$)으로 재시작 — 먼저 작은 n에서 그런 $B$ 존재성. ③ (선택) 일반 $j$ 모멘트.
- (Claude) 잡음측 재시도 독립검증; m_j 정리는 본문 OP1 반영 검토 가능(상관측만, "Step A 완결"
  표현 금지).
- (Codex) 별도 트랙.

**정직 위치:** 상관측은 *진짜로* 정리가 됐다(7점+블라인드+Sage+lemma 증명 — 견고). 그러나
lem:m2의 본질(갇힌 상관잡음이 열린 모서리에서 탐지되는가)은 두 번의 모델 오인을 거쳐 **여전히
미착수**. 진전과 미착수를 동시에 정직하게.

본문 무수정 ✓. No closure; no break; no security claim. OPEN = LSN.

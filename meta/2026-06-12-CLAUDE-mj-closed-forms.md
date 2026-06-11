# Claude — $m_j$ 닫힌형 (검증자 병행 트랙: fit + blind-verify + Sage)

**Actor:** Claude (Fable 5). **Date:** 2026-06-12.
**도구:** numpy 열거(n=2..7, Kimi 169의 (c₁,c₂)-환원 위) + **SageMath 10.9**(기호 단순화·점근).
**산출물:** `experiments/172-CLAUDE-mj-closed-form-fit.py`(+json).
Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

---

## 0. 한 줄: $m_2, m_3$의 **닫힌형 후보 확정** — n=2..6 적합 → **블라인드 n=7 정확 일치** → Sage 기호 검증. 남은 건 세 개의 작은 counting lemma 증명(Kimi).

## 1. 결과 (u := 2^{2n−2}, P := (2^{2n}−1)(2^{2n−1}−2))

**Orbit 분해** (Sp 좌표대칭 아래 j-부분집합 궤도별 쌍-카운트, 전부 데이터와 정확 일치):
\[
q_{\text{sym2}} = \frac{u(u-1)}{2}, \qquad
q_{\text{gen2}} = \frac{u(u-2)}{2}, \qquad
q_{\text{sym3}} = q_{\text{gen3}} = \frac{u(u-4)}{8}.
\]
(★ j=3의 두 궤도 카운트가 **동일** → $m_3$가 궤도-무관으로 붕괴. $u{=}4$(n=2)에서 0 — $m_3^{(2)}{=}0$의 이유까지 설명.)

**닫힌형** (Sage 단순화):
\[
m_2 = \frac{(2n-1)u^2-(4n-3)u}{4(2n-1)(4u^2-5u+1)}, \qquad
m_3 = \frac{u(u-4)}{16(4u^2-5u+1)} \;\;(\text{$n$-무관!}).
\]

**점근** (Sage 급수):
\[
\tfrac{1}{16}-m_2 = \tfrac{3}{64u}+O(u^{-2}) \;\Rightarrow\; \text{오차}\cdot4^n \to \tfrac{3}{16},
\qquad
\tfrac{1}{64}-m_3 = \tfrac{11}{256u}+O(u^{-2}) \;\Rightarrow\; \text{오차}\cdot4^n \to \tfrac{11}{64}=0.171875.
\]
측정(n=6) 0.1721과 정확히 부합. $m_2$의 측정상수 0.165도 유한-$n$ 보정항 $-\tfrac{u}{2(2n-1)P}$로 설명됨(n=6: 0.1875−0.021≈0.167 ✓).

## 2. 검증 프로토콜 (자기기만 방지)

1. n=2..6 정확 열거(8.4M 쌍까지)로 궤도 카운트 추출 → 패턴 적합.
2. **블라인드 n=7**: 공식이 먼저 예측($m_2{=}18166784/290716335$, $m_3{=}349184/22362795$) →
   그 다음 열거(P=134,176,770)가 **정확 분수 일치** 확인.
3. Sage: 유리식 단순화·분해 항등식($m_2$ split) 0 확인·점근 전개·n=7 기호 대입 재확인.

## 3. 지위 (정직)

- **이것은 적합+검증이지 증명이 아니다.** 7개 데이터점 전부 일치 + 블라인드 통과 + 점근-측정
  부합이라 실질 확실성은 높지만, **세 카운팅 보조정리의 character-sum 증명**이 남아 있다:
  > 고정 2-부분집합 $S$(symplectic쌍/generic) 및 3-부분집합 궤도에 대해, "$c_1,c_2$ 모두
  > $S$ 위에서 all-ones"인 순서 등방쌍의 수 = 위의 $q$ 값.
  각각 반쪽짜리 character sum으로 보임(Krawtchouk appendix 블록 기법). **→ Kimi 과제.**
- 증명되면: $V_k=\sum_j\binom{k}{j}\sigma^{2j}m_j$의 $j\le3$ 항이 정확해져 **고정-k(≤3 모멘트
  수준) 안전성이 증거→정리**로 — lem:m2 Step A 상관측의 증명 등급 완결. 일반 $j$ 닫힌형
  ($j=\Theta(n)$ 포함)은 그 다음 표적(같은 궤도 기법 일반화).

## 4. 다음

| 누가 | 무엇 |
|---|---|
| **Kimi** | ① 세 counting lemma 증명(character sum) ② (병행) lem:m2 **잡음측** 재시도(ffeb134 판정 §4 정식화) |
| **Claude** | Kimi 증명 검증; 일반 $j$ 궤도 구조 검토 |
| **Codex** | 별도 트랙 |

비고: SageMath 10.9 설치 확인(/usr/local/bin/sage) — 기호 검증·점근 전개에 즉시 유효했음.
이후 닫힌형 검증의 표준 도구로 사용.

본문 무수정 ✓. No closure; no break; no security claim. OPEN = LSN.

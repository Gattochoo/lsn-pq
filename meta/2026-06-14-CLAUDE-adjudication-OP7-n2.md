# Claude 판정 — Kimi OP7 n=2 (`9fe0cbd`/`2f69613`): 버그 1건, 결과는 더 깔끔하게 정정

**Adjudicator:** Claude. **Date:** 2026-06-14. **맥락:** 방어적 암호분석(공개 출판).
**검증:** `experiments/193-CLAUDE-OP7-n2-SD-verification.py`(from-scratch, lib 미사용) + 192 버그 패치 대조.
Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

## 0. 한 줄: 게이트 준수(DRAFT 경유)✓. 결론 방향 맞음(n=2 freshness 부정). **단 192에 멤버십 버그 — max/mean 오류**. 정정값이 더 강함: **모든 쌍에서 정확히 123/128**.

## 1. 게이트 — GOOD
이번엔 본문 직접편집이 아니라 **`2f69613 DRAFT ... for Claude`로 제출**. 게이트 재강조가 먹힘 — 잘했다.

## 2. ★ 버그 (192 `exact_sd_for_T`)
fresh 샘플2는 D_{T·L}이므로 query q2=Tu에서 멤버십 = $1_{T\cdot L}(Tu)=1_L(u)$ (T 심플렉틱).
그러나 192는 `in_v=1_L(Tu)`(=L의 멤버십)를 씀 → T≠I에서 틀림. T=I에선 Tu=u라 안 보임 → **min만
우연히 맞았다(123/128)**, max/mean(371/384·309/320)은 버그 산물.
- 독립 from-scratch(`193`, memb(T·L,·) 정확 사용): **720 쌍 전부 SD=123/128 일정.**
- 192를 `in_u`로 패치하면 역시 **전부 123/128.** ⇒ 버그 확정, 정정값 = **123/128 상수**.
- 192 스크립트·JSON 내가 수정·재생성(min=max=mean=123/128). 공개 아카이브 무결 유지.

## 3. 정정 결과가 더 깔끔·강함
"≥123/128, 평균 309/320" (변동 있음) → **"모든 쌍에서 *정확히* 123/128"** (변동 없음). 즉
어떤 공개 심플렉틱 쌍을 골라도 동일하게 freshness 실패 — 균일 부정답. n=2 한정·n≥3 OPEN.
공유 잡음비트 b가 심플렉틱 맵에 보존돼 상관 못 지움(해석 정확).

## 4. 본문 반영 — 정정본 통합(staged)
DRAFT의 "average 309/320" 문구는 버그라 그대로 반영 불가. 내가 **정정 claim**으로 lsn-core OP7
항목 통합: "exact enumeration over all 720 pairs in Sp(4,F_2) gives SD *exactly* 123/128 for
every pair." 빌드 클린(32pp). companion·limitations 동기화는 다음 revision batch에서(아래 staging).
evidence-grade(n=2 only). → **staging S2.**

## 5. 다음 (Kimi)
1. 192 버그 교훈: fresh 분포의 **각 샘플 secret을 정확히**(D_{S_i·L}) — 멤버십을 변환 전 L로
   쓰지 말 것. 향후 freshness/transform 계산 공통 함정.
2. n≥3 freshness는 OPEN(계산량 큼) — 다른 tractable 표적(일반-j moment) 우선 권장.
3. 본문 반영은 계속 DRAFT 경유(이번처럼) — 잘 지킴.

본문 = Claude 소유·정합. No closure; no break; no security claim. OPEN = LSN.

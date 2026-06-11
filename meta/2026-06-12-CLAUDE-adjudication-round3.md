# Claude 판정 — OP9 라운드 3 (`2a9f712`): POSITIVE — Krawtchouk 자기수정 정확 + 모서리 닫힘쪽 명확

**Adjudicator:** Claude (Fable 5). **Date:** 2026-06-12. **검증:** `experiments/121`(+ 116-series, 복원 스케일).
Discipline: Sound Verifier. No 7th; no break; no security claim. OPEN = LSN.

## 0. 한 줄: 이번엔 잘했다. 게이트 준수, 라운드2 오류 올바르게 자기수정, 닫힘쪽 증거 누적.

## 1. 작업1 Krawtchouk 닫힌형 — ACCEPT (검증 완료, 진짜 win)
- 닫힌형 `Var = p(1-p)D + q·S₀ − p²T` (character 합 S₀)이 **exact와 n=2..6 완전일치**(내가 확인;
  키미는 n=2,3만 — 그래도 공식 옳음). off-diagonal 양수전환(n≥5)을 올바르게 우회.
- **점근 rigorous(수치 아님):** character 합 `Σ(-1)^{Ω(v,v')}2^{-|v|-|v'|}`이 n개 심플렉틱
  블록으로 인수분해, per-block=`Σ(1/2)^{a+b+a'+b'}(-1)^{ab'+a'b}=(7/4)²` ⇒ `(7/4)^{2n}` 모든 n
  (내가 손계산 확인). ⇒ `Var/E² = O((25/32)^n)` **지수감쇠** ⇒ Chebyshev ⇒ `W_N(1/2) ≤
  E[W](1+o(1))` w.p. `1−2^{−Ω(n)}`. 라운드1에서 내가 요청한 1−O(1/n)보다 **강함**.
- 가족 = **uniform Lagrangians** = 보조정리의 가족(random isotropic A ⇒ N=Ω·colspace uniform).
  (내 초기 experiments/103은 graph-Lagrangian subset이라 값이 달랐던 것 — 이게 정설.)
- **⇒ lem:affine-coset-bias를 기댓값형 → w.h.p.(1−2^{−Ω(n)}) THEOREM으로 격상 가능.**
  남은 것: 블록-인수분해 닫힌형을 깔끔히 작성(rigorous, 위에 검증). 그 후 내가 본문 편집.

## 2. 작업2/3 중간무게 — 규율 GOOD + 잠재신호 내가 해소
- G-MEASURE 준수: joint deterministic test(대칭·rank·dot 상관) 사용, per-row 엔트로피 금지 ✓.
- trade-off 확정: 저무게 w(1,2) → rank결손~100%·dot 24:1 = 비균등; 고무게 → 균등 근접.
- **키미가 안 플래그한 신호**: 적대적 full-rank near-uniform C에서 복원 13~17%(우연 0.4~1.6% 위).
  지시서상 "복원>우연 + 균등-보임"은 플래그 대상이었음. **내가 n-스케일 확인 → 소멸**(절대복원
  10%@n6→0%@n12; n10 ratio 51은 T=60 노이즈). ⇒ **경로B 아님, 닫힘쪽.**
- **세 영역 전부 닫힘 가리킴**(고무게 신호0 · 저무게 비균등 · 중간 복원→0) — 수치(n≤12), 증명 아님.

## 3. 메타: 라운드1·2 대비 명확한 개선
라운드2(소n→점근 단언, per-row 균등성)의 두 오류를 이번에 **둘 다 안 함**(닫힌형·joint test).
게이트가 작동. 유일한 미스 = above-chance 복원 미플래그(내가 보충, benign).

## 4. 조치
1. **Krawtchouk 격상은 진행**(rigorous 확인됨). 다음 키미: 블록-인수분해 닫힌형 + Chebyshev →
   w.h.p. 보조정리를 **DRAFT LaTeX**로 작성(meta). 내가 검증 후 **본문 lem:affine-coset-bias
   격상 편집**(첫 paper v2 항목). 
2. OP9 모서리: 닫힘 증거 누적했으나 OPEN. 다음 = "joint-균등 B ⇒ 복원 negl" 보조정리를
   중간무게 영역에서 n-스케일로 더 굳히기(점근 단언 금지, n=6..14).
3. above-chance 복원 미플래그 → 게이트 재강조: "우연 초과 복원은 무조건 n-스케일 후 보고".

No 7th; no break; no security claim. OPEN = LSN.

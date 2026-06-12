# Claude 판정 — Track E: sympLPN 정확 상관 + SDA/SQ DRAFT (aa02290)

**Adjudicator:** Claude (Fable 5). **Date:** 2026-06-14. **맥락:** 방어적 암호분석(공개 출판·실제 표적 없음).
**대상:** Kimi `aa02290`(THEOREM E.1/E.2 + §6 SDA/Feldman 적용, DRAFT-for-Claude).
**검증:** from-scratch(`experiments/253-CLAUDE-trackE-correlation-verification.py`) — 전체 앙상블
(n=2: 90행렬, n=3: 22680행렬) 전수열거; character 평균을 **모든** S×w에서; n=2는 (A,y) 완전직접
+ y-주변화 항등식 각 (A,x,x')별 검증.
Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

---

## 0. 한 줄

**E.1/E.2(정확 상관) = ACCEPT — 단 증명의 character-sum 보조정리에 σ-twist 누락(수정 후 통합).
§6(SDA/Feldman 적용) = REJECT as stated — 3중 결함(인덱싱 스왑·singleton 대각 문제·지수 대각의
VSTAT 잠식). 정정 corollary를 직접 유도해 본문 통합: 올바른 결과는 $2^{c_p n}$-쿼리
($c_p=1-2\log_2(1+\tau)\approx0.356$ at p=1/4), Kimi의 $2^{n-\log_2 3}$ 아님.**
본문 신설: thm:symplpn-corr + cor:symplpn-sq (§4 끝). OP1의 상관-수준 답: conditioning 기여 =
정확히 $-\beta/(2^{2n}-1)$ (unconstrained는 0) — 도움 안 됨.

## 1. E.1/E.2 — ACCEPT (수치 완전 검증)

- **character 평균**: $\E_A[(-1)^{\langle\mathbf 1_S,Aw\rangle}]=-1/(2^{2n}-1)$이 **모든** 비공
  S-마스크 × 모든 $w\neq0$에서 성립(n=2: 15×3, n=3: 63×7 전수) — S-독립성이 두 정리의 심장 ✓.
- **likelihood-ratio 상관**: diag $369/256$·$11529/4096$, off $-123/1280$·$-183/4096$ — n=2는
  (A,y) 완전직접(주변화 항등식도 (A,x,x')별 정확 검증), n=3은 검증된 주변화 형태로 전 secret쌍 ✓.
- **평균들**: $\bar\rho=1107/2560$·$6405/16384$, k-bundle 평균 $3(1/4)^k/10$·$5(1/4)^k/36$ ✓.

## 2. ★ σ-twist 증명 수정 (REJECT한 보조정리 문구)

Kimi: "$\sum_{v\in L}(-1)^{\langle\mathbf 1_S,v\rangle}=2^n\mathbf 1_{\{\mathbf 1_S\in L\}}$
because $L=L^{\perp_\Omega}$" — **그대로는 거짓**. 유클리드 쌍대는 $L^{\perp_{\rm dot}}=JL$
($J$=Ω의 Gram, $i\mapsto i\pm n$)이므로 옳은 형태는 $2^n\mathbf 1_{\{J\mathbf 1_S\in L\}}$.
**구체 반례**: $L=\mathrm{span}\{e_1,e_2\}$, $S=\{1\}$ → 합=0, untwisted 주장=4 (253이 양쪽 n에서
반례 자동발견 ✓ + 수정형은 모든 (L,S)에서 성립 ✓). **최종 확률은 무사**($J\mathbf 1_S\neq0$이면
충분 — $\Pr_L[w\in L]=1/(2^n+1)$은 벡터-불변). 본문엔 수정형+반례 명기.

## 3. ★ §6 SDA/Feldman 적용 — REJECT as stated, 정정 corollary로 대체

3중 결함:
1. **인덱싱 스왑**: 논문 SDA 정의(부분집합 크기 $\ge|\mathcal D|/d$)에서 "크기 $2^{n-t}$ 부분집합
   통제"가 주는 건 $\mathrm{SDA}\ge 2^t$이지 $2^{n-t}$가 아님. Kimi의 $t{=}0$ 주장(SDA$\ge2^n$)은
   **singleton 부분집합의 대각 상관**($\beta\gg\gamma$)이 즉시 반박(§7.3의 구체 수치도 동일 오류:
   γ=1107/1280 < diag=369/256).
2. **지수 대각의 VSTAT 잠식**: $\beta=(1+\tau)^{2n}-1$이 지수적으로 큼(블록 샘플의 χ²) →
   VSTAT 강도 $2^{n-t}/(6\beta)\ge1$ 조건이 $t\le c_p n-O(1)$, $c_p=1-2\log_2(1+\tau)$로 강제.
   p=1/4: $c_p\approx0.356$. **정직한 헤드라인 = $2^{0.356n}$-쿼리@상수 VSTAT**, "$\Omega(2^n)$
   achieved"는 over-claim.
3. **§6.1 카테고리 혼합**: bundle-제한 상관을 일반-쿼리 정리(thm:feldman)에 투입 — 제한 클래스
   하한은 별도 도구 필요. boxed 식 기각.

**정정 corollary(내 유도, 논문 spread-정리 패턴)**: $\gamma_t=2\beta2^{t-n}$로 모든 크기
$\ge2^{n-t}$ 부분집합 통제 → $\mathrm{SDA}\ge2^t$ → $q\ge2^t/3$ @ $\VSTAT(2^{n-t}/(6\beta))$;
유효범위 $t\le c_pn-O(1)$. cor:symplpn-sq로 본문 수록.

(경미: §4 "same sign and scale as prop:vmax" — 부호는 같으나 scale 다름((25/64)^n vs 4^{-n});
본문 미반영이라 기록만.)

## 4. 본문 반영 — 완료

§4 끝에 `subsec:symplpn-sq` 신설: **thm:symplpn-corr**(E.1+E.2 통합, σ-twist 수정 증명+반례)
+ OP1 상관-수준 답(unconstrained off-diag=0 대비) + **cor:symplpn-sq**(t-트레이드, $c_p$ 명시)
+ 두 formulation의 상보성 단락($2^n$ cap·$c_p$ haircut는 sympLPN 고유). abstract·기여 bullet 갱신.
빌드 ✓(306 KB, 에러 0).

## 5. staging

**S6 등록**(sympLPN 정확 상관 + SQ 하한). 누적 정리 5건(S1·S3·S4·S5·S6) — 전부 posture-불변,
batch 대기 유지.

## 6. 다음 (Kimi Track E)

1. E-노트 §6을 본문 cor:symplpn-sq 형태로 자체 정정(학습 목적; 본문은 이미 정정본).
2. 선택: $c_p$ 개선 시도 — per-block 대신 row-마진 SQ 모델(행 단위 샘플은 비독립이라 SQ 직접
   부적용; 정직한 우회 있는지) 또는 bundle-제한 클래스용 제한-SQ 차원 정리 인용 탐색(BFJ+94 류).
   실패해도 무방(현 결과 자체로 OP1 상관-수준 종결).

No closure; no break; no security claim. OPEN = LSN.

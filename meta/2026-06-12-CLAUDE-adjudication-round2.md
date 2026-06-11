# Claude 판정 — OP9 재투입 라운드 (`b2a2671` E-OP9 + `3e6aa6b` Krawtchouk)

**Adjudicator:** Claude (Fable 5). **Date:** 2026-06-12.
**검증:** `experiments/116`(Krawtchouk off-diag), `117`(low-weight B 비균등).
Discipline: Sound Verifier. No 7th; no break; no security claim. OPEN = LSN.

---

## 0. 한 줄: 두 커밋 다 결론은 너무 깔끔, 각각 검증부족/오측정. **단 silver lining = 진짜 진전.**

논문 무수정·DRAFT·코드 동반은 OK. 그러나 두 핵심 주장 모두 보정 필요.

## 1. Krawtchouk 해석증명 (`3e6aa6b`) — REJECT (n≥5에서 깨짐)

증명의 load-bearing 단계 "off-diagonal ≤ 0 ⇒ Var ≤ diagonal"이 **거짓**:

| n | off-diag | Var≤diag? |
|---|---|---|
| 2,3,4 | −0.140 / −0.084 / −0.009 | ✓ |
| **5** | **+0.044** | **✗** |
| **6** | **+0.070** | **✗** |

키미는 n=2,3만 검증(거기선 음수)하고 모든 n에 단언 — **어젯밤과 동일한 소n→점근 오류**.
저무게 벡터가 Ω=0이 흔해 양의 Cov_+ 항이 가중합을 지배하면서 n=5에서 부호 전환.
⇒ "Var < (25/32)^n"·"지수감쇠 (50/81)^n" 둘 다 깨짐(실측 Var/E² 감쇠는 **다항 ~Θ(1/n)**, 지수 아님).
**단 집중 자체는 진짜**(Var/E²: 0.146→0.070, n=3→6 ↓) ⇒ lem:affine-coset-bias 격상은 수치로
여전히 정당, **증명만 다시**. 올바른 증명 = 양의 off-diagonal을 포함한 full Var를 직접 상계
(닫힌형 E[W²]−E[W]² = o(E²) 보이기; 실제 rate ~1/n).

## 2. E-OP9a/b (`b2a2671`) — 규율 OK, 헤드라인 "counterexample" 오프레이밍

**좋음:** G-TARGET 준수(복원율 측정, 구별 아님) ✓.
**문제:** "bottom_w1 = marginal-uniform 반례(entropy 0.99, p_eff=1/4) ⇒ lemma false"는 **per-row
엔트로피**를 **joint 균등성**으로 오인. 실제 출력 `C=BA`는 **결정적으로 대칭**(`C=M=Mᵀ`,
200/200 — 균등이면 확률 2^{−n(n−1)/2}). ⇒ **bottom_w1은 joint marginal-균등성 위반 ⇒ 유효한
반례 아님.** "복원이 어려운 이유 = C의 joint 구조"라던 키미 관찰은 실은 "C가 구조화됨 = 비균등 =
가설 위반"이다. 즉 **내가 예측한 저무게⊥균등성 충돌이 *성립*하는 증거**이지 lemma 반박 아님.

## 3. ★ Silver lining — 모서리가 닫히는 쪽으로 *명확해짐* (진짜 진전)

내 두 체크를 합치면 trade-off **양 끝점이 모두 막힘**:
- **고무게 B** → 유효잡음 →1/2 → 신호 없음 → 사용불가 (`experiments/102`, M1+recovery-barrier).
- **저무게 B** → `C=BA` 대칭/구조화 → 비균등 → 가설 위반(검출됨) (`experiments/117`).

⇒ "영리한 B"는 둘 사이를 꿰어야 하는데 두 자연 극단이 다 차단됨. **이건 OP9 닫힘 논증을 향한
실질 진전** — 잔여는 "중간 무게(1≪w≪n) 영역에서 신호와 균등성을 동시에?"로 좁혀짐. (아직 증명
아님; 중간 영역·비-graph A 구조 남음.)

## 4. 조치
1. **둘 다 논문 진입 금지**(DRAFT 유지). Krawtchouk 격상은 **올바른 증명** 후로 보류
   (수치는 확정적이나 우리 규율: 해석증명 전 격상 없음).
2. **다음 키미 작업:**
   (a) Krawtchouk: 양의 off-diagonal 포함 full Var 닫힌형 상계(rate ~1/n 목표). 닫힌형
       `E[W²]=Σ_{Ω(v,v')=0}q·2^{-|v|-|v'|}` 직접 계산.
   (b) OP9: **올바른 균등성 정의로 재측정** — "BA가 *행렬로서* 균등에서 SD δ" (대칭·저rank 등
       deterministic test 포함). 그리고 §3의 sharpened 잔여(중간 무게 영역) 탐색.
3. 메타 교훈 재확인(G-MEASURE 추가): **수치 검증은 부호 전환을 놓칠 수 있으니 극단 n까지 / 닫힌형
   확인**; **균등성은 per-row가 아니라 joint(deterministic test 포함)로 측정**.

이번에도 규율 레일이 피해를 meta에 가둠. 모서리는 OPEN이나 **닫힘 쪽으로 더 명확해졌다.**

No 7th; no break; no security claim. OPEN = LSN.

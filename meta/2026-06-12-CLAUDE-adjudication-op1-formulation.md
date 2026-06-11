# Claude 판정 — Kimi OP1 formulation DRAFT (`13b296c`)

**Adjudicator:** Claude (Fable 5). **Date:** 2026-06-12.
**검증:** `experiments/163-CLAUDE-op1-formulation-check.py` (+json) — 우도비·σ²·상관곱·
baseline·등방행렬 개수 전부 재계산, 그리고 **batch 모델의 등방 off-diagonal 상관을 n=2,3
완전열거**.
Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

## 0. 한 줄: 기계는 ACCEPT(수학 전부 정확), 그러나 **batch 모델이 §4 추측을 거짓으로 만든다**(검증됨) → 단일표본 모델로 재정식화.

이건 "Kimi가 틀렸다"가 아니라 Step-1 formulation의 핵심 모델링 결정을 내가 조기 해소한 것.
DRAFT 자신이 §5에서 이 출구("different query class")를 명시 예고했다 — 그 예고가 옳았다.

## 1. 수학 검증 — 전부 PASS (`experiments/163`)

| 항목 | 판정 |
|---|---|
| 우도비 $\prod_i[1+(Ax)_i f(y_i)]$, $f(0)=-(1-2p)/(1-p)$·$f(1)=(1-2p)/p$ | ✓ 손계산 일치($(Ax)_i{=}1$일 때 비율 $p/(1-p)$·$(1-p)/p$) |
| $\E[f]=0$, $\sigma^2=(1-2p)^2/(p(1-p))$, $p{=}1/4{\Rightarrow}4/3$ | ✓ |
| 상관곱 $\E_{y|A}=\prod_i[1+\sigma^2(r_i{\cdot}x)(r_i{\cdot}x')]$ | ✓ 좌표별 전개 일치 |
| 비제약 baseline $(1+\sigma^2/4)^{2n}-1$, $p{=}1/4{\Rightarrow}(4/3)^{2n}$ | ✓ |
| 등방 full-rank 개수 90($n{=}2$)·22680($n{=}3$) | ✓ ($|\Lagr|\cdot|GL|$ 일치, 내 열거가 정확히 이 수) |

DRAFT의 모든 공식은 정확하다. (Kimi가 게이트—"감사 수치엔 유도/스크립트"—를 §7에 박은 것도 좋다.)

## 2. ★ 핵심 발견 — batch 모델 등방 상관은 억제되지 않는다 (n=2,3 완전열거)

DRAFT §4 추측: 등방 조건화가 off-diagonal 상관 $C_n(x,x')$을 $2^{\Theta(n)}$에서
$1+2^{-\Omega(n)}$로 억제하는가?

**완전열거 결과 (p=1/4, 모든 distinct 비영 쌍):**
| n | 비제약 baseline | 등방 off-diag $C_n$ | 억제율 |
|---|---|---|---|
| 2 | 3.160 | **2.975** | ×0.94 |
| 3 | 5.619 | **5.347** | ×0.95 |

등방은 **상수 ~5%만 깎고**, $C_n$은 $n$에 따라 **지수 증가**(2.975→5.347 ≈ baseline 추세).
부수 사실: off-diagonal이 **Hamming 거리와 무관**(모든 거리 동일값) — $\mathrm{Sp}(2n)$ 추이성과
정합. ⇒ **§4 추측은 batch 모델에서 결정적으로 거짓**.

## 3. 왜 이게 중요한가 (SQ 메커니즘 — 내 예측의 *이유*는 정밀화)

내가 처음 떠올린 직관("하드니스엔 상관이 지수적으로 작아야")은 **틀렸다** — 자기수정한다.
정확한 메커니즘은 VSTAT-허용오차다:
- 유용한 SQ 하한 = 평균 off-diagonal 상관 $\gamma$가 **작아야**(상수 이하) → Feldman이 $q\ge(2\alpha-1)d$를
  $\VSTAT(1/(3\gamma))$에서 줌. $\gamma$ 상수면 상수-허용오차 오라클 = 의미있는 $2^{\Omega(n)}$ 하한.
- **batch 모델**: $\gamma=C_n=2^{\Theta(n)}$ → $\VSTAT(2^{-\Theta(n)})$ = 지수적으로 미세한 허용오차
  = 학습자가 그냥 정밀 질의로 우회 = **하한 공허**. (등방이 5%만 깎아도 지수성은 그대로.)
- 참고: 표준 LPN 단일표본도 off-diag 상관 = $\sigma^2/4$ **상수**지만 그래서 SDA$=2^n$·$2^{\Omega(n)}$
  하한이 *나온다*. 멤버십-LSN은 한술 더 떠 $2^{-\Theta(n)}$(지수 감쇠)라 더 강하다.

⇒ batch 공허성은 **모델 인공물**이지 "sympLPN이 SQ-쉽다"가 아니다.

## 4. 재정식화 방향 (Step-1 revised) — 단일표본 모델

OP1의 올바른 표적: **예시 = 단일 잡음 내적** $(a,\,b{=}\langle a,x\rangle\oplus e)$, $a$ = 등방
$A$의 행 주변분포 $\mu_{\text{row}}$에서. 그러면
\[
\langle D_x,D_{x'}\rangle = \sigma^2\,\E_{a\sim\mu_{\text{row}}}[(a{\cdot}x)(a{\cdot}x')],
\]
**OP1 = "$\mu_{\text{row}}$가 LPN의 SQ 하한을 죽이지 않을 만큼 퍼져 있는가"**(= 조건화가
하드니스를 *줄이지* 않는가, 논문 OP1 표현 그대로)로 환원. 멤버십-LSN 기계(Krawtchouk
행-열 쌍대성)가 *여기서* 실제로 물린다(batch에선 안 물렸다).

**정직 주의 — 단일표본도 자명하진 않다:** 행들이 독립 표본이면 등방(전역 제약)이 표본별로
안 보여서 "그냥 비균등 행분포의 LPN"이 된다 — 결과가 약해질 수 있다(제약의 효과를 못 잡음).
*제약이 실제로 무는* 정식화(예: 비밀이 $x$+Lagrangian 결합, 또는 소수표본 묶음에서 $S_A{=}0$이
가시화되는 모델)를 찾는 게 OP1의 진짜 내용이다. 과약속 금지 — 이건 연구.

## 5. minor

DRAFT §2는 분포를 "등방행렬 $\{A:A^\top\Omega A=0\}$"(rank-deficient 포함)에서 뽑는다 하지만
§5 개수(90·22680)는 **full-rank만** 센다. sympLPN 정의(full-rank 등방=Lagrangian 기저)와
맞추려면 §2를 "full-rank 등방"으로 핀할 것. (내 열거도 full-rank 기준 — 90/22680 확인.)

## 6. 판정 + 다음

- **ACCEPT**: §1–§3 기계·공식(검증), §5–§7 가드·정직 framing.
- **REDIRECT**: §4 목표를 batch→단일표본(§4 above)으로. §5 minor 핀.
- (Kimi) Step-1 revised: 단일표본 sympLPN SQ 정식화 DRAFT + $\mu_{\text{row}}$ 정의(등방 $A$의
  행 주변분포) + $n{=}2,3$에서 단일표본 off-diag 상관 실측(코드+JSON; batch가 아니라 단일행).
  "제약이 무는가"의 모델 선택을 명시 토론. **본문 미반영**(연구 단계).
- (Claude) Step-2 판정 대기.

본문 무수정 ✓. No closure; no break; no security claim. OPEN = LSN.

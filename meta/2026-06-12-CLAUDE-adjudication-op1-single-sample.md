# Claude 판정 — Kimi OP1 single-sample DRAFT (`6f6ae83`)

**Adjudicator:** Claude (Fable 5). **Date:** 2026-06-12.
**검증:** `experiments/165-CLAUDE-op1-rowmarginal-check.py` (+json) — §5 row-marginal 추측을
$n=2,3$ 완전열거로 측정, §3 단일표본 상관공식 재계산.
Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

## 0. 한 줄: ACCEPT — redirect 정확·§3 공식 검증·§4 caveat 옳음. **§5 추측은 *거의* 맞음**(내가 닫힌형으로 정정). 단일행 모델은 settled(≈LPN) → 바로 Step 4(multi-row)로.

## 1. §3 단일표본 상관공식 — VERIFIED

$\langle D_x,D_{x'}\rangle = \sigma^2\,c_\mu(x,x')$ ($x\neq x'$), $c_\mu=\E_{a\sim\mu_{\text{row}}}[(a{\cdot}x)(a{\cdot}x')]$ —
batch DRAFT(`163`)에서 검증한 좌표별 전개의 단일표본판, 정확.

## 2. ★ §5 row-marginal 추측 — *거의* 맞음, 닫힌형으로 정정 (`165`, 완전열거)

Kimi 추측: "$\mu_{\text{row}}$는 $\F_2^n\setminus\{0\}$에서 균등." → **부분적으로 거짓**(0에 질량
있음), 그러나 Kimi가 "0에 점질량 있으면…"이라고 예고한 그 경우다. 정확한 구조:

\[
\boxed{\;\mu_{\text{row}} = \tfrac{1}{2^n+1}\cdot\delta_0 \;+\; \tfrac{2^n}{2^n+1}\cdot\mathrm{Unif}(\F_2^n\setminus\{0\})\;}
\]

- **0의 질량 $=1/(2^n+1)$** (n=2: 1/5=0.2 ✓, n=3: 1/9=0.111 ✓) — ★Krawtchouk의 멤버십
  확률 $\Pr[v\in\text{Lagrangian}]=1/(2^n+1)$과 **동일 상수**(zero row ⟺ $L$이 좌표 초평면에
  포함). 우리 기계와의 깔끔한 연결.
- **0 외엔 균등** (각 비영 $v$: n=2 4/15, n=3 8/63 — 완전열거 확인).
- 닫힌형 결과:
  \[
  c_\mu(x,x') = \frac{2^{2n-2}}{2^{2n}-1} = \tfrac14\bigl(1-2^{-2n}\bigr)^{-1} \to \tfrac14^{+},
  \qquad
  \langle D_x,D_x\rangle/\sigma^2 = \Pr[a{\cdot}x{=}1] = \frac{2^{2n-1}}{2^{2n}-1} \to \tfrac12^{+}.
  \]
  (n=2: $c_\mu{=}4/15{=}0.2667$, diag $8/15{=}0.5333$; n=3: $16/63{=}0.25397$, $32/63{=}0.5079$ —
  전부 완전열거와 일치.) **모든 쌍에서 상수**(Hamming 거리 무관, $\mathrm{Sp}$ 추이성).

## 3. 단일행 모델 = settled → Step 2/3a 불필요 (내가 했음)

$c_\mu\to 1/4^+$ 상수 $<1/2$ ⇒ off-diag 상관 $\sigma^2 c_\mu\to\sigma^2/4$ 상수 ⇒ **SDA $=2^{\Omega(n)}$
at $\VSTAT(\text{const})$** — 표준 LPN과 동일(편차는 $\Theta(2^{-2n})$, 지수적으로 작고 무해).
⇒ **"$S_A{=}0$ 조건화는 단일행 모델의 SD를 줄이지 않는다"** — OP1이 단일행 모델에선 **답해짐**.

**단 Kimi §4 caveat가 정확히 옳다:** 단일행은 전역 제약 $S_A{=}0$이 안 보여서 "비균등 $a$의
LPN"으로 환원 — **너무 약해서 진짜 OP1이 아니다**. Step 2/3a는 위 닫힌형으로 종료. **Step 4로
직행.**

## 4. ★ Step 4 방향 (multi-row bundle) — 진짜 OP1, 단 정직 주의

예시 = 같은 등방 $A$의 $k$개 행 $(a_1,b_1),\dots,(a_k,b_k)$. 핵심 통찰:

> **번들은 $k{=}1$(LPN, SDA 안전)과 $k{=}2n$(batch, `163`에서 공허) 사이를 보간한다.**
> 질문 = 어느 $k$에서 $S_A{=}0$의 행간 의존성이 상관을 (a) 통제 가능하게 유지하나(SD 보존,
> 진짜 결과) (b) batch처럼 폭발시키나(공허 벽 재도달, named obstruction).

**Step 4 구체 작업(코드+JSON, $n{=}2,3$, 작은 $k{=}2,3$):** 같은 $A$의 $k$행 결합분포에서
$k$-표본 off-diag 상관 측정 — $k$에 따른 성장 곡선. $k{=}1$(상수)→$k{=}2n$(지수) 전이 지점 탐색.

**정직 주의(과약속 금지·메모리 교훈):**
- **"공허 SDA ≠ sympLPN SQ-쉬움".** batch SDA 공허성(`163`)은 *증명기법/reference 선택*의
  한계지 sympLPN이 SQ-약하다는 게 아니다. 따라서 batch 벽 재도달도 "OP1 음성"이 아니라
  "이 reference로는 안 됨"의 named 정밀화다.
- sympLPN의 *자연* 표본은 batch다 — 단일/번들 모델은 SD를 *분석하기 위한* 대리이지 문제
  재정의가 아니다. 어느 모델이 sympLPN의 진짜 SD를 포착하는지 자체가 OP1의 일부.
- 세 결과 모두 진보: 번들이 통제됨(SD 보존 증명)·batch 벽 재도달(reference-bound obstruction)
  ·중간 전이 닫힌형(구조 결과) 전부 논문급 또는 sharpened-OP1.

## 5. 판정 + 다음

- **ACCEPT**: §1–§4 정식화·공식·caveat. §5는 위 닫힌형으로 정정(점질량 $1/(2^n+1)$).
- (Kimi) **Step 4 직행**: multi-row bundle $k{=}2,3$ 상관 성장 측정(코드+JSON), $k{=}1{\to}2n$
  전이. §4의 "secret-coupled $(x,L)$" 모델도 병행 후보(멤버십-LSN 기계 직접 연결). 위 정직
  주의 준수. **본문 미반영**(연구 단계).
- (Claude) Step 4 판정 대기.

본문 무수정 ✓. No closure; no break; no security claim. OPEN = LSN.

# Claude 판정 — Gemini-3.1-Pro lem:m2 구조 논증 (agy, 사용자 대화형 채널)

**Adjudicator:** Claude (Fable 5). **Date:** 2026-06-14. **맥락:** 방어적 암호분석(공개 출판·실제 표적 없음).
**대상:** Antigravity(Gemini 3.1 Pro High)가 낸 lem:m2 구조적 불가능성 논증(사용자가 터미널 대화형으로
받아 붙여넣음 — agy print 자동화는 Claude 백그라운드 환경에서 미작동, 사용자 TTY 채널이 대체).
**검증:** from-scratch(`experiments/543-CLAUDE-gemini-W0-spike-verification.py`).
Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

---

## 0. 한 줄

**Provable core ACCEPT(검증)·"닫는다" 부분 over-claim(내 catch: q_graph(n)→0).** Gemini 기여 =
W=0 스파이크의 **B-무관성** 명확화(우리가 라운드1/5에서 uniform-B 맥락으로만 본 q_graph가 사실
모든 marginal-uniform B의 provable 누설). 본문 open:marginal-adaptive에 sharpen(점근 한계 명시).
3-에이전트 협업 첫 실전: Gemini 관찰 → Claude 한계 catch → 코드 확정.

## 1. Gemini 논증 (요지)

탐지 invariant = min syndrome weight W=min_w wt(y+Cw). LSN reduction y=Cx+Be에서 **e∈Col(A)이면**
(e=Aw) Be=BAw=Cw → y=C(x+w)=codeword → W=0. Pr[e∈Col(A)]=상수(≥(1-p)^{2n}), B·R 무관.
real LPN은 Pr[W=0]≤2^n(1-p')^m→0. ⟹ SD≥Pr[e∈Col(A)], 모든 B에서. (HEURISTIC: e near Col(A)도
W 작음 → SD→1. 정직 caveat: linear만·non-linear은 OP7 conjecture.)

## 2. 검증 (543)

**(1) e∈Col(A)⟹W=0, B-무관**: n=2, 40개 random (L,A,**임의 B**,x)×전 e∈L = 160 케이스 전부
W=0 정확. 대수(Be=Cw, C=BA 결합법칙) 자명·B 무관 확인. ✓
**(2) Pr[e∈Col(A)]=q_graph(n)**: =Pr[e∈L]=29/64(n=2)·1241/4608(n=3) — q_graph와 정확 일치,
**noise prior만 의존(B 무관)**. ✓ (q_graph=Pr[Ax+e∈A]=Pr[e∈L], Ax∈L 항상이므로.)
**(3) real LPN Pr[W=0]**: m=80에서 ≤4e-10 negligible. ✓
⟹ **SD≥q_graph(n)−negl, 모든 marginal-uniform B**. provable core 성립.

## 3. ★ 내 catch — q_graph(n)→0

**Gemini가 놓친 결정적 사실**: q_graph(n) = 0.453(n2)→0.269(n3)→0.153(n4)→…→0.004(n10) **→0**.
따라서:
- THEOREM(provable)은 **고정 n 상수 하한** SD≥q_graph(n). 그 n에선 구분 가능(reduction 실패).
- **점근적으로 소멸** → lem:m2의 점근(n→∞) 버전(7th 핵심)을 **닫지 못함**.
- "SD→1"은 Gemini의 **HEURISTIC**(e near Col(A)) — 우리 라운드5 Track S의 *uniform-B* 정확
  결과와 일치하나 **일반 B 증명은 OPEN**.
- Gemini "closes the cell for linear"는 **고정-n 의미로만 맞음**·점근은 over-claim. 정직 caveat에
  linear/non-linear은 구분했으나 q_graph→0(점근 소멸)은 미언급 = 내 catch.

## 4. 가치 + 본문 반영

- **진짜 가치**: W=0 스파이크의 **B-무관성**. 우리는 라운드1(rank-member q-cap)·라운드5(uniform-B
  min-syndrome-weight)에서 q_graph를 *특정 전략* 맥락으로만 봄. Gemini가 그게 **reduction의 대수적
  강제(C=BA)에서 나오는 모든 marginal-uniform B의 provable 누설**임을 지적 — 본문 sharpen 가치.
- **본문(open:marginal-adaptive)**: "uniform-B 전략" 다음에 한 문장 추가 — 모든 marginal-uniform B는
  e∈Col(A)(prob q_graph, B-무관)에서 W=0 → rate≥q_graph(n) 누설(provable); **고정 n 상수 갭이나
  q_graph→0이라 점근 미부여**. 빌드 ✓(334 KB).

## 5. 메타 — 3-에이전트 협업

- **agy print 자동화 미작동**(Claude 백그라운드 TTY 부재; --model 문자열·버퍼링 복합) → 결론: agy는
  사용자 터미널 대화형 채널, 답을 Claude가 판정.
- **첫 실전 성공**: Gemini가 강한 관찰(B-무관)·정직 caveat(linear/non-linear) 냈으나 q_graph→0
  점근 한계는 놓침 → Claude 독립 판정이 정확히 catch. 강한 모델도 over-claim 있고 판정 레일 필수
  재확인.

## 6. 다음 (Kimi)

Gemini의 HEURISTIC(e near Col(A)→SD→1)을 **일반 marginal-uniform B로 정확 계산**: W 전체 분포
(W=0 스파이크 + e near Col(A)의 low-W 기여)가 일반 B에서 real LPN의 p'm 집중과 얼마나 벗어나는가.
uniform-B(라운드5)·λ-coupled(라운드6) 넘어 — q_graph 하한을 넘는 점근 SD 하한이 일반 B에서 나오면
lem:m2 점근에 진전. (단 ≈0 가능성·정직 음성결과도 가치.)

No closure; no break; no security claim. OPEN = LSN.

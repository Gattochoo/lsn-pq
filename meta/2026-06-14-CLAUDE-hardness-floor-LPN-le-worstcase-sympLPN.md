# Claude 아크 — hardness FLOOR: LPN ≤ worst-case sympLPN (첫 positive 앵커) + worst-to-avg와의 일관 lock + JJ 판정

**Adjudicator/Author:** Claude (Fable 5). **Date:** 2026-06-14. **맥락:** 방어적 암호분석(공개 출판·실제 표적 없음).
**동기:** (d-지위)로 가는 positive 결과 = trusted 문제(LPN)로부터의 hardness floor.
**산출물:** `experiments/853,854-CLAUDE-*.py` + Gemini-3.1-Pro(agy). **docs-drift 정정 포함.**
Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

---

## 0. 한 줄

**★LPN ≤ worst-case sympLPN을 PROVE (우리의 첫 positive 앵커).** zero-padding 임베딩: LPN 행렬을 등방 A_left=[A';0]로 심고(rows≤N이라 자동 등방) Lagrangian으로 완성, 비밀 s=(x;0), y=(y';noise) → sympLPN oracle이 x 복구. **단 average-case sympLPN으로 못 올림 — Lagrangian 무작위화가 직전 convolution obstruction(850–852)에 막힘.** 두 아크(floor↔worst-to-avg)가 **한 경계로 맞물림**: worst-case sympLPN≥LPN(floor), average≥worst는 worst-to-avg(막힘). +graph-Lagrangian 재구성(853): **average-case sympLPN ≡ [I;S] 구조 LPN**(S uniform symmetric). +JJ 판정: I=Θ(n) 독립 확증.

## 1. docs-drift 정정 (표적 바로잡음)

처음 floor 표적을 membership-LSN(def:lsn)으로 잡았으나 — **paper line 273: membership-LSN은 poly(n) 샘플로 정보이론적 안전 → floor가 cryptographically empty.** 올바른 표적 = **sympLPN(def:symplpn)**(공개 등방 A·비밀 x·y=Ax+e 디코딩, barrier가 다루는 객체). 세 객체 구분: membership-LSN(info-secure)·batch-LSN(=membership for uniform A)·sympLPN(decoding). floor는 sympLPN용.

## 2. ★ LPN ≤ worst-case sympLPN (THEOREM, Gemini 구성 + 854 검증)

**구성**(N≥m): LPN (A'∈F₂^{m×k}, y'=A'x+e'). A_left∈F₂^{2N×k}: top m rows=A', 나머지 0. **등방**(support가 position-half rows≤N라 symplectic partner=0 ⟹ ω=0). rank-k 등방 → Lagrangian A∈F₂^{2N×N}로 완성(항상 가능). s=(x;0_{N-k}), y=As+e=(A'x+e_top; e_bot). 환원은 y=(y'; fresh Bernoulli). **비밀이 (x;0)이므로 sympLPN oracle이 (x;0) 복구 → x.**
- **854 검증(n=2,3 exact brute-force)**: A_left 등방 ~100%, Lagrangian 완성 100%/100%, ML 복구 ~80%(소규모 LPN ML 한계 — 임베딩 결함 아님; **oracle은 정의상 (x;0) 반환이라 환원은 구성상 valid**).
- **판정 ACCEPT**: LPN ≤ worst-case sympLPN. **첫 positive 앵커** — worst-case sympLPN은 최소 LPN만큼 어려움. (Gemini의 N≥m/2는 N≥m으로 정정; 사소.)

## 3. ★ average-case는 막힘 (floor↔worst-to-avg 일관 lock)

worst-case 임베딩의 A는 **special(zero-padded) Lagrangian**. average-case sympLPN(uniform Lagrangian)이 hard라고만 가정하면 special→uniform 무작위화 필요 → g∈Sp 적용 → 노이즈 ge가 **convolution obstruction(850–852)**: W(g)=Θ(n)이라 보정 p'→1/2(신호 소멸). **그래서 average-case floor는 worst-to-avg와 정확히 같은 장벽에 막힘.** Gemini가 graph-Lagrangian 직접 착지도 차단(uniform A' LPN으로 y_top=x+e_top 생성 불가 — x 모름).

**일관 그림(coherent)**: sympLPN hardness 앵커는 **worst-case에 존재(LPN floor)**, average-case로 올리는 것 = worst-to-avg(막힘). 격자는 이 lift가 *작동*(Gaussian self-duality)해서 특별; sympLPN은 *막혀서* lattice-backbone 부재. 두 아크가 한 obstruction의 양면.

## 4. ★ graph-Lagrangian 재구성 (853, publishable 구조)

big Schubert cell Lagrangian = {(v,Sv):v}, S symmetric. basis A=[(e_i;Se_i)] ⟹ y=Ax+e: **y_top=x+e_top, y_bot=Sx+e_bot** = **[I;S] 구조 행렬 LPN**(2n 샘플, S symmetric). graph-cell=2^{n(n+1)/2}≈절반(n=2:8/15, n=3:64/135). ⟹ **average-case sympLPN ≡ [I;S]-LPN(S uniform symmetric)**. floor의 average-case 부분 = "[I;S]-구조 LPN이 uniform LPN만큼 hard?"로 환원(structured-LPN hardness 질문).

## 5. Track JJ 판정 (3de78a5) — ACCEPT, I=Θ(n) 확증

JJ: H(C_L·Be|HBe,C)=H(x|y,C) (**THEOREM**, y↦(C_L y,Hy) bijection+x uniform). uniform-B n=2: H가 m=2→7에 **1.86→1.72 수렴**(full-rank 조건부). ⟹ H(x|y,C)→~0.85n>0 → **I(x;y|C)→~0.15n=Θ(n)**(내 848/849 독립 확증). column-pair는 H를 1.90–1.93로 더 높게 유지(덜 누설, BB와 정합). full-rank 조건부라 내 646과 미세차(설명됨). 점근(H→n?) OPEN 정직.

## 6. (d-지위) 의미 + 다음

- **순 진전**: no-go(sympLPN⊀LPN linear) + **worst-case floor(LPN≤worst-case sympLPN)** → worst-case sympLPN은 ≥LPN이고 LPN으로 안 무너짐. **average-case 앵커가 유일한 gap(worst-to-avg 막힘).**
- 정직: crypto는 average-case라, worst-case floor는 **부분 앵커**. 완전 앵커엔 average-case floor 필요(막힘) or 새 경로.
- **남은 positive 후보**: [I;S]-구조 LPN hardness(853 환원), 또는 외부 stabilizer-LSN 다리(KLP+ floor 상속), 또는 non-linear no-go(OP2).
- **논문**: worst-case floor + graph-L 재구성 + worst-to-avg obstruction = 깔끔한 구조 묶음(Open Problem/Separation 절 후보). Kimi round-9(JJ✓, KK/LL 대기) 후 본문 반영.

No closure; no break; no security claim. OPEN = LSN.

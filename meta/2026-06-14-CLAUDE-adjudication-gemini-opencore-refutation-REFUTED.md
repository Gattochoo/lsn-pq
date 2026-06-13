# Claude 판정 — Gemini의 open-core "refutation"을 반박 (REFUTE the refutation)

**Adjudicator:** Claude (Fable 5). **Date:** 2026-06-14. **맥락:** 방어적 암호분석(공개 출판·실제 표적 없음).
**대상:** Gemini-3.1-Pro(agy) round-9 컨설팅 — open-core 명제 `H(u|s,C) ≥ n−o(n)`(u=C_L·Be, s=HBe)을 **REFUTE**하며 "단일블록 환원이 정보이론적으로 x를 손실없이 복구(I→n), no-go는 computational이어야"라고 주장.
**검증:** from-scratch(`rank(HB)≤n` 재확인, n=2 m=4,5,6 exhaustive) + 740.
Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

---

## 0. 한 줄

**Gemini의 refutation은 틀렸다 — 중심 단계가 `rank(HB)≤n`(문제의 정의적 confinement, 프롬프트에 명시·740 검증)을 정면 위반.** Gemini는 syndrome `s=HBe`를 `(m−n)`차원으로 취급(`H(s|C)≈m−n`)했으나 실제 `rank(HB)≤n`이라 `H(s|C)≤n`. syndrome은 e의 ~1.62n 엔트로피 중 **≤n비트만** 포착 → e를 over-determine 못함 → I↛n. 오히려 엔트로피 예산은 **I(x;y|C) ≤ 0.378n**(full-rank B; Gemini 자신의 round-8b 값과 일치)을 주는 **상한** = no-go 방향. open core(I=o(n) vs ≤0.378n)는 그대로 OPEN.

## 1. Gemini 주장의 구조

1. H(e)=2n·H₂(1/4)=1.622n.
2. H(e|s,C)=1.622n − H(s|C).
3. **"typical marginal-uniform B면 HB가 random (m−n)×2n처럼 행동 → s가 F₂^{m−n}서 거의 uniform → H(s|C)≈m−n."** ← **치명적 오류**.
4. data-processing: H(u|s,C) ≤ H(e|s,C) ≈ 1.622n−(m−n).
5. m≥2.622n이면 s가 e를 결정 → H(u|s,C)→0 → **I(x;y|C)=n−H(u|s,C)→n** → no-go 실패, computational이어야.

## 2. ★ 반박 — step 3가 `rank(HB)≤n`을 위반

**THEOREM (rank(HB)≤n).** H=C의 parity-check(HC=0). `HB·A = H·(BA) = H·C = 0` ⟹ Col(A)⊆ker(HB). A는 rank n ⟹ dim ker(HB)≥n ⟹ **rank(HB) ≤ 2n−n = n**. (깔끔; 740서 n=2 전수 검증.)

**수치 재확인** (n=2, uniform-B 400회):

| m | max rank(HB) (실제) | Gemini 주장 ~m−n |
|---|---|---|
| 4 | **2 (=n)** | 2 |
| 5 | **2 (=n)** | 3 |
| 6 | **2 (=n)** | 4 |

m이 커져도 rank(HB)는 n=2에 고정 — Gemini의 m−n은 m=6서 4라 명백히 틀림. **H는 C=BA에서 만들어져 `HB·A=0`이 강제됨 → H,B는 상관됨 → HB는 full-rank random이 아님.** Gemini는 이 상관(=confinement의 본질)을 무시.

**귀결.** `H(s|C) ≤ rank(HB) ≤ n` (s는 ≤n차원). 따라서:
- H(e|s,C) = 1.622n − H(s|C) ≥ 1.622n − n = **0.622n** (syndrome이 e를 over-determine 못함; Gemini의 "m≥2.622n서 e 결정"은 불가).
- I(x;y|C) = n − H(u|s,C). (u,s)↔Be(전단사, [C_L;H]가 가역) ⟹ H(u|s,C)=H(Be|C)−H(s|C) ≥ H(Be|C)−n. full-rank B면 H(Be|C)=H(e)=1.622n ⟹ H(u|s,C) ≥ 0.622n ⟹ **I(x;y|C) ≤ 0.378n** (상한, 정보이론).

## 3. 판정

- **Gemini refutation = INVALID.** 단일 오류(rank(HB) m−n 가정)가 결론(I→n)을 무너뜨림.
- **Gemini 자기모순:** round-8b 컨설팅선 같은 엔트로피 논증으로 **I≤0.38n**(맞음)을 냈는데, 이번엔 H(s|C)≈m−n으로 바꿔 **I→n**(틀림). 첫 답이 옳고 둘째가 오류 — 차이는 H(s|C)≤n vs m−n.
- **positive byproduct:** confinement `rank(HB)≤n`은 **I(x;y|C)≤0.378n**(full-rank B)이라는 깔끔한 정보이론 상한을 줌 → "환원이 lossless"라는 어떤 주장도 반박. no-go 방향 강화.
- **open core 불변:** I=o(n)인지 (0.378n까지) Θ(n)인지는 여전히 OPEN. lem:m1(heavy-row)이 0.378n→o(n)을 줄 도구. Gemini의 computational-shift 제안도 빗나감(HB는 rank≤n이라 generic LPN generator 아님).

## 4. 메타 — "Gemini 일 팍팍" 시킨 결과

사용자 요청대로 Gemini에 결정적 명제 증명을 강하게 요구 → Gemini가 **대담한 detailed refutation** 산출. 판정 레일이 **중심 오류 1개**(rank(HB) 가정)를 catch. 강한 모델일수록 정교하고 자신만만한 over-claim을 내며, 독립 판정 없이는 "I→n, no-go는 computational"이라는 틀린 결론을 받아들일 뻔. **이번 라운드 교훈: confinement(rank≤n)는 협상 불가 — syndrome은 ≤n차원, 이게 lem:m2의 심장.** Kimi 라운드-9(II–LL)가 이 confinement 위에서 H(u|s,C) 추세를 정확 계산 중.

No closure; no break; no security claim. OPEN = LSN.

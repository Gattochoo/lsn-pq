# Claude 판정 — Gemini Theorem 2는 (대체로) 옳다: I(x;y|C)=Θ(n) 증거, paper의 open-problem 프레임 정정 필요

**Adjudicator:** Claude (Fable 5). **Date:** 2026-06-14. **맥락:** 방어적 암호분석(공개 출판·실제 표적 없음).
**대상:** Gemini-3.1-Pro(agy) round-9 2차 답변 "Theorem 2 (Weight-1 Quotient Collapse)" — `I(x;y|C) ≈ 0.38n`이 **hard floor**(lem:m2 반박)라 주장. **검증:** `experiments/848-...conditional-bias.py`(직접 수치) + GG/646 재해석.
Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.
**★자기수정 포함: 내 이전 "conditional-bias gap" 의심과 GG "sublinear→lem:m2 지지" 프레임을 정정한다.**

---

## 0. 한 줄

**Gemini Theorem 2의 메커니즘은 실제로 성립한다 — 메시지 형식이 syndrome 조건부에서도 편향 유지(848 확증) → I(x;y|C)=Θ(n)(≈0.15n at n=2), o(n) 아님.** 내가 의심한 conditional-bias gap은 없었다(검증하니 bias~0.5 유지·m에 flat). **단 Gemini의 상수 0.38n은 과대**(실제 ~0.15n). **귀결: paper의 open:marginal-adaptive가 제시한 "prove I(x;y|C)=o(n)" 경로는 틀린 표적일 가능성 높음(답=NO).** **그러나 no-go(lem:m2=SD route)는 멀쩡** — I=Θ(n)은 비-LPN 구조의 부분누설이라 usable LPN reduction 안 됨. 결정적 미해결=n-scaling(LL track n=3,4).

## 1. Gemini Theorem 2 메커니즘 — 848로 확증 (내 의심 철회)

**주장:** full-rank B면 row(C_L B)⊕row(HB)=F₂^{2n}. weight-1 e_i = w_u+w_s(w_u∈row(C_L B), w_s∈row(HB)). 메시지 형식 `⟨w_u,e⟩ = e_i + ⟨w_s,e⟩`, ⟨w_s,e⟩는 s로 결정 → 조건부에서 `e_i + const` = bias 1−2p 유지 → u 편향 → Θ(n) 누설.

**내 초기 의심(틀림):** "e_i가 s=HBe에 얽혀 조건부 bias가 무조건부 1−2p와 다를 것(smoothing)."

**848 직접 계산(n=2, uniform-B 평균, m=4,5,6,7):**

| m | avg H(form\|s) | avg \|bias\| |
|---|---|---|
| 4 | 0.7257 | 0.5124 |
| 5 | 0.7239 | 0.5126 |
| 6 | 0.7230 | 0.5123 |
| 7 | 0.7233 | 0.5133 |

**메시지 형식은 조건부에서도 bias≈0.51(≈1−2p) 유지, m에 완전 flat — smoothing 없음.** H(form|s)≈0.72 < H₂(1/4)=0.81(오히려 약간 더 편향). **★내 gap 의심은 틀렸고 Gemini 메커니즘이 옳다.** 구조적 이유: syndrome rank가 **n에 갇힘**(rank(HB)≤n) → 2n개 잡음방향 중 ≤n개만 포착 → 나머지 메시지 방향은 편향 유지(m 무관, rank cap이 n이라).

## 2. 귀결: I(x;y|C)=Θ(n), o(n) 아님 (EVIDENCE/CONJECTURE)

메시지 좌표가 편향 유지 → H(u|s,C)<n by Ω(n) → **I(x;y|C)=n−H(u|s,C)=Θ(n)**.
**수치 재확인(n=2):** GG/646 I가 m에 따라 **수렴**(증분 감소: 0.054,0.059,0.051,0.036,…,0.015) → I_∞(n=2)≈**0.30 bit = 0.15n**. m에 sublinear(수렴)이나 **n에 Θ(n)**. 
- **Gemini 상수 0.38n = 과대**(실제 ~0.15n at n=2). Θ(n) **scaling**은 지지, 상수는 정정.
- **★GG "sublinear→lem:m2 지지" 프레임 정정:** GG의 "sublinear"는 **m**에 대한 수렴이지 n에 대한 o(n)이 아니다. GG는 EVIDENCE/OPEN으로 정직했으나, "I=o(n)"로 해석하면 틀림. recovery가 **부분적**(I<H(x))인 건 맞고 그게 no-go를 지지하나, "I=o(n)"은 별개·아마 거짓.

## 3. ★ no-go는 멀쩡 (over-correction 방지)

I=Θ(n)이 lem:m2를 깨는가? **아니다.**
- no-go = **SD((C,y), LPN_{p'})=1−o(1)** (출력이 LPN과 통계적으로 멂; BB/W-spike가 fixed-n서 SD→1 확증). I≠SD.
- I=Θ(n)은 **symplectic/graph 구조**의 부분누설 — LPN 구조 아님. **LPN oracle은 이걸 못 씀** → usable reduction 아님.
- 정보이론으로도 H(x|y,C)=H(u|s,C)≈0.84n>0 → 한 블록으론 x **완전복구 불가**(부분 Θ(n) 비트만). LPN 풂 아님.
- **결론: no-go INTACT.** I=Θ(n)은 no-go의 **경로**(I=o(n))를 죽일 뿐, no-go **자체**(SD route)는 건드리지 않음.

## 4. ★ paper 정정 권고 (LL 확인 후)

`open:marginal-adaptive`(line 1232)는 "prove I(x;y|C)=o(n) for typical C remains open"을 no-go 경로로 제시. **이 표적은 틀렸을 가능성 높음**(I=Θ(n)). **권고:** open problem을 **SD((C,y),LPN)=1−o(1)**(=lem:m2 proper)로 재정렬하고, "I=o(n)" 경로는 "likely false (message coords stay biased; I=Θ(n))"로 명시. **단 EVIDENCE(n=2)이므로 paper 수정은 LL(n=3,4)이 Θ(n) scaling 확인 후.** 지금 수정 안 함.

## 5. 메타 — "Gemini 팍팍"의 진짜 성과

1차 refutation(rank m−n)은 내가 격파. **2차(Theorem 2)는 내가 검증하니 옳았다** — Gemini가 paper의 open-problem 표적이 틀렸음을 발견. **판정 레일이 양방향 작동: Gemini over-claim도 잡고(상수 0.38n·rank 오류), Gemini의 옳은 통찰도 내 초기 의심을 누르고 인정.** 강한 모델을 강하게 굴리니 paper-급 발견(open problem 재정렬). **교훈: 의심도 검증 전엔 의심일 뿐 — 848 안 돌렸으면 Gemini를 부당하게 기각할 뻔.**

## 6. 다음 (Kimi round-9가 이미 조준)

- **LL(830, n=3,4)**: I(x;y|C)/n → const(Θ(n), Gemini) vs →0(o(n), paper)? **결정적.**
- **JJ(810)**: H(u|s,C) 정확 계산 → I=Θ(n) 직접 확인 + 상수.
- LL 확인되면 paper open:marginal-adaptive 재정렬(I=o(n)→SD route).

No closure; no break; no security claim. OPEN = LSN.

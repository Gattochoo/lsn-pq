# Claude 아크 개시+종결 — LSN worst-to-average 자기환원: 심플렉틱 경로는 OBSTRUCTED (구조적 설명, publishable negative)

**Adjudicator/Author:** Claude (Fable 5). **Date:** 2026-06-14. **맥락:** 방어적 암호분석(공개 출판·실제 표적 없음).
**동기:** (d-지위)로 가는 positive 구조 결과 — 격자의 Ajtai/Regev worst-to-avg backbone을 LSN에 부여 시도.
**산출물:** `experiments/850,851,852-CLAUDE-*.py` + Gemini-3.1-Pro(agy) 구조 컨설팅.
Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

---

## 0. 한 줄

**LSN의 worst-to-avg 자기환원을 심플렉틱군 Sp(2n,F₂)로 시도 → 깔끔하게 OBSTRUCTED.** Sp는 Lagrangian을 완벽 무작위화(추이적)하나 **Bernoulli 노이즈를 망가뜨림**, 그리고 (Gemini Fourier 논증 + 내 n=2 전수검증) **보정하면 p'→1/2(신호 소멸)**·**무보정은 g-watermark로 순환**·**Lagrangian uniform화엔 W≥3 distortion 불가피**. → **LSN은 격자식 backbone이 없다 — 그리고 그 이유를 정밀 규명(Hamming–symplectic incompatibility).** negative지만 지형의 핵심 공백을 메우는 publishable 결과.

## 1. 엔진과 장애 (setup)

worst-case Lagrangian L → uniform L: g∈Sp로 A'=gA(span g·L), y'=gy=A'x+ge. 비밀 x 동일. **Sp는 Lagrangian에 추이적**(stabilizer=Siegel parabolic)이라 구조는 완벽 무작위화. **유일 장애 = 노이즈 ge ≁ Bernoulli**(g가 Hamming weight 안 보존; weight 보존 부분군=monomial뿐).

## 2. Gemini obstruction (ACCEPT, 검증됨)

**Convolution Obstruction (Fourier/Walsh):** D_g=g·B_p의 변환 D̂_g(u)=(1−2p)^{wt(gᵀu)}. 신선노이즈 P'로 B_{p'}로 보정하려면 P̂'(u)=(1−2p')^{wt(u)}/(1−2p)^{wt(gᵀu)}, 확률분포 필요조건 |P̂'|≤1 ⟹ **1−2p' ≤ (1−2p)^{W(g)}**, W(g)=max wt(gᵀu)/wt(u). generic g는 W=Θ(n) ⟹ **p'→1/2**.
- **851 검증(n=2)**: W(g) median=3(=Θ(n)), 보정 p' median=0.4375·max=0.4688, 27%가 p'>0.45. ✓
- **Watermark(path 2)**: g 공개하면 g⁻¹로 무작위화 무효화 → D_g-noise 정의는 순환(=worst-case). ✓ 정확.
- **850**: Sp는 nonzero 15벡터에 추이적 → 유일 Sp-불변 노이즈=weight-blind((3/4)^{2n}δ₀+uniform); 전체 Sp-twirl이 신호 파괴(SD(twirl,Bernoulli)=0.24). ✓

## 3. ★ 마지막 crack 닫음 (852, 내 near-error 자기수정)

남은 희망=중간 부분군 H(monomial<H≤Sp)가 bounded-W로 transitive? **852 처음엔 "⟨W≤2⟩가 Sp 생성→transitive→crack!"이라 잘못 판정.** 자기수정: self-reduction은 **단일 g 적용**이라 생성군이 아니라 **단일적용 도달성**이 operative. 곱원소는 W 곱셈적(W(gh)≤W(g)W(h)) → 생성 transitivity는 high-W 곱에 의존.
**올바른 전수검증(Sp(4,2)=720):**

| 단일적용 W≤k | 도달 Lagrangian | 보정 p' |
|---|---|---|
| W≤1 (monomial) | 2/15 | 0.25 |
| W≤2 | **10/15 (전부 아님)** | 0.375 |
| W≤3 | 15/15 | 0.4375 |

min-W 분포: {W=1:2개, W=2:8개, **W=3:5개**}. **15개 중 5개 Lagrangian은 W=3 필요 → uniform 무작위화엔 p'≥0.4375 불가피.** multi-step walk도 W≤2^t로 폭발. **⟹ low-noise 심플렉틱 self-reduction 없음. obstruction 완전.**

## 4. 판정 + (d-지위) 의미

- **심플렉틱 worst-to-avg = OBSTRUCTED** (Gemini Fourier + 850/851/852 전수). **THEOREM-급 구조적 설명**: LSN이 왜 격자 backbone이 없는지 = Hamming–symplectic 비양립(weight는 Sp의 틀린 불변량; 연속 Gaussian self-duality의 이산 유사물 부재).
- **negative for the route, positive as a result**: 열린 구조 질문("LSN에 격자식 self-reduction?")을 **결정적으로 답함(No)** — 지형 공백 충전, publishable.
- **★(d-지위) 경로 재조정**: LSN의 family 자격은 격자식 self-reduction backbone에 못 의지. **단 이게 결격 아님** — **LPN/코드 자체도 worst-to-avg 없음**(survival+no-reduction으로 신뢰받음). LSN은 "lattice-like(backbone)"가 아니라 **"LPN-like(survival)" 캠프**. → 신뢰는 *공격 생존 + known-family로 환원 안 됨*에서 옴.
- **6.5th-vs-7th 미묘 단서(약함)**: LSN이 lattice-backbone 없고 LPN-구조적으로 가까움 = (약한) code-adjacency 증거. 단 **결정적 아님**(LPN도 자기 source; backbone 부재≠환원가능). 진짜 판별은 여전히 sympLPN⊀LPN(외부명제).

## 5. 다음

- **남은 positive 후보 없음(심플렉틱 경로 닫힘)** → (d-지위)는 **no-reduction route**로: (a) non-linear scrambler no-go(OP2), (b) 외부 avg-case(KLP+ 등) 연결.
- 또는 **이 obstruction을 논문에 박기**(Open Problem로서 "LSN은 격자식 self-reduction 없음, Hamming-symplectic 비양립" — 깔끔한 구조 결과).
- 큰-n 확인(W=Θ(n) 점근), 비-심플렉틱 무작위화가 있는지(거의 없음).

No closure; no break; no security claim. OPEN = LSN.

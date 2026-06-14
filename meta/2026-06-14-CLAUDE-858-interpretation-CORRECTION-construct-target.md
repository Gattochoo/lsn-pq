# Claude 자기정정 (3번째) — 858 lean 오해 교정 + 진짜 construct 표적 = light rows

**Author:** Claude (Fable 5). **Date:** 2026-06-14. **맥락:** 방어적 암호분석(공개 출판·실제 표적 없음).
**대상:** 858/493454c의 "lem:m2가 거짓일 수도" lean. **방법:** 깊은 재추론(comparison/case 분석). 규율: EVIDENCE/OPEN, over-claim 금지.
Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

## 0. 한 줄
**858의 "lem:m2 거짓 lean"은 오해 — 정정.** ①858은 uniform-B를 **matched LPN_{p_eff}**와 비교했으나 lem:m2는 **usable p'(1−2p'≥1/poly)**에 대한 것. uniform-B 출력 노이즈율 **p_eff→1/2**(lem:m1 heavy rows)이라 usable 저노이즈 LPN과 **멂**(W~m/2 vs p'·m) → **lem:m2는 uniform-B서 성립**(matched-p_eff 구별불가는 *unsolvable 고노이즈 LPN*일 뿐, usable 환원 아님). ②uniform-B = **easy case**; 진짜 open = **o(m)개 light rows**(lem:m1 허용, bias≥2^{−0.19n} 유계=usable). **858 data(W-law가 matched-p_eff vs n에서 decay)는 맞으나 lem:m2와 무관**(틀린 비교·틀린 case). lem:m2 OPEN 유지.

## 1. 정정 논리
- **lem:m2(thm:marginal-adaptive) statement**: SD((C,y), LPN_{p'})=1−o(1) for every p' with 1−2p'≥1/poly(n). ⟹ **usable p'(저노이즈)** 기준.
- **uniform-B 출력**: Be (e≠0서) = uniform over F_2^m (균일 B, 행 독립); e=0서 0. ⟹ 노이즈 = (3/4)^{2n}·δ_0 + (1−(3/4)^{2n})·Uniform, 주변율 p_eff=(1−(3/4)^{2n})/2→1/2.
- **vs usable LPN_{p'}**: 출력 노이즈 weight ≈ p_eff·m ≈ m/2, LPN_{p'} weight = p'·m, p'≤1/2−1/poly. gap=(p_eff−p')·m ≥ (1/poly)·m → ∞. **SD→1.** ⟹ **lem:m2 성립(uniform-B).** (858의 matched-p_eff 비교는 다른·쉬운 비교; lem:m2 아님.)
- **858 재해석**: W-law가 matched-p_eff vs n에서 decay = p_eff→1/2로 LPN이 균일화 = **easy case의 점근**. 진짜 open case 아님.

## 2. ★진짜 construct 표적 (light rows)
lem:m2 open = **marginal-adaptive B = g(A,R), BA uniform, but o(m)개 light rows**(weight ≤0.19n). light row b_i: ⟨b_i,e⟩ bias=(1−2p)^{wt}≥2^{−0.19n} **유계**(소멸 안 함) = **usable 저노이즈 좌표**. paper open:marginal-adaptive: "low-weight rows that vary with A evade per-instance bound (∪_A R_w(A) may cover F_2^n)".
- **construct(lem:m2 거짓 방향)**: light rows를 배치해 **usable LPN sub-instance**(poly(n) 저노이즈 좌표, 일관된 secret x) 형성 + BA uniform 유지. 성공=sympLPN→LPN 선형환원=LSN 6.5th(major).
- **obstruction(lem:m2 성립 방향)**: light rows가 BA uniform 유지하며 *일관된* usable LPN을 못 만든다(A마다 light row가 변해 secret 정렬 안 됨 = frame-alignment류). = lem:m2.
- **이게 진짜 열린 칸**; 858(uniform-B)은 여기 안 닿음.

## 3. 규율 (세 번째 정정)
이번 세션 정정 3회: Θ(n)(proxy), floor(search/decisional), 858(틀린 비교/case). **공통: directional lean을 comparison·case 정밀분석 전에 선언.** 교훈 강화: **lean도 주장이다 — 비교 대상(usable p' vs matched p_eff)과 case(uniform vs light-rows)를 먼저 확정.** 858 data는 보존(맞음), 해석만 정정. paper 무변경(lem:m2 conditional/OPEN 그대로).

## 4. 다음
- construct를 **light-rows case**로 재조준: 작은 n서 light-row B(BA uniform 강제)가 usable LPN sub-instance 만드는지 정확 탐색. obstruction(frame-alignment)이 막는지.
- 이게 lem:m2의 진짜 crux; uniform-B 탐색은 종료.

No closure; no break; no security claim. OPEN = LSN.

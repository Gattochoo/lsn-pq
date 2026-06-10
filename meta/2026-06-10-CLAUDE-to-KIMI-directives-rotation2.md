# Claude → Kimi: 지시서 — Rotation 2 (목표: 선형 환원 완전 폐쇄 정리)

**From:** Claude (Fable 5, supervisor). **To:** Kimi (executor). **Date:** 2026-06-10.
**Discipline:** Sound Verifier. No 7th; no break; no security claim. OPEN = LSN.
**전제:** Rotation 1 전체 마감(§1~§5, 판정 기록들 + `868a7c2`까지). 재논쟁 금지 목록 유지.

---

## §0. 왜 이 표적인가 — 1회전 산출물이 만든 기회

1회전이 쌓은 세 조각 — **D.1 pin**(고정 B의 엔트로피 결핍, m ≥ cn 전부) + **D.2 quantifier
pin**(비밀-B 모델: BA의 marginal만 중요) + **lem:affine-coset-bias**(라벨측 통제) — 을 조합하면
다음이 사정권입니다:

> **목표 정리 (A3b-FINAL, "선형 폐쇄"):** 상수잡음 p=1/4에서, sympLPN→LPN의 모든 선형 환원
> (고정/랜덤/적응 B, 모든 m=poly(n))은 실패한다 — 출력 행렬이 균등에 가깝지 않거나(고정 B),
> 가깝다면 라벨 잡음이 Shannon-사망한다(모든 B).

이것이 성립하면 LPQR이 "believe it should be possible for any m=poly(n)"이라고만 했던 것을
**우리가 증명**하는 것 — 프로젝트 최대급 사내 정리입니다. 두 조각 모두 제가 산술 수준에서
사전 검증했습니다(아래). **주의: "완전 폐쇄"는 두 조각이 모두 정리로 선 뒤에만 사용 가능한
어휘입니다 — 그 전엔 "target theorem".**

## §1. 우선순위 1 — A3b-FINAL, 두 조각

### 1a. 명제 (고정-B 전멸): D.1 + Fannes — 거의 공짜

- **내용:** D.1(pinned): 고정 B, m ≥ cn ⇒ `H(BA) ≤ (1−d)mn` (d→1/4, Lane C 실측).
  Fannes–Audenaert 연속성: `H(U)−H(P) ≤ T·mn + H₂(T)` (T = SD) ⇒ **`SD(BA, uniform) ≥ d − 1/(mn)`
  — 상수(≈1/4)-거리, 모든 m ≥ cn, 모든 rank.** 분포-사상 요건(BA ≈ uniform, D.2 모델과 동일
  요건) 위반 ⇒ 고정-B 환원은 rank 무관·m 무관 전멸. 검증 산술: n=41,m=82에서 SD ≥ 0.2497.
- **의의:** mid-rank 띠가 m ≥ cn에서 **이 명제로 닫힙니다**(층화 정리는 구성적 탐지기로서의
  가치를 유지 — 명시적 distinguisher vs Fannes의 비구성적 거리 — 이 구분을 본문에 한 문장).
- **작업:** Fannes 부등식의 정확한 형(상수, H₂(T) 항) 인용 pin(표준 교과서/논문) + 명제 작성.
  d의 출처는 D.1(상수 존재) + Lane C(d→1/4는 실측 라벨로). m < cn 모서리는 정직하게 제외.
- **합격선:** Fannes 인용 정확; "constant statistical distance"의 상수를 d로 명시; 과장 금지.

### 1b. 정리 (비밀/임의-B): 저무게-도달 계수 논증 — 핵심 신규

- **아이디어 (사전 검증된 스케치 — 형식화하라, 재발명 말 것):**
  임의의 B(랜덤·적응·결정적 모두)와 임의 행 i에 대해, 출력 행 `c_i = b_iᵀA`가 **저무게 해를
  갖는 c들의 집합** `R_w = {c : ∃b, |b| ≤ w, bᵀA = c}`는 **A와 무관하게**
  `|R_w| ≤ Σ_{j≤w} C(2n,j)`. w = 0.19n이면 `|R_w|/2^n ≤ 2^{−Θ(n)}` (n=64에서 1.4×10⁻³,
  n=128에서 1.1×10⁻⁵ — 산술 검증 완료).
  ⇒ BA가 균등에 δ-가깝면, 대부분 행에서 `c_i ∉ R_w` ⇒ **`|b_i| > 0.19n` 강제** ⇒ 라벨 잡음
  비트의 bias ≤ `(1−2p)^{0.19n} = 2^{−0.19n}` (piling-up) ⇒ x 복원에 `m ≥ n·2^{0.38n}` 필요
  ⇒ **poly-m 선형 환원 사망 — B의 분포·적응성 전혀 무관.**
- **작업 순서:**
  1. 도달집합 보조정리(`|R_w| ≤ Σ C(2n,j)` — A-무관·결정적) + "δ-균등 ⇒ 행 질량
     ≤ |R_w|/2^n + δ" 마무리(행별 marginal로 환원; 적응 B의 joint 처리 주의 — first-moment
     + Markov, 필요하면 행 union bound).
  2. bias→복원 표본수 하한(per-bit bias β ⇒ m ≥ Ω(n/β²)) — 표준; 정확 진술로.
  3. 조립: 정리 statement + 정직 caveat(점근 정리 — n=8,16에선 상수 약함(질량 6.6%, 8.4%);
     모델 = 분포-사상(D.2와 동일); p 상수(piling-up); "LPN-비균등-약속 솔버" 대상 환원은
     정의상 제외).
  4. **수치 검증 필수 커밋:** n=8..16에서 실제 R_w 크기(전수/샘플링)와 binomial bound 대조 +
     랜덤 균등-출력 B에서 강제 무게 분포 실측.
- **합격선:** 적응-B의 확률 bookkeeping이 정확할 것(내가 재유도함); 상수 0.19n의 출처
  (H₂⁻¹) 명시; "complete closure" 어휘는 1a+1b 둘 다 선 후 §1c에서만.

### 1c. 조립 — "선형 지형 최종장"

1a+1b 성립 시: coverage 표 최종형(고정-B: D.1+Fannes 전멸 / BA≈균등 임의-B: 계수 정리 전멸 /
구성적 탐지기: 층화 정리, ρ>(3/2+ε)n) + abstract·intro 한 문장 갱신("we close the linear-
reduction landscape at constant noise") + Open Problems에서 해당 항목 제거·격하. **이 단계는
내 재판정 통과 후에만.**

## §2. 우선순위 2 — barriers 절 통합 패스

유기적으로 자란 절(transport 정리들 + lemma + B-visibility + coverage)을 단일 "Linear-reduction
landscape" 소절로 재조직: 모델 라벨 일관화(public-B/secret-B), 표 1개로 수렴, 중복 서술 제거.
§1 마감 후 실행(그 결과를 반영해야 하므로).

## §3. 소형 작업 (병렬 가능)

1. **A5 n-스케일링:** δ/(m·κ·2^{−n}) 적합상수(0.7–0.9)가 n에 평탄한지 — n=4(2295개, 기존
   코드)와 n=5를 m·2^{−n} 정렬로 비교. 코드+표 커밋. 평탄하면 메타노트에 "scaling-consistent"
   기록(논문 승격은 보류).
2. **Krawtchouk 집중 추측 → PARK:** §1b 계수 논증이 폐쇄 목적상 이를 대체(우월). 노트에
   "subsumed by counting for closure purposes; standalone interest only" 한 줄.
3. **Bridge → PARK:** 등록된 open problem 유지. 이번 회전 신규 작업 없음.

## §4. 게이트 (불변 — 요약)

모델 정의 먼저 · 모든 수치에 코드 · 모든 인용에 verbatim pin · tex 커밋에 PDF · 본문에 내부
참조 금지 · 극값 주장엔 최적화 probe · "완전 폐쇄/closure" 어휘는 §1c 전 사용 금지 ·
재논쟁 금지 목록 유지.

## §5. 보고

1a → 1b → (내 판정) → 1c → §2 순. 각 조각 = 한 커밋 + 짧은 보고. 막히면 options-doc.

```text
기대 산출: 고정-B 전멸 명제(1a) + 임의-B 계수 정리(1b) → 선형 지형 완전 폐쇄(1c)
          + barriers 절 통합 + A5 스케일링 표. 실패 모드조차 출판급 정밀화.
          7th 지위는 불변 — 이것은 LSN⊀LPN의 '선형' 층을 증명으로 완성하는 일이다.
```

No 7th; no break; no security claim. OPEN = LSN.

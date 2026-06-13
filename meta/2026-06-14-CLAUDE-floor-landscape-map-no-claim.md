# Claude 탐구 (no-claim map) — decisional floor 지형도: batch-LSN floor는 막힘, 유일 thread = LPN≤sympLPN via LPQR26 (미검증)

**Author:** Claude (Fable 5). **Date:** 2026-06-14. **맥락:** 방어적 암호분석(공개 출판·실제 표적 없음).
**모드:** 탐구/매핑(다음 타겟). **floor over-claim(4c6aed4) 직후라 claim 없이 지형만 매핑.** Gemini-3.1-Pro(agy) 컨설팅 + Claude 판정.
Discipline: Sound Verifier. No closure; no break; no security claim. OPEN = LSN.

---

## 0. 한 줄

**batch-LSN(crypto 객체)의 decisional hardness floor는 세 경로 모두 막힘/불만족** — 근본 = **discriminative(멤버십) vs generative(디코딩) type-gulf**. **유일하게 살아있는 thread = `LPN ≤ sympLPN(k=n)` via LPQR26(미검증 EVIDENCE)** — sympLPN의 앵커지 batch-LSN 아님. 외부 논문 확인이 다음 액션. **아무 floor도 주장 안 함.**

## 1. 5 객체 (재확인)

1. LPN (uniform A', decisional, trusted-hard).
2. THEIR stabilizer-LSN (KLP+/LPQR26): public [A|B], junk x, secret logical y. **LPN ≤ THEIR-LSN (외부, decisional, k=1).**
3. sympLPN(k=n) (def:symplpn): public isotropic A, secret x, y=Ax+e. (single-instance search **underdetermined**, 855.)
4. membership-LSN: secret Lagrangian, **poly-sample info-secure(floor empty)**.
5. batch-LSN: public A, secret Lagrangian, 멤버십 라벨. uniform-A ≡ membership; crypto=pseudorandom A.

## 2. 지형도 판정 (Gemini map + 내 over-label 교정)

**P1. THEIR-LSN ≤ batch-LSN** (LPN floor 상속 시도). Gemini: FUNDAMENTALLY OBSTRUCTED(THEOREM).
- **내 교정**: **over-label.** 단일샘플 info-budget(O(n) bits vs n²-dim L)은 맞으나 **다중샘플은 O(mn) bits로 벗어남**(m>n이면 n² 초과). 다중샘플 장애=frame-alignment("정렬하려면 이미 THEIR-LSN 풀어야")는 **CONJECTURE**(Gemini도 "we conjecture"). paper도 "natural map만 막음"이라 함. → **OBSTRUCTED지만 CONJECTURE-급**, impossibility 아님.

**P2. sympLPN ≤ batch-LSN.** Gemini: OBSTRUCTED(type mismatch).
- **generative(Ax+e 벡터) vs discriminative(1_L(a)+e 멤버십비트) gulf** — 벡터 오라클을 boolean property-testing으로 환원하려면 L을 알아야 → 지수손실. **이 구조 gulf는 정확(내 동의).**
- ★**부산물(미검증)**: Gemini recall "LPQR26의 LPN≤THEIR-LSN가 sympLPN(k=n)을 isotropic embedding으로 커버 → **LPN ≤ sympLPN decisional floor 유효**." **EVIDENCE only** — sympLPN(secret x)과 THEIR-LSN(secret logical y)이 def상 달라(line 238) 자동 아님. **검증 필요.**

**P3. 직접 LPN ≤ batch-LSN (pseudorandom A).** Gemini: ACHIEVABLE(severe caveats).
- uniform A → 멤버십 라벨 ~0 (info-secure 차단, THEOREM 맞음). → floor는 **PRG gap 안에만** 존재: LPN-derived L에 상관된 A를 PRG로 생성, uniform과 구별불가 유지하며 라벨 embed. **proves PRG hardness, not batch-LSN 구조 hardness** — 구조 앵커로는 **공허**.

## 3. 종합 (honest, no-claim)

- **batch-LSN decisional floor = 세 경로 다 막힘/공허.** 근본 = **type-gulf**(membership-discriminative vs decoding-generative). Gemini의 이 framing은 통찰적이고 정확.
- **유일 live thread = `LPN ≤ sympLPN(k=n)` via LPQR26** (P2 부산물). 이건 **sympLPN의 decisional 앵커**(batch-LSN 아님). **미검증** — 다음 액션 = LPQR26/KLP+ 정독해 sympLPN(k=n)이 그들 floor에 포함되는지 확인. 포함되면: sympLPN은 ≥LPN(decisional, 외부) + ⊀LPN(우리 no-go) = sympLPN의 (d-지위) 부분앵커. (단 sympLPN≠batch-LSN, bridge 여전히 open.)
- **내 zero-padding floor(853/854)와의 관계**: 그건 search-only·약함(855). LPQR26 floor(있다면)가 진짜(decisional)·외부. 내 것 재발명 아니라 보완(우리 formulation서 직접 search 구성 보임).

## 4. 다음

- **검증 (claim 전)**: LPQR26 §(LPN≤their-LSN)이 sympLPN(k=n) 커버하는가? = 외부 논문 정독 or 정밀 구조 대조. ★유일 live 앵커 thread.
- type-gulf(P2)를 Separation으로 논문에 박기 후보(membership vs decoding 객체 분리는 이미 paper에 floor로 있음).
- consolidate(round-9 LL + I=Θ(n) 본문) 먼저(사용자 합의), 그다음 이 thread.

No closure; no break; no security claim. OPEN = LSN.
